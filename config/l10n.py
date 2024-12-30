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
