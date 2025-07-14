import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title='NYC Collisions Dashboard', layout='wide')

# Load data
@st.cache_data
def load_data(path='data/collisions.csv'):
    df = pd.read_csv(path, low_memory=False)
    df.columns = df.columns.str.strip()
    df['DATETIME'] = pd.to_datetime(df['DATE'] + ' ' + df['TIME'], errors='coerce')
    df['HOUR'] = df['DATETIME'].dt.hour
    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
    return df

# File uploader
st.title('🚦 NYC Traffic Collision Dashboard')
uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])

if uploaded_file is not None:
    df = load_data(uploaded_file)
    st.success("File uploaded successfully.")
else:
    df = load_data()
    st.info("Using default dataset.")

# Date range filter
min_date = df['DATE'].min()
max_date = df['DATE'].max()
start_date, end_date = st.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

df = df[(df['DATE'] >= pd.to_datetime(start_date)) & (df['DATE'] <= pd.to_datetime(end_date))]

# Borough filter
boroughs = df['BOROUGH'].dropna().unique()
selected_borough = st.selectbox('Select Borough', options=sorted(boroughs))

filtered_df = df[df['BOROUGH'] == selected_borough]

# KPIs
col1, col2 = st.columns(2)
with col1:
    st.metric("📊 Total Injuries", int(filtered_df['PERSONS INJURED'].sum()))
with col2:
    st.metric("☠️ Total Fatalities", int(filtered_df['PERSONS KILLED'].sum()))

# Grouped injuries and fatalities
st.subheader('🚑 Injuries and Fatalities by Group')
group_cols = [
    'PEDESTRIANS INJURED', 'PEDESTRIANS KILLED',
    'CYCLISTS INJURED', 'CYCLISTS KILLED',
    'MOTORISTS INJURED', 'MOTORISTS KILLED'
]
group_stats = filtered_df[group_cols].sum()

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=group_stats.values, y=group_stats.index, palette='Reds_r', ax=ax)
ax.set_title('Injuries and Fatalities by Group')
st.pyplot(fig)

# Hourly collision pattern
st.subheader('🕒 Collisions by Hour of Day')
hour_count = filtered_df['HOUR'].value_counts().sort_index()

fig2, ax2 = plt.subplots(figsize=(10, 4))
sns.lineplot(x=hour_count.index, y=hour_count.values, marker='o', ax=ax2)
ax2.set_title('Collisions per Hour')
ax2.set_xlabel('Hour')
ax2.set_ylabel('Number of Collisions')
st.pyplot(fig2)

# Map of collisions
st.subheader('🗺️ Collision Map')
if 'LATITUDE' in filtered_df.columns and 'LONGITUDE' in filtered_df.columns:
    st.map(filtered_df[['LATITUDE', 'LONGITUDE']].dropna())
else:
    st.warning("Latitude and Longitude columns are missing.")

# Download filtered data
st.subheader("⬇️ Download Filtered Data")
st.download_button(
    label="Download CSV",
    data=filtered_df.to_csv(index=False).encode('utf-8'),
    file_name='filtered_collisions.csv',
    mime='text/csv'
)

st.caption("Built with Streamlit")

#for run this code you have to write : streamlit run app.py
