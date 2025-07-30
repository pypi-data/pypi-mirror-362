import logging
import os

import chibi_donkey as donkey

from chibi.atlas import Chibi_atlas, Chibi_atlas_default, Atlas
from chibi.file import Chibi_path
from chibi.file.other import Chibi_json, Chibi_yaml, Chibi_python


logger = logging.getLogger( 'chibi.config.Configuration' )


__all__ = [ 'Configuration' ]


def _default_factory():
    return Configuration()


class Configuration( Chibi_atlas_default ):
    """
    esta clase funciona como un simple dicionario de atributos para asignar
    configuraciones
    """
    def __init__( self, default_factory=None, *args, **kw ):
        if default_factory is None:
            default_factory = _default_factory
        super().__init__( default_factory, *args, **kw )

    def load( self, path ):
        path = Chibi_path( path )
        with path as f:
            if isinstance( f, ( Chibi_json, Chibi_yaml ) ):
                for k, v in f.read().items():
                    self[ k ] = v
            elif isinstance( f, Chibi_python ):
                logger.info( f"ejecutanto archivo python {f}" )
                f.import_()
            else:
                raise NotImplementedError(
                    "no esta implementado la carga de configuracion de los "
                    f"archivos {type(f)} de {f}" )


class Logger_configuration( Chibi_atlas ):
    """
    su default busca los loggers de python usnado el key
    """
    def __getitem__( self, name ):
        try:
            return super().__getitem__( name )
        except KeyError:
            # logger = logging.getLogger( name )
            self[ name ] = Logger( name=name )
            return super().__getitem__( name )


class Logger( Chibi_atlas ):
    @property
    def level( self ):
        logger = self.logger
        while logger:
            if logger.level != logging.NOTSET:
                return logger.level
            logger = logger.parent
        return self.logger.level

    @level.setter
    def level( self, value ):
        if isinstance( value, str ):
            level = getattr( logging, value )
            if isinstance( level, int ):
                self.logger.setLevel( level )
            else:
                raise NotImplementedError(
                    f"no esta implementado la asignacion del level de {value}"
                )
        elif isinstance( value, int ):
            self.logger.setLevel( value )
        else:
            raise NotImplementedError(
                f"no esta implementado la asignacion del level de {value}" )

    @property
    def logger( self ):
        return logging.getLogger( self.name )


class Env_vars( Configuration ):
    def __init__( self, default_factory=None, *args, **kw ):
        if default_factory is None:
            default_factory = str
        d = Atlas( donkey.inflate( os.environ ) )
        super().__init__( default_factory, d, *args, **kw )
