import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

st.set_page_config(page_title="NYC Collision Dashboard", layout="wide")

# ------------------------
# Load Data
# ------------------------
@st.cache_data
def load_data(path='data/collisions.csv'):
    df = pd.read_csv(path, low_memory=False)
    df.columns = df.columns.str.strip()
    df['DATETIME'] = pd.to_datetime(df['DATE'] + ' ' + df['TIME'], errors='coerce')
    df['HOUR'] = df['DATETIME'].dt.hour
    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
    return df

# ------------------------
# Sidebar Controls
# ------------------------
st.sidebar.header("📊 Filters")

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

# ------------------------
# Main Dashboard Tabs
# ------------------------
st.title("🚦 NYC Traffic Collision Dashboard")

tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Trends", "🗺️ Map", "⬇️ Export"])

# ------------------------
# Tab 1: Overview
# ------------------------
with tab1:
    st.subheader("🔢 Key Metrics")
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

# ------------------------
# Tab 2: Trends
# ------------------------
with tab2:
    st.subheader("🕒 Collisions by Hour")
    hour_count = df['HOUR'].value_counts().sort_index()

    fig2, ax2 = plt.subplots(figsize=(10, 4))
    sns.lineplot(x=hour_count.index, y=hour_count.values, marker='o', ax=ax2)
    ax2.set_title("Collisions Per Hour")
    ax2.set_xlabel("Hour")
    ax2.set_ylabel("Number of Collisions")
    st.pyplot(fig2)

    with st.expander("Contributing Factors"):
        if 'VEHICLE 1 FACTOR' in df.columns:
            top_factors = df['VEHICLE 1 FACTOR'].value_counts().head(10)
            fig3, ax3 = plt.subplots(figsize=(10, 5))
            sns.barplot(x=top_factors.values, y=top_factors.index, palette="flare", ax=ax3)
            ax3.set_title("Top 10 Contributing Factors")
            st.pyplot(fig3)

# ------------------------
# Tab 3: Interactive Map
# ------------------------
with tab3:
    st.subheader("🗺️ Collision Locations")

    if 'LATITUDE' in df.columns and 'LONGITUDE' in df.columns:
        map_df = df[['LATITUDE', 'LONGITUDE']].dropna().sample(n=min(5000, len(df)), random_state=1)
        m = folium.Map(location=[40.73, -73.93], zoom_start=10)
        marker_cluster = MarkerCluster().add_to(m)

        for _, row in map_df.iterrows():
            folium.Marker(location=[row['LATITUDE'], row['LONGITUDE']]).add_to(marker_cluster)

        st_data = st_folium(m, width=900, height=500)
    else:
        st.warning("No geographic coordinates found in dataset.")

# ------------------------
# Tab 4: Export
# ------------------------
with tab4:
    st.subheader("⬇️ Download Filtered Data")
    st.download_button(
        label="Download CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="filtered_collisions.csv",
        mime="text/csv"
    )
    st.markdown("You can download the currently filtered dataset for further analysis.")

# ------------------------
# Footer
# ------------------------
st.markdown("---")
st.caption("Built with ❤️ using Streamlit | Design: Pro UI Edition 🚀")
#for run this code you have to write : streamlit run app_ui_pro.py
