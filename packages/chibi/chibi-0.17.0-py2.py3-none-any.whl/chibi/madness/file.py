import tempfile
from chibi.file import Chibi_path

tmp_folder = ''


def make_empty_file( suffix=None ):
    folder = get_temp_folder()
    return Chibi_path( tempfile.mkstemp(
        dir=str( folder ), suffix=suffix )[1] )


def get_temp_folder():
    global tmp_folder
    if not tmp_folder:
        tmp_folder = tempfile.mkdtemp()
    return Chibi_path( tmp_folder )
