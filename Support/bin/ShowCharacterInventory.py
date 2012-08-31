#!/usr/bin/python
# encoding: utf-8

import sys
import os
import codecs
import unicodedata
from UniTools import *

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stdin  = codecs.getreader('utf-8')(sys.stdin)

bundleLibPath = os.environ["TM_BUNDLE_SUPPORT"] + "/lib/"

HEADER_HTML = """<html>
<head><title>Character Inventory</title>
<script type='text/javascript'>//<![CDATA[
function sortTable2(col) {
  var tblEl = document.getElementById('theTable');
  if (tblEl.reverseSort == null)
    tblEl.reverseSort = new Array();
  if (col == tblEl.lastColumn)
    tblEl.reverseSort[col] = !tblEl.reverseSort[col];
  tblEl.lastColumn = col;
  var oldDsply = tblEl.style.display;
  tblEl.style.display = 'none';
  var tmpEl;
  var i, j;
  var minVal, minIdx;
  var testVal;
  var cmp;
  for (i = 0; i < tblEl.rows.length - 1; i++) {
    minIdx = i;
    minVal = getTextValue(tblEl.rows[i].cells[col]);
    for (j = i + 1; j < tblEl.rows.length; j++) {
      testVal = getTextValue(tblEl.rows[j].cells[col]);
      cmp = compareValues(minVal, testVal);
      if (tblEl.reverseSort[col])
        cmp = -cmp;
      if (cmp > 0) {
        minIdx = j;
        minVal = testVal;
      }
    }
    if (minIdx > i) {
      tmpEl = tblEl.removeChild(tblEl.rows[minIdx]);
      tblEl.insertBefore(tmpEl, tblEl.rows[i]);
    }
  }
  tblEl.style.display = oldDsply;
  return false;
}
if (document.ELEMENT_NODE == null) {
  document.ELEMENT_NODE = 1;
  document.TEXT_NODE = 3;
}
function getTextValue(el) {
  var i;
  var s;
  s = '';
  for (i = 0; i < el.childNodes.length; i++)
    if (el.childNodes[i].nodeType == document.TEXT_NODE)
      s += el.childNodes[i].nodeValue;
    else if (el.childNodes[i].nodeType == document.ELEMENT_NODE &&
             el.childNodes[i].tagName == 'BR')
      s += ' ';
    else
      s += getTextValue(el.childNodes[i]);
  return normalizeString(s);
}
function compareValues(v1, v2) {
  var f1, f2;
  f1 = parseFloat(v1);
  f2 = parseFloat(v2);
  if (!isNaN(f1) && !isNaN(f2)) {
    v1 = f1;
    v2 = f2;
  }
  if (v1 == v2)
    return 0;
  if (v1 > v2)
    return 1
  return -1;
}
var whtSpEnds = new RegExp('^\\s*|\\s*$', 'g');
var whtSpMult = new RegExp('\\s\\s+', 'g');
function normalizeString(s) {
  s = s.replace(whtSpMult, ' ');  // Collapse any multiple whites space.
  s = s.replace(whtSpEnds, '');   // Remove leading or trailing white space.
  return s;
}
//]]></script>
<style type='text/css'>

    body {
        font-size: 12pt;
    }
    
    th {
        text-align:left;
        padding: 1px 3px;
        background-color: #aaa;
        color: #fff;
        cursor:pointer;
    }

    table {
        border:1px solid #silver;
        border-collapse: collapse;
        width: 100%;
    }

    tbody tr:nth-child(even) {
        background-color: #eee;
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


    print "<table border=1><tr>"

    if len(keys)<400:
        print "\
        <th><span title='click to sort' onclick='return sortTable2(0)'>Character</span></th> \
        <th><span title='click to sort' onclick='return sortTable2(1)'>Occurrences</span></th> \
        <th><span title='click to sort' onclick='return sortTable2(0)'>UCS</span></th> \
        <th><span title='click to sort' onclick='return sortTable2(3)'>Unicode Block</span></th> \
        <th><span title='click to sort' onclick='return sortTable2(4)'>Unicode Name</span></th>"
    else:
        print "<th>Character</th><th>Occurrences</th><th>UCS</th><th>Unicode Block</th><th>Unicode Name</th>"

    print "</tr><tbody id='theTable'>"
    #len(text) and len(keys) don't work caused by uni chars > U+FFFF
    total = 0
    distinct = 0
    regExp = {}
    data = {}
    for ch in keys:
        try:
            data["%04X" % int(ch)] = unicodedata.name(wunichr(ch))
        except ValueError:
            regExp["%04X" % int(ch)] = 1
        except TypeError:
            regExp["%04X" % int(ch)] = 1


    UnicodeData = os.popen("zgrep -E '^(" + "|".join(regExp.keys()) + ");' '" + bundleLibPath + "UnicodeData.txt.zip'").read().decode("UTF-8")

    for c in UnicodeData.splitlines():
        uniData = c.strip().split(';')
        if len(uniData) > 1: data[uniData[0]] = uniData[1]

    for c in keys:
        if c != 10:
            total += chKeys[c]
            distinct += 1
            t = wunichr(c)
            try:
                name = data["%04X" % int(c)]
            except KeyError:
                name = getNameForRange(c) + "-%04X" % int(c)
            if name[0] == '<': name = getNameForRange(c) + "-%04X" % int(c)
            if "COMBINING" in name: t = u"◌" + t
            print "<tr><td class='a'>", t, "</td><td class='a'>", chKeys[c], "</td><td>", "U+%04X" % (int(c)), "</td><td>", getBlockName(c), "</td><td>", name, "</tr>"

    print "</tbody></table>"

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
