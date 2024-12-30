from .l10n import DEFAULT_LANG

# https://getnikola.com/handbook.html#configuring-tags-and-categories
# TAG_PATH = "categories" # (translatable)
# Use a custom path for the list of tags instead of TAG_PATH/index.html.
# TAGS_INDEX_PATH = "tags.html" # (translatable)

# If TAG_PAGES_ARE_INDEXES is set to True, each tag's page will contain
# the posts themselves. If set to False, it will be just a list of links.
TAG_PAGES_ARE_INDEXES = True 

# (translatable; organized by language first then by category)
TAG_DESCRIPTIONS = { DEFAULT_LANG: {} }
TAG_TITLES = TAG_DESCRIPTIONS

# Hidden tags will not be displayed on the tag list page and posts.
# Tag pages will still be generated.
HIDDEN_TAGS = ['mathjax']

# Tags with fewer posts will be excluded from tag list/overview page.
# (Tag pages are still generated and used for navigation.)
# TAGLIST_MINIMUM_POSTS = 1

# Slug the Tag URL. Easier for users to type, special characters are
# often removed or replaced as well.
# SLUG_TAG_PATH = True
