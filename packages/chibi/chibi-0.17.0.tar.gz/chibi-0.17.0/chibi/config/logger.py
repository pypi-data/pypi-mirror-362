import logging


__all__ = [ 'basic_config', 'silent' ]


def basic_config( level=logging.INFO, force=True ):
    from . import configuration
    level = logging.getLevelName( level )
    logger_formarter = '%(levelname)s %(asctime)s %(name)s %(message)s'
    try:
        logging.basicConfig(
            level=level, format=logger_formarter, force=force )
    except ValueError as e:
        if 'Unrecognised argument(s): force' == str( e ):
            logging.basicConfig( level=level, format=logger_formarter )
            logger = logging.getLogger( 'chibi.config.logger' )
            logger.warning(
                "estas usando una version vieja de python por eso no se "
                "puede usar el parametro 'force' para asignar el "
                "formato del los logs" )
        else:
            raise
    if configuration.env_vars.PYTHON_UNITTEST_LOGGER:
        level = configuration.env_vars.PYTHON_UNITTEST_LOGGER


def silent():
    basic_config( logging.ERROR )
