import tkinter as tk
from tkinter import ttk
from pyswip import Prolog

# Inicializa Prolog
prolog = Prolog()
prolog.consult("minerales.pl")  # Asegúrate de que el archivo Prolog esté en el mismo directorio

def mostrar_pantalla_busqueda(tipo):
    for widget in root.winfo_children():
        widget.destroy()

    def limpiar_campos():
        grupo_combobox.set("")
        color_combobox.set("")
        raya_combobox.set("")
        dureza_scale.set(0)  # Valor inicial para indicar vacío
        densidad_scale.set(0)  # Valor inicial para indicar vacío

    def ajustar_valor(valor):
        return "_" if valor == 0 else valor  # Si el valor es 0, usamos '_'

    # Función para actualizar los resultados en el cuadro de texto
    def actualizar_resultados(texto, color="#4CAF50"):
        resultados_text.delete(1.0, tk.END)  # Limpiar texto anterior
        resultados_text.insert(tk.END, texto)
        resultados_text.tag_add("center", "1.0", tk.END)
        resultados_text.tag_config("center", foreground=color)

    def buscar_exacta():
        grupo = grupo_combobox.get()
        color = color_combobox.get()
        raya = raya_combobox.get()
        dureza = dureza_scale.get()
        densidad = densidad_scale.get()

        if dureza == 0 or densidad == 0 or not (grupo and color and raya):
            actualizar_resultados("Debe completar todos los campos para la búsqueda exacta.", color="red")
            return

        query = f"adivinar_mineral('{grupo}', '{color}', '{raya}', {dureza}, {densidad}, Mineral)"
        resultados = list(prolog.query(query))
        if resultados:
            resultados_texto = "\n".join([str(resultado["Mineral"]) for resultado in resultados])
            actualizar_resultados(f"Resultados de Búsqueda Exacta:\n{resultados_texto}")
        else:
            actualizar_resultados("No se encontraron coincidencias.", color="red")

    def buscar_normal():
        grupo = grupo_combobox.get() if grupo_combobox.get() else "_"
        color = color_combobox.get() if color_combobox.get() else "_"
        raya = raya_combobox.get() if raya_combobox.get() else "_"
        dureza = ajustar_valor(dureza_scale.get())
        densidad = ajustar_valor(densidad_scale.get())

        query = f"adivinar_probabilidad({grupo}, {color}, {raya}, {dureza}, {densidad}, Resultados)"
        resultados = list(prolog.query(query))
        if resultados:
            # Extraer y ordenar los resultados por probabilidad en orden descendente
            resultados_lista = resultados[0]['Resultados']
            resultados_ordenados = sorted(
                resultados_lista,
                key=lambda x: float(x[1]) if isinstance(x, tuple) else float(x.split(',')[1][:-1]),
                reverse=True
            )

            # Filtrar los resultados con probabilidad 0
            resultados_filtrados = [
                r for r in resultados_ordenados 
                if (float(r[1]) if isinstance(r, tuple) else float(r.split(',')[1][:-1])) > 0
            ]

            # Formatear la salida
            resultados_texto = "\n".join([
                f"{r[0]} - {float(r[1]):.2f}" if isinstance(r, tuple) else f"{r.split(',')[0][1:]} - {float(r.split(',')[1][:-1]):.2f}"
                for r in resultados_filtrados
            ])
            actualizar_resultados(f"Resultados de Búsqueda por Probabilidad:\n{resultados_texto}")
        else:
            actualizar_resultados("No se encontraron coincidencias.", color="red")

    def buscar_estricta():
        grupo = grupo_combobox.get() if grupo_combobox.get() else "_"
        color = color_combobox.get() if color_combobox.get() else "_"
        raya = raya_combobox.get() if raya_combobox.get() else "_"
        dureza = ajustar_valor(dureza_scale.get())
        densidad = ajustar_valor(densidad_scale.get())

        query = f"buscar_estricto({grupo}, {color}, {raya}, {dureza}, {densidad}, Resultados)"
        resultados = list(prolog.query(query))
        if resultados:
            resultados_lista = resultados[0]['Resultados']
            resultados_texto = "\n".join([
                f"{r[0]} - {float(r[1]):.2f}" if isinstance(r, tuple) else f"{r.split(',')[0][1:]} - {float(r.split(',')[1][:-1]):.2f}"
                for r in resultados_lista
            ])
            actualizar_resultados(f"Resultados de Búsqueda Estricta:\n{resultados_texto}")
        else:
            actualizar_resultados("No se encontraron coincidencias.", color="red")

    root.config(bg="#f5f5f5")
    frame = tk.Frame(root, bg="#ffffff", relief=tk.RAISED, borderwidth=2)
    frame.place(relx=0.5, rely=0.5, anchor="center", width=700, height=550)

    tk.Label(frame, text="Búsqueda de Minerales", bg="#ffffff", fg="#333333", font=("Arial", 18)).pack(pady=10)
    
    form_frame = tk.Frame(frame, bg="#ffffff")
    form_frame.pack(pady=10)

    def agregar_label(texto):
        return tk.Label(form_frame, text=texto, bg="#ffffff", fg="#555555", font=("Arial", 12))

    agregar_label("Grupo Cristalino:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    grupo_combobox = ttk.Combobox(form_frame, values=["hexagonal", "cubo", "monoclinico", "ortorrombico", "tetragonal", "triclinico", "trigonal"], state="readonly", width=30)
    grupo_combobox.grid(row=0, column=1, padx=10, pady=5)

    agregar_label("Color:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    color_combobox = ttk.Combobox(form_frame, values=["azul", "rojo_oscuro", "incoloro", "gris", "negro", "multicolor", "amarillo_claro", "dorado", "rojo", "violeta", "gris_oscuro", "blanco", "amarillo", "varios_colores", "amarillo_dorado", "verde_intenso", "verde_claro", "verde_oscuro", "gris_claro", "verde", "azul_claro", "naranja", "marron", "rosa_claro", "rosa", "verde_azulado", "azul_intenso", "anaranjado"], state="readonly", width=30)
    color_combobox.grid(row=1, column=1, padx=10, pady=5)

    agregar_label("Raya:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    raya_combobox = ttk.Combobox(form_frame, values=["blanca", "azul", "rojo", "gris_oscuro", "negro", "gris", "amarillo", "incoloro", "verde", "dorado", "amarillo", "azul_claro", "rosa_claro", "marron", "rosa", "varios_colores", "naranja"], state="readonly", width=30)
    raya_combobox.grid(row=2, column=1, padx=10, pady=5)

    agregar_label("Dureza:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    dureza_scale = tk.Scale(form_frame, from_=0, to=10, resolution=0.1, orient=tk.HORIZONTAL, length=300, bg="#ffffff", troughcolor="#007BFF")
    dureza_scale.grid(row=3, column=1, padx=10, pady=5)

    agregar_label("Densidad:").grid(row=4, column=0, padx=25, pady=5, sticky="w")
    densidad_scale = tk.Scale(
        form_frame,
        from_=0, 
        to=25, 
        resolution=0.1,
        orient=tk.HORIZONTAL, 
        length=300, 
        bg="#ffffff", 
        troughcolor="#007BFF"
    )
    densidad_scale.grid(row=4, column=1, padx=10, pady=5)

    botones_frame = tk.Frame(frame, bg="#ffffff")
    botones_frame.pack(pady=10)

    tk.Button(botones_frame, text="Buscar", command=buscar_exacta if tipo == "exacta" else buscar_normal if tipo == "normal" else buscar_estricta,
              bg="#007BFF", fg="white", font=("Arial", 12), width=15).pack(side=tk.LEFT, padx=10)
    tk.Button(botones_frame, text="Limpiar Campos", command=limpiar_campos,
              bg="#6c757d", fg="white", font=("Arial", 12), width=15).pack(side=tk.LEFT, padx=10)
    tk.Button(botones_frame, text="Regresar", command=pantalla_inicio,
              bg="#dc3545", fg="white", font=("Arial", 12), width=15).pack(side=tk.LEFT, padx=10)

    # Frame para contener los resultados con un scrollbar
    resultados_frame = tk.Frame(frame, bg="#ffffff")
    resultados_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(resultados_frame, orient=tk.VERTICAL)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    resultados_text = tk.Text(
        resultados_frame, 
        wrap=tk.WORD, 
        yscrollcommand=scrollbar.set, 
        width=70,  
        height=10,  
        font=("Arial", 12), 
        bg="#f9f9f9", 
        fg="#333333", 
        relief=tk.SOLID, 
        bd=1
    )
    resultados_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=resultados_text.yview)

def pantalla_inicio():
    for widget in root.winfo_children():
        widget.destroy()

    root.config(bg="#343a40")
    frame = tk.Frame(root, bg="#343a40")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame, text="Bienvenido al Identificador de Minerales", font=("Arial", 20), bg="#343a40", fg="white").pack(pady=30)
    tk.Button(frame, text="Búsqueda Exacta", command=lambda: mostrar_pantalla_busqueda("exacta"),
              bg="#007BFF", fg="white", font=("Arial", 15), width=20).pack(pady=10)
    tk.Button(frame, text="Búsqueda por Probabilidad", command=lambda: mostrar_pantalla_busqueda("normal"),
              bg="#28a745", fg="white", font=("Arial", 15), width=20).pack(pady=10)
    tk.Button(frame, text="Búsqueda Estricta", command=lambda: mostrar_pantalla_busqueda("estricta"),
              bg="#ffc107", fg="white", font=("Arial", 15), width=20).pack(pady=10)

# Configuración inicial de la ventana principal
root = tk.Tk()
root.title("Identificador de Minerales")
root.geometry("800x600")
root.resizable(False, False)  # Bloquea el cambio de tamaño de la ventana
pantalla_inicio()
root.mainloop()
