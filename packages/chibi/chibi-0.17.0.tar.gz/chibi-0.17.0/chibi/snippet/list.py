from chibi.atlas import Chibi_atlas


def group_by( _list, key ):
    """
    agrupa por alguna llave

    Arguments
    =========
    _list: list, tuple, finite iter
    key: callable or str
        funcion que separara los elementos
        si es un string se asume que los elementos son dicionarios
        y el valor de key se usara para obtener el valor

    Return:
        Chibi_atlas
            la llave es el valor del key y el valor es una lista
            de con los elementos de ese key
    """
    if isinstance( key, str ):
        return _group_by_str( _list, key )
    elif callable( key ):
        return _group_by_callable( _list, key )
    else:
        raise NotImplementedError(
            f'no esta implementado si la llave es un tipo {type( key )}' )


def _group_by_str( _list, key ):
    result = Chibi_atlas()
    for item in _list:
        value = item[ key ]
        try:
            result[ value ].append( item )
        except KeyError:
            result[ value ] = [ item ]
    return result


def _group_by_callable( _list, key ):
    result = Chibi_atlas()
    for item in _list:
        value = key( item )
        try:
            result[ value ].append( item )
        except KeyError:
            result[ value ] = [ item ]
    return result
