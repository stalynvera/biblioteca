import tkinter as tk
from tkinter import ttk
import requests

API_URL = "http://127.0.0.1:8000/api/"

def obtener_libros():
    response = requests.get(f"{API_URL}libros/")
    return response.json()

def mostrar_libros():
    libros = obtener_libros()
    for libro in libros:
        tree.insert('', tk.END, values=(libro['id'], libro['titulo'], libro['autor'], libro['genero']))

# Interfaz gráfica
root = tk.Tk()
root.title("Biblioteca - Gestión de Libros")

tree = ttk.Treeview(root, columns=('ID', 'Título', 'Autor', 'Género'), show='headings')
tree.heading('ID', text='ID')
tree.heading('Título', text='Título')
tree.heading('Autor', text='Autor')
tree.heading('Género', text='Género')
tree.pack()

btn_cargar = tk.Button(root, text="Cargar Libros", command=mostrar_libros)
btn_cargar.pack()

root.mainloop()
