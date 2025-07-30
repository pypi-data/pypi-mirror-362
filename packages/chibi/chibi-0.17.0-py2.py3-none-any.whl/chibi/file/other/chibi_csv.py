import csv
import itertools
from chibi.file import Chibi_file
from chibi.atlas import Chibi_atlas


__all__ = [ 'Chibi_csv' ]


class Chibi_csv( Chibi_file ):
    def __init__( self, *args, has_headers=False, **kw ):
        super().__init__( *args, **kw )
        self.has_headers = has_headers

    def transform_to_xlsx( self, output=None ):
        raise NotImplementedError

    def append( self, data ):
        if isinstance( data, dict ):
            if self.headers:
                row = [ data[ h ] for h in self.headers ]
            else:
                self.append( data.keys() )
                self.append( data )
                return
        else:
            row = data
        with open( self.path, 'a' ) as f:
            writer = csv.writer( f )
            writer.writerow( row )

    def read_as_dict( self ):
        reader = csv.DictReader( self.file )
        for r in reader:
            yield Chibi_atlas( r )
        self.reread()

    def read_as_list( self ):
        reader = csv.reader( self.file )
        for r in reader:
            yield r
        self.reread()

    @property
    def headers( self ):
        reader = csv.reader( self.file )
        try:
            headers = next( reader )
            self.reread()
        except StopIteration:
            return None
        if headers:
            return headers
        return None

    def __getitem__( self, y ):
        reader = csv.reader( self.file )
        try:
            last_row = next( itertools.islice( reader, y, y + 1 ) )
            self.reread()
            return last_row
        except StopIteration:
            raise IndexError( "csv index out of range" )
