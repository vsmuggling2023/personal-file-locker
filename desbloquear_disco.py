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

def descifrar_archivo(ruta_locked: str, password: str):
    try:
        with open(ruta_locked, 'rb') as f:
            data = f.read()
        if len(data) < 28:
            return False
        salt = data[:16]
        nonce = data[16:28]
        ciphertext = data[28:]
        key = derive_key(password, salt)
        aesgcm = AESGCM(key)
        decrypted = aesgcm.decrypt(nonce, ciphertext, None)
        ruta_original = ruta_locked[:-7]  # sacar .locked
        with open(ruta_original, 'wb') as f:
            f.write(decrypted)
        os.remove(ruta_locked)
        return True
    except Exception:
        return False

def main():
    print("=" * 60)
    print("  DESCFRADO TOTAL DE DISCO")
    print("=" * 60)
    print("\n[!] ESTO VA A DESCIFRAR TODOS LOS ARCHIVOS .locked DE UNA UNIDAD.\n")
    
    discos = []
    for letra in string.ascii_uppercase:
        ruta = f"{letra}:\\"
        if os.path.exists(ruta):
            discos.append(ruta)
    
    if not discos:
        print("No se detectaron discos.")
        input("Presiona Enter para salir...")
        return
    
    print(f"Discos detectados: {', '.join(discos)}")
    
    password = input("\nIngresa la contraseña de descifrado: ").strip()
    if not password:
        print("La contraseña no puede estar vacía.")
        input("Presiona Enter para salir...")
        return
    
    print(f"\nDescifrando {', '.join(discos)} ...")
    
    contador = 0
    errores = 0
    
    for disco_path in discos:
        for root_path, dirs, files in os.walk(disco_path):
            for file in files:
                if not file.endswith(".locked"):
                    continue
                ruta_completa = os.path.join(root_path, file)
                try:
                    if descifrar_archivo(ruta_completa, password):
                        contador += 1
                    else:
                        errores += 1
                except KeyboardInterrupt:
                    print(f"\n\nCancelado. {contador} descifrados, {errores} errores.")
                    input("Presiona Enter para salir...")
                    return
                
                if contador % 100 == 0 and contador > 0:
                    print(f"  Progreso: {contador} archivos descifrados...")
    
    print(f"\n{'=' * 60}")
    print(f"  PROCESO FINALIZADO")
    print(f"  Archivos descifrados: {contador}")
    print(f"  Errores: {errores}")
    print(f"{'=' * 60}")
    input("\nPresiona Enter para finalizar...")

if __name__ == "__main__":
    main()
