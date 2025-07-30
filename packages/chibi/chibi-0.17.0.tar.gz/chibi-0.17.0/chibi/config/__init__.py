from .config import (
    __all__ as config_all,
    Configuration, Logger_configuration, Env_vars )
from .logger import *  # noqa: F403
from chibi.file import Chibi_path


__all__ = config_all + logger.__all__  # noqa: F405


configuration = Configuration(
    loggers=Logger_configuration(),
    env_vars=Env_vars(),
)


def _build_config_path():
    config_home = configuration.env_vars.HOME
    if not config_home:
        return

    config_home = Chibi_path( configuration.env_vars.XDG_CONFIG_HOME )
    if not config_home:
        config_home = Chibi_path( '~/.config' )
    config_home += 'chibi'
    return config_home


def _should_load_config_file( config_home, config_file ):
    return config_home.exists and config_file.exists


def _do_touch( config_home, config_file ):
    if not config_home.exists:
        config_home.mkdir()
    if not config_file.exists:
        config_file.touch()


def default_file_load( python_file_config='chibi.py', touch=False ):
    config_home = _build_config_path()
    if config_home is None:
        return
    config_file = config_home + python_file_config
    if touch:
        _do_touch( config_home, config_file )
    if _should_load_config_file( config_home, config_file ):
        load( config_file )


def load( path ):
    configuration.load( path )


default_file_load()
