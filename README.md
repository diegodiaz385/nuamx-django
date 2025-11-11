# 🚀 NUAMX - Plataforma Operativa Django/API

**NUAMX** es una plataforma web construida con **Django** que utiliza **Django REST Framework (DRF)** para gestionar la **autenticación (JWT)** y el **control de usuarios y roles (RBAC)** a través de una API segura.  
El frontend es renderizado por Django y consume la API mediante JavaScript.

Manual de usuario : https://docs.google.com/document/d/1SDO6DM0cr3O3Fs2VhG7R0z4ISN7CIScp/edit?usp=sharing&oui=106241663586320063931&rtpof=true&sd=true

---

# 📦 NUAMX — Guía de Instalación y Ejecución (método ZIP)

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

## 🐧 Instalación en Linux (Kali, Ubuntu, Debian)

### 1️⃣ Preparar el entorno (método ZIP + panel gráfico)

- **Descarga** el proyecto en **ZIP** desde GitHub.  
- Abre la carpeta donde quedó el ZIP (por ejemplo, **Descargas**).  
- **Click derecho** sobre el ZIP → **Extraer aquí**.  
- *(Opcional)* **Mueve** la carpeta extraída al **Escritorio** para tenerla a mano.  
- Entra a la carpeta **hasta ver** el archivo **`manage.py`**.  
- Dentro de esa carpeta, **click derecho** → **Abrir en una terminal**.

> ✅ A partir de aquí, los comandos asumen que **ya estás** en la carpeta que contiene `manage.py`.

```bash
# 1) Instalacion y exportación
1. Descarga el proyecto en formato ZIP (desde GitHub u otra fuente).
2. Ve a la carpeta donde quedó el archivo (Ej: Descargas).
3. Click derecho → “Extraer aquí” (o “Extract Here”).
4. Mueve la carpeta extraída al Escritorio (opcional, solo para tenerla a mano).
5. Entra a la carpeta hasta ver `manage.py`.
6. Click derecho dentro de la carpeta → “Abrir en una terminal”.
7. Continúa con la sección Instalación.

# 2) Paquetes base del sistema 
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git unzip build-essential findutils curl

# 3) Entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# 4) Herramientas de instalación al día
python -m pip install --upgrade pip setuptools wheel

# 5) Dependencias del proyecto
#    (si falla por cx_Oracle/oracledb, se omiten para dev con SQLite)
pip install -r requirements.txt \
|| (grep -v -E '^(cx_Oracle|oracledb)\b' requirements.txt > requirements.no_oracle.txt && pip install -r requirements.no_oracle.txt)

# 6) openpyxl (necesario para descargar la plantilla XLSX)
python -m pip install --no-cache-dir -i https://pypi.org/simple openpyxl

# 7) Preparar BD y ejecutar
python manage.py migrate
python manage.py runserver


