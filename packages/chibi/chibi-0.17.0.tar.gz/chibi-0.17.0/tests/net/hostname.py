from unittest import TestCase

from chibi.net.hostname import get_hostname


class Test_get_hostname( TestCase ):
    def test_get_hostname( self ):
        self.assertTrue( get_hostname() )
