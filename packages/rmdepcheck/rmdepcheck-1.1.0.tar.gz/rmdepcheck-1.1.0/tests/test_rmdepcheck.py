# Copyright Red Hat
#
# This file is part of rmdepcheck.
#
# rmdepcheck is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Adam Williamson <awilliam@redhat.com>

# Unit tests don't always need docstrings.
# pylint: disable=missing-function-docstring

"""Tests for rmdepcheck."""

import os
import shutil
import sys
import tempfile
import xml.etree.ElementTree as et
from unittest import mock

import pytest
import rmdepcheck

HERE = os.path.abspath(os.path.dirname(__file__))
TESTDATA = f"{HERE}/testdata"
REPOS = f"{TESTDATA}/repos"


def test_mfind():
    repomdtree = et.parse(f"{REPOS}/base/repodata/repomd.xml")
    # test_get_primary and various others test the success path, so
    # we'll just test failure, which shouldn't ever really happen
    assert repomdtree.find("foobar", {}) is None
    with pytest.raises(ValueError):
        rmdepcheck.mfind(repomdtree, "foobar", {})


def test_parse_repoclosure():
    with open(f"{TESTDATA}/test_parse_repoclosure.txt", "r", encoding="utf-8") as fh:
        rctext = fh.read()
    assert rmdepcheck.parse_repoclosure(rctext) == [
        ("python3-wxnatpy-0.4.0-13.fc42.noarch", "baserepo0", "python(abi) = 3.13"),
        ("python3-wxnatpy-0.4.0-13.fc42.noarch", "baserepo0", "python3.13dist(wxpython) >= 4"),
        ("python3-wxnatpy-0.4.0-13.fc42.noarch", "baserepo0", "python3.13dist(xnat) >= 0.3.3"),
        ("python3-x3dh-1.0.4-3.fc43.noarch", "baserepo1", "python3.14dist(pydantic) >= 1.7.4"),
    ]


def test_format_rc_errors(capsys):
    errs = [
        ("python3-wxnatpy-0.4.0-13.fc42.noarch", "baserepo0", "python(abi) = 3.13"),
        ("python3-wxnatpy-0.4.0-13.fc42.noarch", "baserepo0", "python3.13dist(wxpython) >= 4"),
        ("python3-wxnatpy-0.4.0-13.fc42.noarch", "baserepo0", "python3.13dist(xnat) >= 0.3.3"),
        ("python3-x3dh-1.0.4-3.fc43.noarch", "baserepo1", "python3.14dist(pydantic) >= 1.7.4"),
    ]
    rmdepcheck.format_rc_errors(errs)
    captured = capsys.readouterr()
    with open(f"{TESTDATA}/test_format_rc_errors.txt", "r", encoding="utf-8") as fh:
        exptext = fh.read()
    assert captured.out == exptext


def test_get_file():
    with tempfile.TemporaryDirectory() as tempdir:
        testfile = f"file://{HERE}/test_rmdepcheck.py"
        rmdepcheck.get_file(testfile, f"{tempdir}/test_rmdepcheck.py")
        with open(f"{tempdir}/test_rmdepcheck.py", "r", encoding="utf-8") as testfh:
            assert "This file is" in testfh.read()


def test_get_download_primary():
    repomdtree = et.parse(f"{REPOS}/base/repodata/repomd.xml")
    repomdroot = repomdtree.getroot()
    primary = rmdepcheck.get_primary(repomdroot)
    assert isinstance(primary, et.Element)
    assert primary.attrib == {"type": "primary"}
    with tempfile.TemporaryDirectory() as tempdir:
        os.makedirs(f"{tempdir}/repodata")
        rmdepcheck.download_primary(primary, f"file://{REPOS}/base", tempdir)
        # NOTE: this filename changes any time mkrepos.py is run
        assert os.path.exists(
            # pylint: disable-next=line-too-long
            f"{tempdir}/repodata/0e38861f6ebd9d0808917661ecdb6db855222b294611209cf801664f900c9779-primary.xml"
        )


def test_replace_primary():
    with tempfile.TemporaryDirectory() as tempdir:
        shutil.copy2(
            # this is an old version of base's primary file
            f"{TESTDATA}/test_replace_primary.xml",
            f"{tempdir}/test.xml",
        )
        ret = rmdepcheck.replace_primary(f"{tempdir}/test.xml", "ccc")
        print(tempdir)
        assert ret == (
            "42daebf05f6c3cabe9d029acb3a8056f7fc533cde9820b7388d90acb1f6e7dbe",
            1067,
            "562981a96ba946cd0f993d180108c4dd107d1a5f24210c5768b19cdd93e8f33a",
            7531,
        )
        assert os.path.exists(
            # pylint: disable-next=line-too-long
            f"{tempdir}/42daebf05f6c3cabe9d029acb3a8056f7fc533cde9820b7388d90acb1f6e7dbe-primary.xml.zst"
        )


def test_get_base_repoclosure():
    repo = f"file://{REPOS}/base"
    with open(f"{TESTDATA}/test_get_base_repoclosure.txt", "r", encoding="utf-8") as testfh:
        expected = testfh.read()
        expected = expected.replace("{HASH}", rmdepcheck.hash_repo(repo))
    ret = rmdepcheck.get_base_repoclosure([repo], [])
    assert ret == expected


def test_get_modified_repoclosure():
    brepo = f"file://{REPOS}/base"
    with open(f"{TESTDATA}/test_get_modified_repoclosure.txt", "r", encoding="utf-8") as testfh:
        expected = testfh.read()
        expected = expected.replace("{HASH}", rmdepcheck.hash_repo(brepo))
    ret = rmdepcheck.get_modified_repoclosure(
        [brepo], [], [f"file://{REPOS}/new"], ["aaa", "ccc", "eee", "fff", "ggg"]
    )
    assert ret == expected


def test_get_new_repoclosure():
    nrepo = f"file://{REPOS}/new"
    with open(f"{TESTDATA}/test_get_new_repoclosure.txt", "r", encoding="utf-8") as testfh:
        expected = testfh.read()
        expected = expected.replace("{HASH}", rmdepcheck.hash_repo(nrepo))
    ret = rmdepcheck.get_new_repoclosure([f"file://{REPOS}/base"], nrepo)
    assert ret == expected


def test_get_source_packages():
    sources = rmdepcheck.get_source_packages([f"file://{REPOS}/new"])
    assert sources == {"111", "aaa", "ccc", "eee", "fff", "ggg"}


def test_url_check():
    rmdepcheck.url_check("file:///foo/bar")
    rmdepcheck.url_check("https://www.some.where")
    rmdepcheck.url_check("http://some.where.insecure")
    with pytest.raises(ValueError):
        rmdepcheck.url_check("ftp://1997.called")
    with pytest.raises(ValueError):
        rmdepcheck.url_check("whatisthis")


def test_comma_url():
    assert rmdepcheck.comma_url("https://www.some.where") == ["https://www.some.where"]
    assert rmdepcheck.comma_url("https://www.some.where,file:///foo/bar") == [
        "https://www.some.where",
        "file:///foo/bar",
    ]
    with pytest.raises(ValueError):
        rmdepcheck.comma_url("https://www.some.where,ftp://1997.called")
    with pytest.raises(ValueError):
        rmdepcheck.comma_url("ftp://1997.called")
    with pytest.raises(ValueError):
        rmdepcheck.comma_url("https://www.some.where,whatisthis")


def test_comma_list():
    assert rmdepcheck.comma_list("foo,bar") == ["foo", "bar"]
    assert rmdepcheck.comma_list("") == []


@mock.patch("subprocess.run", autospec=True)
def test_check_utils(mock_run):
    rmdepcheck.check_utils()
    mock_run.side_effect = [FileNotFoundError, None, FileNotFoundError]
    with pytest.raises(SystemExit) as excinfo:
        rmdepcheck.check_utils()
    assert excinfo.value.code == "Please install missing required utilities: zstd curl"


@mock.patch("rmdepcheck.check_utils", side_effect=KeyboardInterrupt)
def test_ctrl_c(_, capsys):
    with pytest.raises(SystemExit) as excinfo:
        rmdepcheck.main()
    assert excinfo.value.code == 1
    captured = capsys.readouterr()
    assert captured.err == "Interrupted, exiting...\n"


def test_e2e_null(capsys):
    """End-to-end test using an empty repository, to test what happens
    when no changes are found.
    """
    sys.argv = ["rmdepcheck.py", f"file://{REPOS}/base", f"file://{REPOS}/empty"]
    with pytest.raises(SystemExit) as excinfo:
        rmdepcheck.main()
    assert excinfo.value.code == 0
    captured = capsys.readouterr()
    assert captured.out == ""


@pytest.mark.parametrize("output", ("human", "json", "onlyerrors"))
def test_e2e_devel(output, capsys):
    """End-to-end test similar to a Rawhide or Branched case, with
    a single modified base repo and a single check repo. Also tests
    JSON output.
    """
    sys.argv = ["rmdepcheck.py", f"file://{REPOS}/base", f"file://{REPOS}/new"]
    if output == "json":
        sys.argv.insert(1, "--json")
    if output == "onlyerrors":
        sys.argv.insert(1, "--onlyerrors")
    with pytest.raises(SystemExit) as excinfo:
        rmdepcheck.main()
    assert excinfo.value.code == 3
    captured = capsys.readouterr()
    if output == "human":
        fname = "test_e2e_devel.txt"
    elif output == "onlyerrors":
        fname = "test_e2e_devel_onlyerrors.txt"
    else:
        fname = "test_e2e_devel_json.txt"
    with open(f"{TESTDATA}/{fname}", "r", encoding="utf-8") as fh:
        exptext = fh.read()
        exptext = exptext.replace("{REPOS}", REPOS)
    assert captured.out == exptext


def test_e2e_updates(capsys):
    """End-to-end test similar to a stable Fedora release, with one
    non-modified 'frozen' base repo and one modified updates repo.
    """
    sys.argv = [
        "rmdepcheck.py",
        "--nmbaserepos",
        f"file://{REPOS}/base",
        f"file://{REPOS}/updates",
        f"file://{REPOS}/new",
    ]
    with pytest.raises(SystemExit) as excinfo:
        rmdepcheck.main()
    assert excinfo.value.code == 3
    captured = capsys.readouterr()
    with open(f"{TESTDATA}/test_e2e_updates.txt", "r", encoding="utf-8") as fh:
        exptext = fh.read()
        exptext = exptext.replace("{REPOS}", REPOS)
    assert captured.out == exptext


def test_e2e_removes(capsys):
    """End-to-end test of the alternate --removes mode."""
    sys.argv = ["rmdepcheck.py", "--removes", f"file://{REPOS}/base", "aaa,eee"]
    with pytest.raises(SystemExit) as excinfo:
        rmdepcheck.main()
    assert excinfo.value.code == 1
    captured = capsys.readouterr()
    with open(f"{TESTDATA}/test_e2e_removes.txt", "r", encoding="utf-8") as fh:
        exptext = fh.read()
        exptext = exptext.replace("{REPOS}", REPOS)
    assert captured.out == exptext
