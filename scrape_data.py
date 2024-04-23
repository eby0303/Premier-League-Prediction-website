import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
import os
from io import StringIO
import streamlit as st

# Function to scrape data for a given team and season
def scrape_team_data(team_url, season_year):
    data = requests.get(team_url)
    matches = pd.read_html(StringIO(data.text), match="Scores & Fixtures")[0]

    soup = BeautifulSoup(data.text, 'html.parser')
    links = [a['href'] for a in soup.find_all('a') if a and 'href' in a.attrs and 'all_comps/shooting/' in a['href']]

    if links:
        shooting_url = f"https://fbref.com{links[0]}"
        data = requests.get(shooting_url)
        shooting = pd.read_html(StringIO(data.text), match="Shooting")[0]
        shooting.columns = shooting.columns.droplevel()

        # Merge data based on date
        team_data = matches.merge(shooting[["Date", "Sh", "SoT", "Dist", "FK", "PK", "PKatt"]], on="Date")
        team_data = team_data[team_data["Comp"] == "Premier League"]
        team_data["Season"] = season_year
        team_data["Team"] = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")

        return team_data
    else:
        return None

# Function to scrape data for multiple seasons
def scrape_multiple_seasons_data(seasons):
    all_seasons_data = []

    # Scrape data for each season
    for season_year in seasons:
        csv_file_path = f"premier_league_data_{season_year}.csv"
        
        time.sleep(2) 
        # Check if data already exists
        if os.path.exists(csv_file_path):
            st.write(f"Data for season {season_year} already exists.")
            data = pd.read_csv(csv_file_path)
            all_seasons_data.append(data)
            continue
      
        st.write(f"Scraping data for season {season_year}...")
        time.sleep(2)
        st.write("Hang in there....")

        standings_url = f"https://fbref.com/en/comps/9/{season_year}-{season_year + 1}/{season_year}-{season_year + 1}-Premier-League-Stats"
        data = requests.get(standings_url)

        if data.status_code != 200:
            print(f"Failed to retrieve data from {standings_url}. HTTP status code: {data.status_code}")
            continue

        soup = BeautifulSoup(data.text, 'html.parser')

        # Find the standings table
        standings_table = soup.select('table.stats_table')
        if not standings_table:
            print(f"No table with class 'stats_table' found for season {season_year}.")
            continue

        standings_table = standings_table[0]
        team_links = [a['href'] for a in standings_table.find_all('a') if '/squads/' in a['href'] and 'href' in a.attrs]
        team_urls = [f"https://fbref.com{link}" for link in team_links]

        season_data = []

        for team_url in team_urls:
            team_data = scrape_team_data(team_url, season_year)
            if team_data is not None:
                season_data.append(team_data)
            time.sleep(5)  # Adjust the sleep time if needed

        # Combine all team data for the season
        if season_data:
            season_all_data = pd.concat(season_data)
            # Save data to CSV file for the season
            season_all_data.to_csv(csv_file_path, index=False)
            all_seasons_data.append(season_all_data)
        else:
            st.write(f"No data scraped for season {season_year}.")

    # Combine data from all seasons
    if all_seasons_data:
        combined_data = pd.concat(all_seasons_data)
        combined_file_path = "premier_league_data_combined.csv"
        combined_data.to_csv(combined_file_path, index=False)
        return combined_file_path
    else:
        st.write("No data scraped for any season.")
        return None
