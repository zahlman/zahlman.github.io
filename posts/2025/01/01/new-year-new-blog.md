<!--
.. title: New year, new blog
-->

You're not imagining things - the blog has a whole new look, in large part as a result of switching to the [Nikola](https://getnikola.com) site generator.

<!-- END_TEASER -->

## Meta

{{% hitcounter %}}

## Why Nikola?

Honestly, the most important reason it that it's implemented in Python. That means I can use the Python tools I'm familiar with to manage the program itself, and I can debug, configure and extend the system in Python. I probably could have chosen Pelican instead (and it's probably possible to contort Sphinx into blogging software rather than using it for documentation), but Nikola is what happened to come up first in my search when I first got frustrated with Jekyll.

I have to admit I'm not a huge fan of Ruby. Many years ago I thought I'd learn it properly, but I just never encountered a compelling use case, and I was constantly left with a feeling that the language was just *weird* compared to Python. It fills the same niche, broadly speaking, but somehow it just never clicked with me. (I'm also not a fan of having to write `irb` rather than `ruby` at a command prompt to get an interactive interpreter; the design makes sense from a Unix philosophy standpoint, but still somehow feels wrong.)

Anyway, building Jekyll pages locally was literally the only reason I had Ruby installed, so that frees up quite a bit for me. The main upsides Jekyll offered me is GitHub's out-of-box support: your repo only needs to contain the source, and the GitHub Pages integration system takes care of the rest. At least for now, using Nikola my source is on a separate branch of the repo, and the master branch needs to contain the built Nikola output. This mildly offends my sensibilities as regards how using Git is supposed to work - but I'll live with it.

## Major differences

But while I would have switched anyway as long as I could make things work, I *have* noticed that the Default Nikola Blog Experience (TM) feels a lot better than what Jekyll offers me:

* Post links on the main page show the post contents by default, and make it very easy to trim that down to a teaser. I get a "Read more..." link out of box with straightforward customization.

* The CSS is nicer for the default blog theme, despite still being quite minimal. In particular, font sizes for header tags make more sense, especially with inline code formatting within a header.

* It's easier to organize posts and static pages the way I want, and the default theme includes some additional useful features (an RSS feed, archive directory and tag list). It was also obvious (explained in comments in the main config) how to do DuckDuckGo search integration, so I have that now.

* Posts automatically get previous/next links at the bottom, and controlling pagination for the main index is trivial. (Maybe the latter was trivial with Jekyll, too, and I just didn't notice due to not having enough posts yet to care. Whatever.)

Overall, I'm much happier with what I have now. Aside from what I got for free (or at least very cheap) from Nikola, I've also set up a new system for hit counters - going forward, every post will have one, absent a compelling reason to exclude it. I'm restarting all the counters today, although you can still access the stats for the old counters I considered temporary - you just won't automatically bump them by refreshing the page.
