# MCP D3 Server (Python)

A Python-based MCP (Model Context Protocol) server that provides D3.js visualization information, chart generation, and documentation resources. This is a Python port of the original Node.js MCP D3 server with STDIO support for use with `uv` and other Python package managers.

## Features

- **D3.js Documentation Resources**: Access to curated D3.js documentation and examples
- **Chart Generation Tools**: Generate D3.js chart code for various chart types (bar, line, etc.)
- **AI-Powered Chart Creation**: Use AI to generate custom D3 visualizations based on descriptions
- **Data Analysis**: Analyze data and get visualization recommendations
- **STDIO Transport**: Compatible with MCP clients using stdio transport

## Installation

### Using uv (recommended)

```bash
cd mcp-d3-server-python
uv sync
```

### Using pip

```bash
cd mcp-d3-server-python
pip install -e .
```

## Usage

### Running as STDIO MCP Server

```bash
# Using uv
uv run mcp-d3-server

# Using pip-installed package
mcp-d3-server
```

### Configuration for MCP Clients

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "d3-visualization": {
      "command": "uv",
      "args": ["run", "mcp-d3-server"],
      "cwd": "/path/to/mcp-d3-server-python"
    }
  }
}
```

## Available Resources

- `d3-docs://d3-gallery` - D3.js gallery and examples
- `d3-docs://d3-indepth` - In-depth D3.js guide and documentation  
- `d3-docs://d3-org` - Official D3.js documentation
- `d3-search://query` - Search across all D3 documentation
- `d3-topic://topic[/section]` - Get information about specific D3 topics

## Available Tools

### generate-d3-chart
Generate D3.js chart code based on chart type and data format.

**Parameters:**
- `chartType` (string): Type of chart (bar, line, pie, etc.)
- `dataFormat` (string): Description of your data format
- `features` (array, optional): Additional features to include

### recommend-chart  
Get chart type recommendations based on your data and visualization goals.

**Parameters:**
- `dataDescription` (string): Description of your data
- `purpose` (string): What insights you want to gain

### ai-generate-d3
Use AI to generate custom D3.js visualizations.

**Parameters:**
- `description` (string): Describe the chart you want
- `dataExample` (string): Example of your data structure

### analyze-data
Analyze data and get visualization suggestions.

**Parameters:**
- `data` (string): Your data in JSON or CSV format
- `goal` (string): What you want to learn from the data

## Development

### Setup Development Environment

```bash
cd mcp-d3-server-python
uv sync --extra dev
```

### Running Tests

```bash
uv run pytest
```

### Code Formatting

```bash
uv run black src/
uv run ruff check src/
```

### Type Checking

```bash  
uv run mypy src/
```

## Project Structure

```
mcp-d3-server-python/
├── src/
│   └── mcp_d3_server/
│       ├── __init__.py
│       ├── server.py          # Main MCP server with STDIO support
│       ├── services.py        # Service implementations
│       └── types.py           # Type definitions
├── assets/
│   └── llm-full/             # D3 documentation files
├── pyproject.toml            # Python package configuration
└── README.md
```

## License

MIT