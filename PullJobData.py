#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 09:30:50 2021

@author: chasebrown
"""

import requests
import pandas as pd
import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
import plotly.express as px
import plotly.io as pio
pio.renderers.default='browser'

import random as rand
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import re
from nltk.corpus import stopwords

"""import nltk
nltk.download('stopwords')"""


headers = {
        'x-rapidapi-key': "key",
        'x-rapidapi-host': "host"
        }

def searchIndeed(query, page):
    url = "https://job-search4.p.rapidapi.com/indeed/search"

    querystring = {"query":query,"page":page}

    response = requests.request("GET", url, headers=headers, params=querystring)

    dic = json.loads(response.text)

    return pd.DataFrame.from_dict(dic['jobs'])


# -------- Get the Data ----------

#From API
termsOfInterest = ["AWS", "Amazon Web Services", "Data Science", "AI", "Machine Learning", "AWS Machine Learning", "AWS Data Science", "AWS Solutions Architect", "AWS AI"]
listings = pd.DataFrame()

for term in termsOfInterest:
    for page in range(1,15):
        try:
            listings = listings.append(searchIndeed(term + " Remote", page))
            print("Done with: ", term, " | Page ", page)
        except Exception as e:
            print("Failed at: ", term, " | Page ", page)
            print(e)


#Scraping the full descriptions

counter = 0
WINDOW_SIZE = "1720,1080"

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)

browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)


for index, row in listings.iterrows():
    try:
        url = row['detail_url']

        browser.get(url)

        time.sleep(1 + rand.uniform(0, 1)*2)

        item = browser.find_element_by_id("jobDescriptionText")

        row['description'] = item.text
        print(item.text)
        time.sleep(1 + rand.uniform(0, 1)*2)


    except Exception as e:
        print(row)
        print(e)
    counter += 1
    print(counter, " of ", len(listings))

#Pull Salaries from Descriptions

minSalaries = []
maxSalaries = []
averageSalaries = []

for index, row in listings.iterrows():
    words = row['description'].replace('-', ' ').split()
    numbers = []
    for word in words:
        if '$' in word:
            noCents = word.split('.')[0].replace('K', '000')
            try:
                cleanedInt = int(re.sub('[^0-9]+', '', noCents).strip(' '))
                if cleanedInt > 20000:
                    numbers.append(cleanedInt)
                elif cleanedInt < 100:
                    numbers.append(cleanedInt*2080)
            except:
                print(noCents)
    if len(numbers)>0:
        minSalaries.append(min(numbers))
        maxSalaries.append(max(numbers))
        averageSalaries.append(sum(numbers) / len(numbers))
    else:
        minSalaries.append(None)
        maxSalaries.append(None)
        averageSalaries.append(None)

    print("----------------------------")

listings["Min Salary"] = minSalaries
listings["Max Salary"] = maxSalaries
listings["Average Salary"] = averageSalaries


# ------- Save Data for Later Use --------- #

listings.to_csv('jobListings.csv', index=False)

# ------- Make Some Graphs ------

# 1. Remote/Not Remote Graph

labels = ["Remote", "Not Remote"]
counts = [0, 0]
explode = [0.1, 0]
colors = ['#99ff99', '#ff9999']

for index, row in listings.iterrows():
    if row['location'] == "Remote":
        counts[0] += 1
    else:
        counts[1] += 1

fig1, ax1 = plt.subplots()

fig1.set_dpi(300)

plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"

ax1.pie(counts, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
        shadow=False, startangle=90)
# Equal aspect ratio ensures that pie is drawn as a circle
ax1.axis('equal')
plt.tight_layout()
plt.show()


# 2. State and City Frequency

frequencyState = {}
frequencyCity = {}

for index, row in listings.iterrows():
    if row['state'] == None:
        pass
    else:
        if row['state'] in frequencyState.keys():
            frequencyState[row['state']] += 1
        else:
            frequencyState.update({row['state']: 1})

    if row['city'] == None:
        pass
    else:
        if row['city'] in frequencyCity.keys():
            frequencyCity[row['city']] += 1
        else:
            frequencyCity.update({row['city']: 1})

labelsState = []
countsState = []
for label in frequencyState.keys():
    labelsState.append(label)
    countsState.append(frequencyState[label])

labelsCity = []
countsCity = []
for label in frequencyCity.keys():
    if frequencyCity[label] > 1:
        labelsCity.append(label)
        countsCity.append(frequencyCity[label])



sns.set(style="whitegrid")

plt.figure(2, figsize=(20,15))
the_grid = GridSpec(2, 2)


plt.subplot(the_grid[0, 1])
plt.title('Postings by State', fontweight='bold')
sns.barplot(x=labelsState,y=countsState, palette='Spectral')
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"
plt.xticks(rotation=90)


plt.subplot(the_grid[0, 0])
plt.title('Postings by City', fontweight='bold')

sns.barplot(x=labelsCity,y=countsCity, palette='Spectral')
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"
plt.xticks(rotation=90)

plt.suptitle('Job Postings by Location', fontsize=16, fontweight='bold')

# 3 Treemap of companies by % remote

companyFrequencies = {}

for index, row in listings.iterrows():

    if row['company_name'] == None:
        pass
    else:
        if row['company_name'] in companyFrequencies.keys():
            companyFrequencies[row['company_name']][0] += 1
        else:
            companyFrequencies.update({row['company_name']: [1, 0, []]})


    if row['location'] == "Remote":
        companyFrequencies[row['company_name']][1] += 1

    companyFrequencies[row['company_name']][2].append(row['Average Salary'])


df = pd.DataFrame()

for key in companyFrequencies.keys():
    avgSalary = 0
    count = 0
    for salary in companyFrequencies[key][2]:
        if not salary == None:
            avgSalary += salary
            count += 1
    avgSalary = avgSalary/count
    formatted_float = "${:,.2f}".format(avgSalary)
    if formatted_float == "$nan":
        formatted_float = ""
    df2 = {'Company Name': key, 'Number of Postings': companyFrequencies[key][0], '% Remote': companyFrequencies[key][1]/companyFrequencies[key][0], 'Average Salaries': formatted_float}
    df = df.append(df2, ignore_index = True)



fig = px.treemap(df,
                 path=['Company Name', 'Average Salaries'],
                 values='Number of Postings',
                 color='% Remote')
fig.show()

# 4 Keyword Word Map from Descriptions

wordFrequency = {}

stop_words = list(stopwords.words('english'))


for index, row in listings.iterrows():

    words = row['description'].split()
    cleanWords = []
    for word in words:
        word = word.lower()
        if not word.strip() in stop_words:
            cleanWords.append(re.sub('[^A-Za-z0-9]+', ' ', word).strip())

    for word in cleanWords:
        word = word.lower()
        if not word.strip() == "":
            if word in wordFrequency.keys():
                wordFrequency[word] += 1
            else:
                wordFrequency.update({word: 1})

wordcloud = WordCloud()
wordcloud.generate_from_frequencies(frequencies=wordFrequency)
plt.figure(figsize=(80, 80))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
