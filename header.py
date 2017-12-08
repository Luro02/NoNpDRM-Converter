#!/usr/bin/env python3
# -*- encoding: utf-8 -*-#
"""
Garbage Collection of all Functions used or will be used in this Programm (this is my Code)"
!!! The update.py isn't made by myself (I just improved it lol) !!!
I know my english is awesome :)
"""

from subprocess import Popen, PIPE
import os
import sys
import functools
import wget
import update
import setup_keys
import fileparser
import pandas as pd


def clearscreen(numlines=100):
    """
    Clear the console.numlines is an optional argument used only as a fall-back.
    """
    # Thanks to Steven D'Aprano, http://www.velocityreviews.com/forums
    if os.name == "posix":
        # Unix/Linux/MacOS/BSD/etc
        os.system('clear')
    elif os.name in ("nt", "dos", "ce"):
        # DOS/Windows
        os.system('CLS')
    else:
        # Fallback for other operating systems.
        print('\n' * numlines)


def csv_parser(file):
    """
    advanced way of parsing CSV's with Panda(s)
    if feel so professional now XD
    """
    # The console has problems with the encoding (chinese chars, japanese chars...)
    dataformat = pd.read_csv(file, encoding='utf-8',
                             skipinitialspace=False, header=None, skiprows=1)

    titleid = dataformat[0].tolist()
    region = dataformat[1].tolist()
    name = dataformat[2].tolist()
    link = dataformat[3].tolist()
    zrif = dataformat[4].tolist()
    cid = dataformat[5].tolist()
    size = dataformat[8].tolist()
    sha256 = dataformat[9].tolist()

    return titleid, region, name, link, zrif, cid, size, sha256


def exists(path):
    """Test whether a path exists.  Returns False for broken symbolic links"""
    try:
        st = os.stat(path)
    except os.error:
        return False
    return True


def cutit(s, n):
    """
    cute function that removes chars
    s = string
    n = char to remove
    """
    return s[n:]


def syscmd(cmd):
    """
    executes the given command with a better way than using
    os.system() (I don't know why but it seems to be bad practice !)
    It also returns the exe output instead of printing it :)
    """
    cmoa = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    output, error = cmoa.communicate()
    return output, error


def binarys():
    """
    Check what executeables are inside the Source Directory
    """
    if os.path.exists("pkg_dec.exe") and os.path.exists("pkg2zip"):
        return 0
    elif os.path.exists("pkg_dec.exe"):
        return 1
    elif os.path.exists("pkg2zip.exe"):
        return 2


def download(urllink, filename):
    """
    a downloading function, that does complain
    when you download the database but it has a
    cool Progress Bar :)
    You can use my wget version that has an optimization
    for my Tool but the standard one is fine too :)
    Notice to me: write own function that works and looks
                  better !!!
    """
    wget.download(urllink, filename)


def database(link_0, link_1, link_2, link_3, link_4):
    """
    I know that isn't intended this way but it's easier lol
    """
    download(link_0, "data_0.tsv")
    download(link_1, "data_1.tsv")
    download(link_2, "data_2.tsv")
    download(link_3, "data_3.tsv")
    download(link_4, "data_4.tsv")
    # convert the tsv's to csv's
    syscmd('cat data_0.tsv | tr "\\t" "," > data_0.csv')
    syscmd('cat data_1.tsv | tr "\\t" "," > data_1.csv')
    syscmd('cat data_2.tsv | tr "\\t" "," > data_2.csv')
    syscmd('cat data_3.tsv | tr "\\t" "," > data_3.csv')
    syscmd('cat data_4.tsv | tr "\\t" "," > data_4.csv')

    os.remove("data_0.tsv")
    os.remove("data_1.tsv")
    os.remove("data_2.tsv")
    os.remove("data_3.tsv")
    os.remove("data_4.tsv")
    return None


def database_cleanup():
    """
    cleanup <3
    """
    os.remove("data_0.csv")
    os.remove("data_1.csv")
    os.remove("data_2.csv")
    os.remove("data_3.csv")
    os.remove("data_4.csv")
    return None


def input_txt(filename):
    """
    returns the tid's that were read from
    the specified Input file...
    """
    if os.path.exists(filename) is False:
        sys.exit("The input file wasn't found !")
    else:
        arr = open(filename).read().split("\n")
        return arr

# Add multi threading (download the next file while extracting)


def pkg(file, tid):
    """
    Downloads the PKG's from the given TID and File (database)
    """
    tid_all, region_all, name_all, link_all, zrif_all, cid_all, size_all, sha256_all = csv_parser(
        file)
    position = tid_all.index(tid)  # what if tid doesn't exist ? except ???

    print("\nDownloading %s [%s] [%s]" % (
        name_all[position], region_all[position], tid_all[position]))
    download(link_all[position], 'temp.pkg')
    # extract the Game
    zrif = zrif_all[position]
    if zrif == "NOT REQUIRED":
        zrif = None
    elif zrif != "MISSING":
        # modify these lines to work better ? and add Error parsing when exe fails...
        # change extractor ? make it more flexible ?
        if binarys() == 0:
            syscmd("pkg_dec --make-dirs=ux temp.pkg --license=" + zrif)
            os.remove("temp.pkg")
        elif binarys() == 1:
            syscmd("pkg_dec --make-dirs=ux temp.pkg --license=" + zrif)
            os.remove("temp.pkg")
        elif binarys() == 2:
            syscmd("pkg2zip -x temp.pkg" + zrif)
            os.remove("temp.pkg")
        else:
            pass

    else:
        print("ZRif is Missing for", tid_all[position])

    update_pkg(tid)


def update_pkg(tid):
    """
    Downloads updates for games < 3.60+ only
    """
    if update.patch(tid) != 0:
        download(update.patch(tid), 'temp.pkg')
        syscmd("pkg_dec --make-dirs=ux temp.pkg")
        os.remove("temp.pkg")
    else:
        pass


def psp_dec():
    """
    I know, nice teaser :-)
    should download the binarys to extract PSP,PSX,PSM and PSV Games :)
    """
    url = "http://www73.zippyshare.com/d/82TeF7Wp/21566/PS3P_PKG_Ripper_V1.4.1.rar"
    download(url, "temp.rar")


def cleamup():
    if exists("data_0.csv") is True:
        os.remove("data_0.csv")
    if exists("data_0.tsv") is True:
        os.remove("data_0.tsv")
    if exists("data_1.csv") is True:
        os.remove("data_1.csv")
    if exists("data_1.tsv") is True:
        os.remove("data_1.tsv")
    if exists("data_2.csv") is True:
        os.remove("data_2.csv")
    if exists("data_2.tsv") is True:
        os.remove("data_2.tsv")
    if exists("data_3.csv") is True:
        os.remove("data_3.csv")
    if exists("data_3.tsv") is True:
        os.remove("data_3.tsv")
    if exists("data_4.csv") is True:
        os.remove("data_4.csv")
    if exists("data_4.tsv") is True:
        os.remove("data_4.tsv")


def start_download(tid, console):
    """
    standard function fir downloading from queue (hopefully working)
    """
    # add more of the tabs ?
    if console == 'psv':
        file = "data_0.csv"
    elif console == 'dlc':
        file = "data_1.csv"
    elif console == 'psm':
        file = "data_2.csv"
    elif console == 'psx':
        file = "data_3.csv"
    elif console == 'psp':
        file = "data_4.csv"
    else:
        # I know it's the most usefull error message XD
        sys.exit("Error occured while downloading.")
    pkg(file, tid)


def start_download_inputfile():
    """
    downloads from input.txt instead of the queue
    """
    # add tabs
    file = "data_0.csv"
    for tid in input_txt("input.txt"):
        pkg(file, tid)


def initial_setup():
    """
    loads all links from the config file, to download the tsv database
    """
    clearscreen()
    key = setup_keys.setup()
    key_new = []
    for item in key:
        item = item.replace('\n', '')
        key_new.append(item)
    clearscreen()
    database(key_new[0], key_new[1], key_new[2], key_new[3], key_new[6])


def icon_download_original(tid_all, cid_all, region_all, name_all):
    """
    fetches all icons from the PSN that is possible (sometimes error with region or cid...)
    some things also won't show up :/
    """
    for item in tid_all:
        position = tid_all.index(item)
        if region_all[position] is not None or 'nan':
            fileparser.download_file(
                cid_all[position], region_all[position], tid_all[position], name_all[position])
