from cryptography.fernet import Fernet

# 1. Generar una clave secreta (hazlo solo una vez y guárdala en un lugar seguro)
clave = Fernet.generate_key()
print("CLAVE SECRETA:", clave.decode())

# 2. Crear el objeto de cifrado
fernet = Fernet(clave)

# 3. Mensaje original
mensaje = "diablo".encode()

# 4. Cifrar el mensaje
mensaje_cifrado = fernet.encrypt(mensaje)
print("CIFRADO:", mensaje_cifrado.decode())

# 5. Descifrar el mensaje
mensaje_descifrado = fernet.decrypt(mensaje_cifrado)
print("DESCIFRADO:", mensaje_descifrado.decode())
