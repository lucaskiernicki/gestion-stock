# Documento de Análisis Funcional y Técnico: Sistema de Gestión de Stock
## Versión 5.0 (Definitiva y Homologada)

---

### Datos Académicos
* **Estudiante:** KIERNICKI, Lucas Ignacio
* **Institución:** ISFDyT N° 210 (La Plata, Buenos Aires)
* **Carrera:** Tecnicatura Superior en Análisis de Sistemas — 3° Año
* **Ciclo Lectivo:** 2026

#### Espacios Curriculares Integrados
1. **Prácticas Profesionalizantes III** — Prof. Karina M. Alvarez
2. **Seminario de Actualización e Ingeniería de Software II** — Prof. Marcos Di Lauro
3. **Algoritmos y Estructura de Datos III** — Prof. Nicolás Wilches

---

## 1. Descripción de la Problemática
Actualmente, la administración de inventarios de productos en comercios y depósitos de forma manual o a través de herramientas descentralizadas (como hojas de cálculo desconectadas) introduce graves problemas operativos:
* Discrepancias constantes entre las existencias físicas en góndola o depósito y los registros asentados.
* Pérdida total de trazabilidad histórica sobre quién, cuándo y por qué motivo se modificó una cantidad.
* **Inconsistencias críticas operativas:** generación de salidas de mercadería que superan la existencia física real (quiebres de stock o stock negativo).
* Carencia de mecanismos transaccionales que garanticen la integridad de los datos ante concurrencia de operadores.

Para subsanar de forma definitiva estas falencias, se diseñó e implementó un sistema web centralizado, seguro y escalable, estructurado sobre una base de datos relacional y construido con el framework **Django** bajo la arquitectura **MTV (Modelo-Template-Vista)**, que aplica validaciones lógicas rigurosas y transacciones atómicas antes de confirmar cualquier movimiento de mercadería.

---

## 2. Objetivo del Sistema
Desarrollar un sistema web funcional y robusto de gestión de inventario que permita:
1. Administrar de manera integral el catálogo de productos y categorías.
2. Registrar movimientos de entrada y salida con control estricto de existencias, impidiendo el registro de stock negativo.
3. Asegurar la trazabilidad histórica mediante bajas lógicas y auditoría de motivos por comprobante.
4. Proveer un panel de métricas operativas en tiempo real (Dashboard) con alertas preventivas de bajo stock.
5. Ofrecer una experiencia de usuario clara, accesible y ergonómica mediante soporte nativo de Modo Claro y Modo Oscuro.

---

## 3. Alcance del Sistema
El sistema cubre los siguientes módulos operativos:

* **Módulo de Gestión de Categorías:** Alta, baja, modificación y listado de rubros, con descripción y conteo dinámico de artículos activos asociados.
* **Módulo de Gestión de Productos:** Catálogo completo con categorización obligatoria, precio, stock inicial y control de estado (activo/inactivo).
* **Módulo de Registro de Movimientos:** Control cronológico inmutable de Entradas (reposición/compras), Salidas (ventas/consumo), Altas iniciales y Ajustes manuales por auditoría.
* **Módulo de Validación Crítica y Transacciones Atómicas:** Bloqueo sistemático de egresos que superen el stock disponible, con ejecución dentro de transacciones atómicas (`transaction.atomic`) y bloqueo de fila (`select_for_update`).
* **Módulo de Dashboard y KPIs:** Panel principal con indicadores en tiempo real (total de artículos, alertas por stock <= 2 unidades, movimientos diarios y tabla de últimas operaciones).
* **Módulo de Administración Django:** Panel administrativo protegido para tareas de supervisión técnica de los modelos.

---

## 4. Requerimientos Funcionales (RF)

| Código | Requerimiento | Descripción Detallada |
| :--- | :--- | :--- |
| **RF1** | **ABM de Categorías** | El sistema debe permitir el alta, baja, modificación y listado de clasificaciones, almacenando nombre y descripción. |
| **RF2** | **ABM de Productos** | El sistema debe permitir el alta, baja lógica, edición y listado de productos, vinculados obligatoriamente a una categoría, con precio y stock. |
| **RF3** | **Registro de Entrada** | El sistema debe permitir asentar ingresos de mercadería, incrementando el stock de forma inmediata y registrando comprobante/motivo. |
| **RF4** | **Registro de Salida** | El sistema debe permitir asentar egresos de mercadería, descontando del inventario disponible la cantidad solicitada. |
| **RF5** | **Validación Crítica de Stock (No Negativo)** | El sistema debe validar que la cantidad de una salida sea menor o igual al stock actual. Ante una cantidad mayor, la operación se cancela, no se modifica la base de datos y se notifica el error. |
| **RF6** | **Visualización y Alertas de Stock** | El sistema debe calcular y mostrar el stock remanente en tiempo real, destacando con alertas visuales aquellos productos con stock crítico (<= 2 unidades). |
| **RF7** | **Baja Lógica y Trazabilidad** | La eliminación de un producto no debe borrar el registro de la base de datos física, sino alternar su estado (`activo = False`), resguardando el historial contable de movimientos. |
| **RF8** | **Auditoría y Justificación de Movimientos** | Cada movimiento debe registrar obligatoriamente fecha/hora y un campo de motivo para indicar número de remito, factura o causa del ajuste. |
| **RF9** | **Generación Automática de Movimientos** | Al crear un producto con stock inicial, el sistema debe generar automáticamente un movimiento de tipo `ALTA`. Al modificar el stock desde la edición, debe asentar un movimiento de tipo `AJUSTE` con el delta. |

---

## 5. Requerimientos No Funcionales (RNF)

* **RNF1 - Usabilidad y Diseño Responsive:** Interfaz intuitiva, ordenada y compatible con dispositivos de escritorio y móviles mediante HTML5, CSS3 nativo y componentes Bootstrap 5.
* **RNF2 - Convención Académica e Idioma:** Totalidad del sistema, etiquetas, controladores, mensajes de error y documentación técnica redactados en idioma español formal, sin uso de emoticonos ni caracteres ASCII informales (conforme pauta de rúbrica).
* **RNF3 - Persistencia de Datos Relacional:** Almacenamiento en motor relacional SQLite debidamente normalizado a través del ORM nativo de Django.
* **RNF4 - Integridad Transaccional y Concurrencia (ACID):** Todas las operaciones que alteran inventario se ejecutan dentro de bloques atómicos con bloqueo a nivel de fila (`select_for_update`), previniendo inconsistencias por peticiones simultáneas.
* **RNF5 - Ergonomía Visual y Persistencia de Tema:** Selector de Modo Claro y Modo Oscuro con contraste visual optimizado, persistiendo la selección del usuario mediante `localStorage`.

---

## 6. Casos de Uso Principales (CU)

### Caso de Uso 1: Registrar Entrada de Mercadería
* **Actor:** Operario / Administrador.
* **Precondición:** El producto debe estar previamente registrado y activo en el sistema.
* **Flujo Principal:**
  1. El usuario accede al módulo de Movimientos.
  2. Selecciona el producto destino e ingresa la cantidad a incorporar (entero > 0).
  3. Selecciona el tipo de movimiento como `Entrada (Reposición)` e ingresa el motivo o comprobante de compra.
  4. Presiona el botón de confirmación.
  5. El sistema incrementa el stock de forma atómica, registra el movimiento en el historial y muestra un mensaje de éxito.

### Caso de Uso 2: Registrar Salida de Mercadería con Validación Crítica
* **Actor:** Operario / Administrador.
* **Precondición:** El producto debe estar previamente registrado y activo en el sistema.
* **Flujo Principal:**
  1. El usuario accede al módulo de Movimientos.
  2. Selecciona el producto, define el tipo como `Salida (Consumo / Venta)`, introduce la cantidad a egresar y el motivo.
  3. El sistema evalúa en la base de datos si la cantidad solicitada es menor o igual al stock actual del producto.
  4. Al confirmarse stock suficiente, el sistema descuenta la cantidad, guarda el movimiento histórico y emite confirmación de éxito.
* **Flujo Alternativo 2A (Stock Insuficiente - Validación de Consistencia):**
  * Si en el paso 3 la cantidad solicitada supera el stock disponible:
    * El sistema interrumpe inmediatamente la transacción.
    * No se modifica el valor de stock en la tabla `Producto`.
    * No se almacena ningún registro en la tabla `Movimiento`.
    * Se redirige al formulario emitiendo un mensaje de alerta: `Stock insuficiente para [Producto]. Stock disponible: X unidades`.

### Caso de Uso 3: Baja Lógica de Producto con Preservación Histórica
* **Actor:** Administrador.
* **Precondición:** El producto existe en la base de datos (puede poseer movimientos históricos asociados).
* **Flujo Principal:**
  1. El usuario solicita la eliminación de un artículo desde el listado del Dashboard.
  2. El sistema actualiza el campo `activo = False` del producto.
  3. El producto se oculta de la vista operativa y de los selectores de nuevos movimientos.
  4. Todos los movimientos históricos previos vinculados al producto permanecen inalterados en la base de datos para fines de auditoría.

### Caso de Uso 4: Ajuste Manual de Inventario por Recuento Físico
* **Actor:** Administrador / Auditor.
* **Precondición:** El producto se encuentra activo.
* **Flujo Principal:**
  1. El usuario ingresa a la edición del producto y rectifica el número de existencias físicas.
  2. El sistema calcula la diferencia respecto del stock previo.
  3. Dentro de una transacción atómica, actualiza el stock y genera automáticamente un registro de tipo `AJUSTE` indicando el delta (+/- unidades).
  4. Se muestra un mensaje de confirmación y el cambio queda registrado en el historial cronológico.

---

## 7. Arquitectura de la Base de Datos

### Modelo Entidad-Relación y Diccionario de Datos

#### Tabla: `inventario_categoria`
| Tipo Clave | Nombre del Campo | Tipo de Dato | Restricción / Descripción |
| :--- | :--- | :--- | :--- |
| **PK** | `id` | `Integer` | Autoincremental |
| | `nombre` | `Varchar(100)` | Obligatorio |
| | `descripcion` | `Varchar(255)` | Opcional (Permite valor nulo/blanco) |

#### Tabla: `inventario_producto`
| Tipo Clave | Nombre del Campo | Tipo de Dato | Restricción / Descripción |
| :--- | :--- | :--- | :--- |
| **PK** | `id` | `Integer` | Autoincremental |
| | `nombre` | `Varchar(150)` | Obligatorio |
| **FK** | `categoria_id` | `Integer` | Clave Foránea a `inventario_categoria` (ON DELETE CASCADE) |
| | `stock` | `Integer` | Obligatorio (Default: 0, No negativo) |
| | `precio` | `Decimal(10, 2)` | Obligatorio (Dos decimales para importe monetario) |
| | `activo` | `Boolean` | Obligatorio (Default: True, Control de baja lógica) |

#### Tabla: `inventario_movimiento`
| Tipo Clave | Nombre del Campo | Tipo de Dato | Restricción / Descripción |
| :--- | :--- | :--- | :--- |
| **PK** | `id` | `Integer` | Autoincremental |
| **FK** | `producto_id` | `Integer` | Clave Foránea a `inventario_producto` (ON DELETE SET_NULL) |
| | `tipo` | `Varchar(10)` | Opciones: `ENTRADA`, `SALIDA`, `ALTA`, `AJUSTE` |
| | `cantidad` | `Integer` | Obligatorio (Positivo, mayor a cero) |
| | `motivo` | `Varchar(200)` | Opcional (Comprobante / Justificación) |
| | `fecha` | `DateTime` | Autogenerado (`auto_now_add = True`) |

---

## 8. Arquitectura de Interfaz de Usuario y Vistas

1. **Pantalla 1: Dashboard (Panel Principal):** Métricas consolidadas (total de artículos, alertas por existencia crítica <= 2 unidades, movimientos de la jornada, tabla interactiva de inventario y tabla de transacciones recientes).
2. **Pantalla 2: Gestión de Productos (Catálogo y ABM):** Formulario de alta y edición con campos de nombre, categoría obligatoria, precio y stock. Acciones de edición y baja lógica protegida.
3. **Pantalla 3: Gestión de Categorías:** Panel de administración de clasificaciones con conteo dinámico de productos asociados y formulario de alta/edición.
4. **Pantalla 4: Historial de Movimientos:** Formulario de registro con validaciones de existencias y tabla cronológica de auditoría con distintivos por tipo de operación.
5. **Pantalla 5: Panel de Administración Django:** Interfaz de superusuario para auditoría directa sobre los modelos.

---

## 9. Matriz de Trazabilidad y Casos de Prueba (QA)

| ID Caso | RF Vinculado | Descripción de la Prueba | Método Automatizado (`inventario/tests.py`) | Estado |
| :--- | :--- | :--- | :--- | :--- |
| **CP01** | RF6, RNF1 | Carga de Dashboard con métricas y respuesta HTTP 200 | `test_dashboard_status_code_y_contexto` | **APROBADO** |
| **CP02** | RF1 | Alta y persistencia de categorías con descripción | `test_crear_categoria` | **APROBADO** |
| **CP03** | RF2, RF9 | Alta de producto y generación automática de movimiento `ALTA` | `test_crear_producto_con_stock_inicial` | **APROBADO** |
| **CP04** | RF2, RF9 | Edición de producto y generación automática de movimiento `AJUSTE` | `test_editar_producto_ajuste_stock` | **APROBADO** |
| **CP05** | RF7 | Baja lógica de producto preservando historial de movimientos | `test_eliminar_producto_baja_logica` | **APROBADO** |
| **CP06** | RF3, RF8 | Registro de Entrada de stock con motivo y comprobante | `test_movimiento_entrada_valida` | **APROBADO** |
| **CP07** | RF4, RF8 | Registro de Salida de stock con existencia suficiente | `test_movimiento_salida_valida` | **APROBADO** |
| **CP08** | RF5, RNF4 | Bloqueo absoluto de Salida cuando la cantidad supera el stock | `test_bloqueo_salida_stock_insuficiente` | **APROBADO** |
| **CP09** | RNF4 | Validación y rechazo de cantidades negativas o cero | `test_bloqueo_cantidad_invalida` | **APROBADO** |
| **CP10** | RF1, RF6 | Listado de categorías con conteo dinámico de productos | `test_listar_categorias_con_conteo` | **APROBADO** |

> **Resultado de la Validación Automatizada:**
> * Total de pruebas ejecutadas: **14**
> * Pruebas aprobadas: **14 (100% OK)**
> * Fallos / Errores: **0**
> * Tiempo de ejecución: **0.095s**
