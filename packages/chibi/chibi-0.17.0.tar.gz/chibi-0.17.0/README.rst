=====
chibi
=====

.. image:: https://img.shields.io/pypi/v/chibi.svg
        :target: https://pypi.python.org/pypi/chibi

.. image:: https://readthedocs.org/projects/chibi/badge/?version=latest
    :target: https://chibi.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


python snippets and other useful things

this package is for i can put snippets and other useful things
and i do not need to write the same thing for fifth time


* Free software: WTFPL
* Documentation: https://chibi-apache.readthedocs.io.

*************
cosas utitles
*************

Chibi_path
==========

the chibi path work like strings but with operators have sense for folders
and files

.. code-block:: python

	from chibi.file import Chibi_path

	tmp = Chibi_path( '/tmp/folder' )
	isinstance( tmp, str ) == True
	tmp.mkdir()
	# return a generator with all the files and folders in
	# the path
	ls = list( tmp.ls() )
	print( ls )
	p = tmp + 'file.json'
	str( p ) == '/tmp/folder/file.json'
	f = p.open()
	f.write('some string')
	# check the file to see if it contains the string
	'some string' in f

	# write a dict like json in the file
	f.write( { 'stuff': 'str' } )
	# read the json and transform the dict in a Chibi_atlas
	json = f.read()
	json.stuff == 'str'

	# the same but in yaml
	f = tmp + 'file.yaml'
	y = f.open()

	y.write( { 'stuff': 'str' } )
	yaml = y.read()
	yaml.stuff == 'str'


Chibi_atlas
===========

esta herramienta se migro al paquete chibi-atlas

this is a dict but his keys can be access like attribute

.. code-block:: python

	from chibi.atlas import Chibi_atlas


	c = Chibi_atlas( { 'stuff': 'str', 'l': [ 1, { 'more_stuff': 'str_2' } ] } )
	isinstance( c, dict ) == True
	c.stuff == 'str'
	c.l[0] == 1
	c.l[1].more_stuff == 'str_2'
