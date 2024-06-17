# Streamlit Data Analysis App

This Streamlit app analyzes survey data related to syrup purchases and sales volumes. The app provides insights into different purchase types and sales volumes across various store types.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Data](#data)
- [License](#license)

## Introduction

This Streamlit app presents data analysis results from a survey about syrup purchases. It offers visualizations and insights into different purchase behaviors and sales volumes in branded and non-branded stores.

## Features

- **Introduction Page**: A brief introduction to the app and its purpose.
- **Analysis 1**: Visualizes the counts and percentages of different purchase types.
- **Analysis 2**: Provides a detailed analysis of sales volumes per day for different purchase types across branded and non-branded stores.

## Installation

To run this app, you need to have Python and pip installed. Follow the steps below to set up and run the app:

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/streamlit-data-analysis-app.git
    cd streamlit-data-analysis-app
    ```

2. **Install the required packages**:
    ```sh
    pip install streamlit pandas altair
    ```

3. **Place the data file**:
    Ensure you have the `data.csv` file in the `data` directory. If you have a different data file, adjust the file path in the code accordingly.

## Usage

To run the app, navigate to the project directory and use the following command:

```sh
streamlit run app.py
