import numpy as np
import pandas as pd
import streamlit as st

DATE_COLUMN = "date/time"
DATA_URL = (
    "https://s3-us-west-2.amazonaws.com/"
    "streamlit-demo-data/uber-raw-data-sep14.csv.gz"
)


@st.cache
def load_data(nrows: int) -> pd.DataFrame:
    data = pd.read_csv(DATA_URL, nrows=nrows)

    def lowercase(x):
        return str(x).lower()

    data.rename(lowercase, axis="columns", inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


st.title("Uber pickups in NYC")

# Load data
data_load_state = st.text("Loading data...")
data = load_data(10000)
data_load_state.text("Done! (using st.cache)")

# Show raw data
if st.checkbox("Show raw data"):
    st.subheader("Raw data")
    st.write(data)

# Show histgram
st.subheader("Number of pickups by hour")
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
st.bar_chart(hist_values)

# Show map
hour_to_filter = st.slider("hour", 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f"Map of all pickups at {hour_to_filter}:00")
st.map(filtered_data)
