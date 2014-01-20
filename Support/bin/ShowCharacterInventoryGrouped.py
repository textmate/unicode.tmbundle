#!/usr/bin/python
# encoding: utf-8


import sys
import os
import codecs
import itertools
from UniTools import *

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stdin  = codecs.getreader('utf-8')(sys.stdin)

bundleLibPath = os.environ["TM_BUNDLE_SUPPORT"] + "/lib/"

class SeqDict(dict):
    """Dict that remembers the insertion order."""
    def __init__(self, *args):
        self._keys={}
        self._ids={}
        self._next_id=0
    def __setitem__(self, key, value):
        self._keys[key]=self._next_id
        self._ids[self._next_id]=key
        self._next_id+=1
        return dict.__setitem__(self, key, value)
    def keys(self):
        ids=list(self._ids.items())
        ids.sort()
        keys=[]
        for id, key in ids:
            keys.append(key)
        return keys



HEADER_HTML = """<html>
<head><title>Character Inventory</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<style type='text/css'>

    body {
        font-size: 12pt;
    }
    
    th {
        text-align:left;
        padding: 1px 3px;
        background-color: #aaa;
        color: #fff;
    }

    table {
        border:1px solid #silver;
        border-collapse: collapse;
        width: 100%;
    }

    col {
        width: 15%;
    }

    col.name {
        width: 40%;
    }

    td {
        padding: 1px 3px;
    }

    tr {
        height: 2em;
    }
    .a {
        text-align:center;
    }

    .tr1 {
        background-color:#ddd;
    }

    .tr2 {
        background-color:#bbb;
    }

    .b {
        text-align:center;
        cursor:pointer;
    }

    table#character-inventory {
        width: auto;
        margin: auto;
        text-align: center;
        vertical-align: middle;
    }

    table#character-inventory td {
        border: solid black 1px;
        width: 2em;
        height: 2em;
    }
</style>
</head>
<body>
"""

def main():
    print HEADER_HTML

    # dict of unique chars in doc and the number of its occurrence
    chKeys = {}
    for l in sys.stdin:
        for c in codepoints(l):
            try:
                chKeys[c] += 1
            except KeyError:
                chKeys[c] = 1

    try:
        chKeys.pop(10) # Avoid displaying newlines
    except:
        1

    keys = chKeys.keys()
    keys.sort()

    relDataFile = file(bundleLibPath + "relatedChars.txt", 'r')
    relData = relDataFile.read().decode("UTF-8").splitlines()
    relDataFile.close()
    groups = SeqDict()    # groups of related chars
    unrel  = []    # list of chars which are not in groups

    for ch in keys:
        wch = wunichr(ch)
        for index, group in enumerate(relData):
            if group.__contains__(wch):
                try:
                    groups[index].append(ch)
                except KeyError:
                    groups[index] = []
                    groups[index].append(ch)
                break
        else:
            unrel.append(ch)


    print "<table border=1><tr>"
    print "<th>Character</th><th>Occurrences</th><th>UCS</th><th>Unicode Block</th><th>Unicode Name</th>"
    print "</tr><tbody id='theTable'>"

    total    = 0
    distinct = 0
    regExp   = []
    data     = {}

    for c in keys:
        hexCode = "%04X" % int(c)
        regExp.append(hexCode)

    UnicodeData = os.popen("zgrep -E '^(" + "|".join(regExp) + ");' '" + bundleLibPath + "UnicodeData.txt.gz'").read().decode("UTF-8")

    for c in UnicodeData.splitlines():
        uniData = c.strip().split(';')
        if len(uniData) > 1: data[uniData[0]] = uniData[1]

    bgclasses = ['tr2', 'tr1']

    for (clsstr, gr) in itertools.izip(itertools.cycle(bgclasses), groups.keys()):
        for c in groups[gr]:
            total += chKeys[c]
            distinct += 1
            t = wunichr(c)
            name = data.get("%04X" % int(c), getNameForRange(c) + "-%04X" % int(c))
            # I have no idea why name can be 1 ??
            if name == 1 or name[0] == '<': name = getNameForRange(c) + "-%04X" % int(c)
            if "COMBINING" in name: t = u"◌" + t
            # if groups[gr] has only one element shows up it as not grouped; otherwise bgcolor alternates
            if len(groups[gr]) == 1: clsstr = ''
            print "<tr class='" + clsstr + "'><td class='a'>", \
                    t, "</td><td class='a'>", chKeys[c], "</td><td>", \
                    "U+%04X" % (int(c)), "</td><td>", getBlockName(c), "</td><td>", name, "</tr>"

    for c in unrel:
        total += chKeys[c]
        distinct += 1
        t = wunichr(c)
        name = data.get("%04X" % int(c), getNameForRange(c) + "-%04X" % int(c))
        if name == 1 or name[0] == '<': name = getNameForRange(c) + "-%04X" % int(c)
        if "COMBINING" in name: t = u"◌" + t
        print "<tr><td class='a'>", t, "</td><td class='a'>", chKeys[c], \
                "</td><td>", "U+%04X" % (int(c)), "</td><td>", \
                getBlockName(c), "</td><td>", name, "</tr>"

    print "</table>"

    if total < 2:
        pl = ""
    else:
        pl = "s"

    print '<h2><a name="inventory">Character Inventory</a></h2>'
    print "<p><i>%d character%s total, %d distinct</i></p>" % (total, pl, distinct)

    print '<table id="character-inventory">'
    print '<tr>'
    i = 0
    for c in keys:
        if i > 0 and i % 25 == 0:
            print '</tr><tr>'
        print '<td>', wunichr(c), '</td>',
        i += 1
    print '</tr>'
    print "</table>"
    print "<p></p>"
    print "</body></html>"

if __name__ == "__main__":
    main()
