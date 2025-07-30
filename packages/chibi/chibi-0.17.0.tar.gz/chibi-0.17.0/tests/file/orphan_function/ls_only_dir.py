from chibi.file.snippets import ls_only_dir, is_dir
from tests.snippet.files import Test_with_files


class Test_ls_only_dir( Test_with_files ):
    def test_should_list_all_dirs_and_not_the_files_from_root( self ):
        result = list( ls_only_dir( self.root_dir ) )
        self.assertTrue( result, "cannot find dirs in the root dir" )
        for dir in result:
            self.assertTrue( ( self.root_dir + dir ).is_a_folder )

    def test_should_return_a_empty_list( self ):
        result = list( ls_only_dir( self.empty_folder ) )
        self.assertFalse( result )

    def test_when_is_not_the_current_folder_should_get_the_dirs( self ):
        for dir_level_1 in self.dirs:
            directories_in_sub_folder = list( ls_only_dir( dir_level_1 ) )
            self.assertTrue(
                directories_in_sub_folder,
                "cannot find dirs in the the dir: {}".format(
                    directories_in_sub_folder ) )

            for dir in directories_in_sub_folder:
                abs_dir = dir_level_1 + dir
                self.assertTrue(
                    is_dir( abs_dir ),
                    "is was find the dir {} but is not a dir".format(
                        abs_dir ) )
