# rmdepcheck

rmdepcheck is an RPM dependency check tool based on a repository metadata modification approach.
It works by comparing a checked repository to one or more base repositories. First, checks are run
on the base repositories as-is. Next, modified copies of the base repositories' metadata is
created, with all packages from the same source RPM(s) as the package(s) in the checked
repositories removed. Finally, checks are run again on the modified base repositories, with the
checked repositories available to the dependency solver. The results of the two runs are compared.
New failures should indicate problems introduced by the checked repositories. Also, some relevant
checks are run on the checked repositories with reference to the modified base repositories.

Optionally, additional base repositories can be specified which will not be modified, and
additional new repositories can be specified which will not be checked directly. The former is
intended for testing scenarios like stable Fedora releases, which have a frozen release repository
which is never modified, and an updates repository which is updated. The latter is intended for
multilib scenarios; it may be desirable to use such an additional repository for packages for
the multilib arch(es), if e.g. installability of these should not be tested directly.

An alternative mode allows simply testing the consequences of *removing* a list of source packages
entirely; in this mode, in the second step, the base repository's metadata is modified to entirely
remove all binary packages built from the specified source packages. The installability check is
skipped in this context.

## Requirements

rmdepcheck has no run-time Python dependencies outside the standard library. However, it requires
several command-line utilities:

* dnf
* zstd
* curl

It checks for these, and will exit early with an error if any of them is not found. rmdepcheck
is written primarily for Red Hat-family distributions, but should in theory be usable anywhere
these utilities can be installed (and forward slashes act as directory separators).

## Installation

Installation of rmdepcheck is entirely optional, it can be run just as well directly from the
repository. Otherwise, rmdepcheck uses setuptools for installation and is PEP 518-compliant. You
can build and install with e.g. the `build` module and `pip`. rmdepcheck can also be installed
directly from PyPI with pip and other tools.

## Usage

Simple usage looks like this:
```
rmdepcheck https://a.base.repo.example/repo,file:///another/baserepo file:///the/testedrepo
```

The to-be-modified base repositories are specified as a comma-separated list. Repositories are
always specified as URLs. Only file:// , http:// and https:// URLs are accepted.

For the alternative 'removal' mode, usage looks like:
```
rmdepcheck --removes https://a.base.repo.example/repo,file:///another/baserepo sourcepkg1,sourcepkg2
```

This tests removing all binary packages built from sourcepkg1 or sourcepkg2 from the base
repositories.

For more complex usage, see `rmdepcheck --help`.

Note rmdepcheck is really only intended for use as a script, not as an importable library. If you
want to use it as a library go ahead, but this isn't a supported use case and bugs in it may not
be addressed.

## License

rmdepcheck is released under the [GPL](https://www.gnu.org/licenses/gpl.txt), version 3 or later.
See `COPYING` and the header of `rmdepcheck.py` itself.

## Contributing

Issues and pull requests can be filed in [Codeberg](https://codeberg.org/AdamWill/rmdepcheck).
Pull requests must be signed off (use the `-s` git argument). By signing off
your pull request you are agreeing to the
[Developer's Certificate of Origin](http://developercertificate.org/):

    Developer's Certificate of Origin 1.1

    By making a contribution to this project, I certify that:

    (a) The contribution was created in whole or in part by me and I
        have the right to submit it under the open source license
        indicated in the file; or

    (b) The contribution is based upon previous work that, to the best
        of my knowledge, is covered under an appropriate open source
        license and I have the right under that license to submit that
        work with modifications, whether created in whole or in part
        by me, under the same open source license (unless I am
        permitted to submit under a different license), as indicated
        in the file; or

    (c) The contribution was provided directly to me by some other
        person who certified (a), (b) or (c) and I have not modified
        it.

    (d) I understand and agree that this project and the contribution
        are public and that a record of the contribution (including all
        personal information I submit with it, including my sign-off) is
        maintained indefinitely and may be redistributed consistent with
        this project or the open source license(s) involved.
