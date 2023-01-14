# Asa Rentschler 2023

# imports
import sys
from datetime import datetime
import time
import re

# version
VERSION = '1.0.0'

# system args
OUTPUT = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else 'ad_list.al'
FILTER = True if '--rd' in sys.argv else False

FILE_LIST = sys.argv
FILE_LIST.pop(0)
FILE_LIST.remove('--out') if '--out' in FILE_LIST else None
FILE_LIST.remove(OUTPUT) if OUTPUT in FILE_LIST else None
FILE_LIST.remove('--rd') if '--rd' in FILE_LIST else None


# helper functions #

def out(info, err=False, level='info'):
    if err:
        print("\033[91m {}\033[00m".format("[x] " + info))
    else:
        print("\033[92m {}\033[00m".format("[i] " + info))


# main
out(f"Hello! Welcome to Adlist Wizard version {VERSION}\n\n")

host_cache = []
total = 0
unique = 0
duplicates = 0

# extract all hosts
out(f"Starting extraction of hosts...")
for file in FILE_LIST:
    try:
        with open(file, 'r') as stream:
            out(f"File {file} found. Starting extraction...")
            for line in stream:
                # ignore empty lines and lines with comments
                if line != '\n' and line[0] != '#':
                    split = line.split(' ')
                    for word in split:
                        # filter out non domains
                        if re.search("^[^#].*([a-z|A-Z|0-9]\.[a-z|A-Z])", word) is not None:
                            # check for duplicates if filter is on
                            if FILTER:
                                if word not in host_cache:
                                    host_cache.append(word)
                                    total += 1
                                    unique += 1
                                else:
                                    total += 1
                                    duplicates += 1
                            else:
                                host_cache.append(word)
                                total += 1
        out(f"All host extracted from {file}.\n")
    except (FileNotFoundError, IsADirectoryError) as e:
        out(f"The file {file} could not be found skipping...\n", err=True)
out(f"Extraction complete.")
out(f"Total: {total}" + ('\n\n' if not FILTER else ''))
out(f"Unique: {unique}") if FILTER else None
out(f"Duplicates: {duplicates}") if FILTER else None

# writing to file
out(f"Writing to {OUTPUT}...")
out_file = open(OUTPUT, 'w')
out_file.write(f"# Title: Combined Host List\n")
out_file.write(f"# Date: {datetime.now()} {time.tzname[0]}\n")
out_file.write(f"# Compiler: AdList Wizard\n")
out_file.write(f"# Version: {VERSION}\n")
out_file.write(f"# Website: https://github.com/AcerP-py/adlist-wizard\n")
out_file.write(f"# Host Count: {len(host_cache)}\n")
out_file.write(f"# {'=' * 50}\n")
out_file.write('\n\n')

# write hosts
host_cache.sort()
for host in host_cache:
    out_file.write(host)

# close out file
out_file.close()
out(f"Write complete.\n\n")

# goodbye!
out(f"Goodbye!")
