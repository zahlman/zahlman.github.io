from .l10n import DEFAULT_LANG

# https://getnikola.com/handbook.html#configuring-tags-and-categories
# TAG_PATH = "categories" # (translatable)
# Use a custom path for the list of tags instead of TAG_PATH/index.html.
# TAGS_INDEX_PATH = "tags.html" # (translatable)

# If TAG_PAGES_ARE_INDEXES is set to True, each tag's page will contain
# the posts themselves. If set to False, it will be just a list of links.
TAG_PAGES_ARE_INDEXES = True 

# (translatable; organized by language first then by category)
TAG_TITLES = { DEFAULT_LANG: {
    'meta': 'Meta posts (about the blog)',
    'personal': 'Personal thoughts and reflections',
    'psf-coc-wg': 'Posts about the PSF Code of Conduct Work Group',
    'psf-code-of-conduct': 'Posts about the PSF Code of Conduct',
    'python-standard-library': "Posts about Python's standard library",
    'python-steering-council': 'Posts about the Python Steering Council',
    'the-psf': 'Posts about the Python Software Foundation',
    'virtual-environments': 'Posts about virtual environments',
} }
TAG_DESCRIPTIONS = { DEFAULT_LANG: {
    'jekyll': 'The default Static Site Generator (SSG) software for GitHub blogs. <a href="https://jekyllrb.com/">Homepage</a>',
    'nikola': 'A Static Site Generator (SSG) written in Python, which I currently use. <a href="https://getnikola.com">Homepage</a>',
    'pip': 'The default package installer for Python. <a href="https://pip.pypa.io">Homepage</a>',
    'pipx': 'An application installer for Python, built on Pip. <a href="https://pipx.pypa.io">Homepage</a>',
    'psf-coc-wg': 'An unelected group responsible for Code of Conduct enforcement. <a href="https://www.python.org/psf/workgroups/#code-of-conduct-work-group">Info</a> | <a href="https://wiki.python.org/psf/ConductWG/Charter">Charter</a>',
    'python-standard-library': '<a href="https://docs.python.org/3/library/index.html">Documentation</a>',
    'python': '<a href="https://python.org">Main Website</a>',
    'python-steering-council': 'Governing body for core Python developers. <a href=https://peps.python.org/pep-0013/>Info</a>',
    'setuptools': 'The default build backend for Python projects; originally designed with much broader scope. <a href="https://setuptools.pypa.io/">Homepage</a>',
    'the-psf': 'In their own words, "an organization devoted to advancing open source technology related to the Python programming language". <a href="https://www.python.org/psf-landing/">Landing page on python.org</a>',
    'virtual-environments': 'Isolated environments used for Python development, generally created by the <tt>venv</tt> standard library module.',
}}

# Hidden tags will not be displayed on the tag list page and posts.
# Tag pages will still be generated.
HIDDEN_TAGS = ['mathjax']

# Tags with fewer posts will be excluded from tag list/overview page.
# (Tag pages are still generated and used for navigation.)
# TAGLIST_MINIMUM_POSTS = 1

# Slug the Tag URL. Easier for users to type, special characters are
# often removed or replaced as well.
# SLUG_TAG_PATH = True
