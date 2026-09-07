# DER — Diagrama de Entidad-Relación y Diccionario de Datos
## Backend — Sistema de Gestión de Stock e Inventario
**Fecha de Actualización:** Ciclo Lectivo 2026  
**Autor:** Lucas Ignacio Kiernicki  
**Institución:** ISFDyT N° 210 — La Plata  

---

### 1. INTRODUCCIÓN AL DISEÑO DE DATOS (Django ORM)
El diseño y persistencia de la base de datos se gestiona a través del Object-Relational Mapping (ORM) nativo de Django, el cual mapea las entidades de negocio en clases de Python dentro de `inventario/models.py`. 
El motor de persistencia utilizado es **SQLite3**, configurado con soporte transaccional completo, claves primarias autoincrementales y verificación estricta de restricciones de integridad referencial.

---

### 2. ESQUEMA DE ENTIDADES Y RELACIONES

| Entidad (Tabla) | Clave Primaria (PK) | Claves Foráneas (FK) | Cardinalidad / Tipo de Relación |
| :--- | :--- | :--- | :--- |
| **Categoria** (`inventario_categoria`) | `id` (BigAutoField) | Ninguna | 1 a Muchos con `Producto` |
| **Producto** (`inventario_producto`) | `id` (BigAutoField) | `categoria_id` (FK a Categoria) | Muchos a 1 con `Categoria`<br>1 a Muchos con `Movimiento` |
| **Movimiento** (`inventario_movimiento`) | `id` (BigAutoField) | `producto_id` (FK a Producto) | Muchos a 1 con `Producto` (`on_delete=SET_NULL`) |

---

### 3. DICCIONARIO DE DATOS DETALLADO

#### Tabla 1: `inventario_categoria` (Clasificación de Artículos)
| Nombre de Campo | Tipo Django | Atributos / Restricciones | Descripción Funcional |
| :--- | :--- | :--- | :--- |
| `id` | `BigAutoField` | `primary_key=True`, `auto_created=True` | Identificador único autoincremental de la categoría. |
| `nombre` | `CharField(max_length=100)` | `null=False`, `blank=False` | Denominación del rubro o categoría (ej: "Periféricos", "Herramientas"). |
| `descripcion` | `CharField(max_length=255)` | `null=True`, `blank=True` | Detalle o alcance del rubro de productos clasificados. |

#### Tabla 2: `inventario_producto` (Catálogo de Artículos y Stock)
| Nombre de Campo | Tipo Django | Atributos / Restricciones | Descripción Funcional |
| :--- | :--- | :--- | :--- |
| `id` | `BigAutoField` | `primary_key=True`, `auto_created=True` | Identificador único del producto en el catálogo. |
| `nombre` | `CharField(max_length=150)` | `null=False`, `blank=False` | Nombre o descripción comercial del artículo. |
| `categoria_id` | `ForeignKey(Categoria)` | `on_delete=models.CASCADE` | Enlace con la categoría a la que pertenece el producto. |
| `precio` | `DecimalField(10, 2)` | `max_digits=10`, `decimal_places=2` | Precio unitario del producto en moneda local. |
| `stock` | `IntegerField` | `default=0` | Cantidad de unidades físicas disponibles en depósito. |
| `activo` | `BooleanField` | `default=True` | Indicador de baja lógica. Si es `False`, el artículo se oculta sin borrar su historial. |

#### Tabla 3: `inventario_movimiento` (Auditoría de Entradas y Salidas)
| Nombre de Campo | Tipo Django | Atributos / Restricciones | Descripción Funcional |
| :--- | :--- | :--- | :--- |
| `id` | `BigAutoField` | `primary_key=True`, `auto_created=True` | Identificador único del movimiento contable. |
| `producto_id` | `ForeignKey(Producto)` | `on_delete=models.SET_NULL`, `null=True`, `blank=True` | Producto involucrado. Protegido contra borrado en cascada. |
| `tipo` | `CharField(max_length=10)` | `choices=['ENTRADA', 'SALIDA', 'ALTA', 'AJUSTE']` | Naturaleza de la operación realizada. |
| `cantidad` | `IntegerField` | `null=False`, `min_value=1` | Número de unidades que ingresaron o egresaron. |
| `motivo` | `CharField(max_length=200)` | `null=True`, `blank=True` | Justificación del movimiento (ej: "Compra proveedor", "Venta mostrador"). |
| `fecha` | `DateTimeField` | `auto_now_add=True` | Marca temporal exacta generada por el servidor al confirmar la operación. |

---

### 4. POLÍTICAS DE INTEGRIDAD Y REGLAS DE NEGOCIO
1. **Protección de Auditoría:** La relación entre `Movimiento` y `Producto` utiliza `on_delete=models.SET_NULL`. Si un producto se eliminase de la base de datos, los movimientos no desaparecen; su campo `producto` pasa a nulo y el método `__str__` lo reporta como *"Producto eliminado"*.
2. **Baja Lógica:** En la capa de aplicación, la acción de borrar un producto no invoca `.delete()` sino que marca `activo = False`. Esto garantiza que los informes contables nunca pierdan registros históricos.
3. **Bloqueo de Concurrencia:** Durante las operaciones de movimiento, el producto se consulta mediante `select_for_update()` dentro de un bloque `transaction.atomic()`, garantizando que dos operadores no puedan alterar el stock simultáneamente provocando desfases.
