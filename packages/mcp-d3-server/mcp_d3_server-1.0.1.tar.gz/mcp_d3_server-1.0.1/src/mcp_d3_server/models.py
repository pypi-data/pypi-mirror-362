"""Type definitions for the MCP D3 server."""

from typing import Dict, List, Optional, Protocol
from pydantic import BaseModel


class AIMessage(BaseModel):
    """Message to AI service."""
    role: str
    content: str


class AICompletionResponse(BaseModel):
    """AI service completion response."""
    text: str
    is_error: bool = False


class D3Document(BaseModel):
    """D3 document content."""
    name: str
    content: str
    sections: Dict[str, str]


class AIService(Protocol):
    """Interface for AI service."""
    
    async def generate_completion(
        self, 
        messages: List[AIMessage], 
        options: Optional[Dict] = None
    ) -> AICompletionResponse:
        """Generate a completion from the AI service."""
        ...


class ChartGenerationService(Protocol):
    """Interface for chart generation service."""
    
    async def generate_chart_code(
        self, 
        chart_type: str, 
        data_format: str, 
        features: Optional[List[str]] = None
    ) -> str:
        """Generate D3 chart code."""
        ...
    
    async def recommend_chart(
        self, 
        data_description: str, 
        purpose: str
    ) -> str:
        """Recommend a chart type based on data description and purpose."""
        ...
    
    async def generate_ai_chart(
        self, 
        description: str, 
        data_example: str
    ) -> AICompletionResponse:
        """Generate D3 code using AI."""
        ...
    
    async def analyze_data(
        self, 
        data: str, 
        goal: str
    ) -> AICompletionResponse:
        """Analyze data and suggest visualizations."""
        ...


class D3DocumentService(Protocol):
    """Interface for document service."""
    
    async def get_document(self, name: str) -> D3Document:
        """Get document by name."""
        ...
    
    async def search_documents(self, query: str) -> List[Dict[str, str]]:
        """Search across documents."""
        ...
    
    async def get_document_section(self, name: str, section: str) -> Optional[str]:
        """Get document sections."""
        ...
    
    async def list_documents(self) -> List[str]:
        """List available documents."""
        ...