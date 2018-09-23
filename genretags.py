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


class GenreCache:
    _genreList = []

    def addGenre(self, g):
        if g not in self._genreList:
            self._genreList.append(g)

    def display(self):
        count=0
        for g in self._genreList:
            print(str(count)+" - "+g)
            count+=1

    def getGenre(self, value):
        if value.isnumeric() and int(value) < len(self._genreList):
            return self._genreList[int(value)]
        else:
            return value
def usage():
    print('usage: ' + sys.argv[0] + ' folder')


def get_file_type(f):
    magic_string = magic.from_file(f)
    if 'MPEG' in magic_string:
        return "MPEG"
    if 'FLAC' in magic_string:
        return "FLAC"
    return None



def scan_files(folder, flist, albums, genres):
    for f in os.listdir(folder):
        fpath = os.path.join(folder, f)
        if os.path.isfile(fpath):
            try:
                ftype = get_file_type(fpath)
                if ftype is not None:
                    tags = mutagen.File(fpath, easy=True)
                    g = tags['genre'][0]
                    if g not in genres:
                        genres.append(g)
                    flist.append(fpath)
            except Exception as e:
                # print(traceback.format_exc())
                error_state.append(fpath)


        else:
            albums.append(f)
            scan_files(os.path.join(folder, f), flist, albums, genres)

def edit_genre(flist, genre):
    for f in flist:
        try:
            # print(f)
            tags = mutagen.File(f, easy=True)
            tags['genre'] = (genre)
            tags.save()
        except Exception as e:
            print("Processing "+bcolors.ERROR+f+bcolors.ENDC)
            print(traceback.format_exc())
            error_state.append(f)


def process_folder(folder, genre_memory):
    print("Artist "+bcolors.ARTIST+os.path.basename(folder)+bcolors.ENDC);
    flist = []
    albums = []
    local_genres = []
    scan_files(folder, flist, albums, local_genres)
    print("Albums:")
    for a in albums:
        print(bcolors.ALBUM+a+bcolors.ENDC)
    print("Genres:")
    for g in local_genres:
        print(bcolors.GENRE+g+bcolors.ENDC)
    print("ENTER - Skip folder")
    genre_memory.display()

    var = input()
    if len(var) > 0:
        g = genre_memory.getGenre(var)
        edit_genre(flist, g)
        genre_memory.addGenre(g)
############################################################################


if len(sys.argv) != 2:
    usage()
    exit(0)

root=sys.argv[1]


error_state = []
genre_memory = GenreCache()

count=0
for filename in sorted(os.listdir(root)):
    if not os.path.isfile(os.path.join(root, filename)):
        process_folder(os.path.join(root, filename), genre_memory)
    count+=1



if len(error_state) > 0:
    print(bcolors.ERROR+str(len(error_state)) + " errors in files"+bcolors.ENDC)
    for f in error_state:
        print(f)



