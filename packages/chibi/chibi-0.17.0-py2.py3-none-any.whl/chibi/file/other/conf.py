import re

from chibi.atlas import Chibi_atlas
from chibi.file import Chibi_file
from chibi.snippet.iter import chunk_each


__all__ = [ 'Chibi_conf' ]


category_regex = re.compile( r"\[.*\]" )


class Chibi_conf( Chibi_file ):
    def read( self ):
        data = super().read()
        result = Chibi_atlas()
        lines = filter( bool, data.split( '\n' ) )
        lines = filter( lambda x: not x.startswith( ';' ), lines )
        chunks = chunk_each( lines, lambda x: category_regex.match( x ) )
        for section in chunks:
            section_key = section[0][1:-1].strip()
            section_data = section[1:]
            section_dict = Chibi_atlas()

            for line in section_data:
                key_data = line.split( '=', 1 )
                if len( key_data ) == 1:
                    key = key_data[0]
                    data = ''
                else:
                    key, data = key_data
                key = key.strip()
                data = data.strip()
                section_dict[ key ] = data
            result[ section_key ] = section_dict
        return result

    def write( self, data ):
        result = ''
        sort_order = [ 'www', ]
        other_keys = ( k for k in data.keys() if k not in sort_order )
        for k in sort_order:
            section = data[ k ]
            section_str = self._transform_section( k, section )
            result += section_str
        for k in other_keys:
            section = data[ k ]
            section_str = self._transform_section( k, section )
            result += section_str
        super().write( result )

    def _transform_section( self, name, section ):
        name = name
        result = f"[{name}]\n"
        for k, v in section.items():
            if isinstance( v, list ):
                for inner in v:
                    result += f"{k}={inner}\n"
            else:
                result += f"{k}={v}\n"
        return result
