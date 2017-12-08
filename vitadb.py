#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import wget
from pandas.io.json import json_normalize  # pip install pandas
# Homebrew Database
# ____________________________________________________________________________
wget.download(
    "https://rinnegatamante.it/vitadb/list_hbs_json.php", "homebrew.json")

with open('homebrew.json') as data_file:
    data = json.load(data_file)
dataformat = json_normalize(data)
dataformat.to_pickle('homebrew_database.pkl')
os.remove('homebrew.json')

homebrew = []
homebrew.append(dataformat.values.tolist())
print(homebrew)
# Plugin Database
# ____________________________________________________________________________

wget.download(
    "https://rinnegatamante.it/vitadb/list_plugins_json.php", "plugin.json")
with open('plugin.json') as data_file:
    data = json.load(data_file)
dataformat = json_normalize(data)
dataformat.to_pickle('plugin_database.pkl')
os.remove('plugin.json')

plugin = []
plugin.append(dataformat.values.tolist())
