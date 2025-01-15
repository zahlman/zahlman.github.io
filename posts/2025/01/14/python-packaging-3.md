# Python packaging: Why we can't have nice things @python-packaging
# Part 3: Premature Compilation #python #pip #security #setuptools

*\[This post assumes that you have a basic familiarity with Python's current packaging system: i.e, that you recognize the tools Pip and Setuptools, and understand the concepts of sdists, wheels, and [build](https://peps.python.org/pep-0517/) [systems](https://peps.python.org/pep-0518/)). You should ideally also be familiar with the [`pyproject.toml`](https://packaging.python.org/en/latest/specifications/pyproject-toml/#pyproject-toml-spec) file which is now [used for project metadata](https://peps.python.org/pep-0621/), and with the `setup.py` files used by Setuptools.\]*

*\[If you're missing these fundamentals, please [read part 0 first](), and check out the official [Python Packaging User Guide](https://packaging.python.org/en/latest/) for more info.\]*

<!-- END_TEASER -->

## Meta

{{% hitcounter %}}

## Preamble

Pip 24.3 was [just released a couple of days ago](https://github.com/pypa/pip/releases/tag/24.3) -- followed [less than 9 hours later by a 24.3.1 patch](https://github.com/pypa/pip/releases/tag/24.3.1) to fix a regression. Just as I expected, though, it still doesn't fix what I've privately taken to calling The Bug.

So today, The Bug is what we're going to talk about.

But before I can do that, I need to tell a little story about a blog post, titled [Someone’s Been Messing With My Subnormals!](https://moyix.blogspot.com/2022/09/someones-been-messing-with-my-subnormals.html) and ostensibly about some finer details about what happens to floating-point math in your Python program when C extensions are compiled a certain way and then included in the project, however indirectly. The post was published a little over 2 years ago, and shown to me by a friend sometime in the interim, and it quickly became a focus of my attention.

The basic premise of the post is pretty simple: there's a compiler option `-ffast-math` supported by both GCC and clang, which indirectly causes the compiled code to mess with global process state, which changes the behaviour of ["subnormal"](https://en.wikipedia.org/wiki/Subnormal_number) floating-point values. I think I have a reasonably good understanding of the technical details involved in this -- but they don't normally concern me, so I don't spend a lot of time thinking about them.

You're probably wondering what on Earth that has to do with Pip, and I don't at all blame you. But it turns out that this story has a buried lede. See, our author decided to do an impressively deep analysis of which Python packages most commonly cause that problem "in the wild", how widespread the problem is, etc. Which led to a rather severe exposure to The Bug.

This part is best explained with a quote:

> I actually started down this path and set about running `pip install --dry-run --ignore-installed --report` on all 397,267 packages. This turned out to be a *terrible* idea. Unbeknownst to me, **even with \-\-dry-run pip will execute arbitrary code found in the package's setup.py**. In fact, **merely asking pip to** *download* **a package can execute arbitrary code** (see pip issues 7325 and 1884 for more details)! So when I tried to dry-run install almost 400K Python packages, [hilarity ensued](https://twitter.com/moyix/status/1566561433898426368). I spent a long time [cleaning up the mess](https://twitter.com/moyix/status/1566578412663209984), and discovered some [pretty poor setup.py practices](https://twitter.com/moyix/status/1566609622680608770) along the way. But hey, at least I got [two free pictures of anime catgirls](https://twitter.com/moyix/status/1566612152558944257), deposited directly into my home directory. Convenient!
>
> Once I had managed to clean up the mess (or hopefully, anyway—I never did find out what package tried to execute sudo), I decided I needed a different approach.

(Editor's note: I've removed the links to the Pip issues because they'll come up again later in this post. And yes, that last link *does* include the pictures in question.)

So, yes, that's The Bug: the arbitrary setup code included with an sdist can be run *even for innocuous sounding "download" commands*.

To be clear, I don't fault Python for relying on arbitrary code at install time in general. The *requirements* to set up a Python project are pretty well arbitrarily complex, and nobody has really put forward a system that reliably handles even the common cases in any secure manner - at least, aside from pure Python projects where there's nothing to build. Aside from which, it's the same problem seen in other packaging systems for other languages, like NPM. ([Here's just one of many](https://medium.com/@v_pragma/12-strange-things-that-can-happen-after-installing-an-npm-package-45de7fbf39f0) articles on that topic I found with a [quick search](https://duckduckgo.com/?q=npm+arbitrary+code+on+installation).) And finally, of course, if you're going to *use* an installed library, it can run arbitrary code at `import` time, or when you call any of its functions. That's just how it is with third-party code: ultimately, trust has to come from somewhere.

But the *entire point* of having a command like `pip download` is so that Pip's resolver can figure out which package is appropriate for your system and then *just download it for you*, which you'd typically do *specifically so that you can inspect it* before doing anything with it. (After all, there's nothing to guarantee that the contents correspond to any particular GitHub repository, generally speaking.) Or maybe you want to store it somewhere, perhaps as part of [setting up your own index](https://stackoverflow.com/questions/18052217). But regardless, you *aren't* trying to install it *yet*.

The above quote uses the only red text in the entire article, and is also, as far as I know, the main reason it got as much attention as it did. True, not all of those packages were actually downloaded; and of course a large fraction of those would have been "pre-built" distributions that can be installed without any customization. So no, our author did not exactly run 397,267 pieces of untrusted code unintentionally. But still, I can't pass on the opportunity to make the reference:

<iframe style="width:50%;aspect-ratio:16/9;margin:0 auto;display:block" src="https://www.youtube.com/embed/Az49aNuYeJs" title="YouTube video player" frameborder="0" allow="fullscreen" referrerpolicy="strict-origin-when-cross-origin"></iframe>
<!-- It looks like I have to do the whole thing with raw HTML... -->
<div style="text-align:center"><em>That is not a small number!</em></div><br />

But the situation is *even worse* than it already sounds. See, the author of that post, [Brendan Dolan-Gavitt](https://x.com/moyix) (@moyix) is not just some random C expert who read the Pip documentation (but not thoroughly enough). Brendan Dolan-Gavitt is a **security researcher** with an impressive publication history [going back to at least 2006](https://moyix.blogspot.com/2006/12/malware-with-twist.html).

So there's a cautionary tale for you. If someone like Brendan Dolan-Gavitt can mess this up, so can you. It might seem logical to use `pip download` to obtain packages for inspection, without doing any installation or setup work. But it doesn't work like you'd expect.

<big>**To download sdist packages from PyPI safely without installation, do not use Pip. Instead, go to the [actual PyPI website](https://www.pypi.org), find the page for the package you want, optionally choose a version from the "Release history" (manually determining what version you want), choose the "Download files" option.**</big>

Wheels can be downloaded safely with `pip --download --no-deps --only-binary=:all:` - no `setup.py` code will run, because there's nothing to build (and the wheel doesn't contain that code). It's crucial to use `--only-binary=:all:` so that Pip's resolver won't choose a version that's only available as an sdist.

No, there is no official, ready-made, secure automation for this. There's a JSON API, but you'll need to parse the result, determining the version number yourself. (For wheels you'd also have to determine the wheel tags; but again, Pip handles this case.) 

(This is also the best way to protect yourself against typo-squatters and other malware packages - on top of the PyPI maintenance team's own attempts to remove those projects. The website interface gives you your best possible shot at verifying that the package you're looking at is actually the one you want.)

## Demo

Here's a simple Bash script you can use to demonstrate the main issue on any compatible system, as long as you have `pip` configured to refer to a usable copy of Pip. (It doesn't even need to correspond to the same Python that `python` or `python3` runs.) It will also run completely offline (I tested with my network adapter disabled) as long as version 40.8.0 (that's quite old, BTW - released in February 2019) or later of Setuptools is installed and available in the same environment as that copy of Pip (i.e., the output of `pip list` should include a line for `setuptools`).

```
#!/bin/bash
mkdir demo-0.1.0

echo 'Creating PKG-INFO metadata conforming to the latest spec...'
cat << done_info > demo-0.1.0/PKG-INFO
Metadata-Version: 2.4
Name: demo
Version: 0.1.0
done_info

echo 'Creating setup.py...'
cat << done_setup > demo-0.1.0/setup.py
__import__('sys').exit("Arbitrary code could have been executed here.")
done_setup

echo 'Creating a fully standards-compliant pyproject.toml which matches PKG-INFO...'
cat << done_toml > demo-0.1.0/pyproject.toml
[project]
name = "demo"
version = "0.1.0"
[build-system]
requires = [ "setuptools>=40.8.0" ]
build-backend = "setuptools.build_meta"
done_toml

echo 'Creating an sdist conforming to the latest spec, with a standards-compliant filename (by making a properly-named tar.gz archive from the above)...'
tar czf demo-0.1.0.tar.gz demo-0.1.0/

echo "Pip version: $(pip -V | cut -f-2 -d' ')"
echo "Setuptools version: $(pip show setuptools 2>/dev/null | head -n2 | tail -n1 | cut -f2 -d' ')"
echo '"Downloading" the sdist that was just created...'
pip download --no-deps --no-build-isolation ./demo-0.1.0.tar.gz

# Clean up
rm -r demo-0.1.0/ demo-0.1.0.tar.gz
```

In my case, I installed Pipx with the system package manager, and `pip` refers to its vendored copy of Pip, in its own virtual environment, which I've kept up to date.

When I try this, I get the expected result (demonstrating a serious problem) as follows:

```
Creating PKG-INFO metadata conforming to the latest spec...
Creating setup.py...
Creating a fully standards-compliant pyproject.toml which matches PKG-INFO...
Creating an sdist conforming to the latest spec, with a standards-compliant filename (by making a properly-named tar.gz archive from the above)...
Pip version: pip 24.3.1
Setuptools version: 75.2.0
"Downloading" the sdist that was just created...
Processing ./demo-0.1.0.tar.gz
  File was already downloaded /home/zahlman/Desktop/demo-0.1.0.tar.gz
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

Notice in particular the `Arbitrary code could have been executed here.` message. Of course this is not a warning that Pip or Setuptools generates; it comes from the `setup.py` that was included in the sdist that the script creates.

## It just keeps getting worse

There are a few points I need to highlight here:

1. Yes, the download command in the script has a weird `--no-build-isolation` flag in it. This will be discussed in Part 2.

1. Yes, you can ask Pip to "download" a file that you already have, even one that's already in the PWD where it's supposed to get saved. That's amusing, but ultimately a minor quirk and not a bug. (In fact, it's helpful here, since it allows me to produce this test script without having to host a test package on PyPI.)

1. Yes, in this demo, Pip attempts to *run code from the package* even though it has explicitly only been asked to *download* it -- and even though it has already identified that the file is already there and doesn't need downloading.

You'd probably never guess *why* Pip thinks it should have to build a wheel at this point (which in turn involves asking Setuptools to run arbitrary code from `setup.py`), without me telling you.

It's so that Pip can **make sure that the name and version metadata that you'd get from building the project, match what you requested**.

Which leads to many more points to highlight:

1. Yes, the command says "download" and does *not* say anything like "verify" anywhere. This argument has historically not been very persuasive.

1. This verification is absurd when downloading from PyPI, because Pip has already asked PyPI for a specific version of a project with a specific name. With the local file, it's absurd because the user didn't ask for such verification and has already very deliberately specified the file. The time for such verification, if ever, is when the file is made available -- not when it's received.

1. This still happens even though Pip is on the latest version in my test. (I also demonstrate this with the latest Setuptools version - not that it should be Setuptools' responsibility to detect or do anything about this state of affairs; it's just trying to build a wheel, like Pip explicitly asked it to.)

1. This still happens in projects following up-to-date standards: using `pyproject.toml` and following PEP 621 to describe project metadata.

1. Yes, the correct name and version can already be seen in the filename. Pip doesn't care, because it doesn't think this information is reliable. [PEP 625](https://peps.python.org/pep-0625/) is supposed to make it reliable:

    > The filename contains the distribution name and version, to aid tools identifying a distribution without needing to download, unarchive the file, and perform costly metadata generation for introspection, if all the information they need is available in the filename.
    >
    > ...
    >
    > Currently, tools that consume sdists should, if they are to be fully correct, treat the name and version parsed from the filename as provisional, and verify them by downloading the file and generating the actual metadata (or reading it, if the sdist conforms to [PEP 643](https://peps.python.org/pep-0643/). Tools supporting this specification can treat the name and version from the filename as definitive. In theory, this could risk mistakes if a legacy filename is assumed to conform to this PEP, but in practice the chance of this appears to be vanishingly small.

    However, Pip still doesn't appear to support the specification, despite the fact that the PEP was written by a Pip developer, explicitly so that Pip could avoid this headache (among others).

1. Yes, the correct name and version can already be seen in `pyproject.toml`. But it's the official stance of the Pip development team that "tools should not read metadata from `pyproject.toml`" - since build backends aren't yet required to implement [PEP 621](https://peps.python.org/pep-0621/) (notably, Poetry [didn't until just last month](https://github.com/python-poetry/roadmap/issues/3)), there's no guarantee that the `PKG-INFO` corresponds to `pyproject.toml` . Also, Pip still supports legacy `setup.py`-based builds, therefore sdists aren't required to contain a `pyproject.toml` at all.

1. Yes, the correct name and version can already be seen in `PKG-INFO`. This is, in a sense, the "built" version of `pyproject.toml` containing metadata that tools *are* supposed to read. But this, too, isn't required to be present. And as of Pip 24.3.1, Pip apparently doesn't even *check*.

1. The `PKG-INFO` provided declares version 2.4 of the specification - the latest at time of writing. From version 2.2 onward, it is *required* that the name and version are specified here, and that building the sdist would produce a wheel with metadata (in the `WHEEL` file) with a matching name and version. In fact, the *specific purpose* of the 2.2 update to the specification was to ensure that this part of the metadata would be reliable. But Pip will *still* try to build the wheel, so that it can error out if the resulting wheel doesn't match. (Yes, "error out" *even though it already downloaded* the file it was asked to download.)

1. Historically, a common justification for building the project (going back before wheels existed) was in order to figure out its dependencies, which could then be automatically downloaded. However, Pip later added a `--no-deps` flag for downloading, which is used here, for the cases where you specifically want only the main package. This has no effect here: Pip will *still* try to build the wheel.

## It's been getting worse for over twelve Guido-forsaken years

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

## So where does that leave us?

Readers are invited to draw their own conclusions about the Pip project's attention to detail and the pace at which issues are tackled.

This is certainly not entirely the fault of the Pip development team. Pip is a hideously complex piece of software; there's no real opportunity to refactor it properly since it's so fundamental to Python (it gets shipped with Python and bootstrapped into virtual environments despite not being part of the standard library - more on that in a later post); and there are nowhere near enough people working on it with nowhere near enough free time, relative to the expectations put upon it (especially in terms of backwards compatibility - a theme I will *definitely* be hammering in future posts). Also, there's heavy overlap between the Pip and Setuptools teams, and Setuptools has basically all the same problems and challenges.

But the net result is still quite alarming. Just to emphasize a couple aspects of this whole mess: 

1. In January of 2016, the `pip download` command syntax was added, and the corresponding `pip install --download` syntax was deprecated. It took almost 4 years for someone to *update the title* of issue 1884, one of the most important in Pip's history.

1. In July of 2020, it was proposed to standardize sdist filenames in a way that would allow Pip to make some basic assumptions about what it just downloaded. It took two years to accept that proposal, another two years to make sure Setuptools always conforms to that standard, and now *Pip still doesn't make those assumptions*. We're talking here about standardizing a *file naming convention* -- to follow a pattern that almost everyone was already following outside of abandoned legacy Python 2.x projects -- just so that Pip can actually *trust that PyPI gave it the correct file*.
