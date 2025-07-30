from unittest import TestCase
from chibi.file.temp import Chibi_temp_path
from chibi.file.other import Chibi_conf


content = """
; Start a new pool named 'www'.
[www]

; Unix user/group of processes
; Note: The user is mandatory. If the group is not set, the
; default user's group
;       will be used.
; RPM: apache Choosed to be able to access some dir as httpd
user = apache
; RPM: Keep a group allowed to write in log dir.
group = apache

; The address on which to accept FastCGI requests.
; Valid syntaxes are:
;   'ip.add.re.ss:port'    - to listen on a TCP socket to a specific
;                            a specific port;
;   '[ip:6:addr:ess]:port' - to listen on a TCP socket to a specific
;                            a specific port;
;   'port'                 - to listen on a TCP socket to all addresses
;                            (IPv6 and IPv4-mapped) on a specific port;
;   '/path/to/unix/socket' - to listen on a unix socket.
; Note: This value is mandatory.
listen = 127.0.0.1:9000

; Set listen(2) backlog.
; Default Value: 511 (-1 on FreeBSD and OpenBSD)
;listen.backlog = 511

; Set permissions for unix socket, if one is used. In Linux, read/write
; permissions must be set in order to allow connections from a web server. Many
; BSD-derived systems allow connections regardless of permissions.
; Default Values: user and group are set as the running user
;                 mode is set to 0660
;listen.owner = nobody
;listen.group = nobody
;listen.mode = 0660
; When POSIX Access Control Lists are supported you can set them using
; these options, value is a comma separated list of user/group names.
; When set, listen.owner and listen.group are ignored
;listen.acl_users =
;listen.acl_groups =

; List of addresses (IPv4/IPv6) of FastCGI clients which are
; Equivalent to the FCGI_WEB_SERVER_ADDRS environment variable
; PHP FCGI (5.2.2+). Makes sense only with a tcp listening socket
; must be separated by a comma. If this value is left blank, connections
; accepted from any ip address.
; Default Value: any
listen.allowed_clients = 127.0.0.1
"""


class Test_chibi_conf( TestCase ):
    def setUp( self ):
        self.folder = Chibi_temp_path()
        self.file_service = self.folder.temp_file( extension='conf' )
        with open( self.file_service, 'w' ) as f:
            f.write( content )

    def test_should_be_a_dict( self ):
        conf = Chibi_conf( self.file_service )
        result = conf.read()
        self.assertIsInstance( result, dict )

    def test_should_have_expected_data( self ):
        conf = Chibi_conf( self.file_service )
        result = conf.read()
        expected = {
            'www': {
                'group': 'apache',
                'listen': '127.0.0.1:9000',
                'listen.allowed_clients': '127.0.0.1',
                'user': 'apache',
            }
        }
        self.assertEqual( result, expected )

    def test_when_change_variable_should_work( self ):
        conf = Chibi_conf( self.file_service )
        result = conf.read()
        result[ 'www' ][ 'user' ] = 'qwert'
        conf.write( result )
        result_2 = conf.read()
        expected = {
            'www': {
                'group': 'apache',
                'listen': '127.0.0.1:9000',
                'listen.allowed_clients': '127.0.0.1',
                'user': 'qwert',
            }
        }
        self.assertEqual( result_2, expected )
