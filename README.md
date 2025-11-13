# 📦 NUAMX — Guía de Instalación y Ejecución 

## 📋 Requisitos del Sistema

- **Python:** 3.9 o superior  
- **Gestor de paquetes:** `pip`  
- **Control de versiones:** `git`

> 💡 **Recomendación:** usa siempre un **entorno virtual (`.venv`)** para evitar conflictos de dependencias entre proyectos.  
> 🧠 En desarrollo se usa **SQLite** (no necesitas Oracle). Si `cx_Oracle`/`oracledb` están en `requirements.txt` y causan errores al instalar, **omítelos** (ver pasos abajo).

---

## 🛠️ Guía de Instalación y Ejecución

Sigue las instrucciones específicas para tu sistema operativo.

---

## 🐧 Instalación en Linux (Kali)

### 1️⃣ Instalación y ejecución (terminal, dentro del proyecto)

```bash
# 📦 Paquetes base del sistema
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git unzip build-essential findutils curl

# Clonar el repositorio
git clone https://github.com/usuario/nuamx-django.git
cd nuamx-django

# 🧪 Entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# ⬆️ Actualizar herramientas de instalación
python -m pip install --upgrade pip setuptools wheel

# 📚 Dependencias del proyecto
# Si falla por cx_Oracle/oracledb (no se usan en dev con SQLite), se omiten:
pip install -r requirements.txt \
|| (grep -v -E '^(cx_Oracle|oracledb)\b' requirements.txt > requirements.no_oracle.txt && pip install -r requirements.no_oracle.txt)

# 🧾 Habilitar descarga de plantilla XLSX (endpoint /api/calificaciones/template/)
python -m pip install --no-cache-dir -i https://pypi.org/simple openpyxl

# 🗄️ Migraciones de base de datos
python manage.py migrate

# 👤 (Opcional) Crear superusuario para el admin
python manage.py createsuperuser

# ▶️ Ejecutar servidor de desarrollo
python manage.py runserver 0.0.0.0:8000



































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
