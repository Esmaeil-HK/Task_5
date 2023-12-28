import streamlit as st
from pymongo import MongoClient
import datetime

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["logbook_database"]
collection = db["daily_reports"]


def save_report(report):
    # Save report to MongoDB
    collection.insert_one(report)


# Define app structure
st.set_page_config(layout="wide")

st.title("Daily Logbook")
st.header("Details:")
col1, col2, col3 = st.columns(3)
with col1:
    name = st.text_input("Operator Name")
with col2:
    date = st.date_input("Date", value=datetime.date.today())
with col3:
    Time = st.time_input("TIme", value=datetime.datetime.now())
shift = st.selectbox("Shift", ["Day", "Night"])


st.header("Oil Side:")
st.caption("D_01 Surge Tank:")
col1, col2 = st.columns(2)
with col1:
    drain_check1 = st.checkbox("Surge Tank was drained")
    d_01_surge_tank_drained_min = 0  # Initialize the variable here

with col2:
    if drain_check1:
        d_01_surge_tank_drained_min = st.number_input("Time of Draining (D1) (min)")

st.caption("D_02 Water Tank:")
col1, col2 = st.columns(2)
with col1:
    drain_check2 = st.checkbox("Water Tank was drained")
    d_02_water_tank_drained_min = 0  # Initialize the variable here

with col2:
    if drain_check2:
        d_02_water_tank_drained_min = st.number_input("Time of Draining (D2) (min)")


col1, col2, col3, col4 = st.columns(4)
with col1:
    oil_readings = st.number_input("Oil Readings")
with col2:
    wc_input = st.number_input("W/C")
with col3:
    oil_api_input = st.number_input("Oil API")
with col4:
    condy_api_input = st.number_input("Condy API")


# add_comment_one = st.button('Add Comment ➕',help='Add Comment regarding Oil side')
# if add_comment_one:
st.caption("Adding comment:")
col1, col2, col3 = st.columns(3)
with col1:
    Time_of_comment_Oil_plant = st.time_input(
        "Add Time ", value=datetime.datetime.now(), help="For oil side comment"
    )
oil_side_comment = st.text_area("Comment")
if st.button("Submit 1"):
    st.success(f"Comment Submitted: {oil_side_comment}")


st.header("Gas Plant:")
# add_comment_two = st.button('Add Comment ➕',help='Add Comment regarding Gas Plany')
# if add_comment_two:
col1, col2, col3 = st.columns(3)
with col1:
    Time_of_comment_Gas_Plant = st.time_input(
        "Add Time", value=datetime.datetime.now(), help="For gas plant comment"
    )
gas_plant_comment = st.text_area("Comment", help="add comment for gas plant")
if st.button("Submit 2"):
    st.success(f"Comment Submitted: {gas_plant_comment}")


st.header("Heating Station:")
col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 2])
with col1:
    whp = st.number_input("WHP (psi)")
with col2:
    cp = st.number_input("CP (psi)")
with col3:
    wht = st.number_input("WHT (Fehr)")
with col4:
    flt = st.number_input("FLT")
with col5:
    flp = st.number_input("FLP (psi)")

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    chock_size = st.number_input("Chock Size")
with col2:
    wc_percent = st.number_input("WC (%)")
with col3:
    casing_p = st.number_input("Casing P")
with col4:
    gas_closing = st.number_input("Gas Closing")
with col5:
    oil_closing = st.number_input("Oil Closing")

with col1:
    Time_of_comment_heating_station = st.time_input(
        "Add Time", value=datetime.datetime.now(), help="For Heating Statione comment"
    )
heating_station_comment = st.text_area(
    "Comment", help="add comment for heating station"
)
if st.button("Submit 3"):
    st.success(f"Comment Submitted: {heating_station_comment}")

# Submit report
if st.button("Submit Report"):
    report = {
        "name": name,
        "date": date.strftime("%Y-%m-%d"),
        "shift": shift,
        "oil_side": {
            "d_01_surge_tank_drained_min": d_01_surge_tank_drained_min,
            "d_02_water_tank_drained_min": d_02_water_tank_drained_min,
            "oil_readings": oil_readings,
            "wc": wc_input,
            "oil_api": oil_api_input,
            "condy_api": condy_api_input,
            "comment_of_oil_side": oil_side_comment,
        },
        "gas_plant": {
            "comment_of_gas_plant": gas_plant_comment,
        },
        "heating_station": {
            "whp": whp,
            "cp": cp,
            "wht": wht,
            "chock_size": chock_size,
            "flp": flp,
            "flt": flt,
            "wc_percent": wc_percent,
            "casing_p": casing_p,
            "gas_closing": gas_closing,
            "oil_closing": oil_closing,
            "comment_of_heating_station": heating_station_comment,
        },
    }
try:
    save_report(report)
    st.success("Report submitted successfully!")
except:
    pass
