# This creates the page for displaying data visualizations.

import streamlit as st
import json
import matplotlib.pyplot as plt
import pandas as pd

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Coffee Shop Sales Dashboard")
st.write("Explore coffee sales throughout the week!")


# PART 1: GRAPHS FROM data.json
with open("data.json", "r") as file:
    data = json.load(file)

drinks = []
totals = []

for drink in data:
    drinks.append(drink)
    totals.append(sum(data[drink]["sales"]))

fig, ax = plt.subplots()

ax.bar(drinks, totals)
ax.set_title("Weekly Coffee Sales")
ax.set_xlabel("Coffee Type")
ax.set_ylabel("Cups Sold")

st.pyplot(fig)

st.header("Daily Coffee Sales")
if "selected_drink" not in st.session_state:
    st.session_state.selected_drink = drinks[0]

st.selectbox(
    "Choose a coffee",
    drinks,
    key="selected_drink"
)
choice = st.session_state.selected_drink
daily_sales = data[choice]["sales"]

st.line_chart(daily_sales)
# PART 2: GRAPHS FROM data.csv

st.header("Coffee Preferences Survey Results")

# Read the CSV file
df = pd.read_csv("data.csv")

# Convert the Value column into numbers
df["Value"] = pd.to_numeric(df["Value"], errors="coerce")

# Remove rows with missing or invalid values
df = df.dropna(subset=["Category", "Value"])

if not df.empty:

    # STATIC GRAPH
    st.subheader("Average Price by Coffee Type")

    averages = df.groupby("Category")["Value"].mean()

    fig2, ax2 = plt.subplots()

    ax2.bar(averages.index, averages.values)
    ax2.set_title("Average Price by Coffee Type")
    ax2.set_xlabel("Coffee Type")
    ax2.set_ylabel("Average Price ($)")

    st.pyplot(fig2)

    # DYNAMIC GRAPH
    st.subheader("Prices for a Selected Coffee")

    coffee_options = sorted(df["Category"].unique())

    if "csv_selected_drink" not in st.session_state:
        st.session_state.csv_selected_drink = coffee_options[0]

    st.selectbox(
        "Select a coffee type",
        coffee_options,
        key="csv_selected_drink"
    )

    selected = st.session_state.csv_selected_drink

    filtered = df[df["Category"] == selected]

    fig3, ax3 = plt.subplots()

    ax3.scatter(range(1, len(filtered) + 1), filtered["Value"])
    ax3.set_title("Individual Prices for " + selected)
    ax3.set_xlabel("Response Number")
    ax3.set_ylabel("Price ($)")

    st.pyplot(fig3)

else:
    st.warning("Please submit some valid survey responses first.")

