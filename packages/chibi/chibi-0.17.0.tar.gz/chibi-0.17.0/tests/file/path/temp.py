from chibi.file.temp import Chibi_temp_path
from chibi.file import Chibi_path
from tests.snippet.files import Test_with_files


class Test_path_temp( Test_with_files ):
    def test_when_is_delete_should_remove_the_folder( self ):
        path = Chibi_temp_path()
        path_str = str( path )
        self.assertTrue( Chibi_path( path ).exists )
        del path
        self.assertFalse( Chibi_path( path_str ).exists )

    def test_when_add_string_should_return_a_chibi_path( self ):
        path = Chibi_temp_path()
        result = path + "hello"
        self.assertIsInstance( result, Chibi_path )
        self.assertIn( str( path ), result )
        self.assertIn( "hello", result )

    def test_should_create_a_file( self ):
        f = self.root_dir.temp_file()
        self.assertIsInstance( f, Chibi_path )
        self.assertTrue( f.exists )

    def test_should_create_a_file_with_extencion( self ):
        f = self.root_dir.temp_file( extension='temp' )
        self.assertEqual( 'temp', f.extension )

    def test_if_set_to_be_permanent_should_no_delete_the_folder_on_del( self ):
        path = Chibi_temp_path( delete_on_del=False )
        path_str = str( path )
        self.assertTrue( Chibi_path( path ).exists )
        del path
        self.assertTrue( Chibi_path( path_str ).exists )
