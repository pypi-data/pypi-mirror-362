import glob
import logging
import os
import shutil
import re

import magic
from chibi.snippet import regex


logger = logging.getLogger( "chibi.file.chibi_path" )
logger_delete = logging.getLogger( "chibi.file.chibi_path.delete" )


class Chibi_path( str ):
    def __new__( cls, *args, chibi_file_class=None, **kw ):
        args_2 = []
        for a in args:
            if '~' in a:
                a = os.path.expanduser( a )
            args_2.append( a )
        result = str.__new__( cls, *args_2, **kw )
        result._chibi_file_class = chibi_file_class
        return result

    def __add__( self, other ):
        """
        une el path con otro path o una cadena

        Parameters
        ==========
        other: str or Chibi_path

        Returns
        =======
        Chibi_path
        """
        if isinstance( other, self.__class__ ):
            if self.is_a_file:
                return self.dir_name + other

            return type( self )( os.path.join( str( self ), str( other ) ) )
        if isinstance( other, str ):
            return self + self.__class__( other )

    def __eq__( self, other ):
        if isinstance( other, Chibi_path ):
            return str( self ) == str( other )
        if isinstance( other, str ):
            return str( self ) == other
        return False

    def __hash__( self ):
        return hash( str( self ) )

    def __contains__( self, other ):
        if isinstance( other, Chibi_path ):
            return other.startswith( self )
        else:
            return super().__contains__( other )

    @property
    def is_a_folder( self ):
        """
        es una carpeta
        """
        return os.path.isdir( self )

    @property
    def is_a_file( self ):
        """
        es un archivo
        """
        from chibi.file.snippets import is_a_file
        return is_a_file( self )

    @property
    def is_glob( self ):
        return glob.has_magic( self )

    @property
    def dir_name( self ):
        """
        regresa la carpeta padre
        """
        from chibi.file.snippets import file_dir
        return type( self )( os.path.dirname( str( self ) ) )
        return self.__class__( file_dir( self ) )

    @property
    def base_name( self ):
        """
        regresa el nombre del archivo o de la carpeta
        """
        return Chibi_path( os.path.basename( self ) )

    @property
    def file_name( self ):
        """
        regresa el nombre del archivo sin la extencion
        """
        file_name, ext = os.path.splitext( self.base_name )
        return file_name

    def open( self, chibi_file_class=None, encoding=None, newline=None, **kw ):
        """
        abre el archivo usando un chibi file
        """
        if self.is_a_folder:
            raise NotImplementedError(
                f'abrir folders no esta implementado "{self}"' )
        if chibi_file_class is None:
            if self._chibi_file_class is None:
                from .file import Chibi_file
                chibi_file_class = Chibi_file
            else:
                chibi_file_class = self._chibi_file_class
        return chibi_file_class(
            self, encoding=encoding, newline=newline, **kw )

    def relative_to( self, root ):
        """
        regresa el path relativos

        Parameters
        ==========
        root: string

        Returns
        =======
        string

        Examples
        ========
        >>>Chibi_path( '/usr/var/log' ).relative_to(  root='/usr/var/' )
        'log'
        """
        from .snippets import get_relative_path
        return type( self )( get_relative_path( self, root=root ) )

    def mkdir( self, **kw ):
        """
        crea una carpeta en la direcion del chibi path
        """
        try:
            os.makedirs( self )
            logger.info( "se creo el directorio '{}'".format( self ) )
        except OSError:
            pass
        if kw:
            logger.warning(
                "mkdir de chibi path recibio parametros {}".format( kw ) )

    def move( self, dest ):
        """
        move the chibi path al destino
        """
        dest = Chibi_path( dest )
        if self.is_a_file:
            if dest.is_a_folder:
                dest += self.base_name
            shutil.move( str( self ), str( dest ) )
            logger.info( "{} -> {}".format( self, dest ) )
        elif self.is_a_folder:
            shutil.move( str( self ), str( dest ) )
            logger.info( "{} -> {}".format( self, dest ) )
        elif self.is_glob:
            if not dest.exists:
                dest.mkdir()
            if dest.is_a_folder:
                return [
                    f.move( dest + f.base_name ) for f in self.expand ]
            else:
                raise NotImplementedError(
                    "el destino no es un folder y la src "
                    "es un glob '{self}'" )

    def copy( self, dest, **kw ):
        """
        copia el archivo o carpeta al destino
        """
        from .snippets import copy
        dest = Chibi_path( dest )
        if self.is_a_file:
            if dest.is_a_folder:
                dest += self.base_name
            copy( self, dest, **kw )
            return Chibi_path( dest )
        elif self.is_a_folder:
            if dest.is_a_file:
                raise NotImplementedError(
                    "no se puede copiar un folder dentro de un archivo" )
            shutil.copytree( str( self ), str( dest ), dirs_exist_ok=True )
            return Chibi_path( dest )
        elif self.is_glob:
            if not dest.exists:
                dest.mkdir()
            if dest.is_a_folder:
                return [ f.copy( dest + f.base_name ) for f in self.expand ]
            else:
                raise NotImplementedError(
                    "el destino no es un folder y la src "
                    "es un glob '{self}'" )
        if not self.exists:
            raise OSError( f"the file '{self}' not exists" )
        else:
            raise NotImplementedError(
                f"no esta implementado el copy si "
                f"no es un archivo o folder '{self}'" )

    def delete( self ):
        """
        elimina el archivo o la carpeta
        """
        if self.is_a_file:
            os.remove( str( self ) )
            logger_delete.info( 'delete file "{}"'.format( self ) )
        else:
            shutil.rmtree( str( self ) )
            logger_delete.info( 'delete folder "{}"'.format( self ) )

    def chown(
            self, verbose=True, user_name=None, group_name=None,
            recursive=False ):
        """
        cambia el duano del archivo o carpeta
        """
        from chibi.file.snippets import chown
        chown(
            self, user_name=user_name, group_name=group_name,
            recursive=recursive, verbose=verbose )

    def chmod( self, mod ):
        """
        cambia los attributos del archivo o carpeta
        """
        os.chmod( str( self ), mod )

    @property
    def properties( self ):
        from chibi.file.snippets import stat

        prop = stat( self )
        if self.is_a_folder:
            prop.mime = 'folder'
            prop.extension = ''
        else:
            prop.mime = magic.Magic( mime=True ).from_file( self )
            prop.extension = os.path.splitext( self )[1][1:]
        return prop

    @property
    def extension( self ):
        """
        regresa la extencion del archivo el formato es '.{ext}'
        """
        if self.is_a_file:
            return self.properties.extension
        elif not self.exists:
            file_name, ext = os.path.splitext( self.base_name )
            return ext
        else:
            raise NotImplementedError

    def replace_extensions( self, *extensions ):
        """
        cambia la extencion del archivo
        """
        file_name, ext = os.path.splitext( self )
        extensions = ".".join( extensions )
        file_name = ".".join( ( file_name, extensions ) )
        return type( self )( file_name )

    def add_extensions( self, *extensions ):
        """
        agrega mas extenciones
        """
        file_name, ext = os.path.splitext( self )
        extensions = ".".join( extensions )
        file_name = ".".join( ( file_name, ext + extensions ) )
        return type( self )( file_name )

    def ls( self, dirs=True, files=True ):
        """
        regresa un generador con el listado de archivos y carpetas
        """
        from .snippets import ls, ls_only_dir, ls_only_files
        if dirs and files:
            return ls( self )
        elif dirs and not files:
            return ls_only_dir( self )
        elif not dirs and files:
            return ls_only_files( self )
        else:
            raise NotImplementedError

    def find( self, search_term=".*", dirs=True, files=True ):
        """
        busca archivos y carpetas usando una exprecion regular
        """
        if self.is_a_file:
            raise NotImplementedError(
                "no esta implementa buscar en un archivo" )
        from .snippets import ls
        if dirs and files:
            name = re.compile( search_term )
            list_files = ls( self, recursive=True )
            try:
                for f in list_files:
                    base_name = f.base_name
                    if regex.test( name, base_name ):
                        yield f
            except PermissionError as e:
                logger.warning( f'{e}' )
        elif dirs and not files:
            yield from (
                f for f in self.find( search_term=search_term )
                if f.is_a_folder )
        elif not dirs and files:
            yield from (
                f for f in self.find( search_term=search_term )
                if f.is_a_file )
        else:
            raise NotImplementedError

    @property
    def exists( self ):
        """
        revisa si el archivo o directorio existe

        Returns
        =======
        bool
        """
        from .snippets import exists
        return exists( str( self ) )

    def replace( self, *args, **kw ):
        return Chibi_path( super().replace( *args, **kw ) )

    def made_safe( self ):
        return Chibi_path( re.sub( r'[<>:"|?*]', '', str( self ) ) )

    @classmethod
    def current_dir( cls ):
        """
        regresa el directorio actual de trabajo

        Returns
        =======
        py:class:`chibi.file.Chibi_path`
        """
        return Chibi_path( os.getcwd() )

    @property
    def expand( self ):
        if self.is_glob:
            return ( type( self )( f ) for f in glob.iglob( self ) )
        else:
            raise NotImplementedError( "no se que deberia de hacer" )

    def __enter__( self ):
        return self.open()

    def __exit__( self, exc_type, exc_value, traceback ):
        pass

    def touch( self ):
        if not self.exists or self.is_a_file:
            self.open().touch()
        elif self.is_a_folder:
            raise NotADirectoryError(
                f"no implementado touch a un folder '{self}'" )
        else:
            raise NotADirectoryError(
                f"no implementado touch cuando no es un "
                f"archivo o folder'{self}'" )

    @property
    def inflate( self ):
        if '~' in self:
            return os.path.expanduser( self )
        else:
            return os.path.abspath( self )
