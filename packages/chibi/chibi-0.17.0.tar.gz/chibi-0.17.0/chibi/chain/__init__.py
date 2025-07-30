class Chibi_chain( list ):
    def __init__( self, *args, next_obj=None, retrieve_next=None, **kw ):
        super().__init__( *args, **kw )
        self.next_obj = next_obj
        self.retrieve_next = retrieve_next
        self._validate_next_obj()

    def __iter__( self ):
        iterador = super().__iter__()
        for i in iterador:
            yield i
        if self.next_obj:
            next_obj = self.retrieve_next( self.next_obj )
            self.next_obj = None
            next_obj_iter = iter( next_obj )
            for i in next_obj_iter:
                self.append( i )
                yield i

    def _validate_next_obj( self ):
        if self.next_obj is not None and self.retrieve_next is None:
            raise NotImplementedError(
                "se nesesita una definicion de funcion para obtener "
                "los siguientes items" )

        if self.next_obj is not None and not callable( self.retrieve_next ):
            raise NotImplementedError(
                "retrieve_next deberia de ser llamable" )
        return True
