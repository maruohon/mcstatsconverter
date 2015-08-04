import os
import sys
import json
import shutil
import re
from datetime import datetime


# workdir = os.curdir
workdir = os.getcwd()
mappingsfilename = 'mappings.txt'
printpretty = False

def print_help():
    print ("Usage: %s [--pretty] [--mappings=path/to/mappingsfile] <statsdir>" % sys.argv[0])
    print ("")
    print ("This program will convert the Minecraft stats files from the 1.7 format (numerical IDs)")
    print ("to the 1.8 format (string IDs).")
    print ("You must give it a 'mappings file' that contains all the id -> string mappings.")
    print ("Such a mappings file should be available with this program at the original repository.")
    print ("")
    print ("The '--pretty' option will also output nicely formatted versions of the stats files")
    print ("so that you can better see if everything seems right.")
    print ("")
    print ("v1.0 @ 2015-01-14")
    print ("by masa")
    print ("Available at https://github.com/maruohon/mcstatsconverter")

if len(sys.argv) > 1:
    gotdir = False

    for s in sys.argv[1:len(sys.argv)]:
        if s.startswith('-'):
            if s == '--pretty':
                printpretty = True
            elif s.startswith('--mappings='):
                mappingsfilename = s[11:len(s)]
            elif s == '--help' or s == '-h' or s == '-?':
                print_help()
                exit()
            else:
                print ("Unrecognized option '%s'" % s)
                exit(1)
        elif gotdir == False:
            workdir = s
            gotdir = True
        else:
            print ("Unrecognized/extraneous parameter '%s'" % s)
            exit(1)
else:
    print_help()
    exit(1)

if workdir[len(workdir) - 1] != os.sep:
    workdir = workdir + os.sep

# print ("mappingsfile: " + mappingsfilename)

if os.path.isfile(mappingsfilename) == False:
    print ("Error: Could not find the mappings file '%s'" % mappingsfilename)
    exit(1)

keymappings = {}

with open(mappingsfilename, 'r') as mappingsfile:
    lines = mappingsfile.readlines()
    for line in lines:
        match = re.match('^(\d+)\s*=\s*(.*)$', line)
        if match != None:
            keyid = match.group(1)
            keystr = match.group(2)
            keystrmod = keystr.replace('minecraft:', 'minecraft.')
            # print ("match: %s => %s (%s)" % (keyid, keystrmod, keystr))
            keymappings[keyid] = keystrmod


def backup_statsfile(path, filename):
    # datestr = strftime("%Y-%m-%d_%H.%M.%S", gmtime())
    now = datetime.now()
    datestr = "%d-%02d-%02d_%02d.%02d.%02d.%06d" % (now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond)
    backupfile = filename + "_backup_" + datestr
    shutil.copy2(path + filename, path + backupfile)


def convert_statsfile(path, filename, keymappings):
    statsfile = open(workdir + filename, 'r')
    oldstats = json.load(statsfile)
    statsfile.close()

    newstats = {}

    for oldkey in oldstats:
        # print ("stat: %s" % oldkey)
        newkey = oldkey

        startpos = 0

        if oldkey.startswith('stat.breakItem.'):
            startpos = len('stat.breakItem.')
        elif oldkey.startswith('stat.craftItem.'):
            startpos = len('stat.craftItem.')
        elif oldkey.startswith('stat.mineBlock.'):
            startpos = len('stat.mineBlock.')
        elif oldkey.startswith('stat.useItem.'):
            startpos = len('stat.useItem.')

        if startpos != 0:
            oldid = oldkey[startpos:len(oldkey)]

            if not oldid in keymappings:
                print ("Error: missing mapping for id '%s'" % oldid)
                exit(1)

            newkey = oldkey[0:startpos] + keymappings[oldid]
            # print ("mapping key: %s => %s" % (oldkey, newkey))

        newstats[newkey] = oldstats[oldkey]

    # print newstats

    if printpretty == True:
        with open(workdir + filename + '_sorted_old', 'w') as sorted:
            json.dump(oldstats, sorted, sort_keys=True, indent=4)

        with open(workdir + filename + '_sorted_new', 'w') as sorted:
            json.dump(newstats, sorted, sort_keys=True, indent=4)

    statsfile = open(workdir + filename, 'w')
    json.dump(newstats, statsfile, sort_keys=True)
    statsfile.close



for filename in os.listdir(workdir):
    if filename.endswith(".json"):
        print ("backing up file: %s" % filename)
        backup_statsfile(workdir, filename)
        print ("converting file: %s" % filename)
        convert_statsfile(workdir, filename, keymappings)
