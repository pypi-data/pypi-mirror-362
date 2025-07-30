from unittest import TestCase
from chibi.chain import Chibi_chain


class Test_chibi_chain( TestCase ):
    def test_should_instance_like_a_normal_list( self ):
        _list = Chibi_chain()
        self.assertFalse( _list )
        _list = Chibi_chain( range( 10 ) )
        self.assertEqual( _list, list( range( 10 ) ) )
        _list = Chibi_chain( [ 0, 1, 2, ] )
        self.assertEqual( _list, list( range( 3 ) ) )

    def test_when_no_has_next_object_the_iter_should_work_like_a_list( self ):
        _list = Chibi_chain( range( 2 ) )
        i = iter( _list )
        self.assertEqual( next( i ), 0 )
        self.assertEqual( next( i ), 1 )
        with self.assertRaises( StopIteration ):
            self.assertEqual( next( i ), 2 )

    def test_when_have_next_object_should_concatenate_the_object( self ):
        _list = Chibi_chain(
            range( 2 ), next_obj=range( 10, 12 ),
            retrieve_next=lambda obj: list( obj ) )
        i = iter( _list )
        self.assertEqual( next( i ), 0 )
        self.assertEqual( next( i ), 1 )
        self.assertEqual( next( i ), 10 )
        self.assertEqual( next( i ), 11 )
        with self.assertRaises( StopIteration ):
            next( i )
        self.assertEqual( list( _list ), [ 0, 1, 10, 11 ] )

    def test_when_the_next_obj_is_a_chibi_chain_should_concatenate( self ):
        n = Chibi_chain( range( 10, 12 ) )
        _list = Chibi_chain(
            range( 2 ), next_obj=n, retrieve_next=lambda obj: obj )
        i = iter( _list )
        self.assertEqual( next( i ), 0 )
        self.assertEqual( next( i ), 1 )
        self.assertEqual( next( i ), 10 )
        self.assertEqual( next( i ), 11 )
        with self.assertRaises( StopIteration ):
            next( i )
        self.assertEqual( list( _list ), [ 0, 1, 10, 11 ] )

    def test_when_have_a_chain_of_chain_should_concatenate_all( self ):
        p = Chibi_chain( range( 20, 22 ) )
        n = Chibi_chain(
            range( 10, 12 ), next_obj=p, retrieve_next=lambda obj: obj )
        _list = Chibi_chain(
            range( 2 ), next_obj=n, retrieve_next=lambda obj: obj )
        i = iter( _list )
        self.assertEqual( next( i ), 0 )
        self.assertEqual( next( i ), 1 )
        self.assertEqual( next( i ), 10 )
        self.assertEqual( next( i ), 11 )
        self.assertEqual( next( i ), 20 )
        self.assertEqual( next( i ), 21 )
        with self.assertRaises( StopIteration ):
            next( i )
        self.assertEqual( list( _list ), [ 0, 1, 10, 11, 20, 21 ] )
