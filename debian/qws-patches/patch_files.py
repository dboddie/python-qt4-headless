#!/usr/bin/env python

# patch_files.py - Patch PyQt4 for X11 files.
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

def create_feature_map(paths):

    features = {}
    in_features = []
    in_structures = []
    declared_features = set()
    
    for path in paths:
        print path
        for line in open(path).readlines():
            line = line.strip()
            if line.startswith("%If ("):
                feature = line[5:line.find(")", 5)]
                in_features.append(feature)
                in_structures.append(feature)
            elif line.startswith("%End"):
                if in_features and in_structures[-1] == in_features[-1]:
                    in_features.pop()
                in_structures.pop()
            elif line.startswith("%Include"):
                name = line[9:-4].strip()
                if in_features:
                    features[name] = set(in_features)
            elif line.startswith("%Feature"):
                declared_features.add(line[9:].strip())
            elif line.startswith("%"):
                in_structures.append(line[1:])
    
    for name, in_features in features.items():
        features[name] = in_features.intersection(declared_features)

    return features

def change_graph(path, features):

    lines = open(path).readlines()
    new_lines = []
    
    for line in lines:
    
        at = line.find("{sipName_")
        if at != -1:
        
            # Look up the features corresponding to the class name.
            name = line[at+9:line.find(",", at+9)]
            if name.lower() in features:
            
                # Look at the previous line.
                if not new_lines or not new_lines[-1].strip().startswith("#if "):
                    # Create a check for the class.
                    new_lines.append("    #if ")
                    existing = False
                else:
                    new_lines[-1] = new_lines[-1].rstrip() + " && "
                    existing = True

                # Append conditions to the check.
                new_lines[-1] += " && ".join(map(lambda feature: "defined(SIP_FEATURE_" + feature + ")", features[name.lower()]))
                new_lines[-1] += "\n"

                # Add the line to the output.
                new_lines.append(line)

                if not existing:
                    # For new checks, add a fallback structure.
                    new_lines.append("    #else\n")
                    
                    start = line.find("{") + 1
                    end = line.find("}")
                    values = line[start:end].split(",")
                    new_lines.append(line[:start] + "0, 0," + ", ".join(values[-2:]) + line[end:])
                    new_lines.append("    #endif\n")
        else:
            new_lines.append(line)
    
    open(path, "w").write("".join(new_lines))


if __name__ == "__main__":

    if len(sys.argv) != 3:
    
        sys.stderr.write("Usage: %s <diff directory> <target directory>\n" % sys.argv[0])
        sys.exit(1)
    
    patches_dir = os.path.abspath(sys.argv[1])
    diffs = find_files("*"+os.extsep+"diff", patches_dir)
    target_dir = os.path.abspath(sys.argv[2])
    
    target_files = map(lambda path:
        os.path.join(target_dir, path[len(patches_dir+os.sep):path.rfind(os.extsep)]),
        diffs)
    
    for target, diff in zip(target_files, diffs):
    
        print "patch %s %s" % (target, diff)
        if not os.path.exists(target):
            print "%s not found - assuming it does not exist in this version.\n" % target
        if os.system("cp %s %s.old" % (target, target)):
            sys.stderr.write("Failed to preserve file: %s\n" % target)
            sys.exit(1)
        if os.system("patch %s %s" % (target, diff)):
            sys.stderr.write("Failed to patch file: %s\n" % target)
            sys.exit(1)
    
    # Change the graph data structures of existing files to handle features.
    feature_map = create_feature_map(find_files("Qt*mod"+os.extsep+"sip", target_dir))

    for path in target_files:
        change_graph(path, feature_map)

    new_files = find_files("*"+os.extsep+"sip", patches_dir)
    
    target_files = map(lambda path:
        os.path.join(target_dir, path[len(patches_dir+os.sep):]),
        new_files)
    
    for target, new_file in zip(target_files, new_files):
    
        print "cp %s %s" % (new_file, target)
        if os.system("cp %s %s" % (new_file, target)):
            sys.stderr.write("Failed to preserve file: %s\n" % target)
            sys.exit(1)
    
    sys.exit()
