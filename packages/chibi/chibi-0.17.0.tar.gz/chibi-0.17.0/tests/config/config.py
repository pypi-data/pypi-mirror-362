import logging
import unittest
from unittest.mock import patch

from chibi import config
from chibi.atlas import Chibi_atlas
from chibi.config import Configuration, default_file_load, _build_config_path
from chibi.config.config import Logger, Env_vars
from tests.snippet.files import Test_with_files


class Test_load_config( Test_with_files ):
    def test_should_load_the_settings_from_a_pyton_file( self ):
        python_file = self.root_dir.temp_file( extension='py' )
        self.assertNotIn( 'hello', config.configuration  )
        with python_file as f:
            f.append( 'from chibi.config import configuration\n' )
            f.append( 'configuration.hello = "asdf"' )

        config.load( python_file )
        self.assertEqual( config.configuration.hello, 'asdf' )

    def test_when_read_a_json_should_put_all_the_content_in_the_config( self ):
        json_file = self.root_dir.temp_file( extension='json' )
        self.assertNotIn( 'json_hello', config.configuration  )
        with json_file as f:
            f.write( { 'json_hello': '1234567890' } )

        config.load( json_file )
        self.assertEqual( config.configuration.json_hello, '1234567890' )

    def test_when_read_a_yaml_should_put_all_the_content_in_the_config( self ):
        yaml_file = self.root_dir.temp_file( extension='yaml' )
        self.assertNotIn( 'yaml_hello', config.configuration  )
        with yaml_file as f:
            f.write( { 'yaml_hello': 'qwertyuiop' } )

        config.load( yaml_file )
        self.assertEqual( config.configuration.yaml_hello, 'qwertyuiop' )


class Test_config_default_factory( unittest.TestCase ):
    def setUp( self ):
        super().setUp()
        self.config = Configuration()

    def test_should_create_chibi_atlas_by_default( self ):
        self.assertNotIn( 'new_config', self.config )
        result = self.config.new_config
        self.assertIsInstance( result, Chibi_atlas )


class Test_logger( unittest.TestCase ):
    def setUp( self ):
        super().setUp()
        from chibi.config import configuration
        self.config = configuration
        self.logger = logging.getLogger( 'test.config' )

    def test_should_return_a_instance_of_logger( self ):
        logger = self.config.loggers[ 'test.config' ]
        self.assertIsInstance( logger, Logger )

    def test_should_return_the_current_level( self ):
        logger = self.config.loggers[ 'test.config' ]
        self.assertEqual( logger.level, self.logger.parent.level )

    def test_when_is_set_the_level( self ):
        logger = self.config.loggers[ 'test.config' ]
        current_level = self.logger.level
        logger.level = logging.INFO
        self.assertEqual( logger.level, self.logger.level )
        logger.level = current_level


class Test_envars( unittest.TestCase ):
    def setUp( self ):
        super().setUp()
        from chibi.config import configuration
        self.envars_fixture = {
            'simple': 'simple_value',
            'double__single': 'single_value',
            'double__inner__out': 'out_value',
        }
        self.config = configuration

    def test_envars_should_no_be_empty( self ):
        self.assertTrue( self.config.env_vars )

    def test_envars_should_are_similar_to_chibi_atlas( self ):
        with patch.dict( 'os.environ', self.envars_fixture ):
            envars = Env_vars()
            self.assertEqual( envars.simple, 'simple_value' )
            self.assertEqual( envars.double.single, 'single_value' )
            self.assertEqual( envars.double.inner.out, 'out_value' )


class Test_default_file_load( unittest.TestCase ):
    def setUp( self ):
        super().setUp()
        from chibi.config import configuration
        self.config = configuration

    def test_should_work( self ):
        default_file_load()

    @patch( 'chibi.config._should_load_config_file' )
    @patch( 'chibi.config.load' )
    def test_should_call_load_funtion( self, load, should_load ):
        should_load.return_value = True
        default_file_load()
        load.assert_called_once()

    @patch( 'chibi.config._should_load_config_file' )
    @patch( 'chibi.config.load' )
    def test_should_load_other_default_configs( self, load, should_load ):
        should_load.return_value = True
        default_file_load( 'other.py' )
        load.assert_called_once()
        config_file = load.mock_calls[0].args[0]
        self.assertEqual( config_file.base_name, 'other.py' )

    @patch( 'chibi.config._should_load_config_file' )
    @patch( 'chibi.config.load' )
    def test_when_should_load_is_false_should_no_load(
            self, load, should_load ):
        should_load.return_value = False
        default_file_load()
        load.assert_not_called()

    def test_with_touch_should_create_the_file( self ):
        config_home = _build_config_path()
        config_file = config_home + 'other.py'
        if config_file.exists:
            self.fail( f'el config file {config_file} existe' )
        default_file_load( 'other.py', touch=True )
        self.assertTrue(
            config_file.exists, f'el config file {config_file} no se creo' )
        config_file.delete()

    @patch( 'chibi.config._build_config_path' )
    def test_when_no_have_home_should_nothing( self, build_config ):
        build_config.return_value = None
        default_file_load()
