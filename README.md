# 📦 NUAMX — Guía de Instalación y Ejecución 

## 📖 Manual de Usuario
- https://docs.google.com/document/d/1SDO6DM0cr3O3Fs2VhG7R0z4ISN7CIScp/edit


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

```




























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
## 🐳 Kafka en Windows (opcional, para eventos de calificación)

NUAMX puede enviar eventos a Kafka cada vez que se crean o actualizan calificaciones.  
Si no configuras Kafka, la app funciona igual: solo verás mensajes en consola indicando que el **producer está deshabilitado**.

---

### 1\. Instalar y verificar Docker Desktop

Para ejecutar Kafka en Windows utilizaremos **Docker Desktop**.

1. Descarga Docker Desktop para Windows desde:  
   https://www.docker.com/products/docker-desktop/
2. Instálalo siguiendo el asistente (acepta el uso de **WSL2** si lo pide).
3. Abre Docker Desktop una vez para que arranque el daemon.

Verifica en consola (PowerShell o CMD) que Docker funciona:

```bash
docker version
```

### 2\. Levantar Zookeeper y Kafka con docker-compose

En la carpeta raíz del proyecto existe un archivo docker-compose.yml con la configuración de Zookeeper y Kafka (servicios nuamx-zookeeper y nuamx-kafka).

Desde la carpeta del proyecto, levanta los servicios en segundo plano:

```bash
C:\Users\aronb\Desktop\Nuamx\nuamx a>
docker compose up -d
```

Comprueba que los contenedores están levantados:

```bash
docker ps
```

Deberías ver algo similar a:

```bash
CONTAINER ID   IMAGE                             PORTS
...            confluentinc/cp-kafka:7.6.1       0.0.0.0:9092->9092/tcp
...            confluentinc/cp-zookeeper:7.6.1   0.0.0.0:2181->2181/tcp
```

Nota: Mientras uses Kafka, no cierres Docker Desktop ni pares estos contenedores.

### 3\. Activar el envío de eventos a Kafka en NUAMX

El backend solo enviará eventos a Kafka si la variable de entorno KAFKA_ENABLED está en 1.

Abre una nueva consola entra a la carpeta del proyecto:

```bash
C:\Users\aronb\Desktop\Nuamx\nuamx a>
.\.venv\Scripts\Activate
```

Habilita Kafka en esa sesión y arranca Django:

```bash
set KAFKA_ENABLED=1
```

Iniciar Django

```bash
python manage.py runserver
```

Nota: Si KAFKA_ENABLED no está en 1, la app seguirá funcionando normalmente; solo verás mensajes en consola indicando que el producer Kafka está deshabilitado.

