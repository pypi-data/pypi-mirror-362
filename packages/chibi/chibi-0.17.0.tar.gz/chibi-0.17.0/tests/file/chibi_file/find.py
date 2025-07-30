from tests.snippet.files import Test_with_files
from chibi.file import Chibi_file


class Test_find( Test_with_files ):
    def setUp( self ):
        super().setUp()
        self.chibi_file = Chibi_file( self.files_with_content[0] )

    def test_should_no_fail( self ):
        result = self.chibi_file.find( '' )
        self.assertFalse( result )

    def test_should_find_the_text( self ):
        self.chibi_file.write( 'Pipiru-piru-piru-pipiru-pii' )
        result = self.chibi_file.find( 'piru' )
        self.assertTrue( result )
        self.assertTrue( 'piru' in self.chibi_file )

    def test_should_no_find_the_text( self ):
        self.chibi_file.write( 'Pipiru-piru-piru-pipiru-pii' )
        result = self.chibi_file.find( 'poro' )
        self.assertTrue( result == -1 )
        self.assertFalse( 'poro' in self.chibi_file )
