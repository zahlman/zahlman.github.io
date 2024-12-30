from .l10n import DEFAULT_LANG

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
