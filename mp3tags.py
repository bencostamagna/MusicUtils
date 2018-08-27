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


def process_folder(folder):
    flist = []
    scan_files(folder, flist)

    mismatch = None
    for f in flist:
        try:
            magic_string = magic.from_file(f)
            if 'MPEG' in magic_string:
                tags = eyed3.load(f)
                if tags.tag.artist != os.path.basename(folder):
                    if mismatch == None:
                        mismatch = TagMismatch(tag=tags.tag.artist, expected=os.path.basename(folder))
                    mismatch.add_file(f)
        except:
            error_state.append(f)
    
    if mismatch != None:
        artist_mismatch.append(mismatch)

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
print(str(len(artist_mismatch)) + " bad artist tags")
for m in artist_mismatch:
    print(m.tag + " -> " + m.expected + " in " + str(len(m.files)) + " files")


