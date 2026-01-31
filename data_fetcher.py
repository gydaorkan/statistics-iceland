"""
Data fetcher module for Statistics Iceland (Hagstofan) API.

This module provides functionality to fetch data from the Statistics Iceland
PX-Web API at https://px.hagstofa.is/pxis/api/v1/
"""

import requests
from typing import Dict, List, Any, Optional


class StatisticsIcelandAPI:
    """Client for interacting with Statistics Iceland API."""
    
    BASE_URL = "https://px.hagstofa.is/pxis/api/v1"
    
    def __init__(self, language: str = "is"):
        """
        Initialize the API client.
        
        Args:
            language: Language code ('is' for Icelandic, 'en' for English)
        """
        self.language = language
        self.session = requests.Session()
    
    def get_tables(self) -> List[Dict[str, Any]]:
        """
        Get list of available tables from the API.
        
        Returns:
            List of available tables with metadata
        """
        url = f"{self.BASE_URL}/{self.language}"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching tables: {e}")
            return []
    
    def get_table_metadata(self, table_id: str) -> Optional[Dict[str, Any]]:
        """
        Get metadata for a specific table.
        
        Args:
            table_id: The table identifier (e.g., 'Atvinnuvegir/fyrirtaeki/afkoma/2_rekstrarogefnahags/FYR08010.px')
        
        Returns:
            Table metadata or None if error occurs
        """
        url = f"{self.BASE_URL}/{self.language}/{table_id}"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching table metadata: {e}")
            return None
    
    def get_table_data(self, table_id: str, query: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Get data from a specific table.
        
        Args:
            table_id: The table identifier
            query: Optional query parameters to filter data
        
        Returns:
            Table data or None if error occurs
        """
        url = f"{self.BASE_URL}/{self.language}/{table_id}"
        try:
            if query:
                response = self.session.post(url, json=query)
            else:
                # Get metadata first, then request all data
                metadata = self.get_table_metadata(table_id)
                if not metadata:
                    return None
                
                # Build a simple query to get all data
                query = {
                    "query": [],
                    "response": {"format": "json"}
                }
                response = self.session.post(url, json=query)
            
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching table data: {e}")
            return None
    
    def search_tables(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Search for tables containing a specific keyword.
        
        Args:
            keyword: Search keyword
        
        Returns:
            List of matching tables
        """
        all_tables = self.get_tables()
        keyword_lower = keyword.lower()
        
        def search_recursive(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
            """Recursively search through nested table structure."""
            results = []
            for item in items:
                if item.get('type') == 'l':  # Folder/category
                    # Search in this category's children
                    if 'id' in item:
                        try:
                            category_url = f"{self.BASE_URL}/{self.language}/{item['id']}"
                            response = self.session.get(category_url)
                            response.raise_for_status()
                            children = response.json()
                            results.extend(search_recursive(children))
                        except requests.RequestException:
                            pass
                elif item.get('type') == 't':  # Table
                    # Check if keyword is in text or id
                    text = item.get('text', '').lower()
                    item_id = item.get('id', '').lower()
                    if keyword_lower in text or keyword_lower in item_id:
                        results.append(item)
            return results
        
        return search_recursive(all_tables)
