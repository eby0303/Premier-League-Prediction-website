# Premier League Winner Prediction and Live Standings

Welcome to the Premier League Winner Prediction and Live Standings project! This project allows users to predict the winner of a specified Premier League season and view the live standings of the current Premier League season.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Data Collection](#data-collection)
- [Setup](#setup)
- [Usage](#usage)
- [Contributing](#contributing)


## Overview

The project is a Streamlit application that provides the following features:

- Predicts the winner of a specified Premier League season using historical data and a Random Forest model.
- Scrapes data for multiple seasons and combines them for model training and prediction.
- Displays live standings of the current Premier League season.


## Features

- **Premier League Winner Prediction**: Allows users to predict the winner of a specified season based on historical data and a Random Forest model.


![image](https://github.com/eby0303/PL_prediction/assets/86768805/f70e7eec-dfc0-4735-8e13-6d3f5b4331fc)

![image](https://github.com/eby0303/PL_prediction/assets/86768805/e3131620-6093-492b-9aef-c023af0ea292)

## Data Collection

- The historical data used for the Premier League winner prediction is collected from [FBref](https://fbref.com/), a reliable source for sports statistics.
- The prediction model is based on a Random Forest algorithm, which uses the collected data to forecast the winner of the specified Premier League season.

## Setup

To run the application locally, follow these steps:

1. **Clone the repository**:
    ```shell
    git clone https://github.com/eby0303/PL_prediction.git
    ```

2. **Navigate to the project directory**:
    ```shell
    cd your-repo
    ```

3. **Create and activate a virtual environment**:
    ```shell
    python -m venv venv
    source venv/bin/activate
    ```

4. **Install the project dependencies**:
    ```shell
    pip install -r requirements.txt
    ```

5. **Run the Streamlit application**:
    ```shell
    streamlit run main.py
    ```

## Usage

After running the application, the Streamlit interface will open in a web browser. You can interact with the application to:

- Predict the winner of a Premier League season.
- View the live standings of the current season.
- See the top 3 goal scorers.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix:
    ```shell
    git checkout -b my-feature-branch
    ```
3. Commit your changes:
    ```shell
    git commit -m "Add new feature or fix a bug"
    ```
4. Push your changes to your fork:
    ```shell
    git push origin my-feature-branch
    ```
5. Create a pull request to the original repository.

