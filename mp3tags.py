#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 chupacabra <chupacabra@diziet>
#
# Distributed under terms of the GPL3 license.

import sys, os, os.path
import magic
import eyed3

class TagMismatch:
    def __init__(self, tag, expected):
        self.tag = tag
        self.expected = expected
        self.files = []

    def add_file(self, filepath):
        self.files.append(filepath)



def scan_files(folder, flist):
    for f in os.listdir(folder):
        if os.path.isfile(os.path.join(folder, f)):
            flist.append(os.path.join(folder, f))
        else:
            scan_files(os.path.join(folder, f), flist)


def solve_mismatch(folder, mismatch_list):
    print(str(len(mismatch_list)) + " bad artist tags")
    recheck = False
    for m in mismatch_list:
        print(str(len(m.files)) + " files containing tag "+m.tag+" but folder name is "+m.expected)
        print("1 Rename folder to " + m.tag)
        print("2 Change tags to " + m.expected)
        print("3 Ignore")
        var = input()
        if var == "1":
            print ("Renaming "+folder + " to "+os.path.join(os.path.dirname(folder), m.tag))
            os.rename(folder, os.path.join(os.path.dirname(folder), m.tag))
            recheck = True
        elif var == "2":
            print("Retagging")
        else:
            pass
    return recheck

def process_folder(folder):
    flist = []
    scan_files(folder, flist)
    recheck = True

    while recheck:
        recheck = False
        mismatch_list = []
        for f in flist:
            try:
                magic_string = magic.from_file(f)
                if 'MPEG' in magic_string:
                    tags = eyed3.load(f)
                    if tags.tag.artist != os.path.basename(folder):
                        found=False
                        for m in mismatch_list:
                            if m.tag == tags.tag.artist:
                                m.add_file(f)
                                found=True
                        if not found:
                            mismatch_list.append(TagMismatch(tag=tags.tag.artist, expected=os.path.basename(folder)))
            except:
                error_state.append(f)

        if len(mismatch_list) > 0:
            recheck = solve_mismatch(folder, mismatch_list)


############################################################################


if len(sys.argv) == 0:
    exit(0)

root=sys.argv[1]

eyed3.log.setLevel("ERROR")


artist_mismatch = []
error_state = []

count=0
for filename in os.listdir(root):
    print (filename)
    if not os.path.isfile(os.path.join(root, filename)):
        process_folder(os.path.join(root, filename))
    count+=1



print(str(len(error_state)) + " errors in files")


