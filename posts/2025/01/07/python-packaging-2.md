<!--
.. title: Python Packaging: Why we can't have nice things, Part 2
.. category: python-packaging
-->

# Stupid Pipx Tricks

Pip has a lot of problems (that I'll be discussing in future posts in this series), but the good news is that you don't have to resort to heavyweight third-party tools to improve your experience with Python packaging. [Pipx](https://pipx.pypa.io/stable/) (now [under](https://packaging.python.org/en/latest/key_projects/#pipx) the [Python Packaging Authority (PyPA)](https://www.pypa.io/en/latest/) umbrella) is a focused wrapper around Pip that handles the major pain points without trying to take over your entire workflow.

In this post I'll talk about Pipx's major use cases, its limitations, and how to get more mileage out of it with a few simple tweaks.

<!-- END_TEASER -->

## Meta

{{% hitcounter custom_slug=stupid-pipx-tricks %}}

When I originally conceived of this series, I figured I'd have a post far down the road about good practices to avoid problems with existing tools and ways to make the experience suck less. Unfortunately, while third-party tools work well for a lot of other people, I can't find a lot to recommend them based on my personal needs and preferences. Outside of "wait until my own projects, [Paper](https://github.com/zahlman/paper) and [bbbb](https://github.com/zahlman/bbbb/), are in good working order", I realized that most of the productive suggestions I can offer revolve around a) Pipx and b) some helper scripts I use with Pip. But now that I have Pipx, my workflow around Pip generally involves the copy of Pip that Pipx installs for itself and wraps.

Meanwhile, as I was working on other things and discovering that I really can't post with the frequency I'd like, I got private feedback that giving useful, actionable advice really should be a higher priority than pointing out all the technical issues. So, here we go.

Speaking of posting frequency: the last several days, instead of writing this content, I found myself obsessed with various bits of behind-the-scenes work on the blog. A lot of it isn't visible (extracting a copy of the Nikola theme and refactoring it to be simpler, more personally understandable, and easier to modify in the future); but I did also make some actual changes that I hope you'll agree are for the better. In particular, I've set up [giscus](https://giscus.vercel.app/) comments so you don't have to head over to the GitHub issue tracker (I don't think I got around to mentioning that I would have been totally fine with that!) or give feedback elsewhere. In my research, this was the commenting system that seemed to make the most sense for my use case.

## What Pipx does

Pipx [is](https://pipx.pypa.io/stable/how-pipx-works/) a wrapper for Pip designed for installing and running "applications" from PyPI. Formally this just means that you must specify a [distribution package](https://packaging.python.org/en/latest/discussions/distribution-package-vs-import-package/) *that includes at least one "entry point" in its metadata* - something that, when installed with Pip normally, would offer a command you can use at the command line to run the program. (In theory, "applications" are also supposed to pin their dependencies very strictly, but there isn't really a good reason to insist that developers do so.)

When you install a distribution package with Pipx, Pipx creates a new [virtual environment (venv)](https://chriswarrick.com/blog/2018/09/04/python-virtual-environments/) for it, installs into that environment using its own private copy of Pip (which naturally creates some kind of "exectuable wrapper" in a `bin/` subdirectory of the venv). Then it symlinks (or makes some other kind of wrapper on Windows) those wrappers in a directory that's on your `PATH` - so that you can easily run the program without activating the venv.

[You can also choose](https://pipx.pypa.io/stable/#walkthrough-running-an-application-in-a-temporary-virtual-environment) to "run" the application directly, which installs it into a temporary venv and immediately stars the program.

By default, all of this installation is done at a user level, but with newer versions (and appropriate system permissions, and it doesn't work on Windows yet) you can also make system-wide installations. On Linux, user installations go in `~/.local` by default (the always-available symlinks are in `~/.local/bin`, and per-application venvs are in `~/.local/pipx/venvs`); system-wide installations put the executable in `/usr/local/bin` and the venvs in `/opt/pipx/venvs` - all very logical and in keeping with Linux standards.

## What it doesn't do

Pipx offers a few more commands for managing the venvs it creates, but it's really not a full scale environment manager - at least, not without a bit of prodding.

More importantly, it will refuse to install anything that doesn't offer any entry points. It also won't make use of existing venvs that you create yourself.

Finally, in terms of the actual installation process, it's stuck with all of Pip's limitations and idiosyncrasies. It just takes care of making sure there's an appropriate environment for Pip to install into, and making sure that Pip installs into that environment. (And, you know, making sure that Pip is always available for this purpose.)

## Trick 1: Managing environments and "installing" libraries

Although Pipx doesn't "install libraries", it will happily "inject" arbitrary dependencies into a venv that it created for a different application. The installation also passes arbitrary arguments to Pip (which means you don't have to get things from PyPI, either).

This means for example that if you're developing an application, you can use Pipx to do an "editable" install of your project (`pipx install -e .` from your project root), as long as you have your build set up properly. This will automatically install your project's own already-declared dependencies, but you can also edit those choices independently of what you declared in `pyproject.toml`.

This also means that you can make a new, more or less "blank" project, "install" it and then "inject dependencies" into it, in order to create a venv that just has those libraries available. You might find this a little easier than creating a venv yourself for that purpose; and the venv is automatically put somewhere that won't be in your way. Then, you can activate that environment to test out the library at the Python REPL. Pipx also offers an `environment` command that gives you the path to a given application's venv (in case you changed the defaults, or just don't want to calculate it yourself). Based on that, I made a wrapper function in Bash:

```
# Activate the venv of something installed with Pipx.
activate-pipx-venv() { 
    source "`pipx environment --value PIPX_LOCAL_VENVS`/$1/bin/activate";
}
```

Now I can `activate-pipx-venv foo` to use the `foo` application's environment. In particular, that means I can run `python` to get a REPL in that environment, `import` libraries that I injected into that environment, and play around with them. (Or if I installed a "real" application, I can debug it from here.)

I did a bit of work on an unpublished project intended to facilitate this, among other things. But I probably won't come back to it, because Paper is intended to replace Pipx.

## Trick 2: You get Pip for free!

When you install Pipx, it creates a separate venv for its own copy of Pip - which it will bootstrap using the standard library `venv` and keep updated automatically. When it creates per-application venvs, it won't copy Pip into those, because that isn't necessary. For legacy support reasons (in particular, because some programs want to be able to [run Pip in their own subprocess](https://til.simonwillison.net/python/call-pip-programatically) without having declared it as a dependency (Pip [*does not provide*](https://pip.pypa.io/en/latest/user_guide/#using-pip-from-your-program) a programmatic API) without having declared Pip as a dependency), the new venvs will get a [`.pth file`](https://docs.python.org/3/library/site.html#:~:text=pth%20file) which virtually adds the shared copy of Pip to those environments.

But modern versions of Pip ([since 22.3](https://pip.pypa.io/en/stable/news/#v22-3)) can easily be made to install into other Python environment besides their own, using the `--python` flag. (It was possible before that, but more difficult and more error-prone. The specific way this feature works is really awkward, and will definitely be covered in a future post.) This practically means that you really never need more than one copy of Pip - and the one that Pipx provides is quite convenient even if you're on a Linux distribution that [doesn't include Pip with the system Python](https://software.codidact.com/posts/291787).

To set this up, start by symlinking that Pip so it's always available - I symlinked it in `~/.local/bin/pip`, right beside the symlinks Pipx makes for the applications. Now, I don't want to use this Pip to install into its *own* venv (since that one only exists to give Pip a home - although for older Python versions it might also include Setuptools), and I [don't want](https://stackoverflow.com/questions/75608323) to install for the system Python, even with `--user`. So I use a little wrapper:

```
# PIP (the pipx-installed copy) in the current Environment.
pipe() {
    if [ -z ${VIRTUAL_ENV+x} ]
    then
        echo "No venv active; use pip instead"
    else
        ~/.local/bin/pip --python `which python` "$@"
    fi
}
```

As long as a venv is active, this uses the shared Pip to install into the active venv. It works because of *what "activating a venv" means*: it arranges to ensure that `python` refers to the venv's Python, so we ask `which` for the path to that, then tell Pip to use it. The venv activation script also sets a `VIRTUAL_ENV` environment variable which we can easily use to check for activation. (We could also pass `--require-virtualenv` to Pip, of course.)

With this trick, you never need another copy of Pip - which means you can create new venvs `--without-pip`. This saves considerable space and time. On my system:

```
$ time python -m venv with-pip

real	0m3.242s
user	0m3.013s
sys	0m0.205s
$ time python -m venv --without-pip without-pip

real	0m0.052s
user	0m0.043s
sys	0m0.009s
$ du -B1 -s with-pip/
15974400	with-pip/
$ du -B1 -s without-pip/
57344	without-pip/
```

## Trick 3: Installing Pipx with Pipx

Pipx can "upgrade" installed applications and their dependencies (both the ones specified by the main application, and ones you inject manually), i.e. update them in-place to the latest version. It also automatically upgrades its shared Pip copy.

However, it can't upgrade itself, since it hasn't installed itself the same way it installs other things.

Which means that, for example, if you get Pipx from your system's package manager, you could be stuck with a very out-of-date version missing new functionality. For example, even the latest Mint distribution appears to be stuck with Pipx 1.4.3, meaning it doesn't support global installations.

However, the Pipx code *is* available on PyPI as well. In principle, you could set up your own venv with an existing copy of Pip, install Pipx there, link the `pipx` executable somewhere convenient, and go from there. But that's extra effort, and then the Pip-installed Pipx still won't upgrade itself - you'll have to use plain Pip again to do that.

Or you could install Pipx... with your existing Pipx.

This is [officially not recommended](https://pipx.pypa.io/stable/#install-pipx) and comes with some caveats, but there's a [third-party helper](https://github.com/mattsb42-meta/pipx-in-pipx) available.

But actually you don't need that, either. Just use the `--suffix` option so that your installed pipx-in-pipx has a different name - something like:

```
pipx install --suffix @171 pipx==1.7.1
```

Now `pipx` means your original installation, and `pipx@171` means a separate copy of Pipx, version 1.7.1, which supports global installation. (Note that for local installations, it will default to using the *same* venv folder. But this installation doesn't do anything beyond setting up the `pipx` code in a new venv; and when you run Pipx out of that venv, it will be able to use the same shared Pip copy without having had to set one up.

And, yet again, I have a useful small wrapper for this copy (which I set up specifically to get the global-install feature):

```
# Install things with Pipx globally. Requires sudo.
# For safety, only wheel-based installations are attempted.
global-pipx-install() {
    sudo ~/.local/bin/pipx@171 install --global --pip-args='--only-binary=:all:' "$@"
}
```

Nice and neat. Now I can, for example, `global-pipx-install twine`, and have the [Twine command for uploading to PyPI](https://twine.readthedocs.io/en/stable/) immediately available, to all users, regardless of whether a venv is active (or which one) - and it will fail if there are no wheels available, which is important because of - well, the subject of what I expect to be part 3 in the series.
