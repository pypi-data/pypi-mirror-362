from tests.snippet.files import Test_with_files
from chibi.file import Chibi_file


class Test_chibi_file_binary( Test_with_files ):
    def setUp( self ):
        super().setUp()
        self.file_path = self.root_dir.temp_file( extension='bin' )
        self.chibi_file = Chibi_file( self.file_path, is_binary=True )
        self.data = b"asdf"
        self.chibi_file.write( self.data )

    def test_should_have_the_property_assigned( self ):
        self.assertTrue( self.chibi_file.is_binary  )
        no_binary = Chibi_file( self.file_path, is_binary=False )
        self.assertFalse( no_binary.is_binary )

    def test_should_read_the_file_like_binary( self ):
        data = self.chibi_file.read()
        self.assertIsInstance( data, ( bytes, bytearray ) )

    def test_read_should_return_the_expected( self ):
        data = self.chibi_file.read()
        self.assertEqual( data, self.data )
