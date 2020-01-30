#!/usr/bin python3
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8

from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import re
from time import sleep
from time import time
from random import randint
from warnings import warn

films = list()
years = list()
imdb_ratings = list()
mt_ratings = list()
votes = list()

# Year and page lists for scrapind
url_years = [str(i) for i in range(2000, 2020)]
pages = [str(i) for i in range(1, 6)]

# Get start time
start_time = time()

# Variable for requests count
requests = 1

for year in url_years:
    for page in pages:
        # Get data from URL
        url = f'http://www.imdb.com/search/title?release_date={year}&sort=num_votes,desc&page={page}'
        response = get(url)

        # Pause the loop for time from 8 to 17 seconds to avoid IMDB's block
        sleep(randint(5, 10))

        # Monitor the requests
        elapsed_time = time() - start_time
        print(f'Request: {requests}; Frequency: {requests / elapsed_time} requests/sec')

        # Throw a warning for non-200 status codes
        if response.status_code != 200:
            warn(f'Request: {requests}; Status code: {response.status_code}')

        # Increment requests counter
        requests += 1

        # Get html data
        html_soup = BeautifulSoup(response.text, 'html.parser')
        # Extract containers with movies
        movie_containers = html_soup.find_all('div', class_='lister-item mode-advanced')

        # Loop for containers from html data and get necessary data to lists
        for container in movie_containers:
            # If the movie has Metascore, then extract:
            if container.find('span', class_="metascore favorable") is not None:
                # Film
                film = container.h3.a.text
                films.append(film)
                # Year
                year = container.h3.find('span', class_='lister-item-year text-muted unbold').text
                year = int(re.sub('[^\d]', '', year))
                years.append(year)
                # IMDB rating
                imdb_rating = float(container.find('div', class_="inline-block ratings-imdb-rating").strong.text)
                imdb_ratings.append(imdb_rating)
                # Metascore
                mt_rating = int(container.find('span', class_="metascore favorable").text)
                mt_ratings.append(mt_rating)
                # number of votes
                vote = int(container.find('span', attrs={'name': 'nv'})['data-value'])
                votes.append(vote)


# dataframe for stroring scraped data
imdb_metascore = pd.DataFrame(columns=['Film', 'Year', 'IMDB', 'Metascore', 'IMDB votes'])
imdb_metascore['Film'] = films
imdb_metascore['Year'] = years
imdb_metascore['IMDB'] = imdb_ratings
imdb_metascore['Metascore'] = mt_ratings
imdb_metascore['IMDB votes'] = votes

imdb_metascore.to_csv('imdb_metascore.csv')
