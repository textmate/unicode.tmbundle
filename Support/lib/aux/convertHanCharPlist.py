#!/usr/bin/python
# encoding: utf-8

import unicodedata
import sys
import os
import codecs
import plistlib

with open("/Users/bibiko/Desktop/Category-Unicode.plist", "rb") as f:
    d = plistlib.load(f)['RadicalDataArray']

rad_counter = 0

for a in d:
    dd = a["CVRadicalData"]
    for ddd in dd:
        rad_counter += 1
        e = ddd["CVCategoryData"]["DataArray"]
        for f in e:
            if f["CVDataTitle"] == "":
                sys.stdout.write(str(rad_counter) + "\t" + a["CVDataTitle"] + "\t" + ddd["CVDataTitle"] + "\t" + ",".join(ddd["Radicals"]) + "\t" + "0\t" + f["Data"] + ",\n")
            else:
                sys.stdout.write(str(rad_counter) + "\t" + a["CVDataTitle"] + "\t" + ddd["CVDataTitle"] + "\t" + ",".join(ddd["Radicals"]) + "\t" + f["CVDataTitle"] + "\t" + f["Data"] + ",\n")
