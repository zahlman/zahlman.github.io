# A list of redirection tuples, [("foo/from.html", "/bar/to")].
#
# A HTML file will be created in output/foo/from.html that redirects
# to the "/bar/to.html" URL. notice that the "from" side MUST be a
# relative URL.
#
# If you don't need any of these, just set to []
REDIRECTIONS = [
    # Nikola doesn't include categories in page URLs, or at least there
    # doesn't seem to be an obvious way to do that. (In the long run I
    # really want tags instead anyway). Also, we switched to pretty URLs.
    # Redirect old URLs to the current scheme.
    ("meta/2022/03/02/welcome.html", "/posts/2022/03/02/welcome"),
    ("python-standard-library/2023/04/06/timing.html", "/posts/2023/04/06/timing"),
    ("meta/2023/04/09/ah-yes-im-back-by-the-way.html", "/posts/2023/04/09/ah-yes-im-back-by-the-way"),
    ("misc/2024/05/09/where-ive-been.html", "/posts/2024/05/09/where-ive-been"),
    ("politics/the-psf/2024/07/31/an-open-letter-to-the-psf-coc-wg.html", "/posts/2024/07/31/an-open-letter-to-the-psf-coc-wg"),
    ("politics/the-psf/2024/08/10/open-letter-psf-coc-wg-addendum-1-tim-peters.html", "/posts/2024/08/10/open-letter-psf-coc-wg-addendum-1-tim-peters"),
    ("meta/2024/12/20/todo-finish-todo-list.html", "/posts/2024/12/20/todo-finish-todo-list"),
    ("python-packaging/2024/12/24/python-packaging-1.html", "/posts/2024/12/24/python-packaging-1"),
    ("meta/2024/12/31/todo-list-2.html", "/posts/2024/12/31/todo-list-2"),
    ("posts/2025/01/07/stupid-pipx-tricks/index.html", "/posts/2025/01/07/python-packaging-2"),
]
