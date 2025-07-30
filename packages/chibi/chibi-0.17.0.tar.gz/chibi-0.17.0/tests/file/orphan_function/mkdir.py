from chibi.file.snippets import mkdir, exists
from tests.snippet.files import Test_with_files


class Test_mkdir( Test_with_files ):
    def test_create_a_new_dir_and_that_exists_should_be_ok_in_default( self ):
        mkdir( self.dirs[0] )

    def test_create_a_new_dir_and_that_exists_should_be_should_raise( self ):
        with self.assertRaises( OSError ):
            mkdir( self.dirs[0], False )

    def test_print_the_directory_name_when_is_verbose( self ):
        with self.assertLogs( level='INFO' ) as cm:
            new_dir = self.dirs[0] + 'asdf'
            if exists( new_dir ):
                self.fail(
                    "el directiorio {} ya existe usar"
                    "otro nombre".format( new_dir ) )

            mkdir( new_dir, verbose=True )
            if not exists( new_dir ):
                self.fail(
                    "no se creo el directorio {} ".format( new_dir ) )

        message_print = cm.output[0]
        self.assertRegex( message_print, r".+'{}'".format( new_dir ) )

    def test_if_the_directory_no_exists_should_create( self ):
        new_dir = self.dirs[0] + 'asdf'
        if exists( new_dir ):
            self.fail(
                "el directiorio {} ya existe usar"
                "otro nombre".format( new_dir ) )
        mkdir( new_dir, verbose=False )
        if not exists( new_dir ):
            self.fail(
                "no se creo el directorio {} ".format( new_dir ) )
