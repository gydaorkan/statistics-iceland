"""
Flask application for displaying Statistics Iceland data.
"""
from flask import Flask, render_template, jsonify
import requests
import json
from datetime import datetime

app = Flask(__name__)

# API base URL for Statistics Iceland
API_BASE_URL = "https://px.hagstofa.is/pxis/api/v1/is"


def get_mock_data():
    """
    Return mock data when API is not accessible.
    This provides example data structure for development/testing.
    """
    return {
        "title": "Mannfjöldi eftir sveitarfélögum, kyni og ársfjórðungi 2010-2024",
        "description": "Mannfjöldi eftir sveitarfélögum, kyni og ársfjórðungi frá árinu 2010",
        "updated": datetime.now().strftime("%Y-%m-%d"),
        "columns": [
            {"code": "Sveitarfélag", "text": "Sveitarfélag"},
            {"code": "Kyn", "text": "Kyn"},
            {"code": "Ár", "text": "Ár"},
            {"code": "Mannfjöldi", "text": "Mannfjöldi"}
        ],
        "data": [
            {
                "key": ["Reykjavík", "Alls", "2024"],
                "values": ["139,875"]
            },
            {
                "key": ["Kópavogur", "Alls", "2024"],
                "values": ["39,890"]
            },
            {
                "key": ["Hafnarfjörður", "Alls", "2024"],
                "values": ["31,595"]
            },
            {
                "key": ["Akureyri", "Alls", "2024"],
                "values": ["19,850"]
            },
            {
                "key": ["Reykjanesbær", "Alls", "2024"],
                "values": ["19,676"]
            },
            {
                "key": ["Garðabær", "Alls", "2024"],
                "values": ["17,295"]
            },
            {
                "key": ["Mosfellsbær", "Alls", "2024"],
                "values": ["12,450"]
            },
            {
                "key": ["Árborg", "Alls", "2024"],
                "values": ["9,856"]
            },
            {
                "key": ["Akranes", "Alls", "2024"],
                "values": ["7,532"]
            },
            {
                "key": ["Fjarðabyggð", "Alls", "2024"],
                "values": ["4,891"]
            }
        ],
        "note": "Þetta eru sýnigögn sem notuð eru þegar ekki næst í raunverulega API þjónustu Hagstofunnar."
    }


def fetch_population_data():
    """
    Fetch population statistics from Statistics Iceland.
    Falls back to mock data if API is not accessible.
    """
    try:
        # Get metadata about the population table
        # Using a simple population table: Mannfjöldi eftir sveitarfélögum
        table_url = f"{API_BASE_URL}/Ibuar/mannfjoldi/1_yfirlit/Yfirlit_mannfjolda/MAN00000.px"
        
        # First, get the table metadata
        response = requests.get(table_url, timeout=5)
        response.raise_for_status()
        
        # Prepare a query to get the latest population data
        # Request data for all municipalities for the latest year
        query = {
            "query": [],
            "response": {
                "format": "json"
            }
        }
        
        # Post the query to get data
        data_response = requests.post(table_url, json=query, timeout=5)
        data_response.raise_for_status()
        
        return data_response.json()
    except (requests.RequestException, requests.Timeout) as e:
        print(f"Error fetching data from API (using mock data): {e}")
        return get_mock_data()


def parse_population_data(raw_data):
    """
    Parse the raw API response into a readable format.
    """
    if not raw_data:
        return []
    
    try:
        # Extract columns and data
        columns = raw_data.get('columns', [])
        data = raw_data.get('data', [])
        
        # Create a list of dictionaries for easier display
        parsed_data = []
        for item in data:
            row = {}
            keys = item.get('key', [])
            values = item.get('values', [])
            
            # Map each key to its column
            for i, col in enumerate(columns):
                if i < len(keys):
                    row[col['text']] = keys[i]
            
            # Add the actual value (typically the last column)
            if values and columns:
                row[columns[-1]['text']] = values[0]
            
            parsed_data.append(row)
        
        return parsed_data[:10]  # Return top 10 for display
    except Exception as e:
        print(f"Error parsing data: {e}")
        return []


@app.route('/')
def index():
    """Main page displaying statistics."""
    raw_data = fetch_population_data()
    statistics = parse_population_data(raw_data)
    
    return render_template('index.html', statistics=statistics, raw_data=raw_data)


@app.route('/api/data')
def api_data():
    """API endpoint to get raw data."""
    raw_data = fetch_population_data()
    return jsonify(raw_data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
