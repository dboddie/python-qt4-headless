#!/usr/bin/env python

# undo_patches.py - Undo patches to PyQt4 for X11 files.
# Copyright (C) 2012 David Boddie <david@boddie.org.uk>
#
# This program is free software: you can redistribute it and/or modify
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

import os, glob, shutil, sys


def find_files(pattern, path):

    files = glob.glob(os.path.join(path, pattern))
    
    for dir_name in os.listdir(path):
    
        full_path = os.path.join(path, dir_name)
        
        if os.path.isdir(full_path):
            files += find_files(pattern, full_path)
    
    return files


if __name__ == "__main__":

    if len(sys.argv) != 2:
    
        sys.stderr.write("Usage: %s <target directory>\n" % sys.argv[0])
        sys.exit(1)
    
    target_dir = os.path.abspath(sys.argv[1])
    
    for target in find_files("*.old", target_dir):
    
        print target
        if os.system("cp %s %s" % (target, target[:-4])):
            sys.stderr.write("Failed to recover file: %s\n" % target[:-4])
            sys.exit(1)
    
    sys.exit()
