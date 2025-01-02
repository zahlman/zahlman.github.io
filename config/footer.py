import time
from .l10n import DEFAULT_LANG
from .bio import *

# A HTML fragment describing the license, for the sidebar.
# (translatable)
LICENSE = ""

# A small copyright notice for the page footer (in HTML).
# (translatable)
# Renaming the keys doesn't seem to be supported, even if the rest of the
# config is kept consistent.
CONTENT_FOOTER = 'Contents &copy; 2022-{date}         <a href="mailto:{email}">{author}</a> - Powered by         <a href="https://getnikola.com" rel="nofollow">Nikola</a>         {license}'

# Things that will be passed to CONTENT_FOOTER.format().  This is done
# for translatability, as dicts are not formattable.  Nikola will
# intelligently format the setting properly.
# The setting takes a dict. The keys are languages. The values are
# tuples of tuples of positional arguments and dicts of keyword arguments
# to format().  For example, {'en': (('Hello'), {'target': 'World'})}
# results in CONTENT_FOOTER['en'].format('Hello', target='World').
# If you need to use the literal braces '{' and '}' in your footer text, use
# '{{' and '}}' to escape them (str.format is used)
# WARNING: If you do not use multiple languages with CONTENT_FOOTER, this
#          still needs to be a dict of this format.  (it can be empty if you
#          do not need formatting)
# (translatable)
CONTENT_FOOTER_FORMATS = {
    DEFAULT_LANG: (
        (),
        {
            "email": BLOG_EMAIL,
            "author": BLOG_AUTHOR,
            "date": time.gmtime().tm_year,
            "license": LICENSE
        }
    )
}
