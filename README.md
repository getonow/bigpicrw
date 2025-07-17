# BIGPICTURE Procurement Analytics

Este proyecto implementa un sistema completo de análisis de compras con IA que conecta múltiples fuentes de datos y utiliza agentes de IA para empoderar a los analistas de compras.

## Características

- 🤖 **Agente de IA Inteligente**: Analiza solicitudes de incremento/disminución de precios
- 📊 **4 Gráficos Interactivos**: Evolución de precios, análisis de volumen, comparación de mercado, y pronóstico de impacto
- 💡 **Insights Estructurados**: Resumen ejecutivo, análisis de impacto, y recomendaciones de negociación
- 🔄 **API RESTful**: Endpoints para integración con frontend
- 📈 **Visualizaciones Plotly**: Gráficos interactivos y responsivos

## Arquitectura

```
Frontend (Famous.ai) ←→ Backend (FastAPI) ←→ Supabase ←→ OpenAI
```

## Requisitos
- Python 3.9+
- PostgreSQL (Supabase)
- OpenAI API Key

## Instalación Backend

```bash
# Clonar repositorio
git clone <repository-url>
cd beta2

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales
```

## Variables de entorno
Crea un archivo `.env` en la raíz con:
```
OPENAI_API_KEY=tu_api_key_openai
DATABASE_URL=postgresql+asyncpg://usuario:password@host:puerto/db
SUPABASE_URL=tu_url_supabase
SUPABASE_KEY=tu_key_supabase
```

## Ejecución Backend

```bash
# Ejecutar servidor de desarrollo
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Probar el agente
python test_backend.py
```

## API Endpoints

### Health Check
```bash
GET /health
```

### Analizar Parte
```bash
POST /analyze-part/
Content-Type: application/json

{
  "message": "Supplier requesting 15% increase for part PA-10197"
}
```

**Respuesta:**
```json
{
  "text": "Análisis completo...",
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
  "summary": "Resumen ejecutivo...",
  "impact_analysis": "Análisis de impacto...",
  "recommendations": "Recomendaciones..."
}
```

## Integración Frontend

### 1. Usar Famous.ai
Utiliza el siguiente prompt en Famous.ai para generar el frontend:

```
Create a modern, professional procurement analytics dashboard with the following specifications:

**Main Layout:**
- Clean, enterprise-grade design with a dark/light theme toggle
- Header with company logo and "BIGPICTURE Procurement Analytics" title
- Sidebar navigation (collapsible) with menu items
- Main content area with responsive grid layout

**Chat Interface Section:**
- Large, prominent chat input area at the top center
- Placeholder text: "Enter your price increase/decrease request (e.g., 'Supplier requesting 15% increase for part PA-10197')"
- Send button with modern icon
- Chat history display below input showing user messages and AI responses
- Loading states with skeleton animations

**Analytics Dashboard Section:**
- 2x2 grid layout for 4 chart containers
- Each chart container should be responsive and have:
  - Chart title area
  - Chart rendering area (supporting Plotly.js)
  - Export/download button
  - Fullscreen toggle
- Chart containers should be labeled: "Price Evolution", "Volume Analysis", "Market Comparison", "Impact Forecast"
- Charts should be interactive with hover tooltips and zoom capabilities

**Insights Panel Section:**
- Large text area below charts for AI-generated insights
- Rich text formatting support (bold, italics, bullet points)
- Copy to clipboard functionality
- Export to PDF option
- Collapsible sections for different types of insights

**Technical Requirements:**
- Built with React/Next.js or Vue.js
- Use Tailwind CSS for styling
- Include Plotly.js library for chart rendering
- Responsive design for desktop, tablet, and mobile
- Modern UI components (buttons, inputs, cards, modals)
- Loading states and error handling
- Real-time updates capability

**Color Scheme:**
- Professional blue/gray palette
- Accent colors for important data points
- High contrast for accessibility
- Subtle gradients and shadows

**Additional Features:**
- Toast notifications for success/error messages
- Keyboard shortcuts (Enter to send, Ctrl+Enter for new line)
- Auto-save chat history
- Search functionality for past analyses
- Settings panel for user preferences
```

### 2. Instalar Dependencias Frontend
```bash
npm install plotly.js-dist axios react-markdown
```

### 3. Configurar API
Ver `FRONTEND_INTEGRATION_GUIDE.md` para instrucciones detalladas de integración.

## Uso

1. **Iniciar Backend:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Iniciar Frontend:**
   ```bash
   cd frontend-project
   npm start
   ```

3. **Usar la Aplicación:**
   - Ingresa una solicitud de cambio de precio en el chat
   - Ejemplo: "Supplier requesting 15% increase for part PA-10197"
   - Revisa los 4 gráficos generados
   - Lee los insights y recomendaciones de IA

## Estructura del Proyecto

```
beta2/
├── app/
│   ├── main.py              # FastAPI app con endpoints
│   ├── agent.py             # Lógica del agente de IA
│   ├── schemas.py           # Modelos Pydantic
│   ├── plotly_utils.py      # Generación de gráficos
│   ├── supabase_client.py   # Cliente de base de datos
│   └── config.py            # Configuración
├── requirements.txt         # Dependencias Python
├── test_backend.py          # Script de prueba
├── FRONTEND_INTEGRATION_GUIDE.md  # Guía de integración
└── README.md               # Este archivo
```

## Próximos Pasos

- [ ] Implementar exportación de gráficos
- [ ] Añadir autenticación de usuarios
- [ ] Historial de búsquedas
- [ ] Actualizaciones en tiempo real
- [ ] Filtros avanzados
- [ ] Optimización móvil

## Soporte

Para problemas o preguntas, revisa:
1. `FRONTEND_INTEGRATION_GUIDE.md` para integración
2. Logs del backend para errores
3. Consola del navegador para errores frontend 