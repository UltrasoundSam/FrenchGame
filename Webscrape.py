#!/usr/bin/env python
"""
French revision programme - it gets the 200 most popular verbs,
according to CNRS (via TalkinFrench), and their conjugations.
Chooses one at random, and user has to correctly conjugate it.
"""
# from bs4 import BeautifulSoup
import French as fr
import urllib.request
import urllib.error
import urllib.parse
import pickle
import re
import os
import sys

sys.setrecursionlimit(10000)


def scrape_data() -> dict[str: list[str]]:
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

    # Grab list of most common French verbs from the internet
    base_url = 'https://www.talkinfrench.com/most-common-verbs-in-french/'
    Request = urllib.request.Request(base_url, headers=hdr)
    Webpage = urllib.request.urlopen(Request).read().decode('utf-8')
    lines = Webpage.split('\n')

    # Need to parse through webpage and make a list of most popular verbs
    popular = []

    for line in lines:
        # Create string to do re matching
        reStr = '<td class="column-1">(.+)</td><td class="column-2">(.+)</td>'
        m = re.search(reStr, line)
        if m is None:
            continue

        # Add to list in (French, English) tuple
        popular.append(m.group(1, 2))

    # Creating dictionary to store all web-scraped
    # verb tables (using conjTable object)
    top = {}

    # Create new Folder to store saved conjugation tables
    user_home = os.path.expanduser('~/.French')
    path = os.path.join(user_home, 'VerbTables')
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise

    # Run through all the list of popular verbs and save the conj tables
    for i, verb in enumerate(popular):
        try:
            conjugation = fr.conjTable(verb)
            filename = os.path.join(path, '{0}.pkl'.format(verb[0]))
            with open(filename, 'wb') as fi:
                pickle.dump(conjugation, fi)

            top[i] = conjugation
        except fr.VerbError:
            continue
    return top
