from unittest import TestCase

from chibi.snippet.string import (
    replace_with_dict, get_the_number_of_parameters, split_in_table,
    remove_inner_space
)


class Test_sp_random( TestCase ):
    def setUp( self ):
        pass

    def test_generate_string( self ):
        string_test = 'case_1, asdf, case_2'
        string_espected = 'case_one, asdf, case_two'
        dict_test = {
            'case_1': 'case_one',
            'case_2': 'case_two',
        }

        result = replace_with_dict( string_test, dict_test )
        self.assertEqual( result, string_espected )

    def test_the_number_parameters( self ):
        strings = [
            "{}",
            "pi-piru {}",
            "{} pi-piru {}",
        ]
        expected = [ 1, 1, 2 ]
        for s, e in zip( strings, expected ):
            r = get_the_number_of_parameters( s )
            self.assertEqual(
                r, e,
                "\nfallo con la cadena {} regreso {} se esperaban {}".format(
                    s, r, e ) )


class Test_split_table( TestCase ):
    def setUp( self ):
        self.table_1 = (
            "Pipiru:     piru-piru        pipiru-pii\n"
            "Pipiru:   piru-piru pipiru-pii\n" )
        self.expected_1 = [
            [ 'Pipiru:', 'piru-piru', 'pipiru-pii' ],
            [ 'Pipiru:', 'piru-piru', 'pipiru-pii' ], [],
        ]

    def test_table_1( self ):
        result = split_in_table( self.table_1 )
        self.assertEqual( self.expected_1, result )


class Test_remove_inner_space( TestCase ):
    def test_should_remove_inner_spaces( self ):
        self.assertEqual( "asdf asdf", remove_inner_space( "asdf   asdf" ) )

    def test_should_remove_inner_new_lines( self ):
        self.assertEqual( "asdf asdf", remove_inner_space( "asdf \n  asdf" ) )
