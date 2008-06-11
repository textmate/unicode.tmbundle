#!/usr/bin/python
# encoding: utf-8

import sys
import os
import codecs
import unicodedata
import time

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stdin  = codecs.getreader('utf-8')(sys.stdin)

bundleLibPath = os.environ["TM_BUNDLE_SUPPORT"] + "/lib/"

sourceFile = "UNInames"

if len(sys.argv) != 3:
    print "Wrong number of arguments."

searchkind = sys.argv[1]
if not (searchkind == 'word' or searchkind == 'full'):
    print "Wrong first argument. Only 'word' or 'full'."

if searchkind == "full":
    grepopt = "%"
else:
    grepopt = ""

pattern = sys.argv[2]

if not os.path.exists(bundleLibPath + sourceFile):
    res = os.popen("'" + bundleLibPath + "/aux/createUnicodeNamesDB.sh" + "'")
    print "<i><b>Index was built. Please press RETURN again.</b></i><br><br>"

if os.stat(bundleLibPath + "UnicodeData.txt.zip")[8] > os.stat(bundleLibPath + sourceFile)[8]:
    res = os.popen("'" + bundleLibPath + "/aux/createUnicodeNamesDB.sh" + "'")
    print "<i><b>Index was rebuilt. Please press RETURN again.</b></i><br><br>"

grepcmds = []
froms = []
jns = []
tbl = 1
for pat in pattern.split(' '):
    if pat:
        grepcmds.append("i%s.word LIKE \"%s%s%s\"" % (str(tbl), grepopt, pat, '%'))
        froms.append("nameindex AS i%s" % str(tbl))
        jns.append("n.char = i%s.char" % str(tbl))
        tbl += 1

grepcmd =  "sqlite3 -separator ';' '%s%s' 'SELECT DISTINCT n.char, n.name FROM %s, names AS n WHERE %s AND %s ORDER BY n.char'" %  (bundleLibPath, sourceFile, ", ".join(froms), " AND ".join(grepcmds), " AND ".join(jns))
print grepcmd
suggestions = os.popen(grepcmd).read().decode("utf-8").strip()

if not suggestions:
    print "Nothing found"

print "<span style='font-family:Charis SIL, Lucida Grande'><table>"
for i in suggestions.split('\n'):
    c, n = i.split(';')
    print "<tr><td><big>&%s;</big></td><td>&nbsp;&nbsp;&nbsp;</td><td>%s</td></tr>" % (c, n)
print "</table></span>"