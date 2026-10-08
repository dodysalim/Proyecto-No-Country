# LatAm Job Market — Power BI

PENDIENTE DE DATOS · Supabase sin exportación disponible · no se muestran vacantes ficticias

## Abrir

1. Descarga el repositorio completo.
2. Ejecuta `python powerbi/configure_data.py`. Alternativamente, en Transformar datos → Administrar parámetros cambia `DataFolder` a la carpeta `powerbi/data/` con separador final.
3. Abre `powerbi/Analytics.pbip` en Power BI Desktop y pulsa Actualizar.

## Estructura y correspondencia

Se conservan las diez pestañas del Streamlit original. Las tablas están vacías porque faltan exportaciones autorizadas de Supabase. `Vacantes.csv` y `Skills.csv` deben reemplazarse por exportaciones con las columnas indicadas. Skills usa las métricas precalculadas del original; no se interpreta crecimiento como demanda absoluta. Scraping, Gemini y escritura de reportes permanecen en Python.

Las páginas conservan el análisis del proyecto original. Los controles de entrenamiento, conexión, escritura SQL e inferencia en vivo siguen en Python/Streamlit. El informe consume resultados exportados; no reemplaza esos servicios. Los CSV conservan su grano, y las medidas evitan sumar porcentajes o promedios.

## Verificación de esta entrega

El serializador TMDL nativo instalado con Power BI Desktop aceptó el modelo. Se comprobaron las referencias de los campos y los límites de cada visual. Esto valida la estructura; la apertura, actualización y representación de los gráficos se comprueban por separado. Los proyectos sin datos siguen pendientes.
