# Python packaging: Why we can't have nice things @python-packaging
# Part 3: Premature Compilation #python #pip #security #setuptools

Pip 25.0 [has been out](https://discuss.python.org/t/_/78392) for [a bit over a week now](https://github.com/pypa/pip/releases/tag/25.0); and we now also have an [official blog post](https://ichard26.github.io/blog/2025/01/whats-new-in-pip-25.0/) about the release.

As I very much expected (I suppose I could have verified this against a pre-release version...), it has a very serious bug. I believe that warnings are more important than baiting people to read the post, so here's the PSA up front:

1. **Never use Pip to download, test, "dry-run" etc. an untrusted source distribution (sdist).** [It will try to build the package](https://github.com/pypa/pip/issues/1884), **potentially running arbitrary code** (as building an sdist always entails). Instead, use the [PyPI website](https://pypi.org) directly, or the [API](https://docs.pypi.org/api/json/) it provides.

2. **Never use `sudo` to run Pip** (nor run it with administrative privileges on Windows). Aside from the potential problems caused by conflicting with the system package manager, Pip [**will not drop privileges**](https://github.com/pypa/pip/issues/11034) when it runs as root and attempts to build an sdist - which again, **potentially runs arbitrary code**.

3. If you expect wheels to be available for the packages you want to install with Pip, **strongly consider adding `--only-binary=:all:` to the Pip command** to ensure that only wheels are used. If you really need to use sdists, it's wise to inspect them first, which by definition isn't possible with a fully automated installation.

4. If you release Python packages, [please try to provide wheels for them](https://pradyunsg.me/blog/2022/12/31/wheels-are-faster-pure-python/), even if - no, *especially* if your package includes only Python code and doesn't require explicitly "compiling" anything. An sdist is *much* slower to install than a wheel even in trivial cases; and making a wheel available allows your users to demand wheels from Pip, raising the overall baseline for trust and safety in the Python ecosystem.

There are two things I should clarify up front. First: it's normal and expected that building an sdist involves running arbitrary code - because "building" them can mean arbitrary things. C isn't the only language used to extend Python (not by a long shot), and plenty of projects are dependent on specific compilers, custom settings, additional prep work done before and/or after building, etc. However, running arbitrary code *when you aren't expecting it and prepared for it* is obviously a much bigger problem.

Second: this problem *isn't* some new discovery, nor is it specific to the new release - I'm just taking that opportunity to bring up the topic. This is the Nth iteration of a problem that has plagued Pip *for almost its entire history*.

With that out of the way, let me get into the detailed examination.

<!-- END_TEASER -->

## Meta

{{% hitcounter %}}

## Description and Demonstration

Let's say you want to install a package from PyPI that you aren't sure about. (For the purpose of this hypothetical, we'll use the [`issue7325`](https://pypi.org/project/issue7325) package that was created specifically for one of the many bug reports made about the general problem.)

Sure, the PyPI team strives to keep malware off the system, and there are plenty of eyes on big-name projects all the time; but nothing is guaranteed in this life.

You might suppose that you could just inspect the Python code before you ever try running (or `import`ing) it, but that's only safe for a pure-Python wheel. If the project depends on a compiled C library, for example, then you won't be able to inspect it in a wheel (even if the wheel includes `.c` source code files, you can't verify that the compiled code actually corresponds to it). And if you install from an sdist, of course, Pip will try to build the package for you automatically, and you've heard (correctly) that this can run arbitrary code.

Since you don't want to allow unaudited, arbitrary code execution (to "get pwnt", as the kids probably still say), you hatch the plan of *downloading* the sdist first, so that you can manually unpack it first (it's just an ordinary `.tar.gz` file, after all), inspect it, and only then try the installation (knowing that you can specify the `.tar.gz` filename instead of a PyPI package name when you `pip install`).

You've just learned that Pip has a `download` command, so you try:

    :::bash
    $ pip download issue7325

... and *promptly get pwnt anyway*. The next thing you know, you're getting a message (because this is white-hat hacking; no actual harm was done - this time) every time you start Python in that environment:

    WARNING: use of "pip download --no-deps" allowed arbitrary code execution
             see https://github.com/pypa/pip/issues/7325

There's also a `--dry-run` option for `pip install` which has the same problem. The only thing "dry" about a Pip dry-run install is the actual copying of files into the Python environment. It will still attempt to build a wheel by the normal process.

That's strange. Why did Pip build the package, when it was explicitly asked only to download it? *Well, that's the bug*. Apologies to the impatient, but there's quite a bit more I need to say before the big reveal.

Of course, you can avoid this risk by demanding wheels:

    :::bash
    $ pip download --only-binary=:all: issue7325

... which would fail in this case, because a wheel was deliberately not provided for demonstration purposes. Again: if you release Python code, please provide wheels if you can. If your code is pure Python, you have no excuse. If you use [PyPA's standard build front-end]() (which I highly recommend), it will already make the wheel by default - all you have to do is include it when you upload to PyPI. If you don't have a dedicated build front-end, well first off you [shouldn't be running setup.py directly]() (and if you don't use Setuptools for building then you almost certainly do have a build front-end), but [`pip wheel`] works in a pinch.

And, of course, there are other reasons why you might want to download an sdist. Maybe you know that there's some C code that needs a special patch for your system, or you want to edit some compiler options because you think you can optimize something. Or maybe you really need that package and the wheel just isn't available for your system. Or maybe the *latest version* isn't available as a wheel for your system yet, and you need that.

Whatever your situation, the safe way to get an sdist is from the PyPI website. [Look up the package you want, click on "Download files", and select the file you want](https://pypi.org/project/issue7325/#files). You can get wheels this way, too. If you really need to use the command line, [a JSON API is available](https://docs.pypi.org/api/):

    $ curl -s https://pypi.org/pypi/issue7325/0.1/json | jq '.urls[0].url'
    "https://files.pythonhosted.org/packages/c0/51/bd28cda650e3f0123ea82936f96b3fd28da90ec8b2af89a9029e25768647/issue7325-0.1.tar.gz"

(Here, `"0.1"` is the version; the `urls` array in the JSON data includes any sdists or wheels for that release in arbitrary order. Automation is left as an exercise.)

## It Can Happen to You

I first noticed this issue as a result of a friend showing me a blog post from 2022 titled [Someone’s Been Messing With My Subnormals!](https://moyix.blogspot.com/2022/09/someones-been-messing-with-my-subnormals.html). Ostensibly, it's not about Pip at all. It's rather about what can happen to floating-point math in your Python program when C extensions are compiled a certain way and then included in the project, however indirectly. Specifically: there's a compiler option `--ffast-math` supported by both GCC and clang, which indirectly causes the compiled code to mess with global process state, which changes the behaviour of ["subnormal"](https://en.wikipedia.org/wiki/Subnormal_number) floating-point values. I think I have a reasonably good understanding of the technical details involved in this -- but they don't normally concern me, so I don't spend a lot of time thinking about them.

So why am I bringing this up, you ask? Well, it turns out that this story has a buried lede. Because the floating-point math problem involves *global* process state, you can trigger it simply by having specific dependencies - even transitively - in your project. In order to verify how widespread the problem is, and figure out which packages most commonly cause downstream problems, the author determined that it would be necessary to examine *every* package on PyPI. And because of how poorly the ecosystem handles package metadata (more on that another time), the natural way to do a properly *thorough* job of that would be to *download* every package, and then try to scrape metadata out of them (which might be represented a few different ways - depending on whether a wheel is available, and whether the package includes `pyproject.toml` and/or `PKG-INFO` per modern standards).

And, well, that's where all hell broke loose:

> I actually started down this path and set about running `pip install --dry-run --ignore-installed --report` on all 397,267 packages. This turned out to be a *terrible* idea. Unbeknownst to me, **even with \-\-dry-run pip will execute arbitrary code found in the package's setup.py**. In fact, **merely asking pip to** *download* **a package can execute arbitrary code** (see pip issues 7325 and 1884 for more details)! So when I tried to dry-run install almost 400K Python packages, [hilarity ensued](https://twitter.com/moyix/status/1566561433898426368). I spent a long time [cleaning up the mess](https://twitter.com/moyix/status/1566578412663209984), and discovered some [pretty poor setup.py practices](https://twitter.com/moyix/status/1566609622680608770) along the way. But hey, at least I got [two free pictures of anime catgirls](https://twitter.com/moyix/status/1566612152558944257), deposited directly into my home directory. Convenient!
>
> Once I had managed to clean up the mess (or hopefully, anyway—I never did find out what package tried to execute sudo), I decided I needed a different approach.

(Editor's note: I've removed the links to the Pip issues because they'll come up again later in this post. And yes, that last link *does* include the pictures in question.)

So, to reiterate from the introduction: the arbitrary setup code included with an sdist can be run *even for innocuous sounding "download" commands*.

And, again: I don't fault Python for relying on arbitrary code at install time in general. The *requirements* to set up a Python project are pretty well arbitrarily complex, and nobody has really put forward a system that reliably handles even the common cases in any secure manner - at least, aside from pure Python projects where there's nothing to build. The same problem is also seen in other packaging systems for other languages, like NPM. ([Here's just one of many](https://medium.com/@v_pragma/12-strange-things-that-can-happen-after-installing-an-npm-package-45de7fbf39f0) articles on that topic I found with a [quick search](https://duckduckgo.com/?q=npm+arbitrary+code+on+installation).) And, of course, if you're going to *use* an installed library, it can run arbitrary code at `import` time, or when you call any of its functions. That's just how it is with third-party code: ultimately, trust has to come from somewhere.

But the *entire point* of having a command like `pip download` is so that Pip's resolver can figure out which package is appropriate for your system and then *just download it for you*, which you'd typically do *specifically so that you can inspect it* before doing anything with it. (After all, you can't just rely on reading the code on GitHub etc. in general - there's no guarantee that code actually matches what you downloaded. [There's a new system to make that possible](https://docs.pypi.org/trusted-publishers/), but publishers have to opt in to it.) Or maybe you want to store it somewhere, perhaps as part of [setting up your own index](https://stackoverflow.com/questions/18052217). But regardless, you *aren't* trying to install it *yet*.

The above quote uses the only red text in the entire article, and is also, as far as I know, the main reason it got as much attention as it did. True, not all of those packages were actually downloaded; and of course a lot of them would have been available as wheels. So no, our author did not exactly run 397,267 pieces of untrusted code unintentionally.

But still, I can't pass on the opportunity to make the reference:

<iframe style="width:50%;aspect-ratio:16/9;margin:0 auto;display:block" src="https://www.youtube.com/embed/Az49aNuYeJs" title="YouTube video player" frameborder="0" allow="fullscreen" referrerpolicy="strict-origin-when-cross-origin"></iframe>
<!-- It looks like I have to do the whole thing with raw HTML... -->
<div style="text-align:center"><em>That is not a small number!</em></div><br />

Now here's the big reveal. The author of that post, [Brendan Dolan-Gavitt](https://x.com/moyix) (@moyix) is not just some random C expert who read the Pip documentation (but not thoroughly enough). No, Brendan Dolan-Gavitt is a **security researcher** with an impressive publication history [going back to at least 2006](https://moyix.blogspot.com/2006/12/malware-with-twist.html).

Yeah.

Again: **do not use Pip to download sdists for examination. Instead, go to the [actual PyPI website](https://www.pypi.org), find the page for the package you want, optionally choose a version from the "Release history" (manually determining what version you want), and choose the "Download files" option; or use the JSON API.**

I don't know of any official, ready-made, secure automation for using the JSON API for this task. If you decide to implement a solution, please share and promote it.

Using the website interface is also, arguably, the best way to protect yourself against typo-squatters and other malware packages - on top of the PyPI maintenance team's own attempts to remove those projects.

## Let's Make Things Silly

While I'm thankful to [Wim Jeantine-Glenn](https://pypi.org/user/wim.glenn/) for creating an example (for Pip issue 7325) that demonstrates the problem in a reasonably realistic (but minimal) way, in my opinion it really doesn't show off how absurd the overall problem is.

With that in mind, I prepared the following Bash script you can use to reproduce the problem on Linux - quickly (less than a second on my 10-year-old machine), directly and *without an Internet connection*. All you need is for `pip` to refer to a working copy of Pip. It's also written to highlight many things that might otherwise not be obvious about the nature of the problem.

```
#!/bin/bash
# Copyright (c) 2025 Karl Knechtel.
# Permission is granted to reproduce this code locally for testing purposes,
# but please don't republish or redistribute it - instead, please direct
# interested readers to this blog post at
# https://zahlman.github.io/posts/2025/02/13/python-packaging-3/ .
mkdir demo-0.1.0 # [1]
cat << done_toml > demo-0.1.0/pyproject.toml # [2]
[project]
name = "demo"
version = "0.1.0"
dependencies = []
[build-system]
requires = [ ]
build-backend = "build"
backend-path = "."
done_toml
cat << done_info > demo-0.1.0/PKG-INFO # [3]
Metadata-Version: 2.4
Name: demo
Version: 0.1.0
done_info
cat << done_setup > demo-0.1.0/build.py # [4]
__import__('sys').exit("Arbitrary code could have been executed here.")
done_setup
tar czf demo-0.1.0.tar.gz demo-0.1.0/ # [5]
pip download --no-deps --no-build-isolation ./demo-0.1.0.tar.gz # [6]
rm -r demo-0.1.0/ demo-0.1.0.tar.gz
```

Footnotes from the code:

1. The general approach is to create a [valid sdist - fully compliant with all up-to-date standards](https://packaging.python.org/en/latest/specifications/source-distribution-format/) - locally, and then ask Pip to "download" the file. Yes, this is a perfectly valid (if pointless) use of `pip download`, as the output will make clear. It's actually pretty easy to create such an sdist - it's just a zipped (or should I say [Zzzzzzzzzzzzzzzipped](https://en.wikipedia.org/wiki/Election_Night_Special)?) tar archive, containing "source" metadata in the form of `pyproject.toml` and "built" metadata in the form of `PKG-INFO`. Note in particular that the folder name includes the name and version for the project - that's part of the expected structure for the sdist.

1. Here we create a `pyproject.toml` file [following the appropriate standards](https://packaging.python.org/en/latest/specifications/pyproject-toml/#pyproject-toml-spec). We have a `[project]` table (originally defined by [PEP 621](https://peps.python.org/pep-0621/)) defining name, version and dependency information. Only the name and version are mandatory - and the version could be marked as "dynamic" instead - but that doesn't make sense for our use case. The dependencies would default to an empty list, but it's more amusing IMO to be explicit about this. We also have a `[build-system]` table (originally defined by [PEP 518](https://peps.python.org/pep-0518/)) explaining what tools to use to create a wheel from the sdist. (Normally, the same tool would be used to create the sdist from a source tree - but in this example, the "build system" we specify is a fake.)

1. Here we create the corresponding ["core metadata"](https://packaging.python.org/en/latest/specifications/core-metadata/#core-metadata) `PKG-INFO` file. Normally this would end up copied verbatim into any corresponding wheel (named `METADATA` inside wheels), unless the project uses dynamic metadata. In order to conform to modern standards, we need to implement at least version 2.2 of the metadata spec - but it turns out that we can trivially implement version 2.4, the most recent. Updates to the spec generally *allow* us to add information, but don't *require* it - for example, version 2.4 allows for [using license files](https://peps.python.org/pep-0639/) in an up-to-date way - but our example project, being ephemeral, doesn't have its own license. As with `pyproject.toml`, only the name and version (and the metadata version) need to be specified.

1. Here we define a fake "build system" for the sdist, which just immediately errors out. The name `build.py` corresponds to what was defined in `pyproject.toml`. The main thing I want to highlight here is that **Setuptools has nothing to do with the problem**. For projects that use Setuptools (the default if you don't include a `[build-system]` table), Pip would tell Setuptools to build the project, and Setuptools would (among other things) potentially run a top-level `setup.py` script in order to do so. But this is purely an implementation detail. Setuptools is, in these cases, only doing what it's told. It's entirely Pip's fault that Pip tells Setuptools to do this.

1. Finally we can create the sdist. Notice in particular that the only actual Python code included is the "build system". As described [in part 1](https://zahlman.github.io/posts/2024/12/24/python-packaging-1/), it's perfectly valid for the sdist - as well as any resulting wheel - to define no installable code packages at all. The name `demo` applies to the *distribution* - not to anything that will be `import`ed by users. Anyway, we name the file with the distribution name and version, according to rules [defined in PEP 625](https://peps.python.org/pep-0625/) - there's no wiggle room here.

1. Now that we have an sdist, we can tell Pip to "download" it, and then we'll clean up by deleting the sdist archive and the corresponding folder. Pip won't actually modify any `site-packages` contents, but it will try to build the sdist into a wheel. Note in particular the `--no-deps` and `--no-build-isolation` flags here, for later.

When you try this, you should get a result like:

```
Processing ./demo-0.1.0.tar.gz
  File was already downloaded /<absolute path omitted>/demo-0.1.0.tar.gz
  Preparing metadata (pyproject.toml) ... error
  error: subprocess-exited-with-error
  
  × Preparing metadata (pyproject.toml) did not run successfully.
  │ exit code: 1
  ╰─> [1 lines of output]
      Arbitrary code could have been executed here.
      [end of output]
  
  note: This error originates from a subprocess, and is likely not a problem with pip.
error: metadata-generation-failed

× Encountered error while generating package metadata.
╰─> See above for output.

note: This is an issue with the package mentioned above, not pip.
hint: See above for details.
```

The `Arbitrary code could have been executed here.` message, of course, comes from `build.py` - it's not a warning from Pip.

Perhaps the funniest part here is that there are two disclaimers of responsiblity from Pip. These are standard messages, and normally make sense - when Pip tells the build system to build a wheel, it can't do anything about bugs in the build system itself, nor about errors in the project's build configuration. But, of course, it *is* a problem with Pip in this case *that a build is attempted at all*.

It does this even though the file is *already right there in the current directory*, and Pip *knows* that it's right there (`File was already downloaded`) and simply uses the existing file directly.

It does this even though we explicitly told it that we only want to "download" the code, not to build nor install it.

It does this even though we explicitly told it that we don't want to obtain any project dependencies (`--no-deps`). (The `--no-build-isolation` flag is more just for entertainment. It's perfectly valid to include this flag for `pip download` and that it does something meaningful - although not *relevant* to the demo. Normally, when Pip starts a build process, it would create a temporary venv for it, and install *the build system's* dependencies there - along with the build system itself, if not included. Since we include our fake "build system" and it has no dependencies of its own, we save some time by asking Pip to just build in the current environment. This build system isolation, by the way, often results in needing an Internet connection to build projects even though you already have everything necessary installed - a topic for another day.)

It does this with every version of Pip that's compatible with currently supported versions of Python, and would do it with much older versions as well - going back for almost the entire history of Pip, adjusting for UI tweaks and changes to standards made along the way.

It does this even though we follow every modern packaging standard to the letter. Including some updates that were *specifically* intended to facilitate Pip in avoiding unnecessary builds of this sort.

## The Big Reveal

Dear reader, can you guess *why*, exactly, Pip is starting this build process, and running arbitrary code without oversight? I've made some vague allusions to it already, but you might still never guess.

It's so that Pip can **make sure that the name and version metadata that you'd get from building the project, match what you requested**.

Which leads us to additional highlights:

1. This still happens with the latest version of Pip. (I also demonstrate this with the latest Setuptools version - not that it should be Setuptools' responsibility to detect or do anything about this state of affairs; it's just trying to build a wheel, like Pip explicitly asked it to.)

1. This still happens even though we explicitly say not to obtain any dependencies. I traced through the code, and it preserves the information (through a *very* deep call stack) that dependency information isn't needed. (Although the process it's trying to use to obtain the name and version, would trivially tell it the dependencies as well.)

1. Yes, the command says "download" and does *not* say anything like "verify" anywhere. This argument has historically not been very persuasive.

1. This verification is absurd when downloading from PyPI, because Pip has already asked PyPI for a specific version of a project with a specific name. With the local file, it's absurd because the user didn't ask for such verification and has already very deliberately specified the file. The time for such verification, if ever, is when the file is made available -- not when it's received.

1. This still happens in projects following up-to-date standards: using `pyproject.toml` and following PEP 621 to describe project metadata.

1. Yes, the correct name and version can already be seen in the filename. Pip doesn't care, because it doesn't think this information is reliable. [PEP 625](https://peps.python.org/pep-0625/) is supposed to make it reliable:

    > The filename contains the distribution name and version, to aid tools identifying a distribution without needing to download, unarchive the file, and perform costly metadata generation for introspection, if all the information they need is available in the filename.
    >
    > ...
    >
    > Currently, tools that consume sdists should, if they are to be fully correct, treat the name and version parsed from the filename as provisional, and verify them by downloading the file and generating the actual metadata (or reading it, if the sdist conforms to [PEP 643](https://peps.python.org/pep-0643/). Tools supporting this specification can treat the name and version from the filename as definitive. In theory, this could risk mistakes if a legacy filename is assumed to conform to this PEP, but in practice the chance of this appears to be vanishingly small.

    However, Pip still doesn't appear to support the specification, despite the fact that the PEP was written by a Pip developer, explicitly so that Pip could avoid this headache (among others).

1. Yes, the correct name and version can already be seen in `pyproject.toml`. But it's the official stance of the Pip development team that "tools should not read metadata from `pyproject.toml`" - since build backends aren't yet required to implement [PEP 621](https://peps.python.org/pep-0621/) (notably, Poetry [didn't until just last month](https://github.com/python-poetry/roadmap/issues/3)), there's no guarantee that the `PKG-INFO` corresponds to `pyproject.toml` . Also, Pip still supports legacy `setup.py`-based builds, therefore sdists aren't required to contain a `pyproject.toml` at all.

1. Yes, the correct name and version can already be seen in `PKG-INFO`. This is, in a sense, the "built" version of `pyproject.toml` containing metadata that tools *are* supposed to read. But this, too, isn't required to be present. And as of version 25.0, Pip apparently doesn't even *check*.

1. The `PKG-INFO` provided declares version 2.4 of the specification - the latest at time of writing. From version 2.2 onward, it is *required* that the name and version are specified here, and that building the sdist would produce a wheel with metadata (in the `WHEEL` file) with a matching name and version. In fact, the *specific purpose* of the 2.2 update to the specification was to ensure that this part of the metadata would be reliable. But Pip will *still* try to build the wheel, so that it can error out if the resulting wheel doesn't match. (Yes, "error out" *even though it already downloaded* the file it was asked to download.)

1. Historically, a common justification for building the project (going back before wheels existed) was in order to figure out its dependencies, which could then be automatically downloaded. However, Pip later added a `--no-deps` flag for downloading, which is used here, for the cases where you specifically want only the main package. This has no effect here: Pip will *still* try to build the wheel.

## Timeline

As far as I can tell, The Bug has been present in Pip in one form or another **for almost the entire history** of Pip. Here's a timeline of events I've identified relevant to The Bug:

### February 2012

[Pip v1.1 is released](https://pip.pypa.io/en/stable/news/#v1-1). From the changelog: "`--download` now downloads dependencies as well. Thanks Qiangning Hong. (#315)" (The `--download` flag for `pip install` was available since at least 0.6, but the earliest versions are not dated in the changelog, and there's no clear indication of exactly when the feature was added. PyPI doesn't have the original 0.1.x releases, but [the 0.2 release](https://pypi.org/project/pip/0.2/) -- the first to bear the name "pip" -- is from October 2008.)

### June 2014

Issue 1884, "[Avoid generating metadata in `pip download --no-deps ...`](https://github.com/pypa/pip/issues/1884) (as it's currently titled) is opened on the Pip bug tracker. This appears to be the first report of The Bug. The first reply offers a choice quote:

> It's an unfortunate fact of the Python packaging ecosystem that anything related to packaging always involves arbitrary code execution (referring to `setup.py`).

(This is before wheels existed, of course, so that would have been even more true.)

### January 2016

[Pip v8.0.0 is released](https://pip.pypa.io/en/stable/news/#v8-0-0), deprecating `pip install --download` in favour of the newly added `pip download`. (This doesn't really change anything about The Bug, except for the UI.)

### November 2016

[Pip v9.0.0 is released](https://pip.pypa.io/en/stable/news/#v9-0-0), adding a `--platform` flag for `pip download`. This actually partially fixes The Bug temporarily, in that specifying a platform only works with wheels and errors out unless wheels are demanded.

### February 2017

Issue 4289, "[Issue with "pip download \-\-platform" semantics](https://github.com/pypa/pip/issues/4289)" is opened on the Pip bug tracker, reporting the (undocumented) restriction mentioned above.

### May 2017

Some comments on issue 4289 propose that it shouldn't be necessary to run `setup.py` when using `pip download --no-deps`.

### June 2017

A proposal is made to close issue 1884 because the `pip install --download` command syntax no longer exists (although it does - it's only been deprecated); but it's pointed out that the problem still exists with `pip download`.

### March 2018

[Pip v10.0.0.b1 is released](https://pip.pypa.io/en/stable/news/#b1-2018-03-31), fixing issue 4289 but once again making it possible to encounter The Bug even when specifying a platform explicitly. (Also, the completely nonsensical ability to specify `--editable` for `pip download` was removed, as was the deprecated `pip install --download`.)

### July 2018

Pip switches to [Calendar versioning](https://calver.org/) with the [release of version 18.0](https://pip.pypa.io/en/stable/news/#v18-0). (This isn't particularly relevant to The Bug, but is a useful reference point for understanding the overall history.)

### November 2019

The title of issue 1884 is edited for the first time, to reflect the change from `pip install --download` to `pip download`.

Issue 7325, [Disallow execution of setup.py when "pip download \-\-no-deps someproject"](https://github.com/pypa/pip/issues/7325) is opened on the Pip bug tracker. (This is one of many duplicates, mentioned here primarily because it's one that Brendan Dolan-Gavitt cited.)

### April 2020

Issue 7995, "[`pip download --no-deps --no-binary` does some unwanted build steps](https://github.com/pypa/pip/issues/7995)" is opened on the Pip bug tracker.

A choice quote:

> > Is there any case where it is useful to collect dependencies when `--no-deps` is specified?
>
> No, pip is just not smart enough to not do it. The “problem” here is that `pip download` simply reuses code from `pip install` and just skips the actual install part.

Meanwhile, a workaround is offered on issue 1884, but it turns out not to work in current versions of Pip.

### June 2020

Issue 8387, "[Using pip download to fetch package sources seems to trigger building wheels for some packages.](https://github.com/pypa/pip/issues/8387)" is opened on the Pip bug tracker. This is another duplicate, but it notably reveals the fact that `setup.py egg_info` is run when `--no-use-pep517` is passed to `pip download`.

### July 2020

PEP 625, ["Filename of a Source Distribution"](https://peps.python.org/pep-0625/), is created. The proposal is supposed to standardize the filenames used for sdists, following existing common-but-not-guaranteed practices, such that Pip could reliably determine the project name and version from the filename. It will take over two years for this proposal to be accepted.

### August 2020

Relevant commentary on issue 1884, with links to additional discussion on the Python Discourse forum:

> The root problem is that [source distribution metadata is not trustworthy](https://discuss.python.org/t/why-isnt-source-distribution-metadata-trustworthy-can-we-make-it-so/2620), and [it’s difficult to avoid building metadata sinnce pip needs to check for package integrity](https://discuss.python.org/t/pip-download-just-the-source-packages-no-building-no-metadata-etc/4651). The thing we really need to do before any of this can reasonably happen is to have standardisation on essential sdist metadata (namely package name and version) somehow. There has been efforts on this; feel free to contribute to them.

It's further noted that:

> `pip download foo-1.0` could find a file `foo-1.0.tar.gz` which contained a project called bar, version 2.0.
>
> Pip has to get the package metadata (by building) to confirm that the filename matches the metadata.

(This is the problem that PEP 625 aims to solve.)

It is not really explained why such a hypothetical result should be a problem (or what to do with the already downloaded file) when `--no-deps` is specified. Instead:

>>> Honestly, why not just get the PyPI URL and download it directly? You seem to be going to a lot of effort (and expecting others to as well) to basically download a file whose name you know.
>>
>> ...the reason not to just get the PyPI URL and download directly is that I want to get the same file that `pip install` would have chosen. And I don't know the filename ahead of time, the input is not necessarily a project name + version (pinned) but a general [requirement specifier](https://pip.pypa.io/en/stable/reference/pip_install/#requirement-specifiers).
>>
>> ...
>>
>> So I figure the only way to reliably download the correct release file (correct meaning "same one that pip would choose") is to use pip itself. Since there is no public API here, that means using the command line interface in a subprocess.
>
> *\[no response\]*

### September 2020

Issue 8850, "[`pip download --no-deps` runs `setup.py egg_info` unnecessarily and fails](https://github.com/pypa/pip/issues/8850)" is opened on the Pip bug tracker. Notably, the name of the [`egg_info` subcommand](https://setuptools.pypa.io/en/latest/deprecated/commands.html#egg-info-create-egg-metadata-and-set-build-tags) refers to the long-outdated "egg" format for packages; Pip still supports this (but at least it's *deprecated*... since 23.2... on Python 3.11 and up... and there may still be binary distribution formats that use the corresponding `.egg-info` metadata format). This report was dismissed as a bug in the package (which was trying to use undocumented internals of Pip in its `setup.py` logic).

### October 2020

PEP 643, ["Metadata for Package Source Distributions"](https://peps.python.org/pep-0643/) describes version 2.2 of the core metadata (i.e. `PKG-INFO`) standard. According to this standard, the `Name` and `Version` of the project MUST NOT be marked as `dynamic` in an sdist, and consequently the values for these in the corresponding wheel MUST match.

### December 2020

It is [discovered and reported on issue 1884](https://github.com/pypa/pip/issues/1884#issuecomment-745568242) that the demand for unnecessary metadata may have to do with the resolver. Pull requests [9305](https://github.com/pypa/pip/pull/9305) and [9311](https://github.com/pypa/pip/pull/9311) are created accordingly, but ultimately go nowhere. (This appears to explain the problem with the workaround offered in April.)

### March 2021

Issue 9701, "[pip download \-\-no-deps tries to use PEP517 so badly it is not usable to download stuff](https://github.com/pypa/pip/issues/9701)" is opened on the Pip bug tracker. We get this choice quote:

> The problem is that the only way to be sure that a sdist actually provides the version you specify is to build it. Yes, we could rely on the sdist filename, but it's not technically reliable, and we'd need to special-case stuff to make it work.
>
> If and when build backends start including [PEP 643](https://peps.python.org/pep-0643/) style metadata in sdists, to a level where it's worth the effort to check it before trying a build, we could use that to avoid the build step where the data is available statically. But I'm not even sure if any tools have implemented PEP 643 yet...
>
> To be honest, though, if you want to just download a sdist from PyPI, pip probably isn't the tool you want. It's not that hard to query the PyPI JSON interface for the sdist url, and wget it. If I were doing this often enough that manually downloading via the web interface was insufficient, that's what I'd do.

(Editor's note: the link to PEP 643, "Metadata for Package Source Distributions", is not present in the original.)

Meanwhile, back on issue 1884, in response to someone ruminating about forking Pip or starting work on a replacement:

> I'm genuinely not being sarcastic or passive-aggressive here, I agree with this - I think it could only be healthy for the ecosystem to have alternatives to pip, which can look at alternative approaches without all of the backward compatibility constraints that pip works under.
>
> ...
>
> By the way, I assume you're aware that if all you actually want is to download a file from PyPI, the JSON API is pretty straightforward to use. You can even do it as a shell one-liner, if you like:
>
> ```
> wget $(curl https://pypi.org/pypi/pip/json| jq -r '.releases[.info.version][] | select(.packagetype=="sdist") | .url')
> ```
>
> Making that into a Python script with options, etc, is pretty straightforward.

(But it is still, to the best of my knowledge, not offered officially as a tool by PyPA. It also doesn't invoke any resolver logic.)

There's also a reference back to issue 7995, and an objection that validation can't just be opt-in:

> The biggest roadblock (aside from coming up with a rule that makes sense) is implementation; validation should only be skipped on very specific subcommand-option combinations, and it’s not trivial to pass all the needed context all the way down to where the validation is done.

This "pass all the needed context" language appears to refer to the December 2020 discovery. There's also a reference to issue 6607, ["Build Logic Refactor"](https://github.com/pypa/pip/issues/6607) from June 2019, which proposes some cleanups for that context chain.

(Again, the complaints made on issue 1884 in August 2020 are not addressed.)

Finally the issue was (understandably) duped to 7995.

### July 2021

Issues 7995 (originally specifically about `pyproject.toml` based builds) and 1884 (originally specifically about `setup.py` based builds) are consolidated.

### October 2021

An interesting comment from issue 1884:

> Apologies, I got confused between PEP 621 (Storing project metadata in pyproject.toml) and PEP 643 (Metadata for Package Source Distributions). PEP 621 is irrelevant here, as tools should not read metadata from pyproject.toml. Reading metadata from a sdist via PEP 643 would be useful, and is valid, though. While I guess it's tempting to assume that pip can read pyproject.toml and if it finds PEP 621 data, then use it, it would be wrong because there's no guarantee that the backend supports PEP 621, so there's no reason to believe that the metadata in the generated wheel/sdist would bear any relationship to the PEP 621 data.

### August 2022

Issue 1884 is locked, with the comment:

> ...an easy way to restart discussion is if someone creates a PR with a suggested solution 🙂

### September 2022

PEP 625 is accepted.

Issue 3593, ["[FR] Implement PEP 625 - File Name of a Source Distribution"](https://github.com/pypa/setuptools/issues/3593) is opened on the *Setuptools* issue trtracker. It is closed as completed in June 2024.

## Parting Thoughts

Readers are invited to draw their own conclusions about the Pip project's attention to detail and the pace at which issues are tackled.

This is certainly not entirely the fault of the Pip development team. Pip is a hideously complex piece of software; there's no real opportunity to refactor it properly since it's so fundamental to Python (it gets shipped with Python and bootstrapped into virtual environments despite not being part of the standard library - more on that in a later post); and there are nowhere near enough people working on it with nowhere near enough free time, relative to the expectations put upon it (especially in terms of backwards compatibility - a theme I will *definitely* be hammering in future posts). Also, there's heavy overlap between the Pip and Setuptools teams, and Setuptools has basically all the same problems and challenges.

But the net result is still quite alarming. Just to emphasize a couple aspects of this whole mess:

1. In January of 2016, the `pip download` command syntax was added, and the corresponding `pip install --download` syntax was deprecated. It took almost 4 years until anyone even *updated the title* of issue 1884, one of the most important in Pip's history.

1. In July of 2020, it was proposed to standardize sdist filenames in a way that would allow Pip to make some basic assumptions about what it just downloaded. It took two years to accept that proposal, another two years to make sure Setuptools always conforms to that standard, and now *Pip still doesn't make those assumptions*. We're talking here about standardizing a *file naming convention* -- to follow a pattern that almost everyone was already following outside of abandoned legacy Python 2.x projects -- just so that Pip can actually *trust that PyPI gave it the correct file*.
