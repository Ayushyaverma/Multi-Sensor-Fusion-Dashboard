from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import threading
import serial
from datetime import datetime

# Import custom modules
from distance_calc import calculate_distance
from weatherforcast import get_live_weather, get_mock_forecast

# --- Configuration ---
SERIAL_PORT = "COM3"  # Replace with your actual COM port (e.g., /dev/ttyUSB0)
BAUD_RATE = 115200
API_KEY = "YOUR_OPENWEATHERMAP_API_KEY" # Replace with your API Key
BASE_COORDINATES = (18.5204, 73.8567)  # Generic Base Coordinates (e.g., City Center)

# --- State Management ---
# Stores the latest position of units
transmitter_data = {
    "Unit1": {"lat": 18.5204, "lon": 73.8567, "last_update": datetime.min},
    "Unit2": {"lat": 18.5214, "lon": 73.8577, "last_update": datetime.min},
    "Unit3": {"lat": 18.5224, "lon": 73.8587, "last_update": datetime.min},
}

def read_serial_data():
    """
    Background thread to read GPS data from Arduino/LoRa via Serial.
    Expected Serial Format: "ID:Unit1,Lat:18.5204,Lng:73.8567"
    """
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to Serial Port: {SERIAL_PORT}")
        while True:
            try:
                line = ser.readline().decode('utf-8').strip()
                if line and "Lat:" in line and "Lng:" in line:
                    # Parse the incoming string
                    parts = line.split(',')
                    unit_id = parts[0].split(':')[1].strip()
                    lat = float(parts[1].split(':')[1])
                    lon = float(parts[2].split(':')[1])
                    
                    # Update state if unit exists
                    if unit_id in transmitter_data:
                        transmitter_data[unit_id] = {
                            "lat": lat,
                            "lon": lon,
                            "last_update": datetime.now()
                        }
                        print(f"Updated {unit_id}: {lat}, {lon}")
            except Exception as e:
                # print(f"Parse Error: {e}") # Uncomment for debugging
                pass
    except Exception as e:
        print(f"Serial Connection Error: {e}")

# Start Serial Thread
t = threading.Thread(target=read_serial_data)
t.daemon = True
t.start()

# --- Dash App Layout ---
app = Dash(__name__)

app.layout = html.Div(style={'font-family': 'Arial', 'background-color': '#f4f4f4', 'padding': '20px', 'min-height': '100vh'}, children=[
    html.H1("Situational Awareness Dashboard", style={'text-align': 'center', 'color': '#2c3e50', 'margin-bottom': '30px'}),
    
    html.Div(style={'display': 'flex', 'gap': '20px', 'flex-wrap': 'wrap'}, children=[
        # Left Column: Map
        html.Div(style={'flex': '3', 'min-width': '600px', 'background': 'white', 'padding': '10px', 'border-radius': '8px', 'box-shadow': '0 2px 4px rgba(0,0,0,0.1)'}, children=[
            html.H3("Live Tracking Map", style={'color': '#34495e'}),
            dcc.Graph(id="live-map"),
            dcc.Interval(id="update-interval", interval=1000, n_intervals=0) # Updates every 1 second
        ]),
        
        # Right Column: Analytics
        html.Div(style={'flex': '1', 'min-width': '300px', 'display': 'flex', 'flex-direction': 'column', 'gap': '20px'}, children=[
            # Weather Card
            html.Div(style={'background': 'white', 'padding': '20px', 'border-radius': '8px', 'box-shadow': '0 2px 4px rgba(0,0,0,0.1)'}, children=[
                html.H4("Live Weather", style={'margin-top': '0'}),
                html.Div(id="weather-display")
            ]),
            # Distance Card
            html.Div(style={'background': 'white', 'padding': '20px', 'border-radius': '8px', 'box-shadow': '0 2px 4px rgba(0,0,0,0.1)'}, children=[
                html.H4("Unit Distances (from Base)", style={'margin-top': '0'}),
                html.Div(id="distance-display")
            ]),
            # Forecast Graph
            html.Div(style={'background': 'white', 'padding': '20px', 'border-radius': '8px', 'box-shadow': '0 2px 4px rgba(0,0,0,0.1)'}, children=[
                html.H4("Forecast Trend", style={'margin-top': '0'}),
                dcc.Graph(id="weather-graph", style={'height': '200px'})
            ])
        ])
    ])
])

@app.callback(
    [Output("live-map", "figure"), Output("weather-display", "children"), Output("distance-display", "children"), Output("weather-graph", "figure")],
    [Input("update-interval", "n_intervals")]
)
def update_dashboard(n):
    # 1. Prepare Map Data
    active_units = [{"Name": uid, "Latitude": d["lat"], "Longitude": d["lon"]} for uid, d in transmitter_data.items()]
    df = pd.DataFrame(active_units)
    
    fig_map = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", hover_name="Name", zoom=14, height=600)
    fig_map.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0}, mapbox=dict(center={"lat": BASE_COORDINATES[0], "lon": BASE_COORDINATES[1]}))

    # 2. Weather Info
    weather = get_live_weather(API_KEY, BASE_COORDINATES[0], BASE_COORDINATES[1])
    weather_html = [html.P(f"Temp: {weather['temp']}°C"), html.P(f"Wind: {weather['wind']} m/s"), html.P(f"Condition: {weather['desc']}")] if weather else html.P("Data Unavailable")

    # 3. Distances
    dist_html = [html.P(f"{row['Name']}: {calculate_distance(BASE_COORDINATES[0], BASE_COORDINATES[1], row['Latitude'], row['Longitude']):.2f} km") for _, row in df.iterrows()]

    # 4. Forecast
    return fig_map, weather_html, dist_html, px.line(get_mock_forecast(), x="Time", y=["Temperature", "Humidity"]).update_layout(margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

if __name__ == "__main__":
    app.run_server(debug=True)