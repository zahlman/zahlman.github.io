# Leaning IN to my U/X #linux #personal

    :::bash
    $ stat / | grep Birth | cut -d ' ' -f 3
    2022-01-24

Today (although this won't go live until the 25th in my time zone) is three years since the day I finally kicked Windows to the curb and installed Linux on my home desktop. I'd used Linux before, but all my life I'd had a habit of just using whatever OS was provided to me, without really giving it much thought.

In late 2021, Windows Update told me - entirely unprompted - that my system didn't meet minimum specs to run Windows 11. (Perhaps it would now - I understand that the declared requirements have been relaxed, even if nothing has been optimized or stripped down - but I don't care to check. I'm also told that people still on Windows 10 are under increasing pressure to switch, even though they're [still comfortably in the majority](https://www.pcworld.com/article/2508289/windows-11-market-share-grows-but-windows-10-still-twice-as-popular.html) - unless something has radically changed in the last few months.)

I found this impolite - as I hadn't asked, and didn't consider anything wrong or inadequate about my computer - and a bit absurd (whatever they're offering now that requires more computing power, I'm not interested; especially not if it's anything to do with Cortana). So I took that as my queue to switch. I bought a new SSD (figuring I would need the space anyway) and attempted to set up a dual boot - GRUB never worked properly for me, but I could still use the BIOS screen to boot Windows from the old SSD.

And I never looked back.

Today, I'd like to relate a few anecdotes about that experience.

<!-- TEASER_END -->

## Meta

{{% hitcounter %}}

It's been almost two weeks since [my last post](/posts/2025/01/11/a-brief-annotation/) and I certainly hoped I would have something else written up in that time. I've been struggling with the next post in my [Python packaging series](/tags-and-series/series-python-packaging/), which is supposed to be about a long-standing Pip bug. But I've been feeling rather distracted from it, at least in part because Pip 25.0 [is in development](https://pip.pypa.io/en/latest/) and [probably coming out soon](https://pip.pypa.io/en/stable/development/release-process/). I don't expect that the bug will be fixed, but it would be a bit embarrassing if it were and I went on at length about it just days before.

I really should have written something else in the mean time, but I didn't really commit to the decision until now - I knew long in advance that I would be writing this post, because I knew this anniversary was coming up.

## I use Mint, btw

When I made the switch, I recalled an older recommendation from a family member, claiming that Mint provides a relatively more Windows-like experience out-of-box. My own research seemed to confirm that this was a popular choice for migrants from Windows.

While I'm sure I could have handled setting up a "less friendly" Linux distribution, I figured that life was too short for that sort of thing. Mint comes with Firefox (already my browser of choice - although perhaps I should rethink that), LibreOffice (I had already played with OpenOffice on Windows) and GIMP (not the most fun image editor to use, but a full-powered one) bundled, and offers the Cinnamon desktop environment pre-installed so I wouldn't have to figure that out.

There's a lot included that I'd probably rather do without (such as CUPS) but I've been too lazy to look into what can be safely removed, or whether it's any more involved than just uninstalling it with Apt. All in good time. My `/usr` folder is still quite reasonably sized.

My initial impressions were quite positive (and I'm still overall very happy to have switched). I noticed the OS using considerably less RAM "at base" (i.e. with one user logged in, just looking at the desktop), and the system was much leaner. (I did, after all, set it up on a 16GB partition, and the initial space used was nowhere near even that mark - meanwhile, I'm quite sure my `C:\Windows` had been over 30GB, and that's before considering the backup it left of Windows 8 when upgrading to 10.) And system updates - accepting nearly everything the built-in Update Manager proposes, because life is again too short - run *much* faster.

I was happy to find that I recalled basically all my years-old knowledge of the Linux command line, too.

The main thing I missed in using the GUI is that Nemo apparently doesn't support right-click-dragging - the context menu shows up immediately when the right mouse button is pressed. And, of course, it was nice to be able to find human-readable config files for at least some things (`dconf` notwithstanding) and to be able to create `.desktop` files that are quite a bit more functional than Windows shortcuts to executables. (Similarly, I find symlinks rather more pleasant overall than shortcuts to non-executable files.)

Really, the worst thing about Mint isn't the software itself; it's the support. Users on the [forum](https://forums.linuxmint.com/) (reasonably) assume you're an unsophisticated beginner and often whiff on more advanced issues (or give dogmatic advice that ignores your needs and values). The package repositories give you outdated versions of software, and then the corresponding projects aren't interested in your bug reports or support questions because of that. It's bad enough that the included software sometimes includes its own workarounds: in particular, [Hypnotix will manage its own version of `yt-dlp`](https://www.linuxmint.com/rel_virginia_whatsnew.php) separate from the system. (And it really does need to; the version included in a new Ubuntu release could plausibly be rendered non-functional before the corresponding version of Mint is even available, because it's hacking around YouTube not actually providing a stable API.)

## Traps for the Unwary

When I did my initial configuration, I made some sub-optimal partitioning, in part due to finding outdated advice. I allocated far more space than necessary for a swap partition (and I'd probably be happy enough with a swap file anyway), and set up a rather cramped `/` partition. I don't really regret the latter, but it caused problems a few times.

The first major problem was that Timeshift's default configuration put snapshots into the `/` partition. (It could be worse; some users have had it try to write to a `/boot` or `/boot/efi` partition, which is *clearly* too small.) I hadn't allocated space for this and likely would have ended up in a login loop situation (or even been dropped to the dreaded ["busybox prompt"](https://askubuntu.com/questions/137655)) if I had logged out; as I recall, I managed to delete the snapshot and reconfigure Timeshift before any serious issue arose. The built-in tool for recovering the system from major problems, can *cause* major problems by using up disk space in the place where it's most precious.

Later on, with the various system updates, I learned that old copies of the kernel (and other packages) will accumulate and [need to be cleaned out](https://itsfoss.com/free-up-space-ubuntu-linux/) every now and then with `sudo apt autoclean` and `sudo apt autoremove`. And then I learned about the constantly-growing-by-default log file. (Another irony; the space taken up by logging can compound the problems the log is supposed to help diagnose.) Eventually I did run into a login loop, before I had learned about the [keyboard shortcuts](https://askubuntu.com/questions/33078) used to get to a virtual console for recovery.

The rational course of action, most likely, would have been to boot from rescue media; in my panic, I fired up Windows 10 instead (and suffered through a mountain of updates before I could use it to research the problem, and then finally go back and fix it).

## Having it my way

As I mentioned in the introduction, when I set up the system originally, I had intended to get GRUB working with dual boot. It didn't work right away, and I quickly gave up on trying to diagnose the problem - especially after seeing all the reports of working configurations getting corrupted by later Windows updates anyway, people running into issues with secure boot, etc.

But as it happens, that one time that I ran into a serious space crunch with Linux (which was, of course, trivially fixed by rotating logs with the `journalctl` command I'd just learned about, along with the usual routine to remove old kernels) ended up being the *only* time I booted Windows ever since. I think I can safely say I've left it behind for good, although I still have the old SSD (which, I suppose, serves as one more backup of some of my old data).

Late last year, after upgrading Mint (all the way from 20.3 to 22), I decided to repurpose the partition I'd made on the new SSD for Windows. It's now where my home folders reside, while the original "Linux user-space" partition is now for large data (shared between user accounts). I've also ended up with a rather complex system of bind mounts and redirections, *intended* to make things easier for myself should I ever try my hand at distro-hopping. (Of course, no plan survives first contact with the enemy....)

Specifically, my setup involves:

* a 16GB partition hosting `/usr`, `/etc` and some other small system directories

* swap and boot partitions

* a `/home` partition which is about 1/4 of the drive, which also holds:

    * regularly-scheduled Timeshift backups (because my external media is usually not plugged in)

    * bind mounts for `/opt` and `/tmp`

    * a `user_files/` subdirectory, which contains each user's real `Desktop` folder (and other such folders like `Documents` etc.; but I don't use those)

    * a distro-specific subdirectory which contains the actual user home folders, which themselves symlink into the `user_files/` as needed, and also has `/var` bind-mounted

* and a `/home/media` partition for the balance of the drive.

I debated over the proper mount point for the shared files - eventually I decided that a subdirectory in `/home` would be cleanest, but I suppose I could just as easily have made it `/data` or `/srv`. The reason `/var` is treated differently from `/opt` and `/tmp` is that I figure I'd want to share software between distros in `/opt` (and `/tmp` doesn't matter, of course - TODO: try using a `tmpfs` for it), but I'd want to keep separate logs for each distro in `/var`. Unfortunately, it turns out that Flatpak likes to use `/var` rather than `/opt` - the latter would make far more sense to me for "portable" software, but it is what it is.

## A Fistful of Dollar Signs

I can't really think of a good way to conclude the prose for this post, so instead let me just dump out some of the aliases and functions I've set up in my `~/.bash_aliases` that have made my life easier. I hope they can benefit you, too.

1. A couple of commands for [fixing line endings in Git repositories](https://stackoverflow.com/questions/1510798/) (important when migrating from Windows to Linux):

        :::bash
        alias git-readd='git rm --cached -r .; git add .'
        alias git-refresh='git ls-files -z | xargs -0 rm; git checkout .'

    The `git-readd` will re-add everything from the working copy, which gives Git's `core.autocrlf` setting a chance to re-process the line endings. Then `git-refresh` will check out the re-processed files. This allowed me to start with a working copy and repository both using Windows line endings, and convert both to Linux line endings.

2. An alias to make the first push of a new locally created Git branch:

        :::bash
        alias git-first-push='git push --set-upstream origin `git branch --show-current`'

    Git is queried to get the name of the current branch, which is then used to `--set-upstream` for the push.

3. A wrapper for forking GitHub projects for quick fixes:

        :::bash
        github-dev() { IFS="/" read -r repo project <<< "$1"; git clone --depth 1 https://github.com/${repo}/${project}; cd ${project}; git checkout -b $2; }

    This is run like `github-dev user/project feature`, which will clone the most recent commit for the `user/project` GitHub repository, `cd` into it, and switch to a new `feature` branch.

4. Some wrappers for `wc`:

        :::bash
        lc-all() { find . -not -path '*/.*' -type f "$@" -print0 | xargs -0 wc -l; }
        lc-sorted() { lc-all "$@" | sort -h; }
        lc-total() { lc-all "$@" | tail -n 1 | awk '{print $1}'; }
        cc-all() { find . -not -path '*/.*' -type f "$@" -print0 | xargs -0 wc -c; }
        cc-sorted() { cc-all "$@" | sort -h; }
        cc-total() { cc-all "$@" | tail -n 1 | awk '{print $1}'; }

    These let me easily sum the lines and/or bytes taken up by, say, all the Python files in a project. Hidden files and folders are excluded by default; additional arguments can be passed through to `find`. The `find` results are processed (via `xargs`) into separate arguments for the `wc` command, allowing it to collate the results.

5. My Python "project management" setup:

        :::bash
        alias activate-local="source .local/.venv/bin/activate"
        alias try-it="(cd .local/ && source run-acceptance-test)"
        activate-pipx-venv() {
            source "`pipx environment --value PIPX_LOCAL_VENVS`/$1/bin/activate";
        }
        pipe() {
            if [ -z ${VIRTUAL_ENV+x} ]
            then
                echo "No venv active; use pip instead"
            else
                ~/.local/bin/pip --python `which python` "$@"
            fi
        }
        global-pipx-install() {
            sudo ~/.local/bin/pipx@171 install --global --pip-args='--only-binary=:all:' "$@"
        }

    I have multiple versions of Python compiled from source and set up in `/opt`, with symlinks to the binaries in `/usr/local/bin`; and I have a Python script in `/usr/local/bin` which simplifies making a venv for a given Python version as well as installing the current project into that venv. The venv is created at `.local/.venv` relative to the project root, so I have an alias to simplify activating that from the project root. The `.local` directory can house an informal acceptance test, as well as other files that I neither want to commit nor mention in the repository's `.gitignore` - so it contains its own `.gitignore` file with just `*` (i.e., everything in that folder is ignored; and since the folder is empty from Git's point of view, it never itself gets added).

    `activate-pipx-venv`, `pipe` and `global-pipx-install` [were explained in my previous Python packaging post](/posts/2025/01/07/python-packaging-2/) (how's that for alliteration?).

6. A scan for broken symlinks:

        :::bash
        broken-symlinks() { find -L . -type l "$@"; }

    The idea is that telling `find` to follow symlinks will normally prevent symlinks from showing up in the results (because they were followed instead of being treated as results) - unless they're broken (in which case they can't be followed). Thus, filtering the results to symlinks shows any broken symlinks.

    This has been useful for diagnosing Python venvs that were broken when either the venv moved or the underlying Python did. Looking at it again, this could and probably should be an alias rather than a function, but whatever.
