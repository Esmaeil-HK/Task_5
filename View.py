import streamlit as st
from pymongo import MongoClient
import pandas as pd

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["logbook_database"]
collection = db["daily_reports"]

# Define app structure
st.set_page_config(layout="wide")

# App title and header
st.title("Logbook Data Query")
st.header("Explore Logbook Data")

# Define query parameters
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")

# Query button
if st.button("Query Data"):
    # Query data from MongoDB based on date range
    query = {
        "date": {
            "$gte": start_date.strftime("%Y-%m-%d"),
            "$lte": end_date.strftime("%Y-%m-%d"),
        }
    }
    cursor = collection.find(query)

    # Convert cursor to DataFrame
    data = pd.DataFrame(list(cursor))

    # Display the queried data
    st.subheader("Queried Data:")
    if not data.empty:
        st.dataframe(data)
    else:
        st.info("No data available for the selected date range.")

    # Download Button for CSV
    st.subheader("Download Data:")
    if not data.empty:
        csv_data = data.to_csv(index=False)
        st.download_button("Download CSV", csv_data, "logbook_data.csv", "text/csv")
    else:
        st.warning("No data available for download.")
