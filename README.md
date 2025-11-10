# 🚀 NUAMX - Plataforma Operativa Django/API

**NUAMX** es una plataforma web construida con **Django** que utiliza **Django REST Framework (DRF)** para gestionar la **autenticación (JWT)** y el **control de usuarios y roles (RBAC)** a través de una API segura.  
El frontend es renderizado por Django y consume la API mediante JavaScript.

Manual de usuario : https://docs.google.com/document/d/1SDO6DM0cr3O3Fs2VhG7R0z4ISN7CIScp/edit?usp=sharing&ouid=106241663586320063931&rtpof=true&sd=true

---

## 📋 Requisitos del Sistema

- **Python:** 3.9 o superior  
- **Gestor de paquetes:** `pip`  
- **Control de versiones:** `git`

> 💡 **Recomendación:** usa siempre un **entorno virtual (`.venv`)** para evitar conflictos de dependencias entre proyectos.

---

## 🛠️ Guía de Instalación y Ejecución

Sigue las instrucciones específicas para tu sistema operativo.

---

### 🐧 Instalación en Linux (Kali, Ubuntu, Debian)

Ejecuta los siguientes comandos en la terminal:

#### 1️⃣ Preparar el entorno

```bash
# Instalar dependencias esenciales
sudo apt update
sudo apt install python3 python3-pip python3-venv git build-essential libaio1 python3-dev -y

git clone https://github.com/diegodiaz385/nuamx-django.git
cd nuamx-django

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver

🪟 Instalación en Windows (PowerShell)

# 1. Clonar el repositorio
git clone https://github.com/diegodiaz385/nuamx-django.git
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

