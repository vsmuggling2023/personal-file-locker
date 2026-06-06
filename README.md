# 🔐 PyLocker - Simulador de Cifrado y Descifrado de Carpetas Personales

Language: [Español](#versión-en-español) | [English](#english-version)

---

## Versión en Español

Este repositorio contiene una herramienta educativa de cifrado y descifrado de carpetas de usuario desarrollada en Python utilizando criptografía simétrica avanzada (**AES-256-GCM**).

### ⚠ ADVERTENCIA
> [!WARNING]
> **Este proyecto tiene fines estrictamente educativos y de aprendizaje de conceptos de ciberseguridad.**
> * Este script cifra archivos reales de forma irreversible si se pierde la contraseña.
> * **SOLO** debe ejecutarse en entornos controlados de pruebas (como una **Máquina Virtual**).
> * El autor no se hace responsable de pérdidas accidentales o daños en sistemas de producción. ¡Úsalo con responsabilidad!

### 🛠 Funcionamiento del Proyecto

El sistema consta de dos scripts principales para simular un proceso de bloqueo y rescate:

#### 1. Cifrado de Carpetas Personales (`cifrar_disco.py`)
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

#### 2. Descifrado de Carpetas (`desbloquear_disco.py`)
* Escanea todos los discos del sistema buscando archivos con la extensión `.locked`.
* Solicita la contraseña de descifrado al usuario.
* Si la contraseña es correcta, revierte el cifrado, restaura los archivos originales y elimina los archivos `.locked`.

### ⚙ Requisitos e Instalación

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

### 🚀 Compilación a Ejecutable (`.exe`)

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

### 🔒 Detalles Técnicos del Cifrado

El esquema de seguridad implementado garantiza una fuerte protección de datos:
* **Algoritmo de Cifrado:** **AES-GCM (Galois/Counter Mode)** con clave de 256 bits (Cifrado Autenticado). Asegura que los archivos no puedan modificarse ni descifrarse sin la clave correcta.
* **Derivación de Clave (KDF):** **PBKDF2HMAC** utilizando **SHA-256**, aplicando **600,000 iteraciones** y un *salt* criptográfico aleatorio único de 16 bytes. Esto hace que los ataques de diccionario y fuerza bruta sean extremadamente difíciles y lentos.
* **Estructura del archivo cifrado:** Cada archivo `.locked` generado contiene en su cabecera:
  * Los primeros 16 bytes de `salt` (para derivar la clave).
  * Los siguientes 12 bytes de `nonce` (vector de inicialización único).
  * El resto del archivo corresponde al texto cifrado (`ciphertext`) y al tag de autenticación.

---

## English Version

This repository contains an educational user directory encryption and decryption tool developed in Python using advanced symmetric cryptography (**AES-256-GCM**).

### ⚠ WARNING
> [!WARNING]
> **This project is strictly for educational and cybersecurity learning purposes.**
> * This script encrypts real files irreversibly if the password is lost.
> * It **MUST ONLY** be run in controlled testing environments (such as a **Virtual Machine**).
> * The author is not responsible for accidental data loss or damage to production systems. Use it responsibly!

### 🛠 How it Works

The system consists of two main scripts to simulate a locking and rescue process:

#### 1. Personal Folder Encryption (`cifrar_disco.py`)
* Automatically detects all drive letters and disks connected to the system (`C:\`, `D:\`, etc.).
* Looks for users' personal directories inside `\Users\<username>\` such as:
  * `Desktop`
  * `Documents`
  * `Downloads`
  * `Pictures`
  * `Music`
  * `Videos`
* Recursively encrypts all valid files in these folders, appending the `.locked` extension and deleting the original files.
* Saves a secure local log of the password used in a `contrasena_disco.txt` file in the execution directory.

#### 2. Folder Decryption (`desbloquear_disco.py`)
* Scans all system disks searching for files with the `.locked` extension.
* Prompts the user for the decryption password.
* If the password is correct, it reverts the encryption, restores the original files, and deletes the `.locked` files.

### ⚙ Requirements & Installation

To run the scripts directly from the source code, you need **Python 3.10 or higher** and the `cryptography` library installed.

1. **Install required dependencies:**
   ```bash
   pip install cryptography
   ```

2. **Run disk encryption (inside a Virtual Machine):**
   ```bash
   python cifrar_disco.py
   ```

3. **Run disk decryption:**
   ```bash
   python desbloquear_disco.py
   ```

### 🚀 Compiling to Executable (`.exe`)

If you want to package the scripts into standalone executable files for Windows using **PyInstaller**:

```bash
# Install PyInstaller
pip install pyinstaller

# Compile the disk encryptor to a single executable file
pyinstaller --onefile cifrar_disco.py

# Compile the disk decryptor to a single executable file
pyinstaller --onefile desbloquear_disco.py
```

The resulting executable files will appear in the `./dist/` directory.

### 🔒 Technical Details of Encryption

The implemented security scheme ensures strong data protection:
* **Encryption Algorithm:** **AES-GCM (Galois/Counter Mode)** with a 256-bit key (Authenticated Encryption). This ensures files cannot be modified or decrypted without the correct key.
* **Key Derivation (KDF):** **PBKDF2HMAC** using **SHA-256**, applying **600,000 iterations** and a unique 16-byte random cryptographic *salt*. This makes dictionary and brute-force attacks extremely difficult and slow.
* **Encrypted File Structure:** Each generated `.locked` file contains in its header:
  * The first 16 bytes of the `salt` (to derive the key).
  * The next 12 bytes of the `nonce` (unique initialization vector).
  * The rest of the file corresponds to the ciphertext and the authentication tag.
