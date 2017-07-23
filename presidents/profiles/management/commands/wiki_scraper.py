from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

BASE_DIR = 'https://en.wikipedia.org/wiki/List_of_Presidents_of_the_United_States'


def parse_president_wiki():
    """
    BS4 Scraper for the presidential wiki table here:
    https://en.wikipedia.org/wiki/List_of_Presidents_of_the_United_States
   """
    
    r = requests.get(BASE_DIR)
    soup = BeautifulSoup(r.text, 'html.parser')
    speeches_soup = soup.find_all("table")[1]
    df = pd.read_html(str(speeches_soup), header=1, parse_dates=True, flavor='bs4')
    return df


def extract_party(party):
    """Helper for cleaning party data"""
    pattern = re.compile(r'''
                          ([a-zA-Z]+[\-\s]?[a-zA-Z]+){1,2}
                          (.*)
                         ''', re.VERBOSE)
    match = pattern.search(party)
    result = match.group(0).replace("- ", "-").strip()
    return result


def parse():
    # Pull out a noisy dataframe
    df = parse_president_wiki()[0]

    df = df.dropna(thresh=4)  # drops noise from the HTML table
    sub_df = df['Unnamed: 6']
    df = df['Party[c]']
    df = df.dropna().reset_index().drop(44)['Party[c]'].reset_index()
    df.columns = ['index', 'president']  # renames columns

    # Pattern for extracting presidential lifespan datafrom the name cell
    pattern = re.compile(r"""
                ((?:\w+\.?\s)+)               # name
                (\d{4}).(\d{4})?.*            # dates
                (\d{2})\syears                # age
                .*$                           # garbage
                """, re.X)

    # Shapes the data into reliable tuples
    presidents = list()
    for ps in df.itertuples():
        q = ps.president
        match = pattern.search(q)
        presidents.append(match.groups())

    # Cleans out some noise in the name cell
    presidents = [(n.replace("Born", "").strip(), *ps) for n, *ps in presidents]

    presidents = [[i + 1, *ps, extract_party(str(sub_df.iloc[i]))] for i, ps in enumerate(presidents)]

    # Some finishing touches
    presidents[0][-1] = None
    presidents[9][-1] = "Whig"
    presidents[15][-1] = "Republican National Union"
    presidents[16][-1] = "National Union"
    presidents[44][-1] = "Republican"

    return presidents
