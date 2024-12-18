import tkinter as tk
from tkinter import ttk, messagebox
import requests

API_URL = "http://127.0.0.1:8000/api/"  # Ajusta esta URL si es diferente.

# Función para obtener el CSRF token
def get_csrf_token():
    response = requests.get(f"{API_URL}csrf/")  # Endpoint CSRF
    if response.status_code == 200:
        return response.cookies['csrftoken']
    else:
        messagebox.showerror("Error", "No se pudo obtener el token CSRF.")
        return None

headers = {
    'Authorization': f'Bearer 19d81263ba7cc3f43ca9e61acb538e36b7b4a615',  # Tu token de autorización
    'X-CSRFToken': get_csrf_token()  # Agrega el token CSRF aquí
}

# Uso de los headers en una solicitud
response = requests.post('http://127.0.0.1:8000/api/endpoint/', headers=headers, data={'key': 'value'})

if response.status_code == 200:
    print('Solicitud exitosa')
else:
    print(f'Error en la solicitud: {response.status_code}')


# Función para obtener todos los libros
def obtener_libros():
    headers = {
        'Authorization': f'Bearer 19d81263ba7cc3f43ca9e61acb538e36b7b4a615',
        'X-CSRFToken': get_csrf_token()
    }
    response = requests.get(f"{API_URL}libros/", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        messagebox.showerror("Error", f"Error al cargar libros: {response.status_code}")
        return []

# Mostrar libros en el Treeview
def mostrar_libros():
    for libro in tree.get_children():
        tree.delete(libro)
    libros = obtener_libros()
    for libro in libros:
        tree.insert('', tk.END, values=(libro['codigo'], libro['titulo'], libro['autor'], libro['genero']))

# Función para agregar un nuevo libro
def agregar_libro():
    def enviar_datos():
        codigo = entry_codigo.get().strip()
        titulo = entry_titulo.get().strip()
        autor = entry_autor.get().strip()
        genero = entry_genero.get().strip()

        if not codigo or not titulo or not autor or not genero:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        data = {
            "codigo": codigo,
            "titulo": titulo,
            "autor": autor,
            "genero": genero
        }

        try:
            headers = {
                'Authorization': f'Bearer 19d81263ba7cc3f43ca9e61acb538e36b7b4a615',
                'X-CSRFToken': get_csrf_token()
            }
            response = requests.post(f"{API_URL}libros/", json=data, headers=headers)
            response.raise_for_status()
            if response.status_code == 201:
                messagebox.showinfo("Éxito", "Libro agregado correctamente.")
                ventana_agregar.destroy()
                mostrar_libros()
            else:
                messagebox.showerror("Error", f"No se pudo agregar el libro: {response.status_code}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar con la API: {e}")

    ventana_agregar = tk.Toplevel(root)
    ventana_agregar.title("Agregar Libro")

    tk.Label(ventana_agregar, text="Código:").pack()
    entry_codigo = tk.Entry(ventana_agregar)
    entry_codigo.pack()

    tk.Label(ventana_agregar, text="Título:").pack()
    entry_titulo = tk.Entry(ventana_agregar)
    entry_titulo.pack()

    tk.Label(ventana_agregar, text="Autor:").pack()
    entry_autor = tk.Entry(ventana_agregar)
    entry_autor.pack()

    tk.Label(ventana_agregar, text="Género:").pack()
    entry_genero = tk.Entry(ventana_agregar)
    entry_genero.pack()

    tk.Button(ventana_agregar, text="Agregar", command=enviar_datos).pack()

# Función para modificar un libro
def modificar_libro():
    def enviar_datos():
        codigo = entry_codigo.get().strip()
        titulo = entry_titulo.get().strip()
        autor = entry_autor.get().strip()
        genero = entry_genero.get().strip()

        if not codigo or not titulo or not autor or not genero:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        data = {
            "titulo": titulo,
            "autor": autor,
            "genero": genero
        }

        try:
            headers = {
                'Authorization': f'Bearer 19d81263ba7cc3f43ca9e61acb538e36b7b4a615',
                'X-CSRFToken': get_csrf_token()
            }
            response = requests.put(f"{API_URL}libros/{codigo}/", json=data, headers=headers)
            response.raise_for_status()
            if response.status_code == 200:
                messagebox.showinfo("Éxito", "Libro modificado correctamente.")
                ventana_modificar.destroy()
                mostrar_libros()
            else:
                messagebox.showerror("Error", f"No se pudo modificar el libro: {response.status_code}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar con la API: {e}")

    codigo_seleccionado = tree.item(tree.selection())['values'][0]

    ventana_modificar = tk.Toplevel(root)
    ventana_modificar.title("Modificar Libro")

    tk.Label(ventana_modificar, text="Código:").pack()
    entry_codigo = tk.Entry(ventana_modificar, state='disabled')
    entry_codigo.pack()
    entry_codigo.insert(0, codigo_seleccionado)

    tk.Label(ventana_modificar, text="Título:").pack()
    entry_titulo = tk.Entry(ventana_modificar)
    entry_titulo.pack()

    tk.Label(ventana_modificar, text="Autor:").pack()
    entry_autor = tk.Entry(ventana_modificar)
    entry_autor.pack()

    tk.Label(ventana_modificar, text="Género:").pack()
    entry_genero = tk.Entry(ventana_modificar)
    entry_genero.pack()

    tk.Button(ventana_modificar, text="Modificar", command=enviar_datos).pack()

# Función para eliminar un libro
def eliminar_libro():
    codigo_seleccionado = tree.item(tree.selection())['values'][0]
    headers = {
        'Authorization': f'Bearer 19d81263ba7cc3f43ca9e61acb538e36b7b4a615',
        'X-CSRFToken': get_csrf_token()
    }
    response = requests.delete(f"{API_URL}libros/{codigo_seleccionado}/", headers=headers)
    if response.status_code == 204:
        messagebox.showinfo("Éxito", "Libro eliminado correctamente.")
        mostrar_libros()
    else:
        messagebox.showerror("Error", f"Error al eliminar el libro: {response.status_code}")

# Interfaz gráfica
root = tk.Tk()
root.title("Gestión de Libros")

# Treeview para mostrar libros
tree = ttk.Treeview(root, columns=('Código', 'Título', 'Autor', 'Género'), show='headings')
tree.heading('Código', text='Código')
tree.heading('Título', text='Título')
tree.heading('Autor', text='Autor')
tree.heading('Género', text='Género')
tree.pack()

# Botones para agregar, modificar y eliminar libros
btn_cargar = tk.Button(root, text="Cargar Libros", command=mostrar_libros)
btn_cargar.pack()

btn_agregar = tk.Button(root, text="Agregar Libro", command=agregar_libro)
btn_agregar.pack()

btn_modificar = tk.Button(root, text="Modificar Libro", command=modificar_libro)
btn_modificar.pack()

btn_eliminar = tk.Button(root, text="Eliminar Libro", command=eliminar_libro)
btn_eliminar.pack()

# Mostrar libros al inicio
mostrar_libros()

root.mainloop()
