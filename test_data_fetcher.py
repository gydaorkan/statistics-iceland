"""
Tests for the Statistics Iceland data fetcher module.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from data_fetcher import StatisticsIcelandAPI


class TestStatisticsIcelandAPI(unittest.TestCase):
    """Test cases for the StatisticsIcelandAPI class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.api = StatisticsIcelandAPI(language="is")
    
    def test_init(self):
        """Test API initialization."""
        self.assertEqual(self.api.language, "is")
        self.assertIsNotNone(self.api.session)
    
    def test_init_with_english(self):
        """Test API initialization with English language."""
        api = StatisticsIcelandAPI(language="en")
        self.assertEqual(api.language, "en")
    
    @patch('data_fetcher.requests.Session.get')
    def test_get_tables_success(self, mock_get):
        """Test successful retrieval of tables."""
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = [
            {"id": "table1", "text": "Table 1", "type": "t"},
            {"id": "category1", "text": "Category 1", "type": "l"}
        ]
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        # Call method
        result = self.api.get_tables()
        
        # Assertions
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "table1")
        mock_get.assert_called_once_with(f"{self.api.BASE_URL}/is")
    
    @patch('data_fetcher.requests.Session.get')
    def test_get_tables_error(self, mock_get):
        """Test get_tables when an error occurs."""
        # Mock error
        import requests
        mock_get.side_effect = requests.RequestException("Network error")
        
        # Call method
        result = self.api.get_tables()
        
        # Assertions
        self.assertEqual(result, [])
    
    @patch('data_fetcher.requests.Session.get')
    def test_get_table_metadata_success(self, mock_get):
        """Test successful retrieval of table metadata."""
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "title": "Test Table",
            "updated": "2024-01-01",
            "variables": []
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        # Call method
        table_id = "test/table.px"
        result = self.api.get_table_metadata(table_id)
        
        # Assertions
        self.assertIsNotNone(result)
        self.assertEqual(result["title"], "Test Table")
        mock_get.assert_called_once_with(f"{self.api.BASE_URL}/is/{table_id}")
    
    @patch('data_fetcher.requests.Session.get')
    def test_get_table_metadata_error(self, mock_get):
        """Test get_table_metadata when an error occurs."""
        # Mock error
        import requests
        mock_get.side_effect = requests.RequestException("Network error")
        
        # Call method
        result = self.api.get_table_metadata("test/table.px")
        
        # Assertions
        self.assertIsNone(result)
    
    @patch('data_fetcher.requests.Session.post')
    def test_get_table_data_with_query(self, mock_post):
        """Test get_table_data with a custom query."""
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {"data": [1, 2, 3]}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        # Call method
        table_id = "test/table.px"
        query = {"query": [], "response": {"format": "json"}}
        result = self.api.get_table_data(table_id, query)
        
        # Assertions
        self.assertIsNotNone(result)
        self.assertEqual(result["data"], [1, 2, 3])
        mock_post.assert_called_once()
    
    @patch('data_fetcher.requests.Session.post')
    @patch('data_fetcher.requests.Session.get')
    def test_get_table_data_without_query(self, mock_get, mock_post):
        """Test get_table_data without a query (gets metadata first)."""
        # Mock metadata response
        mock_get_response = Mock()
        mock_get_response.json.return_value = {
            "title": "Test Table",
            "variables": []
        }
        mock_get_response.raise_for_status = Mock()
        mock_get.return_value = mock_get_response
        
        # Mock data response
        mock_post_response = Mock()
        mock_post_response.json.return_value = {"data": [1, 2, 3]}
        mock_post_response.raise_for_status = Mock()
        mock_post.return_value = mock_post_response
        
        # Call method
        table_id = "test/table.px"
        result = self.api.get_table_data(table_id)
        
        # Assertions
        self.assertIsNotNone(result)
        self.assertEqual(result["data"], [1, 2, 3])
        mock_get.assert_called_once()
        mock_post.assert_called_once()
    
    @patch('data_fetcher.requests.Session.post')
    def test_get_table_data_error(self, mock_post):
        """Test get_table_data when an error occurs."""
        # Mock error
        import requests
        mock_post.side_effect = requests.RequestException("Network error")
        
        # Call method
        query = {"query": [], "response": {"format": "json"}}
        result = self.api.get_table_data("test/table.px", query)
        
        # Assertions
        self.assertIsNone(result)


class TestAPIIntegration(unittest.TestCase):
    """Integration tests (these will fail without network access)."""
    
    def test_base_url_format(self):
        """Test that BASE_URL is correctly formatted."""
        api = StatisticsIcelandAPI()
        self.assertTrue(api.BASE_URL.startswith("https://"))
        self.assertIn("hagstofa.is", api.BASE_URL)


if __name__ == '__main__':
    unittest.main()
