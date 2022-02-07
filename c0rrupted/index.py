# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 22:56:15 2021

@author: pavel
"""

# %% imports

import re
# %% opening file with abstracts REWORK
with open('absSet.txt') as textForAnanlysisFile:
	textForAnalysis = textForAnanlysisFile.read()
# %% separating each word and recording word-indexes
word = '' #temp-var for loop to storage the construction word 
wordIndex = 0 #number for each word

curentIndex = 0 #var for calculating the word-frequency

reEachLetter = re.compile('[a-zA-Z]') #regexp for each letter

temp_everyWord = list() #temp-dictionary REWORK

for char in textForAnalysis:
	if reEachLetter.match(char):
		word += char
	elif word != '':
		temp_everyWord.append(word)
		curentIndex += 1
		word = ''
	else:
		continue

print(temp_everyWord)
# %%








