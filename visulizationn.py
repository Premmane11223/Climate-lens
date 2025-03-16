
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as sl
import requests
import numpy as np

# Set page configuration (should be at the very beginning)
sl.set_page_config(page_title="Climate Lens 🌍", page_icon="☀️", layout="wide")

# Function to fetch climate data from API
def fetch_climate_data(location="London", days=7):
    try:
        api_key = "ad1158016a1ba9cc9672ec6d7ceb24ed"  
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={location}&cnt={days}&appid={api_key}&units=metric"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            climate_data = []
            for item in data['list']:
                climate_data.append({
                    'date': item['dt_txt'],
                    'temperature': item['main']['temp'],
                    'humidity': item['main']['humidity'],
                    'weather_condition': item['weather'][0]['main'],
                    'wind_speed': item['wind']['speed']
                })
            return pd.DataFrame(climate_data)
        else:
            sl.error(f"API Error: {response.status_code}")
            return None
    except Exception as e:
        sl.error(f"Error fetching climate data: {e}")
        return None

# Custom Styling
sl.markdown(
    """
    <style>
        .big-title { font-size:45px !important; font-weight: bold; text-align: center; color: #FFD700; }
        .sub-title { font-size:22px !important; text-align: center; color: white; }
        .card { background-color: #2C3E50; padding: 20px; border-radius: 15px; box-shadow: 5px 5px 15px rgba(0,0,0,0.3); color: white; text-align: center; }
        .sidebar-title { font-size:22px; font-weight:bold; color: #FFAA33; }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar Navigation
sl.sidebar.markdown('<p class="sidebar-title">🔎 Navigation</p>', unsafe_allow_html=True)
page = sl.sidebar.radio("Go to", ["Home", "Climate Analysis", "Future Predictions"])

if page == "Home":
    sl.markdown('<h1 class="big-title">🌍 Climate Lens</h1>', unsafe_allow_html=True)
    # sl.image("https://source.unsplash.com/1200x500/?climate,weather", use_column_width=True)

    sl.markdown('<p class="sub-title">Track real-time climate trends, analyze weather patterns, and predict future temperatures!</p>', unsafe_allow_html=True)

    col1, col2, col3 = sl.columns(3)
    with col1:
        sl.markdown('<div class="card"><h3>📊 Climate Analysis</h3><p>Explore weather trends and climate data.</p></div>', unsafe_allow_html=True)
    with col2:
        sl.markdown('<div class="card"><h3>🔮 Future Predictions</h3><p>Get weather forecasts using AI trends.</p></div>', unsafe_allow_html=True)
    with col3:
        sl.markdown('<div class="card"><h3>🏙️ City Information</h3><p>Learn about various cities & their climates.</p></div>', unsafe_allow_html=True)

    sl.subheader("🔍 Quick Weather Search")
    city = sl.text_input("Enter city name for quick weather check", "London")
    if sl.button("Check Weather"):
        with sl.spinner("Fetching current weather..."):
            climate_df = fetch_climate_data(city, days=1)
            if climate_df is not None:
                sl.success(f"✅ Weather in {city}: {climate_df.iloc[0]['temperature']}°C, {climate_df.iloc[0]['weather_condition']}")

elif page == "Climate Analysis":
    sl.markdown('<h2 class="big-title">🌎 Climate Analysis</h2>', unsafe_allow_html=True)
    
    location = sl.sidebar.text_input("Enter location", "London")
    days = sl.sidebar.slider("Forecast days", 1, 7, 3)
    temp_threshold = sl.sidebar.number_input("Set Temperature Threshold (°C)", min_value=-50.0, max_value=50.0, value=5.0)

    if sl.sidebar.button("Fetch Climate Data"):
        with sl.spinner("Fetching climate data..."):
            climate_df = fetch_climate_data(location, days)
            if climate_df is not None:
                sl.success(f"✅ Successfully fetched data for {location}")
                sl.subheader("📋 Climate API Data")
                sl.dataframe(climate_df)

                sl.subheader("📊 Statistical Data")
                sl.write(climate_df.describe())
                
                sl.subheader("🌡️ Days Exceeding Temperature Threshold")
                high_temp_days = climate_df[climate_df['temperature'] > temp_threshold]
                if not high_temp_days.empty:
                    sl.write(high_temp_days)
                    sl.warning(f"⚠️ Alert! {len(high_temp_days)} days exceed the temperature threshold of {temp_threshold}°C.")
                else:
                    sl.write("No days exceeding the threshold.")

                sl.subheader("💧 Humidity Levels Over Time")
                sl.line_chart(climate_df.set_index('date')['humidity'])

                sl.subheader("🌬️ Wind Speed Variation")
                sl.line_chart(climate_df.set_index('date')['wind_speed'])

                sl.subheader("📈 Temperature Variation")
                fig, ax = plt.subplots(figsize=(12, 6))
                ax.bar(climate_df['date'], climate_df['temperature'], color='#FF5733')
                ax.set_xticklabels(climate_df['date'], rotation=45, ha='right')
                ax.set_ylabel("Temperature (°C)")
                sl.pyplot(fig)

                sl.subheader("📉 Temperature Trends")
                sl.line_chart(climate_df.set_index('date')['temperature'])

elif page == "Future Predictions":
    sl.markdown('<h2 class="big-title">🔮 Future Predictions</h2>', unsafe_allow_html=True)
    
    location = sl.sidebar.text_input("Enter location for predictions", "London")
    temp_threshold = sl.sidebar.number_input("Set Temperature Threshold for Future (°C)", min_value=-50.0, max_value=50.0, value=5.0)

    days = sl.sidebar.slider("Number of prediction days", 1, 7, 3)

    if sl.sidebar.button("Predict Future"):
        with sl.spinner("Predicting future climate trends..."):
            climate_df = fetch_climate_data(location, days)
            if climate_df is not None and not climate_df.empty:
                sl.subheader("📉 Future Temperature Predictions")
                sl.dataframe(climate_df[['date', 'temperature']])
                sl.line_chart(climate_df.set_index('date')['temperature'])
                
                sl.subheader("🌡️ Future Days Exceeding Temperature Threshold")
                high_temp_days_future = climate_df[climate_df['temperature'] > temp_threshold]
                if not high_temp_days_future.empty:
                    sl.write(high_temp_days_future)
                    sl.warning(f"⚠️ Alert! {len(high_temp_days_future)} future days exceed the temperature threshold of {temp_threshold}°C.")
                else:
                    sl.write("No future days exceeding the threshold.")

                # Extreme Weather Alerts
                if "Rain" in climate_df['weather_condition'].values:
                    sl.warning("🌧️ Alert! Heavy rain expected in the coming days.")
                if "Storm" in climate_df['weather_condition'].values:
                    sl.error("⛈️ Severe storm alert! Take necessary precautions.")
                if "Hurricane" in climate_df['weather_condition'].values:
                    sl.error("🌀 Hurricane warning! Stay safe.")
                
                # Historical Weather Trends
                sl.subheader("📊 Historical Weather Trends")
                sl.line_chart(climate_df.set_index('date')['temperature'])

            else:
                sl.error("❌ Failed to fetch climate data. Please check the city name and try again.")
