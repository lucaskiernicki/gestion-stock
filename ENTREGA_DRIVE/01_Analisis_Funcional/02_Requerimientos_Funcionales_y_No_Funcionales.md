# DOCUMENTO DE ANÁLISIS FUNCIONAL — REQUERIMIENTOS DEL SISTEMA
## Sistema de Gestión de Stock e Inventario
**Título:** Especificación de Requerimientos Funcionales y No Funcionales  
**Versión:** 1.0 (Ciclo 2026)  
**Institución:** ISFDyT N° 210 — La Plata  

---

### 1. INFORMACIÓN GENERAL

| Campo | Valor |
| :--- | :--- |
| **Cliente / Ámbito** | Comercio Minorista / Depósito de Mercadería |
| **Analista / Desarrollador** | Lucas Ignacio Kiernicki |
| **Carrera** | Tecnicatura Superior en Análisis de Sistemas (3° Año) |
| **Proyecto** | Sistema de Gestión de Stock e Inventario |
| **Tipo de Documento** | Especificación de Requerimientos de Software (SRS) |

---

### 2. REQUERIMIENTOS FUNCIONALES (RF)

* **RF01 - Alta de Productos:**
  El sistema debe permitir registrar un nuevo artículo especificando: Nombre, Categoría, Precio unitario y Stock inicial. Si el stock inicial es mayor a cero, el sistema debe registrar automáticamente un movimiento contable de tipo 'Alta Inicial'.

* **RF02 - Modificación de Productos:**
  El sistema debe permitir actualizar los datos de un artículo existente (nombre, categoría y precio). En caso de modificarse el número de stock en esta pantalla, el sistema debe calcular la diferencia y registrar automáticamente un movimiento de tipo 'Ajuste'.

* **RF03 - Baja Lógica de Productos:**
  El sistema debe permitir dar de baja un artículo. Dicha baja debe ser lógica (`activo = False`) para impedir que se eliminen en cascada los registros de movimientos históricos asociados.

* **RF04 - Visualización y Alertas de Stock:**
  El sistema debe listar los productos activos en el Dashboard clasificando su stock mediante indicadores visuales de color:
  * **Sin Stock:** 0 unidades (Rojo).
  * **Stock Bajo:** entre 1 y 2 unidades (Amarillo / Naranja).
  * **Normal:** 3 o más unidades (Verde / Turquesa).

* **RF05 - Administración de Categorías:**
  El sistema debe permitir crear, editar y eliminar categorías de artículos, calculando dinámicamente cuántos productos activos pertenecen a cada rubro.

* **RF06 - Registro de Entradas de Stock:**
  El sistema debe permitir registrar ingresos de mercadería (reposición de compras). La operación debe sumar la cantidad indicada al stock actual del producto de forma atómica y solicitar un motivo explicativo.

* **RF07 - Registro de Salidas de Stock:**
  El sistema debe permitir registrar egresos de mercadería (ventas o consumo interno), descontando la cantidad indicada del stock físico disponible.

* **RF08 - Control y Prevención de Stock Negativo:**
  El sistema debe validar en el backend que toda salida de mercadería cuente con saldo suficiente (`cantidad <= producto.stock`). En caso de saldo insuficiente, debe abortar la operación y emitir un mensaje de error detallando el stock real disponible.

* **RF09 - Auditoría e Historial de Movimientos:**
  El sistema debe presentar una tabla cronológica inmutable con todos los movimientos registrados, detallando: Fecha y hora exacta, Nombre del producto, Tipo de movimiento (Entrada, Salida, Alta, Ajuste), Cantidad operada y Motivo.

* **RF10 - Panel de Control (Dashboard Métrico):**
  El sistema debe calcular y mostrar al inicio el total de productos activos, el total de artículos en estado de stock bajo y los movimientos ejecutados durante la fecha actual.

---

### 3. REQUERIMIENTOS NO FUNCIONALES (RNF)

* **RNF01 - Integridad Transaccional (ACID):**
  Toda modificación de inventario debe realizarse bajo transacciones atómicas (`transaction.atomic`) y bloqueo de fila (`select_for_update`) para asegurar consistencia ante operaciones concurrentes.

* **RNF02 - Seguridad y Autenticación:**
  Utilización del framework de seguridad de Django, protección CSRF en todos los formularios de captura y acceso protegido con contraseñas encriptadas en el panel administrativo.

* **RNF03 - Rendimiento y Tiempos de Respuesta:**
  El tiempo de carga de las vistas de inventario y listado de movimientos no debe superar los 2 segundos bajo condiciones normales de red local.

* **RNF04 - Usabilidad y Ergonomía Visual:**
  Diseño responsive adaptado a pantallas de escritorio y dispositivos móviles con soporte para Modo Oscuro que almacena la preferencia del usuario en el almacenamiento local del navegador (`localStorage`).

* **RNF05 - Portabilidad y Despliegue:**
  El sistema debe ejecutarse de forma homogénea en Windows, Linux y macOS mediante un entorno virtual de Python (`venv`), sin requerir configuraciones complejas de dependencias externas.
