import streamlit as st
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import BadRequestError
# raouf silly
# Connect to Elasticsearch
es = Elasticsearch(
    ["https://localhost:9200"],
    basic_auth=("elastic", "+YiBKgNPc7Zr5S_poBg-"),
    verify_certs=False,  # Disabling SSL certificate verification (only for testing/development)
)

# List of fields available for search
fields = [
    "date",
    "shift",
    "oil_side.d_01_surge_tank_drained_min",
    "oil_side.d_02_water_tank_drained_min",
    "oil_side.oil_readings",
    "oil_side.wc",
    "oil_side.oil_api",
    "oil_side.condy_api",
    "oil_side.comment_of_oil_side",
    "gas_plant.comment_of_gas_plant",
    "heating_station.whp",
    "heating_station.cp",
    "heating_station.wht",
    "heating_station.chock_size",
    "heating_station.flp",
    "heating_station.flt",
    "heating_station.wc_percent",
    "heating_station.casing_p",
    "heating_station.gas_closing",
    "heating_station.oil_closing",
    "heating_station.comment_of_heating_station",
]

# Streamlit sidebar for selecting multiple fields
st.sidebar.subheader("Filter")
selected_fields = st.sidebar.multiselect("Select fields to compare", fields)

if selected_fields:
    comparison_options = [">", ">=", "<", "<=", "==", "Exact Match"]
    comparison_operators = {}
    query_values = {}
    for field in selected_fields:
        comparison_operators[field] = st.sidebar.selectbox(
            f"Comparison Operator for {field}", comparison_options
        )
        query_values[field] = st.sidebar.text_input(
            f"Enter value to search for {field}", ""
        )

    # Elasticsearch Query for comparison
    try:
        es_query = {
            "query": {
                "bool": {
                    "must": [],
                }
            }
        }

        for field in selected_fields:
            comparison_operator = comparison_operators[field]
            query_value = query_values[field]

            if comparison_operator == "Exact Match":
                es_query["query"]["bool"]["must"].append(
                    {"match_phrase": {f"{field}": query_value}}
                )
            else:
                comparison_dict = {
                    "<": "lt",
                    "<=": "lte",
                    ">": "gt",
                    ">=": "gte",
                    "==": "eq",
                }
                comparison_key = comparison_dict.get(comparison_operator, "eq")

                es_query["query"]["bool"]["must"].append(
                    {
                        "range": {
                            f"{field}": {
                                comparison_key: float(query_value)
                                if query_value == "0"
                                else query_value
                            }
                        }
                    }
                )

        es_results = es.search(index="task5", body=es_query)

        if len(es_results["hits"]["hits"]) == 0:
            st.write("No matching results found.")
        else:
            st.write("Elasticsearch Results:")
            for hit in es_results["hits"]["hits"]:
                st.write(hit["_source"])

    except BadRequestError as e:
        # Handling the specific BadRequestError silently without displaying any message
        if "[range] query does not support [eq]" in str(e):
            es_query = {"query": {"match_phrase": {f"{field}": query_value}}}
            es_results = es.search(index="task5", body=es_query)

            if len(es_results["hits"]["hits"]) == 0:
                st.write("No matching results found.")
            else:
                st.write("Elasticsearch Results (Exact Match):")
                for hit in es_results["hits"]["hits"]:
                    st.write(hit["_source"])
