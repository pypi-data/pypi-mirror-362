from unittest import TestCase, skip
from chibi.file.temp import Chibi_temp_path
from chibi.file.other import Chibi_csv


class Test_chibi_csv( TestCase ):
    def setUp( self ):
        self.folder = Chibi_temp_path()
        self.file_csv = self.folder.temp_file( extension='csv' )

    def test_should_append_the_range( self ):
        csv = Chibi_csv( self.file_csv )
        csv.append( range( 10 ) )
        csv.append( range( 10 ) )
        csv.append( range( 10 ) )
        csv.append( range( 10 ) )
        result = list( csv.read_as_list() )
        self.assertTrue( result )
        self.assertEqual( len( result ), 4 )

    def test_should_append_dicts( self ):
        csv = Chibi_csv( self.file_csv )
        csv.append( { 'cosa1': '1', 'cosa2': '3', 'cosa3': '9' } )
        csv.append(
            { 'cosa1': '1', 'cosa2': '3', 'cosa3': '9', 'cosa4': 'a' } )
        csv.append( { 'cosa1': '1', 'cosa2': '3', 'cosa3': '9' } )
        result = list( csv.read_as_dict() )
        self.assertEqual( len( result ), 3 )
        for r in result:
            self.assertIsInstance( r, dict  )
            self.assertTrue( r )
            self.assertEqual( { 'cosa1': '1', 'cosa2': '3', 'cosa3': '9' }, r )

    def test_should_read_the_file_using_x_y_index( self ):
        csv = Chibi_csv( self.file_csv )
        csv.append( range( 10 ) )
        csv.append( range( 10, 20 ) )
        csv.append( range( 20, 30 ) )
        csv.append( range( 30, 40 ) )
        self.assertEqual( csv[0], list( str( i ) for i in range( 10 ) ) )
        self.assertEqual( csv[1], list( str( i ) for i in range( 10, 20  ) ) )
        self.assertEqual( csv[2], list( str( i ) for i in range( 20, 30  ) ) )
        self.assertEqual( csv[3], list( str( i ) for i in range( 30, 40  ) ) )

    def test_should_raise_a_exception_when_out_of_range( self ):
        csv = Chibi_csv( self.file_csv )
        csv.append( range( 10 ) )
        with self.assertRaises( IndexError ):
            csv[1]

    @skip( (
        'esta prueba esta incompleta porque cambiara el '
        'funcionamiento de los headers' ) )
    def test_when_append_dict_should_be_marked_like_has_headers( self ):
        self.fail( 'incomplreto' )
        csv = Chibi_csv( self.file_csv )
        self.assertFalse( csv.has_headers )
        csv.append( { 'cosa1': '1', 'cosa2': '3', 'cosa3': '9' } )
        csv.append(
            { 'cosa1': '1', 'cosa2': '3', 'cosa3': '9', 'cosa4': 'a' } )
        csv.append( { 'cosa1': '1', 'cosa2': '3', 'cosa3': '9' } )
        result = list( csv.read_as_dict() )
        self.assertEqual( len( result ), 3 )
        for r in result:
            self.assertIsInstance( r, dict  )
            self.assertTrue( r )
            self.assertEqual( { 'cosa1': '1', 'cosa2': '3', 'cosa3': '9' }, r )
