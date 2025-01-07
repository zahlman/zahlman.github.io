from .l10n import DEFAULT_LANG
from .bio import BLOG_AUTHOR, BLOG_EMAIL
import time

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

# 'Read more...' for the feeds, if FEED_TEASERS is True (translatable)
# See teasers.py for the formatting options.
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

RSS_COPYRIGHT = 'Contents © 2022-{date} <a href="mailto:{email}">{author}</a> {license}'
RSS_COPYRIGHT_PLAIN = 'Contents © 2022-{date} {author} {license}'
RSS_COPYRIGHT_FORMATS = {
    DEFAULT_LANG: (
        (),
        {
            "email": BLOG_EMAIL,
            "author": BLOG_AUTHOR,
            "date": time.gmtime().tm_year,
            "license": ''
        }
    )
}
