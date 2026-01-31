"""
Simple Flask web application to display data from Statistics Iceland.
"""

from flask import Flask, render_template, request, jsonify
from data_fetcher import StatisticsIcelandAPI
import os

app = Flask(__name__)
api = StatisticsIcelandAPI()


@app.route('/')
def index():
    """Main page displaying available data categories."""
    return render_template('index.html')


@app.route('/api/tables')
def get_tables():
    """API endpoint to get available tables."""
    tables = api.get_tables()
    return jsonify(tables)


@app.route('/api/table/<path:table_id>')
def get_table(table_id):
    """API endpoint to get specific table metadata."""
    metadata = api.get_table_metadata(table_id)
    if metadata:
        return jsonify(metadata)
    return jsonify({'error': 'Table not found'}), 404


@app.route('/api/table/<path:table_id>/data', methods=['POST'])
def get_table_data(table_id):
    """API endpoint to get table data with optional query."""
    query = request.get_json() if request.is_json else None
    data = api.get_table_data(table_id, query)
    if data:
        return jsonify(data)
    return jsonify({'error': 'Could not fetch data'}), 500


@app.route('/api/search')
def search_tables():
    """API endpoint to search for tables."""
    keyword = request.args.get('q', '')
    if not keyword:
        return jsonify({'error': 'Search keyword required'}), 400
    
    results = api.search_tables(keyword)
    return jsonify(results)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
