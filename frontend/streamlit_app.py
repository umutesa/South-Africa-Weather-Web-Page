import streamlit as st
import sqlite3
import pandas as pd
import pydeck as pdk
import random

st.set_page_config(page_title="South Africa Weather Map", layout="wide")
st.title("South Africa Weather Coordination (Map View)")

# City coordinates for mapping
CITY_COORDS = {
    'Cape Town': [-33.9249, 18.4241],
    'Johannesburg': [-26.2041, 28.0473],
    'Durban': [-29.8587, 31.0218],
    'Pretoria': [-25.7479, 28.2293],
    'Port Elizabeth': [-33.9608, 25.6022],
    'Bloemfontein': [-29.0852, 26.1596],
    'Polokwane': [-23.9045, 29.4689],
    'Nelspruit': [-25.4658, 30.9853],
    'Kimberley': [-28.7383, 24.7637],
    'Mthatha': [-31.5889, 28.7844],
}

DB_PATH = 'weather.db'

# Get latest weather for each city
def get_latest_weather():
    # Simulate more realistic weather data for South Africa
    simulated_data = []
    for city in CITY_COORDS.keys():
        # More realistic temperature ranges for South Africa
        temp = round(random.uniform(15, 32), 1)  # Normal range
        conditions = ['Clear', 'Clouds', 'Clear', 'Clouds', 'Rain', 'Drizzle']  # More common conditions
        condition = random.choice(conditions)
        wind = round(random.uniform(5, 15), 1)  # Normal wind speeds
        
        # Occasionally add extreme conditions
        if random.random() < 0.2:  # 20% chance of extreme weather
            if random.random() < 0.5:
                temp = round(random.uniform(35, 42), 1)  # Hot
            else:
                wind = round(random.uniform(20, 25), 1)  # Windy
            if random.random() < 0.2:
                condition = random.choice(['Thunderstorm', 'Rain'])
        
        simulated_data.append({
            'city': city,
            'temp': temp,
            'condition': condition,
            'wind': wind,
            'timestamp': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    return pd.DataFrame(simulated_data)

weather_df = get_latest_weather()



# Add coordinates to dataframe (pydeck expects [lon, lat])
weather_df['lon'] = weather_df['city'].map(lambda c: CITY_COORDS[c][1])
weather_df['lat'] = weather_df['city'].map(lambda c: CITY_COORDS[c][0])


# Define color and icon for major alerts
# Major alert: temp > 40, temp < 0, wind > 20, or condition in ['Thunderstorm', 'Tornado']
def get_alert(row):
    if row['temp'] > 40 or row['temp'] < 0:
        return 'Extreme Temp'
    if row['wind'] > 20:
        return 'Extreme Wind'
    if row['condition'] in ['Thunderstorm', 'Tornado']:
        return 'Extreme Weather'
    return ''

weather_df['alert'] = weather_df.apply(get_alert, axis=1)
weather_df['color'] = weather_df['alert'].apply(lambda a: [220,4,41] if a else [0,119,182])

# Add weather emoji for condition
def weather_emoji(condition):
    mapping = {
        'Clear': '☀️',
        'Clouds': '☁️',
        'Rain': '🌧️',
        'Thunderstorm': '⛈️',
        'Drizzle': '🌦️',
        'Snow': '❄️',
        'Mist': '🌫️',
        'Tornado': '🌪️',
    }
    return mapping.get(condition, '')
weather_df['emoji'] = weather_df['condition'].apply(weather_emoji)

# Map display
st.subheader("Weather Map of South Africa")

if not weather_df.empty:
    # Create weather label with temp and emoji
    weather_df['label'] = weather_df.apply(lambda x: f"{x['city']}\n{x['temp']}°C {x['emoji']}", axis=1)
    
    # Text layer for weather details
    text_layer = pdk.Layer(
        "TextLayer",
        data=weather_df,
        get_position='[lon, lat]',
        get_text='label',
        get_color=[0, 0, 0, 255],
        get_size=16,
        get_alignment_baseline="'bottom'",
        pickable=True
    )
    
    # Weather icon markers
    icon_layer = pdk.Layer(
        "ScatterplotLayer",
        data=weather_df,
        get_position='[lon, lat]',
        get_color='color',
        get_radius=20000,
        pickable=True,
        opacity=0.7,
        stroked=True,
        filled=True,
        get_line_color=[255, 255, 255],
        line_width_min_pixels=2
    )

    view_state = pdk.ViewState(
        latitude=-29,
        longitude=24,
        zoom=4.8,
        pitch=0
    )

    r = pdk.Deck(
        layers=[icon_layer, text_layer],
        initial_view_state=view_state,
        map_style='road',
        tooltip={
            "html": "<b>{city}</b><br>{temp}°C, {condition} {emoji}<br>Wind: {wind} m/s<br><span style='color:#d90429'>{alert}</span>",
            "style": {"backgroundColor": "#fff", "color": "#222", "fontSize": "14px"}
        }
    )
    
    # Show the map
    st.pydeck_chart(r)
    
    # Show detailed weather information in a table below
    st.subheader("Detailed Weather Information")
    
    # Format the DataFrame for display
    display_df = weather_df[['city', 'temp', 'condition', 'wind', 'timestamp']].copy()
    display_df.columns = ['City', 'Temperature (°C)', 'Condition', 'Wind Speed (m/s)', 'Last Updated']
    
    # Sort by temperature to show hottest cities first
    display_df = display_df.sort_values('Temperature (°C)', ascending=False)

    # Add emoji to condition
    display_df['Condition'] = weather_df.apply(lambda x: f"{x['condition']} {x['emoji']}", axis=1)
    
    # Add alert information if any
    display_df['Status'] = weather_df['alert'].apply(lambda x: f"⚠️ {x}" if x else "✓ Normal")

    def style_dataframe(df):
        # Style the dataframe with custom colors
        return df.style.apply(lambda x: [
            'background-color: #ffebee; color: #d32f2f' if '⚠️' in str(x['Status'])  # Red background for alerts
            else 'background-color: #e8f5e9; color: #2e7d32'  # Green background for normal
            for _ in x
        ], axis=1).format({
            'Temperature (°C)': '{:.1f}°C',
            'Wind Speed (m/s)': '{:.1f} m/s'
        }).set_properties(**{
            'background-color': 'white',
            'font-family': 'Arial, sans-serif',
            'font-size': '14px',
            'padding': '10px'
        })

    # Display the styled dataframe
    st.dataframe(style_dataframe(display_df), use_container_width=True)
else:
    st.warning("No weather data available to display on the map.")
