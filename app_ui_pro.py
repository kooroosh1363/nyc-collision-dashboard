import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

st.set_page_config(page_title="NYC Collision Dashboard", layout="wide")

@st.cache_data
def load_data(path='data/collisions.csv'):
    df = pd.read_csv(path, low_memory=False)
    df.columns = df.columns.str.strip()
    df['DATETIME'] = pd.to_datetime(df['DATE'] + ' ' + df['TIME'], errors='coerce')
    df['HOUR'] = df['DATETIME'].dt.hour
    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
    df['WEEK'] = df['DATE'].dt.isocalendar().week
    df['MONTH'] = df['DATE'].dt.month
    df['YEAR'] = df['DATE'].dt.year
    return df

# Sidebar Filters
st.sidebar.header("Filters")

uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=['csv'])
df = load_data(uploaded_file) if uploaded_file else load_data()

min_date = df['DATE'].min()
max_date = df['DATE'].max()
start_date, end_date = st.sidebar.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

df = df[(df['DATE'] >= pd.to_datetime(start_date)) & (df['DATE'] <= pd.to_datetime(end_date))]

boroughs = df['BOROUGH'].dropna().unique()
selected_boroughs = st.sidebar.multiselect("Select Borough(s)", sorted(boroughs), default=sorted(boroughs))
df = df[df['BOROUGH'].isin(selected_boroughs)]

vehicle_types = df['VEHICLE 1 TYPE'].dropna().unique()
selected_vehicles = st.sidebar.multiselect("Vehicle Type(s)", sorted(vehicle_types), default=[])
if selected_vehicles:
    df = df[df['VEHICLE 1 TYPE'].isin(selected_vehicles)]

st.title("NYC Traffic Collision Dashboard")
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Overview", "Trends", "Map", "Export", "Compare Boroughs", "Search"])

# Tab 1: Overview
with tab1:
    st.subheader("Key Metrics")
    k1, k2, k3 = st.columns(3)
    k1.metric("Total Collisions", f"{len(df):,}")
    k2.metric("Total Injuries", int(df['PERSONS INJURED'].sum()))
    k3.metric("Total Fatalities", int(df['PERSONS KILLED'].sum()))

    with st.expander("Show Breakdown by Group"):
        group_cols = [
            'PEDESTRIANS INJURED', 'PEDESTRIANS KILLED',
            'CYCLISTS INJURED', 'CYCLISTS KILLED',
            'MOTORISTS INJURED', 'MOTORISTS KILLED'
        ]
        group_stats = df[group_cols].sum()
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x=group_stats.values, y=group_stats.index, palette='mako', ax=ax)
        ax.set_title("Injuries and Fatalities by Type")
        st.pyplot(fig)

# Tab 2: Trends
with tab2:
    st.subheader("Collisions Over Time")
    option = st.selectbox("Time Unit", options=['Hour', 'Week', 'Month', 'Year'])
    time_column = option.upper()
    
    if time_column in df:
        trend_data = df[time_column].value_counts().sort_index()
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.lineplot(x=trend_data.index, y=trend_data.values, marker='o', ax=ax)
        ax.set_title(f"Collisions per {option}")
        ax.set_xlabel(option)
        ax.set_ylabel("Number of Collisions")
        st.pyplot(fig)

    with st.expander("Contributing Factors"):
        if 'VEHICLE 1 FACTOR' in df.columns:
            top_factors = df['VEHICLE 1 FACTOR'].value_counts().head(10)
            fig3, ax3 = plt.subplots(figsize=(10, 5))
            sns.barplot(x=top_factors.values, y=top_factors.index, palette="flare", ax=ax3)
            ax3.set_title("Top 10 Contributing Factors")
            st.pyplot(fig3)

# Tab 3: Map
with tab3:
    st.subheader("Collision Locations")
    if 'LATITUDE' in df.columns and 'LONGITUDE' in df.columns:
        latlon_df = df[['LATITUDE', 'LONGITUDE']].dropna()
        if not latlon_df.empty:
            map_df = latlon_df.sample(n=min(5000, len(latlon_df)), random_state=1)
            m = folium.Map(location=[40.73, -73.93], zoom_start=10)
            marker_cluster = MarkerCluster().add_to(m)
            for _, row in map_df.iterrows():
                folium.Marker(location=[row['LATITUDE'], row['LONGITUDE']]).add_to(marker_cluster)
            st_data = st_folium(m, width=900, height=500)
        else:
            st.warning("No data available to display on the map. Please adjust filters.")
    else:
        st.warning("Latitude/Longitude columns are missing in the dataset.")

# Tab 4: Export
with tab4:
    st.subheader("Download Filtered Data")
    st.download_button(
        label="Download CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="filtered_collisions.csv",
        mime="text/csv"
    )
    st.markdown("You can download the currently filtered dataset for further analysis.")

# Tab 5: Compare Boroughs
with tab5:
    st.subheader("Compare Boroughs")
    borough_metrics = df.groupby('BOROUGH')[['PERSONS INJURED', 'PERSONS KILLED']].sum()
    fig_cb, ax_cb = plt.subplots(figsize=(10, 5))
    borough_metrics.plot(kind='barh', stacked=True, ax=ax_cb, colormap='tab20')
    ax_cb.set_title("Injuries and Fatalities by Borough")
    st.pyplot(fig_cb)

# Tab 6: Search
with tab6:
    st.subheader("Search Specific Record")
    search_term = st.text_input("Search by Unique Key, Zip Code or Contributing Factor")
    if search_term:
        mask = df.apply(lambda row: search_term.lower() in str(row).lower(), axis=1)
        results = df[mask]
        st.write(f"Found {len(results)} records")
        st.dataframe(results.head(100))

st.markdown("---")
st.caption("Built with ❤️ using Streamlit | Design: Ultra Pro Edition 🚀")


#address:https://nyc-collision-dashboard-xru5gcgjhrxkhhmuvghhjd.streamlit.app
#for run you have to write: streamlit run app_ui_pro.py