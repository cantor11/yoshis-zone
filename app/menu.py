# app/interfaz/menu.py

from tkinter import *
from tkinter import ttk, messagebox, PhotoImage
import os
from tablero import main as run_game

# Valores de configuración en la interfaz
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COLOR_FONDO = "#303030"
COLOR_BOTON  = "#606060"
COLOR_TEXTO  = "#FFFFFF"
MENSAJE_BIENVENIDA = """Bienvenido a Yoshi's zones, para jugar selecciona una dificultad y luego dale al botón iniciar.\n
El Yoshi que marque más zonas especiales con su color, gana.\n
Solo se permiten movimientos en "L" como la pieza del caballo en ajedrez.\n"""

# Definición de las dificultades
dificultades = ["...", "Principiante", "Amateur", "Experto"]
            
def habilitar_controles():
    boton_iniciar.config(state=NORMAL)
    boton_borrar.config(state=NORMAL)
    combo_dificultad.config(state="readonly")

def iniciar():
    dificultad = dificultad_seleccionada.get()
    # Validar que se haya seleccionado una dificultad
    if dificultad == "...":
        messagebox.showerror("Error", "Debe seleccionar una dificultad antes de iniciar.")
        return

    # 1) Deshabilitar controles
    boton_iniciar.config(state=DISABLED)
    boton_borrar.config(state=DISABLED)
    combo_dificultad.config(state=DISABLED)

    # 2) Actualizar mensaje en el panel
    panel_texto.configure(state="normal")
    panel_texto.delete("1.0", END)
    panel_texto.insert(END, MENSAJE_BIENVENIDA + f"\nIniciando dificultad: {dificultad}...\n")
    panel_texto.configure(state="disabled")
    raiz.update_idletasks()

    try:
        v, r, winner = run_game(dificultad)

        panel_texto.configure(state="normal")
        if winner == "Empate":
            panel_texto.insert(END, f"\nFin de la partida → Verde: {v}  Rojo: {r}\n  ¡{winner}!\n")
        else:
            panel_texto.insert(END, f"\nFin de la partida → Verde: {v}  Rojo: {r}\n  ¡{winner} gana!\n")
        panel_texto.configure(state="disabled")

    except Exception as e:
        messagebox.showerror("Error", f"Se abortó la partida. No hay resultado.")

    raiz.after(100, habilitar_controles)


def main():
    global raiz, combo_dificultad, dificultad_seleccionada
    global boton_iniciar, boton_borrar, panel_texto

    raiz = Tk()
    raiz.title("Yoshi's zones")
    raiz.resizable(False, False)
    raiz.configure(bg=COLOR_FONDO)

    # Icono de la ventana
    icono_path = os.path.join(BASE_DIR, "assets", "imagenes", "yoshi-verde.png")
    icono = PhotoImage(file=icono_path)
    raiz.iconphoto(True, icono)

    style = ttk.Style()
    style.theme_use("vista")

    # Variable para la dificultad
    dificultad_seleccionada = StringVar(value=dificultades[0])

    # Contenedor de opciones
    cont_opts = LabelFrame(raiz, text="Opciones", bd=3, bg=COLOR_FONDO, fg=COLOR_TEXTO)
    cont_opts.grid(row=0, column=0, columnspan=2, padx=8, pady=8, sticky="we")

    Label(cont_opts, text="Escoger dificultad:", bg=COLOR_FONDO, fg=COLOR_TEXTO) \
        .grid(row=0, column=0, padx=28, pady=5, sticky="w")

    combo_dificultad = ttk.Combobox(
        cont_opts, state="readonly", width=20, textvariable=dificultad_seleccionada
    )
    combo_dificultad["values"] = dificultades
    combo_dificultad.current(0)
    combo_dificultad.grid(row=0, column=1, padx=5, pady=5)

    # Contenedor de reportes
    cont_rep = LabelFrame(raiz, text="Reportes", bd=3, bg=COLOR_FONDO, fg=COLOR_TEXTO)
    cont_rep.grid(row=1, column=0, columnspan=2, padx=8, pady=4, sticky="we")

    panel_texto = Text(
        cont_rep, height=17, width=41,
        bg=COLOR_FONDO, fg=COLOR_TEXTO,
        wrap=WORD, font=("MS Sans Serif", 11)
    )
    panel_texto.pack(padx=5, pady=5)
    panel_texto.insert(END, MENSAJE_BIENVENIDA)
    panel_texto.configure(state="disabled")

    # Contenedor de botones
    cont_bot = LabelFrame(raiz, bd=3, bg=COLOR_FONDO, fg=COLOR_TEXTO)
    cont_bot.grid(row=2, column=0, columnspan=2, padx=8, pady=8, sticky="we")

    boton_iniciar = Button(
        cont_bot, text="Iniciar", width=20,
        command=iniciar, bg=COLOR_BOTON, fg=COLOR_TEXTO
    )
    boton_iniciar.grid(row=0, column=0, padx=5, pady=5)

    boton_borrar = Button(
        cont_bot, text="Salir", width=20,
        command=raiz.destroy, bg=COLOR_BOTON, fg=COLOR_TEXTO
    )
    boton_borrar.grid(row=0, column=1, padx=5, pady=5)

    raiz.mainloop()


if __name__ == "__main__":
    main()
