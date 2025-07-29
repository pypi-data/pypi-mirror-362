from fastmcp import FastMCP


def test_server_creation():
    server = FastMCP("test-server")
    assert server is not None


def test_main_import():
    from hectofinancial_mcp_server.server import main

    assert callable(main)
