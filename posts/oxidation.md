# Python Packaging 外伝１: Oxidation and Radiation @python-packaging
# The Rise of <code>uv</code> in 2025 #python #uv #design ?2025-12-31

Today I'm offering a sort of ["side story"](https://en.wikipedia.org/wiki/Spinoff_%28media%29#Sidequels) to my main series on Python packaging. The main thrust of the series has been that everything is broken or historically has been broken; but I've also been trying to fight some common misconceptions and defend some things that people don't seem to like but which are actually quite reasonable in context.

But I've been doing this in the shadow of `uv` existing, and `uv`'s [momentum has been unstoppable this year](https://www.star-history.com/#astral-sh/uv&type=date&legend=top-left). Of course there were many adopters in 2024 as well, but we're now seeing more and more evidence in PyPI stats, surveys, CI pipelines etc. that [people are switching](https://old.reddit.com/r/Python/comments/1isv37n/is_uv_package_manager_taking_over/) away from `pip` (and other tools) to `uv`.

Which is unsurprising, given how positive the coverage has been overall. There have been [many](https://hn.algolia.com/?dateRange=pastYear&page=0&prefix=false&query=uv&sort=byPopularity&type=story) popular posts about it on Hacker News this year (I wouldn't mind adding to the pile!) and everyone is touting its features and praising their experience with it.

So before the year is out, I really wanted to write down some thoughts about `uv`'s success so far and the impact it's had on me — which as it turns out is mostly *not* about actually using it. This will mostly be gathering things that I've already said repeatedly in the aforementioned threads, but I think there's value to that.

<!-- TEASER_END -->

## Meta

{{% hitcounter %}}

It seems that writing has been difficult for me this year, much like everything else (although I did [get published in LWN](https://lwn.net/Articles/1020576/) which felt like a significant accomplishment). Or rather, it's somehow much easier to write comment replies on forums — responding to someone else's thought — than to choose a topic out of my ever-growing backlog and give it the organized, consolidated attention it deserves. Perhaps I'll have more thoughts on that another time.

At any rate, since I've let so many opportunities slip past this year, I *really* wanted to force myself to get in one last post this year. And this topic seemed like the obvious choice: `uv` still has lots of room to "eat" the Python ecosystem, and discussing it is definitely still popular. This probably won't be my best writing, but I know there are a lot of things I'd like to say on the topic — since I've said them before and enjoyed doing so.

In the new year, I'm thinking of moving these "meta" sections back to the end of my posts, and possibly updating my old posts that way as well. Please feel free to let me know how you feel about that, or anything else. There should be a Giscus-powered comment section at the bottom; or you can use the ['discussions' in the blog repo](https://github.com/zahlman/zahlman.github.io/discussions) directly; or send me an email at the link in the footer.

## The Elephant in my Room

If you haven't heard by now, I'm making [PAPER](https://github.com/zahlman/paper), a pure-Python package installer intended to replace the main use cases of both `pip` and [Pipx](https://pipx.pypa.io/stable/) along with doing some *very basic* virtual environment management. It should end up being much smaller and faster than `pip`, and capable of directly installing cross-environment cleanly without re-launching itself in the target environment.

But why? And why would I mention this in an article about `uv`?

Pretty simple: the superiority of `uv` over `pip` makes Python look bad, and in my view *needlessly so*. I think `pip` could be a lot better if it weren't hamstrung by ancient, short-sighted design and concessions to backwards compatibility. And the best way to prove that is to make something better.

## Rocket-ship-emoji Blazing Fast, Written in Rust Sparkle-emoji

The most obvious thing to say about `uv`, snark aside, is that it genuinely does perform `pip`'s tasks far faster than `pip` does, overall. The thing that annoys me about this is that the discussion will be full of people who attribute this to the implementation language and seemingly don't think about it any further. That's overly reductive, and a bad habit in general, but in this case I'm very solidly convinced that the conclusion is mostly just wrong.

First off, it's not really that `uv` is fast. It's much more that *`pip` is slow*. And there are many reasons I can point to for this. My thesis — and one of the main reasons I'm making PAPER — is that "`pip` is written in Python" is honestly pretty far down the list of causes of its poor performance. Of course I don't deny that doing things in a compiled language like Rust is going to offer additional benefits; I just doubt that they're as significant, or that they would matter so much once the real problems are addressed.

I recognize that's a bold claim. Python has a reputation for poor performance even among other "dynamic" languages (where JavaScript in particular has seen significant work on optimization). The proof is in the pudding, of course, and I've been cooking for far too long. But let me just point out the things I'm trying to fix, performance-wise:

1. `pip` is slow *even when it's effectively doing nothing*. Running something simple like `pip --version`, or `pip install` (with no packages specified) takes much longer than it ought to — many times as long as starting up the Python runtime itself; longer than a cold import of `numpy`; and certainly longer than the equivalent command for many other Python applications. And since installing with `--python` requires re-starting `pip` (re-running the code in a new process, under the target environment's Python), part of that cost is paid again.

    In my analysis, there's no single bottleneck causing this, but there is a clear cause: the sheer amount of modules being imported, which requires top-level code to run for each. In general this isn't explicitly doing anything explicitly costly, but "top-level code" includes `class` and `def` statements. Not the cost of calling functions or instantiating classes, but of creating the `function` and `class` objects in the first place. (Of course there is also the cost of garbage collection afterwards).

    In `pip`'s case, the main culprits are Rich and Requests (and their dependencies). The total module count is over five hundred — seriously. These are things that are not expensive in Rust, of course, but they're also things that are *generally unnecessary in Python, too*. Much of the imported code is not relevant to `pip`'s operation at all, and much more will be irrelevant most of the time.

    Python 3.15 is set to offer a [`lazy` soft keyword for imports](https://peps.python.org/pep-0810/), but it will be years before `pip` can reliably take advantage of that unless they offer separate wheels per Python version (which I doubt they will try). In the mean time, `pip` does try to defer the Requests imports until the first time an Internet request is needed.

    Speaking of Internet requests...

1. The cache that `pip` uses for downloads isn't really a download cache. It's an *HTTP* cache; `pip`'s web requests go through a wrapper that checks the cache first, through a controller that simulates a real web request. That cache stores the wheels according to a *hash of the original URL*, with a bit of `msgpack` metadata attached. (Wheels that are locally built from an sdist are cached separately, though.)

    So, for example, `pip` has been held back from [offering an offline mode](https://github.com/pypa/pip/issues/8057) (install only what's available in cache) for years since the idea was proposed, in large part because it *literally can't figure out what it has downloaded without contacting the Internet again*.

    Seriously.

    Nothing prevents a Python program from caching in a more intelligent way. It could also trivially cache the unpacked files from a wheel instead of (just) the wheel.

    Speaking of files...

1. One of the features `uv` is praised for, outside of its speed and ergonomics, is that its environments don't waste redundant disk space. Even without making several copies of `pip` itself (to avoid the issues with the `--python` option), it will waste your disk space in the long run by copying the files for the same wheel into multiple environments.

    The way `uv` achieves this is by making hard links to files from the cache rather than copying them. It's also a performance feature, and it's trivial to perform in Python, and it isn't meaningfully sped up by Rust because it mainly depends on making system calls (to code written in C).

    Hard-linking the files means not doing the disk I/O to read and write the file data, of course. But it's also much faster *even for empty files* in Python, because it can be cleanly expressed with fewer system calls:

        $ touch foo
        $ python -m timeit --setup 'import os' 'with open("foo") as f, open("bar", "w") as b: b.write(f.read()); os.unlink("bar")'
        5000 loops, best of 5: 54.4 usec per loop
        $ python -m timeit --setup 'import os' 'os.link("foo", "bar"); os.unlink("bar")'
        50000 loops, best of 5: 8.46 usec per loop

    There are even more opportunities to cache stuff than what `uv` currently does (I don't mind if they take the idea from here). In PAPER I'm keeping the wheel itself as well as unpacked files, just in case they're useful later; and I'm caching pre-compiled `.pyc` files (in my testing, reusing these is not problematic; the worst that happens is that paths might disappear from stack traces, but even then, only if the corresponding `.py` files are removed.)

    Speaking of precompilation...

1. In that famous initial benchmark, "Installing Trio's dependencies with a warm cache" (the one still at the top of the README), one major reason for `uv`'s outperformance (aside of course from the fact that tools like `pip-sync` rely on `pip`, which as explained above can't have *nearly* as "warm" of a cache) is that the default setting for `uv` was (maybe still is; I haven't been paying enough attention) not to pre-compile `.py` files to `.pyc` on installation, where `pip` does this by default. This pre-compilation is usually not *necessary* (unless perhaps you're installing something as root into a root-owned folder, that will later be run by an unprivileged user), and is sometimes completely *un*necessary (some modules of some packages might never be touched by some users). But it does avoid a performance hiccup the first time you use a third-party library.

    `uv` certainly *can* pre-compile to bytecode, of course. And when it does so, it parallelizes the process, and `pip` does not. Again, `pip` currently can't rely on modern Python features that would make thread-based concurrency actually parallel; it would need to spin up separate processes using `multiprocessing`.

    But it *could* do that. It's nothing specific to Rust. In fact, the standard library `compileall` offers a primitive solution for it (which Python itself depends on for its own installation process, in the Makefile). Separate processes have a cost, but it can be incurred according to heuristics and be a net win (and the per-process cost could be improved by other changes). And to my understanding, `pip` support for this is being actively worked on.

    And of course, when `pip` pre-compiles bytecode, it's invoking functionality within the interpreter which again is written in C. To my understanding, `uv` also uses that at the core, rather than trying to reinvent it.

    Speaking of parallelism...

1. `uv` also apparently parallelizes downloads. I'm unsure how much that really matters given that you only have one Internet connection and it's normally targeting either `pypi.org` or `pythonhosted.com`, but people have told me it's significant when you download a lot of packages.

    Speaking of downloading multiple packages...

1. The algorithm `pip` uses to resolve dependencies is overkill (and the code for it, [extracted](https://github.com/sarugaku/resolvelib) as `resolvelib`, is quite arcane). It's a fully backtracking resolve which rather naively chooses where to backtrack when it has options. Of course, it beats the one `pip` had prior to [April 2020](https://pip.pypa.io/en/stable/news/#b1-2020-04-21), which from the reports I heard (I've really never had any difficult package resolution cases for my own projects) often just straight up didn't work.

    The algorithm in `uv` is apparently much more sophisticated. This is very much not my wheelhouse (pun intended) and I'm hoping I can find a small third-party solution for it. But clearly it's the sort of thing that can be make to work by writing Python code. (More easily, if anything.)

Any of those could merit a separate post, and indeed I consider most of those topics part of my backlog.

## Easy as Seven-Two-Three

The hype around `uv` is strong enough that it seems to get credit for things that even the authors explicitly disclaim. In particular, [a workflow using a `uv`-based shebang has become popularized](https://duckduckgo.com/?q=uv+pep+723), using the [provision for declaring a script's dependencies inline](https://docs.astral.sh/uv/guides/scripts/#declaring-script-dependencies) described in the `uv` documentation.

Astral employees are, to their credit, quick to point out that this is not their invention; they've only implemented the [PEP 723 standard](https://peps.python.org/pep-0723/). For example, you [can do all the same things with Pipx](https://github.com/pypa/pipx/pull/1100) using `pipx run` (although the [reference documentation doesn't explain this](https://pipx.pypa.io/stable/docs/#pipx-run) and you [have to dig pretty deep](https://pipx.pypa.io/stable/examples/#pipx-run-examples) to find it mentioned in the examples), and have been able to do so since late 2023. (But of course, it's even less performant than `pip`, as it wraps `pip`.)

And again, this is an ecosystem-wide standard now. It's worth noting that it was authored by [the creator](https://github.com/ofek) of [Hatch](https://github.com/pypa/hatch), and the [competing proposal](https://peps.python.org/pep-0722/) came from [a `pip` maintainer](https://github.com/pfmoore). So of course Hatch [can do it](https://hatch.pypa.io/dev/how-to/run/python-scripts/). And while it [appears that a script runner would be out of scope for `pip`](https://github.com/pypa/pip/issues/12891), at least support [has been recently merged from a PR](https://github.com/pypa/pip/pull/13052) for *installing* PEP 723 dependencies (so it presumably will appear in 26.0).

Presumably there are other tools that can do it too.

## It Slices, it Dices, it Makes Julienne... Wheels?

One of the things many people seem to like about Rust is that it strives to be an all-in-one solution, for both developers and end users. On top of what other tools like Hatch, Poetry and PDM have offered, it even grabs and installs [standalone builds](https://github.com/astral-sh/python-build-standalone) of Python, thanks to the work of [Gregory Szorc](https://github.com/indygreg).

This is not my favourite thing at all; I very much subscribe to the UNIX philosophy and would prefer to compose my tool chain. It comes across that the various packaging standards developed over the last several years have been aimed at facilitating that. There was a period when I was using Poetry, but it wasn't really for package management, but for its build backend. (Since my projects generally are pure Python, I mainly use Flit now, but will of course switch to [`bbbb`](https://github.com/zahlman/bbbb) when and where it meets my needs.) Of course, `uv` [even covers that now](https://docs.astral.sh/uv/concepts/build-backend/), at least for pure Python projects.

Really, I'm mainly not a fan of having a bunch of subcommands of `uv` (and the shortcut `uvx`) that do what I see as widely disparate things. I felt the same way about Poetry, and I especially dislike having these tools manage the *use* of virtual environments (by providing a "shell" and/or automatically choosing which one to use based on the current working directory). I use the stock activation script when in development mode; that isn't everyone's cup of tea, of course, but I know I have the freedom to just specify a path to the environment's Python directly. (Which I often do when I'm just messing around with temporary environments to test something out.)

But I can't really do anything to change popular opinion.

## Conclusion

I can't really offer much of a conclusion here. I'm writing out some thoughts in a blog post; this isn't some formulaic high school essay. If you like `uv` and it's solving real problems for you, by all means continue to use it and don't let me hold you back from that. It just... isn't the tooling I hoped we'd get, for reasons that probably don't matter to a lot of people. If you like the ideas behind what I'm doing, I'm happy for any and all support. And I hope I can keep teaching people about Python packaging — and about Python, and really anything else I know about — far into the future.

Happy New Year.
