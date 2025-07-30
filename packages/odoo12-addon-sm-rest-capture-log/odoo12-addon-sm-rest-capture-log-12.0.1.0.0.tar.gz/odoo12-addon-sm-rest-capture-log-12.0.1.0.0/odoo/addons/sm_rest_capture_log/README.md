# REST Capture Log Module

## Descripción

Módulo temporal para Odoo 12 que intercepta y registra todas las peticiones REST realizadas a través de `base_rest` durante el proceso de migración a Odoo 17.

## Funcionalidades

### Captura de Peticiones
- ✅ Intercepta todas las peticiones HTTP (GET, POST, PUT, DELETE, etc.)
- ✅ Registra fecha y hora de cada petición
- ✅ Captura método HTTP, URL completa y parámetros de query
- ✅ Almacena headers completos de la petición
- ✅ Guarda el cuerpo (body) de la petición
- ✅ Registra IP del cliente y User-Agent
- ✅ Identifica nombre del endpoint y servicio cuando es posible

### Captura de Respuestas
- ✅ Registra código de estado HTTP
- ✅ Almacena headers de respuesta
- ✅ Guarda cuerpo de la respuesta
- ✅ Mide tiempo de respuesta en milisegundos
- ✅ Maneja errores y excepciones

### Gestión de Migración
- ✅ Estado de procesamiento (pendiente, procesado, error, migrado)
- ✅ Marcado de peticiones migradas a Odoo 17
- ✅ Notas de migración
- ✅ Función para obtener datos de replay

## Instalación

1. Copiar el módulo al directorio de addons de Odoo 12
2. Actualizar la lista de módulos
3. Instalar el módulo `sm_rest_capture_log`

## Dependencias

- `base` (Odoo core)
- `base_rest` (OCA)

## Uso

### Visualización de Logs

Acceder al menú: **REST Capture Log > Request Logs**

### Filtros Disponibles
- Por método HTTP (GET, POST, PUT, DELETE)
- Por estado de procesamiento
- Por fecha (hoy, última semana)
- Por estado de migración

### Funciones de Migración

```python
# Marcar como migrado
log_entry.mark_as_migrated("Migrado exitosamente a Odoo 17")

# Obtener datos para replay
replay_data = log_entry.get_replay_data()
```

## Arquitectura Técnica

### Interceptación
El módulo utiliza monkey patching sobre el método `dispatch` de `RestController` de `base_rest` para interceptar todas las peticiones de forma transparente.

### Almacenamiento
Todos los datos se almacenan en el modelo `rest.request.log` con transacciones independientes para evitar interferir con el procesamiento normal.

### Compatibilidad
Diseñado para ser completamente compatible con `base_rest` sin afectar su funcionamiento normal.

## Modelo de Datos

### Campos Principales

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `request_datetime` | Datetime | Fecha y hora de la petición |
| `http_method` | Selection | Método HTTP (GET, POST, etc.) |
| `request_url` | Text | URL completa con parámetros |
| `endpoint_name` | Char | Nombre del endpoint |
| `service_name` | Char | Nombre del servicio base_rest |
| `request_headers` | Text | Headers de la petición (JSON) |
| `request_body` | Text | Cuerpo de la petición |
| `client_ip` | Char | IP del cliente |
| `response_status_code` | Integer | Código de estado HTTP |
| `response_body` | Text | Cuerpo de la respuesta |
| `response_time_ms` | Float | Tiempo de respuesta en ms |
| `processing_status` | Selection | Estado del procesamiento |
| `migrated_to_odoo17` | Boolean | Marcador de migración |

## Consideraciones de Rendimiento

- Las operaciones de logging se realizan en cursores separados
- Manejo de errores robusto para no afectar las peticiones normales
- Logging asíncrono para minimizar impacto en tiempo de respuesta

## Seguridad

- Acceso de lectura para usuarios normales
- Acceso completo solo para administradores del sistema
- Los datos sensibles se almacenan de forma segura

## Migración a Odoo 17

### Proceso de Replay

1. Exportar logs desde Odoo 12
2. Implementar endpoints equivalentes en Odoo 17
3. Reproducir peticiones usando `get_replay_data()`
4. Marcar como migradas usando `mark_as_migrated()`

### Script de Ejemplo

```python
# Obtener peticiones no migradas
pending_logs = env['rest.request.log'].search([
    ('migrated_to_odoo17', '=', False),
    ('processing_status', '=', 'processed')
])

for log in pending_logs:
    replay_data = log.get_replay_data()
    # Procesar en Odoo 17
    # ...
    log.mark_as_migrated("Procesado en Odoo 17")
```

## Limitaciones

- Solo funciona con endpoints definidos por `base_rest`
- Requiere que `base_rest` esté instalado y funcionando
- Módulo temporal, no recomendado para uso en producción a largo plazo

## Soporte

Este es un módulo temporal para migración. Para soporte contactar al equipo de desarrollo de Som Mobilitat.

## Licencia

Módulo propietario de Som Mobilitat SCCL.