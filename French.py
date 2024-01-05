#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
French revision programme - it gets the 200 most popular verbs,
according to CNRS (via TalkinFrench), and their conjugations.
Chooses one at random, and user has to correctly conjugate it.
"""
from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import urllib.parse
import re
import unicodedata


class VerbError(Exception):
    """
    Error raised when verb is not found on http://conjf.cactus2000.de/
    """
    pass


class conjTable:
    """
    Object for retaining and printing French conjugation tables
    """
    def __init__(self, verb: tuple[str, str]):
        """
        verb - 		len 2 tuple containing (French, English) form of verb
        """

        self.French, self.English = verb
        self.tables = {}				# Dictionary for holding conjugation table

        headers = {
            'HTTP_USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36',
            'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml; q=0.9,*/*; q=0.8',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        urlverb = self.remove_accents(self.French)
        verb = urlverb.split()[-1]
        self.reqURL = f'http://conjf.cactus2000.de/showverb.en.php?verb={verb}'
        request = urllib.request.Request(self.reqURL, headers=headers)
        fi = urllib.request.urlopen(request)

        # Read in html
        try:
            Webpage = fi.read()
        finally:
            fi.close()

        # Check in case the verb has not been found
        if re.search(b'Verb not found.', Webpage):
            raise VerbError

        # Parse web-page using BeautifulSoup
        soup = BeautifulSoup(Webpage, 'lxml')

        # Know that all verbs of interest are in 4th table,
        # and separated by "div" tags
        tenses = soup.find("table", {"class": "conjtab"})

        # Read in all information into list
        result = []
        for row in tenses.findAll('tr'):
            cells = row.findAll('td')
            sub = [cell.text for cell in cells]

            # Append sub to result
            result.append(sub)

        # Hack to get required tenses - (vertical, horizontal) offsets
        offset = {'présent': (1, 0),
                  'imparfait': (1, 1),
                  'futur simple': (8, 1),
                  'passé composé': (15, 0),
                  'conditionnel présent': (45, 0)}

        # Go through result table and parse
        for tense, pos in offset.items():
            conj = []
            down, right = pos
            for n in range(6):
                try:
                    conj.append(result[n+down][right])
                except IndexError:
                    # Likely to be Falloir - can skip
                    raise VerbError

            # Save to dictionary
            self.tables[tense] = conj

    def __repr__(self):
        """
        Text representation of the object
        """
        representation = f"French:{self.French:<20} English:{self.English:<20}"
        print((80*"=" + "\n\t" + representation))
        return (80*"=")

    def remove_accents(self, input_str: str) -> str:
        """
        Removes accented characters from string and tries to get a close
        ascii character match
        """
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        only_ascii = nfkd_form.encode('ASCII', 'ignore')
        return str(only_ascii, 'utf-8')

    def tenses(self) -> list:
        """
        Return keys for all tenses of verb
        """
        return list(self.tables.keys())

    def alt_tenses(self) -> dict[str: str]:
        """
        Conversion between non-accented and accented tenses
        """
        # Convert non-accented tense into accented one

        alt_tenses = {}
        for ten in self.tenses():
            alt_tenses[self.remove_accents(ten)] = ten

        return alt_tenses

    def tenses_print(self):
        """
        Prints all available tenses in pretty form (i.e. with accents)
        """
        print((',\n'.join(self.tenses())))

    def conjugate(self, tense: str):
        """
        Creates list of the conjugation table for given tense

        input:
            tense:	Desired tense of conjugation - must be in self.tenses()
                    or non-accented equivilent using self.remove_accents

        returns:
            conj:	List of conjugation in [je, tu, il, nous, vous, ils] form
        """

        if tense in self.alt_tenses():
            tense = self.alt_tenses()[tense]

        if tense not in self.tenses():
            raise ValueError

        return self.tables[tense]

    def prints(self, tense: str):
        """
        Displays (in nice form!) the conjugation table for given tense

        input:
            tense:				Desired tense of conjugation - must be in self.tenses()
                                or non-accented equivilent using self.remove_accents

        returns:
            conj:				List of conjugation in [je, 		nous
                                                        tu, 		vous
                                                        il,			ils] form
        """
        tense_list = self.conjugate(tense)
        print_header = '\n' + 80*'=' + '\n\t\t\t  {0} --------------- {1}\n'.format(self.French, self.English) + 80*'='
        print_tense = '\n' + '{0:^80}\n'.format(tense) + 80*'-'
        print_table = '\n\t\t{0:28} {3}\n\t\t{1:28} {4}\n\t\t{2:28} {5}\n'.format(*tense_list)
        print((print_header + print_tense + print_table))


def save_conj(conjtable, filename):
    """
    Write the ConjTable object to a file
    """
    return


def load_conj(filename):
    """
    Reads ConjTable information from file
    """
    return
