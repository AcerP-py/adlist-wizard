"""Asa Rentschler 2023"""

# imports
import sys
import urllib
from datetime import datetime
import time
import re
import argparse
import os
import wget

# version
VERSION = 'v1.1.0'

"""System Arguments"""
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-v', '--version', action='version', version=VERSION)
arg_parser.add_argument('-o', '--out', type=str, default='ad_list.al', help='output file')
arg_parser.add_argument('-m', '--mode', type=str, choices=['files', 'lists'], default='files', help='source mode')
arg_parser.add_argument('source', type=str, nargs='*', help='list of input files/lists')
arg_parser.add_argument('-rd', '--remove_duplicates', action='store_const', const=True,
                        default=False, help='remove duplicates')
args = arg_parser.parse_args()

"""Helper Functions"""


def out(info, err=False, level='info'):
    """
    Print function.
    :param info: string to write
    :param err: if the string is about an err
    :param level: prefix header
    """
    headers = {'info': 'i', 'err': 'x', 'section': '#'}
    if err:
        level = 'err'
        print("\033[91m {}\033[00m".format(
            ('\t' if level != 'section' else '') + "[" + headers[level] + "] " + info))
    else:
        print("\033[92m {}\033[00m".format(
            ('\t' if level != 'section' else '') + "[" + headers[level] + "] " + info))


def extract_from_file(host_file, verbose=True):
    """
    Extracts hosts from file.
    :param verbose: print info
    :param host_file: the file to extract from
    """
    try:
        with open(host_file, 'r') as stream:
            out(f"File {host_file} found. Starting extraction...") if verbose else None
            for line in stream:
                split = line.split(' ') if re.search("^(#|\/\/|\\n)", line) is None else []
                for word in split:
                    host_cache.append(word.strip('\n')) if re.search("^[^#].*([a-z|A-Z|0-9]\.[a-z|A-Z])", word) is not None \
                        else None
        out(f"All host extracted from {host_file}.") if verbose else None
    except (FileNotFoundError, IsADirectoryError) as e:
        out(f"The file {host_file} could not be found skipping...", err=True)


def extract_from_list(source_file):
    try:
        with open(source_file, 'r') as source_list:
            for source in source_list:
                clean_source = source.strip('\n')
                try:
                    out(f"Starting extraction from {clean_source}...")
                    wget.download(clean_source, "temp")
                    print('')
                    extract_from_file("temp", verbose=False)
                    os.remove("temp")
                    out(f"All host extracted from {clean_source}")
                except (ValueError, urllib.error.HTTPError) as e:
                    out(f"The url {clean_source} could not be found skipping...", err=True)
                    print('')
    except (FileNotFoundError, IsADirectoryError) as e:
        out(f"The file {source_file} could not be found skipping...", err=True)


def write_to_host_file():
    """
    Write host to file.
    """
    try:
        out(f"Writing to {args.out}...", level='section')
        with open(args.out, 'w') as out_file:
            out_file.write(f"# Title: Combined Host List\n")
            out_file.write(f"# Date: {datetime.now()} {time.tzname[0]}\n")
            out_file.write(f"# Compiler: AdList Wizard\n")
            out_file.write(f"# Version: {VERSION}\n")
            out_file.write(f"# Website: https://github.com/AcerP-py/adlist-wizard\n")
            out_file.write(f"# Host Count: {len(host_cache)}\n")
            out_file.write(f"# {'=' * 60}\n")
            out_file.write('\n\n')
            for host in host_cache:
                out_file.write(host + '\n')
        out(f"Write complete.")
    except (FileNotFoundError, IsADirectoryError) as e:
        out(f"The file {args.out} could not be found. Write canceled.", err=True)


"""main"""
out(f"Hello! Welcome to Adlist Wizard version {VERSION}", level='section')

# variables
host_cache = []
total = None
unique = None if args.remove_duplicates else None
duplicates = None if args.remove_duplicates else None

# extract all hosts
out(f"Starting extraction of hosts...", level='section')
if args.mode == 'files':
    for file in args.source:
        extract_from_file(file)
elif args.mode == 'lists':
    for a_list in args.source:
        extract_from_list(a_list)
out(f"Extraction complete.")

# remove duplicates
if args.remove_duplicates:
    out("Removing duplicates...", level='section')
    total = len(host_cache)
    host_cache = list(set(host_cache))
    host_cache.sort()
    unique = len(host_cache)
    duplicates = total - unique
    out("Duplicates removed.")
else:
    total = len(host_cache)

# calculate and print stats
out(f"Stats -", level='section')
out(f"Total: {total}")
out(f"Unique: {unique}") if unique is not None else None
out(f"Duplicates: {duplicates}") if duplicates is not None else None

# write new host file
write_to_host_file()

# goodbye!
out(f"Goodbye!", level='section')
