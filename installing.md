[Please help Ukraine!](https://novaukraine.org)

[Sponsor](https://github.com/users/jgm/sponsorship)

<img src="https://www.paypalobjects.com/en_US/i/scr/pixel.gif" width="1" height="1" />

<span class="big">Pandoc</span>   <span class="small">a universal
document converter</span>

-   <a href="index.html" class="nav-link">About</a>
-   <a href="installing.html" class="nav-link">Installing</a>
-   <a href="demos.html" class="nav-link">Demos</a>
-   <a href="#" id="navbarDropdown" class="nav-link dropdown-toggle">Documentation</a>
    -   <a href="getting-started.html" class="dropdown-item">Getting started</a>
    -   <a href="MANUAL.html" class="dropdown-item">User's Guide</a>
    -   <a href="MANUAL.pdf" class="dropdown-item">User's Guide (PDF)</a>
    -   <a href="CONTRIBUTING.html" class="dropdown-item">Contributing</a>
    -   <a href="faqs.html" class="dropdown-item">FAQ</a>
    -   <a href="press.html" class="dropdown-item">Press</a>
    -   <a href="filters.html" class="dropdown-item">Filters</a>
    -   <a href="lua-filters.html" class="dropdown-item">Lua filters</a>
    -   <a href="custom-readers.html" class="dropdown-item">Custom readers</a>
    -   <a href="custom-writers.html" class="dropdown-item">Custom writers</a>
    -   <a href="pandoc-server.html" class="dropdown-item">pandoc-server</a>
    -   <a href="epub.html" class="dropdown-item">Making an ebook</a>
    -   <a href="org.html" class="dropdown-item">Emacs Org mode support</a>
    -   <a href="jats.html" class="dropdown-item">JATS support</a>
    -   <a href="using-the-pandoc-api.html" class="dropdown-item">Using the Pandoc API</a>
    -   <a href="http://hackage.haskell.org/package/pandoc" class="dropdown-item">API documentation</a>
-   <a href="help.html" class="nav-link">Help</a>
-   <a href="extras.html" class="nav-link">Extras</a>
-   <a href="releases.html" class="nav-link">Releases</a>
-   Search

The simplest way to get the latest pandoc release is to use the
installer.

<a href="https://github.com/jgm/pandoc/releases/latest" id="downloadInstallerBtn" class="btn btn-primary">Download the latest installer</a>

For alternative ways to install pandoc, see below under the heading for
your operating system.

<a href="#windows" class="anchor"></a>Windows
---------------------------------------------

There is a package installer at pandoc’s [download
page](https://github.com/jgm/pandoc/releases/latest). This will install
pandoc, replacing older versions, and update your path to include the
directory where pandoc’s binaries are installed.

If you prefer not to use the msi installer, we also provide a zip file
that contains pandoc’s binaries and documentation. Simply unzip this
file and move the binaries to a directory of your choice.

Alternatively, you can install pandoc using
[Chocolatey](https://chocolatey.org):

    choco install pandoc

Chocolatey can also install other software that integrates with Pandoc.
For example, to install <span class="nowrap">`rsvg-convert`</span> (from
[librsvg](https://wiki.gnome.org/Projects/LibRsvg), covering formats
without SVG support), [Python](https://www.python.org) (to use Pandoc
filters), and [MiKTeX](https://miktex.org/) (to typeset PDFs with
[LaTeX](https://www.latex-project.org)):

    choco install rsvg-convert python miktex

Or, you can install pandoc using
[winget](https://github.com/microsoft/winget-pkgs):

    winget install --source winget --exact --id JohnMacFarlane.Pandoc

Using multiple installation methods can result in two separate
installations of pandoc; it is recommended to properly uninstall pandoc
before switching to an alternative installation method.

By default, Pandoc creates PDFs using LaTeX. We recommend installing it
via [MiKTeX](https://miktex.org/). With the option <span
class="nowrap">`--pdf-engine`</span>, you however can specify other
programs for this task.

<a href="#macos" class="anchor"></a>macOS
-----------------------------------------

There is a package installer at pandoc’s [download
page](https://github.com/jgm/pandoc/releases/latest). If you later want
to uninstall the package, you can do so by downloading [this
script](https://raw.githubusercontent.com/jgm/pandoc/main/macos/uninstall-pandoc.pl)
and running it with <span
class="nowrap">`perl uninstall-pandoc.pl`</span>.

Alternatively, you can install pandoc using [Homebrew](https://brew.sh):

     brew install pandoc

Homebrew can also install other software that integrates with Pandoc.
For example, to install
[librsvg](https://wiki.gnome.org/Projects/LibRsvg) (its <span
class="nowrap">`rsvg-convert`</span> covers formats without SVG
support), [Python](https://www.python.org) (to use Pandoc filters), and
[BasicTeX](https://www.tug.org/mactex/morepackages.html) (to typeset
PDFs with [LaTeX](https://www.latex-project.org)):

     brew install librsvg python homebrew/cask/basictex

Note: On unsupported versions of macOS (more than three releases old),
Homebrew installs from source, which takes additional time and disk
space for the <span class="nowrap">`ghc`</span> compiler and dependent
Haskell libraries.

We also provide a zip file containing the binaries and man pages, for
those who prefer not to use the installer. Simply unzip the file and
move the binaries and man pages to whatever directory you like.

By default, Pandoc creates PDFs using LaTeX. Because a full
[MacTeX](https://tug.org/mactex/) installation uses four gigabytes of
disk space, we recommend
[BasicTeX](https://www.tug.org/mactex/morepackages.html) or
[TinyTeX](https://yihui.org/tinytex/) and using the <span
class="nowrap">`tlmgr`</span> tool to install additional packages as
needed. If you receive errors warning of fonts not found:

    tlmgr install collection-fontsrecommended

With the option <span class="nowrap">`--pdf-engine`</span>, you however
can specify other programs for this task.

<a href="#linux" class="anchor"></a>Linux
-----------------------------------------

Check whether the pandoc version in your package manager is not
outdated. Pandoc is in the
[Debian](https://packages.debian.org/search?keywords=pandoc),
[Ubuntu](https://packages.ubuntu.com/search?keywords=pandoc),
[Slackware](https://www.slackbuilds.org/result/?search=pandoc&sv=),
[Arch](https://archlinux.org/packages/?q=pandoc),
[Fedora](https://packages.fedoraproject.org/pkgs/pandoc/pandoc/),
[NiXOS](https://search.nixos.org/packages?query=pandoc),
[openSUSE](https://software.opensuse.org/package/pandoc),
[gentoo](https://packages.gentoo.org/package/app-text/pandoc) and
[Void](https://voidlinux.org/packages/?arch=x86_64&q=pandoc)
repositories.

To get the latest release, we provide a binary package for amd64
architecture on the **[download
page](https://github.com/jgm/pandoc/releases/latest)**.

The executable is statically linked and has no dynamic dependencies or
dependencies on external data files. Note: because of the static
linking, the pandoc binary from this package cannot use lua filters that
require external lua modules written in C.

Both a tarball and a deb installer are provided. To install the deb:

    sudo dpkg -i $DEB

where <span class="nowrap">`$DEB`</span> is the path to the downloaded
deb. This will install the <span class="nowrap">`pandoc`</span>
executable and man page.

If you use an RPM-based distro, you may be able to install the deb from
our download page using <span class="nowrap">`alien`</span>.

On any distro, you may install from the tarball into <span
class="nowrap">`$DEST`</span> (say, <span
class="nowrap">`/usr/local/`</span> or <span
class="nowrap">`$HOME/.local`</span>) by doing

    tar xvzf $TGZ --strip-components 1 -C $DEST

where <span class="nowrap">`$TGZ`</span> is the path to the downloaded
zipped tarball. For Pandoc versions before 2.0, which don’t provide a
tarball, try instead

    ar p $DEB data.tar.gz | tar xvz --strip-components 2 -C $DEST

You can also install from source, using the instructions below under
[Compiling from source](#compiling-from-source). Note that most distros
have the Haskell platform in their package repositories. For example, on
Debian/Ubuntu, you can install it with <span
class="nowrap">`apt-get install haskell-platform`</span>.

By default, Pandoc creates PDFs using LaTeX. We recommend installing
[TeX Live](https://www.tug.org/texlive/) via your package manager. (On
Debian/Ubuntu, <span class="nowrap">`apt-get install texlive`</span>.)
With the option <span class="nowrap">`--pdf-engine`</span>, you however
can specify other programs for this task.

<a href="#chrome-os" class="anchor"></a>Chrome OS
-------------------------------------------------

On Chrome OS, pandoc can be installed using the
[chromebrew](https://github.com/skycocker/chromebrew) package manager
with the command:

    crew install pandoc

This will automatically build and configure pandoc for the specific
device you are using.

<a href="#bsd" class="anchor"></a>BSD
-------------------------------------

Pandoc is in the [NetBSD](https://pkgsrc.se/converters/pandoc) and
[FreeBSD ports](https://www.freshports.org/textproc/hs-pandoc/)
repositories.

<a href="#docker" class="anchor"></a>Docker
-------------------------------------------

The official Docker images for pandoc can be found at
<a href="https://github.com/pandoc/dockerfiles" class="uri">https://github.com/pandoc/dockerfiles</a>
and at [dockerhub](https://hub.docker.com/).

The [pandoc/core](https://hub.docker.com/r/pandoc/core) image contains
<span class="nowrap">`pandoc`</span>.

The [pandoc/latex](https://hub.docker.com/r/pandoc/latex) image also
contains the minimal LaTeX installation needed to produce PDFs using
pandoc.

To run pandoc using Docker, converting <span
class="nowrap">`README.md`</span> to <span
class="nowrap">`README.pdf`</span>:

    docker run --rm --volume "`pwd`:/data" --user `id -u`:`id -g` pandoc/latex README.md -o README.pdf

<a href="#github-actions" class="anchor"></a>GitHub Actions
-----------------------------------------------------------

Pandoc can be run through [GitHub
Actions](https://github.com/features/actions). For some examples, see
<a href="https://github.com/pandoc/pandoc-action-example" class="uri">https://github.com/pandoc/pandoc-action-example</a>.

<a href="#gitlab-cicd" class="anchor"></a>GitLab CI/CD
------------------------------------------------------

Pandoc can be run through [GitLab
CI/CD](https://about.gitlab.com/stages-devops-lifecycle/continuous-integration/).
For some examples, see
<a href="https://gitlab.com/pandoc/pandoc-ci-example" class="uri">https://gitlab.com/pandoc/pandoc-ci-example</a>.

<a href="#compiling-from-source" class="anchor"></a>Compiling from source
-------------------------------------------------------------------------

If for some reason a binary package is not available for your platform,
or if you want to hack on pandoc or use a non-released version, you can
install from source.

### <a href="#getting-the-pandoc-source-code" class="anchor"></a>Getting the pandoc source code

Source tarballs can be found at
<a href="https://hackage.haskell.org/package/pandoc" class="uri">https://hackage.haskell.org/package/pandoc</a>.
For example, to fetch the source for version 1.17.0.3:

    wget https://hackage.haskell.org/package/pandoc-1.17.0.3/pandoc-1.17.0.3.tar.gz
    tar xvzf pandoc-1.17.0.3.tar.gz
    cd pandoc-1.17.0.3

Or you can fetch the development code by cloning the repository:

    git clone https://github.com/jgm/pandoc
    cd pandoc

Note: there may be times when the development code is broken or depends
on other libraries which must be installed separately. Unless you really
know what you’re doing, install the last released version.

### <a href="#quick-stack-method" class="anchor"></a>Quick stack method

The easiest way to build pandoc from source is to use
[stack](https://docs.haskellstack.org/en/stable/install_and_upgrade.html):

1.  Install
    [stack](https://docs.haskellstack.org/en/stable/install_and_upgrade.html).
    Note that Pandoc requires stack &gt;= 1.7.0.

2.    stack setup
          stack install pandoc-cli

    <span class="nowrap">`stack setup`</span> will automatically
    download the ghc compiler if you don’t have it. <span
    class="nowrap">`stack install`</span> will install the <span
    class="nowrap">`pandoc`</span> executable into <span
    class="nowrap">`~/.local/bin`</span>, which you should add to your
    <span class="nowrap">`PATH`</span>. This process will take a while,
    and will consume a considerable amount of disk space.

### <a href="#quick-cabal-method" class="anchor"></a>Quick cabal method

1.  Install [ghcup](https://www.haskell.org/ghcup/install/). This will
    give you <span class="nowrap">`ghc`</span> and <span
    class="nowrap">`cabal`</span>.

2.  Update your package database:

        cabal update

3.  Use <span class="nowrap">`cabal`</span> to install pandoc and its
    dependencies:

        cabal install pandoc-cli

    This procedure will install the released version of pandoc, which
    will be downloaded automatically from HackageDB. The <span
    class="nowrap">`pandoc`</span> executable will be placed in <span
    class="nowrap">`$HOME/.cabal/bin`</span> on linux/unix/macOS and in
    <span class="nowrap">`%APPDATA%\cabal\bin`</span> on Windows. Make
    sure this directory is in your path.

    If you want to install a modified or development version of pandoc
    instead, switch to the source directory before running the above
    command – cabal will use the local code for all projects mentioned
    in the <span class="nowrap">`cabal.project`</span>.

4.  You should now be able to run <span class="nowrap">`pandoc`</span>:

        pandoc --help

5.  Cabal does not install the <span class="nowrap">`pandoc.1`</span>
    man page, but you can copy it from the <span
    class="nowrap">`man/`</span> directory of the source code to <span
    class="nowrap">`/usr/local/share/man/man1/`</span> or wherever man
    pages go on your system.

### <a href="#custom-cabal-method" class="anchor"></a>Custom cabal method

This is a step-by-step procedure that offers maximal control over the
build and installation. Most users should use the quick install, but
this information may be of use to packagers. For more details, see the
[Cabal User’s Guide](https://cabal.readthedocs.io/). These instructions
assume that the pandoc source directory is your working directory. You
will need cabal version 2.0 or higher.

1.  Install dependencies: in addition to the [Haskell
    platform](https://hackage.haskell.org/platform/), you will need a
    number of additional libraries. You can install them all with

        cabal update
        cabal install --only-dependencies

2.  Configure:

        cabal configure --prefix=DIR --bindir=DIR --libdir=DIR \
          --datadir=DIR --libsubdir=DIR --datasubdir=DIR --docdir=DIR \
          --htmldir=DIR --program-prefix=PREFIX --program-suffix=SUFFIX \
          --mandir=DIR --flags=FLAGSPEC --enable-tests

    All of the options have sensible defaults that can be overridden as
    needed.

    <span class="nowrap">`FLAGSPEC`</span> is a list of Cabal
    configuration flags, optionally preceded by a <span
    class="nowrap">`-`</span> (to force the flag to <span
    class="nowrap">`false`</span>), and separated by spaces. <span
    class="nowrap">`pandoc`</span>’s flags include:

    -   <span class="nowrap">`embed_data_files`</span>: embed all data
        files into the binary (default no). This is helpful if you want
        to create a relocatable binary.

    <span class="nowrap">`pandoc-cli`</span>’s flags include:

    -   <span class="nowrap">`lua`</span>: compile in support for Lua
        filters and custom writers.

    -   <span class="nowrap">`server`</span>: compile in support for
        running in HTTP server mode when the executable is renamed (or
        symlinked as) <span class="nowrap">`pandoc-server`</span>.

3.  Build:

        cabal build
        cabal test

4.  Build API documentation:

        cabal haddock --html-location=URL --hyperlink-source

### <a href="#creating-a-relocatable-binary" class="anchor"></a>Creating a relocatable binary

It is possible to compile pandoc such that the data files pandoc uses
are embedded in the binary. The resulting binary can be run from any
directory and is completely self-contained. With cabal, add <span
class="nowrap">`-fembed_data_files`</span> to the <span
class="nowrap">`cabal configure`</span> or <span
class="nowrap">`cabal install`</span> commands.

With stack, use <span
class="nowrap">`--flag pandoc:embed_data_files`</span>.

### <a href="#running-tests" class="anchor"></a>Running tests

Pandoc comes with an automated test suite. To run with cabal, <span
class="nowrap">`cabal test`</span>; to run with stack, <span
class="nowrap">`stack test`</span>.

To run particular tests (pattern-matching on their names), use the <span
class="nowrap">`-p`</span> option:

    cabal test --test-options='-p markdown'

Or with stack:

    stack test --test-arguments='-p markdown'

It is often helpful to add <span class="nowrap">`-j4`</span> (run tests
in parallel) and <span class="nowrap">`--hide-successes`</span> (don’t
clutter output with successes) to the test arguments as well.

If you add a new feature to pandoc, please add tests as well, following
the pattern of the existing tests. The test suite code is in <span
class="nowrap">`test/test-pandoc.hs`</span>. If you are adding a new
reader or writer, it is probably easiest to add some data files to the
<span class="nowrap">`test`</span> directory, and modify <span
class="nowrap">`test/Tests/Old.hs`</span>. Otherwise, it is better to
modify the module under the <span class="nowrap">`test/Tests`</span>
hierarchy corresponding to the pandoc module you are changing.

### <a href="#running-benchmarks" class="anchor"></a>Running benchmarks

To build and run the benchmarks:

    cabal configure --enable-benchmarks && cabal build
    cabal bench

or with stack:

    stack bench

To use a smaller sample size so the benchmarks run faster:

    cabal bench --benchmark-options='-s 20'

To run just the markdown benchmarks:

    cabal bench --benchmark-options='markdown'

-   <a href="#windows" id="toc-windows">Windows</a>
-   <a href="#macos" id="toc-macos">macOS</a>
-   <a href="#linux" id="toc-linux">Linux</a>
-   <a href="#chrome-os" id="toc-chrome-os">Chrome OS</a>
-   <a href="#bsd" id="toc-bsd">BSD</a>
-   <a href="#docker" id="toc-docker">Docker</a>
-   <a href="#github-actions" id="toc-github-actions">GitHub Actions</a>
-   <a href="#gitlab-cicd" id="toc-gitlab-cicd">GitLab CI/CD</a>
-   <a href="#compiling-from-source" id="toc-compiling-from-source">Compiling from source</a>
    -   <a href="#getting-the-pandoc-source-code" id="toc-getting-the-pandoc-source-code">Getting the pandoc source code</a>
    -   <a href="#quick-stack-method" id="toc-quick-stack-method">Quick stack method</a>
    -   <a href="#quick-cabal-method" id="toc-quick-cabal-method">Quick cabal method</a>
    -   <a href="#custom-cabal-method" id="toc-custom-cabal-method">Custom cabal method</a>
    -   <a href="#creating-a-relocatable-binary" id="toc-creating-a-relocatable-binary">Creating a relocatable binary</a>
    -   <a href="#running-tests" id="toc-running-tests">Running tests</a>
    -   <a href="#running-benchmarks" id="toc-running-benchmarks">Running benchmarks</a>

<span aria-hidden="true">×</span>

<span class="modal-title">Search results</span>
