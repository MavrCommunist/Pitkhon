# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 12:28:08 2021

@author: User
"""
# %% imports
import urllib3
from bs4 import BeautifulSoup
import pymongo
import json

# %% importing data from search-page file
listOf_Query_URLs = list()

with open('searchURLs.txt', 'r', encoding='utf-8') as file:
	listOf_Query_URLs = file.read().splitlines()
print(listOf_Query_URLs)

# %% making text from http request of srcPages
http = urllib3.PoolManager()
http_response = http.request('GET', listOf_Query_URLs[0])
byn_src_page = http_response.data
src_txt = byn_src_page.decode('utf-8')

# %%
soup = BeautifulSoup(src_txt, 'html.parser')

#creating the list of titles
temp_titleTags = soup.find_all('div', {'class' : 'list-title mathjax'})

listOfTitles = [None] * len(temp_titleTags)
for i in range(len(listOfTitles)):
    listOfTitles[i] = temp_titleTags[i].text[8:]
#

#list of urls to annotations
temp_refsToAnnotations = soup.find_all('a', {'title': 'Abstract'})

listOfAnnotURLs = [None] * len(temp_refsToAnnotations)
for i in range(len(listOfAnnotURLs)):
    listOfAnnotURLs[i] = temp_refsToAnnotations[i].get('href')
#

#list of arxiv ids
listOfArxivIDs = [None] * len(listOfAnnotURLs)#[0-9]{4}.[0-9]{5}
for i in range(len(listOfArxivIDs)):
    listOfArxivIDs[i] = listOfAnnotURLs[i][5:]
#

#list of primary subjects
temp_listOfSubjects = soup.find_all('span', {'class': 'primary-subject'})

listOfPrimarySubjects = [None] * len(temp_listOfSubjects)
for i in range(len(listOfPrimarySubjects)):
    listOfPrimarySubjects[i] = temp_listOfSubjects[i].text
#

#list of authors
temp_listOfAutBlocks = soup.find_all('div', {'class': 'list-authors'})

listOfAuthors = [None] * len(temp_listOfAutBlocks)
for i in range(len(listOfAuthors)):
    
    temp_auTags = temp_listOfAutBlocks[i].find_all('a')
    #author tags/ first is span
    
    for auTag in temp_auTags:
        if listOfAuthors[i] == None or listOfAuthors[i] == '':
            listOfAuthors[i] = auTag.text
        else:
            listOfAuthors[i] += ', ' + auTag.text
#       

#list of annotations REWORK
listOfAnnotations = [None] * len(listOfAnnotURLs)

for i in range(len(listOfAnnotURLs)):
    hr_artPage = http.request('GET', 'https://export.arxiv.org' + listOfAnnotURLs[i])
    articleMarkup = hr_artPage.data.decode('utf-8')
    soupFromArticle = BeautifulSoup(articleMarkup, 'html.parser')
    listOfAnnotations[i] = soupFromArticle.find('blockquote', {'class': 'abstract mathjax'}).text[10:]
#

listOfArticles = [None] * len(listOfAnnotations)
for i in range(len(listOfArticles)):
    listOfArticles[i] = {
        'title': listOfTitles[i],
        '_id': listOfArxivIDs[i],
        'authors': listOfAuthors[i],
        'subject': listOfPrimarySubjects[i],
        'annotation': listOfAnnotations[i]
            }
#List of Documents is ready to insert 




conn_str = 'mongodb://localhost:27017'


client = pymongo.MongoClient(conn_str)
db = client.pyArxivBase
collection = db.pyArxivCollection

for articleDoc in listOfArticles:
    collection.insert_one(articleDoc)
