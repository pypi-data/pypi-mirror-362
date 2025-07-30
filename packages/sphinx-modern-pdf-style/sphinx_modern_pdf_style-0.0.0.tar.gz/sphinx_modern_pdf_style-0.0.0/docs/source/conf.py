import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from sphinx_modern_pdf_style import *

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Sphinx modern PDF style'
copyright = '2025, Michael Park'
author = 'Michael Park'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx_modern_pdf_style']

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

# Extension specific config

set_modern_pdf_config = True

modern_pdf_options = {
    "author": "Mr. Author",
    "logo": "test_logo.png"
}

# latex config

latex_additional_files = [
    "_static/pdf/test_logo.png"
]