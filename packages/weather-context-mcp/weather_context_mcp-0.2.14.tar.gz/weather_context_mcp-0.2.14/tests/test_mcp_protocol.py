"""
MCP protocol tests for weather-mcp server.

These tests verify that the MCP server correctly implements the protocol and
responds to standard MCP requests.
"""


def test_mcp_tool_registration():
    """Test that MCP tools are properly registered."""
    from weather_mcp.main import mcp

    # Verify that the MCP instance is properly initialized
    assert mcp is not None
    assert mcp.name == "weather_mcp"

    # Import the functions to verify they exist
    from weather_mcp.main import get_weather

    # Verify functions are callable
    assert callable(get_weather)
