#!/usr/bin/env python3
"""
Test script for BIGPICTURE AI Agent backend
"""

import asyncio
import json
from app.agent import analyze_part

async def test_agent():
    """Test the AI agent with a sample request"""
    
    # Test message
    test_message = "Supplier requesting 15% increase for part PA-10197"
    
    print("Testing BIGPICTURE AI Agent...")
    print(f"Input message: {test_message}")
    print("-" * 50)
    
    try:
        # Call the agent
        result = await analyze_part(None, test_message)
        
        print("✅ Agent response received successfully!")
        print(f"Text length: {len(result['text'])} characters")
        print(f"Number of charts: {len(result['charts'])}")
        
        # Display chart titles
        for i, chart in enumerate(result['charts'], 1):
            print(f"Chart {i}: {chart['title']} ({chart['chart_type']})")
        
        # Display structured sections
        if result.get('summary'):
            print(f"\n📋 Summary: {len(result['summary'])} characters")
        
        if result.get('impact_analysis'):
            print(f"📊 Impact Analysis: {len(result['impact_analysis'])} characters")
        
        if result.get('recommendations'):
            print(f"💡 Recommendations: {len(result['recommendations'])} characters")
        
        print("\n" + "="*50)
        print("Full AI Response:")
        print("="*50)
        print(result['text'])
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing agent: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_agent())
    if success:
        print("\n✅ Backend test completed successfully!")
    else:
        print("\n❌ Backend test failed!") 