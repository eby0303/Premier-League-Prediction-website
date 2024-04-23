import requests
import pandas as pd
from bs4 import BeautifulSoup

# Function to scrape live Premier League standings data
def scrape_live_standings():
    # URL for the Premier League stats page
    url = "https://fbref.com/en/comps/9/Premier-League-Stats"

    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve data from {url}. HTTP status code: {response.status_code}")
        return None

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the live standings table
    standings_table = soup.select_one('table.stats_table')

    if standings_table is None:
        print("No standings table found.")
        return None

    # Convert the HTML table to a DataFrame
    df_standings = pd.read_html(str(standings_table))[0]

    # Return the DataFrame containing the live standings data
    return df_standings
