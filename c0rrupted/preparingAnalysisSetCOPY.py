#* -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 22:49:32 2021

@author: pavel
"""

# %% imports
import pandas as pd
import re

# %% error-definitions
class mtcLstZrLen(Exception):
	pass

# %% function-definitions
def extractQueryTxtsFromURList(listOfURLs):
	

# %% creating list of search-URLs and 
listOf_Query_URLs = [
	'https://export.arxiv.org/find/all/1/all:+AND+networks+AND+convolutional+neural/0/1/0/all/0/1',
	'https://export.arxiv.org/find/all/1/all:+aerodynamics/0/1/0/all/0/1',
	'https://export.arxiv.org/find/all/1/all:+AND+industrial+robots/0/1/0/all/0/1',
	'https://export.arxiv.org/find/all/1/all:+AND+bio+resistance/0/1/0/all/0/1',
	'https://export.arxiv.org/find/all/1/all:+AND+space+AND+quaternions+in/0/1/0/all/0/1'
	] # should be copied to the db-creating program

# %% creating list of query-strings DONE: right order of words


# regular expression for extractiong query-words from URLs
reQueryWords = re.compile(r'(?<=\+)((?=[^AND])\w{1,})') # words from search-query

listOfQueryTexts = list() 

for url in listOf_Query_URLs:
	raw_listOf_queryWords = reQueryWords.findall(url)  #raw list of query-words
# 
	if len(raw_listOf_queryWords) == 1:
		listOfQueryTexts.append(raw_listOf_queryWords[0])
	elif len(raw_listOf_queryWords) == 0:
		raise mtcLstZrLen('no match with regExp in text')
	else:
		#sorting raw_listOf_queryWords
		for i in range(len(raw_listOf_queryWords) - 2):
			raw_listOf_queryWords.append(raw_listOf_queryWords.pop(0))
		#end of sorting
		queryText = ''
		for wordElement in raw_listOf_queryWords:
			queryText += wordElement + ' '
		listOfQueryTexts.append(queryText)

print(listOfQueryTexts)
# %% Excel-file
numberOfSearches = len(listOf_Query_URLs)

writer = pd.ExcelWriter('Experiment Preparations.xlsx') 
#filling up the DICT - base for DataFrame
dataDict = {'Index of search request': range(numberOfSearches), 
			'Include in the next experiment?': [False] * numberOfSearches, 
			'Text of search request': listOfQueryTexts}
#creating DataFrame from the DICT
dataFrame = pd.DataFrame(dataDict) # spcl-type-var from which table is made
#creating Excel-file from DataFrame
dataFrame.to_excel(writer, sheet_name='sheet1', index=False, na_rep='NaN')

# %% auto-adjusting the column-width in the Excel-file
for column in dataFrame:
    column_width = max(dataFrame[column].astype(str).map(len).max(), len(column))
    col_idx = dataFrame.columns.get_loc(column)
    writer.sheets['sheet1'].set_column(col_idx, col_idx, column_width)
writer.save()
# %%






