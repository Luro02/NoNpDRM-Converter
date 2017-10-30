#!/usr/bin/env python3
import os
import sys
import hashlib
import csv
import urllib
import urllib.request
from subprocess import call
import update
from path import Path

def setup_keys():
	if  os.path.exists(keys.cfg)==False: sys.exit("The 'keys.cfg' file wasn't found !")
	#read File
	with open ("keys.cfg", "r") as r:
		key = r.readlines()
	key[1] = key[1].replace(' ', '')[:-20]
	#Hashcheck
	hash_1 = hashlib.sha1((key[1]).encode("utf-8"))

	if "e6125b7856d917f776b73563f67a26b867724f30" != hash_1.hexdigest():
		sys.exit("The link is wrong !")
	else:
		link = key[1]+"export?format=csv&id=18PTwQP7mlwZH1smpycHsxbEwpJnT8IwFP7YZWQT7ZSs&gid=1180017671"

	return link

# https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def input_txt(filename):
	if  os.path.exists(filename)==False: sys.exit("The input file wasn't found !")
	arr = open(filename).read().split("\n")
	return arr

def database(link):
	urllib.request.urlretrieve(link, 'data.csv')

def search_tid(string):
    with open('data.csv', 'r', encoding="utf-8") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            for j, column in enumerate(row):
                if string in column:
                    # print ((i,j))
                    return i # i ist die Linie und j ist die Spalte
    return None

def read_cell(x, y):
    with open('data.csv', 'r', encoding="utf-8") as f:
        reader = csv.reader(f)
        y_count = 0
        for n in reader:
            if y_count == y:
                cell = n[x]
                return cell
            y_count += 1

def pkg(tid):
	if  os.path.exists(pkg_dec.exe)==False: sys.exit("The pkg_dec.exe wasn't found !")
	i = search_tid(tid)
	link = read_cell(3, i)
	urllib.request.urlretrieve(link, 'temp.pkg')
	zrif = read_cell(4, i)
	if zrif == "NOT REQUIRED":
		zrif = None
	if zrif != "MISSING":
		os.system("pkg_dec --make-dirs=ux temp.pkg --license="+zrif)
		Path("temp.pkg").remove_p()
	else:
		print("ZRif is Missing for", tid)
def downupdate(tid):
    link = update.patch(tid)
    if link != 0:
        urllib.request.urlretrieve(link, 'temp.pkg')
        call("pkg_dec --make-dirs=ux temp.pkg")
        Path("temp.pkg").remove_p()

def down(tid):
    database(setup_keys())
    pkg(tid)
    downupdate(tid)

# I think my Code is Clean XD
# Maybe I could minimize the amount 
# of Functions but most of them may be 
# usefull in the Future