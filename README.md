# Sistema de Gestión de Stock - ISFDyT N° 210

## Descripción del Proyecto
Este sistema es un desarrollo web realizado para el **Trabajo Práctico Integrador de Consolidación de Temas (2026)** de la carrera **Tecnicatura Superior en Análisis de Sistemas** (3° Año).

El objetivo principal es resolver la problemática de control de inventario de un comercio o depósito, permitiendo administrar productos y categorías, y registrar movimientos de stock de entrada y salida con control de consistencia y trazabilidad.

---

## Espacios Curriculares Integrados
* **Prácticas Profesionalizantes III** - Prof. Karina M. Alvarez
* **Seminario de Actualización e Ingeniería de Software II** - Prof. Marcos Di Lauro
* **Algoritmos y Estructura de Datos III** - Prof. Nicolás Wilches

---

## Tecnologías Utilizadas
* **Lenguaje:** Python 3.10+
* **Framework Web:** Django 5.2+
* **Base de Datos:** SQLite3
* **Frontend:** HTML5, CSS3 personalizado, JavaScript nativo, Bootstrap 5
* **Control de Versiones:** Git y GitHub

---

## Funcionalidades Principales
* **Dashboard Principal:** Métricas en tiempo real (total de productos, alertas por stock bajo, movimientos diarios y tabla de últimas operaciones).
* **Gestión de Productos:** Alta con stock inicial, edición de características y baja lógica para resguardar la trazabilidad contable.
* **Gestión de Categorías:** Clasificación y organización del catálogo con conteo dinámico de artículos.
* **Registro de Movimientos:** Control de Entradas (reposición/compras) y Salidas (ventas/consumo) con validación estricta para evitar stock negativo.
* **Modo Claro / Modo Oscuro:** Interfaz con selector de tema persistente en el navegador.
* **Panel de Administración:** Configuración avanzada de modelos en Django Admin.

---

## Requisitos Previos

Antes de comenzar, asegurarse de tener instalado en el sistema:
1. **Python 3.10 o superior** (marcar la casilla "Add Python to PATH" durante la instalación en Windows).
2. **Git** para clonar el repositorio.

---

## Instrucciones de Instalación y Ejecución

Es posible instalar el proyecto de dos formas: **automática (recomendada)** o **manual**.

---

### Opción A: Instalación Rápida Automática (Windows)

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/lucaskiernicki/gestion-stock.git
   cd gestion-stock
   ```
2. Hacer doble clic en el archivo **`instalar.bat`** (o ejecutarlo desde la consola):
   ```cmd
   instalar.bat
   ```
   *Este script se encargará automáticamente de crear el entorno virtual, instalar las librerías necesarias y configurar la base de datos.*
3. Una vez finalizado, hacer doble clic en **`iniciar.bat`** o ejecutar:
   ```cmd
   iniciar.bat
   ```
   *Se abrirá automáticamente el navegador en `http://127.0.0.1:8000/`.*

---

### Opción B: Instalación Manual Paso a Paso

Si se prefiere realizar la configuración manual en la consola (Windows, Linux o macOS), seguir estos pasos:

#### 1. Clonar el repositorio
```bash
git clone https://github.com/lucaskiernicki/gestion-stock.git
cd gestion-stock
```

#### 2. Crear el entorno virtual
En la raíz del proyecto, crear un entorno virtual aislado:
```bash
# Windows / Linux / macOS
python -m venv env
```

#### 3. Activar el entorno virtual
* **En Windows (PowerShell):**
  ```powershell
  .\env\Scripts\Activate.ps1
  ```
  *(Si PowerShell bloquea la ejecución de scripts, ejecutar primero: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*

* **En Windows (CMD / Símbolo del Sistema):**
  ```cmd
  env\Scripts\activate.bat
  ```

* **En Linux o macOS:**
  ```bash
  source env/bin/activate
  ```

#### 4. Instalar las dependencias
Con el entorno virtual activado, instalar los paquetes requeridos:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 5. Aplicar las migraciones de la base de datos
Configurar las tablas del sistema ejecutando:
```bash
python manage.py migrate
```

#### 6. (Opcional) Crear usuario Administrador
Para acceder al panel de administración nativo de Django (`/admin/`), crear un superusuario:
```bash
python manage.py createsuperuser
```
*(Ingresar nombre de usuario, correo y contraseña).*

#### 7. Iniciar el servidor de desarrollo
Levantar el servidor local:
```bash
python manage.py runserver
```

Abrir el navegador web e ingresar a:
**`http://127.0.0.1:8000/`**

---

## Rutas y Navegación del Sistema

| Ruta | Descripción |
| :--- | :--- |
| `/` | **Dashboard:** Resumen métrico, inventario activo y últimos movimientos |
| `/crear_producto/` | **Nuevo Producto:** Formulario de alta con stock inicial |
| `/editar_producto/<id>/` | **Editar Producto:** Modificación de datos y ajuste manual |
| `/movimientos/` | **Movimientos:** Formulario de entrada/salida e historial completo |
| `/categorias/` | **Categorías:** Listado y conteo de artículos por rubro |
| `/admin/` | **Panel Django:** Administración avanzada (requiere superusuario) |

---

## Estructura del Proyecto

```text
gestion-stock/
│
├── config/                  # Configuración principal del proyecto Django
│   ├── settings.py          # Ajustes generales (apps, base de datos, estáticos)
│   ├── urls.py              # Enrutador principal de URLs
│   └── wsgi.py
│
├── inventario/              # Aplicación principal del sistema
│   ├── migrations/          # Historial de migraciones de la base de datos
│   ├── static/              # Archivos estáticos
│   │   ├── css/styles.css   # Hojas de estilo y diseño visual
│   │   └── js/script.js     # Lógica interactiva (popups, modo oscuro, etc.)
│   ├── templates/           # Vistas HTML
│   │   └── inventario/
│   │       ├── base.html
│   │       ├── dashboard.html
│   │       ├── crear_producto.html
│   │       ├── categorias.html
│   │       ├── formulario_categoria.html
│   │       └── movimientos.html
│   ├── admin.py             # Configuración del panel de administración Django
│   ├── models.py            # Modelos de datos (Producto, Categoria, Movimiento)
│   └── views.py             # Lógica de controladores y reglas de stock
│
├── .gitignore               # Archivos excluidos de Git
├── db.sqlite3               # Base de datos relacional local
├── iniciar.bat              # Script para iniciar el servidor
├── instalar.bat             # Script de instalación automática
├── manage.py                # Gestor de comandos de Django
├── README.md                # Documentación del proyecto
└── requirements.txt         # Lista de dependencias de Python
```

---

## Autor
* **Lucas Kiernicki**
* Carrera: **Tecnicatura Superior en Análisis de Sistemas** (3° Año)
* Institución: **ISFDyT N° 210** (2026)