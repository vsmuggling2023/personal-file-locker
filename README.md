# 🔐 PyLocker - Simulador de Cifrado y Descifrado de Carpetas Personales

Este repositorio contiene una herramienta educativa de cifrado y descifrado de carpetas de usuario desarrollada en Python utilizando criptografía simétrica avanzada (**AES-256-GCM**).

---

## ⚠ ADVERTENCIA / WARNING
> [!WARNING]
> **Este proyecto tiene fines estrictamente educativos y de aprendizaje de conceptos de ciberseguridad.**
> * Este script cifra archivos reales de forma irreversible si se pierde la contraseña.
> * **SOLO** debe ejecutarse en entornos controlados de pruebas (como una **Máquina Virtual**).
> * El autor no se hace responsable de pérdidas accidentales o daños en sistemas de producción. ¡Úsalo con responsabilidad!

---

## 🛠 Funcionamiento del Proyecto

El sistema consta de dos scripts principales para simular un proceso de bloqueo y rescate:

### 1. Cifrado de Carpetas Personales (`cifrar_disco.py`)
* Detecta automáticamente todas las letras de unidades y discos conectados al sistema (`C:\`, `D:\`, etc.).
* Busca los directorios personales de los usuarios dentro de `\Users\<nombre_usuario>\` como:
  * `Escritorio` (Desktop)
  * `Documentos` (Documents)
  * `Descargas` (Downloads)
  * `Imágenes` (Pictures)
  * `Música` (Music)
  * `Videos` (Videos)
* Cifra recursivamente todos los archivos válidos contenidos en estas carpetas, añadiendo la extensión `.locked` y eliminando los archivos originales.
* Guarda un registro local seguro con la contraseña utilizada en un archivo `contrasena_disco.txt` en el directorio de ejecución.

### 2. Descifrado de Carpetas (`desbloquear_disco.py`)
* Escanea todos los discos del sistema buscando archivos con la extensión `.locked`.
* Solicita la contraseña de descifrado al usuario.
* Si la contraseña es correcta, revierte el cifrado, restaura los archivos originales y elimina los archivos `.locked`.

---

## ⚙ Requisitos e Instalación

Para ejecutar los scripts directamente desde el código fuente necesitas tener instalado **Python 3.10 o superior** y la biblioteca `cryptography`.

1. **Instalar dependencias necesarias:**
   ```bash
   pip install cryptography
   ```

2. **Ejecutar el cifrado de disco (en una Máquina Virtual):**
   ```bash
   python cifrar_disco.py
   ```

3. **Ejecutar el descifrado de disco:**
   ```bash
   python desbloquear_disco.py
   ```

---

## 🚀 Compilación a Ejecutable (`.exe`)

Si deseas empaquetar los scripts en archivos ejecutables para Windows usando **PyInstaller**:

```bash
# Instalar PyInstaller
pip install pyinstaller

# Compilar el cifrador de disco a un único archivo ejecutable
pyinstaller --onefile cifrar_disco.py

# Compilar el descifrador de disco a un único archivo ejecutable
pyinstaller --onefile desbloquear_disco.py
```

Los archivos ejecutables resultantes aparecerán en la carpeta `./dist/`.

---

## 🔒 Detalles Técnicos del Cifrado

El esquema de seguridad implementado garantiza una fuerte protección de datos:
* **Algoritmo de Cifrado:** **AES-GCM (Galois/Counter Mode)** con clave de 256 bits (Cifrado Autenticado). Asegura que los archivos no puedan modificarse ni descifrarse sin la clave correcta.
* **Derivación de Clave (KDF):** **PBKDF2HMAC** utilizando **SHA-256**, aplicando **600,000 iteraciones** y un *salt* criptográfico aleatorio único de 16 bytes. Esto hace que los ataques de diccionario y fuerza bruta sean extremadamente difíciles y lentos.
* **Estructura del archivo cifrado:** Cada archivo `.locked` generado contiene en su cabecera:
  * Los primeros 16 bytes de `salt` (para derivar la clave).
  * Los siguientes 12 bytes de `nonce` (vector de inicialización único).
  * El resto del archivo corresponde al texto cifrado (`ciphertext`) y al tag de autenticación.
