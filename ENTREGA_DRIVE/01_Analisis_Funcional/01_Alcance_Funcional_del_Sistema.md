# Alcance Funcional del Sistema (Ciclo 2026)
## Sistema de Gestión de Stock e Inventario
**Estudiante:** Lucas Ignacio Kiernicki  
**Carrera:** Tecnicatura Superior en Análisis de Sistemas (3° Año)  
**Institución:** ISFDyT N° 210 — La Plata  
**Espacios Curriculares:** Prácticas Profesionalizantes III / Seminario de Actualización e Ing. de Software II / Algoritmos y ED III

---

### 1. Objetivo
Digitalizar, centralizar y optimizar la administración de stock e inventario en comercios y depósitos de distribución, reemplazando el registro informal o manual en planillas de cálculo ("sheets") por una plataforma web segura desarrollada en Django. El sistema busca asegurar la integridad de los datos, evitar pérdidas de mercadería mediante una trazabilidad absoluta de entradas y salidas, e impedir errores críticos como el stock negativo.

---

### 2. Módulos Incluidos

* **Módulo de Dashboard y Métricas Principales:**
  * Panel de control centralizado con métricas cuantitativas en tiempo real: total de artículos registrados, cantidad de alertas por stock bajo (<= 2 unidades) y total de movimientos procesados durante la jornada.
  * Tabla con visualización de los últimos movimientos realizados para auditoría rápida.

* **Módulo de Gestión de Productos (Catálogo de Artículos):**
  * Alta de nuevos productos especificando denominación, asignación de categoría, precio unitario y stock inicial.
  * Modificación de datos descriptivos, categoría y precio.
  * Ajuste manual de stock con registro automático del motivo de ajuste.
  * Baja lógica del producto (`activo = False`) que oculta el artículo del inventario activo pero preserva intacto todo el historial de movimientos previo.

* **Módulo de Clasificación por Categorías:**
  * Alta, modificación y eliminación de rubros o categorías de inventario.
  * Conteo dinámico y automático de la cantidad de productos activos asociados a cada categoría.

* **Módulo de Movimientos de Stock (Entradas y Salidas):**
  * Registro de **Entradas (Reposición / Compras)** con incremento automático del stock disponible.
  * Registro de **Salidas (Consumo / Ventas)** con descuento automático del stock físico.
  * Control y validación estricta que bloquea cualquier salida si la cantidad solicitada supera el stock disponible (prevención de stock negativo).
  * Historial cronológico inmutable con fecha, hora, producto, tipo de movimiento, cantidad y motivo/observación.

* **Módulo de Administración (Django Admin):**
  * Panel nativo de Django configurado con permisos, filtros avanzados, búsquedas por nombre y campos de auditoría protegidos contra edición directa.

* **Módulo de Ergonomía Visual (Modo Claro / Modo Oscuro):**
  * Selector de tema visual con persistencia en el navegador del operador (`localStorage`).

---

### 3. Módulos Fuera de Alcance
* Facturación electrónica directa con AFIP.
* Cobro digital mediante pasarelas de pago externas (MercadoPago / Stripe).
* Gestión de compras automatizadas mediante API de proveedores externos.
* Módulo de logística de envíos con geolocalización.

---

### 4. Supuestos
* El usuario operador dispone de una computadora o dispositivo con navegador web moderno (Chrome, Edge, Firefox).
* La conectividad de red se mantiene estable durante las operaciones de registro de movimientos.
* Las cantidades cargadas en stock corresponden a unidades enteras medibles físicamente.

---

### 5. Restricciones
* La aplicación se ejecuta bajo el framework Django 5.x utilizando Python 3.10 o superior.
* El motor de base de datos relacional para el entorno local es SQLite3, garantizando portabilidad sin necesidad de instalar servicios pesados de bases de datos.
* Todas las operaciones que modifican el stock deben ejecutarse en bloques atómicos (`transaction.atomic`) para evitar inconsistencias por interrupciones o concurrencia.
