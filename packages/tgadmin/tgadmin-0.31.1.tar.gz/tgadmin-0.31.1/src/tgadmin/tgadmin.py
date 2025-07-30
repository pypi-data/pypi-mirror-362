# SPDX-FileCopyrightText: 2024 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import logging
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path, PurePath

import rich_click as click
from rich import box
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeRemainingColumn,
)
from rich.table import Column, Table

# from rich.pretty import pprint
from tgclients import (
    TextgridAuth,
    TextgridConfig,
    TextgridCrud,
    TextgridCrudException,
    TextgridCrudRequest,
    TextgridMetadata,
    TextgridPublish,
    TextgridSearch,
)
from tgclients.config import DEV_SERVER, PROD_SERVER, TEST_SERVER
from tgclients.databinding import MetadataContainerType
from tgclients.databinding.tgpublish.tgpub import ProcessStatusType, PublishResponse
from tgclients.utils import Utils

from . import __version__
from .imex import Imex
from .tgimport import (
    ImportStatus,
    TextgridImportException,
    TGimport,
    metafile_to_object,
)
from .utils import (
    imex_to_path_dict,
    is_collection,
    is_edition,
    is_portalconfig,
    is_readme,
    rewrite_portalconfig_string,
    serialize_metadata,
    write_imex,
)

log = logging.getLogger(__name__)

# we only want one instance of console, see https://rich.readthedocs.io/en/stable/console.html
console = Console()


class TGclient:
    """Class to configure tgclients with server url from server and keep the SID."""

    def __init__(self, sid, server, verbose):
        # TODO: init on demand, otherwise every call will create a soap client etc
        self.sid = sid
        self.config = TextgridConfig(server)
        self.tgauth = TextgridAuth(self.config)
        self.tgsearch = TextgridSearch(self.config, nonpublic=True)
        self.crud_req = TextgridCrudRequest(self.config)
        self.crud = TextgridCrud(self.config)
        self.publish = TextgridPublish(self.config)
        self.verbose = verbose

        if verbose:
            log_level = logging.INFO
        else:
            log_level = logging.WARN
        logging.basicConfig(
            level=log_level,
            format='%(message)s',
            datefmt='[%X]',
            handlers=[RichHandler(show_path=False)],
        )


pass_tgclient = click.make_pass_decorator(TGclient)


@click.group()
@click.version_option(__version__)
@click.option(
    '-s',
    '--sid',
    default=lambda: os.environ.get('TEXTGRID_SID', ''),
    required=True,
    help='A textgrid session ID. Defaults to environment variable TEXTGRID_SID',
)
@click.option(
    '--server',
    default=PROD_SERVER,
    help='the server to use, defaults to ' + PROD_SERVER,
)
@click.option('--dev', is_flag=True, help='use development system: ' + DEV_SERVER)
@click.option('--test', is_flag=True, help='use test system: ' + TEST_SERVER)
@click.option('--verbose', is_flag=True, help='verbose')
@click.pass_context
def cli(ctx, sid, server, dev, test, verbose):
    """Helper cli tool to list or create TextGrid projects."""
    if dev and test:
        console.print('you have to decide, dev or test ;-)')
        sys.exit(0)

    authz = 'textgrid-esx2.gwdg.de'
    if dev:
        server = DEV_SERVER
        authz = 'textgrid-esx1.gwdg.de'

    if test:
        server = TEST_SERVER
        authz = 'test.textgridlab.org'

    if sid == '':
        exit_with_error(
            f"""Please provide a textgrid session ID. Get one from
            {server}/1.0/Shibboleth.sso/Login?target=/1.0/secure/TextGrid-WebAuth.php?authZinstance={authz}
            and add with '--sid' or provide environment parameter TEXTGRID_SID
            In BASH: export TEXTGRID_SID=YOURSESSION-ID
            In Windows Powershell: $env:TEXTGRID_SID="YOURSESSION-ID"
            """
        )

    ctx.obj = TGclient(sid, server, verbose)


@cli.command('list')
@click.option('--urls', 'as_urls', help='list projects as urls for staging server', is_flag=True)
@pass_tgclient
def list_projects(client, as_urls):
    """List existing projects."""
    projects = client.tgauth.list_assigned_projects(client.sid)

    for project_id in projects:
        desc = client.tgauth.get_project_description(project_id)
        if as_urls:
            console.print(f'https://test.textgridrep.org/project/{project_id} : {desc.name}')
        else:
            console.print(f'{project_id} : {desc.name}')


@cli.command()
@click.option('-d', '--description', help='project description')
@click.argument('name')
@pass_tgclient
def create(client, name, description):
    """Create new project with name "name"."""
    project_id = client.tgauth.create_project(client.sid, name, description)
    console.print(f'created new project with ID: {project_id}')


def complete_project_ids(ctx, param, incomplete):
    """Autocompletion helper for project IDs."""
    params = ctx.parent.params
    sid = params['sid']
    if sid == '':
        return

    if params['dev']:
        server = DEV_SERVER
    elif params['test']:
        server = TEST_SERVER
    else:
        server = params['server']
    config = TextgridConfig(server)
    tgauth = TextgridAuth(config)
    projects = tgauth.list_assigned_projects(sid)
    return [k for k in projects if k.startswith(incomplete)]


@cli.command()
@click.option('--name', help='name to look for')
@click.option('--mail', help='email to look for')
@click.option('--org', help='organisation to look for')
@pass_tgclient
def find_user(client, name, mail, org):
    """Search for users by name, email and/or organisation."""
    if not (name or mail or org):
        console.print(
            'Please specify at least one property you want to look for: name, mail or organisation.'
        )
        sys.exit(1)
    res = client.tgauth.get_ids(client.sid, name=name, mail=mail, organisation=org)

    table = Table(
        Column(header='ePPN', justify='right', style='cyan'),
        'Name',
        'E-Mail',
        'Organisation',
        box=box.MINIMAL,
    )

    keys = ['ePPN', 'name', 'mail', 'organisation']
    for entry in res:
        table.add_row(*[entry[key] for key in keys])

    console.print(table)


@cli.command()
@click.argument('project_id', shell_complete=complete_project_ids)
@click.argument('eppn')
@click.option('--admin', is_flag=True, help='as admin')
@click.option('--manager', is_flag=True, help='as manager')
@click.option('--editor', is_flag=True, help='as editor')
@click.option('--observer', is_flag=True, help='as observer')
@pass_tgclient
def add_role(
    client, project_id: str, eppn: str, admin: bool, manager: bool, editor: bool, observer: bool
):
    """Add role(s) for person identified by eppn to project."""
    if not (admin or manager or editor or observer):
        console.print(f'Please specify at least one role you want {eppn} to have in {project_id}')
        sys.exit(1)

    if admin:
        client.tgauth.add_admin_to_project(client.sid, project_id, eppn)
    if manager:
        client.tgauth.add_manager_to_project(client.sid, project_id, eppn)
    if editor:
        client.tgauth.add_editor_to_project(client.sid, project_id, eppn)
    if observer:
        client.tgauth.add_observer_to_project(client.sid, project_id, eppn)

    print_project_members(client, project_id)


@cli.command()
@click.argument('project_id', shell_complete=complete_project_ids)
@click.argument('eppn')
@click.option('--admin', is_flag=True, help='as admin')
@click.option('--manager', is_flag=True, help='as manager')
@click.option('--editor', is_flag=True, help='as editor')
@click.option('--observer', is_flag=True, help='as observer')
@pass_tgclient
def remove_role(
    client, project_id: str, eppn: str, admin: bool, manager: bool, editor: bool, observer: bool
):
    """Remove role(s) for person identified by eppn from project."""
    if not (admin or manager or editor or observer):
        console.print(f'Please specify at least one role you want {eppn} to lose in {project_id}')
        sys.exit(1)

    if admin:
        client.tgauth.remove_admin_from_project(client.sid, project_id, eppn)
    if manager:
        client.tgauth.remove_manager_from_project(client.sid, project_id, eppn)
    if editor:
        client.tgauth.remove_editor_from_project(client.sid, project_id, eppn)
    if observer:
        client.tgauth.remove_observer_from_project(client.sid, project_id, eppn)

    print_project_members(client, project_id)


@cli.command()
@click.argument('project_id', shell_complete=complete_project_ids)
@pass_tgclient
def show_members(client, project_id):
    """Show project members."""
    res = client.tgauth.get_project_description(project_id)
    console.print(f'\nProject: {res["name"]}\nDescription: {res["description"]}\n')
    print_project_members(client, project_id)


def print_project_members(client, project_id):
    """Show roles of users in projects in a tabular form."""
    res = client.tgauth._client.service.getUserRole(
        auth=client.sid, project=project_id
    )  # TODO: add to tgclients
    tabulate_tgauth_response(res)


def tabulate_tgauth_response(data):
    """A tgauth response consists of a list of objects, specify which keys to show."""
    table = Table(
        Column(header='Username', justify='right', style='cyan'),
        'Roles',
        box=box.MINIMAL,
    )

    for entry in data:
        table.add_row(entry['username'], ', '.join(entry['roles']))

    console.print(table)


@cli.command()
@click.argument('project_id', shell_complete=complete_project_ids)
@pass_tgclient
def contents(client, project_id):
    """List contents of project."""
    project_contents = client.tgsearch.search(
        filters=['project.id:' + project_id], sid=client.sid, limit=100
    )

    console.print(f'project {project_id} contains {project_contents.hits} files:')

    for tgobj in project_contents.result:
        title = tgobj.object_value.generic.provided.title
        tguri = tgobj.object_value.generic.generated.textgrid_uri.value
        mime = tgobj.object_value.generic.provided.format

        console.print(f' - {tguri}: {title} ({mime})')


@cli.command()
@click.option(
    '--clean',
    'do_clean',
    help='call clean automatically if project not empty',
    is_flag=True,
    show_default=True,
)
@click.option(
    '--limit',
    help='how much uris to retrieve for deletion in one query (if called with --clean)',
    default=10,
    show_default=True,
)
@click.confirmation_option(prompt='Are you sure you want to delete the project?')
@click.argument('project_id')
@pass_tgclient
def delete(client, project_id, do_clean, limit):
    """Delete project with project id "project_id"."""
    project_contents = client.tgsearch.search(filters=['project.id:' + project_id], sid=client.sid)
    if int(project_contents.hits) > 0:
        console.print(
            f"""Project {project_id} contains {contents.hits} files.
            Can not delete project (clean or force with --clean)"""
        )
        if do_clean:
            clean_op(client, project_id, limit)
        else:
            sys.exit(0)

    res = client.tgauth.delete_project(client.sid, project_id)
    console.print(f'deleted, status: {res}')


@cli.command()
@click.argument('project_id', shell_complete=complete_project_ids)
@click.option(
    '--limit',
    help='how much uris to retrieve for deletion in one query',
    default=10,
    show_default=True,
)
@click.option(
    '--threaded',
    help='use multithreading for crud delete requests (experimental, try without in case of errors)',
    is_flag=True,
)
@click.option(
    '--yes',
    'force',
    is_flag=True,
    show_default=True,
    default=False,
    help='delete without further confirmation',
)
@pass_tgclient
def clean(client, project_id, limit, threaded, force):
    """Delete all content from project with project id "project_id".

    NOTE: This may run into loops if you have public (non-deletable objects)
          in your project. In that case adapt your limit (and do not use threaded)
    """
    clean_op(client, project_id, limit, threaded, force)


def clean_op(
    client: TGclient,
    project_id: str,
    limit: int = 10,
    threaded: bool = False,
    force: bool = False,
):
    """Delete all objects belonging to a given project id.

    Args:
        client (TGclient): instance of tgclient
        project_id (str): the project ID
        limit (int): how much uris to retrieve for deletion in one query
        threaded (bool): wether to use multiple threads for deletion
        force (bool): skip confirmation question
    """
    project_contents = client.tgsearch.search(
        filters=['project.id:' + project_id], sid=client.sid, limit=limit
    )

    if not force:
        console.print(f'project {project_id} contains {project_contents.hits} files:')

        for tgobj in project_contents.result:
            title = tgobj.object_value.generic.provided.title
            tguri = tgobj.object_value.generic.generated.textgrid_uri.value

            console.print(f' - {tguri}: {title}')

        if int(project_contents.hits) > limit:
            console.print(f' ...and ({int(project_contents.hits) - limit}) more objects')

    if not force and not click.confirm('Do you want to delete all these objects'):
        sys.exit(0)
    else:
        with Progress(
            SpinnerColumn(),
            BarColumn(),
            TaskProgressColumn(),
            TimeRemainingColumn(),
            TextColumn('[progress.description]{task.description}'),
        ) as progress:
            # iterate with paging
            task1 = progress.add_task('deleting...', total=int(project_contents.hits))

            nextpage = True
            while nextpage:
                if not threaded:
                    for tgobj in project_contents.result:
                        result = _crud_delete_op(client, tgobj)
                        progress.update(
                            task1,
                            advance=1,
                            description=result,
                        )
                else:
                    with ThreadPoolExecutor(max_workers=limit) as ex:
                        futures = [
                            ex.submit(_crud_delete_op, client, tgobj)
                            for tgobj in project_contents.result
                        ]

                        for future in as_completed(futures):
                            result = future.result()
                            progress.update(
                                task1,
                                advance=1,
                                description=result,
                            )

                if int(project_contents.hits) < limit:
                    # stop if there are no more results left
                    nextpage = False
                else:
                    # get next page of results from tgsearch
                    project_contents = client.tgsearch.search(
                        filters=['project.id:' + project_id],
                        sid=client.sid,
                        limit=limit,
                    )


def _crud_delete_op(client, tgobj):
    tguri = tgobj.object_value.generic.generated.textgrid_uri.value
    title = tgobj.object_value.generic.provided.title
    try:
        client.crud.delete_resource(client.sid, tguri)
        return f'deleted {tguri}: {title}'
    except TextgridCrudException as e:
        return f'error deleting {tguri}: {title} - {e}'


@cli.command()
@click.argument('project_id', shell_complete=complete_project_ids)
@click.argument('files', type=click.File('rb'), nargs=-1)
@pass_tgclient
def put(client, files, project_id):
    """Put files together with textgrid metadata (.meta) online."""
    for file in files:
        metadata = MetadataContainerType()
        metadata.object_value = metafile_to_object(PurePath(file.name))
        res: MetadataContainerType = client.crud.create_resource(
            client.sid, project_id, file, metadata
        )
        mg = res.object_value.generic
        console.print(f'{mg.provided.title[0]} -> {mg.generated.textgrid_uri.value}')


@cli.command()
@click.argument('project_id', shell_complete=complete_project_ids)
@click.argument('the_data', type=click.File('rb'))
@click.argument('metadata', type=click.File('rb'))
@pass_tgclient
def put_d(client, project_id, the_data, metadata):
    """[deprecated] put a file with metadata online."""
    res = client.crud_req.create_resource(client.sid, project_id, the_data, metadata.read())
    console.print(res)


@cli.command()
@click.argument('textgrid_uri')
@click.argument('the_data', type=click.File('rb'))
@pass_tgclient
def update_data(client, textgrid_uri, the_data):
    """Update a file."""
    metadata = client.crud.read_metadata(textgrid_uri, client.sid)
    client.crud.update_resource(client.sid, textgrid_uri, the_data, metadata)


@cli.command()
@click.option('--xslt', help='also download own xslt as example', is_flag=True)
def portalconfig(xslt):
    """Download portalconfig templates in current directory."""
    # baseUris of readme.md and portalconfig examples to download
    uris = ['textgrid:46dt5', 'textgrid:46n7n']
    # baseUri of avatar img
    # TODO: avatar and xslt uris should be taken from portalconfig
    other_uris = ['textgrid:40rj2']
    if xslt:
        other_uris.append('textgrid:476bf')  # TODO: which XSLT to provide
    # collection for other material (avatar image and xslt)
    othercol_name = 'Other Files'

    # tgcrud with default configuration for download from prod repo
    crud = TextgridCrud()
    mdservice = TextgridMetadata()
    example_download(crud, mdservice, uris)

    # create collection for avatar, xslt
    othercol_ondisk = mdservice.transliterate(othercol_name)
    os.makedirs(othercol_ondisk, exist_ok=True)
    files = example_download(crud, mdservice, other_uris, othercol_ondisk)
    with (
        open(f'{othercol_ondisk}.collection.meta', 'w', encoding='UTF-8') as meta_file,
        open(f'{othercol_ondisk}.collection', 'w', encoding='UTF-8') as file,
    ):
        col = Utils.list_to_aggregation('self', files)
        file.write(col)
        # create col metadata | https://gitlab.gwdg.de/dariah-de/textgridrep/textgrid-python-clients/-/issues/90 - mimetypes!
        colmd = mdservice.build(othercol_name, 'text/tg.collection+tg.aggregation+xml')
        meta_file.write(serialize_metadata(colmd))

    # echo how to upload with put and/or put-aggregation
    console.print(f"""Config file templates and avatar example image downloaded.
    Now edit README.md and portalconfig.xml, exchange your avatar image and upload to your project afterwards:

    tgadmin put-aggregation <PROJECT_ID> {othercol_ondisk}.collection portalconfig.xml README.md
    """)


def example_download(crud, mdservice, uris, localpath='.'):
    files = []
    for uri in uris:
        meta = crud.read_metadata(uri)
        title = meta.object_value.generic.provided.title[0]
        # portalconfig.xml and readme.md are on "." and have their extension already in their title
        if localpath == '.':
            filename = title
        else:
            extension = mdservice.extension_for_format(meta.object_value.generic.provided.format)
            filename = f'{localpath}/{mdservice.transliterate(title)}.{extension}'
        with (
            open(f'{filename}.meta', 'w', encoding='UTF-8') as meta_file,
            open(f'{filename}', 'wb') as file,
        ):
            data = crud.read_data(uri).content
            if title == 'portalconfig.xml':
                data = rewrite_portalconfig_string(
                    data, './Other_Files/Eule_zeigt_nach_oben.png'
                )  # TODO: we just know this
            file.write(data)
            meta_file.write(serialize_metadata(meta))
        files.append(filename)
    return files


@cli.command()
@click.argument('textgrid_uri')
@click.option('--really-publish', help='really publish, no dryrun', is_flag=True)
@click.option('--ignore-warnings', help='ignore metadata warnings on publish', is_flag=True)
@pass_tgclient
def publish(client, textgrid_uri, really_publish, ignore_warnings):
    """Publish an publishable object (edition or collection)."""
    dryrun = not really_publish
    textgrid_uri = (
        f'textgrid:{textgrid_uri}' if not textgrid_uri.startswith('textgrid:') else textgrid_uri
    )
    console.print(
        f'\nPublishing {textgrid_uri} in mode dryrun={dryrun} and ignore-warnings={ignore_warnings}. Run with --verbose if you want detailed output.\n'
    )

    # check for format
    metadata = client.crud.read_metadata(textgrid_uri, client.sid).object_value

    if is_collection(metadata) or is_edition(metadata):
        jobid = client.publish.publish(client.sid, textgrid_uri, ignore_warnings, dry_run=dryrun)
    elif is_portalconfig(metadata) or is_readme(metadata):
        jobid = client.publish.publish_worldreadable(client.sid, textgrid_uri, ignore_warnings, dry_run=dryrun)
    else:
        sys.exit(1)

    if process_publishstatus(client, jobid):
        if really_publish:
            console.print(
                '[magenta]\n\n 🥳 FINISHED - Congratulations! Your data is published.\n[/]'
            )
        else:
            console.print(
                """[magenta]\n\n 🎉 FINISHED - Congratulations! Your data is ready for publication.
 Now run tgadmin with --really-publish\n[/]""",
            )

    print_publish_status(client, jobid)


@cli.command()
@click.argument('project_id', shell_complete=complete_project_ids)
@click.argument('textgrid_uris', nargs=-1)
@pass_tgclient
def copy(client, project_id, textgrid_uris):
    """Copy textgrid_uri(s) to project_id."""
    # add 'textgrid:'-prefix to each uri if not there
    textgrid_uris = [f'textgrid:{s}' if not s.startswith('textgrid:') else s for s in textgrid_uris]

    console.print(
        f'\nCopying {textgrid_uris} to {project_id}. Run with --verbose if you want detailed output.\n'
    )

    jobid = client.publish.copy(client.sid, textgrid_uris=textgrid_uris, project_id=project_id)

    if process_publishstatus(client, jobid):
        console.print("""[magenta]\n Copy finished.\n[/]""")

    print_publish_status(client, jobid)


def process_publishstatus(client, jobid) -> bool:
    if jobid.startswith('tgcopy:'):
        label = 'Copying'
    else:
        label = 'Publishing'

    # with click.progressbar(length=100, label=label, item_show_func=lambda a: a) as pbar:
    with Progress(
        SpinnerColumn(),
        BarColumn(),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        TextColumn('[progress.description]{task.description}'),
    ) as progress:
        task1 = progress.add_task('publishing...', total=100)
        while True:
            status: PublishResponse = client.publish.get_status(jobid)

            pstate = status.publish_status.process_status
            progressbar_message = f'{pstate.name} [{status.publish_status.active_module}]'
            # pbar.update(status.publish_status.progress - pbar.pos, progressbar_message)
            progress.update(
                task1, completed=status.publish_status.progress, description=progressbar_message
            )

            # there is no switch / case before python 3.10
            if pstate is ProcessStatusType.RUNNING:
                pass
            elif pstate is ProcessStatusType.QUEUED:
                pass
            elif pstate is ProcessStatusType.FAILED:
                console.print('[red]\n\n 💀 FAILED! Check the messages below for details[/]')
                return False
            elif pstate is ProcessStatusType.FINISHED:
                return True
            else:
                console.print('status unknown:' + pstate.name)

            time.sleep(0.5)

        return False  # should not be reached, so it must be an error ;-)


def print_publish_status(client, jobid):
    status: PublishResponse = client.publish.get_status(jobid)
    for po in status.publish_object:
        if client.verbose or len(po.error) > 0:
            meta = client.tgsearch.info(sid=client.sid, textgrid_uri=po.uri)
            title = meta.result[0].object_value.generic.provided.title[0]
            mime = meta.result[0].object_value.generic.provided.format
            if po.dest_uri:
                msg = f' * [{po.status.name}] copied {po.uri} to {po.dest_uri} - {title} ({mime})'
            else:
                msg = f' * [{po.status.name}] {po.uri} - {title} ({mime})'
            console.print(msg)
            for e in po.error:
                console.print(f'[red]    - {e.message}[/]')


def exit_with_error(message: str):
    console.print(f'\n:warning-emoji: [bold red] {message}[/]\n')
    sys.exit(1)


@cli.command()
@click.argument('textgrid_uris', nargs=-1)
@click.option(
    '--output-path',
    help="Specify path where exported data will be saved (default: './tgexport')",
    default='./tgexport',
)
@pass_tgclient
def export_batch(client, textgrid_uris, output_path: str = './tgexport'):
    """Function to export a batch of textgrid resources and save them locally, including an IMEX so they may be re-imported later."""
    imex_filename = output_path + '/.INDEX.imex'
    if os.path.isfile(imex_filename):
        console.print(f"Found existing imex file at '{imex_filename}' - updating this.")
        imex_map = imex_to_path_dict(imex_filename)
    else:
        imex_map = {}

    data_folder = 'data'
    os.makedirs(output_path + '/' + data_folder, exist_ok=True)

    # add 'textgrid:'-prefix to each uri if not there
    textgrid_uris = [f'textgrid:{s}' if not s.startswith('textgrid:') else s for s in textgrid_uris]

    for textgrid_uri in textgrid_uris:
        # retrieve metadata
        metadata: MetadataContainerType = client.crud.read_metadata(textgrid_uri, client.sid)

        # make variables for paths
        data_format = metadata.object_value.generic.provided.format.split('/')[1]
        local_data = data_folder + '/' + textgrid_uri.replace('textgrid:', '') + '.' + data_format
        local_metadata = local_data + '.meta'

        # fill imex_map
        imex_map[PurePath(output_path + '/' + local_data)] = (
            metadata.object_value.generic.generated.textgrid_uri.value
        )

        # save metadata
        with open(output_path + '/' + local_metadata, 'w', encoding='UTF-8') as file:
            file.write(serialize_metadata(metadata))

        # retrieve and save data
        data = client.crud.read_data(textgrid_uri, client.sid)
        with open(output_path + '/' + local_data, 'wb') as file:
            file.write(data.content)

    # make and save .INDEX.imex
    write_imex(imex_map, imex_filename)

    console.print(
        f"""[magenta]Finished. You may change your data in dir '{output_path}' and re-import with 'tgadmin update-imex {output_path}/.INDEX.imex'.
          To re-import as a new revision, use 'tgadmin update-imex {output_path}/.INDEX.imex --newrev'[/]"""
    )


@cli.command()
@click.argument('textgrid_uris', nargs=-1)
@click.option(
    '-r',
    '--recursive',
    help='delete recursive (in case of aggregations/editions/collections)',
    is_flag=True,
)
@click.option(
    '--yes',
    'force',
    is_flag=True,
    show_default=True,
    default=False,
    help='delete without further confirmation',
)
@pass_tgclient
def delete_object(client, textgrid_uris, recursive: bool = False, force: bool = False):
    """Delete textgrid objects from the repository"""
    # TODO: all revisions (http://textgridlab.org/doc/services/submodules/tg-search/docs/api/info.html#get-info-textgriduri-revisions)
    limit = 10  # how much titles to show

    # add 'textgrid:'-prefix to each uri if not there
    textgrid_uris = [f'textgrid:{s}' if not s.startswith('textgrid:') else s for s in textgrid_uris]
    all_uris: list[str] = textgrid_uris.copy()

    if recursive:
        for tguri in textgrid_uris:
            all_uris.extend(client.tgsearch.children(textgrid_uri=tguri).textgrid_uri)

    if not force:
        console.print(f'found {len(all_uris)} objects:')

        for tguri in all_uris[:limit]:
            res = client.tgsearch.info(tguri, client.sid).result
            if len(res) > 0:
                tgobj = res[0]
                title = tgobj.object_value.generic.provided.title
                console.print(f' - {tguri}: {title}')
            else:
                console.print(
                    f'[magenta] - {tguri}: not found - may be a dead reference in aggregation[/]'
                )

        if len(all_uris) > limit:
            console.print(f' ...and ({len(all_uris) - limit}) more objects')

    if not force and not click.confirm('Do you want to delete all these objects'):
        sys.exit(0)
    else:
        with click.progressbar(
            length=len(all_uris),
            label='deleting object',
            show_eta=True,
            show_pos=True,
            item_show_func=lambda a: a,
        ) as bar:
            for tguri in all_uris:
                try:
                    client.crud.delete_resource(client.sid, tguri)
                    result = f'deleted {tguri}'
                except TextgridCrudException as e:
                    result = f'error deleting {tguri} - {e}'
                bar.update(1, result)


@cli.command()
@click.argument('project_id', shell_complete=complete_project_ids)
@click.argument('aggregation_files', type=click.File('rb'), nargs=-1)
@click.option('--ignore-warnings', help='do not stop on tgcrud warnings', is_flag=True)
@click.option(
    '--threaded',
    help='deprecated, we do not support threaded upload anymore and ignore this flag ;-)',
    is_flag=True,
)
@pass_tgclient
def put_aggregation(
    client, project_id: str, aggregation_files, threaded: bool, ignore_warnings: bool
):
    """Upload aggregations and referenced objects recursively."""
    files = [file.name for file in aggregation_files]

    console.print(f"""
    Starting import of {files}. This may take some time.
    If you want so see tgadmin working try --verbose
    """)
    start_time = time.time()

    # create imex at the location of the first file with ending .imex
    imex_location = files[0] + '.imex'

    try:
        tgimp = TGimport(
            sid=client.sid,
            project_id=project_id,
            crud=client.crud,
            imex_location=imex_location,
            ignore_warnings=ignore_warnings,
            initial=True,
        )
        status = tgimp.upload(files)

    except TextgridImportException as error:
        exit_with_error(error)

    time_format = time.strftime('%Hh%Mm%Ss', time.gmtime(time.time() - start_time))
    console.print(f"""
    Done: imported {status.completed} files in {time_format}.
    Find the imex file at {status.imex.location.as_posix()}
    TextgridURI of first file is {status.imex.get(PurePath(aggregation_files[0].name))}
    """)


@cli.command()
@click.argument('imex', type=click.File('rb'))
@click.argument('project_id', shell_complete=complete_project_ids, required=False)
@click.argument('aggregation_files', type=click.File('rb'), nargs=-1, required=False)
@click.option('--newrev', 'make_revision', help='to update data as new revisions', is_flag=True)
@click.option('--data-only', 'data_only', help='only update data, not metadata', is_flag=True)
@click.option('--ignore-warnings', help='do not stop on tgcrud warnings', is_flag=True)
@pass_tgclient
def update_imex(
    client,
    imex,
    project_id: str = '',
    aggregation_files=None,
    make_revision: bool = True,
    data_only: bool = False,
    ignore_warnings: bool = False,
):
    """Update with an IMEX file.

    Argument 1 is the IMEX file. Optional Argument 2 the projectId
    where new objects shall be uploaded to and Argument 3 to ... are
    locations of aggregation files.
    """
    files = [file.name for file in aggregation_files]
    console.print("""
    Starting update. This may take some time.
    If you want so see tgadmin working try --verbose
    """)
    start_time = time.time()

    try:
        tgimp = TGimport(
            client.sid,
            project_id=project_id,
            crud=client.crud,
            imex_location=imex.name,
            ignore_warnings=ignore_warnings,
            new_revision=make_revision,
            data_only=data_only,
        )
        status = tgimp.upload(files)
    except TextgridImportException as error:
        exit_with_error(error)

    time_format = time.strftime('%Hh%Mm%Ss', time.gmtime(time.time() - start_time))
    console.print(f"""
    Done: updated {status.completed} files in {time_format}.
    """)


@cli.command('import')
@click.argument('aggregation_files', type=click.File('rb'), nargs=-1, required=False)
@click.option(
    '--project-id',
    '-p',
    shell_complete=complete_project_ids,
    required=False,
    help='project id where to upload files to. necessary when new objects are created. not for update only',
)
@click.option(
    '--imex',
    '-i',
    type=click.File('rb'),
    help='location of IMEX file. Defaults to location of aggregation file + .imex',
)
@click.option('--newrev', 'make_revision', help='to update data as new revisions', is_flag=True)
@click.option('--data-only', 'data_only', help='only update data, not metadata', is_flag=True)
@click.option('--ignore-warnings', help='do not stop on tgcrud warnings', is_flag=True)
@click.option('--fresh', help='do a fresh upload, ignoring old IMEX files', is_flag=True)
@click.option('--resume', '-r', help='resume import', is_flag=True)
@click.option(
    '--linkrewriter-cli',
    default=lambda: os.environ.get('LINK_REWRITER_CLI', 'linkrewriter-cli'),
    help='path to link-rewriter-cli',
)
@pass_tgclient
def tgimport(
    client,
    imex,
    project_id: str = '',
    aggregation_files=None,
    make_revision: bool = False,
    data_only: bool = False,
    ignore_warnings: bool = False,
    fresh: bool = False,
    resume: bool = False,
    linkrewriter_cli='linkrewriter-cli',
):
    """Import data into (or update in) textgrid repository."""
    files = [file.name for file in aggregation_files]
    console.print("""
    Starting upload. This may take some time.
    If you want so see tgadmin working try --verbose
    """)
    start_time = time.time()

    if imex:
        imex_filename = imex.name
    else:
        imex_filename = aggregation_files[0].name + '.imex'
        if Path(imex_filename).is_file() and not fresh:
            if not click.confirm(
                f"""There is already a file {imex_filename}
Use this for update? hit "y" for update or "n" to do a fresh upload""",
                default=True,
            ):
                fresh = True
                log.info('ignoring imex file and uploading with new uris')
            else:
                log.info('using existing imex file')

    if fresh and not project_id:
        console.print('please provide a project ID for new uploads')
        return

    try:
        tgimp = TGimport(
            client.sid,
            project_id=project_id,
            crud=client.crud,
            imex_location=imex_filename,
            ignore_warnings=ignore_warnings,
            initial=fresh,
            new_revision=make_revision,
            data_only=data_only,
            link_rewriter=linkrewriter_cli,
            resume=resume,
        )
        status = tgimp.upload(files, threaded=True)

    except TextgridImportException as error:
        exit_with_error(error)

    with Progress(
        SpinnerColumn(),
        BarColumn(),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        TextColumn('[progress.description]{task.description}'),
    ) as progress:
        task1 = progress.add_task('uploading...', total=status.total)
        while status.status == ImportStatus.Status.RUNNING:
            progress.update(
                task1,
                completed=status.completed,
                description=f'{status.message} {status.current}',
            )
            time.sleep(0.2)
        progress.update(task1, completed=status.completed, description=status.message)

    if status.status == ImportStatus.Status.FAILED:
        exit_with_error(status.message)

    time_format = time.strftime('%Hh%Mm%Ss', time.gmtime(time.time() - start_time))
    console.print(f"""
    Done: imported {status.completed} files in {time_format}.
    Find the imex file at {status.imex.location.as_posix()}
    TextgridURI of first file is {status.imex.get(PurePath(aggregation_files[0].name))}
    """)
