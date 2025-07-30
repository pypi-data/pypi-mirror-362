from unittest import TestCase

from chibi.file.snippets import get_relative_path


class Test_get_relative_path( TestCase ):
    def test_should_return_the_relative_paths( self ):
        result = get_relative_path( '/usr/var/log', '/usr/var/security' )
        self.assertEqual( [ 'log', 'security' ], result  )

    def test_should_return_the_relative_path( self ):
        result = get_relative_path( '/usr/var/log', root='/usr/var' )
        self.assertEqual( 'log', result  )
