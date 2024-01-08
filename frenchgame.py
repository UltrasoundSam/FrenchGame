#!/usr/bin/env python
# -*- coding: utf-8 -*-
from webscape import scrape_data
import pickle
import random
import os
import sys

# Check to see whether data needs to be scraped or not
datadir = os.path.expanduser('~/.French/VerbTables')

if not os.path.exists(datadir):
    # Scrape data from web, and save to disk for future use
    print('Downloading Conjugations for Top 200 most popular French verbs')
    Verbs = scrape_data()
else:
    # Read conjugations from file
    print('Loading Conjugation tables from file')
    VerbFiles = (fi for fi in os.listdir(datadir) if fi.endswith('pkl'))

    Verbs = {}

    # Read in all verbs
    for i, fi in enumerate(VerbFiles):
        with open(os.path.join(datadir, fi)) as fi2:
            Buff = pickle.load(fi2)
        Verbs[i] = Buff

personage = {0: 'je',
             1: 'tu',
             2: 'il/elle',
             3: 'nous',
             4: 'vous',
             5: 'ils/elles'}

while True:
    # Let user choose what conjugation they want to practice
    Request = """Choose tense to practice:
    1.\t{0}
    2.\t{1}
    3.\t{2}
    4.\t{3}
    5.\t{4}
    6.\t{5}\n""".format(*Verbs[0].tenses())

    tense = input(str(Request))

    if tense == 'q':
        sys.exit()

    # Checking input to make sure it makes sense
    valid = ['1', '2', '3', '4', '5', '6']

    if tense not in valid:
        print((f"""This is not a valid choice -
               choose integer between {valid[0]} - {valid[-1]}"""))
        tense = input(Request)

    tense = Verbs[0].tenses()[int(tense)-1]

    # Choose verbs at random
    score = 0

    for _ in range(10):
        test = random.choice(Verbs)

        person = random.randint(0, 5)

        package = (test.French, personage[person], tense)
        question = """Please conjugate the verb:
        {0} in the {1} form for the {2} tense\n""".format(*package)
        answer = input(str(question))

        if answer == test.conjugate(tense)[person]:
            print("CORRECT!\n")
            score += 1
        else:
            ans = test.conjugate(tense)[person]
            print(f"Correct answer was {ans}\n")

    print(('Your score was {0}%!\n\n'.format(int(100 * score/10.))))
