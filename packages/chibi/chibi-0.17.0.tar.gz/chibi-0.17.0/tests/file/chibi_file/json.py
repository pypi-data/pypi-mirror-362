from tests.snippet.files import Test_with_files
import json
from chibi.file import Chibi_file
from chibi.file.other import Chibi_json


class Test_chibi_file_json( Test_with_files ):
    def setUp( self ):
        super().setUp()
        self.file_path = self.root_dir.temp_file( extension='json' )
        self.chibi_file = Chibi_file( self.file_path )
        self.data = { 'a': 'a' }
        self.json_data = json.dumps( self.data )

    def test_should_be_the_correct_instance( self ):
        self.assertIsInstance( self.chibi_file, Chibi_json )

    def test_should_can_write_and_read_json( self ):
        whole_file = "".join( self.chibi_file.chunk() )
        self.assertFalse( whole_file, "el archivo no esta vacio" )
        self.chibi_file.write( self.data )
        whole_file = "".join( self.chibi_file.chunk() )
        self.assertEqual( whole_file, self.json_data )

        result = self.chibi_file.read()
        self.assertIsInstance( result, dict )
        self.assertEqual( result, self.data )
