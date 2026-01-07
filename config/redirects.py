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
    # Also, canonical URLs now don't have date components (the system
    # can still group posts by year, label the date in category posts etc.
    # using explicit in-document metadata).
    # Redirect old (and older) URLs to the current scheme.
    ("meta/2022/03/02/welcome.html", "/posts/welcome"),
    ("posts/2022/03/02/welcome/", "/posts/welcome"),
    ("python-standard-library/2023/04/06/timing.html", "/posts/timing"),
    ("posts/2023/04/06/timing/", "/posts/timing"),
    ("meta/2023/04/09/ah-yes-im-back-by-the-way.html", "/posts/ah-yes-im-back-by-the-way"),
    ("posts/2023/04/09/ah-yes-im-back-by-the-way/", "/posts/ah-yes-im-back-by-the-way"),
    ("misc/2024/05/09/where-ive-been.html", "/posts/where-ive-been"),
    ("posts/2024/05/09/where-ive-been/", "/posts/where-ive-been"),
    ("politics/the-psf/2024/07/31/an-open-letter-to-the-psf-coc-wg.html", "/posts/an-open-letter-to-the-psf-coc-wg"),
    ("posts/2024/07/31/an-open-letter-to-the-psf-coc-wg/", "/posts/an-open-letter-to-the-psf-coc-wg"),
    ("politics/the-psf/2024/08/10/open-letter-psf-coc-wg-addendum-1-tim-peters.html", "/posts/open-letter-psf-coc-wg-addendum-1-tim-peters"),
    ("posts/2024/08/10/open-letter-psf-coc-wg-addendum-1-tim-peters/", "/posts/open-letter-psf-coc-wg-addendum-1-tim-peters"),
    ("meta/2024/12/20/todo-finish-todo-list.html", "/posts/todo-finish-todo-list"),
    ("posts/2024/12/20/todo-finish-todo-list/", "/posts/todo-finish-todo-list"),
    ("python-packaging/2024/12/24/python-packaging-1.html", "/posts/python-packaging-1"),
    ("posts/2024/12/24/python-packaging-1/", "/posts/python-packaging-1"),
    ("meta/2024/12/31/todo-list-2.html", "/posts/todo-list-2"),
    ("posts/2024/12/31/todo-list-2/", "/posts/todo-list-2"),
    ("posts/2025/01/01/new-year-new-blog/", "/posts/new-year-new-blog"),
    ("posts/2025/01/07/stupid-pipx-tricks/", "/posts/python-packaging-2"),
    ("posts/2025/01/07/python-packaging-2/", "/posts/python-packaging-2"),
    ("posts/2025/01/11/a-brief-annotation/", "/posts/a-brief-annotation"),
    ("posts/2025/01/24/leaning-in-to-my-ux/", "/posts/leaning-in-to-my-ux"),
    ("posts/2025/02/28/python-packaging-3/", "/posts/python-packaging-3"),
    ("posts/2025/12/31/oxidation/", "/posts/oxidation"),
]
