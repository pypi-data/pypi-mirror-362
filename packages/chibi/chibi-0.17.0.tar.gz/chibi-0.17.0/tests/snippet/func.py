from unittest import TestCase
from chibi.snippet.func import retry_on_exception, delay


class Test_retry( TestCase ):
    def setUp( self ):
        pass

    def test_should_work( self ):
        @retry_on_exception
        def asdf():
            return "hello my world!!!"
        self.assertTrue( asdf(), 'hello my world!!!' )

    def test_if_not_exception_should_fast_fail( self ):
        exceptions = 0

        @retry_on_exception
        def asdf():
            nonlocal exceptions
            exceptions += 1
            raise Exception( exceptions )

        with self.assertRaises( Exception ):
            asdf()
            self.assertEqual( exceptions, 1 )

    def test_by_default_is_going_to_retry_5_times( self ):
        e = 0

        @retry_on_exception
        def asdf():
            nonlocal e
            e += 1
            raise KeyError( 'asdf' )

        with self.assertRaises( KeyError ):
            asdf()
            self.assertEqual( e, 5 )

    def test_when_is_the_exception_should_do_the_retries( self ):
        es = 0

        @retry_on_exception( exceptions=( KeyError ) )
        def asdf():
            nonlocal es
            es += 1
            raise KeyError( 'asdf' )

        with self.assertRaises( KeyError ):
            asdf()
            self.assertEqual( es, 5 )


class Test_delay( TestCase ):
    def setUp( self ):
        pass

    def test_should_work( self ):
        @delay( seconds=1 )
        def asdf():
            return "hello my world!!!"
        self.assertTrue( asdf(), 'hello my world!!!' )
