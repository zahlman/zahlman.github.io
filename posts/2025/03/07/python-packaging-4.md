# Python packaging: Why we can't have nice things @python-packaging
# Part 4: Multipiplation #python #pip #bloat #virtual-environments

Over the years I've seen a lot of grumbling about Python's virtual environments, and resistance to using them - directly, at least. I have another piece planned about the general topic, and about how most of the issues people seem to complain about with virtual environments are really Pip's fault.

Today, I want to focus on one specific issue: the perception that creating a virtual environment is slow and wastes disk space.

Spoiler: it's almost entirely Pip's fault (except on Windows, where it's partly Windows' fault).

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

## Windows, Egg, Pip and Python

(Don't worry, I'm not bringing up the legacy "egg" packaging format here - just continuing with the [reference](https://en.wikipedia.org/wiki/Spam_%28Monty_Python_sketch%29).)

As part of my research for this piece, I booted into the copy of Windows 10 I had lying around on another SSD, for the first time in probably years. I didn't dare connect to the Internet, but I could still test how `venv` under Python 3.8 coped with installing an older Pip version (20.1.1, I think).

To keep a long story short: Pip of that era was comparable in size. A Windows venv, at least in that test, took about an additional 1MB of disk space beyond what Pip requires - mainly because of a surprisingly large wrapper executable used to delegate to the system Pip, which also has to be duplicated for terminal vs. GUI uses of Python. (On Linux, the same `python` executable works either way, and the venv just uses a symlink by default. Asking `venv` on Windows for `--symlinks` failed for me and I didn't feel like investigating it, beyond noting that the error messages vaguely implied that it was trying to create symlinks *in the wrong direction*.) And it takes about three times as long to create the venv, whether or not Pip is included. Taking about 150 milliseconds instead of 50 [isn't a big deal](https://lawsofux.com/doherty-threshold/), but taking about 9 seconds instead of 3 certainly is.

(Overall, I was amazed how sluggish *everything* felt - since I didn't really have a memory of everything suddenly feeling more performant when I switched to Linux in the first place. I knew that my "baseline" RAM usage - i.e. with a single user logged in graphically, not running any programs - was higher on Windows, but I hadn't realized it was on the order of 70% higher. I guess the built-in "Windows Defender" has a lot to do with this - and perhaps also the venv creation time, considering all the I/O it does. I don't really want to get into this in any detail, but I do wish I'd done the experiment [before my Linux anniversary]().)

So, one could say that the slow performance on Windows is mostly Windows' fault, since the majority of the time taken there is time not taken on Linux. But I suspect this is really a multiplier that applies to pretty much everything, and anyway, neither Pip nor Python devs can really do anything about it. So I don't mind keeping my attention focused on Pip here. More to the point: the results vary slightly according to Python and Pip versions, but not enough to matter to the discussion. It's not a *temporary* problem in Pip; if anything, the long-term trend has been for the problem to get worse, as Pip builds in more backwards-compatibility layers. (The most recent versions of Pip are not the biggest, though; they've recently completed some migrations from one dependency to another, and no longer have to vendor both.)

## Pip, Setuptools, `easy_install`, Python and Pip

## Pip, Pip, Baked `.pyc`s and Pip

## Pandas Thermidor aux Matplotlib with a Numpy Dependency, Garnished with Truffle PIL, Brandy and a Vendored Requests on top, and Pip

## Bloody `venv`s!
