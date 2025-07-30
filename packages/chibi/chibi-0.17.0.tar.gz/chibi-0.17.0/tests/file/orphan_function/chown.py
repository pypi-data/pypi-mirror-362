from chibi.file.snippets import chown, stat
from tests.snippet.files import Test_with_files


class Test_chown_to_file( Test_with_files ):
    amount_of_files = 3
    amount_of_dirs = 3

    def test_verbose_when_no_change_the_owners( self ):
        current_stat = stat( self.files[0] )
        with self.assertLogs( level='INFO' ) as cm:
            chown( self.files[0] )
        output = cm.output[0]
        self.assertIn( 'permanece', output )
        self.assertIn(
            '{}:{}'.format(
                current_stat.user.name, current_stat.group.name ),
            output )
