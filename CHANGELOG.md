# Changelog

Todos los cambios relevantes de este proyecto se documentan aquí.
El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y [Versionado Semántico](https://semver.org/lang/es/).

## [2.0.0] - 2026-10-26

### 🔧 Mantenimiento

- **Arquitectura:** `dashboard.py` (1.043 líneas) dividido en el paquete `dashboard_app/` con capas `config`, `data`, `services` y `ui`. El punto de entrada (`streamlit run dashboard.py`) no cambia.
- **SOLID:** la UI depende del protocolo `JobMarketRepository` (inversión de dependencias); Supabase es un adaptador intercambiable. Las pestañas se registran en una lista (abierto/cerrado) y cada módulo tiene una sola responsabilidad.
- **DRY:** una fábrica de gráficos reemplaza 13 bloques de Plotly casi idénticos.
- **Diseño moderno:** tema oscuro coherente con el portafolio, encabezado destacado, tarjetas de KPI, pestañas tipo píldora y gráficos con estilo unificado.
- **Corregido:** propiedad CSS mal escrita (`box_shadow`) que anulaba la sombra de los botones.
- 13 pruebas nuevas para limpieza, filtros, KPIs, comandos, caché y repositorio (27 en total).
- Verificación: con datos de prueba, el dashboard modular muestra el mismo contenido que el original en las 10 pestañas (13 gráficos, 0 errores).

## [1.1.0] - 2026-10-26

### 🔧 Mantenimiento

- Verificación: 14 pruebas del ETL y reportes aprobadas en un entorno limpio con Python 3.12.
- Arranque del dashboard comprobado sin credenciales: informa la falta de conexión a Supabase sin excepciones.
- README con insignias de CI y versión.
