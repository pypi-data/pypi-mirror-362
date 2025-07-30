# SPDX-FileCopyrightText: 2025 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import logging
import os
import subprocess
import threading
import xml.etree.ElementTree as ET
from enum import Enum
from io import FileIO
from pathlib import PurePath
from shutil import which
from xml.etree.ElementTree import Element

from tgclients import TextgridCrud, TextgridCrudException
from tgclients.databinding import MetadataContainerType
from tgclients.databinding import Object as TextgridObject
from xsdata.exceptions import ConverterWarning, ParserError

from .imex import Imex
from .utils import (
    NAMESPACES,
    PARSER,
    PC_NAMESPACES,
    RDF_RESOURCE,
    base_uri_from,
    is_aggregation,
    is_allowed_in_project_root,
    is_edition,
    is_portalconfig,
    is_readme,
    is_xml,
)

log = logging.getLogger(__name__)

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


class ImportStatus:
    """Keeps track of progress when uploading objects."""

    class Status(Enum):
        """Possible status of the import job."""

        RUNNING = 1
        FAILED = 2
        FINISHED = 3

    def __init__(self, imex: Imex):
        self._imex = imex
        self._total = len(self._imex.map)
        self._current: str = 'none'  # the tguri currently working on
        self._current_status: ImportStatus.Status = ImportStatus.Status.RUNNING
        self._current_message: str = 'nothing going on yet'
        self._progress_file_name = self._imex.location.parent / '.progress'
        self._progress_file: FileIO | None = None
        self._progress: list = []

    @property
    def total(self) -> int:
        """Total number of files to upload.

        Returns:
            int: total of files to upload
        """
        return self._total

    @property
    def current(self) -> str:
        """TextGridUri of object currently uploaded.

        Returns:
            str: TextGridUri of object currently uploaded
        """
        return self._current

    @property
    def completed(self) -> int:
        """Number of files already uploaded.

        Returns:
            int: number if files uploaded
        """
        return len(self._progress)

    @property
    def message(self) -> str:
        """Current status message.

        Returns:
            str: status message
        """
        return self._current_message

    @property
    def status(self):
        """Current status.

        Returns enum of type ImportStatus.Status.

        Returns:
            ImportStatus.Status: status
        """
        return self._current_status

    @property
    def imex(self) -> Imex:
        """The imex object of this upload job.

        Returns:
            Imex: imex object of thibs upload
        """
        return self._imex

    def _upload_started(self, tguri: str, message: str):
        self._current = tguri
        self._current_message = message
        # self._current_status = ImportStatus.Status.RUNNING

    def _upload_finished(self, tguri: str):
        if not self._progress_file:
            self._progress_file = open(self._progress_file_name, 'w')

        self._progress_file.write(f'{tguri}\n')
        self._progress.append(tguri)

        if len(self._imex.map) == len(self._progress):
            self._progress_file.close()
            os.remove(self._progress_file_name)
            self._progress_file = None
            self._current = 'none'
            self._current_message = 'finished'
            self._current_status = ImportStatus.Status.FINISHED
        else:
            self._current = 'none'
            self._current_message = 'nothing going on right now'

    def _upload_error(self, message):
        self._current_message = message
        self._current_status = ImportStatus.Status.FAILED


class TGimport:
    """Class to take care of importing and updating textgrid objects from disk."""

    # pylint: disable=logging-fstring-interpolation

    def __init__(
        self,
        sid: str,
        crud: TextgridCrud,
        ignore_warnings: bool = False,
        project_id: str = '',
        imex_location: str = '',
        initial: bool = False,
        new_revision: bool = False,
        data_only: bool = False,
        link_rewriter: str = 'linkrewriter-cli',
        resume: bool = False,
    ) -> None:
        """Import an TextGrid aggregation (or collection or edition).

        Also able to import portalconfig and README.md, which may be on top level.

        Args:
            sid (str): sessionId
            crud (TextgridCrud): tgcrud
            ignore_warnings (bool): wether to continue in case of warnings
            project_id (str, optional): project id. Defaults to "" because not needed on updates, only for create
            imex_location(str, optional): imex file to use for update. not needed for initial import, will be created then
            initial(bool, optional): initial import, do not read existing imex files and create new uris
            new_revision(bool, optional): wether to create a new revision
            data_only(bool, optional): only update data, use online metadata
            link_rewriter(str, optional): location of linkrewriter-cli binary
            resume(bool, optional): wether to resume an old import process
        """
        self._sid: str = sid
        self._project_id: str = project_id
        self._crud: TextgridCrud = crud
        self._ignore_warnings: bool = ignore_warnings
        self._imex = Imex(imex_file_path=imex_location, new=initial)
        self._new_objects: set = set()  # we collect every new object (without uri) here
        self._new_revision = new_revision
        self._data_only = data_only
        self._link_rewriter = self._find_linkrewriter(link_rewriter)
        self._import_status: ImportStatus
        self._resume = resume

    @staticmethod
    def _find_linkrewriter(executable_name: str) -> str | None:
        """Find linkrewriter binary with given name in path (or at ./).

        Args:
            executable_name (str): name of linkrewriter executable to locate in path

        Returns:
            str | None: full path to link rewriter binary or None if none found
        """
        log.info(f'searching for link-rewriter in path, proposal is "{executable_name}"')
        lr = which(executable_name)
        if not lr:
            log.info(f'did not find global, trying local "./{executable_name}"')
            lr = which('./' + executable_name)
        log.info(f'setting path for linkrewriter-cli: {lr}')
        return lr

    def upload(self, filenames: list[str], threaded: bool = False) -> ImportStatus:
        """Import or update given filenames recursively in(to) textgrid repository.

        First file will be used for imex location with [filename].imex, if not given.

        Args:
            filenames (list[str]): list of files on disk.
            threaded (bool): run upload itself in background thread, you will have to
                             check for yourself with help of the returned status object
                             whether the job is done.

        Returns:
            ImportStatus: status object with the state of the upload
        """
        if self._resume:
            raise TextgridImportException(
                'Resume not yet implemented, check https://gitlab.gwdg.de/dariah-de/textgridrep/tgadmin/-/issues/27 for progress'
            )

        # do we need to look for new files, or do we just update with imex
        if len(filenames) > 0:
            self.collect_filenames_to_imex(filenames)
            self._imex.write_file()

        self._import_status = ImportStatus(self._imex)

        if threaded:
            thread = threading.Thread(target=self._upload_objects_threaded)
            thread.start()
        else:
            self._upload_objects()

        return self._import_status

    def _upload_objects_threaded(self):
        try:
            self._upload_objects()
        except TextgridImportException as error:
            self._import_status._upload_error(error)

    def _upload_objects(self):
        """Iterate through aggregations, rewrite aggs, xml and portalconfig and upload data."""
        for path, tguri in self._imex.items:
            # the metadata on disk
            md_local = metafile_to_object(path)

            # update or create new?
            if not self._is_create(path):
                log.info('update, reading online metadata')
                md_online = self._crud.read_metadata(tguri, self._sid)
                # rev uri, because we may have base uris, but metadata will have latest rev
                revision_uri = md_online.object_value.generic.generated.textgrid_uri.value
                if not self._data_only:
                    # we take generated from online object, as tgcrud wants to check last-modified,
                    # and will not keep anything from lokal generated block anyway
                    log.info('updating with local metadata')
                    md_local.generic.generated = md_online.object_value.generic.generated
                    metadata = md_local
                else:
                    log.info('ignoring local metadata and using online metadata. data only upload.')
                    metadata = md_online.object_value
            else:
                metadata = md_local
                revision_uri = ''

            if self.is_rewriteable_file(metadata):
                log.info(f'rewriting {path}')
                self._import_status._upload_started(tguri, 'rewrite and upload')
                self._rewrite_and_upload(path, metadata, revision_uri)
            else:
                log.info(f'uploading {path}')
                self._import_status._upload_started(tguri, 'upload')
                self._upload_file(path, metadata, revision_uri)

            self._import_status._upload_finished(tguri)

    def is_rewriteable_file(self, metadata: TextgridObject) -> bool:
        """Decide wether the file is rewriteable (Exchange paths with textgrid URIs).

        Decision is based on mimetype and existance of linkrewriter-cli.
        Rewrite of aggregations will fall back to builtin, portalconfig will
        always be rewritten by builtin and existance of linkrewriter-cli
        will also allow XML rewrite.

        Args:
            metadata (TextgridObject): metadata to decide rewriteability for

        Returns:
            bool: true if file with given metadata shall be rewritten
        """
        if self._link_rewriter:
            return is_aggregation(metadata) or is_portalconfig(metadata) or is_xml(metadata)
        else:
            return is_aggregation(metadata) or is_portalconfig(metadata)

    def _is_create(self, path: PurePath) -> bool:
        """Is the object with given path is already created in Textgrid?

        Decide with the help of self._new_objects list.

        Args:
            path (PurePath): path to file

        Returns:
            bool: true if path is in list of _new_objects
        """
        return path in self._new_objects

    def _rewrite_and_upload(
        self, path: PurePath, metadata: TextgridObject, revision_uri: str = ''
    ) -> str:
        """Use ./linkrewriter-cli to rewrite links in file.

        Uses URIs and paths from IMEX.

        Args:
            path (PurePath): path to file to rewrite and upload
            metadata (TextgridObject): metadata of file to upload
            revision_uri(str, optional): uri of last revision, needed in case of updates

        Returns:
            str: textgrid uri of uploaded file
        """
        tguri = self._imex.get(path)

        # rewrite data
        if is_portalconfig(metadata):
            data = self._rewrite_portalconfig_file(path)
        elif self._link_rewriter:
            data = self._rewrite_with_linkrewriter_cli(path, metadata)
        else:
            data = self._rewrite_with_python(path, metadata)

        # rewrite metadata for editions
        if is_edition(metadata):
            work_path = PurePath(path.parent, metadata.edition.is_edition_of)
            metadata.edition.is_edition_of = self._imex.get(work_path)

        try:
            mdcont = MetadataContainerType()
            mdcont.object_value = metadata

            if self._is_create(path):
                log.info(f'uploading modified file {path.name} with uri: {tguri}')
                res = self._crud.create_resource(
                    self._sid, self._project_id, data, mdcont, uri=tguri
                )
            else:
                log.info(f'uploading modified file {path.name} with uri: {tguri}')
                res = self._crud.update_resource(
                    self._sid,
                    revision_uri,
                    data,
                    mdcont,
                    create_revision=self._new_revision,
                )
            handle_crud_warnings(res, path, self._ignore_warnings)
        except TextgridCrudException as error:
            handle_crud_exception(error, self._sid, self._project_id, path)
        return res.object_value.generic.generated.textgrid_uri.value

    def _rewrite_with_linkrewriter_cli(self, path: PurePath, metadata: TextgridObject) -> str:
        """Rewrite object with linkrewriter-cli (aggregations and tei).

        Args:
            path (PurePath): path to object
            metadata (TextgridObject): metadata for object

        Returns:
            str: content of file after rewrite
        """
        if is_aggregation(metadata):
            spec = f'{__location__}/linkrewrite-specs/textgrid.xml'
        else:
            spec = f'{__location__}/linkrewrite-specs/tei.xml'

        base = self._imex.get_basepath(path).as_posix() + '/'
        imex_loc = self._imex.location.as_posix()

        log.info(
            f'running: {self._link_rewriter} -c {spec} -i {imex_loc} -b {base} {path.as_posix()}'
        )
        result = subprocess.run(
            [
                self._link_rewriter,
                '-c',
                spec,
                '-i',
                imex_loc,
                '-b',
                base,
                path.as_posix(),
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        return result.stdout

    def _rewrite_with_python(self, path: PurePath, metadata: TextgridObject) -> str:
        """Rewrite object with python (only aggregations).

        Args:
            path (PurePath): path to object
            metadata (TextgridObject): metadata for object

        Returns:
            str: content of file after rewrite
        """
        path_prefix = self._imex.path_prefix
        agg_xml = ET.parse(path)
        agg_xml_root = agg_xml.getroot()
        for ore_aggregates in agg_xml_root.findall('.//ore:aggregates', NAMESPACES):
            # TODO: put this call for finding key to Imex class and write tests.
            #       also check if get_relpath_for() is really useful
            tguri = self._imex.get(
                PurePath(
                    path_prefix.as_posix()
                    + '/'
                    + self._imex.get_basepath(path).as_posix()
                    + '/'
                    + self._imex.get_relpath_for(
                        path_prefix / PurePath(ore_aggregates.attrib[RDF_RESOURCE])
                    ).as_posix()
                )
            )
            ore_aggregates.set(RDF_RESOURCE, base_uri_from(tguri))

        data_str = ET.tostring(agg_xml_root, encoding='utf8', method='xml')
        return data_str

    def _rewrite_portalconfig_file(self, portalconfig_file: PurePath) -> str:
        """Rewrite portalconfig - exchange paths with textgrid URIs.

        This is done for avatar and xslt locations.

        Args:
            portalconfig_file (PurePath): path to file

        Returns:
            str: rewritten portalconfig xml
        """
        data_path = portalconfig_file.parent
        parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
        the_dataXML = ET.parse(portalconfig_file, parser).getroot()

        # modify avatar element
        avatar_location = the_dataXML.find('pc:avatar', PC_NAMESPACES)
        self._check_path_and_rewrite(data_path, avatar_location)
        # optionally modify xslt element
        xslt_tag = the_dataXML.find('pc:xslt', PC_NAMESPACES)
        if xslt_tag:
            # look into each tag (only <html> as of now) and rewrite locations
            for html_xslt_location in xslt_tag.findall('pc:html', PC_NAMESPACES):
                self._check_path_and_rewrite(data_path, html_xslt_location)

        data_str = ET.tostring(the_dataXML, encoding='utf8', method='xml')
        return data_str

    def _check_path_and_rewrite(self, data_path: PurePath, element: Element):
        """Check if the path referenced in 'element' is already contained in imex.

        Exchange element content if so, fail if not

        Args:
            data_path (PurePath): path to object
            element (Element): XML Element

        Raises:
            TextgridImportException: if element not contained IMEX
        """
        path = PurePath(data_path / element.text)
        if self._imex.has(path):
            element.text = self._imex.get(path)
        else:
            message = f"'{element.text}' is referenced in portalconfig, but not found in import. Did you forget to add a collection with additional assets?"
            if not self._ignore_warnings:
                raise TextgridImportException(message)
            else:
                log.warning(f'{message} - but ignore warnings is enabled')

    def _upload_file(self, path: PurePath, metadata: TextgridObject, revision_uri: str = '') -> str:
        """Upload file.

        Args:
            path (PurePath): path of file to upload
            metadata (TextgridObject): metadata of file to upload
            revision_uri(str, optional): uri of last revision, needed in case of updates

        Raises:
            TextgridImportException: in case of error

        Returns:
            str: textgrid uri of uploaded file
        """
        tguri = self._imex.get(path)
        try:
            with open(path, 'rb') as the_data:
                # tgcrud wants a MetadataContainerType, see https://gitlab.gwdg.de/dariah-de/textgridrep/textgrid-python-clients/-/issues/76
                mdcont = MetadataContainerType()
                mdcont.object_value = metadata

                if self._is_create(path):
                    log.info(f'uploading file {path.name} with uri: {tguri}')
                    res = self._crud.create_resource(
                        self._sid, self._project_id, the_data.read(), mdcont, uri=tguri
                    )
                else:
                    log.info(f'uploading file {path.name} with uri: {tguri}')
                    res = self._crud.update_resource(
                        self._sid,
                        revision_uri,
                        the_data.read(),
                        mdcont,
                        create_revision=self._new_revision,
                    )
                handle_crud_warnings(res, path.name, self._ignore_warnings)

                return res.object_value.generic.generated.textgrid_uri.value
                # imex_map[data_path] = tguri
                # return tguri
        except FileNotFoundError:
            raise TextgridImportException(f"File '{data_path}' not found")
        except TextgridCrudException as error:
            handle_crud_exception(error, self._sid, self._project_id, path)
        return ''

    def collect_filenames_to_imex(self, filenames: list[str]) -> str:
        """Collect filenames referenced in on disk aggregation files.

        Creates IMEX file and already gets textgrid URIS for each file.
        The IMEX file will be located next to the first filename mentioned and
        be named like to file with an .imex suffix.

        Args:
            filenames (list[str]): lsit of aggregation files and/or portalconfgi/readme

        Raises:
            TextgridImportException: in case of error

        Returns:
            str: textgridUri of first filename from list
        """
        for filename in filenames:
            filepath = PurePath(filename)
            meta = metafile_to_object(filepath, referenced_in=filename)
            if not is_allowed_in_project_root(meta):
                raise TextgridImportException(f"File '{filename}' is not of type aggregation")

            if is_aggregation(meta):
                self._collect_aggregation_contents(filepath, meta)

            if is_portalconfig(meta):
                # portalconfig needs to go after avatar img / xslt upload for uri rewrite
                self._add_object_if_new(filepath)
            elif is_readme(meta):
                self._add_object_if_new(filepath)

        # we need to decide wether to append to existing imex or create new, and if there are new objects in path
        if len(self._new_objects) > 0:
            all_uris = self._crud.get_uri(self._sid, len(self._new_objects))
            self._imex.add_all(dict(zip(self._new_objects, all_uris)))

        return self._imex.get(PurePath(filenames[0]))

    def _add_object_if_new(self, filepath: PurePath):
        """Add object to new_objects list if not found in imex.

        Args:
            filepath (PurePath): path to object

        Returns:
            boolean: True if object is new, False otherwise
        """
        log.debug(f'checking {filepath}: {self._imex.has(filepath)}')
        if not self._imex.has(filepath):
            self._new_objects.add(filepath)
            return True
        else:
            return False

    def _collect_aggregation_contents(self, agg_data_path: PurePath, agg_meta: TextgridObject):
        """Recursively go through the aggregation file and add all found files to all_objects.

        Works mentioned in editions will also be added to all_objects

        Args:
            agg_data_path (PurePath): path to aggregation
            agg_meta (TextgridObject): textgrid metadata of aggregation
        """
        # if aggregation is edition then upload related work object
        if is_edition(agg_meta):
            assert agg_meta.edition is not None
            assert agg_meta.edition.is_edition_of is not None
            work_path = PurePath(agg_data_path.parent, agg_meta.edition.is_edition_of)
            self._add_object_if_new(work_path)
        agg_xml = ET.parse(agg_data_path)
        agg_xml_root = agg_xml.getroot()

        for ore_aggregates in agg_xml_root.findall('.//ore:aggregates', NAMESPACES):
            data_path = PurePath(agg_data_path.parent, ore_aggregates.attrib[RDF_RESOURCE])
            meta = metafile_to_object(
                data_path, referenced_in=agg_data_path.name
            )  # TODO: only use purepath
            if is_aggregation(meta):
                self._collect_aggregation_contents(data_path, meta)
            else:
                self._add_object_if_new(data_path)

        self._add_object_if_new(agg_data_path)


###
# some methods from old tgimport
###
def metafile_to_object(filename: PurePath, referenced_in: str = '') -> TextgridObject:
    metafile_path = PurePath(f'{filename}.meta')
    try:
        with open(metafile_path, 'rb') as meta_file:
            try:
                meta: TextgridObject = PARSER.parse(meta_file, TextgridObject)
            except ParserError:  # try parsing again as metadatacontainertype
                meta_file.seek(0)  # rewind
                metadata: MetadataContainerType = PARSER.parse(meta_file, MetadataContainerType)
                meta = metadata.object_value
        return meta
    except FileNotFoundError:
        if filename == referenced_in:
            raise TextgridImportException(
                f"File '{filename}.meta' not found, which belongs to '{filename}'"
            )
        else:
            raise TextgridImportException(
                f"File '{filename}.meta' not found, which belongs to '{filename}' and is referenced in '{referenced_in}'"
            )
    except ConverterWarning as warning:
        # TODO ConverterWarning is not thrown, only shown
        raise TextgridImportException(f'xsdata found a problem: {warning}')

    except ParserError as error:
        raise TextgridImportException(f'xsdata found a problem: {error} in file "{filename}"')


def handle_crud_warnings(res, filename, ignore_warnings):
    for crudwarn in res.object_value.generic.generated.warning:
        log.warning(f' ⚠️ Warning from tgcrud for {filename}: {crudwarn}')
    if len(res.object_value.generic.generated.warning) > 0 and not ignore_warnings:
        raise TextgridImportException(
            'Stopped import. Please fix your input or try again with --ignore-warnings'
        )


def handle_crud_exception(error, sid, project_id, filename):
    # TODO: we can check both here, if sessionid is valid, and if project is existing and accessible, for better feedback
    # tgrud should also communicate the cause
    # error mapping
    # * 404 - project not existing
    # * 401 - sessionid invalid
    # * 500 - something went terribly wrong (invalid metadata)

    msg = f"""
        tgcrud responded with an error uploading '{filename}'
        to project '{project_id}'
        with sessionid starting...ending with '{sid[0:3]}...{sid[-3:]}'

        """
    if '404' in str(error):
        msg += 'Are you sure the project ID exists?'
    elif '401' in str(error):
        msg += 'Possibly the SESSION_ID is invalid'
    elif '500' in str(error):
        msg += f"""A problem on tgcrud side - is you metadata valid?
        Please check {filename}.meta"""
    else:
        msg += f'new error code found'

    msg += f"""

        ----
        Error message from tgcrud:
        {error}
    """

    raise TextgridImportException(msg)


class TextgridImportException(Exception):
    """Exception thrown by tgimport module."""
