import tkinter as tk
from tkinter import filedialog, messagebox
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def cifrar_archivo_gui():
    archivo = filedialog.askopenfilename()
    if not archivo:
        return

    clave = os.urandom(32)
    iv = os.urandom(16)

    with open(archivo, "rb") as f:
        datos = f.read()

    padder = padding.PKCS7(128).padder()
    datos_padded = padder.update(datos) + padder.finalize()

    cipher = Cipher(algorithms.AES(clave), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    datos_cifrados = encryptor.update(datos_padded) + encryptor.finalize()

    output = filedialog.asksaveasfilename(defaultextension=".bin", filetypes=[("Binarios", "*.bin")])
    if output:
        with open(output, "wb") as f:
            f.write(datos_cifrados)

        with open("clave_gui.bin", "wb") as f:
            f.write(clave)
        with open("iv_gui.bin", "wb") as f:
            f.write(iv)

        messagebox.showinfo("Éxito", "Archivo cifrado y guardado.")

def descifrar_archivo_gui():
    archivo = filedialog.askopenfilename()
    if not archivo:
        return

    with open("clave_gui.bin", "rb") as f:
        clave = f.read()
    with open("iv_gui.bin", "rb") as f:
        iv = f.read()

    with open(archivo, "rb") as f:
        datos_cifrados = f.read()

    cipher = Cipher(algorithms.AES(clave), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    datos_padded = decryptor.update(datos_cifrados) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    datos = unpadder.update(datos_padded) + unpadder.finalize()

    output = filedialog.asksaveasfilename(defaultextension=".txt")
    if output:
        with open(output, "wb") as f:
            f.write(datos)
        messagebox.showinfo("Éxito", "Archivo descifrado y guardado.")

# GUI
ventana = tk.Tk()
ventana.title("🔐 Cifrador de Archivos AES")
ventana.geometry("300x180")

tk.Button(ventana, text="Cifrar archivo", command=cifrar_archivo_gui, height=2, width=20).pack(pady=10)
tk.Button(ventana, text="Descifrar archivo", command=descifrar_archivo_gui, height=2, width=20).pack(pady=10)
tk.Button(ventana, text="Salir", command=ventana.destroy, height=2, width=20).pack(pady=10)

ventana.mainloop()
