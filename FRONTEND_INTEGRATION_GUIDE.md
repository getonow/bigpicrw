# Frontend Integration Guide for BIGPICTURE Procurement Analytics

## Overview
This guide provides step-by-step instructions for integrating a Famous.ai generated frontend with the BIGPICTURE AI Agent backend.

## Backend API Endpoints

### Base URL
```
http://localhost:8000
```

### Available Endpoints

1. **Health Check**
   ```
   GET /health
   Response: {"status": "healthy", "service": "BIGPICTURE AI Agent"}
   ```

2. **Analyze Part**
   ```
   POST /analyze-part/
   Content-Type: application/json
   
   Request Body:
   {
     "message": "Supplier requesting 15% increase for part PA-10197"
   }
   
   Response:
   {
     "text": "Full AI response text...",
     "charts": [
       {
         "title": "Price Evolution",
         "plotly_json": {...},
         "chart_type": "price_evolution"
       },
       {
         "title": "Volume Analysis", 
         "plotly_json": {...},
         "chart_type": "volume_analysis"
       },
       {
         "title": "Market Comparison",
         "plotly_json": {...},
         "chart_type": "market_comparison"
       },
       {
         "title": "Impact Forecast",
         "plotly_json": {...},
         "chart_type": "impact_forecast"
       }
     ],
     "summary": "Executive summary...",
     "impact_analysis": "Detailed impact analysis...",
     "recommendations": "Negotiation recommendations..."
   }
   ```

## Frontend Integration Steps

### Step 1: Install Dependencies
```bash
npm install plotly.js-dist axios react-markdown
# or
yarn add plotly.js-dist axios react-markdown
```

### Step 2: API Service Setup
Create `src/services/api.js`:
```javascript
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const analyzePart = async (message) => {
  try {
    const response = await api.post('/analyze-part/', { message });
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

export const healthCheck = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    console.error('Health check failed:', error);
    throw error;
  }
};
```

### Step 3: Chart Component
Create `src/components/ChartContainer.jsx`:
```jsx
import React, { useEffect, useRef } from 'react';
import Plotly from 'plotly.js-dist';

const ChartContainer = ({ chartData, title, onExport, onFullscreen }) => {
  const chartRef = useRef(null);

  useEffect(() => {
    if (chartData && chartRef.current) {
      Plotly.newPlot(chartRef.current, chartData.data, chartData.layout, {
        responsive: true,
        displayModeBar: true,
        modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
      });
    }
  }, [chartData]);

  return (
    <div className="chart-container bg-white rounded-lg shadow-md p-4">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold text-gray-800">{title}</h3>
        <div className="flex space-x-2">
          <button
            onClick={onExport}
            className="px-3 py-1 text-sm bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            Export
          </button>
          <button
            onClick={onFullscreen}
            className="px-3 py-1 text-sm bg-gray-500 text-white rounded hover:bg-gray-600"
          >
            Fullscreen
          </button>
        </div>
      </div>
      <div ref={chartRef} className="w-full h-80" />
    </div>
  );
};

export default ChartContainer;
```

### Step 4: Main Dashboard Component
Create `src/components/Dashboard.jsx`:
```jsx
import React, { useState } from 'react';
import { analyzePart } from '../services/api';
import ChartContainer from './ChartContainer';
import ReactMarkdown from 'react-markdown';

const Dashboard = () => {
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!message.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const result = await analyzePart(message);
      setAnalysis(result);
    } catch (err) {
      setError('Failed to analyze part. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleExportChart = (chartData, title) => {
    // Implementation for chart export
    console.log('Exporting chart:', title);
  };

  const handleFullscreenChart = (chartData, title) => {
    // Implementation for fullscreen view
    console.log('Fullscreen chart:', title);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <h1 className="text-2xl font-bold text-gray-900">
              BIGPICTURE Procurement Analytics
            </h1>
            <div className="flex items-center space-x-4">
              <button className="px-4 py-2 bg-gray-200 rounded-md">
                Theme
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Chat Input */}
        <div className="mb-8">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="message" className="block text-sm font-medium text-gray-700 mb-2">
                Enter your price increase/decrease request
              </label>
              <textarea
                id="message"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="e.g., Supplier requesting 15% increase for part PA-10197"
                className="w-full h-32 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                disabled={loading}
              />
            </div>
            <button
              type="submit"
              disabled={loading || !message.trim()}
              className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Analyzing...' : 'Analyze Part'}
            </button>
          </form>
        </div>

        {/* Error Display */}
        {error && (
          <div className="mb-8 p-4 bg-red-50 border border-red-200 rounded-md">
            <p className="text-red-800">{error}</p>
          </div>
        )}

        {/* Analysis Results */}
        {analysis && (
          <div className="space-y-8">
            {/* Charts Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {analysis.charts.map((chart, index) => (
                <ChartContainer
                  key={index}
                  chartData={chart.plotly_json}
                  title={chart.title}
                  onExport={() => handleExportChart(chart.plotly_json, chart.title)}
                  onFullscreen={() => handleFullscreenChart(chart.plotly_json, chart.title)}
                />
              ))}
            </div>

            {/* Insights Panel */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">AI Insights</h2>
              
              {analysis.summary && (
                <div className="mb-6">
                  <h3 className="text-lg font-medium text-gray-700 mb-2">Executive Summary</h3>
                  <div className="prose max-w-none">
                    <ReactMarkdown>{analysis.summary}</ReactMarkdown>
                  </div>
                </div>
              )}

              {analysis.impact_analysis && (
                <div className="mb-6">
                  <h3 className="text-lg font-medium text-gray-700 mb-2">Impact Analysis</h3>
                  <div className="prose max-w-none">
                    <ReactMarkdown>{analysis.impact_analysis}</ReactMarkdown>
                  </div>
                </div>
              )}

              {analysis.recommendations && (
                <div className="mb-6">
                  <h3 className="text-lg font-medium text-gray-700 mb-2">Negotiation Recommendations</h3>
                  <div className="prose max-w-none">
                    <ReactMarkdown>{analysis.recommendations}</ReactMarkdown>
                  </div>
                </div>
              )}

              <div className="border-t pt-4">
                <h3 className="text-lg font-medium text-gray-700 mb-2">Full Analysis</h3>
                <div className="prose max-w-none">
                  <ReactMarkdown>{analysis.text}</ReactMarkdown>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
```

### Step 5: Environment Configuration
Create `.env.local`:
```
REACT_APP_API_BASE_URL=http://localhost:8000
```

### Step 6: CORS Configuration
Ensure your backend has CORS enabled (already done in main.py):
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Running the Application

### Backend
```bash
cd beta2
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd your-frontend-project
npm start
# or
yarn start
```

## Key Features Implemented

1. **Real-time Chart Rendering**: Uses Plotly.js to render interactive charts
2. **Structured Insights**: Displays AI analysis in organized sections
3. **Responsive Design**: Works on desktop, tablet, and mobile
4. **Error Handling**: Graceful error handling and loading states
5. **Export Functionality**: Ready for chart export implementation
6. **Markdown Support**: Renders AI responses with proper formatting

## Next Steps

1. **Implement Chart Export**: Add functionality to export charts as PNG/PDF
2. **Add Authentication**: Implement user authentication if needed
3. **Add Search History**: Store and search past analyses
4. **Real-time Updates**: Add WebSocket support for real-time updates
5. **Advanced Filtering**: Add filters for different chart types
6. **Mobile Optimization**: Enhance mobile experience

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure backend CORS is properly configured
2. **Chart Not Rendering**: Check if Plotly.js is properly imported
3. **API Connection**: Verify backend is running on correct port
4. **Chart Data Format**: Ensure plotly_json is properly formatted

### Debug Tips

1. Check browser console for errors
2. Verify API responses in Network tab
3. Test API endpoints with Postman/curl
4. Check backend logs for errors 