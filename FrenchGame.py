#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Webscrape import scrape_data
import French as fr
import cPickle
import re
import random
import os

# Check to see whether data needs to be scraped or not
datadir = os.path.expanduser('~/.French/VerbTables')

if not os.path.exists(datadir):
	# Scrape data from web, and save to disk for future use
	print("Downloading Conjugation Tables for Top 200 most popular French verbs")
	Verbs = scrape_data()
else:
	# Read conjugations from file
	VerbFiles = (fi for fi in os.listdir(datadir) if fi.endswith('pkl'))
	
	Verbs = {}
	
	# Read in all verbs
	for i, fi in enumerate(VerbFiles):
		with open(os.path.join(datadir, fi)) as fi2:
			Buff = cPickle.load(fi2)
		Verbs[i] = Buff
	
personage = {0: 'je', 1: 'tu', 2: 'il/elle', 3: 'nous', 4: 'vous', 5: 'ils/elles'}

# Let user choose what conjugation they want to practice
Request = u"Choose tense to practice: \n1.\t{0}\n2.\t{1}\n3.\t{2}\n4.\t{3}\n5.\t{4}\n".format(*Verbs[0].tenses())
Tense = raw_input(Request.encode('utf-8'))

# Checking input to make sure it makes sense
Valid = ['1', '2', '3', '4', '5']

if Tense not in Valid:
	print "This is not a valid choice - choose integer between 1 - 5"
	Tense = raw_input(Request)

Tense = Verbs[0].tenses()[int(Tense)-1]

# Choose verbs at random
score = 0
while score < 5:
	Test = random.choice(Verbs)

	person = random.randint(0, 5)
	
	Question = u"Please conjugate the verb: {0} in the {1} form for the {2} tense\n".format(Test.French, personage[person], Tense)
	Answer = raw_input(Question.encode('utf-8')).decode('utf-8')
	
	if Answer == Test.conjugate(Tense)[person]:
		print "CORRECT!\n"
		score += 1
	else:
		print(u"Correct answer was {0}\n".format(Test.conjugate(Tense)[person]))

