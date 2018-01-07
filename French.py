#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
French revision programme - it gets the 200 most popular verbs, 
according to CNRS (via TalkinFrench), and their conjugations. 
Chooses one at random, and user has to correctly conjugate it.
"""
from bs4 import BeautifulSoup
import urllib2
import re
import unicodedata

class VerbError(Exception):
	"""
	Error raised when verb is not found on http://conjf.cactus2000.de/
	"""
	pass

class conjTable(object):
	"""
	Object for retaining and printing French conjugation tables
	"""
	def __init__(self, verb):
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
		
		urlverb = self.remove_accents(unicode(self.French)) #urllib2.quote(self.French.encode('utf-8'))
		self.reqURL = 'http://conjf.cactus2000.de/showverb.en.php?verb={0}'.format(urlverb.split()[-1])
		request = urllib2.Request(self.reqURL, headers=headers)
		fi = urllib2.urlopen(request)
		
		# Read in html
		Webpage = fi.read()
		fi.close()
		
		# Check in case the verb has not been found
		if re.search("Verb not found.", Webpage):
			raise VerbError
		
		# Parse web-page using BeautifulSoup
		soup = BeautifulSoup(Webpage, 'lxml')
		
		# Know that all verbs of interest are in 4th table, and separated by "div" tags
		Tenses = soup('table')[3]('div')
		
		Interest = [0, 2, 6, 8, 16, 24]			# Hack to get required tenses
		
		for i in Interest:
			Tense = Tenses[i+1]
			Conj = []
			for form in Tense.strings:
				Conj.append(form)
			self.tables[Tenses[i].string] = Conj
	
	def __repr__(self):
		"""
		Text representation of the object
		"""
		representation = u"French: {0:<20} English: {1:<20}".format(self.French, self.English)
		print(80*u"=" + "\n\t" + representation)
		return(80*"=")
	
	def remove_accents(self, input_str):
		"""
		Removes accented characters from string and tries to get a close
		ascii character match
		"""
		nfkd_form = unicodedata.normalize('NFKD', input_str)
		only_ascii = nfkd_form.encode('ASCII', 'ignore')
		return only_ascii
	
	def tenses(self):
		"""
		Return keys for all tenses of verb
		"""
		return self.tables.keys()
	
	def alt_tenses(self):
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
		print(',\n'.join(self.tenses()))
		
	def conjugate(self, tense):
		"""
		Creates list of the conjugation table for given tense
		
		input:
			tense:				Desired tense of conjugation - must be in self.tenses() 
								or non-accented equivilent using self.remove_accents
			
		returns:
			conj:				List of conjugation in [je, tu, il, nous, vous, ils] form		
		"""
		
		if tense in self.alt_tenses():
			tense = self.alt_tenses()[tense]
			
		if tense not in self.tenses():
			raise(ValueError, 'Tense not in table!')
		
		return self.tables[tense]
	
	def prints(self, tense):
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
		print(print_header + print_tense + print_table)

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


#P = conjTable(('parler', 'to talk'))
#P.English
#P.French
#P.tenses()
#P.tenses_print()
#P.conjugate(u'conditionnel pr\xe9sent')
#P.conjugate('indicatif present')
#P.prints('conditionnel present')
