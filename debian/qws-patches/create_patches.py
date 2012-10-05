#!/usr/bin/env python

# create_patches.py - Create a set of patches from a modified PyQt4 distribution.
# Copyright (C) 2009 David Boddie <david@boddie.org.uk>
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


def mkdir(parent_path, directories):

    for name, subdirectories in directories.items():
    
        path = os.path.join(parent_path, name)
        os.mkdir(path)
        print "Created directory:", path
        mkdir(path, subdirectories)


if __name__ == "__main__":

    if len(sys.argv) != 3:
    
        sys.stderr.write("Usage: %s <original directory> <diff directory>\n\n" % sys.argv[0])
        sys.stderr.write("Scans the original directory and creates diffs for all files that are\n")
        sys.stderr.write("accompanied by versions with .old suffixes.\n")
        sys.stderr.write("The patches are stored within the diff directory in a directory structure\n")
        sys.stderr.write("that follows the locations of the files relative to the current directory.\n\n")
        sys.stderr.write("In other words, run this from the root directory of the package you have\n")
        sys.stderr.write("changed, specifying the subdirectory containing changes and the root\n")
        sys.stderr.write("directory of the target package.\n")
        sys.exit(1)
    
    original_dir = os.path.abspath(sys.argv[1])
    suffix = os.extsep + "old"
    new_suffix = os.extsep + "diff"
    old_files = find_files("*" + suffix, original_dir)
    target_dir = os.path.abspath(sys.argv[2])
    
    current_dir = os.path.abspath(os.curdir)
    current_dir_pieces = current_dir.split(os.sep)
    directories = {}
    
    for path in old_files:
    
        path = os.path.abspath(path)
        directory, file_name = os.path.split(path)
        
        directory = directory.split(os.sep)
        
        if directory[:len(current_dir_pieces)] == current_dir_pieces:
        
            pieces = directory[len(current_dir_pieces):]
            dir_path = target_dir
            
            for piece in pieces:
                dir_path = os.path.join(dir_path, piece)
                if not os.path.exists(dir_path):
                    os.mkdir(dir_path)
            
            path = path[len(current_dir):].lstrip(os.sep)
            new_path = path[:-len(suffix)]
            diff_path = os.path.join(dir_path, file_name[:-len(suffix)]+new_suffix)
            
            os.chdir(current_dir)
            os.system("diff -u "+path+" "+new_path+" > "+diff_path)
    
    sys.exit()
