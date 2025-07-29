from .mcp_python_temp import mcp

def main() -> None:
    """uvx mcp-python … 으로 실행되는 진입점."""
    mcp.run(transport="stdio")

if __name__ == "__main__":   # pip install 후 직접 호출도 가능
    main()