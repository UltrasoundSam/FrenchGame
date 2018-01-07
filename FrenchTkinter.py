#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Webscrape import scrape_data
import French as fr
import Tkinter as Tk
import cPickle
import re
import random
import os

class Game(Tk.Frame):
	def __init__(self, master=None):
		# Initialise the Game screen
		self.master = master
		self.master.title('French Verb Conjugation')
		self.master.minsize(width=500, height=200)
		
		# Creating all necesary frames
		self.Choiceframe = Tk.Frame(self.master)
		self.gameframe = Tk.Frame(self.master)
		self.answerframe = Tk.Frame(self.master)		
		
		# Get conjugation data
		self.welcomeScreen()
		
		# Move to choice of tense
		self.ChoiceScreen()
		
		# Make Answer Screen
		self.answerScreen()
	
	def welcomeScreen(self):
		'''
		Gets the conjugation info either by web-scraping or by
		reading from file if the data has already been scraped 
		'''
		# Check to see whether data needs to be scraped or not
		datadir = os.path.expanduser('~/.French/VerbTables')
		
		if not os.path.exists(datadir):
			# Scrape data from web, and save to disk for future use
			self.Verbs = scrape_data()
		else:
			# Read conjugations from file
			VerbFiles = (fi for fi in os.listdir(datadir) if fi.endswith('pkl'))
			
			self.Verbs = {}
			
			# Read in all verbs
			for i, fi in enumerate(VerbFiles):
				with open(os.path.join(datadir, fi)) as fi2:
					Buff = cPickle.load(fi2)
				self.Verbs[i] = Buff

	def ChoiceScreen(self):
		'''
		Creates all the buttons for the choice screen
		'''
		self.gameframe.grid_forget()
		self.answerframe.grid_forget()
		
		# Create label
		self.TenseMsg = Tk.Label(self.Choiceframe, text='Choose tense to practice:\n\n')
		self.TenseMsg.grid(row=0, column=2, columnspan=3)
		
		# Create Quit Button
		self.Quit = Tk.Button(self.Choiceframe, text='Quit', fg='red', command=self.master.quit)
		self.Quit.grid(row=14, column=10, sticky=Tk.SE)
		
		# Create Radio Buttons for tense selection
		self.tensechoice = Tk.IntVar()
		self.tensechoice.set(0)
		
		tenselist = self.Verbs[0].tenses()
		
		self.buttons = {}
		for val, tense in enumerate(tenselist[:3]):
			self.buttons[val] = Tk.Radiobutton(self.Choiceframe, text=tense, variable=self.tensechoice, value=val)
			self.buttons[val].grid(row=val+3, column=2, sticky=Tk.W)
		
		for val, tense in enumerate(tenselist[3:]):
			self.buttons[val+3] = Tk.Radiobutton(self.Choiceframe, text=tense, variable=self.tensechoice, value=val+3)
			self.buttons[val+3].grid(row=val+3, column=6, sticky=Tk.W)
		
		# Create button to Accept choice
		self.select = Tk.Button(self.Choiceframe, text='Select', command=self.choose)
		self.select.grid(row=14, column=0)
		self.Choiceframe.grid()
	
	def gameScreen(self, tense):
		'''
		Creates the screen for the main game
		'''
		self.Choiceframe.grid_forget()
		self.answerframe.grid_forget()
		
		self.personage = {0: 'je', 1: 'tu', 2: 'il/elle', 3: 'nous', 4: 'vous', 5: 'ils/elles'}
		
		self.Quit = Tk.Button(self.gameframe, text='Quit', fg='red', command=self.master.quit)
		self.Quit.grid(row=14, column=10, sticky=Tk.SE)
		
		# Initiate score and make button layouts
		self.score = 0
		
		self.randVerb = random.choice(self.Verbs)
		self.randPerson = random.randint(0, 5)
		self.tense = tense
		
		# Question Label
		self.Question = Tk.Label(self.gameframe, text=self.questionfmt(self.randVerb, self.randPerson, self.tense))
		self.Question.grid(row=0, column=1, columnspan=2, rowspan=3)
		
		# Response Box
		self.AnsBox = Tk.Entry(self.gameframe, background='white')
		self.AnsBox.grid(row=1, column=1, columnspan=2, rowspan=3)
		
		# Choose Verbs again
		self.ChoseVerb = Tk.Button(self.gameframe, text='Choose Verb', command=self.ChoiceScreen)
		self.ChoseVerb.grid(row=14, column=2) 
		
		# Select Box
		self.Sel = Tk.Button(self.gameframe, text='OK', command=self.comparison)
		self.Sel.grid(row=14, column=0)
		
		self.gameframe.grid()
	
	def answerScreen(self):
		'''
		Creates layout for answer screen
		'''
		self.gameframe.grid_forget()
		# Answer Response
		self.Answer = Tk.Label(self.answerframe, text=u'')
		self.Answer.pack()
		
		# Quit Button and Next
		self.Quit = Tk.Button(self.answerframe, text='Quit', fg='red', command=self.master.quit)
		self.Quit.pack()
		
		self.Next = Tk.Button(self.answerframe, text='Next', command=self.nextquestion)
		self.Next.pack()
	
	def choose(self):
		'''
		Get Tense choice and progress onto gameplay
		'''
		tense = self.tensechoice.get()
		self.game(self.Verbs[0].tenses()[tense])
	
	def game(self, tense):
		'''
		Function for doing the main game loop
		'''
		self.gameScreen(tense)
	
	def questionfmt(self, verb, person, tense):
		'''
		Formats the question in a easy way
		'''
		Question = u"Please conjugate the verb: {0} in the {1} form\n for the {2} tense\n\n\n\n".format(verb.French, self.personage[person], tense)
		return Question
	
	def comparison(self):
		'''
		Compares response to correct answer
		'''
		self.gameframe.grid_forget()
		
		# Get Answer
		answer = self.AnsBox.get().encode('utf-8').decode('utf-8')
		
		# Compare against correct answer
		CorrectAnswer = self.randVerb.conjugate(self.tense)[self.randPerson]
		
		if answer == CorrectAnswer:
			self.score += 1
			self.Answer['text'] = u'Correct!'
		else:
			self.Answer['text'] = u'Incorrect, the correct answer is {0}'.format(CorrectAnswer)
		self.answerframe.grid()	
	
	def nextquestion(self):
		'''
		Moves to the next question
		'''
		self.answerframe.grid_forget()
		
		# Choose verb and personage at random again
		self.randVerb = random.choice(self.Verbs)
		self.randPerson = random.randint(0, 5)
		
		# Update Question
		self.Question['text'] = self.questionfmt(self.randVerb, self.randPerson, self.tense)
		self.AnsBox.delete(0, Tk.END)
		self.gameframe.grid()
		

root = Tk.Tk()
A = Game(root)
root.mainloop()

