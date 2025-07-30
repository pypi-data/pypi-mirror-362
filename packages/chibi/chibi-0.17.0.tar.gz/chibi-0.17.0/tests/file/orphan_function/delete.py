import random

from faker import Factory as Faker_factory

from chibi.file.snippets import delete, exists
from tests.snippet.files import Test_with_files


faker = Faker_factory.create()


class Test_delete( Test_with_files ):
    def test_when_delete_a_file_should_no_exists( self ):
        file = random.choice( self.files )
        self.assertTrue( exists( file ) )
        delete( file )
        self.assertFalse( exists( file ) )

    def test_whe_delete_a_dir_should_removed( self ):
        dir = random.choice( self.dirs )
        self.assertTrue( exists( dir ) )
        delete( dir )
        self.assertFalse( exists( dir ) )
