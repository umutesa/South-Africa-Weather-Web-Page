# Real Time South Africa Weather Coordination Web Dashboard 

An interactive weather dashboard that displays real-time weather data and extreme weather alerts for major cities in South Africa.

<img width="1181" height="498" alt="Screenshot (2)" src="https://github.com/user-attachments/assets/c676d8c2-2f7d-4e4f-b0bb-e478411c86d7" />


##  Features

- Interactive map showing weather conditions across South Africa
- Real-time temperature and weather updates
- Extreme weather alerts (temperature, wind, storms)


### Prerequisites

- Python 3.7+



**Install Dependencies**
   ```bash
   pip install -r backend/requirements.txt
   pip install streamlit pandas pydeck
   ```

### Running the Application

#### Option 1: Using Real Weather Data (OpenWeatherMap API)

1. Get your API key from [OpenWeatherMap](https://openweathermap.org/api)
2. Set your API key:
   ```bash
   export OPENWEATHERMAP_API_KEY=your_api_key_here
   ```
3. Start the backend:
   ```bash
   python3 backend/app.py
   ```

#### Option 2: Using Simulated Weather Data

1. Start the backend (no API key needed):
   ```bash
   python3 backend/app.py
   ```

### View the Dashboard

Start the Streamlit frontend:
```bash
streamlit run frontend/streamlit_app.py
```

The dashboard will open in your default web browser.

## Covered Cities

- Cape Town
- Johannesburg
- Durban
- Pretoria
- Port Elizabeth
- Bloemfontein
- Polokwane
- Nelspruit
- Kimberley
- Mthatha


