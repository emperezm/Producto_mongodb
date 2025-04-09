# Sistema de Gestión de Inventario

![Sistema de Gestión de Inventario](capturas/logo.svg)

## Tabla de Contenido

1. [Descripción](#descripción)
2. [Características](#características)
3. [Tecnologías](#tecnologías)
4. [Instalación](#instalación)
5. [Configuración](#configuración)
6. [Estructura del Proyecto](#estructura-del-proyecto)
7. [Diagramas](#diagramas)
8. [Capturas de Pantalla](#capturas-de-pantalla)
9. [Uso](#uso)
10. [Contribuciones](#contribuciones)

## Descripción

Este proyecto es un Sistema de Gestión de Inventario desarrollado con Python y Flask. Permite a los usuarios gestionar un catálogo de productos, llevar un control del stock, y realizar operaciones básicas de administración de inventario a través de una interfaz web intuitiva y moderna.

El sistema ofrece funcionalidades completas de CRUD (Crear, Leer, Actualizar y Eliminar) para productos, junto con un sistema de autenticación para proteger el acceso a la información. Utiliza MongoDB como base de datos para almacenar la información de manera eficiente y escalable.

## Características

- **Autenticación de Usuarios**: Sistema de registro e inicio de sesión seguro.
- **Dashboard Interactivo**: Panel principal con visualización clara del inventario.
- **Gestión de Productos**:
  - Añadir nuevos productos al inventario
  - Editar información de productos existentes
  - Eliminar productos del catálogo
  - Visualizar detalles completos de los productos
- **Control de Stock**: Seguimiento de cantidades disponibles con alertas visuales.
- **Interfaz Responsiva**: Diseño adaptable para diferentes dispositivos.
- **Búsqueda y Filtros**: Herramientas para encontrar productos rápidamente.
- **Seguridad**: Protección de rutas mediante middleware de autenticación.

## Tecnologías

- **Backend**:
  - Python 3.8+
  - Flask (Framework web)
  - PyMongo (Driver de MongoDB para Python)
  - Werkzeug (Utilidades de seguridad)

- **Frontend**:
  - HTML5, CSS3, JavaScript
  - Bootstrap 5.3 (Framework CSS)
  - Bootstrap Icons (Iconografía)
  
- **Base de Datos**:
  - MongoDB (Base de datos NoSQL)

- **Herramientas de Desarrollo**:
  - Visual Studio Code
  - Git (Control de versiones)

## Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/emperezm/Producto_mongodb
   cd Producto_mongodb
   ```

2. **Crear y activar entorno virtual**:
   ```bash
   # En Windows
   python -m venv venv
   venv\Scripts\activate
   
   # En macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Instalar MongoDB**:
   - Descargar e instalar [MongoDB Community Server](https://www.mongodb.com/try/download/community)
   - Alternativamente, usar MongoDB Atlas para una base de datos en la nube

## Configuración

1. **Configurar la conexión a MongoDB**:

   Asegúrate de que el archivo `database.py` esté correctamente configurado:

   ```python
   from pymongo import MongoClient

   def dbConnection():
       try:
           client = MongoClient('mongodb://localhost:27017/')
           db = client['dbb_producto']
           return db
       except Exception as e:
           print(f"Error de conexión a MongoDB: {e}")
           return None
   ```

   Si utilizas MongoDB Atlas u otra configuración, ajusta la URL de conexión según corresponda.

2. **Configurar variables de entorno** (opcional):

   Crea un archivo `.env` en la raíz del proyecto:

   ```
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=ProyectoSENA25Abril
   ```

## Estructura del Proyecto

```
sistema-inventario/
│
├── app.py                  # Punto de entrada principal
├── database.py             # Configuración de conexión a la base de datos
├── product.py              # Modelo de producto
├── requirements.txt        # Dependencias del proyecto
│
│
├── templates/              # Plantillas HTML
│   ├── index.html          # Dashboard principal
│   ├── login.html          # Página de inicio de sesión
│   └── register.html       # Página de registro
│
└── README.md               # Documentación del proyecto
```
## Diagramas
![Diagrama de Casos de Uso](capturas/casos-uso.jpeg)

*Diagrama de casos de uso.*

![Diagrama de Clases](capturas/clases.jpeg)

*Diagrama de clases.*


## Capturas de Pantalla

### Inicio de Sesión
![Pantalla de Inicio de Sesión](capturas/login.png)

*Pantalla de autenticación para acceder al sistema.*

### Dashboard de Inventario
![Dashboard Principal](capturas/inventario.png)

*Panel principal con listado de productos, indicadores de stock y opciones de gestión.*

### Formulario de Producto
![Formulario de Producto](capturas/agregar-producto.png)

*Interfaz para agregar o modificar información de productos en el inventario.*

## Uso

1. **Iniciar el servidor**:
   ```bash
   python app.py
   ```

2. **Acceder a la aplicación**:
   - Abre tu navegador y visita: `http://localhost:4200`
   - Regístrate para crear una nueva cuenta
   - Inicia sesión para acceder al dashboard

3. **Gestión de Productos**:
   - **Añadir**: Navega a la pestaña "Nuevo Producto" y completa el formulario
   - **Editar**: Haz clic en el botón "Editar" junto a un producto para modificar sus detalles
   - **Eliminar**: Haz clic en "Eliminar" para quitar un producto del inventario
   - **Visualizar**: Todos los productos se muestran en la página principal con su información relevante

4. **Búsqueda de Productos**:
   - Utiliza el campo de búsqueda para filtrar productos por nombre o descripción
   - Cambia entre vista de cuadrícula o lista según tus preferencias

## Contribuciones

Las contribuciones son bienvenidas. Si deseas mejorar este proyecto, sigue estos pasos:

1. Haz un Fork del repositorio 
2. Crea una nueva rama (`git checkout -b feature/nueva-caracteristica`)
3. Realiza tus cambios y haz commit (`git commit -m 'Añadir nueva característica'`)
4. Sube tus cambios (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request
6. También me puedes contactar vía correo electrónico al E-mail: mari-perez36@hotmai.com

---

Desarrollado como proyecto de Mariana Pérez Montalvo para el curso Github del SENA © 2025
