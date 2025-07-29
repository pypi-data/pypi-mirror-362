#!/usr/bin/python3

# Copyright Red Hat
#
# This file is part of rmdepcheck.
#
# rmdepcheck is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author(s): Adam Williamson <awilliam@redhat.com>

"""RPM package installability and reverse-dependency checks using a
repository modification strategy (hence 'rm').
"""

# Standard libraries

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as et

from functools import partial
from typing import Iterable
from urllib.parse import urlparse

CURLARGS = ("curl", "-s", "--retry-delay", "10", "--max-time", "300", "--retry", "5")
# use a fresh temporary cache for each run to avoid collisions between
# runs and polluting the 'real' cache
# pylint: disable-next=consider-using-with
DNFTEMP = tempfile.TemporaryDirectory(prefix="rmdepcheck", dir="/var/tmp")
DNFARGS = ["dnf", "--setopt", f"cachedir={DNFTEMP.name}", "-q", "--disablerepo=*"]
XMLNS = {
    "repo": "http://linux.duke.edu/metadata/repo",
    "common": "http://linux.duke.edu/metadata/common",
    "rpm": "http://linux.duke.edu/metadata/rpm",
}
SUBPCAPTURE = partial(subprocess.run, capture_output=True, text=True, check=False)
SUBPCAPTCHECK = partial(subprocess.run, capture_output=True, text=True, check=True)
SUBPCHECK = partial(subprocess.run, check=True)
REPOHASHES = {}


def mfind(element: et.Element, string: str, ns: dict) -> et.Element:
    """Wrapper for element.find which raises an error if it comes back
    with None.
    """
    ret = element.find(string, ns)
    if ret is not None:
        return ret
    raise ValueError("Cannot find required element!")


def hash_repo(repo: str) -> str:
    """Generate a hash for the repo name, stash it in a dict so we can
    map back out later, and return it. This is so we can show the repo
    URLs in our final output, as opposed to non-useful made-up repo
    names. Not security sensitive.
    """
    gothash = hashlib.sha256(repo.encode(encoding="utf-8")).hexdigest()[:8]
    REPOHASHES[gothash] = repo
    return gothash


def parse_repoclosure(rc: str) -> list[tuple[str, str, str]]:
    """Given some `dnf repoclosure` output, parse it into a list of
    3-tuples each containing a package name, a repo URL (or generated
    repo name if we can't look up the hash, should only happen in
    tests) and an unresolved dependency for that package.
    """
    out = []
    pkg = None
    for line in rc.splitlines():
        if line.strip().startswith("package:"):
            # package, repo
            elems = line.split()
            pkg = (elems[1], REPOHASHES.get(elems[3], elems[3]))
            continue
        if line.strip().startswith("unresolved deps (") or line.strip().startswith("Error:"):
            continue
        # anything else is an unresolved dep
        # repoclosure doesn't handle rich deps with 'if' conditions
        if line.strip().startswith("(") and " if " in line:
            continue
        if pkg:
            out.append(pkg + (line.strip(),))
    return out


def format_rc_errors(errors: list[tuple[str, str, str]]) -> None:
    """Format and print parse_repoclosure-style tuples for humans to
    read. Used for final output after we do some diffing on the lists
    of tuples.
    """
    pkg = ("", "")
    for error in errors:
        if error[:2] != pkg:
            pkg = error[:2]
            print(f"package: {error[0]} from {error[1]}")
        print(f"  {error[2]}")


def get_file(src: str, dest: str) -> None:
    """Just downloads a file from src to dest."""
    SUBPCHECK(CURLARGS + ("-o", dest, src))


def get_primary(repomdroot: et.Element) -> et.Element:
    """Given a repomd.xml root element, return the element for the
    primary data file.
    """
    return mfind(repomdroot, "repo:data[@type='primary']", XMLNS)


def download_primary(primary: et.Element, repourl: str, mrepodir: str) -> str:
    """Given the ET element with information about it, and the URL of
    the repo to download from and the local directory to download to,
    download and uncompress the primary data file, returning
    the filename. Note mrepodir/repodata is assumed to exist.
    """
    primloc = mfind(primary, "repo:location", XMLNS).attrib["href"]
    encprimfn = f"{mrepodir}/{primloc}"
    get_file(f"{repourl}/{primloc}", encprimfn)
    SUBPCHECK(("unzstd", "-q", encprimfn))
    os.remove(encprimfn)
    return encprimfn.replace(".zst", "")


def replace_primary(primfn: str, removes: Iterable[str]) -> tuple[str, int, str, int]:
    """Parse the primary data file, remove any packages whose source
    package name matches one in removes, and write out a new file
    with the correct name (containing its own sha256sum). Return the
    checksums and sizes of the new uncompressed and compressed files,
    for writing back into the repomd.
    """
    rddir = os.path.dirname(primfn)
    et.register_namespace("", "http://linux.duke.edu/metadata/common")
    et.register_namespace("rpm", "http://linux.duke.edu/metadata/rpm")
    primtree = et.parse(primfn)
    primroot = primtree.getroot()
    for pkg in primroot.findall("common:package", XMLNS):
        srpm = mfind(mfind(pkg, "common:format", XMLNS), "rpm:sourcerpm", XMLNS).text
        if srpm and srpm.rsplit("-", 2)[0] in removes:
            primroot.remove(pkg)

    tempfn = f"{rddir}/primtemp.xml"
    primtree.write(tempfn)
    with open(tempfn, "rb") as tempfh:
        opensum = hashlib.sha256(tempfh.read()).hexdigest()
    opensize = os.path.getsize(tempfn)
    SUBPCHECK(("zstd", "-q", tempfn))
    with open(f"{tempfn}.zst", "rb") as tempfhz:
        csum = hashlib.sha256(tempfhz.read()).hexdigest()
    size = os.path.getsize(f"{tempfn}.zst")
    os.rename(f"{tempfn}.zst", f"{rddir}/{csum}-primary.xml.zst")
    os.remove(tempfn)
    os.remove(primfn)
    return (csum, size, opensum, opensize)


def get_base_repoclosure(baserepos: Iterable[str], nmbaserepos: Iterable[str]) -> str:
    """Gets the reference repoclosure text. Both to-be-modified and
    not-modified base repos are available to the solver, but only the
    to-be-modified repos are checked.
    """
    cmdargs = DNFARGS + ["repoclosure"]
    for repo in list(baserepos) + list(nmbaserepos):
        cmdargs.extend(["--repofrompath", f"{hash_repo(repo)},{repo}"])
    cmdargs.append("--check")
    # only check the repos that will be modified
    cmdargs.append(",".join([hash_repo(baserepo) for baserepo in baserepos]))
    return SUBPCAPTURE(cmdargs).stdout


# pylint: disable-next=too-many-locals
def get_modified_repoclosure(
    mrepos: Iterable[str], nmrepos: Iterable[str], nrepos: Iterable[str], removes: Iterable[str]
) -> str:
    """Does the repository metadata modification (the clever bit!) and
    returns the modified repoclosure text. Non-modified base repos,
    modified base repos after modification, and the new repo are
    available to the solver; only modified base repos are checked.
    """
    args = DNFARGS + ["repoclosure"]
    # place to stash the modified repos
    with tempfile.TemporaryDirectory() as mreposdir:
        for mrepo in mrepos:
            mrepodir = f"{mreposdir}/{hash_repo(mrepo)}"
            os.makedirs(f"{mrepodir}/repodata")
            repomdfn = f"{mrepodir}/repodata/repomd.xml"
            get_file(f"{mrepo}/repodata/repomd.xml", repomdfn)
            et.register_namespace("", "http://linux.duke.edu/metadata/repo")
            repomdtree = et.parse(repomdfn)
            repomdroot = repomdtree.getroot()
            primary = get_primary(repomdroot)
            primfn = download_primary(primary, mrepo, mrepodir)
            (csum, size, opensum, opensize) = replace_primary(primfn, removes)

            # modify the repomd
            mfind(primary, "repo:checksum", XMLNS).text = csum
            mfind(primary, "repo:size", XMLNS).text = str(size)
            mfind(primary, "repo:open-checksum", XMLNS).text = opensum
            mfind(primary, "repo:open-size", XMLNS).text = str(opensize)
            mfind(primary, "repo:location", XMLNS).attrib[
                "href"
            ] = f"repodata/{csum}-primary.xml.zst"
            # requires Python 3.10:
            # notprimary = repomdroot.findall("repo:data[@type]", XMLNS)
            alldata = repomdroot.findall("repo:data[@type]", XMLNS)
            notprimary = [data for data in alldata if data is not primary]
            for item in notprimary:
                repomdroot.remove(item)
            et.register_namespace("", "http://linux.duke.edu/metadata/repo")
            repomdtree.write(repomdfn)
            # add the modified repo to the repoclosure command
            args.extend(["--repofrompath", f"{hash_repo(mrepo)},{mrepodir}"])

        # now add the non-modified base repos
        for nmrepo in nmrepos:
            args.extend(["--repofrompath", f"{hash_repo(nmrepo)},{nmrepo}"])

        # now add the new package repos
        for nrepo in nrepos:
            args.extend(["--repofrompath", f"{hash_repo(nrepo)},{nrepo}"])

        # finally, add the check arg
        args.append("--check")
        args.append(",".join([hash_repo(mrepo) for mrepo in mrepos]))

        ret = SUBPCAPTURE(args).stdout
    return ret


def get_new_repoclosure(baserepos: Iterable[str], nrepo: str) -> str:
    """Gets and returns repoclosure text for the new repository; this
    is effectively an installability check. All base repos are
    available to the solver but are not checked. Note this is run
    *after* repo modification, so the check runs against the modified
    versions of the modifiable base repositories.
    """
    cmdargs = DNFARGS + ["repoclosure"]
    for repo in baserepos:
        cmdargs.extend(["--repofrompath", f"{hash_repo(repo)},{repo}"])
    cmdargs.extend(["--repofrompath", f"{hash_repo(nrepo)},{nrepo}", "--check", hash_repo(nrepo)])
    return SUBPCAPTURE(cmdargs).stdout


def get_source_packages(repos: Iterable[str]) -> set[str]:
    """Finds and returns the source package names for all packages in
    the repositories specified, as a set.
    """
    args = list(DNFARGS)
    for repo in repos:
        args.extend(["--repofrompath", f"{hash_repo(repo)},{repo}"])
    args.extend(["repoquery", "--qf", "%{sourcerpm} "])
    srpms = SUBPCAPTCHECK(args).stdout.split()
    return {srpm.rsplit("-", 2)[0] for srpm in srpms}


def url_check(arg: str) -> str:
    """Check arg is a file, http or https URL."""
    parsed = urlparse(arg)
    if parsed.scheme in ("http", "https", "file"):
        return arg
    if parsed.scheme:
        raise ValueError(f"Unsupported URL scheme {parsed.scheme} in {arg}")
    raise ValueError(f"No URL scheme in {arg}")


def comma_url(arg: str) -> list[str]:
    """Check arg is a comma-separated list of URLs and return them
    all as a list. If arg is the empty string, return empty list.
    """
    if arg == "":
        return []
    split = arg.split(",")
    for item in split:
        try:
            url_check(item)
        except ValueError as err:
            newerr = str(err) + f"from {arg}"
            raise ValueError(newerr) from err
    return split


def comma_list(arg: str) -> list[str]:
    """Handle a comma-separated list, return as a list."""
    if arg == "":
        return []
    return arg.split(",")


def parse_args() -> argparse.Namespace:
    """Parse arguments with argparse."""
    parser = argparse.ArgumentParser(
        description=("Reverse dependency check implemented as a repoclosure diff.")
    )
    parser.add_argument(
        "--addrepos",
        type=comma_url,
        default="",
        help="The URL(s) of additional repositories containing new packages to be tested "
        "(comma-separated). This is mainly intended for multilib cases: i.e. for testing "
        "x86_64 package sets it should contain the matching i686 packages. It will be "
        "available to the repoclosure check, but will be ignored by the installability check",
    )
    parser.add_argument(
        "--nmbaserepos",
        type=comma_url,
        default="",
        help="The URL(s) of non-modified base repositories to compare against (comma-separated). "
        "These repositories *will not* be modified as part of testing. They should be repositories "
        "whose packages would *not* be replaced with those from the new package repo(s) - e.g. "
        "the frozen release repository for a stable release, which is never changed",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON rather than human-readable format",
    )
    parser.add_argument(
        "--onlyerrors",
        action="store_true",
        help="Only print messages about problems caused, not about things that would be fixed",
    )
    parser.add_argument(
        "--removes",
        action="store_true",
        help="Alternative mode: test removal (only) of all binary packages in the baserepos built "
        "from the source package(s) specified as the final argument (a comma-separated list)",
    )
    parser.add_argument(
        "baserepos",
        type=comma_url,
        help="The URL(s) of base repositories to compare against (comma-separated). "
        "These repositories *will* be modified as part of testing. They should be "
        "repositories whose packages would be replaced with those from the new package "
        "repo(s) - e.g. the main repository for a development release, or the updates repository "
        "for a stable release",
    )
    # I wanted to do this with parse_known_args, but it messes up --help. aw
    if "--removes" in sys.argv:
        parser.add_argument(
            "removes",
            type=comma_list,
            help="A comma-separated list of source packages to test the removal of",
        )
    else:
        parser.add_argument(
            "repo",
            metavar="repo_or_removes",
            type=url_check,
            help="The URL of the repo containing the main set of new packages to be tested, "
            "or a comma-separated list of source packages to test the removal of (if --removes "
            "is passed)",
        )
    args = parser.parse_args()
    if args.removes:
        args.repo = ""
    else:
        args.removes = ""
    return args


def check_utils() -> None:
    """Check required utilities are installed."""
    missing = []
    for prog in (("zstd", "-V"), ("dnf", "--version"), ("curl", "-V")):
        try:
            subprocess.run(prog, stdout=subprocess.DEVNULL, check=True)
        except FileNotFoundError:
            missing.append(prog[0])
    if missing:
        sys.exit("Please install missing required utilities: " + " ".join(missing))


def main() -> None:
    """Main loop."""
    try:
        check_utils()
        exitcode = 0
        args = parse_args()
        if args.removes:
            nrepos = []
            sources = args.removes
            iut = "the specified source package removals"
        else:
            nrepos = [args.repo] + args.addrepos
            # find source package(s) of our tested repo(s)
            # whether to include addrepos is arguable, but should usually be moot
            sources = get_source_packages(nrepos)
            iut = "the tested packages"

        baserc = parse_repoclosure(get_base_repoclosure(args.baserepos, args.nmbaserepos))

        # get the modified rpmclosure output
        modrc = parse_repoclosure(
            get_modified_repoclosure(args.baserepos, args.nmbaserepos, nrepos, sources)
        )

        # figure out the diffs
        newerrors = [dep for dep in modrc if dep not in baserc]
        fixederrors = [dep for dep in baserc if dep not in modrc]
        newrc = []
        if args.repo:
            # get repoclosure on new repo - this is an installability test
            newrc = parse_repoclosure(
                get_new_repoclosure(args.baserepos + args.nmbaserepos, args.repo)
            )

        # output
        if args.json:
            jsonout = {}
        if newerrors:
            if args.json:
                jsonout["newerrors"] = [list(err) for err in newerrors]
            else:
                print(f"Dependencies of other packages that would be BROKEN by {iut}:")
                format_rc_errors(newerrors)
            exitcode += 1
        if newrc:
            if args.json:
                jsonout["installability"] = [list(err) for err in newrc]
            else:
                print("")
                print("Dependency problems in the tested packages themselves:")
                format_rc_errors(newrc)
            exitcode += 2
        if fixederrors:
            if args.json:
                jsonout["fixederrors"] = [list(err) for err in fixederrors]
            elif not args.onlyerrors:
                print("")
                print(f"Dependencies of other packages that would be FIXED by {iut}:")
                format_rc_errors(fixederrors)
        if args.json:
            json.dump(jsonout, sys.stdout, indent=4)
            sys.stdout.write("\n")

        sys.exit(exitcode)

    except KeyboardInterrupt:
        sys.stderr.write("Interrupted, exiting...\n")
        sys.exit(1)


if __name__ == "__main__":  # pragma: no cover
    main()

# vim: set textwidth=100 ts=8 et sw=4:
