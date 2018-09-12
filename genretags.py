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

class bcolors:
    ERROR = '\033[91m'#Red
    ALBUM = '\033[94m' # Blue
    GENRE = '\033[92m' # Green
    ARTIST = '\033[93m'
    ENDC = '\033[0m'


def usage():
    print('usage: ' + sys.argv[0] + ' folder')


def get_file_type(f):
    magic_string = magic.from_file(f)
    if 'MPEG' in magic_string:
        return "MPEG"
    if 'FLAC' in magic_string:
        return "FLAC"
    return None



def scan_files(folder, flist, albums):
    for f in os.listdir(folder):
        if os.path.isfile(os.path.join(folder, f)):
            flist.append(os.path.join(folder, f))
        else:
            albums.append(f)
            scan_files(os.path.join(folder, f), flist, albums)


def process_folder(folder):
    print("Artist "+bcolors.ARTIST+os.path.basename(folder)+bcolors.ENDC);
    flist = []
    albums = []
    local_genres = []
    scan_files(folder, flist, albums)
    for f in flist:
        try:
            ftype = get_file_type(f)
            if ftype is not None:
                tags = mutagen.File(f, easy=True)
                genre = tags["genre"][0] 
                if genre not in local_genres:
                    local_genres.append(genre)

        except Exception as e:
            # print(traceback.format_exc())
            error_state.append(f)

    print("Albums:")
    for a in albums:
        print(bcolors.ALBUM+a+bcolors.ENDC)
    print("Genres:")
    for g in local_genres:
        print(bcolors.GENRE+g+bcolors.ENDC)
    print("ENTER - Skip folder")
    var = input()

############################################################################


if len(sys.argv) != 2:
    usage()
    exit(0)

root=sys.argv[1]


error_state = []

count=0
for filename in sorted(os.listdir(root)):
    if not os.path.isfile(os.path.join(root, filename)):
        process_folder(os.path.join(root, filename))
    count+=1



if len(error_state) > 0:
    print(bcolors.ERROR+str(len(error_state)) + " errors in files"+bcolors.ENDC)
    for f in error_state:
        print(f)



