#* -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 22:49:32 2021

@author: pavel
"""

# %% imports
import pandas as pd
import re

# %% error-definitions
class mtcLstZrLen(Exception): #rises when regExp for query-string has no match
	pass

# %% function-definitions
def extractQueryTxtsFromURList(listOfURLs):
	"""Extracts the query-string from each search-page URL 
	on the site 'Arxiv.org'. Execution of this function 
	results in list of strings that user used for getting the search-pages 
	Example of the input list: 
		[
		'https://export.arxiv.org/find/all/1/all:+AND+networks+AND+convolutional+neural/0/1/0/all/0/1',
		'https://export.arxiv.org/find/all/1/all:+aerodynamics/0/1/0/all/0/1',
		'https://export.arxiv.org/find/all/1/all:+AND+industrial+robots/0/1/0/all/0/1',
		'https://export.arxiv.org/find/all/1/all:+AND+bio+resistance/0/1/0/all/0/1',
		'https://export.arxiv.org/find/all/1/all:+AND+space+AND+quaternions+in/0/1/0/all/0/1'
		]
	Corresponding output list:
		['convolutional neural networks ', 'aerodynamics', 'industrial robots ', 'bio resistance ', 'quaternions in space ']
	"""
	
	listOfQueryStrings = list()
	
	# regular expression for query-strings from URLs
	reQueryWords = re.compile(r'(?<=\+)((?=[^AND])\w{1,})')
	
	for url in listOf_Query_URLs:
		raw_listOf_queryWords = reQueryWords.findall(url)
	
		if len(raw_listOf_queryWords) == 1:
			listOfQueryStrings.append(raw_listOf_queryWords[0])
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
			listOfQueryStrings.append(queryText)

	print(listOfQueryStrings)
	
	return listOfQueryStrings

def URLfileToList(listOf_Query_URLs):
	"""Открывает файл с ссылкой (на результат запроса на сайте Arxiv.org)
	в каждой строке. Добавляет каждую строку в список, 
	возвращает этот список"""
	
	
# %% importing data from search-pages file
listOf_Query_URLs = list()

with open('searchURLs.txt', 'r', encoding='utf-8') as file:
	listOf_Query_URLs = file.read().splitlines()
print(listOf_Query_URLs)

# %% Excel-file
numberOfSearchPages = len(listOf_Query_URLs)

listOfQueryTexts = extractQueryTxtsFromURList(listOf_Query_URLs)

writer = pd.ExcelWriter('Experiment Preparations.xlsx') 
#filling up the DICT - base for DataFrame
dataDict = {'Index of search request': range(numberOfSearchPages), 
			'Include in the next experiment?': [False] * numberOfSearchPages, 
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






