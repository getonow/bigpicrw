import plotly.graph_objs as go
from plotly.subplots import make_subplots
from typing import List, Dict, Optional
import plotly.express as px

def price_evolution_figure(price_data: List[float], market_index_data: List[float], months: List[str]) -> Dict:
    """Create price evolution chart"""
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=price_data, mode='lines+markers', name='Company Price', line=dict(color='#2563eb')))
    if any(market_index_data):
        fig.add_trace(go.Scatter(x=months, y=market_index_data, mode='lines+markers', name='Market Index', line=dict(color='#dc2626')))
    fig.update_layout(
        title='Price Evolution Over Time',
        xaxis_title='Month',
        yaxis_title='Price',
        legend_title='Legend',
        template='plotly_white',
        height=400
    )
    return fig.to_dict()

def volume_analysis_figure(volume_data: List[float], months: List[str]) -> Dict:
    """Create volume analysis chart"""
    fig = go.Figure()
    fig.add_trace(go.Bar(x=months, y=volume_data, name='Volume', marker_color='#059669'))
    fig.update_layout(
        title='Volume Analysis',
        xaxis_title='Month',
        yaxis_title='Volume',
        template='plotly_white',
        height=400
    )
    return fig.to_dict()

def market_comparison_figure(company_prices: List[float], market_prices: List[float], months: List[str]) -> Dict:
    """Create market comparison chart"""
    fig = make_subplots(rows=2, cols=1, subplot_titles=('Price Comparison', 'Price Difference'))
    
    # Price comparison
    fig.add_trace(go.Scatter(x=months, y=company_prices, mode='lines+markers', name='Company Price'), row=1, col=1)
    fig.add_trace(go.Scatter(x=months, y=market_prices, mode='lines+markers', name='Market Price'), row=1, col=1)
    
    # Price difference
    price_diff = [cp - mp if cp and mp else 0 for cp, mp in zip(company_prices, market_prices)]
    fig.add_trace(go.Bar(x=months, y=price_diff, name='Price Difference'), row=2, col=1)
    
    fig.update_layout(height=600, template='plotly_white', showlegend=True)
    return fig.to_dict()

def impact_forecast_figure(current_price: float, new_price: float, volumes: List[float], months: List[str]) -> Dict:
    """Create impact forecast chart"""
    current_cost = [v * current_price for v in volumes]
    new_cost = [v * new_price for v in volumes]
    cost_increase = [nc - cc for nc, cc in zip(new_cost, current_cost)]
    
    fig = make_subplots(rows=2, cols=1, subplot_titles=('Cost Comparison', 'Cost Increase Impact'))
    
    fig.add_trace(go.Scatter(x=months, y=current_cost, mode='lines+markers', name='Current Cost'), row=1, col=1)
    fig.add_trace(go.Scatter(x=months, y=new_cost, mode='lines+markers', name='New Cost'), row=1, col=1)
    fig.add_trace(go.Bar(x=months, y=cost_increase, name='Cost Increase', marker_color='#dc2626'), row=2, col=1)
    
    fig.update_layout(height=600, template='plotly_white', showlegend=True)
    return fig.to_dict()

def create_all_charts(price_data: List[float], market_data: List[float], volume_data: List[float], 
                     months: List[str], current_price: float, new_price: float) -> List[Dict]:
    """Create all four charts for the dashboard"""
    charts = []
    
    # Chart 1: Price Evolution
    charts.append({
        "title": "Price Evolution",
        "plotly_json": price_evolution_figure(price_data, market_data, months),
        "chart_type": "price_evolution"
    })
    
    # Chart 2: Volume Analysis
    charts.append({
        "title": "Volume Analysis", 
        "plotly_json": volume_analysis_figure(volume_data, months),
        "chart_type": "volume_analysis"
    })
    
    # Chart 3: Market Comparison
    charts.append({
        "title": "Market Comparison",
        "plotly_json": market_comparison_figure(price_data, market_data, months),
        "chart_type": "market_comparison"
    })
    
    # Chart 4: Impact Forecast
    charts.append({
        "title": "Impact Forecast",
        "plotly_json": impact_forecast_figure(current_price, new_price, volume_data, months),
        "chart_type": "impact_forecast"
    })
    
    return charts 