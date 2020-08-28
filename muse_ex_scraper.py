import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re

# start urls
urls = ["https://www.crma.org/exhibitions/current", "https://www.crma.org/exhibitions/upcoming", "https://www.crma.org/exhibitions/past"]
# urls for each exhibit
exhibit_urls = []
# exhibit titles, dates, details
titles = []
dates = []
details = []
data = []
# make sure its in english
headers = {"Accept-Language": "en-US, en;q=0.5"}
# iterate through the starting urls
for url in urls:
    # get the html
    results = requests.get(url, headers=headers)
    # get the soup to analyze
    soup = BeautifulSoup(results.text, "html.parser")
    # to separate the exhibits
    exhibit_div = soup.find_all('a', class_='feature')
    # iterate through all the exhibits
    for exhibit in exhibit_div:
        # the link of the exhibit
        exhibit_url = exhibit.get('href')
        #exhibit_urls.append(exhibit_url)
        # get the soup for the particular exhibit
        results = requests.get(exhibit_url, headers=headers)
        soup_exhibit = BeautifulSoup(results.text, "html.parser")
        # now we need to extract date, description, pictures, etc.

        # grab title using regular expressions to separate the class title and the tag
        title = soup_exhibit.find(class_="text").find(re.compile("^h")).text if soup_exhibit.find(class_="text").find(re.compile("^h")) else ''
        # get all descendent and paragraph tags from the date and description section
        date_and_description = soup_exhibit.find(class_="text").find_all('p')
        date_and_description_text = ''

        for tag in date_and_description:
            # not all separated by new line character, some have more paragraphs than others, some don't seperate
            # the date and details in different paragraphs
            date_and_description_text = date_and_description_text + tag.text
        #datez = date_detail.split("\n")[0]

        data_for_exhibit = [exhibit_url, title, date_and_description_text]
        data.append(data_for_exhibit)


# make dataframe
df = pd.DataFrame(data, columns = ['url', 'title', 'date and description'])
#print(df)

# transfer to csv
df.to_csv('exhibits.csv')


# think about preprocesssing text,
# get more general information to process, then deal with it?

#TODO
# grab pictures, make an attribute the main page, museum, location