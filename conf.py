import time

# Data about this site
BLOG_AUTHOR = "Karl Knechtel"  # (translatable)
BLOG_TITLE = "Zahlblog"  # (translatable)
# This is the main URL for your site. It will be used
# in a prominent link. Don't forget the protocol (http/https)!
SITE_URL = "https://zahlman.github.io/"
# This is the URL where Nikola's output will be deployed.
# If not set, defaults to SITE_URL
# BASE_URL = "https://example.com/"
BLOG_EMAIL = "zahlman@proton.me"
BLOG_DESCRIPTION = "Ramblings of a veteran Pythonista with a passion for refactoring and education."  # (translatable)

# A list of redirection tuples, [("foo/from.html", "/bar/to.html")].
#
# A HTML file will be created in output/foo/from.html that redirects
# to the "/bar/to.html" URL. notice that the "from" side MUST be a
# relative URL.
#
# If you don't need any of these, just set to []
REDIRECTIONS = []

# Localization config (refer to initial config for details)
# This blog isn't likely to use any localization in the foreseeable future.
# Translatable strings (marked `(translatable)`) can be localized
# by using a mapping of {language: text} instead of a simple string.
# e.g. BLOG_TITLE = {"en": "My Blog", "es": "Mi Blog"}
# Where a string is provided, it will be the same regardless of language.
DEFAULT_LANG = "en"
TRANSLATIONS = { DEFAULT_LANG: "" }
TRANSLATIONS_PATTERN = '{path}.{lang}.{ext}'
# Customize the locale/region used for a language.
# For example, to use British instead of US English: LOCALES = {'en': 'en_GB'}
# LOCALES = {}
# Allow posts to be shown in the DEFAULT_LANG when no translations exist.
# SHOW_UNTRANSLATED_POSTS = True
# List of translatable strings for tags names
# TAG_TRANSLATIONS = []
# If set to True, a tag in a language will be treated as a translation
# of the literally same tag in all other languages. Enable this if you
# do not translate tags, for example.
# TAG_TRANSLATIONS_ADD_DEFAULTS = True
# Similarly for categories
# CATEGORY_TRANSLATIONS = []
# CATEGORY_TRANSLATIONS_ADD_DEFAULTS = True


# Links for the sidebar / navigation bar.  (translatable)
# Detailed structure described at:
# https://getnikola.com/handbook.html#customizing-your-site
NAVIGATION_LINKS = {
    DEFAULT_LANG: (
        ("/archive.html", "Archives"),
        ("/categories/index.html", "Tags"),
        ("/rss.xml", "RSS feed"),
        ("/pages/about/", "About Me"),
        ("/pages/codidact/", "Codidact"),
        ("/pages/dpo/", "My archived posts from discuss.python.org"),
    ),
}

# Alternative navigation links. Works the same way NAVIGATION_LINKS does,
# although themes may not always support them. (translatable)
# (Bootstrap 4: right-side of navbar, Bootblog 4: right side of title)
NAVIGATION_ALT_LINKS = {
    DEFAULT_LANG: ()
}

# Name of the theme to use.
THEME = "bootblog4"

# A theme color. In default themes, it might be displayed by some browsers as
# the browser UI color (eg. Chrome on Android). Other themes might also use it
# as an accent color (the default ones don’t). Must be a HEX value.
THEME_COLOR = '#5670d4'

# Theme configuration. Fully theme-dependent. (translatable)
# Samples for bootblog4 (enabled) and bootstrap4 (commented) follow.
# bootblog4 supports: featured_large featured_small featured_on_mobile
#                     featured_large_image_on_mobile featured_strip_html sidebar
# bootstrap4 supports: navbar_light (defaults to False)
#                      navbar_custom_bg (defaults to '')

# Config for bootblog4:
THEME_CONFIG = {
    DEFAULT_LANG: {
        # Show the latest featured post in a large box, with the previewimage as its background.
        'featured_large': False,
        # Show the first (remaining) two featured posts in small boxes.
        'featured_small': False,
        # Show featured posts on mobile.
        'featured_on_mobile': True,
        # Show image in `featured_large` on mobile.
        # `featured_small` displays them only on desktop.
        'featured_large_image_on_mobile': True,
        # Strip HTML from featured post text.
        'featured_strip_html': False,
        # Contents of the sidebar, If empty, the sidebar is not displayed.
        'sidebar': ''
    }
}

# POSTS and PAGES contains (wildcard, destination, template) tuples.
# (translatable)
# Detailed description:
# https://getnikola.com/handbook.html#how-does-nikola-decide-where-posts-should-go
POSTS = (
    ("posts/*.rst", "posts", "post.tmpl"),
    ("posts/*.md", "posts", "post.tmpl"),
    ("posts/*.txt", "posts", "post.tmpl"),
    ("posts/*.html", "posts", "post.tmpl"),
)
PAGES = (
    ("pages/*.rst", "pages", "page.tmpl"),
    ("pages/*.md", "pages", "page.tmpl"),
    ("pages/*.txt", "pages", "page.tmpl"),
    ("pages/*.html", "pages", "page.tmpl"),
)
# One or more folders containing files to be copied as-is into the output.
# The format is a dictionary of {source: relative destination}.
# Default is:
# FILES_FOLDERS = {'files': ''}
# Which means copy 'files' into 'output'
# One or more folders containing code listings to be processed and published on
# the site. The format is a dictionary of {source: relative destination}.
# Default is:
# LISTINGS_FOLDERS = {'listings': 'listings'}
# Which means process listings from 'listings' into 'output/listings'

# Default timezone and date formatting
# Also, if you want to use a different time zone in some of your posts,
# you can use the ISO 8601/RFC 3339 format (ex. 2012-03-30T23:00:00+02:00)
TIMEZONE = "America/Toronto"
# FORCE_ISO8601 = False # does not affect DATE_FORMAT even if True
# Date format used to display post dates. (translatable)
# Used by babel.dates, CLDR style: 
# http://cldr.unicode.org/translation/date-time-1/date-time
# You can also use 'full', 'long', 'medium', or 'short'
# DATE_FORMAT = 'yyyy-MM-dd HH:mm'
# LUXON_DATE_FORMAT = {
#     DEFAULT_LANG: {'preset': False, 'format': 'yyyy-MM-dd HH:mm'},
# }
# 0 = using DATE_FORMAT and TIMEZONE (without JS)
# 1 = using LUXON_DATE_FORMAT and local user time (JS, using Luxon)
# 2 = using a string like “2 days ago” (JS, using Luxon)
# Your theme must support it, Bootstrap already does.
# DATE_FANCINESS = 0

# A mapping of languages to file-extensions that represent that language.
# See original config for full options, but this blog uses only Markdown.
COMPILERS = {
    "markdown": ['.md', '.mdown', '.markdown'],
    "html": ['.html', '.htm'], # just in case
}
# What Markdown extensions to enable?
# `gist`, `nikola` and `podcast` are hard-coded.
# Note: most Nikola-specific extensions are done via the Nikola plugin system,
#       with the MarkdownExtension class and should not be added here.
# markdown.extensions.meta is required for Markdown metadata.
MARKDOWN_EXTENSIONS = [
    'markdown.extensions.fenced_code',
    'markdown.extensions.codehilite',
    'markdown.extensions.extra'
]
# Options to be passed to markdown extensions (translatable)
# (See https://python-markdown.github.io/reference/)
# MARKDOWN_EXTENSION_CONFIGS = {DEFAULT_LANG: {}}
# There are also possible extra options for pandoc if that compiler is added.

# Preferred metadata format for new posts
# "Nikola": reST comments, wrapped in a HTML comment if needed (default)
# "YAML": YAML wrapped in "---"
# "TOML": TOML wrapped in "+++"
# "Pelican": Native markdown metadata or reST docinfo fields. Nikola style for other formats.
# METADATA_FORMAT = "Nikola"

# Use date-based path when creating posts?
# Can be enabled on a per-post basis with `nikola new_post -d`.
# The setting is ignored when creating pages.
NEW_POST_DATE_PATH = True 
NEW_POST_DATE_PATH_FORMAT = '%Y/%m/%d'

# Nikola supports logo display.  If you have one, you can put the URL here.
# Final output is <img src="LOGO_URL" id="logo" alt="BLOG_TITLE">.
# The URL may be relative to the site root.
# LOGO_URL = ''

# When linking posts to social media, Nikola provides Open Graph metadata
# which is used to show a nice preview. This includes an image preview
# taken from the post's previewimage metadata field.
# This option lets you use an image to be used if the post doesn't have it.
# The default is None, valid values are URLs or output paths like
# "/images/foo.jpg"
# DEFAULT_PREVIEW_IMAGE = None

# If you want to hide the title of your website (for example, if your logo
# already contains the text), set this to False.
# Note: if your logo is a SVG image, and you set SHOW_BLOG_TITLE = False,
# you should explicitly set a height for #logo in CSS.
# SHOW_BLOG_TITLE = True

# Paths for different autogenerated bits. These are combined with the
# translation paths.

# Final locations are:
# output / TRANSLATION[lang] / TAG_PATH / index.html (list of tags)
# output / TRANSLATION[lang] / TAG_PATH / tag.html (list of posts for a tag)
# output / TRANSLATION[lang] / TAG_PATH / tag RSS_EXTENSION (RSS feed for a tag)
# (translatable)
# TAG_PATH = "categories"

# By default, the list of tags is stored in
#     output / TRANSLATION[lang] / TAG_PATH / index.html
# (see explanation for TAG_PATH). This location can be changed to
#     output / TRANSLATION[lang] / TAGS_INDEX_PATH
# with an arbitrary relative path TAGS_INDEX_PATH.
# (translatable)
# TAGS_INDEX_PATH = "tags.html"

# If TAG_PAGES_ARE_INDEXES is set to True, each tag's page will contain
# the posts themselves. If set to False, it will be just a list of links.
TAG_PAGES_ARE_INDEXES = True 

# (translatable)
TAG_DESCRIPTIONS = {
    DEFAULT_LANG: {
    },
}
TAG_TITLES = TAG_DESCRIPTIONS

# Hidden tags will not be displayed on the tag list page and posts.
# Tag pages will still be generated.
HIDDEN_TAGS = ['mathjax']

# Tags with fewer posts will be excluded from tag list/overview page.
# (Tag pages are still generated and used for navigation.)
# TAGLIST_MINIMUM_POSTS = 1

# https://getnikola.com/handbook.html#configuring-tags-and-categories
# CATEGORY_PATH = "categories" # (translatable)
# CATEGORY_PREFIX = "cat_"
# CATEGORIES_INDEX_PATH = "categories.html" # (translatable)

# Enable hierarchical categories.
# replace old `categories: [foo, bar]` with `category: foo/bar`.
# Forward and backward slashes need to be backslash-escaped.
CATEGORY_ALLOW_HIERARCHIES = True
# If True, the output written to output contains only the name of the leaf
# category rather than the whole path.
CATEGORY_OUTPUT_FLAT_HIERARCHY = False
# Include post teasers in category pages.
CATEGORY_PAGES_ARE_INDEXES = True

# As with tag descriptions and titles.
# (translatable)
CATEGORY_DESCRIPTIONS = {
    DEFAULT_LANG: {
    },
}
CATEGORY_TITLES = CATEGORY_DESCRIPTIONS

# As with hidden tags.
HIDDEN_CATEGORIES = []

# Additional options, unlikely to be useful
# CATEGORY_DESTPATH_AS_DEFAULT = False
# CATEGORY_DESTPATH_TRIM_PREFIX = False
# CATEGORY_DESTPATH_FIRST_DIRECTORY_ONLY = True
# CATEGORY_DESTPATH_NAMES = {
#    DEFAULT_LANG: {
#    },
# }

# By default, category indexes will appear in CATEGORY_PATH and use
# CATEGORY_PREFIX. If this is enabled, those settings will be ignored (except
# for the index) and instead, they will follow destination paths (eg. category
# 'foo' might appear in 'posts/foo'). If the category does not come from a
# destpath, first entry in POSTS followed by the category name will be used.
# For this setting, category hierarchies are required and cannot be flattened.
# CATEGORY_PAGES_FOLLOW_DESTPATH = False

# AUTHORS
# If another author is somehow ever added, check the original config comments.

# Final location for the main blog page and sibling paginated pages is
# output / TRANSLATION[lang] / INDEX_PATH / index-*.html
# (translatable)
# INDEX_PATH = ""

# Optional HTML that displayed on “main” blog index.html files.
# May be used for a greeting. (translatable)
FRONT_INDEX_HEADER = {
    DEFAULT_LANG: ''
}

# Archive frequency options
# CREATE_SINGLE_ARCHIVE = False
# CREATE_MONTHLY_ARCHIVE = False
# Create year, month, and day archives each with a (long) list of posts
# (overrides both CREATE_MONTHLY_ARCHIVE and CREATE_SINGLE_ARCHIVE)
# CREATE_FULL_ARCHIVES = False
# If monthly or full archives are created, adds also one archive per day
# CREATE_DAILY_ARCHIVE = False
# Create previous, up, next navigation links for archives
# CREATE_ARCHIVE_NAVIGATION = False
# ARCHIVE_PATH = "" # (translatable)
# ARCHIVE_FILENAME = "archive.html"

# Show post teasers in archive pages instead of just links
ARCHIVES_ARE_INDEXES = True 

# URLs to other posts/pages can take 3 forms:
# rel_path: a relative URL to the current page/post (default)
# full_path: a URL with the full path from the root
# absolute: a complete URL (that includes the SITE_URL)
# URL_TYPE = 'rel_path'

# Extension for RSS feed files
# RSS_EXTENSION = ".xml"

# RSS filename base (without extension); used for indexes and galleries.
# (translatable)
# RSS_FILENAME_BASE = "rss"

# Final location for the blog main RSS feed is:
# output / TRANSLATION[lang] / RSS_PATH / RSS_FILENAME_BASE RSS_EXTENSION
# (translatable)
# RSS_PATH = ""

# Final location for the blog main Atom feed is:
# output / TRANSLATION[lang] / ATOM_PATH / ATOM_FILENAME_BASE ATOM_EXTENSION
# (translatable)
# ATOM_PATH = ""

# Atom filename base (without extension); used for indexes.
# (translatable)
ATOM_FILENAME_BASE = "feed"

# Extension for Atom feed files
# ATOM_EXTENSION = ".atom"

# Slug the Tag URL. Easier for users to type, special characters are
# often removed or replaced as well.
# SLUG_TAG_PATH = True

# Github deployment config
# There are other deploy options described in the original conf.py.
# https://getnikola.com/handbook.html#deploying-to-github
# You will need to configure the deployment branch on GitHub.
GITHUB_SOURCE_BRANCH = 'nikola'
GITHUB_DEPLOY_BRANCH = 'master'
GITHUB_REMOTE_NAME = 'origin'
# Commit to the source branch automatically before deploying?
GITHUB_COMMIT_SOURCE = True
# Override default output and cache folders
# OUTPUT_FOLDER = 'output'
# CACHE_FOLDER = 'cache'

# Expert postprocessing stuff

# Filters to apply to the output (to transform files in-place).
# dict of (file extension or tuple of file extensions) to commands.
# Each command must be either:
# * a Python callable, called with the filename as argument
# * a shell command string, with a single %s placeholder for the filename
# By default, only .php files uses filters to inject PHP into
# Nikola’s templates. All other filters must be enabled through FILTERS.
# Many filters are shipped with Nikola. A list is available in the manual:
# <https://getnikola.com/handbook.html#post-processing-filters>
# from nikola import filters
# FILTERS = {
#    ".html": [filters.typogrify],
#    ".js": [filters.closure_compiler],
#    ".jpg": ["jpegoptim --strip-all -m75 -v %s"],
# }
# Executable for the "yui_compressor" filter (defaults to 'yui-compressor').
# YUI_COMPRESSOR_EXECUTABLE = 'yui-compressor'
# Executable for the "closure_compiler" filter (defaults to 'closure-compiler').
# CLOSURE_COMPILER_EXECUTABLE = 'closure-compiler'
# Executable for the "optipng" filter (defaults to 'optipng').
# OPTIPNG_EXECUTABLE = 'optipng'
# Executable for the "jpegoptim" filter (defaults to 'jpegoptim').
# JPEGOPTIM_EXECUTABLE = 'jpegoptim'
# Executable for the "html_tidy_withconfig", "html_tidy_nowrap",
# "html_tidy_wrap", "html_tidy_wrap_attr" and "html_tidy_mini" filters
# (defaults to 'tidy5').
# HTML_TIDY_EXECUTABLE = 'tidy5'

# List of XPath expressions which should be used for finding headers
# ({hx} is replaced by headers h1 through h6).
# You must change this if you use a custom theme that does not use
# "e-content entry-content" as a class for post and page contents.
# HEADER_PERMALINKS_XPATH_LIST = ['*//div[@class="e-content entry-content"]//{hx}']
# Include *every* header (not recommended):
# HEADER_PERMALINKS_XPATH_LIST = ['*//{hx}']
# File blacklist for header permalinks. Contains output path
# (eg. 'output/index.html')
# HEADER_PERMALINKS_FILE_BLACKLIST = []

# Set up gzip compression. Requires that the server uses appropriate headers:
# it must not return "Accept-Ranges: bytes" for compressed files, and
# range requests must not return partial content of another representation.
# TODO investigate whether GitHub supports this. Probably not.
# GZIP_FILES = False
# File extensions that will be compressed
# GZIP_EXTENSIONS = ('.txt', '.htm', '.html', '.css', '.js', '.json', '.atom', '.xml')
# Use an external gzip command? None means no.
# Example: GZIP_COMMAND = "pigz -k {filename}"
# GZIP_COMMAND = None

# #############################################################################
# Image Gallery Options
# #############################################################################

# One or more folders containing galleries. The format is a dictionary of
# {"source": "relative_destination"}, where galleries are looked for in
# "source/" and the results will be located in
# "OUTPUT_PATH/relative_destination/gallery_name"
# Default is:
# GALLERY_FOLDERS = {"galleries": "galleries"}
# More gallery options:
# THUMBNAIL_SIZE = 180
# MAX_IMAGE_SIZE = 1280
# USE_FILENAME_AS_TITLE = True
# EXTRA_IMAGE_EXTENSIONS = []

# Use a thumbnail (defined by ".. previewimage:" in the gallery's index) in
# list of galleries for each gallery
GALLERIES_USE_THUMBNAIL = False

# Image to use as thumbnail for those galleries that don't have one
# None: show a grey square
# '/url/to/file': show the image in that url
GALLERIES_DEFAULT_THUMBNAIL = None

# If set to False, it will sort by filename instead. Defaults to True
# GALLERY_SORT_BY_DATE = True

# If set to True, EXIF data will be copied when an image is thumbnailed or
# resized. (See also EXIF_WHITELIST)
# PRESERVE_EXIF_DATA = False

# If you have enabled PRESERVE_EXIF_DATA, this option lets you choose EXIF
# fields you want to keep in images. (See also PRESERVE_EXIF_DATA)
#
# For a full list of field names, please see here:
# http://www.cipa.jp/std/documents/e/DC-008-2012_E.pdf
#
# This is a dictionary of lists. Each key in the dictionary is the
# name of a IDF, and each list item is a field you want to preserve.
# If you have a IDF with only a '*' item, *EVERY* item in it will be
# preserved. If you don't want to preserve anything in a IDF, remove it
# from the setting. By default, no EXIF information is kept.
# Setting the whitelist to anything other than {} implies
# PRESERVE_EXIF_DATA is set to True
# To preserve ALL EXIF data, set EXIF_WHITELIST to {"*": "*"}

# EXIF_WHITELIST = {}

# Some examples of EXIF_WHITELIST settings:

# Basic image information:
# EXIF_WHITELIST['0th'] = [
#    "Orientation",
#    "XResolution",
#    "YResolution",
# ]

# If you want to keep GPS data in the images:
# EXIF_WHITELIST['GPS'] = ["*"]

# Embedded thumbnail information:
# EXIF_WHITELIST['1st'] = ["*"]

# If set to True, any ICC profile will be copied when an image is thumbnailed or
# resized.
# PRESERVE_ICC_PROFILES = False

# Folders containing images to be used in normal posts or pages.
# IMAGE_FOLDERS is a dictionary of the form {"source": "destination"},
# where "source" is the folder containing the images to be published, and
# "destination" is the folder under OUTPUT_PATH containing the images copied
# to the site. Thumbnail images will be created there as well.

# To reference the images in your posts, include a leading slash in the path.
# For example, if IMAGE_FOLDERS = {'images': 'images'}, write
#
#   .. image:: /images/tesla.jpg
#
# See the Nikola Handbook for details (in the “Embedding Images” and
# “Thumbnails” sections)

# Images will be scaled down according to IMAGE_THUMBNAIL_SIZE and MAX_IMAGE_SIZE
# options, but will have to be referenced manually to be visible on the site
# (the thumbnail has ``.thumbnail`` added before the file extension by default,
# but a different naming template can be configured with IMAGE_THUMBNAIL_FORMAT).
# Panoramas (aspect ratio over 3:1) get 4x larger thumbnails due to scaling issues.

IMAGE_FOLDERS = {'images': 'images'}
# IMAGE_THUMBNAIL_SIZE = 400
# IMAGE_THUMBNAIL_FORMAT = '{name}.thumbnail{ext}'

# #############################################################################
# HTML fragments and diverse things that are used by the templates
# #############################################################################

# Data about post-per-page indexes.
# INDEXES_PAGES defaults to ' old posts, page %d' or ' page %d' (translated),
# depending on the value of INDEXES_PAGES_MAIN.
#
# (translatable) If the following is empty, defaults to BLOG_TITLE:
# INDEXES_TITLE = ""
#
# (translatable) If the following is empty, defaults to ' [old posts,] page %d' (see above):
# INDEXES_PAGES = ""
#
# If the following is True, INDEXES_PAGES is also displayed on the main (the
# newest) index page (index.html):
# INDEXES_PAGES_MAIN = False
#
# If the following is True, index-1.html has the oldest posts, index-2.html the
# second-oldest posts, etc., and index.html has the newest posts. This ensures
# that all posts on index-x.html will forever stay on that page, now matter how
# many new posts are added.
# If False, index-1.html has the second-newest posts, index-2.html the third-newest,
# and index-n.html the oldest posts. When this is active, old posts can be moved
# to other index pages when new posts are added.
# INDEXES_STATIC = True
#
# (translatable) If PRETTY_URLS is set to True, this setting will be used to create
# prettier URLs for index pages, such as page/2/index.html instead of index-2.html.
# Valid values for this settings are:
#   * False,
#   * a list or tuple, specifying the path to be generated,
#   * a dictionary mapping languages to lists or tuples.
# Every list or tuple must consist of strings which are used to combine the path;
# for example:
#     ['page', '{number}', '{index_file}']
# The replacements
#     {number}     --> (logical) page number;
#     {old_number} --> the page number inserted into index-n.html before (zero for
#                      the main page);
#     {index_file} --> value of option INDEX_FILE
# are made.
# Note that in case INDEXES_PAGES_MAIN is set to True, a redirection will be created
# for the full URL with the page number of the main page to the normal (shorter) main
# page URL.
# INDEXES_PRETTY_PAGE_URL = False
#
# If the following is true, a page range navigation will be inserted to indices.
# Please note that this will undo the effect of INDEXES_STATIC, as all index pages
# must be recreated whenever the number of pages changes.
# SHOW_INDEX_PAGE_NAVIGATION = False

# If the following is True, a meta name="generator" tag is added to pages. The
# generator tag is used to specify the software used to generate the page
# (it promotes Nikola).
# META_GENERATOR_TAG = True

# Color scheme to be used for code blocks. If your theme provides
# "assets/css/code.css" this is ignored. Set to None to disable.
# Can be any of:
# algol, algol_nu, autumn, borland, bw, colorful, default, emacs, friendly,
# fruity, igor, lovelace, manni, monokai, murphy, native, paraiso-dark,
# paraiso-light, pastie, perldoc, rrt, tango, trac, vim, vs, xcode
# This list MAY be incomplete since pygments adds styles every now and then.
# Check with list(pygments.styles.get_all_styles()) in an interpreter.
#
# CODE_COLOR_SCHEME = 'default'

# FAVICONS contains (name, file, size) tuples.
# Used to create favicon link like this:
# <link rel="name" href="file" sizes="size"/>
# FAVICONS = (
#     ("icon", "/favicon.ico", "16x16"),
#     ("icon", "/icon_128x128.png", "128x128"),
# )

# Show teasers (instead of full posts) in indexes? Defaults to False.
INDEX_TEASERS = True

# HTML fragments with the Read more... links.
# The following tags exist and are replaced for you:
# {link}                        A link to the full post page.
# {read_more}                   The string “Read more” in the current language.
# {reading_time}                An estimate of how long it will take to read the post.
# {remaining_reading_time}      An estimate of how long it will take to read the post, sans the teaser.
# {min_remaining_read}          The string “{remaining_reading_time} min remaining to read” in the current language.
# {paragraph_count}             The amount of paragraphs in the post.
# {remaining_paragraph_count}   The amount of paragraphs in the post, sans the teaser.
# {post_title}                  The title of the post.
# {{                            A literal { (U+007B LEFT CURLY BRACKET)
# }}                            A literal } (U+007D RIGHT CURLY BRACKET)

# 'Read more...' for the index page, if INDEX_TEASERS is True (translatable)
INDEX_READ_MORE_LINK = '<p class="more"><a href="{link}">{read_more}…</a></p>'
# 'Read more...' for the feeds, if FEED_TEASERS is True (translatable)
FEED_READ_MORE_LINK = '<p><a href="{link}">{read_more}…</a> ({min_remaining_read})</p>'

# Append a URL query to the FEED_READ_MORE_LINK in Atom and RSS feeds. Advanced
# option used for traffic source tracking.
# Minimum example for use with Piwik: "pk_campaign=feed"
# The following tags exist and are replaced for you:
# {feedRelUri}                  A relative link to the feed.
# {feedFormat}                  The name of the syndication format.
# Example using replacement for use with Google Analytics:
# "utm_source={feedRelUri}&utm_medium=nikola_feed&utm_campaign={feedFormat}_feed"
FEED_LINKS_APPEND_QUERY = False

# A HTML fragment describing the license, for the sidebar.
# (translatable)
LICENSE = ""
# I recommend using the Creative Commons' wizard:
# https://creativecommons.org/choose/
# LICENSE = """
# <a rel="license" href="https://creativecommons.org/licenses/by-nc-sa/4.0/">
# <img alt="Creative Commons License BY-NC-SA"
# style="border-width:0; margin-bottom:12px;"
# src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png"></a>"""

# A small copyright notice for the page footer (in HTML).
# (translatable)
CONTENT_FOOTER = 'Contents &copy; {date}         <a href="mailto:{email}">{author}</a> - Powered by         <a href="https://getnikola.com" rel="nofollow">Nikola</a>         {license}'

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

# A simple copyright tag for inclusion in RSS feeds that works just
# like CONTENT_FOOTER and CONTENT_FOOTER_FORMATS
RSS_COPYRIGHT = 'Contents © {date} <a href="mailto:{email}">{author}</a> {license}'
RSS_COPYRIGHT_PLAIN = 'Contents © {date} {author} {license}'
RSS_COPYRIGHT_FORMATS = CONTENT_FOOTER_FORMATS

# Third-party comment systems
# Supported:
# disqus, discourse, facebook, intensedebate, isso, muut, commento, utterances
COMMENT_SYSTEM = ''
COMMENT_SYSTEM_ID = '' # need to obtain an ID to use these

# Create index.html for page folders?
# WARNING: if a page would conflict with the index file (usually
#          caused by setting slug to `index`), the PAGE_INDEX
#          will not be generated for that directory.
# PAGE_INDEX = False
# Enable comments on pages (i.e. not posts)?
# COMMENTS_IN_PAGES = False
# Enable comments on picture gallery pages?
# COMMENTS_IN_GALLERIES = False

# What file should be used for directory indexes?
# Defaults to index.html
# Common other alternatives: default.html for IIS, index.php
# INDEX_FILE = "index.html"

# If a link ends in /index.html,  drop the index.html part.
# http://mysite/foo/bar/index.html => http://mysite/foo/bar/
# (Uses the INDEX_FILE setting, so if that is, say, default.html,
# it will instead /foo/default.html => /foo)
STRIP_INDEXES = True

# List of files relative to the server root (!) that will be asked to be excluded
# from indexing and other robotic spidering. * is supported. Will only be effective
# if SITE_URL points to server root. The list is used to exclude resources from
# /robots.txt and /sitemap.xml, and to inform search engines about /sitemapindex.xml.
# ROBOTS_EXCLUSIONS = ["/archive.html", "/category/*.html"]

# Instead of putting files in <slug>.html, put them in <slug>/index.html.
# No web server configuration is required. Also enables STRIP_INDEXES.
# This can be disabled on a per-page/post basis by adding
#    .. pretty_url: False
# to the metadata.
PRETTY_URLS = True

# Draft scheduling

# If True, publish future dated posts right away instead of scheduling them.
# Defaults to False.
# FUTURE_IS_NOW = False

# If True, future dated posts are allowed in deployed output
# Only the individual posts are published/deployed; not in indexes/sitemap
# Generally, you want FUTURE_IS_NOW and DEPLOY_FUTURE to be the same value.
# DEPLOY_FUTURE = False
# If False, draft posts will not be deployed
# DEPLOY_DRAFTS = True

# Allows scheduling of posts using the rule specified here (new_post -s)
# Specify an iCal Recurrence Rule: https://www.kanzaki.com/docs/ical/rrule.html
# SCHEDULE_RULE = ''
# If True, use the scheduling rule to all posts (not pages!) by default
# SCHEDULE_ALL = False

# Mathjax/Katex/ipynb stuff

# Do you want to add a Mathjax config file?
# MATHJAX_CONFIG = ""

# If you want support for the $.$ syntax (which may conflict with running
# text!), just use this config:
# MATHJAX_CONFIG = """
# <script type="text/x-mathjax-config">
# MathJax.Hub.Config({
#     tex2jax: {
#         inlineMath: [ ['$','$'], ["\\\(","\\\)"] ],
#         displayMath: [ ['$$','$$'], ["\\\[","\\\]"] ],
#         processEscapes: true
#     },
#     displayAlign: 'center', // Change this to 'left' if you want left-aligned equations.
#     "HTML-CSS": {
#         styles: {'.MathJax_Display': {"margin": 0}}
#     }
# });
# </script>
# """

# Want to use KaTeX instead of MathJax? While KaTeX may not support every
# feature yet, it's faster and the output looks better.
# USE_KATEX = False

# KaTeX auto-render settings. If you want support for the $.$ syntax (which may
# conflict with running text!), just use this config:
# KATEX_AUTO_RENDER = """
# delimiters: [
#     {left: "$$", right: "$$", display: true},
#     {left: "\\\\[", right: "\\\\]", display: true},
#     {left: "\\\\begin{equation*}", right: "\\\\end{equation*}", display: true},
#     {left: "$", right: "$", display: false},
#     {left: "\\\\(", right: "\\\\)", display: false}
# ]
# """

# Do you want to customize the nbconversion of your IPython notebook?
# IPYNB_CONFIG = {}
# With the following example configuration you can use a custom jinja template
# called `toggle.tpl` which has to be located in your site/blog main folder:
# IPYNB_CONFIG = {'Exporter': {'template_file': 'toggle'}}

# HTML for social buttons (translatable).
# Will probably want something eventually.
# Maybe hit counters can go here?
SOCIAL_BUTTONS_CODE = """
<!-- Social buttons -->
<!-- End of social buttons -->
"""

# Copy source files in the output
COPY_SOURCES = False
# If they're copied, the rendered HTML can include links to the source versions
# SHOW_SOURCELINK = True

# Number of posts per index page (default 10)
INDEX_DISPLAY_POST_COUNT = 5

# By default, Nikola generates RSS files for the website and for tags, and
# links to it.  Set this to False to disable everything RSS-related.
GENERATE_RSS = True

# By default, Nikola does not generates Atom files for indexes and links to
# them. Generate Atom for tags by setting TAG_PAGES_ARE_INDEXES to True.
# Atom feeds are built based on INDEX_DISPLAY_POST_COUNT and not FEED_LENGTH
# Switch between plain-text summaries and full HTML content using the
# FEED_TEASER option. FEED_LINKS_APPEND_QUERY is also respected. Atom feeds
# are generated even for old indexes and have pagination link relations
# between each other. Old Atom feeds with no changes are marked as archived.
# GENERATE_ATOM = False

# Only include teasers in Atom and RSS feeds. Disabling include the full
# content. Defaults to True.
# FEED_TEASERS = True

# Strip HTML from Atom and RSS feed summaries and content. Defaults to False.
# FEED_PLAIN = False

# Number of posts in Atom and RSS feeds.
# FEED_LENGTH = 10

# RSS_LINK is a HTML fragment to link the RSS or Atom feeds. If set to None,
# the base.tmpl will use the feed Nikola generates. However, you may want to
# change it for a FeedBurner feed or something else.
# RSS_LINK = None

# DDG search form from suggestions in the original config.
# (translatable)
SEARCH_FORM = f"""
<!-- DuckDuckGo custom search -->
<form method="get" id="search" action="https://duckduckgo.com/"
 class="navbar-form pull-left">
<input type="hidden" name="sites" value="{SITE_URL}">
<input type="hidden" name="k8" value="#444444">
<input type="hidden" name="k9" value="#D51920">
<input type="hidden" name="kt" value="h">
<input type="text" name="q" maxlength="255"
 placeholder="Search&hellip;" class="span2" style="margin-top: 4px;">
<input type="submit" value="DuckDuckGo Search" style="visibility: hidden;">
</form>
<!-- End of custom search -->
"""

# Use content distribution networks for jQuery, twitter-bootstrap css and js,
# and html5shiv (for older versions of Internet Explorer)
# If this is True, jQuery and html5shiv are served from the Google CDN and
# Bootstrap is served from BootstrapCDN (provided by MaxCDN)
# Set this to False if you want to host your site without requiring access to
# external resources.
# USE_CDN = False

# Check for USE_CDN compatibility.
# If you are using custom themes, have configured the CSS properly and are
# receiving warnings about incompatibility but believe they are incorrect, you
# can set this to False.
# USE_CDN_WARNING = True

# Extra things you want in the pages HEAD tag. This will be added right
# before </head>
# (translatable)
# EXTRA_HEAD_DATA = ""
# Google Analytics or whatever else you use. Added to the bottom of <body>
# in the default template (base.tmpl).
# (translatable)
# BODY_END = ""

# The possibility to extract metadata from the filename by using a
# regular expression.
# To make it work you need to name parts of your regular expression.
# The following names will be used to extract metadata:
# - title
# - slug
# - date
# - tags
# - link
# - description
#
# An example re is the following:
# '.*\/(?P<date>\d{4}-\d{2}-\d{2})-(?P<slug>.*)-(?P<title>.*)\.rst'
# (Note the '.*\/' in the beginning -- matches source paths relative to conf.py)
# FILE_METADATA_REGEXP = None

# Should titles fetched from file metadata be unslugified (made prettier?)
# FILE_METADATA_UNSLUGIFY_TITLES = True

# If enabled, extract metadata from docinfo fields in reST documents.
# If your text files start with a level 1 heading, it will be treated as the
# document title and will be removed from the text.
# USE_REST_DOCINFO_METADATA = False

# If enabled, hide docinfo fields in reST document output
# HIDE_REST_DOCINFO = False

# Map metadata from other formats to Nikola names.
# Supported formats: yaml, toml, rest_docinfo, markdown_metadata
# METADATA_MAPPING = {}
#
# Example for Pelican compatibility:
# METADATA_MAPPING = {
#     "rest_docinfo": {"summary": "description", "modified": "updated"},
#     "markdown_metadata": {"summary": "description", "modified": "updated"}
# }
# Other examples: https://getnikola.com/handbook.html#mapping-metadata-from-other-formats

# Map metadata between types/values. (Runs after METADATA_MAPPING.)
# Supported formats: nikola, yaml, toml, rest_docinfo, markdown_metadata
# The value on the right should be a dict of callables.
# METADATA_VALUE_MAPPING = {}
# Examples:
# METADATA_VALUE_MAPPING = {
#     "yaml": {"keywords": lambda value: ', '.join(value)},  # yaml: 'keywords' list -> str
#     "nikola": {
#         "widgets": lambda value: value.split(', '),  # nikola: 'widgets' comma-separated string -> list
#         "tags": str.lower  # nikola: force lowercase 'tags' (input would be string)
#      }
# }

# Add any post types here that you want to be displayed without a title.
# If your theme supports it, the titles will not be shown.
# TYPES_TO_HIDE_TITLE = []

# Additional metadata that is added to a post when creating a new_post
# ADDITIONAL_METADATA = {}

# Nikola supports Twitter Card summaries (disabled by default);
# see the original conf for details.

# Bundle JS and CSS into single files to make site loading faster in a HTTP/1.1
# environment but is not recommended for HTTP/2.0 when caching is used.
# Defaults to True.
# USE_BUNDLES = True

# Plugins you don't want to use. Be careful :-)
# DISABLED_PLUGINS = ["render_galleries"]

# Special settings to disable only parts of the indexes plugin.
# Use with care.
# DISABLE_INDEXES = False
# DISABLE_MAIN_ATOM_FEED = False
# DISABLE_MAIN_RSS_FEED = False

# Add the absolute paths to directories containing plugins to use them.
# For example, the `plugins` directory of your clone of the Nikola plugins
# repository.
# EXTRA_PLUGINS_DIRS = []

# Add the absolute paths to directories containing themes to use them.
# For example, the `v7` directory of your clone of the Nikola themes
# repository.
# EXTRA_THEMES_DIRS = []

# List of regular expressions, links matching them will always be considered
# valid by "nikola check -l"
# LINK_CHECK_WHITELIST = []

# If set to True, enable optional hyphenation in your posts (requires pyphen)
# Enabling hyphenation has been shown to break math support in some cases,
# use with caution.
# HYPHENATE = False

# The <hN> tags in HTML generated by certain compilers (reST/Markdown)
# will be demoted by that much (1 → h1 will become h2 and so on)
# This was a hidden feature of the Markdown and reST compilers in the
# past.  Useful especially if your post titles are in <h1> tags too, for
# example.
# (defaults to 1.)
DEMOTE_HEADERS = 0 

# If you don’t like slugified file names ([a-z0-9] and a literal dash),
# and would prefer to use all the characters your file system allows.
# USE WITH CARE!  This is also not guaranteed to be perfect, and may
# sometimes crash Nikola, your web server, or eat your cat.
# USE_SLUGIFY = True

# If set to True, the tags 'draft', 'mathjax' and 'private' have special
# meaning. If set to False, these tags are handled like regular tags.
USE_TAG_METADATA = False

# If set to True, a warning is issued if one of the 'draft', 'mathjax'
# and 'private' tags are found in a post. Useful for checking that
# migration was successful.
WARN_ABOUT_TAG_METADATA = False

# Templates will use those filters, along with the defaults.
# Consult your engine's documentation on filters if you need help defining
# those.
# TEMPLATE_FILTERS = {}

# Put in global_context things you want available on all your templates.
# It can be anything, data, functions, modules, etc.
GLOBAL_CONTEXT = {}

# Add functions here and they will be called with template
# GLOBAL_CONTEXT as parameter when the template is about to be
# rendered
GLOBAL_CONTEXT_FILLER = []
