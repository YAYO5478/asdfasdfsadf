from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

# === CIFRAR ARCHIVO ===

def cifrar_archivo(nombre_entrada, nombre_salida, clave_path, iv_path):
    clave = os.urandom(32)  # AES-256
    iv = os.urandom(16)     # IV de 16 bytes

    with open(nombre_entrada, "rb") as f:
        datos = f.read()

    # Padding
    padder = padding.PKCS7(128).padder()
    datos_padded = padder.update(datos) + padder.finalize()

    cipher = Cipher(algorithms.AES(clave), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    datos_cifrados = encryptor.update(datos_padded) + encryptor.finalize()

    with open(nombre_salida, "wb") as f:
        f.write(datos_cifrados)

    with open(clave_path, "wb") as f:
        f.write(clave)

    with open(iv_path, "wb") as f:
        f.write(iv)

    print("✅ Archivo cifrado guardado como:", nombre_salida)


# === DESCIFRAR ARCHIVO ===

def descifrar_archivo(nombre_entrada, nombre_salida, clave_path, iv_path):
    with open(nombre_entrada, "rb") as f:
        datos_cifrados = f.read()

    with open(clave_path, "rb") as f:
        clave = f.read()

    with open(iv_path, "rb") as f:
        iv = f.read()

    cipher = Cipher(algorithms.AES(clave), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    datos_padded = decryptor.update(datos_cifrados) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    datos = unpadder.update(datos_padded) + unpadder.finalize()

    with open(nombre_salida, "wb") as f:
        f.write(datos)

    print("🔓 Archivo descifrado guardado como:", nombre_salida)

# === USO DEL PROGRAMA ===

# 1. Cifrar
cifrar_archivo("ejemplo.txt", "ejemplo_cifrado.bin", "clave.bin", "iv.bin")

# 2. Descifrar
descifrar_archivo("ejemplo_cifrado.bin", "ejemplo_descifrado.txt", "clave.bin", "iv.bin")
    