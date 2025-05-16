from tkinter import *
from tkinter import ttk, messagebox, PhotoImage
import os
try:
    from .tablero import main  # Para ejecución como módulo (desde main.py)
except ImportError:
    from tablero import main   # Para ejecución directa (menu.py)


# Valores de configuración en la interfaz
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Ruta base del proyecto
COLOR_FONDO = "#303030"  # Color gris oscuro para el fondo
COLOR_BOTON = "#606060"  # Color gris claro para botones
COLOR_TEXTO = "#FFFFFF"  # Color blanco para el texto de los botones
MENSAJE_BIENVENIDA = """Bienvenido a Yoshi's zones, para jugar selecciona una dificultad y luego dale al botón iniciar.\n
El Yoshi que marque más casillas especiales con su color, gana.\n
Solo se permiten movimientos en "L" como la pieza del caballo en ajedrez."""

# Definición de las dificultades
dificultades = ["...", "Principiante", "Amateur", "Experto"]

def habilitar_controles():
    boton_iniciar.config(state=NORMAL)
    boton_borrar.config(state=NORMAL)
    combo_algoritmo.config(state="readonly")

# Función para iniciar la simulación
def iniciar():
    if dificultad_seleccionada.get() == "...":
        messagebox.showerror("Error", "Debe seleccionar una dificultad antes de iniciar.")
        return

    # 1) Deshabilito controles
    boton_iniciar.config(state=DISABLED)
    boton_borrar.config(state=DISABLED)
    combo_algoritmo.config(state=DISABLED)

    # 2) Actualizo el mensaje en el panel
    dificultad = dificultad_seleccionada.get()
    mensaje_iniciar = f"Iniciando Yoshi's zones en dificultad {dificultad}..."
    panel_texto.configure(state="normal")
    panel_texto.delete("1.0", END)
    panel_texto.insert(END, MENSAJE_BIENVENIDA + "\n\n" + mensaje_iniciar)
    panel_texto.configure(state="disabled")
    raiz.update_idletasks()

    # 3) Ejecuto el Pygame (bloquea aquí hasta que cierres la ventana)
    main()

    # 4) Programo la re‑habilitación 100 ms después
    raiz.after(100, habilitar_controles)
    
# Instanciamiento Tkinter
raiz = Tk()
raiz.title("Yoshi's zones")  # Titulo de la ventana
raiz.resizable(False, False)  # Bloquear el redimensionamiento de la ventana
raiz.configure(bg=COLOR_FONDO) # Color de fondo
icono = PhotoImage(file=os.path.join(BASE_DIR, "assets", "imagenes", "yoshi-verde.png")) # Asignacion de icono
raiz.iconphoto(True, icono)             
style = ttk.Style() # Estilo para el tema de la interfaz
style.theme_use("vista") # Tema de la interfaz

# Variable para manipular la dificultad seleccionada
dificultad_seleccionada = StringVar(value=dificultades[0])

# Contenedor para seleccionar dificultad
contenedor1 = LabelFrame(raiz, text="Opciones", bd=3, bg=COLOR_FONDO, fg=COLOR_TEXTO)
contenedor1.grid(row=1, column=0, columnspan=2, padx=8, pady=8, sticky="we")

# Etiqueta para el ComboBox
label_algoritmo = Label(contenedor1, text="Escoger dificultad:", bg=COLOR_FONDO, fg=COLOR_TEXTO)
label_algoritmo.grid(row=0, column=0, padx=28, pady=5, sticky="")

# Combobox de dificultades
combo_algoritmo = ttk.Combobox(contenedor1, state="readonly", width=21, textvariable=dificultad_seleccionada)
combo_algoritmo["values"] = dificultades
combo_algoritmo.grid(row=0, column=1, padx=5, pady=5)
combo_algoritmo.current(0)

# Contenedor para el panel de texto
contenedor_texto = LabelFrame(raiz, text="Reportes", bd=3, bg=COLOR_FONDO, fg=COLOR_TEXTO)
contenedor_texto.grid(row=2, column=0, columnspan=2, padx=8, pady=4, sticky="we")

# Panel de texto dentro del contenedor
panel_texto = Text(contenedor_texto, height=15, width=41, bg=COLOR_FONDO, fg=COLOR_TEXTO, wrap=WORD, font=("MS Sans Serif", 11))
panel_texto.pack(padx=5, pady=5)
panel_texto.insert(END, MENSAJE_BIENVENIDA)
panel_texto.configure(state="disabled")

# Contenedor de botones finales
contenedor3 = LabelFrame(raiz, bd=3, bg=COLOR_FONDO, fg=COLOR_TEXTO)
contenedor3.grid(row=3, column=0, columnspan=2, padx=8, pady=8, sticky="we")

boton_iniciar = Button(contenedor3, text="Iniciar", width=20, command=iniciar, bg=COLOR_BOTON, fg=COLOR_TEXTO)
boton_iniciar.grid(row=0, column=0, padx=5, pady=5)

boton_borrar = Button(contenedor3, text="Salir", width=20, command=raiz.destroy, bg=COLOR_BOTON, fg=COLOR_TEXTO)
boton_borrar.grid(row=0, column=1, padx=5, pady=5)

# Iniciar la interfaz gráfica
raiz.mainloop()