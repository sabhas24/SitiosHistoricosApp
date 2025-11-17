# PatrimoniosBA

Aplicación web para explorar y gestionar sitios históricos de Buenos Aires.

## Estructura del Proyecto

- `admin/` - Backend Flask con Poetry
- `web/` - Frontend Vue 3 con Vite
- `portal/` - Portal público
- `calculadora/` - Módulo de cálculo

## Configuración

### Backend (Flask)

1. Instalar Poetry:
```bash
pip install poetry
```

2. Instalar dependencias:
```bash
cd admin
poetry install
```

3. Configurar variables de entorno:
Editar `admin/src/web/config.py` con tus credenciales de base de datos:
```python
BD_USER = "tu_usuario"
BD_PASSWORD = "tu_contraseña"
BD_HOST = "localhost"
BD_PORT = "5432"
BD_NAME = "grupo44"
```

4. Ejecutar servidor:
```bash
poetry run python main.py
```

### Frontend (Vue)

1. Instalar dependencias:
```bash
cd web
npm install
```

2. Configurar variables de entorno:
Copiar `.env.example` a `.env` y configurar:
```bash
cp .env.example .env
```

Editar `.env` con tus credenciales de MinIO y URL de la API.

3. Ejecutar servidor de desarrollo:
```bash
npm run dev
```

### Base de Datos

Base de datos PostgreSQL llamada `grupo44`.

### MinIO (Almacenamiento de Imágenes)

Se utiliza MinIO como almacenamiento de objetos (compatible con S3).

- Endpoint: `192.168.1.43:9000`
- Bucket: `grupo44`
- Credenciales: Configurar en `.env`

## ⚠️ Archivos Sensibles (NO SUBIR A GIT)

- `web/.env` - Variables de entorno del frontend
- `admin/src/web/config.py` - Contiene credenciales de base de datos hardcodeadas
- `flask_session/` - Sesiones de Flask
- `[B` y `[B.pub` - Claves SSH
- Cualquier archivo con extensión `.env*` (excepto `.env.example`)

## Tecnologías

### Backend
- Flask
- PostgreSQL
- SQLAlchemy
- MinIO Python SDK
- JWT para autenticación

### Frontend
- Vue 3
- Vite
- Vue Router
- Axios
- Leaflet (mapas)

## Licencia

Proyecto Universitario - UNLP 2024

