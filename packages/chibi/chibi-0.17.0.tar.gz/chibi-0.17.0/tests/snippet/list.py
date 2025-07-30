from unittest import TestCase
from chibi.snippet.list import group_by


class Test_group_by( TestCase ):
    def setUp( self ):
        self._list = [
            dict( s='ok' ),
            dict( s='no' ),
            dict( s='fail' ),
            dict( s='fail' ),
            dict( s='ok' ),
            dict( s='ok' ),
        ]
        self.expected = {
            'ok': [ dict( s='ok' ), dict( s='ok' ), dict( s='ok' ), ],
            'fail': [ dict( s='fail' ), dict( s='fail' ), ],
            'no': [ dict( s='no' ), ],
        }

    def test_should_return_expected_result_if_is_a_callable( self ):
        result = group_by( self._list, lambda v: v[ 's' ] )
        self.assertEqual( result, self.expected )

    def test_should_return_expected_result_if_is_a_string( self ):
        result = group_by( self._list, 's' )
        self.assertEqual( result, self.expected )
