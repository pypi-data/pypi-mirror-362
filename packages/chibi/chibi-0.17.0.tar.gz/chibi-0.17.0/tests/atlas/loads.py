from unittest import TestCase

from chibi.atlas import loads, Chibi_atlas


class Test_loads_json( TestCase ):
    def setUp( self ):
        self.string = """
        { "tests": { "test_1": "123" } }
        """

    def test_should_return_a_chibi_atlas( self ):
        result = loads( self.string )
        self.assertIsInstance( result, Chibi_atlas )
        self.assertTrue( result )


class Test_loads_yaml( Test_loads_json ):
    def setUp( self ):
        self.string = """martin:
    name: Martin D'vloper
    job: Developer
    skills:
    - python
    - perl
    - pascal
tabitha:
    name: Tabitha Bitumen
    job: Developer
    skills:
    - lisp
    - fortran
    - erlang

        """


class Test_loads_xml( Test_loads_json ):
    def setUp( self ):
        self.string = """<?xml version="1.0" encoding="UTF-8"?>
        <note>
            <to>Tove</to>
            <from>Jani</from>
            <heading>Reminder</heading>
            <body>Don't forget me this weekend!</body>
        </note>
        """
