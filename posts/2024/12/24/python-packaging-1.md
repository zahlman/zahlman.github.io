# Python packaging: Why we can't have nice things @python-packaging
# Part 1: The Old Refrain #python #pip #virtual-environments

This post is a start of a series I've planned about how packaging currently works in Python, what's wrong with it, and how to cope with the problems. But before I get into the meat of it, I want to talk about common complaints that *don't* resonate with me.

<!-- TEASER_END -->

## Meta

{{% hitcounter %}} ([Stats for old temporary hit counter](https://hits.sh/zahlman.github.io%202024%20python-packaging-1/))

### Changelog

**January 1, 2025**: Split off most of the original intro section, leaving the first paragraph as a teaser (since the default Nikola configuration expects one). Also added this Meta section and moved the hit counter into it (using a new and improved hit counter setup), to keep the counter out of the teaser (where it would log extra hits).

## Simple is better than complex, complex is better than complicated

It's no secret that [lots of people are unhappy with the system](https://duckduckgo.com/?q=python+packaging+is+a+mess) and have been for a long time. It's [practically a meme](https://xkcd.com/1987/). And to be clear, things [really aren't as good as they ought to be](https://nielscautaerts.xyz/python-dependency-management-is-a-dumpster-fire.html). There are plenty of problems that can be fixed, should be fixed, don't happen for other programming languages and have existed for an embarrassingly long time. And there are plenty of [discussions about how to fix things properly that drag on forever](https://discuss.python.org/t/pep-751-now-with-graphs/69721), sometimes [ultimately leading to a dead end](https://discuss.python.org/t/pep-582-python-local-packages-directory/963). (More about the ways that *discussing change proposals* fails, in a later post.)

But many of the things I hear people complain about constantly... are not like that.

I've gathered a handful of these points below, recasting them as some [well known pop rock lyrics](https://en.wikipedia.org/wiki/Complicated_(Avril_Lavigne_song)). Feel free to sing or hum along if you know the [tune](https://www.youtube.com/watch?v=5NPBIwQyPWE). 

With that explanation out of the way, let me te-e-ell you:

## Wheels and eggs and sdists make it seem so complicated

The idea of [sharing your Python code on the Internet](https://wiki.python.org/moin/VaultsOfParnassus) is older than the idea of [properly "packaging" it](https://wiki.python.org/moin/Distutils), which is older than the [idea](https://en.wikipedia.org/wiki/Python_Package_Index#History) of distributing it on the Internet through a [central repository](https://pypi.org) (which [hasn't had its current look for all that long](https://pyfound.blogspot.com/2018/08/redesigning-python-package-index.html)), which is older than the idea of having an [automated installer](https://setuptools.pypa.io/en/latest/deprecated/easy_install.html), which is older than the idea of [even trying to install dependencies automatically at all](https://packaging.python.org/en/latest/discussions/pip-vs-easy-install/)...

... And that only gets us to just past the halfway point of Python's [history](https://en.wikipedia.org/wiki/History_of_Python), 35 years and counting.

So, yes, of course there are a lot of historical formats for packaging Python code. But in practical terms, unless you maintain a Linux distribution (and need to build `.deb` or `.rpm` etc. for the system package manager to use), the [only formats that still matter are wheels and sdists](https://packaging.python.org/en/latest/discussions/package-formats/).

Eggs are a legacy format, and [it has not been possible to upload them to PyPI for about a year and a half now](https://blog.pypi.org/posts/2023-06-26-deprecate-egg-uploads/). Yes, [you can still *make* an egg](https://setuptools.pypa.io/en/latest/deprecated/commands.html#bdist-egg-create-a-python-egg-for-the-project) with Setuptools, but both the format *and the necessary [workflow](https://blog.ganssle.io/articles/2021/10/setup-py-deprecated.html)* are deprecated. (And yes, Setuptools still understands an `egg_info` command, and Pip may still use it; but this should be considered purely an implementation detail.) Even if you ignored all the advice, made an egg and created your own package index to share it with your clients, they would in turn have to go out of their way to find a way to install it. (Using Pip, they'd need a very out-of-date version, which would in turn constrain what Python version they could use.)

Nobody expects `.exe` installer wrappers on Windows any more like Setuptools [made long ago, in prehistory](https://setuptools.pypa.io/en/latest/deprecated/distutils/builtdist.html). Unless perhaps your users literally don't even know what Python is. If you're expecting others to `import` your code, you are not in this position; if you're in this position, you don't have to worry about "the ecosystem" at all and should instead be worrying about the *separate* choice of tools available for your very specific niche.

If you're writing code today to distribute on PyPI, all you need to understand is:

* **If your project *requires* the user to compile *your* non-Python code locally, use an sdist.** (And prepare to document the build process, especially on Windows, because chances are that your users don't have the necessary compiler(s) and Pip can't automatically set them up - people are [still working on metadata for that](https://peps.python.org/pep-0725/). And keep in mind that your project could become someone else's dependency, and *those* users will yell at you one day.)

* **If it doesn't, use a wheel.** That is, if it's at all feasible for you to do whatever necessary compilation etc. steps on your own machine first, use a wheel. Do this even - *especially* - if there are no compilation steps at all: if you [have only Python code](https://pradyunsg.me/blog/2022/12/31/wheels-are-faster-pure-python/), or if the non-Python code is all pushed into your dependencies. Not only is this faster and more streamlined, it gives your users peace of mind - they can [forbid Pip to build anything](https://pip.pypa.io/en/stable/cli/pip_install/#cmdoption-only-binary) (which would *run* arbitrary code in order to orchestrate the build) and still install your project (which, since it doesn't require building anything, shouldn't act like it does).

Despite the name, sdists aren't really a good tool for publishing your source and making it inspectable. The kinds of users who *want to* compile your non-Python code locally, generally also want to *read* the code first. The sdist format exists so that Pip (or other such tooling, like `uv` or future hypothetical competitors) can download code and immediately (try to) build it automatically and then install the result. That's what online VCS hosting services (like GitHub) are for. (Especially since systems for *verifying that an sdist corresponds to any particular VCS commit* - as [necessary](https://en.wikipedia.org/wiki/XZ_Utils_backdoor) as you might think them - are still very much a work in progress.)

## Your package name that ain't what you `import`, makes me frustrated

A lot of users express annoyance that when they get an `ImportError` and trace it to code that tries to `import foo` from a missing third-party library (supposing the library is indeed missing, after ruling out [configuration issues](https://stackoverflow.com/questions/14295680)), that doesn't give the name that needs to be used to install the code with Pip. **In general, `pip install foo` might seem like a reasonable guess, but it would often be wrong.** For example, to be able to [`import PIL`](https://pillow.readthedocs.io/en/stable/handbook/tutorial.html) one must install [`pillow`](https://pypi.org/project/pillow/); for [`cv2`](https://docs.opencv.org/4.x/db/deb/tutorial_display_image.html), one needs [`opencv-python`](https://pypi.org/project/opencv-python/) (or a [variant chosen after reading the documentation](https://github.com/opencv/opencv-python?tab=readme-ov-file#installation-and-usage)); and so on.

In principle, when you use someone else's code, the author of that code is supposed to worry about those issues for the `import`s in that code. A major part of the point of current systems is that you can install something and Pip will automatically ensure that you also have the dependencies; it does so by following metadata provided alongside the code - a `METADATA` file included in the wheel, which is generated by building the corresponding sdist. (There are multiple different ways to specify metadata declaratively in an sdist. Right now you aren't really required to use any of them; this *is* a problem and I will cover it properly in due time.)

But of course, if *you're the author* and you want to use someone else's third-party code as a dependency, then **you'll need to research both the dependency name to include in that metadata, and the name to `import`** in the code. And this is equally true if you *don't* intend to distribute your code - if, say, you're relatively new to Python and trying to follow a poorly written tutorial that assumes your environment is already set up. Or if you're trying to "learn by doing" and grabbing code examples anywhere you can find them (perhaps from LLM output).

And even if you *do* understand it, of course, you might find it strange. A lot of people do seem to feel like it shouldn't be this way.

**But in the current Python ecosystem, it really does need to be this way** - for a few reasons:

* [As I pointed out on HN recently](https://news.ycombinator.com/item?id=42422076), what you install may provide *zero or more* importable top-level names for your code: it isn't required to make any new `import` statement work (i.e. you're allowed to offer something installable that is installed purely for side effects of the installation process), and it may make multiple such statements work.

* Conversely (as alluded to above), *multiple different installations could provide the same `import`able name*, and there are some valid use cases for that. Aside from OpenCV providing separate versions for headless servers and/or including third-party (fourth-party?) contributions, one could use this to allow multiple different backends to provide a service to a frontend module that can then always `import` the same name.

  (Actually, the OpenCV use case isn't so vital any more, because of the ability to give lists of "optional" dependencies. But this fails if you need to change the rest of the code to account for the presence or absence of an optional dependency; and for the "headless" version it's awkward since you'd prefer to *default* to including certain dependencies and have a way to *withhold* them - which optional dependency lists can't do.)

* Many projects would like to give themselves clever names for "marketing" purposes, and many of those are not valid Python identifier names. They do get [normalized](https://packaging.python.org/en/latest/specifications/name-normalization/) (such that that part of a Pip command line is case insensitive); but even after following that normalization algorithm and then replacing hyphens with underscores, you'd still have names that *start with a digit*.

* Python developers tend to care about backwards compatibility (frequently they care far too much, in my opinion; but that, too, is a topic for another day). Sometimes project names change for open-source-political reasons, but it's important not to break existing code and people get upset even when you ask them to make one-line fixes. That's what happened with Pillow/PIL.

This is probably not an exhaustive list.

The careful reader may notice I've been avoiding a word in the above discussion: "package". Unfortunately, this has several meanings in the Python world, and it shouldn't be like that - but it's too late now. (And to be fair, it's nowhere near as bad as, say, the word `static` in the world of C/C++/C#/Java taken collectively.) There are [efforts](https://packaging.python.org/en/latest/discussions/distribution-package-vs-import-package/) to fix the terminology: documentation now says "distribution package" to mean something that you download from PyPI (and thus, one puts a "distribution package name" on a Pip command line), and "import package" to mean something you use in the code (thus, one writes an "import package name" in an `import` statement). (A note here: where the above link claims "An import package is a Python module", this *does* include both "modules" created from an ordinary `.py` file and "packages" created from a folder or `__init__.py`. From the perspective of Python's type system, *those are the same thing* - neither is even a subtype of the other.)

## Life's like this: you resolve, and install, and it breaks

There are two basic problems that I want to consider together under this heading.

First, "dependency hell". Installing a (distribution) package isn't as simple as just installing its dependencies and then the package itself. Well, it *is*, but it turns out that in the real world, your dependencies are themselves very likely to have dependencies. So actually, an installer like Pip has to compute the entire transitive cover of those dependencies.

No big deal, except that libraries can also have version incompatibilities, such that only certain versions of a dependency will work. Eventually you reach a point where the requirements are simply not satisfiable. Say for example that a project A depends on B and C; both of them depend on D; but they can't agree on a version of D that they'll both accept.

How does it happen that A ends up on PyPI in this state? Simple: the author explicitly installed a D version that *works with* both B and C *when the A code is tested*, but which either or both doesn't *claim to* support. Or author used out-of-date versions of both B and C that used to play together harmoniously, but the current versions don't.

You could reasonably blame many different people for this. Perhaps B and C authors made a [needless](https://iscinumpy.dev/post/bound-version-constraints/) restriction, perhaps following a "best practices" opinion from a packaging tool that blindly applied a [vision of how versioning should work](https://semver.org/) that just doesn't fit the reality of the Python ecosystem. Surely, A should have tested deployment in a new, pristine environment.

You might even blame the design of Python itself. Python environments don't properly support multiple versions of the same library - they really *can't*, because:

* there's no way *in the standard `import` syntax* to specify a version number unless it's actually part of the name;

* the import is resolved dynamically, so you can't arrange ahead of time to have different parts of the code look in different library paths (you have to make it happen at runtime, which entails having code run before the `import`); 

* by design, `import`s are singleton (stored in a global cache accessible as `sys.modules`) and *many modules depend on this for correctness*. (If the module API involves changing its global state, you really want it to be singleton. The module can always expose a class for you to instantiate if you *don't* want to share state. For example, if you circumvented `sys.modules` to obtain a fresh copy of the `random` standard library module, you'd end up producing a separate, separately-seeded PRN stream - not what you wanted, or you would have instantiated `random.Random`.)

Because of this design, you can't just [have both](https://www.youtube.com/watch?v=vqgSO8_cRio) versions to avoid the problem.

But regardless of whether you blame any of the developers, or Python itself, **it's definitely not *Pip*'s fault.** It really bothers me to see the blame thrown at Pip here, because *there are very many things wrong with Pip but this isn't one of them*.

----

The second problem is that even if Pip can correctly find what to install, it might fail in installation - because it might only be able to find an sdist and then not be able to make a wheel from it *on your (as the user) machine*. This *could be better, but it's hard*. Remember the thing I said above about documenting your (as the author) build process? This is why.

And this is where you get the infamous problem [that users only know how to describe as "subprocess-exited-with-error"](https://duckduckgo.com/?q=subprocess-exited-with-error), which of course often [gets blamed on Pip](https://github.com/pypa/pip/issues?q=label%3A%22resolution%3A+wrong+project%22+subprocess-exited-with-error) despite their efforts to explain right in the error message that `This is an issue with the package mentioned above, not pip`. And of course, when you try to search for help with that issue, you'll find a million other people who had a million different problems with that same symptom - because that isn't the actual diagnostic; **the important part comes *above* that line**.

The Pip maintainers are not wrong here. Pip isn't magic. It can't detect that you're missing a specific C compiler, or that the build backend's rules for choosing (or locating) one will fail on your system. It can't know that the library doesn't *actually* support your Python version despite claiming to in the metadata. It can't know that some legacy project using Setuptools has a hidden build-time dependency that's explained in the `setup.py`, but is *needed in order for `setup.py` to run* so that the need for it can be determined.

All Pip can do is identify (and possibly install) a build backend following the [protocol for specifying it](https://peps.python.org/pep-0518/), spawn a subprocess for the build backend, ask it to create a wheel from the sdist following the [protocol](https://peps.python.org/pep-0517/#build-backend-interface), grab the resulting wheel (if any), and forward the resulting output. In other words - act as a build frontend.

----

Unfortunately, these two problems sometimes play off of each other - because Pip's search for compatible versions might find an sdist that's difficult or impossible for most users to build, and it might give up there even though a wheel exists that could solve the dependency constraints (as they say). There has been a **ton** of discussion about what to do about this ([here's a proposal I floated](https://discuss.python.org/t/_/57474); and here's [arguably the simplest thing that could possibly work](https://github.com/pypa/pip/issues/9140), presented as a GitHub issue) but no clear consensus.

But it still isn't Pip's fault, and none of this is easily solved stuff that Python is just stumbling over for no reason. In other language ecosystems, installing projects doesn't commonly involve compiling code written in multiple other languages.

## [668 was a PEP](https://peps.python.org/pep-0668/), now I'm learning `venv`s too

(Windows users should probably just skip this part.)

Ah, yeah, [that one Stack Overflow Q&A with over a million views](https://stackoverflow.com/questions/75608323). The one where a bunch of supposedly technically sophisticated Linux users get a full-screen message, customized by their distro, [which exactly explains the problem](https://www.youtube.com/watch?v=35PQrzG0rG4) and suggests multiple reasonable courses of action; and then they throw up their hands in resignation and look for ways to beat the system into submission.

[For years, Python experts have been trying](https://askubuntu.com/questions/802544) to get the masses to stop randomly giving Pip `sudo` rights to install packages so that it can install libraries in the system's `site-packages` folder. This is dangerous (installation can **run arbitrary code**, and unlike the actual libraries you're about to use in your project, it's code that you won't get to *inspect* first) and egregiously unnecessary. I've also occasionally seen people randomly "fix" a problem with `sudo`, not understanding that it really only worked *because the root user has different environment variables*.

But not only are huge amounts of people - reminder: people who chose to use Linux as their operating system, who are nominally capable of using a terminal and writing code in a programming language - entirely cavalier about their use of `sudo` ([even when explicitly warned](https://stackoverflow.com/questions/68673221/)); they'll happily add a `--break-system-packages` flag to a command line, and their only complaint will be that they had to change their workflow. The *literal text "break system packages"* doesn't seem to give them the *slightest* pause.

The distro maintainers - in cooperation with the Pip team - have tried *many* things to get users to stop compromising their own systems and this is just the most recent. They've tried deliberately crippling the system-installed Python, by omitting Pip (which is included when you build Python from source) so that users have to install a separate package for it. They've gotten Pip to include warnings of its own. For that matter, all the way back in the `easy_install` days, `easy_install` would [install Pip in the user's home folder](https://askubuntu.com/questions/378349) instead of as part of the system.

But people just keep refusing to pay attention to clear warnings or to care about important concepts; they just want the code installed so they can run whatever thing. It really makes me wonder why anyone even uses Linux in the first place.

----

As explained previously, you can only practically have one version of a library in a given Python environment. As a developer, you're likely to create more than one project eventually. And the requirements of one project could actively create a problem for another, just by being there. The way you solve this problem is by having a separate environment, and the simplest approach is a virtual environment. Seriously.

(Keep in mind: if you use some all-in-one tool like Hatch, PDM, Poetry or Flit, *that tool is just wrapping that virtual environment management for you anyway*. Wouldn't you rather understand what it's doing, for debugging purposes?)

Plus, if you want your users to have a smooth installation experience (and not go yelling at the Pip maintainers about something that was *your* fault), you'll want to test deploying your code. That requires the ability to start from scratch, which you do with a new virtual environment.

----

But now perhaps you wonder: the system environment should be fine for *non-programmers*, who just want to use someone else's application written in Python... right?

No, not really.

[For a while](https://github.com/pypa/pip/pull/7002), `pip install` into the system Python installation, as a normal user, would default to a "user install", putting the packages in a user-specific location. (Before that, you would have to request `--user` explicitly.) This is supposed to keep them isolated from libraries installed by the system package manager (`apt`, `yum`, `pacman` etc.) and allow installation with user rights, so a renegade `setup.py` can't just stomp all over everything. (Pip [**will not drop root privileges**](https://github.com/pypa/pip/issues/11034) for building, *even now that it happens in a subprocess*. That *is* a problem, but PEP 668 is not.)

But such installations are still in the system *environment*. They can **still interfere with your system's operation despite not being in a system directory**. Because a lot fo the time, you run those tools as yourself, not as root. When you do so, the "user-level" libraries you installed are made available (i.e., the directory will be put on `sys.path` at startup), and they can therefore shadow imports that should use a system package instead.

For example, on a Debian-based system you can put modules in the user site-packages that shadow things that the `apt` script will import, and then user-level invocations of Apt can be broken. Or you can shadow the entire `command-not-found` utility, breaking the system for suggesting Apt packages to install when you typo a program name.

It's not a privilege escalation in itself (as far as I can tell - thankfully), but it adds annoyance, and risk. Perhaps, for example, malware on PyPI could drop a fake `command-not-found` program which then attempts some social engineering to get you to install the real payload, do someting regrettable as root, etc.

----

Please, just use the expletive-deleted venv. [It's not hard](https://chriswarrick.com/blog/2018/09/04/python-virtual-environments/). It's really not that bad of a design (there will be a post dedicated to this). It will make your life much easier in the long run.

The system Python is, generally speaking, just not suitable for development. It's not *there* to serve your needs as a developer. It's there to serve *Linux's* needs.

But it works very well as a base for creating venvs.

## Honestly, why can't we just have a standard package toolchain?

Speaking of all-in-one tools, a lot of people seem to think that Python would be better off including one, and that it was a [mistake](https://dublog.net/blog/so-many-python-package-managers/) to allow third parties to develop multiple competing options.

The thing is: in order to achieve the "ideal" of "only one way to do it", you need to be able to agree on *what "it" is*. Chris Warrick offers [one possible short list of "its"](https://chriswarrick.com/blog/2023/01/15/how-to-improve-python-packaging/#tooling-proliferation-and-the-python-package-authority); there's quite a lot of room for debate there. For example, "supporting pyproject.toml files" isn't well defined as a separate point; you might need to take `pyproject.toml` into consideration *as part of* implementing other functionality (building sdists and wheels), but also some people think that their "one way to do it" tool should provide an interface to *update* `pyproject.toml` (what's wrong with, you know, a text editor?), or perhaps *automatically* update it to correspond to its own "package management".

Contrasting all the various tools that exist in the Python universe, and counting up the "features" they offer and where they do and don't overlap, is in my view a completely misguided exercise. Most of the tools listed under the [PyPA umbrella](https://packaging.python.org/en/latest/key_projects/) are designed to be single-purpose, Unix-philosophy building blocks - and that's how I like it, personally. I don't see a point in "integrating" them under a single application name; running `awesome-tool build . && awesome-tool upload` doesn't seem inherently any better than typing `pyproject-build . && twine upload`. Sure, maybe the tool combines those steps. And maybe you can write a couple lines of shell script to do it yourself, and have control over how it works. (I'll probably come back to this theme in later posts.)

The way I see it, *users* should have a "single tool" so that they don't have to understand virtual environments and can just run applications. And that should include programmers who are just starting out, so that they can be eased into the concept of environments (which, again, is ultimately unavoidable if your code has dependencies and you have multiple projects) while installing libraries as simply as possible. Right now, Pip and the standard library `venv` can sort of fill this niche, but you end up having to talk non-technical users through a multiple-step command-line process, which is very much not ideal. And Pip has a lot of problems. From the other end, Pipx provides a surprisingly good application-installation experience, but it arbitrarily refuses to install libraries (but you can hack around this - more in part 2) - and it's still based on Pip.

On the other hand, *developers* have all of those needs *plus several more, which are not universal*. Some of them need to handle very complex build processes with CMake, Meson etc. Some might need to cross-compile or interface to CI systems. Some need to default to uploading to a private package index; some need to *implement* a private package index. Some want lock files, and there are many different opinions about how those should work. Some need to work with containers. Some have subtle nuanced needs that I can't eaisly explain here, or that I don't even understand.

And then many others will need *none* of that, and be overwhelmed with a tool that documents way too many options.

Something that isn't intended to be a secret, but doesn't get mentioned nearly often enough: the PEPs that [describe pyproject.toml](https://packaging.python.org/en/latest/specifications/pyproject-toml/) were conceived with the *explicit intent* that third parties would create multiple different build backends. And the `[tool]` table was provided so that existing single-purpose tools (such as Black and other linters or formatters, and MyPy and other type checkers, and automation systems like Tox and Nox, etc....) could all put their config data in a single "project" file. (Even though the file *nominally* existed specifically to *describe the wheel-building process*, leading to an [identity crisis](https://discuss.python.org/t/_/29684) of sorts.) But what ended up happening, of course, is that we got competition in *workflow tools* trying to manage everything, because that's what the community felt was lacking. And then each of those tools implemented its own build backend anyway.

In the next post in the series I'll show how the Unix-philosophy approach can be made to work with existing tools, and in later posts I'll comment on how it could be better.

## Yeah, yeah, yeah

Finally: I'd like to make an appeal for *honesty* from anyone out there complaining about the system. Approach the problems from a place of understanding how they came to be, rather than a place of pure frustration. If you present a "history" of Python packaging, don't just use that as an excuse to rant - it should be abundantly clear that you don't *need* an excuse. Instead, take the opportunity to show *how* that history is relevant today (i.e.: people haven't updated their workflows, and tools and standards can't properly fix problems because of the burden of legacy support - a topic for a future post in this series). Don't misrepresent what resources are available to solve the problems - there's no grand conspiracy here, just perhaps some mismanagement.

Please don't carelessly say that the reason such and such Python tool is so good is because it isn't written in Python. In almost every case, the *real* benefit is that the tool isn't *sharing the environment* of the project it's operating on. This line is especially often dropped when talking about `uv`, often accompanied by explicit Rust evangelism. Sure, Python code can be much slower than in other languages. But that doesn't matter a lot of the time (if you don't believe this, why are you developing in Python?), and a lot of `uv`'s performance advantages are algorithmic: its package resolution is (to my understanding) less... thorough and pedantic than Pip's, and it has much better strategies for reusing cached downloads.

And most of all, please don't [throw together a bunch of unrelated names from completely different categories](https://news.ycombinator.com/item?id=42419822#42420869) to try to emphasize the point about how complicated things are. There's more than enough *actual* complication to discuss. After all, no matter how good the system becomes, you'll still have to learn it.
