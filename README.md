# TimeScope Prototype

This repository contains a minimal prototype for **TimeScope**, a map-based web application that lets users explore historical U.S. Census data through an interactive map. It combines OpenStreetMap tiles with the U.S. Census Bureau API.

## Features

- Click anywhere on the map to query the Census Bureau geocoder and retrieve the census tract.
- Fetch population data from the decennial census. The server currently knows
  how to query the 2010 and 2020 decennial datasets and chooses the correct API
  parameters automatically based on the requested year (the map uses 2010).
- Display the population in a pop-up on the map.
- Responses are cached locally to minimize Census API calls.

## Requirements

- Python 3.8+
- Flask
- requests

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Running the App

1. Start the Flask server. By default it listens on port 5001, but you can
   override the port by setting the `PORT` environment variable:

```bash
# run on the default port (5001)
python src/app.py

# or specify a custom port
PORT=8000 python src/app.py
```

2. Visit `http://localhost:5001/` (or your chosen port) in a browser to view
   the map interface.

Click on the map to fetch population data for the selected location. A few
sample points are loaded automatically so you can verify the API connection even
if random clicks fail to resolve to a census tract.

The application creates a `cache.db` SQLite database in the project
directory to store query results. You can delete this file at any time to
clear the cache.

This is only a starting point. You can extend it with additional endpoints for other years, overlay more datasets, and build a richer frontend.
