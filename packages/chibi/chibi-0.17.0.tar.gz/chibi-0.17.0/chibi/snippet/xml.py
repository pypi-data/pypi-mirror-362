def guaranteed_list( d, *keys ):
    def transform( x ):
        if not x:
            result = []
        elif isinstance( x, list ):
            result = x
        else:
            result = [x]
        return result

    if isinstance( d, dict ):
        for k, v in d.items():
            if k in keys:
                d[ k ] = transform( v )
            guaranteed_list( v, *keys )
    elif isinstance( d, list ):
        for i in d:
            guaranteed_list( i, *keys )
    return d


def compress_dummy_list( d ):
    def transform( self, x ):
        if isinstance( x, list ):
            result = []
            for y in x:
                if isinstance( y, dict ) and len( y ) == 1:
                    result += list( y.values() )
                else:
                    result.append( y )
            return result
        else:
            return x

    if isinstance( d, dict ):
        for k, v in d.items():
            if isinstance( v, dict ) and len( v ) == 1:
                vk = list( v.keys() )[0]
                if vk in k:
                    d[ k ] = v[ vk ]
            compress_dummy_list( d[ k ] )
    elif isinstance( d, list ):
        for i in d:
            compress_dummy_list( i )
    return d
