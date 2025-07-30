#!/usr/bin/env python3
"""
Integration tests for the outscraper_mcp server with mocked API responses.
"""

import pytest
import json
from unittest.mock import Mock, patch
import requests
from outscraper_mcp.server import OutscraperClient, google_maps_search, google_maps_reviews


class TestIntegration:
    """Integration tests with realistic API responses"""
    
    @patch('outscraper_mcp.server.client')
    def test_search_integration_success(self, mock_client):
        """Test successful search with realistic response"""
        
        # Mock realistic API response
        mock_client.google_maps_search.return_value = [[{
            "name": "Joe's Pizza",
            "full_address": "123 Main St, New York, NY 10001",
            "rating": 4.5,
            "reviews": 1234,
            "phone": "+1 212-555-0123",
            "site": "https://joespizza.com",
            "type": "Pizza restaurant",
            "place_id": "ChIJtest123",
            "working_hours_old_format": "Mon-Sun: 11AM-11PM",
            "working_hours": {
                "Monday": "11:00 AM - 11:00 PM",
                "Tuesday": "11:00 AM - 11:00 PM"
            }
        }, {
            "name": "Tony's Italian",
            "full_address": "456 Broadway, New York, NY 10002",
            "rating": 4.3,
            "reviews": 890,
            "phone": "+1 212-555-0456",
            "site": "https://tonysitalian.com",
            "type": "Italian restaurant",
            "place_id": "ChIJtest456"
        }]]
        
        # Execute search
        result = google_maps_search("pizza restaurants NYC", limit=2)
        
        # Verify result formatting
        assert "Found 2 places" in result
        assert "Joe's Pizza" in result
        assert "4.5 (1234 reviews)" in result
        assert "Tony's Italian" in result
        assert "ChIJtest123" in result
    
    @patch('outscraper_mcp.server.client')
    def test_reviews_integration_success(self, mock_client):
        """Test successful reviews with realistic response"""
        
        # Mock realistic API response
        mock_client.google_maps_reviews.return_value = [{
            "name": "Joe's Pizza",
            "address": "123 Main St, New York, NY 10001",
            "rating": 4.5,
            "reviews": 1234,
            "phone": "+1 212-555-0123",
            "site": "https://joespizza.com",
            "reviews_data": [
                {
                    "autor_name": "John Doe",
                    "review_rating": 5,
                    "review_datetime_utc": "2024-01-15 10:30:00",
                    "review_text": "Best pizza in NYC! The crust is perfect and the sauce is amazing. Highly recommend the pepperoni slice.",
                    "review_likes": 42
                },
                {
                    "autor_name": "Jane Smith",
                    "review_rating": 4,
                    "review_datetime_utc": "2024-01-10 15:45:00",
                    "review_text": "Great pizza but can get crowded during lunch hours. The staff is friendly and service is quick.",
                    "review_likes": 15
                }
            ]
        }]
        
        # Execute reviews extraction
        result = google_maps_reviews("ChIJtest123", reviews_limit=2)
        
        # Verify result formatting
        assert "Joe's Pizza" in result
        assert "4.5 (1234 total reviews)" in result
        assert "John Doe" in result
        assert "5⭐" in result
        assert "Best pizza in NYC!" in result
        assert "Jane Smith" in result
    
    @patch('outscraper_mcp.server.client')
    def test_search_with_enrichment(self, mock_client):
        """Test search with email enrichment"""
        
        # Mock response with enrichment data
        mock_client.google_maps_search.return_value = [[{
            "name": "Tech Startup Inc",
            "full_address": "789 Tech Blvd, San Francisco, CA 94105",
            "rating": 4.8,
            "reviews": 45,
            "phone": "+1 415-555-0789",
            "site": "https://techstartup.com",
            "type": "Software company",
            "place_id": "ChIJtest789",
            "emails": [
                {"value": "info@techstartup.com", "type": "primary"},
                {"value": "support@techstartup.com", "type": "support"}
            ]
        }]]
        
        # Execute search with enrichment
        result = google_maps_search(
            "tech companies san francisco",
            limit=1,
            enrichment=["emails_validator_service"]
        )
        
        # Verify enrichment data is included
        assert "Tech Startup Inc" in result
        assert "info@techstartup.com" in result
        assert "support@techstartup.com" in result
    
    @patch('outscraper_mcp.server.client')
    def test_async_response_handling(self, mock_client):
        """Test handling of async responses"""
        
        # Mock async response
        mock_client.google_maps_search.return_value = "⏳ **Request processing asynchronously**\n\n📋 **Available tools:**\n• google_maps_search\n• google_maps_reviews\n\n🔗 **Request ID:** req_123\n📍 **Results URL:** https://api.outscraper.com/results/req_123\n\n💡 **Note:** This server only provides Google Maps Search and Reviews tools."
        
        # Execute large search that triggers async
        result = google_maps_search("restaurants", limit=100)
        
        # Verify async response is returned properly
        assert "Request processing asynchronously" in result
        assert "Request ID:" in result
        assert "Results URL:" in result
    
    @patch('outscraper_mcp.server.client')
    def test_empty_results_handling(self, mock_client):
        """Test handling of empty results"""
        
        # Mock empty response
        mock_client.google_maps_search.return_value = []
        
        # Execute search
        result = google_maps_search("nonexistent place xyz123")
        
        # Verify empty results message
        assert "No results found" in result
    
    @patch('outscraper_mcp.server.client')
    def test_api_error_handling(self, mock_client):
        """Test API error handling"""
        
        # Mock API error
        mock_client.google_maps_search.side_effect = Exception("Invalid API key. Please check your OUTSCRAPER_API_KEY.")
        
        # Execute search
        result = google_maps_search("test query")
        
        # Verify error is handled gracefully
        assert "Error searching Google Maps" in result
        assert "Invalid API key" in result
    
    @patch('outscraper_mcp.server.client')
    def test_malformed_response_handling(self, mock_client):
        """Test handling of malformed API responses"""
        
        # Mock malformed response (dict instead of list)
        mock_client.google_maps_search.return_value = {
            "error": "Unexpected response format"
        }
        
        # Execute search
        result = google_maps_search("test query")
        
        # Should handle gracefully
        assert "Search results for 'test query'" in result
    
    def test_input_validation_errors(self):
        """Test input validation"""
        # Test empty query
        result = google_maps_search("")
        assert "Error: Search query cannot be empty" in result
        
        # Test invalid limit
        result = google_maps_search("test", limit=500)
        assert "Error: Limit must be between 1 and 400" in result
        
        # Test invalid sort for reviews
        result = google_maps_reviews("test", sort="invalid_sort")
        assert "Error: Sort must be one of" in result
        
        # Test negative reviews limit
        result = google_maps_reviews("test", reviews_limit=-10)
        assert "Error: Reviews limit must be between 0 and" in result


class TestErrorScenarios:
    """Test various error scenarios"""
    
    @patch('outscraper_mcp.server.requests.Session')
    def test_network_timeout(self, mock_session_class):
        """Test network timeout handling"""
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        
        # Mock timeout
        mock_session.get.side_effect = requests.exceptions.Timeout()
        
        client = OutscraperClient("test_key")
        
        with pytest.raises(Exception) as exc_info:
            client.google_maps_search("test query")
        
        assert "Request timed out" in str(exc_info.value)
    
    @patch('outscraper_mcp.server.requests.Session')
    def test_connection_error(self, mock_session_class):
        """Test connection error handling"""
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        
        # Mock connection error
        mock_session.get.side_effect = requests.exceptions.ConnectionError()
        
        client = OutscraperClient("test_key")
        
        with pytest.raises(Exception) as exc_info:
            client.google_maps_reviews("test query")
        
        assert "Connection error" in str(exc_info.value)
    
    @patch('outscraper_mcp.server.requests.Session')
    def test_rate_limit_error(self, mock_session_class):
        """Test rate limit error handling"""
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        
        # Mock rate limit response
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.json.return_value = {"message": "Rate limit exceeded"}
        mock_session.get.return_value = mock_response
        
        client = OutscraperClient("test_key")
        
        with pytest.raises(Exception) as exc_info:
            client.google_maps_search("test query")
        
        assert "Rate limit exceeded" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])