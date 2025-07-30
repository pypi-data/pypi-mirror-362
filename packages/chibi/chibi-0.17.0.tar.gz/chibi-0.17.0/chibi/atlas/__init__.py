import json
import xml
import xmltodict
import yaml
from chibi.snippet.dict import hate_ordered_dict, remove_xml_notatation

from chibi_atlas import (
    Chibi_atlas, Chibi_atlas_default, Chibi_atlas_ignore_case, Atlas,
)

from chibi_atlas.chibi_atlas import _wrap  # noqa: F401


__all__ = [
    'Chibi_atlas',
    'Chibi_atlas_default',
    'Chibi_atlas_ignore_case',
    'Atlas',
    'loads',
]


def loads( string ):
    try:
        return Chibi_atlas( json.loads( string ) )
    except ( json.JSONDecodeError, TypeError ):
        try:
            result = xmltodict.parse( string )
            result = hate_ordered_dict( result )
            result = remove_xml_notatation( result )
            return Chibi_atlas( result )
        except xml.parsers.expat.ExpatError:
            return Chibi_atlas( yaml.safe_load( string ) )
