import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import statsmodels.api as sm
# Load the dataset
data = pd.read_csv('BSS_Data_Edited.csv')

# App Title and Description
st.title("Interactive Retail Data Exploration App")
st.write("Explore patterns in the data ")


# Sidebar Filters
st.sidebar.header("Filter Options")   #give a title for the sidebar menu


# Sidebar Filters for Numerical Variables

data['salesdate'] = pd.to_datetime(data['salesdate']).dt.date

# Sidebar date range slider
Date_range = st.sidebar.slider(
    "Select Date Range",
    min_value=min(data['salesdate']),
    max_value=max(data['salesdate']),
    value=(min(data['salesdate']), max(data['salesdate'])))



Price_range = st.sidebar.slider("Price", int(data['price'].min()), int(data['price'].max()), (10, 40))
# create a slider, and tentatively show a range from 5 to 35


# Filter data based on selections
filtered_data = data[
    (data['profit'].between(-92,158)) &
    (data['new_profit_Plastic'].between(-830,1415)) &
    (data['new_profit_Wood'].between(-806,1420)) 
   
]

# Show filtered data if user selects the option
if st.sidebar.checkbox("Show Filtered Data"):
    st.write(filtered_data)

## Add a histogram
# Section: Distribution of Hours Worked per Week
st.header("Comparison of cogs by material")
st.write("This histogram shows the distribution of the different cogs.")

# Plot histogram
fig, ax = plt.subplots()
sns.histplot(filtered_data[['cogs','cogs-Plastic_Price','cogs-Wood_Price']], bins=20, color='skyblue', kde=False, ax=ax)
ax.set_title("Histogram of cogs")
ax.set_xlabel("Price")
ax.set_ylabel("Count")
st.pyplot(fig)


## Add a correlation matrix

# Section: Correlation Matrix
st.header("Correlation Matrix")
st.write("Check the box to view the correlation matrix for numerical variables.")

continuous_vars = ['price', 'unitsordered', 'sales', 'cogs', 'fba', 'reffee', 'adspend', 'profit', 'comp_1_price', 'comp_2_price', 'min_price', 'max_price', 'Wood_Price', 'Plastic_Price', 'cogs-Wood_Price', 'cogs-Plastic_Price', 'new_profit_Plastic', 'new_profit_Wood']

# Show correlation matrix
if st.checkbox("Show Correlation Matrix"):
    corr_matrix = filtered_data[continuous_vars].corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)


# Adding a Scatter Plot
# Section: Scatter Plot - Experience vs. Hours Worked per Week
st.header("Scatter Plot: Price  vs. Salesdate")
st.write("Check the box below to add a trendline to the scatter plot.")
show_trendline = st.checkbox("Show Trendline", value=False)

fig = px.scatter(filtered_data, x='price', y='salesdate', title="Price vs. Salesdate",
                 labels={"price": "price", "salesdate": "salesdate(yyyy/mm/dd)"},
                 trendline="ols" if show_trendline else None)
st.plotly_chart(fig)
