from pydantic import BaseModel
from typing import Dict, Any, List, Optional

class AnalyzePartRequest(BaseModel):
    message: str

class AgentTextResponse(BaseModel):
    text: str

class AgentGraphResponse(BaseModel):
    plotly_json: Dict[str, Any]

class ChartData(BaseModel):
    title: str
    plotly_json: Dict[str, Any]
    chart_type: str = "price_evolution"

class AnalyzePartResponse(BaseModel):
    text: str
    charts: List[ChartData]
    summary: Optional[str] = None
    impact_analysis: Optional[str] = None
    recommendations: Optional[str] = None 