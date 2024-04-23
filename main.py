import streamlit as st
import pandas as pd
from live_standings import scrape_live_standings
from prediction import make_prediction
from scrape_data import scrape_multiple_seasons_data

# Define the main Streamlit application
def app():


    # Call the scrape_live_standings function to get the live standings data
    live_standings = scrape_live_standings()

   # Display the live Premier League standings
    if live_standings is not None:
        st.title("Live Premier League Standings:")
        st.write(live_standings)
        
        
    # Section for season year input and predictions
    st.title("Season Year and Predictions")

    # Get the season year from the user
    season_year = st.number_input("Enter the season year (e.g., 2023 for the 2023-2024 season):", min_value=2020, max_value=2025, step=1, value=2023)

    # Create a button for making predictions
    if st.button("Make Prediction"):
        # Calculate the two previous seasons based on the user's input season year
        seasons_to_scrape = [season_year - 1, season_year - 2]

        # Call the scrape_multiple_seasons_data function to scrape data for the specified seasons
        csv_file_path = scrape_multiple_seasons_data(seasons_to_scrape)

        # Call the make_prediction function to get the predicted winner
        winner = make_prediction(csv_file_path)

        # Display the predicted winner
        st.subheader(f"The predicted winner of the {season_year}-{season_year + 1} season is: {winner}")


# Run the application
if __name__ == "__main__":
    app()
