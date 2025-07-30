#!/usr/bin/env python3
"""
Basic tests for the outscraper_mcp server.
"""

import pytest
import os
from unittest.mock import Mock, patch
from outscraper_mcp.server import OutscraperClient, google_maps_search, google_maps_reviews


class TestOutscraperClient:
    """Test cases for OutscraperClient"""
    
    def test_init(self):
        """Test client initialization"""
        client = OutscraperClient("test_api_key")
        assert client.api_key == "test_api_key"
        assert client.headers['X-API-KEY'] == "test_api_key"
        assert client.headers['client'] == "MCP Server"
    
    @patch('outscraper_mcp.server.requests.Session')
    def test_google_maps_search_success(self, mock_session_class):
        """Test successful Google Maps search"""
        # Mock session and response
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [[{"name": "Test Business", "rating": 4.5}]]
        mock_session.get.return_value = mock_response
        
        client = OutscraperClient("test_api_key")
        result = client.google_maps_search("test query")
        
        assert result is not None
        mock_session.get.assert_called_once()
    
    @patch('outscraper_mcp.server.requests.Session')
    def test_google_maps_reviews_success(self, mock_session_class):
        """Test successful Google Maps reviews"""
        # Mock session and response
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"name": "Test Business", "reviews_data": []}]
        mock_session.get.return_value = mock_response
        
        client = OutscraperClient("test_api_key")
        result = client.google_maps_reviews("test query")
        
        assert result is not None
        mock_session.get.assert_called_once()
    
    @patch('outscraper_mcp.server.requests.Session')
    def test_api_error_handling(self, mock_session_class):
        """Test API error handling"""
        # Mock session and error response
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_session.get.return_value = mock_response
        
        client = OutscraperClient("test_api_key")
        
        with pytest.raises(Exception) as exc_info:
            client.google_maps_search("test query")
        
        assert "API request failed" in str(exc_info.value)


class TestToolFunctions:
    """Test cases for MCP tool functions"""
    
    @patch('outscraper_mcp.server.client.google_maps_search')
    def test_google_maps_search_tool(self, mock_search):
        """Test google_maps_search tool function"""
        # Mock successful response
        mock_search.return_value = [[{
            "name": "Test Restaurant",
            "full_address": "123 Test St",
            "rating": 4.5,
            "reviews": 100,
            "phone": "+1234567890",
            "site": "https://test.com",
            "type": "Restaurant",
            "place_id": "test_place_id"
        }]]
        
        result = google_maps_search("restaurants near me")
        
        assert "Test Restaurant" in result
        assert "4.5" in result
        mock_search.assert_called_once()
    
    @patch('outscraper_mcp.server.client.google_maps_reviews')
    def test_google_maps_reviews_tool(self, mock_reviews):
        """Test google_maps_reviews tool function"""
        # Mock successful response
        mock_reviews.return_value = [{
            "name": "Test Business",
            "address": "123 Test St",
            "rating": 4.5,
            "reviews": 50,
            "reviews_data": [{
                "autor_name": "John Doe",
                "review_rating": 5,
                "review_datetime_utc": "2024-01-01",
                "review_text": "Great place!"
            }]
        }]
        
        result = google_maps_reviews("test business")
        
        assert "Test Business" in result
        assert "John Doe" in result
        assert "Great place!" in result
        mock_reviews.assert_called_once()
    
    @patch('outscraper_mcp.server.client.google_maps_search')
    def test_search_error_handling(self, mock_search):
        """Test error handling in search tool"""
        mock_search.side_effect = Exception("API Error")
        
        result = google_maps_search("test query")
        
        assert "Error searching Google Maps" in result
        assert "API Error" in result


@pytest.fixture
def mock_env_api_key():
    """Mock environment variable for API key"""
    with patch.dict(os.environ, {'OUTSCRAPER_API_KEY': 'test_key'}):
        yield


def test_environment_setup(mock_env_api_key):
    """Test that environment variables are properly handled"""
    from outscraper_mcp.server import API_KEY
    # Note: This will test the module-level import, which may use the original env
    # In a real scenario, you'd want to reload the module or use dependency injection
    assert API_KEY is not None


if __name__ == "__main__":
    pytest.main([__file__])