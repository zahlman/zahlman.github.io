# A Brief Annotation #python

I've been quite busy working on both the next article in my [packaging series](/tags-and-series/series-python-packaging) and on the overall appearance of the blog (I wasn't able to keep that confined to the weekend, apparently).

So, today, just a quick note, on the occasion of the 4th anniversary of the creation of [PEP 649](https://peps.python.org/pep-0649/) "Deferred Evaluation Of Annotations Using Descriptors".

Yes, that's a mouthful, but in short: starting in Python 3.14, if you use annotations, you'll be able to defer the evaluation of the annotation code. (The feature [was supposed to be added for 3.13, but didn't make it in](https://discuss.python.org/t/_/21331/43).) That means you don't have to rely on strings for forward references in your type annotations, but you can still make full use of annotations at runtime (you'll have a proper object for the annotation itself, rather than just a string). Thank you to core Python developer Mr. Larry Hastings for putting a tremendous amount of effort into refining this proposal.

Now, I don't personally use type annotations very much - I don't use a type checker at all; I only write annotations as a form of documentation. But as it happened, [when I was new to the Python Discourse forum](/tags-and-series/series-python-discourse-ban), I came across Mr. Hastings' post, puzzling over the best way to name what will soon become the `__annotate__` attribute of annotated objects.

The name `__annotate__` [was my suggestion](https://discuss.python.org/t/_/25672/4).

I was not credited in the PEP, and I [was ignored](https://discuss.python.org/t/_/25672/61) when I tried to point this out. So it falls to me to draw attention to my contribution.

This is all very niche stuff, of course - but I'm happy to have been able to leave this mark on the Python language itself, as opposed to just making useful things with it.
