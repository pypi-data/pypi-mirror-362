import random

from faker import Factory as Faker_factory

from chibi.file.snippets import move, exists, ls, get_file_from_path
from tests.snippet.files import Test_with_files


faker = Faker_factory.create()


class Test_move( Test_with_files ):
    def test_when_move_a_empty_file_should_create_a_new_empty_file( self ):
        file = random.choice( self.files )
        dest = self.root_dir + faker.file_name()
        self.assertFalse( dest.exists )
        with open( file ) as file_str:
            self.assertFalse( file_str.read() )

        move( file, dest )
        self.assertFalse( exists( file ) )
        with open( dest ) as file_dest:
            self.assertFalse( file_dest.read() )

    def test_when_move_a_file_with_content_should_have_the_content( self ):
        file = random.choice( self.files_with_content )
        dest = self.root_dir + faker.file_name()
        self.assertFalse( dest.exists )
        with open( file ) as file_src:
            str_data = file_src.read()

        move( file, dest )
        self.assertFalse( exists( file ) )
        with open( dest ) as file_dest:
            self.assertEqual( str_data, file_dest.read() )

    def test_when_move_with_wild_card_should_move_all_the_files( self ):
        self.assertTrue( list( ls( self.folder_with_files_with_content ) ) )
        files = list( ls( self.folder_with_files_with_content ) )
        source = self.folder_with_files_with_content + '*'
        move( source, self.root_dir )
        for f in files:
            self.assertFalse( exists( f ) )

        files = [ get_file_from_path( f ) for f in files ]

        for f in files:
            self.assertTrue( ( self.root_dir + f ).exists )
