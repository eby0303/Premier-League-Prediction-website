import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score
import streamlit as st

# Define the prediction function
def make_prediction(csv_file_path, season_year=None):
    # Load the data from the CSV file
    matches = pd.read_csv(csv_file_path)
    
    # Display the loaded data
    st.write(matches)
    
    # Convert 'Date' column to datetime
    matches["Date"] = pd.to_datetime(matches["Date"])

    # Create target column for match results (1 for win, 0 otherwise)
    matches["target"] = matches["Result"].apply(lambda result: 1 if result == "W" else 0)
    
    # Encode categorical columns as numerical values
    matches["venue_code"] = matches["Venue"].astype("category").cat.codes
    matches["opp_code"] = matches["Opponent"].astype("category").cat.codes
    
    # Extract the hour from the 'Time' column and convert it to integer
    matches["hour"] = matches["Time"].str.extract(r"(\d+):").astype(int)
    
    # Get the day of the week from 'Date'
    matches["day_code"] = matches["Date"].dt.dayofweek
    
    # Define the list of predictors
    predictors = ["venue_code", "opp_code", "hour", "day_code"]
    
    # Columns for rolling averages
    cols = ["GF", "GA", "Sh", "SoT", "Dist", "FK", "PK", "PKatt"]
    new_cols = [f"{col}_rolling" for col in cols]
    
    # Calculate rolling averages for each team
    def calculate_rolling_averages(group):
        group = group.sort_values("Date")
        rolling_stats = group[cols].rolling(window=3, closed="left").mean()
        group[new_cols] = rolling_stats
        return group.dropna(subset=new_cols)
    
    # Apply rolling averages to each group (team)
    matches = matches.groupby("Team").apply(calculate_rolling_averages)
    matches = matches.reset_index(drop=True)
    
    # Update predictors list with the new rolling average columns
    predictors.extend(new_cols)
    
    # Determine the train-test split dynamically based on the latest date in the data
    if season_year:
        # If season_year is provided, use the season year for filtering data
        season_start = f"{season_year}-01-01"
    else:
        # Otherwise, use the last date in the dataset to determine the train-test split
        season_start = matches["Date"].max() - pd.DateOffset(years=1)
    
    train_data = matches[matches["Date"] < season_start]
    test_data = matches[matches["Date"] >= season_start]
    
    st.write("Train data shape:", train_data.shape)
    st.write("Test data shape:", test_data.shape)

    # Initialize the Random Forest Classifier
    rf = RandomForestClassifier(n_estimators=50, min_samples_split=10, random_state=1)
    
    # Train the model using the train data and predictors
    rf.fit(train_data[predictors], train_data["target"])
    
    # Make predictions using the test data and predictors
    preds = rf.predict(test_data[predictors])
    
    # Calculate the precision score
    precision = precision_score(test_data["target"], preds)
    
    # Display the precision score
    st.write("Model Precision Score:", precision)
    
    # Combine the actual and predicted results
    combined_results = pd.DataFrame({
        "actual": test_data["target"],
        "predicted": preds,
        "Team": test_data["Team"]
    })
    
    # Calculate the predicted winner based on predicted win probabilities
    win_probabilities = combined_results.groupby("Team")["predicted"].mean()
    predicted_winner = win_probabilities.idxmax()
    

    return predicted_winner