from chibi.file import Chibi_file
from chibi.file.snippets import add_extensions
from chibi.file.path import Chibi_path


class Chibi_image( Chibi_file ):
    @property
    def dimension( self ):
        return self._PIL.size

    @property
    def _PIL( self ):
        raise NotImplementedError
        from PIL import Image
        return Image.open( self.path )

    def read_cv2( self ):
        import cv2 as cv
        return cv.imread( self.path, cv.IMREAD_COLOR )

    def read_cv( self ):
        import cv2 as cv
        return cv.imread( self.path, cv.IMREAD_COLOR )

    def read_cv_gray( self ):
        import cv2 as cv
        return cv.imread( self.path, cv.IMREAD_GRAYSCALE )

    def __eq__( self, other ):
        if not isinstance( other, Chibi_image ):
            return False
        return (
            self.properties.mime == other.properties.mime
            and self.dimension == other.dimension
            and self.properties.size == other.properties.size
        )

    def thumbnail( self, path, size=( 64, 64 ) ):
        path = Chibi_path( path )
        if ( path.is_a_folder ):
            path = path + add_extensions( self.file_name, 'thumbnail' )
            thumbnail = self._PIL.copy()
            thumbnail.thumbnail( size )
            thumbnail.save( path )
            return type( self )( path )
        else:
            raise NotImplementedError

    def show( self ):
        return self._PIL.show()

    '''
    @property
    def flatter( self, h, w ):
        import cv2 as cv
        row = cv.resize(
            image,( h, w ), interpolation=cv.INTER_AREA ).flatten()
        col = cv.resize(
            image,( h, w ), interpolation=cv2.INTER_AREA ).flatten( 'F' )
        return col, row
    '''
