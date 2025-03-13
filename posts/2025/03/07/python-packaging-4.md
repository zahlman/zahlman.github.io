# Python packaging: Why we can't have nice things @python-packaging
# Part 4: Multipiplation #python #pip #bloat #virtual-environments

If you - like many other Python users - have multiple copies of Pip on your system, you might eventually start to wonder about why.

Now, the pat answer for how they got there is that you [have multiple Python environments](https://pypi.org/project/package-installation-test/), and each of them gets a dedicated copy of Pip (or at least most of them do). And the pat answer for why they should each have a separate Pip is [so that you can run them from Python in order to choose the right Pip](https://stackoverflow.com/questions/25749621), which will then install into that environment. Besides which - if every environment has Pip in it, people who want to [make programmatic use of Pip](https://stackoverflow.com/questions/12332975) won't have to list it as a dependency.

But if you're anything like me, eventually you'll find these answers like these supremely unsatisfying. You'll grow more and more annoyed with the realization that multiple copies of Pip are wasting your hard drive space. Sure, we have terabytes of it now, even on SSDs - but this is a matter of principle. Besides, making those copies takes time, and degrades your user experience of Python.

From within a virtual environment - sorry, a café - in the theatre of my mind, I hear a chant: [Lovely Pip! Wonderful Pip!](https://en.wikipedia.org/wiki/Spam_%28Monty_Python_sketch%29).)

Let's see what's going on over there, shall we?

<!-- TEASER_END -->

## Meta

{{% hitcounter %}}

## `virtualenv`

Before we can talk about Pip, we really need to talk about [virtual environments](https://peps.python.org/pep-0405/). If you use Python in any serious capacity, [you really should understand them](https://chriswarrick.com/blog/2018/09/04/python-virtual-environments/). I understand that a lot of people only run others' Python code, or put together some short scripts for personal use, and it's hard to get these users to care, [most of the time anyway](https://stackoverflow.com/questions/75608323).

If you've ever created a virtual environment "manually" - using the standard library [`venv`](https://docs.python.org/3/library/venv.html) module - you may have been underwhelmed by the results. It's slow, and seems to use a lot of disk space.

It wasn't always like this. Before `venv` was added to the standard library, there was [`virtualenv`](https://virtualenv.pypa.io/en/latest/). Only part of its functionality was ever included, and it's actively maintained in parallel, so it's actually become rather popular. And its users know that it can be made to run very fast.

When `venv` first showed up in Python 3.3, it was quite fast, too. Even in a debug build, using my 10+-year-old hardware (SSD notwithstanding):

```
$ time py3.3d -m venv test335d
[67557 refs]

real	0m0.111s
user	0m0.097s
sys	0m0.015s
```

## `venv` and Pip

I used Python 3.3.5 for that example because it was the last patch before Python 3.4.0, where it all changed.

But unfortunately, I can't show you an authentic demo on Python 3.4.0, because of OpenSSL, of all things. See, in Python 3.6, [older versions of SSL were deprecated](https://docs.python.org/3/library/ssl.html), but Python 3.3 and 3.4 actually expected an older version - I can't build SSL support for them on my current setup. And I suspect that's why I needed to use a debug build of 3.3.5 - the default build was segfaulting on startup, and I suspect that's SSL-related.

3.4.x builds start up fine for me, but trying to use `venv` with the default options will produce an error message - and hacking the relevant check out of the standard library will result in either an uncaught Python exception or another segfault.

Support for linking newer SSL (1.1.0) was backported to Python 3.5 - starting with [Python 3.5.3](https://www.python.org/downloads/release/python-353/), the first release after 3.6.0. But it was not backported to [Python 3.4.6](https://www.python.org/downloads/release/python-346/) - released the same day as 3.5.3 - (ironically) because the 3.4 branch was already in the "security fixes only" phase of development.

Interestingly enough, that new linking support has lasted quite some time:

```
$ ./python
Python 3.5.3 (default, Mar 12 2025, 18:33:13)
[GCC 13.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import ssl
>>> ssl.OPENSSL_VERSION
'OpenSSL 3.0.13 30 Jan 2024'
```

... except that I still got a segfault when trying to test out `python -m venv` with this build, and trying to track that down ended with a truly bizarre [heisenbug](https://en.wikipedia.org/wiki/Heisenbug) that I won't even try to explain here.

But thankfully, my pre-existing build of 3.5.10 worked, at least:

```
$ time py3.5 -m venv test3510

real	0m1.613s
user	0m1.439s
sys	0m0.177s
```

So, what happened?

## `venv`, Setuptools and Pip

The secret here is really impossible to keep. What changed is that Python 3.4 adds the `ensurepip` standard library module. This allows you to add Pip (and, originally, also Setuptools - which was a dependency of Pip for quite some time) to your Python installation's `site-packages`. But also, of course, to virtual environments, and in fact this became the default behaviour. You could (and still can) turn it off using `--without-pip` - but then you'd be on your own for figuring out how to install anything there.

Another issue here is the version of Pip involved. That Python 3.5 virtual environment ends up with Pip version 9.0.1 and Setuptools 28.8.0. Modern Pip is quite a bit bulkier, even though Setuptools is no longer included. For example, with the Python 3.12 build included in my Linux distro:

```
$ time python -m venv test312

real	0m3.292s
user	0m3.020s
sys	0m0.219s
```

The worst-case scenario is probably with Python 3.10 (before `ensurepip` stopped bootstrapping Setuptools):

```
$ time py3.10 -m venv test310

real	0m4.053s
user	0m3.638s
sys	0m0.236s
```

On the other hand, if I hack together a separate Python 3.5.10 build that bootstraps the "original" Pip and Setuptools dependencies from 3.4.0 (Pip 1.5.4 and Setuptools 2.1, respectively):

```
$ time ./python3510 -m venv test3510

real	0m1.286s
user	0m1.157s
sys	0m0.130s
```

## Pip, `venv`, Setuptools and Pip

The other issue here, of course, is that the bootstrap provided by `ensurepip` is effectively frozen in time. In that Python 3.12 virtual environment, for example, we get a *reasonably* new version:

```
$ ./test312/bin/pip list
Package Version
------- -------
pip     24.0
```

However, the Pip development team only ever supports the *most recent* release, and Pip itself likes to nag you with messages that a new version is available (unless you `--disable-pip-version-check`). So, in practice, you'll need to upgrade as well:

```
$ rm -r test312/ # start fresh
$ time python -m venv --upgrade-deps test312

real	0m4.890s
user	0m4.462s
sys	0m0.357s
```

Notably, this requires an Internet connection *even if* Pip's cache already contains the new version wheel - because it will contact PyPI to check if there's anything even newer. So the timing is a bit variable. (Doing the upgrade manually afterwards doesn't chagne anything.)

## Pip, Disk Space, Pip, Pip, Time, and Pip

Regardless of the approach you take, the resulting environment also takes up quite a bit of space:

```
$ du -sh test312
13M	test312
$ du -sB1 test312
13537280	test312
```

Which, to be clear, is almost entirely due to the Pip installation:

```
$ ls test312/lib/python3.12/site-packages/
pip  pip-25.0.1.dist-info
$ du -sB1 test312/lib/python3.12/site-packages/
13471744	test312/lib/python3.12/site-packages/
```

(The exact size will vary slightly depending on the directory where you try this, because compiled .pyc bytecode files will include paths.)

## Don't Worry, Dear, I'll Have Your Pip

Okay, so there seems to be a pretty clear bottleneck here. But what if we were to go back to the approach of `virtualenv` and Python 3.3, and just skip the Pip? What if we just made virtual environments that haven't got any Pip in them?

[As I discussed in a previous post](https://zahlman.github.io/posts/2025/01/07/python-packaging-2/), we absolutely can set up a system that only has a little bit of Pip. We'll just use the `--without-pip` flag for `venv`, and our virtual environment creation becomes dramatically faster:

```
$ time python -m venv --without-pip without-pip

real	0m0.053s
user	0m0.041s
sys	0m0.012s
```

And the environments become dramatically smaller:

```
$ du -sh without-pip/
56K	without-pip/
```

(And only about a quarter of that space is file contents; it needs to make a handful of folders.)

And from there, of course, we can use any modern external copy of Pip (22.3 or newer) to install into that new environment, using something like `pip --python without-pip/bin/python`.

So of course that raises two questions: Why don't people seem to know about this? And why isn't it the default?

In short, because everyone has been taught to do it that way, because it's supposedly easier to explain - given how Pip works.

Windows plays a significant role here. See, the normal way of organizing installed applications on Windows isn't very friendly for command-line use. Typically, each program gets a sub-folder within `C:\Program Files` (or whatever other drive letter you chose) - so if you want to use them from the command line, you'd have to add each of those entries to the `PATH` environment variable. That would pollute a [length-limited](https://stackoverflow.com/questions/34491244) environment variable, and also cause confusion between `.exe`s with matching names (not just Python, but the `pip.exe` wrappers).

This leads to all sorts of ways to set up a system where either `python` doesn't run Python, `pip` doesn't run Pip, or - most importantly - [`pip` installs for a different version of Python than `python` runs](https://stackoverflow.com/questions/14295680). (And the advice you can find about the problem most easily - such as the previous link - tends to be very confused.)

As a result, the common practice on Windows is to have the installer *not* add entries to `PATH`, and to use a single common [launcher program](https://docs.python.org/3/using/windows.html#python-launcher-for-windows) - installed directly into the Windows folder, so it's always on `PATH` - to choose a Python version. However, with this approach, `pip.exe` won't be on the user's `PATH` - not any of the copies. Instead, `py -m pip` is the recommended way to run Pip on Windows. (This also solves the problem that Windows won't allow `pip.exe` to replace itself on disk while running.) This way, the launcher finds an appropriate Python environment (and in 3.5, it was [improved](https://peps.python.org/pep-0486/) to support virtual environments as well!), and then that Python runs the `pip` module from its `site-packages`. And now there's a simple approach that can be taught to everyone - well, notwithstanding that Windows users have to write `py` while Linux users are expected to write `python`. (More recently, one of the core Python developers [got the idea](https://github.com/brettcannon/python-launcher) that Linux systems would also benefit from a Python launcher. But the idea doesn't seem to have gotten much traction - there's no PEP for it or anything.)

## Pip, Pip, Pip, Windows, and Pip

Speaking of Windows, a brief interlude.

As part of my research for this piece, I booted into the copy of Windows 10 I had lying around on another SSD, for the first time in probably years. I didn't dare connect to the Internet, but I could still test how `venv` under Python 3.8 coped with installing an older Pip version (20.1.1, I think).

To keep a long story short: Pip of that era was comparable in size. A Windows venv, at least in that test, took about an additional 1MB of disk space beyond what Pip requires - mainly because of a surprisingly large wrapper executable used to delegate to the system Pip, which also has to be duplicated for terminal vs. GUI uses of Python. (On Linux, the same `python` executable works either way, and the venv just uses a symlink by default. Asking `venv` on Windows for `--symlinks` failed for me and I didn't feel like investigating it, beyond noting that the error messages vaguely implied that it was trying to create symlinks *in the wrong direction*.) And it takes about three times as long to create the venv, whether or not Pip is included. Taking about 150 milliseconds instead of 50 [isn't a big deal](https://lawsofux.com/doherty-threshold/), but taking about 9 seconds instead of 3 certainly is.

(Overall, I was amazed how sluggish *everything* felt - since I didn't really have a memory of everything suddenly feeling more performant when I switched to Linux in the first place. I knew that my "baseline" RAM usage - i.e. with a single user logged in graphically, not running any programs - was higher on Windows, but I hadn't realized it was on the order of 70% higher. I guess the built-in "Windows Defender" has a lot to do with this - and perhaps also the venv creation time, considering all the I/O it does. I don't really want to get into this in any detail, but I do wish I'd done the experiment [before my Linux anniversary](https://zahlman.github.io/posts/2025/01/24/leaning-in-to-my-ux/).)

So, one could say that the slow performance on Windows is mostly Windows' fault, since the majority of the time taken there is time not taken on Linux. But I suspect this is really a multiplier that applies to pretty much everything, and anyway, neither Pip nor Python devs can really do anything about it. So I don't mind keeping my attention focused on Pip here. More to the point: the results vary slightly according to Python and Pip versions, but not enough to matter to the discussion. It's not a *temporary* problem in Pip; if anything, the long-term trend has been for the problem to get worse, as Pip builds in more backwards-compatibility layers. (The most recent versions of Pip are not the biggest, though; they've recently completed some migrations from one dependency to another, and no longer have to vendor both.)

## Pip, Setuptools, Pip, Pip, `easy_install`, and Pip

The justification I gave above for having Pip install by default... rings a bit hollow to me. Sure, our system might have multiple versions of Python installed, each serving as a base for multiple virtual environments. Using a command like `python -m pip` (or `py -m pip`) makes it immediately clear which Python we want to use. But having an entire copy of the program seems incredibly wasteful just to control the context in which it's used. Pip has its own command line, and as mentioned above (and in part 2), it *can* install cross-environment.

So, why are we copying Pip into the destination environment? Rather, why would Pip struggle to install outside of its host environment?

It seems like that has at least a bit to do with the history of Pip's relationship with Python. The core Python dev team has seemingly always sought to keep packaging at arms-length distance from the main project. (Well, notwithstanding the part where `distutils` was incorporated into the standard library [years before Pip existed](https://docs.python.org/2.2/lib/lib.html) and didn't get removed [until 3.12](https://docs.python.org/3/whatsnew/3.12.html), despite being roundly judged as broken, [long obsolete](https://stackoverflow.com/questions/25337706/) and unfixable - [e.g.](https://mail.python.org/archives/list/distutils-sig@python.org/message/HPQOKOFVTZUCSGKGCPLV64JZI2F4LVO3).) As such (and learning from the mistakes made with `distutils`), Pip really couldn't really (and didn't) become a standard library module or package. (Doing that would also have interfered with the separate versioning and maintenance of Pip; "the standard library is where modules go to die", as stated [in a famous talk by Kenneth Reitz](https://kennethreitz.org/talks/python-for-humans).)

But rather than becoming an entirely separately distributed program (perhaps even one that the Windows Python installer could check for and install when needed, like how it does with the Launcher), it became... a wheel stored within the standard library directory, with a separate standard library `ensurepip` that bootstraps that wheel into `site-packages`, if not already present. (I assume the `pip.exe` wrapper on Windows runs something like `python -m ensurepip` first before `python -m pip`.) So now you don't have to have Pip installed (although you still pay disk space for it, but the wheel is a fraction of the size of the unpacked library), but it's still available for you if you want it (and spend the time to let it unpack). Well, a specific version of it, anyway (the point was to *avoid* tying the Pip version to the Python version, but this way does allow for upgrades).

Well, that's *one* way to solve the bootstrapping problem, I guess. And I'm sure it's much more pleasant than the initial offer made by Python 3.3 - where you'd have to find a separate path to install Pip, perhaps using `easy_install`, or `ez_setup` (both part of Setuptools at the time, but maybe also made available separately - this is a depth of historical research I'm just not that interested in).

But really, a much cleaner solution was staring everyone in the face the entire time. Install Pip as a separate application, like the Python Launcher for Windows. Let that installation include its own private environment just for Pip, using the virtual environment mechanism that was just added. Fix the Pip command line to make it as easy as possible to specify a target environment (and have it refuse to install in its own environment, except to self-upgrade). And for bonus points on Windows: have the launcher expose its Python-detection logic, so that Pip in its own environment could deduce the *path for* the environment that `py` would run, and choose that as the destination by default.

Because of the history, however, Pip didn't initially face pressure to shape itself up to work that way. (It goes without saying, I hope, that this is one of the key design mistakes I'm trying to address with [Paper](https://github.com/zahlman/paper).)

## Pip, `runpy`, Pip, Pip, Pip, `importlib`, Pip, `subprocess`, and Pip

As mentioned above, the simple way to make Pip install cross-environment is with the `--python` argument. I proposed it in my previous piece, it's simple, and it normally works.

So this is a good time to point out that it's kind of a hack, and not completely reliable.

It's not just any hack - it's clever ([and surprisingly complex](https://github.com/pypa/pip/blob/main/src/pip/__pip-runner__.py)). When Pip is given the `--python` argument, it basically re-runs itself via `subprocess` standard library functionality - using the destination environment's Python executable, to interpret its own code in the current location. But since its own code isn't in the destination environment, `import`s won't work normally in the new process, so it has to use more tools from the standard library: [runpy](https://github.com/python/cpython/blob/d457345bbc6414db0443819290b04a9a4333313d/Lib/runpy.py#L215)) (the same code [that powers Python's `-m` command-line option](https://docs.python.org/3/library/runpy.html)), and the [advanced import machinery](https://docs.python.org/3/library/importlib.html#importlib.abc.MetaPathFinder) provided by `importlib`, creating a `MetaPathFinder` that is added to [`sys.meta_path`](https://docs.python.org/3/library/sys.html#sys.meta_path). Part of the logic for this is contained in a specially named file, intended to make sure it isn't imported directly, but itself run as a subprocess [after looking up the filename](https://github.com/pypa/pip/blob/2d772146d94e65c948e41e4b19e1fc3bdfa4feae/src/pip/_internal/build_env.py#L43). And the re-run Pip gets the same complete command line, including the `--python` argument, so [an environment variable is used as a recursion guard](https://github.com/pypa/pip/blob/2d772146d94e65c948e41e4b19e1fc3bdfa4feae/src/pip/_internal/cli/main_parser.py#L80).

This complex process doesn't actually create a whole lot of overhead, but it does come with a limitation: the destination environment's Python has to be able to run Pip. That normally isn't an issue, since the Pip support window from Python versions generally moves in lock-step with the support window for Python itself. And normally you won't need to use an older version of Pip (only the current Pip version is ever supported, remember?), so you can just keep it up to date, and use it with whatever Python environments are currently not EOL. However, if you maintain a package for an EOL version of Python - maybe you're one of those unfortunate people still stuck maintaining a 2.7-based system - too bad for you:

```
$ # Since Python 2.7 didn't have a venv standard library module,
$ # we'll use the third-party virtualenv first.
$ virtualenv --no-seed --python py2.7 old-venv
$ pip --python old-venv/bin/python install numpy
This version of pip does not support python 2.7 (requires >=3.8).
```

In fact, current Pip will explicitly guard against using Python 3.7 or lower, without considering whether it would actually work.

So really, the robust way to do it is the pre-Pip-22.3 way:

```
$ pip --prefix old-venv install numpy

Usage:   
  pip <command> [options]

no such option: --prefix
```

Oh, sorry, the `--python` option has to come before `install`, but `--prefix` goes after `install`.

```
$ pip install --prefix old-venv numpy
Collecting numpy
  Using cached numpy-2.2.3-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (62 kB)
```

Oh, sorry again, of course it needs to be told the Python version. After all, the point of virtual environments is that they mimic "real" environments, and a "real" environment (like, say, `/usr`) could have multiple Python versions in it.

```
$ pip install --prefix old-venv --python-version 2.7 numpy
ERROR: When restricting platform and interpreter constraints using --python-version, --platform, --abi, or --implementation, either --no-deps must be set, or --only-binary=:all: must be set and --no-binary must not be set (or must be set to :none:).
```

Whoops! Well, Numpy has pretty good wheel support, so let's demand a wheel:

```
$ pip install --prefix old-venv --python-version 2.7 --only-binary=:all: numpy
ERROR: Can not use any platform or abi specific options unless installing via '--target' or using '--dry-run'
```

My mistake, again. Although I really can't explain this limitation [and would consider it a bug](https://github.com/pypa/pip/issues/11890). Anyway, instead of giving it the location of the virtual environment, let's just directly specify the subdirectory where the files should go. Since there's a separate `site-packages` subdirectory per Python version on Linux, maybe it can even use that information!

```
$ pip install --target old-venv/lib/python2.7/site-packages/ --only-binary=:all: numpy
Collecting numpy
  Using cached numpy-2.2.3-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (62 kB)
Downloading numpy-2.2.3-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (16.1 MB)
```

Hmm, I guess not.

```
$ pip install --target old-venv/lib/python2.7/site-packages/ --python-version 2.7 --only-binary=:all: numpy
Collecting numpy
  Downloading numpy-1.16.6-cp27-cp27mu-manylinux1_x86_64.whl.metadata (2.1 kB)
Downloading numpy-1.16.6-cp27-cp27mu-manylinux1_x86_64.whl (17.0 MB)
```

Phew. Except it's still wrong, because Numpy's `f2py` etc. scripts are now in the wrong place (a `bin` subdirectory` of the `site-packages`, rather than the virtual environment's main `bin` directory).

At least now we know why `--python` was added.

## Pip, Pip, Pip, Pip, Pip, Pip, Baked `.pyc`s, Pip, Pip, Pip and Pip

## Pandas Thermidor aux Matplotlib with a Numpy Dependency, Garnished with Truffle PIL, Brandy and a Vendored Requests on top, and Pip

## Bloody `venv`s!

Thanks for reading this far. I hope I've improved your view of Python virtual environments, and sharpened your critique of Pip.

As I said in the teaser, there's more that people don't seem to like about venvs, but that will wait for another day. For now, just know that you *can* create them quickly, and use them effectively. And when you use a workflow tool like `uv`, Poetry, Hatch or PDM, it actually creates and manages virtual environments for you - you aren't really avoiding them, just adding a layer of abstraction. For all the supposed benefits of being written in Rust, `uv` doesn't save you time on this, either:

```
$ time uv venv --no-progress --no-config --offline --quiet --no-project with-uv

real	0m0.105s
user	0m0.049s
sys	0m0.016s
```

That's about twice as long as the built-in `venv`. As far as I can tell, Astral has basically ported the logic of the third-party `virtualenv` (which the standard library `venv` is based upon) in Rust. This adds more activation scripts for additional environments, as well as a shim used for distutils support - even after the [removal of distutils from the standard library]().

At any rate, it's faster than `virtualenv`:

```
$ time virtualenv --no-seed --no-download --quiet with-virtualenv

real	0m0.180s
user	0m0.155s
sys	0m0.026s
```

...but it's not faster than `venv` using `--without-pip`, as seen earlier. Without installing Pip, the overall logic is pretty simple - you really just need to copy a template into place. There's no real reason to expect massive gains from Rust (or any statically compiled language) there.
