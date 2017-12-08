#!/usr/bin/env python3
# -*- encoding: utf-8 -*-#
import re
import sys
import os
from urllib.request import urlopen
import urllib.error

# maybe don't use the CSV CID's and instead extract them from the Links (PKG Downloads) ????


def create_link(cid, region):
    # write all missing Icon, TID's into log.txt or smth similiar ? when exception happens
    if region == "US":
        region = "US/en/999/"
    elif region == "US ":
        region = "US/en/999/"

    elif region == "EU":
        region = "DE/de/19/"
    elif region == "EU ":
        region = "DE/de/19/"

    elif region == "JP":
        region = "JP/ja/999/"
    elif region == "JP ":
        region = "JP/ja/999/"

    elif region == "ASIA":
        region = "SG/en/999"
    elif region == "ASIA":
        region = "SG/en/999"

    else:
        print("\n" + str(region) + ".")
        sys.exit("Something went wrong with the region !!!")
    base = "https://store.playstation.com/store/api/chihiro/00_09_000/container/" + region
    url = base + cid
    return url


def get_apollo(raw):
    raw = re.findall(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', raw)
    raw = [x for x in raw if "apollo2" in x]  # filter out all apollo2 Links
    # The different Apollo Links are the Icon Size's (0 to 3) but 0 seems to be the best compromise out of space and quality :)
    return raw[0]


def download_file(cid, region, tid, name):
    try:
        response = urlopen(create_link(cid, region))
        html = response.read().decode('utf-8')
        response = urlopen(get_apollo(html))
        html = response.read()
        with open(cid + '.png', 'wb') as f:
            # convert to bytearray before writing # "html" is already binary
            f.write(bytearray(html))
        try:
            os.mkdir("icons")
        except FileExistsError:
            pass
        try:
            os.rename(cid + ".png", "icons" + "\\" + cid + ".png")
        except FileExistsError:
            try:
                os.remove(cid + ".png")
            except OSError:
                sys.exit(
                    "Something went really wrong (Python says it's a File and this Error says it's a Dir lol)")
        except OSError:
            sys.exit("Destination File is a Directory !")

    except urllib.error.HTTPError:
        try:
            print(str(cid), str(name), str(tid))
        except UnicodeEncodeError:
            pass
