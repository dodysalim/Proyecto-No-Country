# Verificación · LatAm Insights

Fecha: 7 de octubre de 2026 (Ecuador). Entorno local Python 3.12.14. Las dependencias de QA se registran aparte; esta comprobación no certifica todas las combinaciones de versiones del proyecto.

## Ejecutado

14 pruebas ETL y reportes aprobadas. Arranque del dashboard comprobado sin credenciales: muestra la falta de conexión, sin excepción no controlada.

## Dependencias externas y límites

Requiere SUPABASE_URL y SUPABASE_SERVICE_KEY en un .env local. GEMINI_API_KEY es opcional. La ausencia de credenciales se informa; no se inventan vacantes.

No se comprobó una extracción en vivo ni la escritura en Supabase. La disponibilidad depende de las fuentes, permisos y credenciales.

## Presentación Power BI

Las definiciones se revisaron para límites y superposiciones, y el diseño móvil sigue el esquema oficial PBIR. La prueba nativa completa en teléfono permanece pendiente. Las fuentes externas deben exportarse antes de actualizar las páginas sin datos.
