# 🪟 NUAMX - Plataforma Operativa Django/API (Guía para Linux)




























# 🪟 NUAMX - Plataforma Operativa Django/API (Guía para Windows)

**NUAMX** es una plataforma web construida con **Django** que utiliza **Django REST Framework (DRF)** para gestionar la **autenticación (JWT)** y el **control de usuarios y roles (RBAC)** a través de una API segura.  
El frontend es renderizado por Django y consume la API mediante JavaScript.

---

## 📋 Requisitos del Sistema

- **Windows 10 / 11**
- **Python:** versión 3.9 o superior  
- **Git:** instalado y configurado  
- **PIP:** gestor de paquetes de Python  
- **Editor recomendado:** Visual Studio Code  

> 💡 **Recomendación:** usa siempre un **entorno virtual (`.venv`)** para evitar conflictos de dependencias entre proyectos.

---

## 🧱 1️⃣ Instalar herramientas necesarias

### 🔧 Microsoft Visual C++ Build Tools

Algunos paquetes de Python (como `cx_Oracle`) requieren compiladores en C++.  
Descárgalo desde el sitio oficial de Microsoft:

👉 [https://visualstudio.microsoft.com/visual-cpp-build-tools/](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

Durante la instalación:
- Marca **“Desktop development with C++”**  
- Instala los componentes sugeridos  
- Reinicia el sistema al finalizar (opcional)

---

## 🐍 2️⃣ Clonar el repositorio del proyecto

Abre **PowerShell** o **Git Bash** en la carpeta donde quieras guardar el proyecto y ejecuta:

```powershell
- git clone https://github.com/diegodiaz385/nuamx-django.git
- cd nuamx-django

## 🌐 3️⃣ Crear y activar el entorno virtual
- python -m venv .venv
- .\.venv\Scripts\Activate.ps1

## ⚠️ Si PowerShell bloquea la activación, ejecuta como administrador(SOLO SI LA BLOQUEA):
Set-ExecutionPolicy Unrestricted -Scope Process

- pip install --upgrade pip
- pip install -r requirements.txt

## 4.Aplicar migraciones y crear superusuario
- python manage.py migrate
- python manage.py createsuperuser

## 5.Ejecuta el Servidor
- python manage.py runserver

