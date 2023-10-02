import sys
import os


sys.path.insert(0, os.path.abspath('../..'))

project = 'Tg Bot Api'
author = 'Elnar Mengelbaev'
release = '1.1.0'

extensions = [
    'sphinx.ext.doctest',
    'sphinxcontrib.autodoc_pydantic',
    'sphinx.ext.viewcode',
    'sphinx.ext.autodoc.typehints',
]

autodoc_pydantic_model_show_json = False
autodoc_pydantic_model_show_field_summary = False
autodoc_typehints = 'description'
exclude_patterns = []
language = 'en'
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
templates_path = ['_templates']
