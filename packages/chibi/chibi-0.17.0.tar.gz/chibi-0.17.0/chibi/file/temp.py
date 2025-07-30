import tempfile

from .path import Chibi_path


class Chibi_temp_path( Chibi_path ):
    """
    cuando se instancia crea un directorio temporal en /tmp/ y cuando
    se elimina la instancia se borra la carpeta( algunas veces )
    """
    def __new__( cls, *args, delete_on_del=True, **kw ):
        args_2 = []
        args_2.append( tempfile.mkdtemp() )
        result = str.__new__( cls, *args_2, **kw )
        result._delete_on_del = delete_on_del
        return result

    def __del__( self ):
        if self._delete_on_del:
            self.delete()

    def __add__( self, other ):
        return Chibi_path( str( self ) ) + other

    def temp_file( self, extension='' ):
        subffix = f'.{extension}' if extension else extension
        file_name = tempfile.mkstemp( suffix=subffix, dir=str( self ) )[1]
        return Chibi_path( file_name )

    def temp_dir( self ):
        return Chibi_path( tempfile.mkdtemp( dir=str( self ) ) )
