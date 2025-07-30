# SPDX-FileCopyrightText: 2024 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: LGPL-3.0-or-later

# this file should contain general utility functions for
# working with tgclient, textgrid metadata and the import
# so the functions here ca move to tgclients itself
# they should be generic and make no assumptions about
# their usage, e.g. have no references to click, jupyter or pandas

import logging
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.dom.minidom import parse

from jinja2 import Template
from tgclients.databinding import MetadataContainerType
from tgclients.databinding import Object as TextgridObject
from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

log = logging.getLogger(__name__)

NAMESPACES = {'ore': 'http://www.openarchives.org/ore/terms/'}
PC_NAMESPACES = {
    'pc': 'http://textgrid.info/namespaces/metadata/portalconfig/2020-06-16',
    'xml': 'http://www.w3.org/XML/1998/namespace',
}
RDF_RESOURCE = '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource'
TG_METADATA_NAMESPACE = 'http://textgrid.info/namespaces/metadata/core/2010'

context = XmlContext()
PARSER = XmlParser(context=context)
SERIALIZER = XmlSerializer(context=context, config=SerializerConfig(indent='  '))


def calc_relative_path(filename: str, path: str) -> Path:
    """Find the path of 'path' relative to 'filename'.

    this could possibly be solved with walk_up=true from python 3.12 on
    https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.relative_to
    """
    return Path(path).resolve().relative_to(Path(filename).parent.resolve())


def write_imex(imex_map: dict, filename: str) -> None:
    """Write an .imex file which keeps track of local filenames and their related textgrid uris.

    This is useful for reimporting the data with the same uris (or new revisions of them).
    """
    imex_template_string = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<importSpec xmlns="http://textgrid.info/import">
  {%- for path, tguri in imex.items() %}
  <importObject textgrid-uri="{{tguri}}" local-data="{{calc_relative_path(filename, path)}}"/>
  {%- endfor %}
</importSpec>

"""
    template = Template(imex_template_string)
    template.globals.update(calc_relative_path=calc_relative_path)
    xml = template.render(imex=imex_map, filename=filename)
    with open(filename, 'w') as file:
        file.write(xml)


def imex_to_dict(imex_file_path, path_as_key: bool = False) -> dict:
    """Parse textgrid_uris and paths from imex file.

    Return a dict with uri as key per default,
    or use path as key if path_as_key is true
    """
    imex_map = {}
    imexXML = parse(imex_file_path)
    for importObject in imexXML.getElementsByTagName('importObject'):
        textgrid_uri = importObject.getAttribute('textgrid-uri')
        path = importObject.getAttribute('local-data')

        if path_as_key:
            imex_map[path] = textgrid_uri
        else:
            imex_map[textgrid_uri] = path

    return imex_map


def imex_to_path_dict(imex_file_path) -> dict:
    """Parse textgrid_uris and paths from imex file.

    Return a dict with purepath as key, tguri as value
    """
    # TODO: merge with imex_to_dict() - needs adapting tgadmin.update_imex()
    imex_map = {}
    imexXML = parse(imex_file_path)
    for importObject in imexXML.getElementsByTagName('importObject'):
        textgrid_uri = importObject.getAttribute('textgrid-uri')
        path_str = importObject.getAttribute('local-data')
        path = Path(Path(imex_file_path).parent / path_str)
        imex_map[path] = textgrid_uri

    return imex_map


def base_uri_from(textgrid_uri: str) -> str:
    return textgrid_uri.split('.')[0]


def is_aggregation(meta: TextgridObject) -> bool:
    """Wether this object is an aggregation (including subtypes edition/collection).

    Args:
        meta (TextgridObject): textgrid metadata object

    Returns:
        bool: true if 'tg.aggregation' found in format
    """
    assert meta.generic is not None
    assert meta.generic.provided is not None
    assert meta.generic.provided.format is not None
    return 'tg.aggregation' in meta.generic.provided.format


def is_edition(meta: TextgridObject) -> bool:
    return meta.generic.provided.format == 'text/tg.edition+tg.aggregation+xml'


def is_collection(meta: TextgridObject) -> bool:
    return meta.generic.provided.format == 'text/tg.collection+tg.aggregation+xml'


def is_portalconfig(meta: TextgridObject) -> bool:
    return meta.generic.provided.format == 'text/tg.portalconfig+xml'


def is_readme(meta: TextgridObject) -> bool:
    return meta.generic.provided.format == 'text/markdown'


def is_xml(meta: TextgridObject) -> bool:
    return meta.generic.provided.format.startswith(
        'text/xml'
    ) or meta.generic.provided.format.startswith('application/xml')


def is_allowed_in_project_root(meta: TextgridObject) -> bool:
    """Check if this file may be in the root of a project."""
    return is_aggregation(meta) or is_portalconfig(meta) or is_readme(meta)


def rewrite_portalconfig_string(portalconfig, avatar_location, xslt_location=''):
    parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
    the_dataXML = ET.fromstring(portalconfig, parser)

    # modify avatar element
    the_dataXML.find('pc:avatar', PC_NAMESPACES).text = avatar_location
    # optinally modify xslt element
    if xslt_location != '':
        the_dataXML.find('pc:xslt', PC_NAMESPACES).text = xslt_location

    the_data = ET.tostring(
        the_dataXML,
        encoding='utf8',
        method='xml',
        default_namespace=PC_NAMESPACES['pc'],
    )
    return the_data


def serialize_metadata(metadata: MetadataContainerType) -> str:
    # render with default namespace
    return SERIALIZER.render(metadata.object_value, ns_map={None: TG_METADATA_NAMESPACE})
