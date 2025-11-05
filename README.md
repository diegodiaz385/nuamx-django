# 🚀 NUAMX - Plataforma Operativa Django/API

Este proyecto es una plataforma web construida con Django que utiliza Django REST Framework (DRF) para gestionar la autenticación (JWT) y el control de usuarios/roles (RBAC) a través de una API. El frontend es renderizado por Django y consume la API vía JavaScript.

## 📋 Requisitos del Sistema

* **Python:** Versión 3.9 o superior.
* **Gestor de paquetes:** `pip`
* **Sistema de control:** `git`

---

## 🛠 Guía de Instalación y Ejecución

Sigue las instrucciones específicas para tu sistema operativo. **Recomendamos usar un Entorno Virtual (`.venv`) siempre.**

### 🐧 1. Instalación en Linux (Kali, Ubuntu, Debian)

Ejecuta los siguientes comandos en la terminal.

#### a) Preparar el Entorno

```bash
# 1. Instalar dependencias esenciales
sudo apt update
sudo apt install python3 python3-pip python3-venv git -y

# 2. Clonar el repositorio
git clone [https://github.com/diegodiaz385/nuamx-django](https://github.com/diegodiaz385/nuamx-django)
cd nuamx-django

# 3. Crear y activar el entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# 4. Instalar dependencias del proyecto
pip install -r requirements.txt

# 5. Aplicar migraciones (crea la base de datos)
python manage.py migrate

# 6. Crear un usuario administrador (requerido para acceder al panel de roles)
python manage.py createsuperuser

# 7. Iniciar el servidor de desarrollo
python manage.py runserver 0.0.0.0:8000







Instalación en Windows (PowerShell)

# 1. Clonar el repositorio
git clone [https://github.com/diegodiaz385/nuamx-django](https://github.com/diegodiaz385/nuamx-django)
cd nuamx-django

# 2. Crear el entorno virtual
python -m venv .venv

# 3. Activar el entorno virtual
.\.venv\Scripts\Activate.ps1

# 4. Instalar dependencias del proyecto
pip install -r requirements.txt

# 5. Aplicar migraciones (crea la base de datos)
python manage.py migrate

# 6. Crear un usuario administrador
python manage.py createsuperuser

# 7. Iniciar el servidor de desarrollo
python manage.py runserver
