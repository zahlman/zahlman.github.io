# Python packaging: Why we can't have nice things @python-packaging
# Part 4: Multipiplation #python #pip #bloat #virtual-environments

Over the years I've seen a lot of grumbling about Python's [virtual environments](https://peps.python.org/pep-0405/), and resistance to using them - directly, at least. I have another piece planned about the general topic, and about how most of the issues people seem to complain about with virtual environments are really Pip's fault.

Today, I want to focus on one specific issue: the perception that creating a virtual environment is slow and wastes disk space.

Spoiler: it's Pip's fault - but also partly Windows' fault, *even if you don't use Windows*.

<!-- TEASER_END -->

## Meta

{{% hitcounter %}}

## Lovely Pip! Wonderful Pip!

Now, I'm writing this from hardware that's over 10 years old (although I did replace the SSD and power supply along the way), so you might see better numbers. But when I create a virtual environment in Python 3.12:

```
$ time python -m venv test-venv

real	0m3.292s
user	0m3.020s
sys	0m0.219s
```

That's already not great, but there's a further problem:

```
$ ./test-venv/bin/pip list
Package Version
------- -------
pip     24.0
```

The virtual environment is created with a fresh copy of Pip, allowing standard idioms like `python -m pip` to just work, cross-platform<sup>\*</sup> and regardless of whether you're using a virtual environment or the base Python environment. However, this copy comes from a "bootstrap" wheel vendored with the Python standard library. In short, it's frozen in time along with the Python distribution. The Pip development team, meanwhile, only ever supports the most recent release, and Pip itself likes to nag you with messages that a new version is available (unless you `--disable-pip-version-check`). So, in practice, you'll need to upgrade as well:

```
$ time (python -m venv test-venv && ./test-venv/bin/pip install pip --upgrade)
Requirement already satisfied: pip in ./test-venv/lib/python3.12/site-packages (24.0)
Collecting pip
  Using cached pip-25.0.1-py3-none-any.whl.metadata (3.7 kB)
Using cached pip-25.0.1-py3-none-any.whl (1.8 MB)
Installing collected packages: pip
  Attempting uninstall: pip
    Found existing installation: pip 24.0
    Uninstalling pip-24.0:
      Successfully uninstalled pip-24.0
Successfully installed pip-25.0.1

real	0m4.829s
user	0m4.438s
sys	0m0.344s
```

Notably, this requires an Internet connection *even if* Pip's cache already contains the new version wheel - because it will contact PyPI to check if there's anything even newer.

And, of course, it takes up quite a bit of space for this, too:

```
$ du -sh test-venv/
13M	test-venv/
$ du -sB1 test-venv/ # More precisely:
13520896	test-venv/
```

Which, to be clear, is almost entirely due to the Pip installation:

```
$ ls test-venv/lib/python3.12/site-packages
pip  pip-25.0.1.dist-info
$ du -sB1 test-venv/lib/python3.12/site-packages
13455360	test-venv/lib/python3.12/site-packages
```

This is primarily what I mean about it being Pip's fault.

## Don't worry, dear, I'll have your Pip

Okay, so there seems to be a pretty clear bottleneck here. What if we could just make a virtual environment that just... hasn't got any Pip in it?

As it turns out - [as I discussed in a previous post](https://zahlman.github.io/posts/2025/01/07/python-packaging-2/) - we absolutely can set up a system that only has a little bit of Pip. Of course we want to be able to install packages into the new virtual environment, but we aren't forced to give it a separate copy of Pip. The `venv` standard library module lets us simply create the venv `--without-pip`, and it's dramatically faster:

```
$ time python -m venv --without-pip without-pip

real	0m0.053s
user	0m0.041s
sys	0m0.012s
```

And smaller:

```
$ du -sh without-pip/
56K	without-pip/
```

(And only about a quarter of that space is file contents; it needs to make a handful of folders.)

And from there, of course, we can use any modern external copy of Pip (22.3 or newer) to install into that new environment, using something like `pip --python without-pip/bin/python`.

Oh, by the way: *you've always been able to do this*, for as long as there have been virtual environments. When [venv](https://docs.python.org/3/library/venv.html) was added to the standard library in Python 3.3, it actually didn't bootstrap Pip; in 3.4, along with adding that functionality (as well as the [ensurepip](https://docs.python.org/3/library/ensurepip.html) standard library module), the `--without-pip` flag was added so that you could still have a "bare" environment.

So of course that raises two questions: Why don't people seem to know about this? And why isn't it the default?

In short, because everyone has been taught to do it that way, because it's supposedly easier to explain - given how Pip works.

Windows plays a significant role here. See, the normal way of organizing installed applications on Windows isn't very friendly for command-line use. Typically, each program gets a sub-folder within `C:\Program Files` (or whatever other drive letter you chose) - so if you want to use them from the command line, you'd have to add each of those entries to the `PATH` environment variable. That would pollute a [length-limited](https://stackoverflow.com/questions/34491244) environment variable, and also cause confusion between `.exe`s with matching names (not just Python, but the `pip.exe` wrappers).

This leads to all sorts of ways to set up a system where either `python` doesn't run Python, `pip` doesn't run Pip, or - most importantly - [`pip` installs for a different version of Python than `python` runs](https://stackoverflow.com/questions/14295680). (And the advice you can find about the problem most easily - such as the previous link - tends to be very confused.)

As a result, the common practice on Windows is to have the installer *not* add entries to `PATH`, and to use a single common [launcher program](https://docs.python.org/3/using/windows.html#python-launcher-for-windows) - installed directly into the Windows folder, so it's always on `PATH` - to choose a Python version. However, with this approach, `pip.exe` won't be on the user's `PATH` - not any of the copies. Instead, `py -m pip` is the recommended way to run Pip on Windows. (This also solves the problem that Windows won't allow `pip.exe` to replace itself on disk while running.) This way, the launcher finds an appropriate Python environment (and in 3.5, it was [improved](https://peps.python.org/pep-0486/) to support virtual environments as well!), and then that Python runs the `pip` module from its `site-packages`. And now there's a simple approach that can be taught to everyone - well, notwithstanding that Windows users have to write `py` while Linux users are expected to write `python`. (More recently, one of the core Python developers [got the idea](https://github.com/brettcannon/python-launcher) that Linux systems would also benefit from a Python launcher. But the idea doesn't seem to have gotten much traction - there's no PEP for it or anything.)

## Windows, Egg, Pip and Python

(Don't worry, I'm not bringing up the legacy "egg" packaging format here - just continuing with the [reference](https://en.wikipedia.org/wiki/Spam_%28Monty_Python_sketch%29).)

Speaking of Windows, a brief interlude.

As part of my research for this piece, I booted into the copy of Windows 10 I had lying around on another SSD, for the first time in probably years. I didn't dare connect to the Internet, but I could still test how `venv` under Python 3.8 coped with installing an older Pip version (20.1.1, I think).

To keep a long story short: Pip of that era was comparable in size. A Windows venv, at least in that test, took about an additional 1MB of disk space beyond what Pip requires - mainly because of a surprisingly large wrapper executable used to delegate to the system Pip, which also has to be duplicated for terminal vs. GUI uses of Python. (On Linux, the same `python` executable works either way, and the venv just uses a symlink by default. Asking `venv` on Windows for `--symlinks` failed for me and I didn't feel like investigating it, beyond noting that the error messages vaguely implied that it was trying to create symlinks *in the wrong direction*.) And it takes about three times as long to create the venv, whether or not Pip is included. Taking about 150 milliseconds instead of 50 [isn't a big deal](https://lawsofux.com/doherty-threshold/), but taking about 9 seconds instead of 3 certainly is.

(Overall, I was amazed how sluggish *everything* felt - since I didn't really have a memory of everything suddenly feeling more performant when I switched to Linux in the first place. I knew that my "baseline" RAM usage - i.e. with a single user logged in graphically, not running any programs - was higher on Windows, but I hadn't realized it was on the order of 70% higher. I guess the built-in "Windows Defender" has a lot to do with this - and perhaps also the venv creation time, considering all the I/O it does. I don't really want to get into this in any detail, but I do wish I'd done the experiment [before my Linux anniversary](https://zahlman.github.io/posts/2025/01/24/leaning-in-to-my-ux/).)

So, one could say that the slow performance on Windows is mostly Windows' fault, since the majority of the time taken there is time not taken on Linux. But I suspect this is really a multiplier that applies to pretty much everything, and anyway, neither Pip nor Python devs can really do anything about it. So I don't mind keeping my attention focused on Pip here. More to the point: the results vary slightly according to Python and Pip versions, but not enough to matter to the discussion. It's not a *temporary* problem in Pip; if anything, the long-term trend has been for the problem to get worse, as Pip builds in more backwards-compatibility layers. (The most recent versions of Pip are not the biggest, though; they've recently completed some migrations from one dependency to another, and no longer have to vendor both.)

## Pip, Setuptools, `easy_install`, Python and Pip

## Pip, Pip, Baked `.pyc`s and Pip

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
