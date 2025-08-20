import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px

st.set_page_config(page_title="🇨🇭 Swiss Job Explorer", layout="wide")

# --- Load data
@st.cache_data
def load_data():
    df = pd.read_csv("JOB_APP/cleaned_jobs.csv")  # Adjust path as needed
    df = df.dropna(subset=["latitude", "longitude"])  # Remove rows without coordinates
    return df

df = load_data()

st.title("💼 Job Map of Switzerland")
st.markdown("Explore job postings across Switzerland by profession, location, and type.")

# --- Sidebar filters
professions = sorted(df['profession'].dropna().unique())
selected_profession = st.sidebar.selectbox("🔍 Filter by profession:", ["All"] + professions)

if selected_profession != "All":
    df = df[df['profession'] == selected_profession]

# --- Map visualization
st.subheader("📍 Job Locations Map")

view_state = pdk.ViewState(
    latitude=df["latitude"].mean(),
    longitude=df["longitude"].mean(),
    zoom=6.5,
    pitch=0,
)

layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position='[longitude, latitude]',
    get_radius=8000,
    get_color='[200, 30, 0, 160]',
    pickable=True,
)


deck = pdk.Deck(
    map_style=None,  # ✅ No API key needed, still shows a visible map
    initial_view_state=view_state,
    layers=[layer],
    tooltip={"text": "{profession}\n{title}\n{location}"},
)

st.pydeck_chart(deck)

# --- Job count by city
st.subheader("🏙️ Job Distribution by City")
city_counts = df['location'].value_counts().nlargest(20).reset_index()
city_counts.columns = ['location', 'job_count']

fig = px.bar(city_counts, x="location", y="job_count", title="Top 20 Cities by Job Count")
st.plotly_chart(fig, use_container_width=True)

# --- Show full table
with st.expander("🗃️ Show job listings"):
    st.dataframe(df[['profession', 'title', 'link', 'date', 'location', 'workload',
       'emp_type', 'company']])