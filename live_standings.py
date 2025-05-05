import requests
import pandas as pd
from bs4 import BeautifulSoup

def scrape_live_standings():
    url = "https://fbref.com/en/comps/9/Premier-League-Stats"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/112.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve data from {url}. HTTP status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    standings_table = soup.select_one('table.stats_table')

    if standings_table is None:
        print("No standings table found.")
        return None

    df_standings = pd.read_html(str(standings_table))[0]

    return df_standings
