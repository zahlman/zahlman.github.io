# Python Packaging 外伝１: Oxidation and Radiation @python-packaging
# The Rise of `uv` in 2025 #python #uv #design

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

## Rocket-ship-emoji Blazing Fast, Written in Rust Sparkle-emoji

The most obvious thing to say about `uv`, snark aside, is that it genuinely does perform `pip`'s tasks far faster than `pip` does, overall. The thing that annoys me about this is that the discussion will be full of people who attribute this to the implementation language and seemingly don't think about it any further. That's overly reductive, and a bad habit in general, but in this case I'm very solidly convinced that the conclusion is mostly just wrong.

First off, it's not really that `uv` is fast. It's much more that *`pip` is slow*. And there are many reasons I can point to for this. My thesis — and one of the main reasons I'm making PAPER — is that "`pip` is written in Python" is honestly pretty far down the list of causes of its poor performance. Of course I don't deny that doing things in a compiled language like Rust is going to offer additional benefits; I just doubt that they're as significant, or that they would matter so much once the real problems are addressed.

I recognize that's a bold claim. Python has a reputation for poor performance even among other "dynamic" languages (where JavaScript in particular has seen significant work on optimization). The proof is in the pudding, of course, and I've been cooking for far too long. But let me just point out the things I'm trying to fix, performance-wise:

 of causes of its poor performance. Of course I don't deny that doing things in a compiled language like Rust is going to offer additional benefits; I just doubt that they're as significant, or that they would matter so much once the real problems are addressed.

 I recognize that's a bold claim. Python has a reputation for poor performance even among other "dynamic" languages (where JavaScript in particular has seen significant work on optimization). The proof is in the pudding, of course, and I've been cooking for far too long. But let me just point out the things I'm trying to fix:, performance-wise:

1. (top-level imports and `--python`)

1. (download cache)

1. (hard-linking)

1. (precompilation)

1. (resolver)

## Easy as Seven-Two-Three

The hype around `uv` is strong enough that it seems to get credit for things that even the authors explicitly disclaim. In particular, [a workflow using a `uv`-based shebang has become popularized](https://duckduckgo.com/?q=uv+pep+723), using the [provision for declaring a script's dependencies inline](https://docs.astral.sh/uv/guides/scripts/#declaring-script-dependencies) described in the `uv` documentation.

Astral employees are, to their credit, quick to point out that this is not their invention; they've only implemented the [PEP 723 standard](https://peps.python.org/pep-0723/). For example, you [can do all the same things with Pipx](https://github.com/pypa/pipx/pull/1100) using `pipx run` (although the [reference documentation doesn't explain this](https://pipx.pypa.io/stable/docs/#pipx-run) and you [have to dig pretty deep](https://pipx.pypa.io/stable/examples/#pipx-run-examples) to find it mentioned in the examples), and have been able to do so since late 2023. (But of course, it's even less performant than `pip`, as it wraps `pip`.)

And again, this is an ecosystem-wide standard now. It's worth noting that it was authored by [the creator](https://github.com/ofek) of [Hatch](https://github.com/pypa/hatch), and the [competing proposal](https://peps.python.org/pep-0722/) came from [a `pip` maintainer](https://github.com/pfmoore). So of course Hatch [can do it](https://hatch.pypa.io/dev/how-to/run/python-scripts/). And while it [appears that a script runner would be out of scope for `pip`](https://github.com/pypa/pip/issues/12891), at least support [has been recently merged from a PR](https://github.com/pypa/pip/pull/13052) for *installing* PEP 723 dependencies (so it presumably will appear in 26.0).

Presumably there are other tools that can do it too.

## It Slices, it Dices, it Makes Julienne... Wheels

One of the things many people seem to like about Rust is that it strives to be an all-in-one solution, for both developers and end users. On top of what other tools like Hatch, Poetry and PDM have offered, it even grabs and installs [standalone builds](https://github.com/astral-sh/python-build-standalone) of Python, thanks to the work of [Gregory Szorc](https://github.com/indygreg).

This is not my favourite thing at all; I very much subscribe to the UNIX philosophy and would prefer to compose my tool chain. It comes across that the various packaging standards developed over the last several years have been aimed at facilitating that. There was a period when I was using Poetry, but it wasn't really for package management, but for its build backend. (Since my projects generally are pure Python, I mainly use Flit now, but will of course switch to [`bbbb`](https://github.com/zahlman/bbbb) when and where it meets my needs.) Of course, `uv` [even covers that now](https://docs.astral.sh/uv/concepts/build-backend/), at least for pure Python projects.

Really, I'm mainly not a fan of having a bunch of subcommands of `uv` (and the shortcut `uvx`) that do what I see as widely disparate things. I felt the same way about Poetry, and I especially dislike having these tools manage the *use* of virtual environments (by providing a "shell" and/or automatically choosing which one to use based on the current working directory). I use the stock activation script when in development mode; that isn't everyone's cup of tea, of course, but I know I have the freedom to just specify a path to the environment's Python directly. (Which I often do when I'm just messing around with temporary environments to test something out.)

But I can't really do anything to change popular opinion.

## Conclusion

I can't really offer much of a conclusion here. I'm writing out some thoughts in a blog post; this isn't some formulaic high school essay. If you like `uv` and it's solving real problems for you, by all means continue to use it and don't let me hold you back from that. It just... isn't the tooling I hoped we'd get, for reasons that probably don't matter to a lot of people. If you like the ideas behind what I'm doing, I'm happy for any and all support. And I hope I can keep teaching people about Python packaging — and about Python, and really anything else I know about — far into the future.

Happy New Year.
