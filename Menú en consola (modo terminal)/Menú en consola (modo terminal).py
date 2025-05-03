import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def cifrar_archivo(nombre_entrada, nombre_salida, clave_path, iv_path):
    clave = os.urandom(32)
    iv = os.urandom(16)

    with open(nombre_entrada, "rb") as f:
        datos = f.read()

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

    print("✅ Archivo cifrado con éxito.")

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

    print("🔓 Archivo descifrado con éxito.")

def menu():
    while True:
        print("\n📦 Herramienta de cifrado de archivos")
        print("1. Cifrar archivo")
        print("2. Descifrar archivo")
        print("3. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            origen = input("Archivo a cifrar: ")
            destino = input("Nombre del archivo cifrado: ")
            cifrar_archivo(origen, destino, "clave.bin", "iv.bin")

        elif opcion == "2":
            origen = input("Archivo cifrado: ")
            destino = input("Nombre del archivo descifrado: ")
            descifrar_archivo(origen, destino, "clave.bin", "iv.bin")

        elif opcion == "3":
            print("Saliendo...")
            break
        else:
            print("❌ Opción inválida.")

if __name__ == "__main__":
    menu()
