from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

# 1. Crear una clave secreta de 32 bytes (AES-256)
clave = os.urandom(32)  # Nunca la compartas
iv = os.urandom(16)     # Vector de inicialización

# 2. Crear el mensaje a cifrar
mensaje = b"Este es un mensaje secreto"

# 3. Añadir relleno (padding) para que sea múltiplo de 16
padder = padding.PKCS7(128).padder()
mensaje_padded = padder.update(mensaje) + padder.finalize()

# 4. Crear el objeto de cifrado (AES en modo CBC)
cipher = Cipher(algorithms.AES(clave), modes.CBC(iv), backend=default_backend())
encryptor = cipher.encryptor()

# 5. Cifrar
mensaje_cifrado = encryptor.update(mensaje_padded) + encryptor.finalize()
print("Mensaje cifrado (hex):", mensaje_cifrado.hex())

# 6. Para descifrar
cipher_dec = Cipher(algorithms.AES(clave), modes.CBC(iv), backend=default_backend())
decryptor = cipher_dec.decryptor()
mensaje_descifrado_padded = decryptor.update(mensaje_cifrado) + decryptor.finalize()

# 7. Quitar el padding
unpadder = padding.PKCS7(128).unpadder()
mensaje_descifrado = unpadder.update(mensaje_descifrado_padded) + unpadder.finalize()

print("Mensaje descifrado:", mensaje_descifrado.decode())
