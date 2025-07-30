# SPDX-FileCopyrightText: 2024 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import logging
from pathlib import Path, PurePath
from xml.dom.minidom import parse

from jinja2 import Template

log = logging.getLogger(__name__)


IMEX_TEMPLATE = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<importSpec xmlns="http://textgrid.info/import">
  {%- for path, tguri in imex.items() %}
  <importObject textgrid-uri="{{tguri}}" local-data="{{calc_relative_path(filename, path)}}"/>
  {%- endfor %}
</importSpec>
"""


class Imex:
    """The imex object shall keep track of the mapping of local files paths to TextGrid URIs.

    * It shall provide functions for serializing the imex as xml or find references.
    * It shall also keep track of relative paths between the imex file location and
      the referenced objects.

    TODOs:
        * possibly use databinding?
            https://gitlab.gwdg.de/dariah-de/textgridrep/link-rewriter/-/blob/develop/src/main/xsd/textgrid-import-2010.xsd
    """

    def __init__(self, imex_file_path, imex_map: dict = {}, new: bool = False) -> None:
        self._imex_map: dict = imex_map
        self._location: PurePath = PurePath(imex_file_path)
        self._path_prefix: PurePath = PurePath(imex_file_path).parent

        log.info(f'setting imex loc to {self._location}')

        if not new and imex_file_path and Path(imex_file_path).is_file():
            # initialize from file, if existing
            log.info(f'reading imex from {imex_file_path}')
            self._read_file(imex_file_path=imex_file_path)

    @property
    def map(self):
        return self._imex_map

    @property
    def items(self):
        return self._imex_map.items()

    def has(self, key) -> bool:
        return key in self._imex_map

    def get(self, key) -> str:
        return self._imex_map[key]

    def add(self, path, textgrid_uri):
        self._imex_map[path] = textgrid_uri

    def add_all(self, path_uri_map: dict):
        for path, key in path_uri_map.items():
            self.add(path, key)

    @property
    def location(self) -> PurePath:
        return self._location

    @property
    def path_prefix(self) -> PurePath:
        return self._path_prefix

    def _read_file(self, imex_file_path: str):
        """Read an .imex file.

        Args:
            imex_file_path (str): _description_
        """
        log.info(f'reading imex file from {imex_file_path}')
        # we take the dir where the imex file is located as base, as every path mentioned shall be relative to this file
        imex_xml = parse(imex_file_path)
        for import_object in imex_xml.getElementsByTagName('importObject'):
            textgrid_uri = import_object.getAttribute('textgrid-uri')
            path = PurePath(self._path_prefix / import_object.getAttribute('local-data'))
            self._imex_map[path] = textgrid_uri

    def print_imex(self):
        template = Template(IMEX_TEMPLATE)
        template.globals.update(calc_relative_path=Imex.calc_relative_path)
        xml = template.render(imex=self._imex_map, filename=self._location)
        print(xml)

    def print_map(self):
        print(self._imex_map)
        for path, uri in self._imex_map.items():
            print(f'uri: {uri} - path: {path}')

    def write_file(self, location: PurePath | None = None):
        """Write an .imex file which keeps track of local filenames and their related textgrid uris.

        This is useful for reimporting the data with the same uris (or new revisions of them).
        """
        if not location:
            location = self._location
        log.info(f'writing imex file to {location}')
        template = Template(IMEX_TEMPLATE)
        template.globals.update(calc_relative_path=Imex.calc_relative_path)
        xml = template.render(imex=self._imex_map, filename=location)
        with open(location, 'w') as file:
            file.write(xml)

    def get_basepath(self, file: PurePath) -> PurePath:
        """Calculate the location of a file relative to the imex file location.

        Useful e.g. for setting linkrewriter base.

        Args:
            file (PurePath): location of file

        Returns:
            PurePath: relative path element
        """
        return file.parent.relative_to(self._location.parent)

    def get_relpath_for(self, path: PurePath) -> Path:
        """Get path for object with path relative to imex location.

        Args:
            path (PurePath): path to object

        Returns:
            Path: relative path to object
        """
        return self.calc_relative_path(self._location.as_posix(), path.as_posix())

    @staticmethod
    def calc_relative_path(filename: str, path: str) -> Path:
        """Find the path of 'path' relative to 'filename'.

        this could possibly be solved with walk_up=true from python 3.12 on
        https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.relative_to
        """
        return Path(path).resolve().relative_to(Path(filename).parent.resolve())
