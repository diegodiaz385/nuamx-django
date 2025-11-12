# 🪟 NUAMX - Plataforma Operativa Django/API (Guía para Linux)
# Instalar dependencias básicas
sudo apt update
sudo apt install python3 python3-pip python3-venv git -y

# Clonar el repositorio
git clone https://github.com/usuario/nuamx-django.git
cd nuamx-django

# Crear entorno virtual
python3 -m venv .venv

# Activar entorno
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Migrar base de datos
python3 manage.py migrate

# Crear superusuario
python3 manage.py createsuperuser

# Ejecutar servidor
python3 manage.py runserver 0.0.0.0:8000


































# 🪟 NUAMX - Plataforma Operativa Django/API (Guía para Windows)

**NUAMX** es una plataforma web construida con **Django** que utiliza **Django REST Framework (DRF)** para gestionar la **autenticación (JWT)** y el **control de usuarios y roles (RBAC)** a través de una API segura.

El frontend es renderizado por Django y consume la API mediante JavaScript.

---

## 📋 Requisitos del Sistema

* **Windows 10 / 11**
* **Python:** versión 3.9 o superior
* **Git:** instalado y configurado
* **PIP:** gestor de paquetes de Python
* **Editor recomendado:** Visual Studio Code

> 💡 **Recomendación:** Usa siempre un **entorno virtual (`.venv`)** para evitar conflictos de dependencias entre proyectos.

---

## 🚀 Guía de Instalación

Sigue estos pasos en orden desde **PowerShell** o **Git Bash**.

### 1. Instalar Microsoft Visual C++ Build Tools

Algunos paquetes de Python (como `cx_Oracle`) requieren compiladores en C++. Descárgalo e instálalo desde el sitio oficial:

👉 [https://visualstudio.microsoft.com/visual-cpp-build-tools/](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

Durante la instalación:
* Marca **“Desktop development with C++”**
* Instala los componentes sugeridos
* Reinicia el sistema si es solicitado.

### 2. Clonar el Repositorio

Clona el proyecto y entra en su carpeta:

```powershell
git clone [https://github.com/diegodiaz385/nuamx-django.git](https://github.com/diegodiaz385/nuamx-django.git)
cd nuamx-django
````

### 3\. Crear y Activar el Entorno Virtual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

> ⚠️ **Nota de PowerShell:** Si la activación falla por políticas de ejecución, ejecuta este comando como Administrador (y solo si falla):
>
> ```powershell
> Set-ExecutionPolicy Unrestricted -Scope Process
> ```

### 4\. Instalar Dependencias

Actualiza `pip` e instala los paquetes del proyecto:

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### 5\. Configurar la Base de Datos

Aplica las migraciones y crea una cuenta de administrador:

```powershell
python manage.py migrate
python manage.py createsuperuser
```

### 6\. Ejecutar el Servidor

¡Listo\! Lanza el servidor de desarrollo:

```powershell
python manage.py runserver
```

```
