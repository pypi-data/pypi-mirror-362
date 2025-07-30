import copy
import math


class End_book( Exception ):
    pass


class Book:
    """
    clase que representa la metafora de libros y separacion de paginas

    Arguments
    ---------
    total_elements: int
        numero de elementos individuales
    page_size: int
        tamaño de la pagina
    page: int default 1
        pagina con la que iniciara el libro
    min_page: int default 1
        minima pagina del libro
    offset_dict: dict default { 'page': 'page', 'page_size': 'page_size' }
        formato del offset que se generara

    Examples
    --------
    >>>book = Book( total_elements=30, page_size=10 )
    >>>assert book.total_pages == 3
    >>>assert book.page == 1
    >>>book.next()
    >>>assert book.page == 2
    >>>assert book.offset == { 'page': 2, 'page_size': 10 }
    """
    def __init__(
            self, total_elements, page_size, page=1, min_page=1,
            offset_dict=None ):
        self.total_elements = total_elements
        self.page_size = page_size
        self.page = page
        self.min_page = min_page
        if not offset_dict:
            offset_dict = { 'page': 'page', 'page_size': 'page_size' }
        self.offset_dict = offset_dict

    def __repr__( self ):
        return (
            f"{self.__class__.__name__}( page={self.page}, "
            f"page_size={self.page_size}, "
            f"total_elements={self.total_elements} )"
        )

    def next( self ):
        if self.page >= self.total_pages:
            raise End_book
        self.page += 1

    def prev( self ):
        if self.page <= self.min_page:
            raise End_book
        self.page -= 1

    @property
    def total_pages( self ):
        return math.ceil( self.total_elements / self.page_size )

    @property
    def offset( self ):
        return {
            v: getattr( self, k, None ) for k, v in self.offset_dict.items() }

    def __iter__( self ):
        temp_book = copy.copy( self )
        yield temp_book
        try:
            while True:
                temp_book.next()
                yield temp_book
        except End_book:
            pass
