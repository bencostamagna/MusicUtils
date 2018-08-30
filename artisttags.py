#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 chupacabra <chupacabra@diziet>
#
# Distributed under terms of the GPL3 license.

import sys, os, os.path
import traceback
import magic
import mutagen

class TagMismatch:
    def __init__(self, tag, expected):
        self.tag = tag
        self.expected = expected
        self.files = []

    def add_file(self, filepath):
        self.files.append(filepath)


def usage():
    print('usage: ' + sys.argv[0] + ' folder')


def get_file_type(f):
    magic_string = magic.from_file(f)
    if 'MPEG' in magic_string:
        return "MPEG"
    if 'FLAC' in magic_string:
        return "FLAC"
    return None



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
            for f in m.files:
                audiofile = mutagen.File(f)
                audiofile["artist"] = m.expected
                audiofile.save()
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
                ftype = get_file_type(f)
                if ftype is not None:
                    tags = mutagen.File(f, easy=True)
                    artist = tags["artist"][0] 
                    if artist != os.path.basename(folder):
                        found=False
                        for m in mismatch_list:
                            if m.tag == artist:
                                m.add_file(f)
                                found=True
                        if not found:
                            mm = TagMismatch(tag=artist, expected=os.path.basename(folder))
                            mm.add_file(f)
                            mismatch_list.append(mm)

            except Exception as e:
                # print(e)
                print(traceback.format_exc())
                error_state.append(f)

        if len(mismatch_list) > 0:
            recheck = solve_mismatch(folder, mismatch_list)


############################################################################


if len(sys.argv) != 2:
    usage()
    exit(0)

root=sys.argv[1]


artist_mismatch = []
error_state = []

count=0
for filename in os.listdir(root):
    print (filename)
    if not os.path.isfile(os.path.join(root, filename)):
        process_folder(os.path.join(root, filename))
    count+=1



print(str(len(error_state)) + " errors in files")


