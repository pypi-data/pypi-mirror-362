from tests.snippet.files import Test_with_files
from chibi.file import Chibi_file


class Test_chibi_file_append( Test_with_files ):
    def setUp( self ):
        super().setUp()
        self.chibi_file = Chibi_file( self.files_with_content[0] )
        self.chibi_file_other = Chibi_file( self.files_with_content[1] )

    def test_should_add_more_text( self ):
        whole_file = "".join( self.chibi_file.chunk() )
        self.assertTrue( whole_file, "el archivo esta vacio" )

        self.chibi_file.append( 'explosion!!!' )
        whole_file_before = "".join( self.chibi_file.chunk() )
        self.assertNotEqual( whole_file, whole_file_before )
        self.assertGreater( whole_file_before, whole_file )

    def test_should_work_the_plus_equal__str( self ):
        whole_file = "".join( self.chibi_file.chunk() )
        self.assertTrue( whole_file, "el archivo esta vacio" )

        self.chibi_file += 'explosion!!!'
        whole_file_before = "".join( self.chibi_file.chunk() )

        self.assertNotEqual( whole_file, whole_file_before )
        self.assertGreater( whole_file_before, whole_file )

    def test_should_work_the_plus_equal__himself( self ):
        whole_file = "".join( self.chibi_file.chunk() )
        self.assertTrue( whole_file, "el archivo esta vacio" )

        self.chibi_file += self.chibi_file
        whole_file_before = "".join( self.chibi_file.chunk() )

        self.assertNotEqual( whole_file, whole_file_before )
        self.assertEqual( whole_file * 2, whole_file_before )

    def test_should_work_the_plus_equal__another_file( self ):
        whole_file = "".join( self.chibi_file.chunk() )
        whole_file_other = "".join( self.chibi_file_other.chunk() )
        self.assertTrue( whole_file, "el archivo esta vacio" )
        self.assertTrue( whole_file_other, "el archivo esta vacio" )

        self.chibi_file += self.chibi_file_other
        whole_file_before = "".join( self.chibi_file.chunk() )

        self.assertNotEqual( whole_file, whole_file_before )
        self.assertEqual( whole_file + whole_file_other, whole_file_before )
