from chibi.config import configuration, basic_config
import logging


basic_config()

configuration.loggers[ 'chibi.file.chibi_path.delete' ].level = logging.WARNING
configuration.loggers[ 'chibi.file.chibi_path' ].level = logging.WARNING
