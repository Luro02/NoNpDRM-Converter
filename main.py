#!/usr/bin/env python3
import header
import os

var1 = header.input_txt("input.txt")

for tid in var1:
   header.down(tid)
os.remove("data.csv") # wget doesn't overwrite files :(