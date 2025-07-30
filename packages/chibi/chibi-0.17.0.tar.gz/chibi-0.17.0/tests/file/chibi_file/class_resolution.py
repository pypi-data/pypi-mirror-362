from chibi.file.other import Chibi_csv, Chibi_yaml
from tests.snippet.files import Test_with_files


class Test_chibi_file_resolution_class( Test_with_files ):
    def test_when_the_file_have_a_extension_yaml_should_be_a_yaml( self ):
        f = self.root_dir.temp_file( extension='yml' )
        file_open = f.open()
        self.assertIsInstance( file_open, Chibi_yaml )
        f = self.root_dir.temp_file( extension='yaml' )
        file_open = f.open()
        self.assertIsInstance( file_open, Chibi_yaml )

    def test_when_the_file_have_a_extension_csv_should_be_a_csv( self ):
        f = self.root_dir.temp_file( extension='csv' )
        file_open = f.open()
        self.assertIsInstance( file_open, Chibi_csv )
