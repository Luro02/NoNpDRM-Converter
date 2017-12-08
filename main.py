#!/usr/bin/env python3
# -*- encoding: utf-8 -*-#

import header
import fileparser
import setup_keys
# port these functions to header.py ?!
key = setup_keys.setup()

input_file = header.input_txt("input.txt")
header.database(key[0], key[1], key[2], key[3])

# for tid in input_file:
#	cid = header.csv_parser(5, tid, file)
#   region = header.csv_parser(1, tid, file)
#	if region is not None:
#		fileparser.download_file(cid, region, tid, name)
cid = []
file = "data_0.csv"

for tid in input_file:
    header.pkg(file, tid)


header.database_cleanup()
