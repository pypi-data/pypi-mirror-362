#!/usr/bin/env python3

# Copyright Red Hat
#
# This script is free software; you can redistribute it and/or modify
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

"""Script to create test packages and repos for rpdepcheck testing."""

import os
import shutil

import rpmfluff
import rpmfluff.yumrepobuild

# base packages, used in both the 'base' and 'stable' repos
pkgaaa = rpmfluff.SimpleRpmBuild("aaa", "1.0", "1", ["x86_64"])
pkgbbb = rpmfluff.SimpleRpmBuild("bbb", "1.0", "1", ["x86_64"])
pkgccc = rpmfluff.SimpleRpmBuild("ccc", "1.0", "1", ["x86_64"])
pkgddd = rpmfluff.SimpleRpmBuild("ddd", "1.0", "1", ["x86_64"])
pkgeee = rpmfluff.SimpleRpmBuild("eee", "1.0", "1", ["x86_64"])
pkgfff = rpmfluff.SimpleRpmBuild("fff", "1.0", "1", ["x86_64"])
pkgggg = rpmfluff.SimpleRpmBuild("ggg", "1.0", "1", ["x86_64", "i686"])
pkghhx = rpmfluff.SimpleRpmBuild("hhh", "1.0", "1", ["x86_64"])
pkghhi = rpmfluff.SimpleRpmBuild("hhh", "1.0", "1", ["i686"])
allbase = (pkgaaa, pkgbbb, pkgccc, pkgddd, pkgeee, pkgfff, pkgggg, pkghhx, pkghhi)
# currently works
pkgbbb.add_requires("aaa < 3.0")
# currently broken
pkgddd.add_requires("ccc = 3.0")
# currently works, both sides replaced in new repo
pkgfff.add_requires("eee = 1.0")
# multilib
pkghhx.add_requires("ggg(x86-64)")
pkghhi.add_requires("ggg(x86-32)")

# existing stable update packages
updaaa = rpmfluff.SimpleRpmBuild("aaa", "2.0", "1", ["x86_64"])
updbbb = rpmfluff.SimpleRpmBuild("bbb", "2.0", "1", ["x86_64"])
updccc = rpmfluff.SimpleRpmBuild("ccc", "2.0", "1", ["x86_64"])
updddd = rpmfluff.SimpleRpmBuild("ddd", "2.0", "1", ["x86_64"])
allupd = (updaaa, updbbb, updccc, updddd)
# should be broken by the new packages
updbbb.add_requires("aaa == 2.0")
# should be OK
updddd.add_requires("ccc >= 2.0")

# replaces aaa-1.0-1, breaks bbb
newaaa = rpmfluff.SimpleRpmBuild("aaa", "3.0", "1", ["x86_64"])
# replaces ccc-1.0-1, fixes ddd
newccc = rpmfluff.SimpleRpmBuild("ccc", "3.0", "1", ["x86_64"])
# replaces eee, would break fff but we also replace fff below
neweee = rpmfluff.SimpleRpmBuild("eee", "3.0", "1", ["x86_64"])
newfff = rpmfluff.SimpleRpmBuild("fff", "3.0", "1", ["x86_64"])
# replaces ggg-1.0-1, breaks hhh.i686 as there's no i686 here
newggg = rpmfluff.SimpleRpmBuild("ggg", "3.0", "1", ["x86_64"])
# intentionally broken to check installability
new111 = rpmfluff.SimpleRpmBuild("111", "3.0", "1", ["x86_64"])
allnew = (newaaa, newccc, neweee, newfff, newggg, new111)
newfff.add_requires("eee = 3.0")
new111.add_requires("nonexistent")

for pkg in allbase + allupd + allnew:
    pkg.addVendor("Fedora Project")
    pkg.addPackager("Fedora Project")

base = rpmfluff.yumrepobuild.YumRepoBuild(allbase)
basedir = "base"
new = rpmfluff.yumrepobuild.YumRepoBuild(allnew)
newdir = "new"
updates = rpmfluff.yumrepobuild.YumRepoBuild(allupd)
upddir = "updates"
empty = rpmfluff.yumrepobuild.YumRepoBuild([])
empdir = "empty"


def cleanup(repos=True):
    dirs = [pkgaaa.get_base_dir()]
    if repos:
        dirs.extend((basedir, upddir, newdir, empdir))
    for _dir in dirs:
        if os.path.isdir(_dir):
            shutil.rmtree(_dir)


cleanup()

os.mkdir(basedir)
os.mkdir(newdir)
os.mkdir(upddir)
os.mkdir(empdir)
base.repoDir = basedir
new.repoDir = newdir
updates.repoDir = upddir
empty.repoDir = empdir
base.make("x86_64", "i686")
new.make("x86_64")
updates.make("x86_64")
empty.make()

cleanup(repos=False)
