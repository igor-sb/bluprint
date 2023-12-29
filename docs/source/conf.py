# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'bluprint'
copyright = '2023, Igor Segota'
author = 'Igor Segota'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.githubpages",
	"sphinx_copybutton",
]

templates_path = ['_templates']
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'sphinx_rtd_theme'
# html_theme = 'sphinxawesome_theme'
html_theme = 'sphinx_material'
html_static_path = ['_static']
html_css_files = [
    'css/custom.css',
]

html_theme_options = {

    # Set the name of the project to appear in the navigation.
    'nav_title': 'Bluprint',

    # Specify a base_url used to generate sitemap.xml. If not
    # specified, then no sitemap will be built.
    'base_url': 'https://igor-sb.github.io/bluprint',

    # Set the color and the accent color
    'color_primary': 'blue',
    'color_accent': 'light-blue',

    # Set the repo location to get a badge with stats
    'repo_url': 'https://github.com/igor-sb/bluprint/',
    'repo_name': 'Github',
	'repo_type': 'github',

    # Visible levels of the global TOC; -1 means unlimited
    'globaltoc_depth': 1,
    # If False, expand all TOC entries
    'globaltoc_collapse': False,
    # If True, show hidden TOC entries
    'globaltoc_includehidden': False,

    "google_analytics_account": "UA-XXXXX",
    "html_minify": False,
    # "html_prettify": True,
    "css_minify": True,	
	'logo_icon': '&#xe41c',
}

html_sidebars = {
    "**": ["globaltoc.html"]
}
