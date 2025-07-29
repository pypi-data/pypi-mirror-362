"""Main MCP D3 server implementation with STDIO support."""

import mcp.types as types
from mcp.server import Server
from pydantic import AnyUrl

from .services import get_chart_service, get_document_service


# Initialize services
document_service = get_document_service()
chart_service = get_chart_service()


# Create the server
server = Server("D3-Visualization-Server")


@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    """List available D3 resources."""
    return [
        types.Resource(
            uri=AnyUrl("d3-docs://d3-gallery"),
            name="d3-docs-gallery",
            mimeType="text/plain",
            description="D3.js gallery and examples"
        ),
        types.Resource(
            uri=AnyUrl("d3-docs://d3-indepth"),
            name="d3-docs-indepth", 
            mimeType="text/plain",
            description="In-depth D3.js guide and documentation"
        ),
        types.Resource(
            uri=AnyUrl("d3-docs://d3-org"),
            name="d3-docs-org",
            mimeType="text/plain", 
            description="Official D3.js documentation"
        )
    ]


@server.read_resource()
async def handle_read_resource(uri: AnyUrl) -> str:
    """Read a D3 resource."""
    uri_str = str(uri)

    # Handle d3-docs:// URIs
    if uri_str.startswith("d3-docs://"):
        doc_name = uri_str.replace("d3-docs://", "")
        try:
            document = await document_service.get_document(doc_name)
            return document.content
        except Exception as error:
            raise ValueError(f"Error loading document: {error}")

    # Handle d3-search:// URIs
    if uri_str.startswith("d3-search://"):
        query = uri_str.replace("d3-search://", "")
        try:
            results = await document_service.search_documents(query)
            if results:
                formatted_results = []
                for result in results:
                    formatted_results.append(f"== From {result['source']} ==\n{result['context']}")
                return "\n\n".join(formatted_results)
            else:
                return f'No results found for "{query}"'
        except Exception as error:
            return f'Error searching for "{query}": {error}'
    
    # Handle d3-topic:// URIs
    if uri_str.startswith("d3-topic://"):
        topic_path = uri_str.replace("d3-topic://", "")
        parts = topic_path.split("/")
        topic = parts[0]
        section = parts[1] if len(parts) > 1 else ""
        
        try:
            results = []
            documents = await document_service.list_documents()
            
            for doc_name in documents:
                if section:
                    # Get specific section
                    section_content = await document_service.get_document_section(doc_name, topic)
                    if section_content:
                        results.append(f"== {doc_name}: {topic} ==\n\n{section_content}")
                else:
                    # Get all matching sections
                    document = await document_service.get_document(doc_name)
                    for section_title, content in document.sections.items():
                        if topic.lower() in section_title.lower():
                            results.append(f"== {doc_name}: {section_title} ==\n\n{content}")
            
            if results:
                return "\n\n---\n\n".join(results)
            else:
                return f'No information found for topic "{topic}"'
        except Exception as error:
            raise ValueError(f"Error processing topic: {error}")
    
    raise ValueError(f"Resource not found: {uri}")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available D3 tools."""
    return [
        types.Tool(
            name="generate-d3-chart",
            description="Generate D3.js chart code based on chart type and data format",
            inputSchema={
                "type": "object",
                "properties": {
                    "chartType": {
                        "type": "string",
                        "description": "The type of chart to generate (bar, line, pie, etc)"
                    },
                    "dataFormat": {
                        "type": "string", 
                        "description": "Description of the data format"
                    },
                    "features": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional features to include"
                    }
                },
                "required": ["chartType", "dataFormat"]
            }
        ),
        types.Tool(
            name="recommend-chart",
            description="Get recommendations for the best chart type based on your data and purpose",
            inputSchema={
                "type": "object",
                "properties": {
                    "dataDescription": {
                        "type": "string",
                        "description": "Description of the data you want to visualize"
                    },
                    "purpose": {
                        "type": "string",
                        "description": "What insights you want to gain from the visualization"
                    }
                },
                "required": ["dataDescription", "purpose"]
            }
        ),
        types.Tool(
            name="ai-generate-d3",
            description="Use AI to generate a D3.js chart based on your description and data example",
            inputSchema={
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "Describe the chart you want to create"
                    },
                    "dataExample": {
                        "type": "string",
                        "description": "Example of your data structure"
                    }
                },
                "required": ["description", "dataExample"]
            }
        ),
        types.Tool(
            name="analyze-data",
            description="Analyze data and suggest appropriate visualizations",
            inputSchema={
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "JSON or CSV data to analyze"
                    },
                    "goal": {
                        "type": "string",
                        "description": "What you want to learn from this data"
                    }
                },
                "required": ["data", "goal"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Handle tool calls."""
    
    if name == "generate-d3-chart":
        chart_type = arguments.get("chartType", "")
        data_format = arguments.get("dataFormat", "")
        features = arguments.get("features", [])
        
        try:
            code = await chart_service.generate_chart_code(chart_type, data_format, features)
            return [types.TextContent(type="text", text=code)]
        except Exception as error:
            return [types.TextContent(type="text", text=f"Error generating chart: {error}")]
    
    elif name == "recommend-chart":
        data_description = arguments.get("dataDescription", "")
        purpose = arguments.get("purpose", "")
        
        try:
            recommendation = await chart_service.recommend_chart(data_description, purpose)
            return [types.TextContent(type="text", text=recommendation)]
        except Exception as error:
            return [types.TextContent(type="text", text=f"Error recommending chart: {error}")]
    
    elif name == "ai-generate-d3":
        description = arguments.get("description", "")
        data_example = arguments.get("dataExample", "")
        
        response = await chart_service.generate_ai_chart(description, data_example)
        return [types.TextContent(type="text", text=response.text)]
    
    elif name == "analyze-data":
        data = arguments.get("data", "")
        goal = arguments.get("goal", "")
        
        response = await chart_service.analyze_data(data, goal)
        return [types.TextContent(type="text", text=response.text)]
    
    else:
        raise ValueError(f"Unknown tool: {name}")


def main_sync():
    """Synchronous entry point for console script."""
    import asyncio
    from mcp.server.stdio import stdio_server
    
    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())
    
    asyncio.run(main())


if __name__ == "__main__":
    main_sync()