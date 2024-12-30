from .l10n import DEFAULT_LANG

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
# (translatable; organized by language first then by category)
CATEGORY_DESCRIPTIONS = { DEFAULT_LANG: {} }
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
