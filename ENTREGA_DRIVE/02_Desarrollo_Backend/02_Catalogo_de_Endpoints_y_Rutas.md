# Catálogo y Documentación de Endpoints / Rutas del Sistema
## Backend — Sistema de Gestión de Stock e Inventario
**Fecha de Actualización:** Ciclo Lectivo 2026  
**Versión:** 1.0 (Documentación Técnica Individual)  
**Autor:** Lucas Ignacio Kiernicki  
**Institución:** ISFDyT N° 210 — La Plata  

---

### 1. Arquitectura de Comunicación del Backend
El backend utiliza el paradigma de Renderizado del Lado del Servidor (**Server-Side Rendering — SSR**) mediante el motor de plantillas de Django, combinado con la gestión de estado interactivo mediante JavaScript nativo para la manipulación del DOM (modo oscuro con almacenamiento local y popups dinámicos para mensajes del servidor).

---

### 2. Catálogo Detallado de Rutas (Endpoints)

| Método HTTP | Ruta (URI) | Nombre de Ruta (`name`) | Tipo de Respuesta | Lógica y Comportamiento del Endpoint |
| :---: | :--- | :--- | :--- | :--- |
| **GET** | `/` | `home_admin` | HTML (`dashboard.html`) | Consulta los productos activos (`activo=True`), calcula las métricas cuantitativas (total de artículos, alertas de stock bajo y movimientos de la fecha) y renderiza la pantalla principal. |
| **GET** | `/crear_producto/` | `crear_producto` | HTML (`crear_producto.html`) | Renderiza el formulario de alta con el selector de categorías disponibles. |
| **POST** | `/crear_producto/` | `crear_producto` | Redirección (302 a `home_admin`) | Valida los campos ingresados, crea el producto dentro de un bloque atómico y, si el stock inicial es > 0, genera de inmediato el movimiento de tipo 'ALTA'. Emite mensaje de éxito. |
| **GET** | `/editar_producto/<id>/` | `editar_producto` | HTML (`crear_producto.html`) | Recupera el producto activo por su ID y presenta el formulario pre-cargado para su edición. |
| **POST** | `/editar_producto/<id>/` | `editar_producto` | Redirección (302 a `home_admin`) | Actualiza los datos base del artículo. Si se alteró el stock en este formulario, registra de forma automática un movimiento de tipo 'AJUSTE' por la diferencia neta calculada. |
| **POST / GET** | `/eliminar_producto/<id>/` | `eliminar_producto` | Redirección (302 a `home_admin`) | Ejecuta la baja lógica del artículo estableciendo `producto.activo = False`. No destruye filas en la base de datos, preservando la trazabilidad. |
| **GET** | `/movimientos/` | `movimientos` | HTML (`movimientos.html`) | Obtiene la lista completa de movimientos ordenados cronológicamente (`order_by('-fecha')`) y los productos activos para alimentar el selector del formulario. |
| **POST** | `/movimientos/` | `movimientos` | Redirección (302 a `movimientos`) | Procesa entradas y salidas. Valida que la cantidad sea > 0. En salidas, verifica saldo suficiente; si no alcanza, bloquea la operación y envía mensaje de error. Si es válido, actualiza el stock y guarda el movimiento atómicamente. |
| **GET** | `/categorias/` | `listar_categorias` | HTML (`categorias.html`) | Lista todas las categorías registradas y calcula dinámicamente cuántos productos activos tiene asignada cada una. |
| **GET / POST** | `/categorias/crear/` | `crear_categoria` | HTML / Redirección (302) | Presenta el formulario de carga y guarda nuevas categorías en la base de datos. |
| **GET / POST** | `/categorias/editar/<id>/`| `editar_categoria` | HTML / Redirección (302) | Permite modificar la denominación de una categoría existente. |
| **POST** | `/categorias/eliminar/<id>/`| `eliminar_categoria` | Redirección (302 a `listar_categorias`) | Elimina la categoría seleccionada de la base de datos. |
| **GET / POST** | `/admin/` | `admin:index` | HTML (Django Admin) | Panel nativo de administración para gestión avanzada de datos y usuarios por parte del superadministrador. |
