from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

# === CIFRAR Y GUARDAR ===

# 1. Crear clave y IV
clave = os.urandom(32)  # AES-256
iv = os.urandom(16)     # IV de 16 bytes

# 2. Mensaje original
mensaje = b"Este es un mensaje importante y cifrado."

# 3. Padding
padder = padding.PKCS7(128).padder()
mensaje_padded = padder.update(mensaje) + padder.finalize()

# 4. Cifrado
cipher = Cipher(algorithms.AES(clave), modes.CBC(iv), backend=default_backend())
encryptor = cipher.encryptor()
mensaje_cifrado = encryptor.update(mensaje_padded) + encryptor.finalize()

# 5. Guardar en archivos
with open("mensaje_cifrado.bin", "wb") as f:
    f.write(mensaje_cifrado)

with open("clave.bin", "wb") as f:
    f.write(clave)

with open("iv.bin", "wb") as f:
    f.write(iv)

print("✅ Mensaje cifrado y guardado.")

# === LEER Y DESCIFRAR ===

# 6. Leer datos desde archivos
with open("mensaje_cifrado.bin", "rb") as f:
    mensaje_cifrado = f.read()

with open("clave.bin", "rb") as f:
    clave = f.read()

with open("iv.bin", "rb") as f:
    iv = f.read()

# 7. Descifrado
cipher_dec = Cipher(algorithms.AES(clave), modes.CBC(iv), backend=default_backend())
decryptor = cipher_dec.decryptor()
mensaje_descifrado_padded = decryptor.update(mensaje_cifrado) + decryptor.finalize()

# 8. Quitar padding
unpadder = padding.PKCS7(128).unpadder()
mensaje_descifrado = unpadder.update(mensaje_descifrado_padded) + unpadder.finalize()

print("🔓 Mensaje descifrado:", mensaje_descifrado.decode())
print("✅ Proceso completado.")
# Este código cifra un mensaje, lo guarda en un archivo y luego lo lee y descifra.
# Asegúrate de manejar la clave y el IV con cuidado, ya que son esenciales para el descifrado.
# Recuerda que la seguridad de tu cifrado depende de mantener la clave y el IV en secreto.
# No compartas la clave ni el IV con nadie.
