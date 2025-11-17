# ANTES DE SUBIR A GIT - CHECKLIST DE SEGURIDAD

## ⚠️ ARCHIVOS QUE **NO** DEBES SUBIR (ya están en .gitignore)

### Credenciales y Variables de Entorno
- ❌ `web/.env` - Contiene credenciales de MinIO
- ❌ Cualquier archivo `.env` excepto `.env.example`

### Claves SSH
- ❌ `admin/[B` - Clave privada SSH
- ❌ `admin/[B.pub` - Clave pública SSH
- ❌ Cualquier archivo `*.pem`, `id_rsa`, `id_ed25519`

### Sesiones y Datos Temporales
- ❌ `admin/flask_session/` - Contiene sesiones que pueden tener datos sensibles
- ❌ `node_modules/` - Dependencias (muy pesado)
- ❌ `__pycache__/` - Cache de Python

### Archivos del Sistema
- ❌ `.vscode/` - Configuración personal de VS Code
- ❌ `.DS_Store` - Archivos de macOS
- ❌ `Thumbs.db` - Archivos de Windows

## ⚠️ PROBLEMA ACTUAL: Credenciales Hardcodeadas

El archivo `admin/src/web/config.py` contiene credenciales hardcodeadas:

```python
BD_USER = "postgres"
BD_PASSWORD = "nico+1234"  # ⚠️ EXPUESTO
MINIO_ACCESS_KEY = "minioadmin"  # ⚠️ EXPUESTO
MINIO_SECRET_KEY = "minioadmin"  # ⚠️ EXPUESTO
```

### Solución Recomendada

1. **Crear archivo `.env` en admin/**:
```bash
cd admin
touch .env
```

2. **Mover credenciales al .env**:
```
BD_USER=postgres
BD_PASSWORD=nico+1234
BD_HOST=localhost
BD_PORT=5432
BD_NAME=grupo44

MINIO_ENDPOINT=192.168.1.43:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET_NAME=grupo44

JWT_SECRET_KEY=un-secreto-muy-seguro-aqui
```

3. **Modificar config.py** para leer de variables de entorno:
```python
from os import environ
from dotenv import load_dotenv

load_dotenv()

class DevelopmentConfig(Config):
    BD_USER = environ.get("BD_USER", "postgres")
    BD_PASSWORD = environ.get("BD_PASSWORD")  # Sin default!
    BD_HOST = environ.get("BD_HOST", "localhost")
    # etc...
```

4. **Instalar python-dotenv**:
```bash
poetry add python-dotenv
```

## ✅ ARCHIVOS QUE **SÍ** DEBES SUBIR

### Código Fuente
- ✅ `admin/src/**/*.py` - Código Python
- ✅ `web/src/**/*.vue` - Componentes Vue
- ✅ `web/src/**/*.js` - JavaScript
- ✅ `static/**/*` - Archivos estáticos (CSS, imágenes)

### Configuración del Proyecto
- ✅ `admin/pyproject.toml` - Dependencias Python
- ✅ `admin/poetry.lock` - Lock file de Poetry
- ✅ `web/package.json` - Dependencias Node
- ✅ `web/package-lock.json` - Lock file de npm
- ✅ `web/vite.config.js` - Configuración de Vite
- ✅ `.gitignore` - Archivo de ignores

### Documentación
- ✅ `README.md` - Documentación principal
- ✅ `web/.env.example` - Ejemplo de variables de entorno
- ✅ Este archivo (`SECURITY.md`)

### Ejemplos y Plantillas
- ✅ Crear `admin/.env.example` con valores de ejemplo (sin credenciales reales)

## 🔍 VERIFICAR ANTES DE COMMIT

Ejecuta estos comandos para verificar qué se va a subir:

```bash
# Ver archivos que se van a subir
git status

# Ver diferencias
git diff

# Ver archivos ignorados
git status --ignored

# Verificar que archivos sensibles NO están staged
git ls-files | grep -E "\.env$|flask_session|\.pub$|\[B"
```

## 🚀 COMANDOS SEGUROS PARA SUBIR

```bash
# 1. Agregar todos los archivos (el .gitignore filtrará los sensibles)
git add .

# 2. Verificar qué se va a subir
git status

# 3. Si todo está bien, hacer commit
git commit -m "feat: implementación de catálogo de sitios históricos"

# 4. Subir al repositorio
git push origin main
```

## 📝 NOTA IMPORTANTE

Si ya subiste archivos con credenciales anteriormente:
1. Cambiar TODAS las contraseñas expuestas inmediatamente
2. Rotar claves de API (MinIO, JWT, etc.)
3. Considerar limpiar el historial de git (complejo, consultar documentación)

## 🆘 EN CASO DE EMERGENCIA

Si accidentalmente subiste credenciales:
1. ❗ **Inmediatamente** cambiar todas las contraseñas
2. Rotar claves SSH y API keys
3. Contactar al administrador de sistemas
4. Usar `git-filter-repo` o BFG Repo-Cleaner para limpiar historial

## 📞 Contacto

Si tienes dudas sobre qué subir, consulta con tu equipo antes de hacer push.
