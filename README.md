# 🔐 PyLocker & Clone Hero Song Protector

Este repositorio contiene dos herramientas de cifrado y protección desarrolladas en Python utilizando criptografía simétrica avanzada (**AES-256-GCM**). 

---

## ⚠ ADVERTENCIA IMPORTANTE / WARNING
> [!WARNING]
> **Este proyecto incluye herramientas con capacidad de cifrar archivos del sistema de forma irreversible si se pierde la contraseña.**
> * La herramienta de cifrado de disco (`cifrar_disco.py`) **SOLO debe ser ejecutada en entornos controlados (Máquinas Virtuales)**.
> * El autor no se hace responsable de pérdida de datos accidental. ¡Úsalo bajo tu propio riesgo!

---

## 🛠 Contenido del Proyecto

El proyecto está dividido en dos utilidades principales:

### 1. 🎸 Clone Hero Song Protector (`proteger.py` & `desbloquear.py`)
Diseñado especialmente para streamers, creadores de contenido o torneos de **Clone Hero** que deseen "bloquear" temporalmente el acceso a ciertas canciones (impidiendo que el juego las cargue al no encontrar los archivos de notas e información).

* **`proteger.py` (CLI):** 
  * Escanea la carpeta actual y sus subcarpetas en busca de archivos `notes.mid` y `song.ini` (estructura típica de canciones de Clone Hero).
  * Cifra estos archivos usando AES-GCM, renombrándolos a `.locked` y eliminando los originales.
  * Guarda un registro local de las contraseñas utilizadas en `contrasenas.txt` para mayor seguridad del administrador.
* **`desbloquear.py` (GUI):**
  * Aplicación gráfica limpia y moderna creada con **Tkinter**.
  * Permite al usuario/jugador introducir la contraseña correspondiente para restaurar los archivos `notes.mid` y `song.ini` y poder jugar la canción al instante.

### 2. 🖥 Cifrador y Descifrador de Carpetas de Disco (`cifrar_disco.py` & `desbloquear_disco.py`)
Una herramienta de simulación educativa/ciberseguridad de tipo "locker".
* **`cifrar_disco.py`:** 
  * Escanea automáticamente todas las unidades/discos del sistema.
  * Localiza las carpetas personales de los usuarios (`Escritorio`, `Documentos`, `Descargas`, `Imágenes`, `Música`, `Videos`).
  * Cifra recursivamente todos los archivos contenidos con una contraseña global de tu elección.
* **`desbloquear_disco.py`:**
  * Escanea todos los discos buscando archivos con la extensión `.locked` y los descifra en masa utilizando la contraseña correcta.

---

## ⚙ Requisitos e Instalación

Para ejecutar los scripts directamente desde el código fuente necesitas **Python 3.10 o superior** y las dependencias de criptografía.

1. **Instalar dependencias:**
   ```bash
   pip install cryptography
   ```

2. **Ejecutar el protector de canciones (Clone Hero):**
   ```bash
   python proteger.py
   ```

3. **Ejecutar el desbloqueador de canciones (interfaz gráfica):**
   ```bash
   python desbloquear.py
   ```

---

## 🚀 Compilación a Ejecutable (`.exe`)

Si deseas generar archivos ejecutables independientes para Windows utilizando **PyInstaller**, ejecuta los siguientes comandos:

```bash
# Instalar PyInstaller si no lo tienes
pip install pyinstaller

# Compilar el protector de canciones (Consola)
pyinstaller --onefile proteger.py

# Compilar el desbloqueador de canciones (Sin consola - GUI limpia)
pyinstaller --onefile --noconsole desbloquear.py

# Compilar cifrador de disco (Consola)
pyinstaller --onefile cifrar_disco.py

# Compilar descifrador de disco (Consola)
pyinstaller --onefile desbloquear_disco.py
```

Los archivos `.exe` listos para usar se generarán dentro de la carpeta `dist`.

---

## 🔒 Detalles Técnicos del Cifrado

El esquema de seguridad implementado garantiza que los archivos sean indescifrables sin la contraseña correcta:
* **Algoritmo de Cifrado:** **AES-GCM (Galois/Counter Mode)** con clave de 256 bits, que proporciona confidencialidad y verificación de integridad (cifrado autenticado).
* **Derivación de Clave (KDF):** **PBKDF2HMAC** utilizando **SHA-256**, con **600,000 iteraciones** y un *salt* aleatorio único de 16 bytes generado por sesión, lo que mitiga ataques de fuerza bruta y tablas arcoíris.
* **Metadatos del archivo cifrado:** Cada archivo `.locked` almacena en su cabecera los 16 bytes de `salt` y los 12 bytes del vector de inicialización (`nonce`) necesarios para su posterior descifrado.
