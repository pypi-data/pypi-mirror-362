from unittest import TestCase

from chibi.file import Chibi_path
from chibi.file.snippets import inflate_dir


class Test_inflate_dir( TestCase ):
    def test_inflate_dir_should_inflate_current_dir( self ):
        result = inflate_dir( '.' )
        expected = Chibi_path.current_dir()

        self.assertEqual( result, expected )

    def test_inflate_dir_should_inflate_parent_dir( self ):
        current = inflate_dir( '.' )
        parent = inflate_dir( '..' )

        self.assertTrue( current.startswith( parent ) )

    def test_inflate_dir_should_inflate_home_dir( self ):
        home = inflate_dir( '~' )

        self.assertIn( 'home', home )

    def test_inflate_dir_should_no_change_root( self ):
        root = inflate_dir( '/' )
        self.assertEqual( '/', root )
