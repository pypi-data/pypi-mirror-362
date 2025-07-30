from unittest import TestCase

from chibi.snippet.table import _clean_empty_strings


class test_helpers(TestCase):
    def test_generate_string( self ):
        result = _clean_empty_strings( [ 'a', '', 'b', '', 'c', '' ] )
        self.assertListEqual( [ 'a', 'b', 'c' ], result )
