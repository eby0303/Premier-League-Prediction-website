def make_prediction(csv_file_path, season_year=None, return_details=False):
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import precision_score
    import streamlit as st
    import time

    matches = pd.read_csv(csv_file_path)

    time.sleep(3)
    st.write("Getting your prediction...")

    matches["Date"] = pd.to_datetime(matches["Date"])
    matches["target"] = matches["Result"].apply(lambda result: 1 if result == "W" else 0)
    matches["venue_code"] = matches["Venue"].astype("category").cat.codes
    matches["opp_code"] = matches["Opponent"].astype("category").cat.codes
    matches["hour"] = matches["Time"].str.extract(r"(\d+):").astype(int)
    matches["day_code"] = matches["Date"].dt.dayofweek

    predictors = ["venue_code", "opp_code", "hour", "day_code"]

    cols = ["GF", "GA", "Sh", "SoT", "Dist", "FK", "PK", "PKatt"]
    new_cols = [f"{col}_rolling" for col in cols]

    def calculate_rolling_averages(group):
        group = group.sort_values("Date")
        rolling_stats = group[cols].rolling(window=3, closed="left").mean()
        group[new_cols] = rolling_stats
        return group.dropna(subset=new_cols)

    matches = matches.groupby("Team").apply(calculate_rolling_averages)
    matches = matches.reset_index(drop=True)

    predictors.extend(new_cols)

    if season_year:
        season_start = f"{season_year}-01-01"
    else:
        season_start = matches["Date"].max() - pd.DateOffset(years=1)

    train_data = matches[matches["Date"] < season_start]
    test_data = matches[matches["Date"] >= season_start]

    rf = RandomForestClassifier(n_estimators=50, min_samples_split=10, random_state=1)
    rf.fit(train_data[predictors], train_data["target"])
    preds = rf.predict(test_data[predictors])

    precision = precision_score(test_data["target"], preds)

    st.write("Model Precision Score:", precision)

    combined_results = pd.DataFrame({
        "actual": test_data["target"],
        "predicted": preds,
        "Team": test_data["Team"]
    })

    win_probabilities = combined_results.groupby("Team")["predicted"].mean()
    predicted_winner = win_probabilities.idxmax()

    if return_details:
        return predicted_winner, precision, win_probabilities
    else:
        return predicted_winner
