import unittest
from chibi_atlas.multi import Chibi_atlas_multi


class Test_chibi_atlas_multi( unittest.TestCase ):
    def test_should_work_normal( self ):
        m = Chibi_atlas_multi()
        m[ 'a' ] = 'a'
        m[ 'b' ] = 'b'
        m[ 'c' ] = 'c'

        self.assertEqual( { 'a': 'a', 'b': 'b', 'c': 'c' }, m )

    def test_should_append_the_repeated_keys( self ):
        m = Chibi_atlas_multi()
        m[ 'a' ] = 'a'
        m[ 'a' ] = 'b'
        m[ 'a' ] = 'c'

        self.assertEqual( { 'a': [ 'a', 'b', 'c', ] }, m )

    def test_when_update_should_add_a_list( self ):
        m = Chibi_atlas_multi()
        m[ 'a' ] = 'a'
        d = { 'a': 'b' }
        m.update( d )
        self.assertEqual( m, { 'a': [ 'a', 'b' ] } )
