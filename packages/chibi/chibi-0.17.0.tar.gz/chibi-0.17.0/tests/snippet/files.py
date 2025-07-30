import tempfile
from unittest import TestCase

from faker import Factory as Faker_factory

from chibi.file import Chibi_file, Chibi_path
from chibi.file.snippets import cd
from chibi.file.temp import Chibi_temp_path


faker = Faker_factory.create()


class Test_with_files( TestCase ):
    amount_of_files = 3
    amount_of_dirs = 3
    amount_of_files_with_content = 3
    amount_of_inner_dirs = 3

    defined_folders = []
    defined_files = []

    def setUp(self):
        self.root_dir = Chibi_temp_path()
        self.empty_folder = Chibi_temp_path()
        self.folder_with_files_with_content = Chibi_temp_path()
        self.files = [  ]

        self.files = [
            self.root_dir.temp_file()
            for i in range( self.amount_of_files ) ]
        self.dirs = [
            self.root_dir.temp_dir()
            for i in range( self.amount_of_dirs ) ]

        for dir_level_1 in self.dirs:
            for i in range( self.amount_of_inner_dirs ):
                tempfile.mkdtemp( dir=str( dir_level_1 ) )

        self.files_with_content = []
        for i in range( self.amount_of_files_with_content ):
            file_path = self.folder_with_files_with_content.temp_file()
            file_path.open().write(
                faker.text(max_nb_chars=200, ext_word_list=None) )
            self.files_with_content.append( file_path )

        for f in self.defined_folders:
            ( self.root_dir + f ).mkdir()

        for f in self.defined_files:
            Chibi_file( self.root_dir + f )


class Test_moving_dir( TestCase ):
    def setUp( self ):
        self.origin_dir = Chibi_path.current_dir()

    def tearDown(self):
        cd( self.origin_dir )
