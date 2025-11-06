# Guía para Solucionar el Error de Healthcheck en Railway

## Problema Identificado

El servicio estaba fallando en el healthcheck porque:
1. **Falta de validación de variables de entorno**: Si faltaban variables críticas, la aplicación podía fallar al iniciar
2. **Healthcheck no robusto**: El endpoint `/health` no manejaba errores correctamente
3. **Falta de logging**: Era difícil diagnosticar problemas sin logs adecuados

## Cambios Realizados

### 1. Mejoras en `app/config.py`
- ✅ Agregado logging para advertir sobre variables faltantes
- ✅ La aplicación ahora puede iniciar incluso si faltan algunas variables (solo advertirá)

### 2. Mejoras en `app/main.py`
- ✅ Healthcheck robusto que siempre retorna 200 si el servicio está corriendo
- ✅ Logging detallado al iniciar
- ✅ Manejo de errores mejorado en endpoints
- ✅ Evento de startup que muestra el estado de configuración

### 3. Mejoras en `app/supabase_client.py`
- ✅ Validación de credenciales antes de hacer requests
- ✅ Timeout configurado (30 segundos)
- ✅ Mejor manejo de errores con logging

### 4. Mejoras en `app/agent.py`
- ✅ Validación de API key antes de usar OpenAI
- ✅ Timeout configurado para requests a OpenAI (60 segundos)
- ✅ Mejor manejo de errores

### 5. Mejoras en `railway.json`
- ✅ Aumentado `healthcheckTimeout` de 100 a 300 segundos

## Pasos para Solucionar el Problema en Railway

### Paso 1: Verificar Variables de Entorno

En el dashboard de Railway, ve a **Settings → Variables** y asegúrate de tener configuradas:

```
OPENAI_API_KEY=tu_api_key_de_openai
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_ANON_KEY=tu_anon_key_de_supabase
```

**⚠️ IMPORTANTE**: 
- `SUPABASE_KEY` en el README se refiere a `SUPABASE_ANON_KEY` en el código
- Verifica que los nombres de las variables coincidan exactamente

### Paso 2: Hacer Push de los Cambios

```bash
# Asegúrate de estar en la rama main
git add .
git commit -m "Fix: Improve healthcheck and error handling for Railway deployment"
git push origin main
```

### Paso 3: Verificar el Despliegue

1. Ve al dashboard de Railway
2. Espera a que se complete el build (debería tomar ~1 minuto)
3. Revisa los logs en la pestaña **Logs**
4. Deberías ver mensajes como:
   ```
   Starting BIGPICTURE AI Agent...
   OpenAI API Key configured: True/False
   Supabase URL configured: True/False
   Server will listen on port: [puerto]
   ```

### Paso 4: Probar el Healthcheck

Una vez desplegado, prueba el endpoint:

```bash
curl https://tu-app.railway.app/health
```

Deberías recibir:
```json
{
  "status": "healthy",
  "service": "BIGPICTURE AI Agent",
  "config": {
    "openai_configured": true,
    "supabase_configured": true
  }
}
```

### Paso 5: Verificar Logs si Aún Falla

Si el healthcheck aún falla:

1. Ve a **Logs** en Railway
2. Busca errores relacionados con:
   - Variables de entorno faltantes
   - Errores de importación
   - Errores de conexión a Supabase
   - Errores de OpenAI

## Solución de Problemas Comunes

### Error: "Module not found"
**Solución**: Verifica que `requirements.txt` tenga todas las dependencias necesarias.

### Error: "Supabase credentials not configured"
**Solución**: Asegúrate de que `SUPABASE_URL` y `SUPABASE_ANON_KEY` estén configuradas en Railway.

### Error: "OpenAI API key is not configured"
**Solución**: Asegúrate de que `OPENAI_API_KEY` esté configurada en Railway.

### Error: "Healthcheck timeout"
**Solución**: 
- Verifica que el puerto esté configurado correctamente (Railway lo establece automáticamente)
- Revisa los logs para ver si hay errores al iniciar
- El timeout ahora es de 300 segundos, debería ser suficiente

### El servicio inicia pero el healthcheck falla
**Solución**: 
- Verifica que el endpoint `/health` esté accesible
- Prueba manualmente: `curl https://tu-app.railway.app/health`
- Revisa los logs para ver si hay errores en el endpoint

## Verificación Final

Una vez que el servicio esté funcionando:

1. ✅ Healthcheck responde correctamente
2. ✅ Logs muestran configuración correcta
3. ✅ Endpoint `/` responde
4. ✅ Endpoint `/analyze-part/` funciona (requiere variables configuradas)

## Notas Adicionales

- El healthcheck ahora es más robusto y siempre retornará 200 si el servicio está corriendo
- Los logs te ayudarán a diagnosticar problemas de configuración
- La aplicación puede iniciar incluso si faltan algunas variables (solo advertirá en los logs)
- Los endpoints funcionales (como `/analyze-part/`) validarán las variables cuando se necesiten

