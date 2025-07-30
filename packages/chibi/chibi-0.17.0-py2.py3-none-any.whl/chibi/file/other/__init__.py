import os
from .chibi_csv import Chibi_csv
from .chibi_yaml import Chibi_yaml
from .chibi_json import Chibi_json
from .chibi_python import Chibi_python
from .chibi_systemd import Chibi_systemd  # noqa: F401
from .conf import Chibi_conf  # noqa: F401


__all__ = [ 'Chibi_csv', 'Chibi_yaml', 'Chibi_json', 'Chibi_python' ]


def find_correct_class( path, cls ):
    file_name, ext = os.path.splitext( path )
    if ext == '.csv':
        return Chibi_csv
    elif ext in ( '.yml', '.yaml' ):
        return Chibi_yaml
    elif ext == '.json':
        return Chibi_json
    elif ext == '.py':
        return Chibi_python
    return cls
