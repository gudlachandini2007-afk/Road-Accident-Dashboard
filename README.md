# Traffic Accident Probability Analysis Dashboard

## Project Overview

This project analyzes road accident data using probability and data visualization techniques.

The project focuses on understanding accident patterns based on factors such as:

- Weather conditions
- Accident causes
- Accident severity
- City
- Time of occurrence

An interactive Streamlit dashboard was developed to present the analysis in an easy-to-understand visual format.

## Objectives

- Clean and analyze the road accident dataset.
- Calculate basic and conditional probabilities.
- Study the relationship between weather conditions and accident severity.
- Analyze major causes of recorded accidents.
- Create interactive visualizations.
- Provide a probability explorer through the dashboard.
- Present the results using an interactive web application.

## Technologies Used

- Python
- Pandas
- Plotly
- Streamlit
- Google Colab
- GitHub
- Render

## Dataset

The dataset contains recorded road accident information including:

- City
- Weather condition
- Accident cause
- Accident severity
- Date and time information
- Other accident-related attributes

The dataset was cleaned before performing the analysis.

## Data Processing

The following steps were performed:

1. Loaded the accident dataset.
2. Checked the structure and data types.
3. Handled missing and inconsistent values.
4. Removed duplicate records.
5. Prepared the data for probability analysis.
6. Created visualizations to identify patterns and distributions.

## Probability Analysis

The project uses:

### Basic Probability

The proportion of recorded accidents belonging to different categories was calculated.

### Conditional Probability

Conditional probability was used to analyze accident severity under different weather conditions.

For example:

- Probability of a fatal accident given clear weather.
- Probability of a fatal accident given rainy weather.
- Probability of a fatal accident given foggy weather.

### Bayes' Theorem

Bayes' theorem was also used to understand the probability of a weather condition given a particular accident severity.

## Dashboard Features

The Streamlit dashboard provides:

- Interactive city filtering
- Weather-based filtering
- Accident statistics
- Accident severity visualization
- Accident cause analysis
- Hourly accident analysis
- Conditional probability analysis
- Probability explorer
- Interactive Plotly charts
- Data tables

## Dashboard Structure

```text
Road-Accident-Dashboard/
│
├── .streamlit/
│   └── config.toml
│
├── data/
│   ├── cause_counts.csv
│   ├── cleaned_accidents.csv
│   └── conditional_severity_by_weather.csv
│
├── app.py
├── requirements.txt
└── README.md


Running the Project Locally

Clone the repository:

git clone https://github.com/YOUR-USERNAME/Road-Accident-Dashboard.git

Open the project folder:

cd Road-Accident-Dashboard

Install the required libraries:

pip install -r requirements.txt

Run the Streamlit application:

python -m streamlit run app.py

The dashboard will open in your browser.

Deployment

The Streamlit dashboard is deployed using Render.

Live Dashboard:

https://road-accident-dashboard.onrender.com

Important Interpretation Note

The probabilities in this project represent proportions within the recorded accident dataset.

They should not be interpreted as the actual probability of having an accident during a particular trip or on a particular day.

The analysis identifies patterns and relationships in the recorded data. It does not establish that weather conditions or other variables directly cause accidents.

Conclusion

This project demonstrates how probability, conditional probability, Bayes' theorem, data analysis, and interactive visualization can be applied to a road accident dataset.

The interactive dashboard makes it easier to explore accident patterns and understand the results of the probability analysis.


### One small change

In this line:

```text
https://github.com/YOUR-USERNAME/Road-Accident-Dashboard.git
