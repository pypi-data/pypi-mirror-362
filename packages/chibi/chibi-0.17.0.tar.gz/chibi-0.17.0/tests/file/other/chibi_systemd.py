from unittest import TestCase
from chibi.file.temp import Chibi_temp_path
from chibi.file.other import Chibi_systemd


content = """
[Unit]
Description=Network Manager
Documentation=man:NetworkManager(8)
Wants=network.target
After=network-pre.target dbus.service
Before=network.target

[Service]
Type=dbus
BusName=org.freedesktop.NetworkManager
ExecReload=/usr/bin/busctl call org.freedesktop.NetworkManager
#ExecReload=/bin/kill -HUP $MAINPID
ExecStart=/usr/bin/NetworkManager --no-daemon
Restart=on-failure
# NM doesn't want systemd to kill its children for it
KillMode=process
CapabilityBoundingSet=CAP_NET_ADMIN CAP_DAC_OVERRIDE CAP_NET_RAW

ProtectSystem=true
ProtectHome=read-only

[Install]
WantedBy=multi-user.target
Also=NetworkManager-dispatcher.service

# We want to enable NetworkManager-wait-online.service whenever this service
# is enabled. NetworkManager-wait-online.service has
# WantedBy=network-online.target, so enabling it only has an effect if
# network-online.target itself is enabled or pulled in by some other unit.
Also=NetworkManager-wait-online.service
"""


class Test_chibi_service( TestCase ):
    def setUp( self ):
        self.folder = Chibi_temp_path()
        self.file_service = self.folder.temp_file( extension='service' )
        with open( self.file_service, 'w' ) as f:
            f.write( content )

    def test_should_be_a_dict( self ):
        service = Chibi_systemd( self.file_service )
        result = service.read()
        self.assertIsInstance( result, dict )

    def test_should_have_the_3_sections( self ):
        service = Chibi_systemd( self.file_service )
        result = service.read()
        self.assertIn( 'unit', result )
        self.assertIn( 'service', result )
        self.assertIn( 'install', result )

    def test_unit_should_have_the_expected_keys( self ):
        service = Chibi_systemd( self.file_service )
        result = service.read()
        expected = dict(
            Description='Network Manager',
            Documentation='man:NetworkManager(8)',
            Wants='network.target',
            After='network-pre.target dbus.service',
            Before='network.target' )
        self.assertIn( 'unit', result )
        self.assertEqual( result.unit, expected )

    def test_write_should_write_update_the_file_using_systemd_format( self ):
        service = Chibi_systemd( self.file_service )
        result = service.read()
        result.service.TimeoutSec = '900'
        service.write( result )
        result_after_save = service.read()
        self.assertEqual( result, result_after_save )
