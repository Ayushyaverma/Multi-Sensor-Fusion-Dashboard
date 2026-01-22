# Multi-Sensor-Fusion-Dashboard
A fusion dashboard designed for monitoring operational conditions in real-time.

## Due to the confidential nature of the project only some sreenshots and some logic is shown, For detailes contact the owner.

It is a fusion dashboard designed for monitoring operational conditions in real-time. Developed as a project undertaken by **Para 23 SF** under the guidance of **MILIT (Military Institute of Technology)**, this system integrates inputs from various sources—including Radars, UAVs, moving targets, and diverse sensors—to provide a comprehensive situational awareness picture.

## Project Overview

The dashboard serves as a central command interface capable of displaying:
*   **Real-time Position Tracking:** Live coordinates of personnel and assets (Pathfinders, UAVs, Paramotors) via LoRa communication.
*   **Live Weather & Forecasting:** Integration with weather APIs to display current conditions and forecasts (24-hour and 3-day).
*   **Operational Analytics:** Distance calculations from strategic reference points using the Haversine formula.
*   **Personnel Details:** Quick access to rank, appointment, and equipment details of deployed units.

This project was submitted to the **Indian Army**. For their exceptional work on this project, the students received a **Commendation from the Commandant, MILIT**, along with Letters of Recommendation (LORs).

## Team & Credits

*   **Software Development:** Ayushya Verma
    *   Responsible for the entire software architecture, dashboard creation, and data integration.
*   **Hardware Variant:** Saurabh Kushwah
    *   Developed the hardware components required for sensor data and communication.
*   **Key Contributors:**
    *   Aditya Vardhan Singh
    *   Pranjeet Sarkar
    *   Aadarsh Sinha

## Technical Stack

*   **Language:** Python
*   **Framework:** [Dash](https://dash.plotly.com/) (by Plotly) for the web interface.
*   **Visualization:** [Plotly Express](https://plotly.com/python/plotly-express/) for interactive maps and weather graphs.
*   **Communication:** `pyserial` for reading live GPS data from LoRa receivers via USB (COM ports).
*   **Data Handling:** `pandas` for data manipulation and state management.
*   **APIs:** OpenWeatherMap API for meteorological data.

## Features

1.  **Live Map Visualization:**
    *   Uses Mapbox open-street-maps to plot dynamic markers.
    *   Updates in real-time (1-second intervals) based on incoming serial data.
    *   Visual distinction for specific units (Alpha, Bravo, Delta, Tango).

2.  **LoRa Integration:**
    *   Reads serial data streams to parse Transmitter IDs, Latitude, and Longitude.
    *   Threaded serial reading to ensure the dashboard remains responsive while processing hardware inputs.

3.  **Situational Tools:**
    *   **Distance Calculator:** Automatically computes the distance of deployed units from the base.
    *   **Weather Module:** Displays live temperature, humidity, and wind speed, alongside a graphical forecast.

## Installation & Usage

1.  **Prerequisites:**
    Ensure Python is installed. Install the required dependencies:
    ```bash
    pip install dash plotly pandas pyserial requests
    ```

2.  **Hardware Setup:**
    *   Connect the LoRa receiver to the USB port.
    *   Update the `SERIAL_PORT` variable in `cptdash.py` (e.g., `COM5` or `/dev/ttyUSB0`).

3.  **Running the Dashboard:**
    ```bash
    python cptdash.py
    ```
    The application will run locally at `http://127.0.0.1:8050/`.

---
*Developed for the Indian Army / MILIT.*
