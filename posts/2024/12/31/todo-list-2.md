# `fixup! added list` #meta #personal #python

# The rest of the TODOwl

Happy new year to all.

Today's post is about a folder on my desktop named `dev`. It's where I've kept (for many years, well into my Windows-using days, even into the era when I used SVN rather than Git) all my working copies for my own projects (and forks of others'), mostly Python code of course. (I'm not sure how I organized things at the time, but there are projects in there dating back to 2006.)

<!-- END_TEASER -->

## Meta

{{% hitcounter %}}

### Changelog

**January 1, 2025**: Added this meta section; reorganized the introduction to allow for a short, sensible teaser (and to update on blog migration status); added a hit counter (going forward, most if not all posts will use this setup).

## But first...

[A little while back, I resolved](/meta/2024/12/20/todo-finish-todo-list.html) to establish a daily habit of work on this blog and/or my code projects, with the goal of posting every weekday.

That is, optimistically I hoped that [my previous post](/python-packaging/2024/12/24/python-packaging-1.html) would appear December 23, the next in its series on the 24th, this one (written in advance on the weekend) on the 25th, and today I'd be making the 7th post since that resolution.

Obviously, I've fallen well short of that mark. But I actually feel confident about the current project, because I'm doing a pretty good job with the underlying goal of Doing Something every day. It just turns out that the kinds of blog posts I want to write are, apparently, around 4500 words long (at least, the previous one and this one are in that ballpark - I didn't really expect to end up with 30 top-level bullet points in today's list of project ideas!), and it takes me longer to produce that volume of content (with the quality of editing that I want) than I realized. Going forward, it seems like 2 posts per week is a more realistic target - and that's without accounting for [posting canonical Q&A on Codidact](/codidact) in lieu of blogging.

One thing I noticed is that my previous post (which I actually finished after midnight, and didn't share on [HN](https://news.ycombinator.com) until the afternoon of the 25th) has gotten enduring attention - [traffic picked up](https://hits.sh/zahlman.github.io%202024%20python-packaging-1/) after the weekend. I don't know who looks through [older HN posts with few upvotes](https://news.ycombinator.com/item?id=42511439); or shares links to technical content like mine even without a fancy social-media widget being provided; or if anyone is actually *following* my blog - but thank you all.

One more point of order: over the weekend, I investigated switching from Jekyll to [Nikola](https://getnikola.com/) as a blog engine, and I'm generally very happy with the results. As you can see, I've now migrated over; check out the [next post]() for details.

Anyway.

Somewhere around that time in late June that I mentioned in the first TODO post - when I deleted that blank TODO text document - I also reorganized `dev`, categorizing projects roughly by status - actively developed, actively maintained, shelved, ideas for later etc. My classification is not entirely accurate, though, and many things stored in `dev` are not really worth mentioning here (for example, checkouts of random FOSS projects just to fix a bug and submit a PR). Many of my projects are filed as "superseded", meaning that I've given up on them in favour of a newer idea for the same general sort of project that I think is better.

Today I'm going to try to give an accurate picture of the projects that still hold some importance for me, grouped in a way that makes sense to me today (as I scanned through the folder, I found myself questioning many of my categorization choices).

Without further ado:

## In development, now or soon

The two projects at the forefront of my mind right now are a Python [build backend](https://packaging.python.org/en/latest/glossary/#term-Build-Backend), "bbbb", and a Python package installer, "PAPER". Neither of these projects is really usable for anything yet, but I'll include links for the GitHub repos anyway.

* [bbbb](https://github.com/zahlman/bbbb/) is the "Bare-Bones Build Backend".

    * The main goal is to improve on Flit's ideas (like having a separate wheel for *just* the wheel building backend that an installer like Pip can use, vs. a full environment for devs to create wheels and sdists), by focusing even more on size and simplicity (using `build` to provide a frontend for developers, and taking extra steps to ensure that the "core" wheel contains *only* what is needed to make wheels).

    * On the other hand, it will provide *simple* hooks that make it possible to invoke a customization module in the wheel-building process, and also to use a separate script to customize making an sdist from the source tree. Unlike with Setuptools, the wheel-customization code has clear, specific, narrow purposes (not specifying metadata!), and it implements some basic hooks (here's an entry point where you can shell out to compilers; there's a hook to rearrange package folders in the build environment) rather than calling a "setup" function or working with a giant plugin class library.

    * Additional functionality will be provided through "plugins" - although for the most part, this will probably just consist of libraries that you can import from a `bbbb` sdist-building or wheel-building script to get additional useful functionality. For example, I have a design for a simple Python-based make system, wherein your "Makefile" equivalent is actually Python code - the library just uses decorators to interpret your functions as build rules, and determines which to call.

* [PAPER](https://github.com/zahlman/paper) is the "Python Application, Package and Environment wRangler", a replacement for Pip and Pipx. The focus is on an elegant design and on making a tool *much smaller* than Pipx - or even just Pip - while covering the basics of package installation and smoothing over the bumps with using venvs.

    * Initial versions will support Linux only until the basic idea is worked out.

    * The expected way to install Paper for command-line use is to download and run a zipapp, which bootstraps Paper into its own isolated environment (similar to how Pipx sets up a Pip environment and reuses the same copy of Pip, but much more [ouroboros](https://en.wikipedia.org/wiki/Ouroboros)-y).

    * It will explicitly offer an actual programmatic API from the start, even though you shouldn't ordinarily need one. Instead of using `subprocess.call` to run Paper through the command line, you explicitly declare one of its internal packages as a dependency, and call its functions (which might involve decorators to spawn the code in a new process or run asynchronously).

    * It will only run as an ordinary user (or at least drop privileges when building), and only install into venvs. But you can choose which venv to use(it doesn't need to be in the environment it installs into), and you can ask for a new venv to install a library (unlike Pipx, which arbitrarily refuses to make a new venv unless it can find an application entry point).

    * The planned strategy for caching downloads is much simpler, saving tons of code while also making it much easier to work with the cache externally. (In particular, the wheels are already right there in the cache, saved as plain files with their actual names, rather than a `cachecontrol` database.) 

It feels hard to make these points briefly - perhaps my ideas will be clearer after I've done my other posts explaining the problems with Pip and Setuptools.

## Upcoming

* Parstruct will be a successor to [dsa](https://github.com/zahlman/dsa), the latest (and hopefully final) in a chain of attempts I've made at tools for *giving meaning to binary data*. The general theme of these tools is that they read some binary chunk at some file offset, parse it according to rules created in a domain-specific language, and output a friendly, text-based representation. Then the process can be reversed: edit the textual output, and the tool can use the same ruleset to pack the data back into binary and dump it to file, or insert it into an existing file.

  The special trick here is to have a language which allows for describing "pointers" or other references in the data - i.e., values that represent another file offset. This way, it becomes possible to deal with complex data structures such as one might find in, say, a static data segment of a compiled executable, or even the machine code itself (creatively interpreting jump instructions as "pointers").

  The old `dsa` project has most of the building blocks in place for this (as well as a plugin system for filters that can handle more complex data transformations, like compression), but I've left it unmaintained for quite some time. I also had two key ideas for the new project: a common syntax for the rules themselves and the "disassembled" output; and integrating the rules-based parsing into the overall system as though it were just another plugin (rather than the plugin system being a hack on top of the rules language-parser). Both of these ideas will be encapsulated in `ctb` (described under "smaller ideas" below).

  I've been working on this general idea on and off since the 2000s - but attempts prior to `dsa` don't feel worth mentioning at this point.

* `zrender` is the name I'm giving to a suite of rendering software, aimed at creating images and videos from a programmatic description - similar to [Manim](https://www.manim.community/). I want to include simple command-line utilities for tasks such as making a collage from a few images (giving layout rules in a simple language), and a text layout language focused on shaping, positioning and justifying text and elegantly handling Unicode (rather than being focused on making it easy to present mathematical equations properly, like with LaTeX).

## Visions

* Fawlty is the programming language I'm designing as a spiritual successor to Python, with a focus on naturally avoiding the pitfalls that new Python developers fall into (and stepping back from a few newer ideas in the language that I disagree with), while preserving general ease of use and syntactic elegance. It's designed explicitly under the assumption of a 64-bit, managed environment (I'll be assuming .NET in discussion, with the expectation that C# would fill the role for Fawlty extensions that C does for Python).

  It might be years before I can put any serious implementation work together (or it might never happen), but I plan to blog about various aspects of the design in the near future. I've been thinking about the design off and on since February, in quite a bit of detail for certain aspects (like the key data structures, and the compilation model).

* I keep [a repository called Peptides](https://github.com/zahlman/peptides), where I once gathered some miscellaneous ideas for things that I'd like to see as improvement to Python: refactorings of the standard library, little bits of functionality, etc. I was also going to draft PEPs in there - although eventually I realized that the process of even getting traction for a new idea in Python is really daunting, never mind actually writing a PEP and getting it considered, much less accepted.

  As part of that effort, though, I imagined a project called PACL - Python Alternative Core Libraries, intended as a radical departure from the "batteries included" idea. The idea is to replace the standard library: offer a Python distribution that includes only those few standard libraries that really need to be built into the interpreter (stuff like `sys`) and some bootstrap installer (like Paper, perhaps 😉), and then offer a package which covers a variety of essential needs with Pythonic interfaces. So for example, instead of including low-level networking libraries, there would be a top-level package similar to Requests (vendoring what it needed from the original standard libraries). Then, you'd have options to install either the entire suite, or just coherent chunks of it.

  One of the posts I have in mind for the further future is a whirlwind tour of the Python standard library. The idea behind PACL would probably make more sense after that.

* WebBoard is a concept I had in early 2023 for a sort of collaborative whiteboard webapp - although "corkboard with red string" might be more accurate. The basic idea is that you can drag around panels where you input Markdown source and can toggle a rendered view; selecting text from a panel and dragging it to the background copies the text to a new panel, which is automatically associated with the original. Then, changes to the Markdown source are tracked in a Git repository (each panel represented by a `.md` file, perhaps with some metadata), with each user automatically set up on a separate branch. The branches could be merged either collaboratively or by a designated coordinator. The panels would have some form of ID allowing for easy cross-linking (with the standard `[]()` Markdown syntax, but using an ID in place of a URL) and explicit association (separate from the implicit tree structure created by the drag-and-drop method).

* TutorRing is a hypothetical website (or site software) that I imagined being built on top of WebBoard - adding tags and other metadata to the panels, and a permission system etc. to users. The idea is that plain WebBoard provides a Wiki-like experience, but by allowing some panels to represent "questions", you can build something more like Stack Exchange or Codidact.

## Smaller ideas

* `cmdargs` is a barely-started alternative to `argparse`. I'd need a separate blog post to explain my motivations properly.

* [`cookiebaker`](https://github.com/zahlman/cookiebaker) is a wrapper for [`cookiecutter`](https://github.com/cookiecutter/cookiecutter) that also does an initial Git commit and some other small things. I've been using it to start new projects. I want to come back to this, and fork `cookiecutter` to cut out some bloat and use TOML exclusively rather than YAML (which cuts out more bloat, is simpler and IMO just overall nicer - especially since `pyproject.toml` means Python developers will need to understand TOML more going forward, and since TOML support made it into the standard library).

* [`codecs2`](https://github.com/zahlman/codecs2) would be an attempt to bring back the elegance of how the standard library `codecs` worked in Python 2, but preserving a clear `str`/`bytes` distinction. You'd be able to build a codec chain simply, with automatic checking that each stage produces appropriate input for the next (and codecs that convert between `str` and `bytes` would automatically choose the "direction" to transform based on the input). It would also offer a command-line interface to let you do simple tasks like changing the encoding of a Unicode text file (by specifying its current encoding and a new one).

* `ctb` stands for "Command-Tagged Block" - the format I alluded to above in the Parstruct description. It's a simple way to describe data that logically consists of separate "chunks" in a custom format, each tagged with metadata "commands" that explain how to interpret the custom format and apply filters. I can also see this being used to externalize Python docstrings: the "chunks" are plain text (or perhaps using some simple escaping syntax) and the "commands" indicate which function/module/class the corresponding chunk belongs to. This is hard to explain without concrete examples - when I have something stable that I'm actually benefiting from, I'll definitely want to blog about it.

* [`data`](https://github.com/zahlman/data) would be a way to manipulate "multi-dimensional arrays" like NumPy's, but using native Python data (for "arrays" of objects, a list of those objects; for numeric elements, a `bytes` containing the raw, packed value representations) and code (implementing only the basics of NumPy's magic slicing/indexing, and broadcasting for simple operators like addition). This would allow people to do simple manipulations on image data (for example) without a heavyweight compiled dependency (i.e. attaching tens of megabytes of NumPy to a few kilobytes of one-off scripting), in places where performance isn't critical, while obviating standard library modules like `struct` and `array`.

  Like NumPy, my design for `data` is based heavily on the idea of having "views" for the underlying actual storage. One way I can see these used is to transform image data transparently between different colour spaces: you could have a simple wrapper where you modify the `.y` of some RGB data as if it were actually YUV data, and the corresponding new RGB values are computed and stored.

* f(t) will be a library for making simple composable functions in one parameter (usually a floating-point time value, but also possibly an integer) - useful both standalone and as a key component of `zrender`. The key idea is that if, for example, `t` is an object wrapping the function `lambda t: t`, then writing `t * t` creates a wrapper for `lambda t: t * t` (although under the hood, without optimizations, it'd look more like `lambda t: ((lambda t: t)(t))*((lambda t: t)(t))`). Slicing could give a function with a restricted domain (and slices could be combined to make piecewise functions); indexing would actually apply the function (since calling it would do function composition).

  I have previous work for this called [`funcyprop`](https://github.com/zahlman/funcyprop), which uses SymPy (which feels absurdly heavyweight for what I'm actually doing with it). The idea here was to create object properties that would automatically update according to a combination of a global time value and the object's internal state. However, this is probably not a real usability win over just having plain functions which can be easily composed.

* [`indexify`](https://github.com/zahlman/indexify) is supposed to implement "buffered" lazy iterators: as you step over the source iterator, the results are cached, so that you can seek backwards and even have random access (if the index has been seen already, it's just returned; otherwise the iterator is advanced as far as needed). This would allow, for example, for implementing a lazy Cartesian product of multiple infinite generators (like `itertools.count`). With a bit of work, I think this could also handle use cases like reading file data into a buffer a chunk at a time. The repository has sat idle for a decade now, but I still like the underlying idea. I think `more-itertools` might supply something similar; I need to investigate that properly.

* [`lzp`](https://github.com/zahlman/lzp) is supposed to be a combination patching and compression format based on the Lempel-Ziv algorithm. The idea is that instead of having a rolling window based on previous input, you have a potentially unbounded window (and commands to seek around that window by bounded distances) which is seeded with zero or more inputs. For example, if you diff files X and Y, you produce a patch which transforms X into Y; to decode the patch file, you supply X as a seed for the window (without that seed, the decoder will reach out of bounds and raise an error). But you can equally well just compress Y by, in effect, asking for a compressed diff between an empty input and Y. 

* [`package-installation-test`](https://github.com/zahlman/package-installation-test) is exactly what it says on the tin - a package specifically designed so you can test that your package installation processes are working as intended. In particular, it was intended to help diagnose problems due to [`pip` and `python` referring to different environments](https://stackoverflow.com/questions/14295680). (Note to self: that Stack Overflow canonical is *awful*; offering a better replacement on Codidact is high priority.) I'm thinking of revising it to help demonstrate some other basic Python packaging concepts: like what happens when no wheel is available for a specific version of a package (and [how version capping can go wrong](https://iscinumpy.dev/post/bound-version-constraints/)), and the differences between [namespace packages](https://peps.python.org/pep-0420/) and regular packages (with `__init__.py`). (Hopefully this can help stop people cargo-culting about `__init__.py`, and therefore stop asking [questions about why adding `__init__.py` didn't fix a problem that it isn't intended to fix](https://stackoverflow.com/questions/11536764).)

* `pyrameters` was an idea I had for representing a group of function arguments (positional + keyword) for a function call as an object. You'd be able to `.invoke` a callable on that object to call it with the represented arguments, and easily combine argument groups, and do further manipulations. Basically, a framework for making adapters for functions that bind parameters (but with more flexibility than `functools.partial`, and without accumulating layers of wrapping if you bind repeatedly), but also for reordering parameters or inserting dummy parameters.

  I also wanted to include some support (likely through dynamic code generation + `eval` tricks, like how `namedtuple` works) for writing generic decorators where the decorated result has a signature based on the original function (instead of hiding that information behind a `(*args, **kwargs)` signature and hoping the documentation is enough to go on). This makes it sort of a successor to `frosting` (see the next section).

* [`retile`](https://github.com/zahlman/retile) is a tool for reading raw bitmap data that's organized into tiles (e.g. 8x8 or 16x16 tiles that are common in raw or custom-compressed image data for older hardware, especially consoles) and doing simple manipulations. If it doesn't get folded into `zrender`, it'll probably at least take advantage of some of the other pieces I'll need to develop for it.

* SLIP (Simple Logging and Instrumentation in Python) is an idea I recently had (no code written whatsoever) to replace the standard library `logging` functionality with a more modern, Pythonic approach. Logger objects would use simple, Pythonic interfaces rather than the old-school, heavily-class-oriented design inspired by Log4J; and functions can be given a decorator which times their execution and updates an indent level for logging calls within the function (so you can see hierarchical output breaking down execution time). I've taken DIY approaches to this sort of thing in a few previous projects and I'd like to have something standard and reusable.

* `strext` is another idea, like `codecs2`, that should have gone into my Peptides repository but that I kept separated out for some reason. The idea is just to add some functionality to the built-in `str` type. In principle, `str` isn't supposed to be modifiable from Python (so *string literals* wouldn't get the functionality without explicit wrapping), but apparently in CPython there's a trick abusing the GC which allows for faking it.

  Unfortunately, I've largely forgotten what "some functionality" entails, beyond a tweak to the `translate` method....

* I keep coming back to the idea of a data type that efficiently represents sets of integers, or dicts with integer keys - with a compact representation for ranges of adjacent integers, and the potential to represent ideas like "every even value from k to infinity". I'll write a little bit and then stop and forget about it until perhaps years later. I don't know why, except that a tool like this would be useful in contexts where Parstruct is useful (in particular: to keep track of regions in a file that have already been unpacked, or which are conceptually "free" to overwrite).

* I really want to make some kind of tool for handling common simple representations of structured text data - so, XML, TOML, JSON, CSV (viewing the data as simply a list of dicts or list of lists) and possibly a few others - and converting between them (with warnings for structures too complex to store into CSV). It would preserve comments where applicable, as well as metadata about how the original data was represented in cases where multiple representations are possible (like how [tomlkit](https://github.com/python-poetry/tomlkit) can preserve these things for TOML specifically). And for the in-code representation (which of course you could modify before writing out data), it would "auto-vivify" like traditional Perl data strucutres.

  However, there are probably a lot of unknown unknowns in putting together a coherent design for something like this; I really haven't thought about it as much as I'd like to pretend I have. Scope creep is a definite issue here. (Rules for filtering or otherwise transforming the data? Schema validation? etc. etc....)

  (Also, [my first choice of name was taken for some machine-learning thing](https://pypi.org/project/automl/).)

## Shelved... ?

There are many more old scraps of code in my `dev/` folder that I'll likely never touch again - including projects that were prototypes for, or superseded by, other things mentioned above.

But I can identify a few standouts:

* `burglar` is a hack to set up libraries in new venvs with Pipx and create your own entry points for them - so that you can quickly get at some library function instead of having to spin up a REPL or make your own CLI. I'm not sure if I'll come back to this after working on Paper, but it does also offer some potential for the standard library (by making it easier to get at e.g. `random` functionality without having to figure out a whole line of code for `python -c`).

* `cli` was my entry in the Click/Cloup/etc. genre, predating `cmdargs`. I think it'll make much more sense to develop `cmdargs` first, because I want to decouple from the idea that the input is a *command line*, making it more feasible to implement an interactive prompt loop with the same parsing strategies.

* [`epmanager`](https://github.com/zahlman/epmanager) was a tool specifically for Poetry projects to help manage entry points. The idea is that a decorator added `.invoke` "methods" (using a `functools.partial` trick) to functions you wanted to use as entry points. Then you could use an included tool to scan the codebase for the decorated functions and update `pyproject.toml` with Poetry-specific entry-point descriptions. When the package is installed, Pip would then generate an executable wrapper that calls the `.invoke` method, which would parse `sys.argv` and make the appropriate call to the original function. Yes, of course this idea overlapped with `cli` a fair bit.

  I don't use Poetry any more, but I'd like to come back to this now that there's widespread support for [*standard* `pyproject.toml` contents](https://packaging.python.org/en/latest/specifications/pyproject-toml/) (in particular, `[project.entry-points]`) as described in [PEP 621](https://peps.python.org/pep-0621/).

* `frosting` is something I made a while back to try to simplify the process of writing decorators. I'll have to check whether my old ideas actually offered anything better than [`decorator`](https://github.com/micheles/decorator) - I'm guessing not.

* `fspath` was an attempt to add even higher-level functionality to the standard library `pathlib.Path`. Acceptable equivalents, for at least some of it, were probably added to `pathlib` between the time I had the idea and now. I'd have to completely re-evaluate to decide if there's anything worth salvaging here.

* `ivp` is a little wrapper I made for Pip and `venv`: when a venv is active, it delegates to its own copy of Pip but using the `--python` option to install into the active venv. When there's no `venv` active, it offers a simple interface to make one. The idea is that you'd install this with Pipx and then you can use it regardless of whether a venv is active, and it'd install into the active venv even though it has its own environment, and it'd use Pipx's copy of Pip for this.

  However, like with `burglar`, this seems pointless now that I'm working on Paper. Even more so, really. I don't even use it now (I'll explain what I do instead, in part 2 of the Python packaging series).

* [`larch`](https://github.com/zahlman/larch) was the realization of a wild idea I had in early 2023 that every algorithm is really a graph traversal. I guess compiler writers are intimately familiar with the idea of viewing code as a graph of basic blocks connected by jumps; but this was an attempt to empower the Python programmer to view the Python code that way while writing it - and then process the graph in Python. - I think. Honestly, I'm not sure what I was hoping to accomplish here.
