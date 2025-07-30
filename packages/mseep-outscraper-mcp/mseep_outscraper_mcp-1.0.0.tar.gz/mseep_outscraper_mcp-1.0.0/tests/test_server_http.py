#!/usr/bin/env python3
"""
Tests for the HTTP server module
"""

import pytest
import json
from unittest.mock import Mock, patch, AsyncMock
from fastapi.testclient import TestClient
from outscraper_mcp.server_http import app, _parse_query_params, _execute_tool


class TestHTTPServer:
    """Test cases for HTTP server endpoints"""
    
    def setup_method(self):
        """Set up test client"""
        self.client = TestClient(app)
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "outscraper-mcp"
        assert "version" in data
        assert "api_key_configured" in data
    
    def test_mcp_get(self):
        """Test GET /mcp endpoint"""
        response = self.client.get("/mcp?apiKey=test_key")
        assert response.status_code == 200
        data = response.json()
        assert "server" in data
        assert "tools" in data
        assert len(data["tools"]) == 2
        assert data["tools"][0]["name"] == "google_maps_search"
        assert data["tools"][1]["name"] == "google_maps_reviews"
    
    @patch('outscraper_mcp.server.google_maps_search')
    def test_mcp_post_search(self, mock_search):
        """Test POST /mcp endpoint with search tool"""
        mock_search.return_value = "Search results"
        
        payload = {
            "tool": "google_maps_search",
            "arguments": {
                "query": "restaurants NYC",
                "limit": 10
            }
        }
        
        response = self.client.post("/mcp?apiKey=test_key", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == "Search results"
        mock_search.assert_called_once_with(query="restaurants NYC", limit=10)
    
    @patch('outscraper_mcp.server.google_maps_reviews')
    def test_mcp_post_reviews(self, mock_reviews):
        """Test POST /mcp endpoint with reviews tool"""
        mock_reviews.return_value = "Reviews results"
        
        payload = {
            "tool": "google_maps_reviews",
            "arguments": {
                "query": "ChIJtest",
                "reviews_limit": 20
            }
        }
        
        response = self.client.post("/mcp", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == "Reviews results"
    
    def test_mcp_post_missing_tool(self):
        """Test POST /mcp with missing tool name"""
        payload = {"arguments": {"query": "test"}}
        response = self.client.post("/mcp", json=payload)
        assert response.status_code == 400
        assert "Missing 'tool'" in response.json()["detail"]
    
    def test_mcp_post_invalid_tool(self):
        """Test POST /mcp with invalid tool name"""
        payload = {
            "tool": "invalid_tool",
            "arguments": {}
        }
        response = self.client.post("/mcp", json=payload)
        assert response.status_code == 500
        assert "Unknown tool" in response.json()["detail"]
    
    def test_mcp_post_invalid_json(self):
        """Test POST /mcp with invalid JSON"""
        response = self.client.post(
            "/mcp",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 400
    
    def test_mcp_delete(self):
        """Test DELETE /mcp endpoint"""
        response = self.client.delete("/mcp")
        assert response.status_code == 200
        assert "cleanup completed" in response.json()["message"]


class TestHelperFunctions:
    """Test cases for helper functions"""
    
    def test_parse_query_params_simple(self):
        """Test parsing simple query parameters"""
        params = {"apiKey": "test123", "debug": "true"}
        result = _parse_query_params(params)
        assert result == {"apiKey": "test123", "debug": "true"}
    
    def test_parse_query_params_nested(self):
        """Test parsing nested query parameters"""
        params = {
            "server.host": "localhost",
            "server.port": "8000",
            "apiKey": "test"
        }
        result = _parse_query_params(params)
        assert result == {
            "server": {
                "host": "localhost",
                "port": "8000"
            },
            "apiKey": "test"
        }
    
    def test_parse_query_params_deep_nested(self):
        """Test parsing deeply nested query parameters"""
        params = {
            "config.server.host": "localhost",
            "config.server.port": "8000",
            "config.debug": "true"
        }
        result = _parse_query_params(params)
        assert result == {
            "config": {
                "server": {
                    "host": "localhost",
                    "port": "8000"
                },
                "debug": "true"
            }
        }
    
    @pytest.mark.asyncio
    @patch('outscraper_mcp.server.google_maps_search')
    async def test_execute_tool_search(self, mock_search):
        """Test executing search tool"""
        mock_search.return_value = "Search results"
        result = await _execute_tool("google_maps_search", {"query": "test"})
        assert result == "Search results"
    
    @pytest.mark.asyncio
    @patch('outscraper_mcp.server.google_maps_reviews')
    async def test_execute_tool_reviews(self, mock_reviews):
        """Test executing reviews tool"""
        mock_reviews.return_value = "Reviews results"
        result = await _execute_tool("google_maps_reviews", {"query": "test"})
        assert result == "Reviews results"
    
    @pytest.mark.asyncio
    async def test_execute_tool_unknown(self):
        """Test executing unknown tool"""
        with pytest.raises(ValueError) as exc_info:
            await _execute_tool("unknown_tool", {})
        assert "Unknown tool" in str(exc_info.value)
    
    @pytest.mark.asyncio
    @patch('outscraper_mcp.server.google_maps_search')
    async def test_execute_tool_invalid_args(self, mock_search):
        """Test executing tool with invalid arguments"""
        mock_search.side_effect = TypeError("missing required argument: 'query'")
        with pytest.raises(ValueError) as exc_info:
            await _execute_tool("google_maps_search", {})
        assert "Invalid arguments" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])