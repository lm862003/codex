# TimeScope Prototype

This repository contains a minimal prototype for **TimeScope**, a map-based web application that lets users explore historical U.S. Census data through an interactive map. It combines OpenStreetMap tiles with the U.S. Census Bureau API.

## Features

- Click anywhere on the map to query the Census Bureau geocoder and retrieve the census tract.
- Fetch population data from the decennial census (default year 2010).
- Display the population in a pop-up on the map.

## Requirements

- Python 3.8+
- Flask
- requests

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Running the App

1. Start the Flask server:

```bash
python src/app.py
```

2. Open `static/index.html` in a browser.

Click on the map to fetch population data for the selected location.

This is only a starting point. You can extend it with additional endpoints for other years, overlay more datasets, and build a richer frontend.
