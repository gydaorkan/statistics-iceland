"""
Tests for the Flask web application.
"""

import unittest
import json
from unittest.mock import patch, Mock
from app import app


class TestFlaskApp(unittest.TestCase):
    """Test cases for the Flask application."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_index_route(self):
        """Test that the index route returns successfully."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hagstofa', response.data)
    
    @patch('app.api.get_tables')
    def test_api_tables_endpoint(self, mock_get_tables):
        """Test the /api/tables endpoint."""
        # Mock data
        mock_get_tables.return_value = [
            {"id": "table1", "text": "Table 1", "type": "t"}
        ]
        
        # Make request
        response = self.client.get('/api/tables')
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], "table1")
    
    @patch('app.api.get_table_metadata')
    def test_api_table_metadata_success(self, mock_get_metadata):
        """Test the /api/table/<id> endpoint with successful response."""
        # Mock data
        mock_get_metadata.return_value = {
            "title": "Test Table",
            "updated": "2024-01-01"
        }
        
        # Make request
        response = self.client.get('/api/table/test/table.px')
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["title"], "Test Table")
    
    @patch('app.api.get_table_metadata')
    def test_api_table_metadata_not_found(self, mock_get_metadata):
        """Test the /api/table/<id> endpoint when table is not found."""
        # Mock data
        mock_get_metadata.return_value = None
        
        # Make request
        response = self.client.get('/api/table/nonexistent.px')
        
        # Assertions
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    @patch('app.api.get_table_data')
    def test_api_table_data_success(self, mock_get_data):
        """Test the /api/table/<id>/data endpoint with successful response."""
        # Mock data
        mock_get_data.return_value = {
            "data": [1, 2, 3]
        }
        
        # Make request
        response = self.client.post(
            '/api/table/test/table.px/data',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["data"], [1, 2, 3])
    
    @patch('app.api.get_table_data')
    def test_api_table_data_error(self, mock_get_data):
        """Test the /api/table/<id>/data endpoint when an error occurs."""
        # Mock data
        mock_get_data.return_value = None
        
        # Make request
        response = self.client.post(
            '/api/table/test/table.px/data',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        # Assertions
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    @patch('app.api.search_tables')
    def test_api_search_success(self, mock_search):
        """Test the /api/search endpoint with successful response."""
        # Mock data
        mock_search.return_value = [
            {"id": "table1", "text": "Population Table"}
        ]
        
        # Make request
        response = self.client.get('/api/search?q=population')
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        mock_search.assert_called_once_with('population')
    
    def test_api_search_no_keyword(self):
        """Test the /api/search endpoint without keyword."""
        # Make request
        response = self.client.get('/api/search')
        
        # Assertions
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)


if __name__ == '__main__':
    unittest.main()
