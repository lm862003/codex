from flask import Flask, request, jsonify
import os
import requests

# Serve static files from the repository-level "static" directory so
# users can access index.html via the Flask server.
app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'),
    static_url_path='/static'
)

CENSUS_API_URL = "https://api.census.gov/data"  # base URL

@app.route('/census')
def census():
    """Query the Census API by latitude/longitude and year."""
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    year = request.args.get('year', '2010')
    if not lat or not lon:
        return jsonify({'error': 'lat and lon are required'}), 400

    # Example: call the Census geocoder to get the census tract
    geocoder_url = f"https://geocoding.geo.census.gov/geocoder/geographies/coordinates?x={lon}&y={lat}&benchmark=Public_AR_Census2020&vintage={year}&format=json"
    geo_resp = requests.get(geocoder_url)
    if geo_resp.status_code != 200:
        return jsonify({'error': 'Failed to geocode'}), 500

    geojson = geo_resp.json()
    try:
        tract = geojson['result']['geographies']['Census Tracts'][0]['GEOID']
    except (KeyError, IndexError):
        return jsonify({'error': 'Census tract not found'}), 404

    # Example: fetch population from the decennial census
    census_url = f"{CENSUS_API_URL}/{year}/dec/pl?get=P1_001N&for=tract:{tract[-6:]}&in=state:{tract[:2]}+county:{tract[2:5]}"
    census_resp = requests.get(census_url)
    if census_resp.status_code != 200:
        return jsonify({'error': 'Failed to fetch census data'}), 500

    data = census_resp.json()
    return jsonify({'tract': tract, 'population': data[1][0], 'year': year})


# Serve the main map interface via Flask so users can simply visit
# the root URL in a browser instead of opening the HTML file manually.
@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, port=port)
