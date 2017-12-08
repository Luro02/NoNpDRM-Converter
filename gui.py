#!/usr/bin/env python3
# -*- encoding: utf-8 -*-#
import itertools
import functools
import re
import os
import sys
import pandas as pd
import header

if header.exists("data_0.csv") is False:
    header.initial_setup()
elif header.exists("data_1.csv") is False:
    header.initial_setup()
elif header.exists("data_2.csv") is False:
    header.initial_setup()
elif header.exists("data_3.csv") is False:
    header.initial_setup()
elif header.exists("data_4.csv") is False:
    header.initial_setup()

position = None
search_input = None
selection = []

# The console has problems with the encoding (chinese chars, japanese chars...)
dataformat = pd.read_csv("data_0.csv", encoding='utf-8',
                         skipinitialspace=False, header=None, skiprows=1)

titleid = dataformat[0].tolist()
region = dataformat[1].tolist()
name = dataformat[2].tolist()
link = dataformat[3].tolist()
zrif = dataformat[4].tolist()
cid = dataformat[5].tolist()
size = dataformat[8].tolist()
sha256 = dataformat[9].tolist()


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


def send_variables():
    return name, titleid
# searching and get_position already used/defined in header !!! (remove it)


def searching(value, liste):
    """ filter the items that math the search term """
    list1 = []
    for item in liste:
        if value.lower() in item.lower():
            list1.append(item)
    return list1


def search_item(itm, lst):
    """Pass an item and a list and get all idexes of it in the list"""
    indexes = [x for x in range(len(lst)) if lst[x] == itm]
    return indexes


def get_position(value1, liste):
    """ get all positions of the search terms in the specified list"""
    positions = []
    for item in value1:
        positions.append(search_item(item, liste))
    # merge all lists and remove duplicates:
    positions = list(set(functools.reduce(lambda x, y: x + y, positions)))
    return positions


def show_results(value1):
    for item in enumerate(value1, start=1):
        item = list(item)
        item.insert(1, '.')
        item = list(map(str, item))
        print(''.join(item))


def create_regions_list(position):
    regions = []
    for item in position:
        regions.append(region[int(item)])
    return regions


def start_searching(value):
    if value is None:
        print("What do you want to search ?")
        search = input(">> ")
    else:
        search = value
    result = searching(search, name)  # just what the search found
    position = get_position(result, name)  # where it's located
    # result with region added:
    result = list(zip(result, create_regions_list(position)))
    new_result = []
    for item in result:
        item = item[0] + ' ' + '[' + item[1] + ']'
        new_result.append(item)
    clearscreen()
    show_results(new_result)
    print("")
    selectioner = []
    selectioner.append(titleid[position[int(input("Select a number: ")) - 1]])

    return search, selectioner

# iput() nach nummer abfragen
# j nach nummer auswählen und downloaden ah ich habe ne idee lol titleid[position[input()]]
