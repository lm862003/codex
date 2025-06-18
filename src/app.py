from flask import Flask, request, jsonify
import os
import requests
import sqlite3

# Serve static files from the repository-level "static" directory so
# users can access index.html via the Flask server.
app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'),
    static_url_path='/static'
)

CENSUS_API_URL = "https://api.census.gov/data"  # base URL

# Decennial dataset parameters for supported years
DECENNIAL = {
    '2020': {
        'dataset': '2020/dec/pl',
        'var': 'P1_001N',
        'benchmark': 'Public_AR_Census2020',
        'vintage': 'Census2020_Census2020'
    },
    '2010': {
        'dataset': '2010/dec/sf1',
        'var': 'P001001',
        'benchmark': 'Public_AR_Census2010',
        'vintage': 'Census2010_Census2010'
    },
}

# SQLite database for caching API responses
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'cache.db')

# Ensure the cache table exists
with sqlite3.connect(DB_PATH) as conn:
    conn.execute(
        """CREATE TABLE IF NOT EXISTS census_cache (
                lat REAL,
                lon REAL,
                year TEXT,
                tract TEXT,
                population TEXT,
                PRIMARY KEY (lat, lon, year)
            )"""
    )
    conn.commit()

@app.route('/census')
def census():
    """Query the Census API by latitude/longitude and year."""
    lat_param = request.args.get('lat')
    lon_param = request.args.get('lon')
    year = request.args.get('year', '2010')
    if not lat_param or not lon_param:
        return jsonify({'error': 'lat and lon are required'}), 400

    # Round coordinates for cache lookup
    lat = round(float(lat_param), 4)
    lon = round(float(lon_param), 4)

    # Check cache first
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            'SELECT tract, population FROM census_cache WHERE lat=? AND lon=? AND year=?',
            (lat, lon, year)
        )
        row = cur.fetchone()
        if row:
            return jsonify({'tract': row[0], 'population': row[1], 'year': year, 'cached': True})

    # Example: call the Census geocoder to get the census tract
    info = DECENNIAL.get(year, DECENNIAL['2010'])

    geocoder_url = (
        f"https://geocoding.geo.census.gov/geocoder/geographies/coordinates?x={lon}&y={lat}"
        f"&benchmark={info['benchmark']}&vintage={info['vintage']}&format=json"
    )
    geo_resp = requests.get(geocoder_url)
    if geo_resp.status_code != 200:
        return jsonify({'error': 'Failed to geocode'}), 500

    geojson = geo_resp.json()
    try:
        tract = geojson['result']['geographies']['Census Tracts'][0]['GEOID']
    except (KeyError, IndexError):
        return jsonify({'error': 'Census tract not found'}), 404

    # Example: fetch population from the decennial census
    census_url = (
        f"{CENSUS_API_URL}/{info['dataset']}?get={info['var']}"
        f"&for=tract:{tract[-6:]}&in=state:{tract[:2]}+county:{tract[2:5]}"
    )
    census_resp = requests.get(census_url)
    if census_resp.status_code != 200:
        return jsonify({'error': f"Failed to fetch census data ({census_resp.status_code})"}), 500

    data = census_resp.json()
    population = data[1][0]

    # Store in cache
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            'INSERT OR REPLACE INTO census_cache (lat, lon, year, tract, population) VALUES (?,?,?,?,?)',
            (lat, lon, year, tract, population)
        )
        conn.commit()

    return jsonify({'tract': tract, 'population': population, 'year': year, 'cached': False})


# Serve the main map interface via Flask so users can simply visit
# the root URL in a browser instead of opening the HTML file manually.
@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, port=port)
