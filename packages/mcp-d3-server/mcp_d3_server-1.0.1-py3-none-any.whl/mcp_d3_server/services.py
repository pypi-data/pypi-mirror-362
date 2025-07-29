"""Service implementations for the MCP D3 server."""

import asyncio
import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional

from .models import (
    AIMessage,
    AICompletionResponse,
    AIService,
    ChartGenerationService,
    D3Document,
    D3DocumentService,
)


class MockAIService(AIService):
    """Implementation of AIService that uses a mock response."""
    
    async def generate_completion(
        self, 
        messages: List[AIMessage], 
        options: Optional[Dict] = None
    ) -> AICompletionResponse:
        """Generate a completion from the mock AI service."""
        print(f"Would call AI service with: {json.dumps([msg.dict() for msg in messages], indent=2)}")
        
        # Build a simple mock response based on the last user message
        user_messages = [m for m in messages if m.role == 'user']
        response_text = "This is a placeholder response from the AI service."
        
        if user_messages:
            last_message = user_messages[-1]
            if 'chart' in last_message.content.lower():
                response_text += "\n\nHere's how you can create a simple chart with D3:"
                response_text += "\n\n```javascript\n// Create an SVG element\nconst svg = d3.select('#chart')\n  .append('svg')\n  .attr('width', 600)\n  .attr('height', 400);\n```"
            elif 'data' in last_message.content.lower():
                response_text += "\n\nWhen working with data in D3, you'll typically want to use data joins:"
                response_text += "\n\n```javascript\nsvg.selectAll('rect')\n  .data(dataset)\n  .enter()\n  .append('rect');\n```"
        
        return AICompletionResponse(text=response_text, is_error=False)


class FileSystemD3DocumentService(D3DocumentService):
    """Implementation of D3DocumentService that uses filesystem."""
    
    def __init__(self, base_path: str):
        """Create a new FileSystemD3DocumentService."""
        self.base_path = Path(base_path)
        self.document_cache: Dict[str, D3Document] = {}
    
    def _extract_sections(self, content: str) -> Dict[str, str]:
        """Extract sections from D3 text content."""
        sections = {}
        
        # Split by markdown level 2 headers
        section_regex = re.compile(r'^## (.+?)$([\s\S]*?)(?=^## |$)', re.MULTILINE)
        
        for match in section_regex.finditer(content):
            title = match.group(1).strip()
            section_content = match.group(2).strip()
            sections[title] = section_content
        
        return sections
    
    async def get_document(self, name: str) -> D3Document:
        """Get a D3 document by name."""
        # Check cache first
        if name in self.document_cache:
            return self.document_cache[name]
        
        # Load from file system
        file_path = self.base_path / f"{name}.txt"
        try:
            content = file_path.read_text(encoding='utf-8')
            sections = self._extract_sections(content)
            
            document = D3Document(name=name, content=content, sections=sections)
            
            # Cache for next time
            self.document_cache[name] = document
            
            return document
        except Exception as error:
            raise Exception(f"Error loading document '{name}': {error}")
    
    async def list_documents(self) -> List[str]:
        """List available D3 documents."""
        # In a real implementation, this would scan the directory
        # For simplicity, we'll return the known document names
        return ['d3-gallery', 'd3-indepth', 'd3-org']
    
    async def search_documents(self, query: str) -> List[Dict[str, str]]:
        """Search for a query across all documents."""
        results = []
        documents = await self.list_documents()
        
        for doc_name in documents:
            try:
                document = await self.get_document(doc_name)
                
                # Simple search - find matches and context
                lines = document.content.split('\n')
                matches = [
                    (line, i) for i, line in enumerate(lines)
                    if query.lower() in line.lower()
                ]
                
                # If found matches, add context around them
                if matches:
                    context_results = []
                    for line, index in matches[:5]:  # Limit to 5 matches per document
                        start = max(0, index - 3)
                        end = min(len(lines), index + 4)
                        context = '\n'.join(lines[start:end])
                        context_results.append({
                            'source': doc_name,
                            'context': context
                        })
                    results.extend(context_results)
            except Exception as error:
                print(f"Error searching {doc_name}: {error}")
        
        return results
    
    async def get_document_section(self, name: str, section_name: str) -> Optional[str]:
        """Get a specific section from a document."""
        try:
            document = await self.get_document(name)
            
            # Look for exact match first
            if section_name in document.sections:
                return document.sections[section_name]
            
            # Then try case-insensitive partial match
            lower_section_name = section_name.lower()
            for key, content in document.sections.items():
                if lower_section_name in key.lower():
                    return content
            
            return None
        except Exception as error:
            print(f"Error getting section {section_name} from {name}: {error}")
            return None


class D3ChartGenerationService(ChartGenerationService):
    """Implementation of ChartGenerationService."""
    
    def __init__(self, ai_service: AIService, document_service: D3DocumentService):
        """Create a new D3ChartGenerationService."""
        self.ai_service = ai_service
        self.document_service = document_service
    
    async def generate_chart_code(
        self, 
        chart_type: str, 
        data_format: str, 
        features: Optional[List[str]] = None
    ) -> str:
        """Generate D3 chart code."""
        if features is None:
            features = []
        
        # Simple chart templates - would be more sophisticated in production
        if chart_type.lower() == 'bar':
            return self._generate_bar_chart_template(data_format, features)
        elif chart_type.lower() == 'line':
            return self._generate_line_chart_template(data_format, features)
        else:
            return f"""// D3.js Chart Example for {chart_type}
// No specific template available for this chart type
// See D3 documentation for details on implementing {chart_type} charts"""
    
    def _generate_bar_chart_template(self, data_format: str, features: List[str]) -> str:
        """Generate bar chart template."""
        return f"""// D3.js Bar Chart Example
// Data format: {data_format}
// Features: {', '.join(features)}

<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <script src="https://d3js.org/d3.v7.min.js"></script>
  <style>
    .bar {{ fill: steelblue; }}
    .bar:hover {{ fill: brown; }}
  </style>
</head>
<body>
  <svg width="600" height="400"></svg>
  <script>
    // Sample data - replace with your actual data
    const data = [
      {{name: "A", value: 10}},
      {{name: "B", value: 20}},
      {{name: "C", value: 30}},
      {{name: "D", value: 40}},
      {{name: "E", value: 50}}
    ];

    // Set up dimensions and margins
    const margin = {{top: 20, right: 20, bottom: 30, left: 40}};
    const width = 600 - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;

    // Create SVG
    const svg = d3.select("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", `translate(${{margin.left}},${{margin.top}})`);

    // Create scales
    const x = d3.scaleBand()
      .domain(data.map(d => d.name))
      .range([0, width])
      .padding(0.1);

    const y = d3.scaleLinear()
      .domain([0, d3.max(data, d => d.value)])
      .nice()
      .range([height, 0]);

    // Add bars
    svg.selectAll(".bar")
      .data(data)
      .enter().append("rect")
      .attr("class", "bar")
      .attr("x", d => x(d.name))
      .attr("y", d => y(d.value))
      .attr("width", x.bandwidth())
      .attr("height", d => height - y(d.value));

    // Add axes
    svg.append("g")
      .attr("transform", `translate(0,${{height}})`)
      .call(d3.axisBottom(x));

    svg.append("g")
      .call(d3.axisLeft(y));
  </script>
</body>
</html>"""
    
    def _generate_line_chart_template(self, data_format: str, features: List[str]) -> str:
        """Generate line chart template."""
        return f"""// D3.js Line Chart Example
// Data format: {data_format}
// Features: {', '.join(features)}

<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <script src="https://d3js.org/d3.v7.min.js"></script>
  <style>
    .line {{ fill: none; stroke: steelblue; stroke-width: 2px; }}
    .dot {{ fill: steelblue; }}
  </style>
</head>
<body>
  <svg width="600" height="400"></svg>
  <script>
    // Sample data - replace with your actual data
    const data = [
      {{date: "2022-01", value: 10}},
      {{date: "2022-02", value: 20}},
      {{date: "2022-03", value: 15}},
      {{date: "2022-04", value: 25}},
      {{date: "2022-05", value: 22}}
    ];

    // Parse dates
    const parseDate = d3.timeParse("%Y-%m");
    data.forEach(d => d.date = parseDate(d.date));

    // Set up dimensions and margins
    const margin = {{top: 20, right: 20, bottom: 30, left: 50}};
    const width = 600 - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;

    // Create SVG
    const svg = d3.select("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", `translate(${{margin.left}},${{margin.top}})`);

    // Create scales
    const x = d3.scaleTime()
      .domain(d3.extent(data, d => d.date))
      .range([0, width]);

    const y = d3.scaleLinear()
      .domain([0, d3.max(data, d => d.value)])
      .nice()
      .range([height, 0]);

    // Create line generator
    const line = d3.line()
      .x(d => x(d.date))
      .y(d => y(d.value));

    // Add line path
    svg.append("path")
      .datum(data)
      .attr("class", "line")
      .attr("d", line);

    // Add dots
    svg.selectAll(".dot")
      .data(data)
      .enter().append("circle")
      .attr("class", "dot")
      .attr("cx", d => x(d.date))
      .attr("cy", d => y(d.value))
      .attr("r", 4);

    // Add axes
    svg.append("g")
      .attr("transform", `translate(0,${{height}})`)
      .call(d3.axisBottom(x));

    svg.append("g")
      .call(d3.axisLeft(y));
  </script>
</body>
</html>"""
    
    async def recommend_chart(self, data_description: str, purpose: str) -> str:
        """Recommend a chart type based on data description and purpose."""
        lower_purpose = purpose.lower()
        lower_desc = data_description.lower()
        
        # Simple recommendation logic - would be more sophisticated in production
        if 'comparison' in lower_purpose or 'compare' in lower_purpose:
            if 'time' in lower_desc or 'dates' in lower_desc:
                return """Based on your need to compare data over time, I recommend a **Bar Chart** or **Line Chart**.

- **Bar Chart**: Good for comparing discrete categories over time periods
- **Line Chart**: Better for showing trends and continuous changes over time

Example D3 code for a line chart:
```javascript
const line = d3.line()
  .x(d => x(d.date))
  .y(d => y(d.value));

svg.append("path")
  .datum(data)
  .attr("class", "line")
  .attr("d", line);
```"""
            else:
                return """For comparing categories, I recommend a **Bar Chart** or **Grouped Bar Chart**.

- **Bar Chart**: Simple comparison of values across categories
- **Grouped Bar Chart**: Compare multiple variables across categories

Example D3 code for a basic bar chart:
```javascript
svg.selectAll(".bar")
  .data(data)
  .enter().append("rect")
  .attr("class", "bar")
  .attr("x", d => x(d.category))
  .attr("y", d => y(d.value))
  .attr("width", x.bandwidth())
  .attr("height", d => height - y(d.value));
```"""
        elif 'distribution' in lower_purpose or 'spread' in lower_purpose:
            return """For showing data distribution, I recommend a **Histogram**, **Box Plot**, or **Violin Plot**.

- **Histogram**: Shows the distribution of a single variable
- **Box Plot**: Shows median, quartiles, and outliers
- **Violin Plot**: Combines box plot with kernel density plot

Example D3 code for a histogram:
```javascript
const histogram = d3.histogram()
  .value(d => d.value)
  .domain(x.domain())
  .thresholds(x.ticks(20));

const bins = histogram(data);

svg.selectAll("rect")
  .data(bins)
  .enter().append("rect")
  .attr("x", d => x(d.x0))
  .attr("width", d => Math.max(0, x(d.x1) - x(d.x0) - 1))
  .attr("y", d => y(d.length))
  .attr("height", d => height - y(d.length));
```"""
        else:
            return """Based on your description, here are some general recommendations:

- For comparing values: **Bar Chart**
- For showing trends over time: **Line Chart**
- For parts of a whole: **Pie Chart**
- For distributions: **Histogram**
- For relationships: **Scatter Plot**

If you can provide more specific details about your data and goals, I can give a more tailored recommendation."""
    
    async def generate_ai_chart(self, description: str, data_example: str) -> AICompletionResponse:
        """Generate D3 code using AI."""
        try:
            # Get some examples from our D3 gallery for context
            gallery_doc = await self.document_service.get_document('d3-gallery')
            
            # Use AI service to generate code
            return await self.ai_service.generate_completion([
                AIMessage(
                    role="system",
                    content="You are a D3.js expert. Generate complete, working D3 code (v7) based on the user's request. Include HTML, CSS and JS. Make the result beautiful and professional."
                ),
                AIMessage(
                    role="user",
                    content=f"""I need a D3 visualization with these requirements:

Description: {description}

My data looks like this:
{data_example}

Please use D3.js v7 and create a complete working example including HTML, CSS and JavaScript."""
                )
            ])
        except Exception as error:
            return AICompletionResponse(
                text=f"Error generating D3 code: {error}",
                is_error=True
            )
    
    async def analyze_data(self, data: str, goal: str) -> AICompletionResponse:
        """Analyze data and suggest visualizations."""
        try:
            # Use AI service to analyze data
            return await self.ai_service.generate_completion([
                AIMessage(
                    role="system",
                    content="You are a data visualization expert. Analyze the provided data and suggest D3.js visualizations that would help achieve the user's goals."
                ),
                AIMessage(
                    role="user",
                    content=f"I have this data:\n\n{data}\n\nMy goal is: {goal}\n\nWhat D3.js visualizations would be most appropriate, and why?"
                )
            ])
        except Exception as error:
            return AICompletionResponse(
                text=f"Error analyzing data: {error}",
                is_error=True
            )


# Service singletons
_document_service: Optional[D3DocumentService] = None
_chart_service: Optional[ChartGenerationService] = None


def get_document_service(base_path: Optional[str] = None) -> D3DocumentService:
    """Get the D3 document service."""
    global _document_service
    if _document_service is None:
        if base_path is None:
            # Default to assets directory
            current_dir = Path(__file__).parent.parent.parent
            base_path = str(current_dir / "assets" / "llm-full")
        _document_service = FileSystemD3DocumentService(base_path)
    return _document_service


def get_chart_service() -> ChartGenerationService:
    """Get the chart generation service."""
    global _chart_service
    if _chart_service is None:
        ai_service = MockAIService()
        document_service = get_document_service()
        _chart_service = D3ChartGenerationService(ai_service, document_service)
    return _chart_service