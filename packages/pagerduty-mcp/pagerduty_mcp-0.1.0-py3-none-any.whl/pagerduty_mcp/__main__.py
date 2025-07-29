from pagerduty_mcp.server import app

if __name__ == "__main__":
    print("Starting PagerDuty MCP Server. Use the --enable-write-tools flag to enable write tools.")
    app()
