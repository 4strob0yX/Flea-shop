COLOR_FONDO = "#f9f9f9"
COLOR_TEXTO = "#000000"
COLOR_VERDE_CLARO = "#6ab04c"
COLOR_VERDE_OSCURO = "#218c74"
COLOR_ROJO = "#eb4d4b"

FONT_TITLE = ("Arial", 24, "bold")
FONT_SUBTITLE = ("Arial", 18, "bold")
FONT_BODY = ("Arial", 12)
FONT_BODY_BOLD = ("Arial", 12, "bold")
FONT_LABEL = ("Arial", 11)
FONT_HEADER = ("Arial", 18, "bold")

# Nueva función para aplicar estilos globales
import tkinter.ttk as ttk

def aplicar_estilos():
    style = ttk.Style()
    style.configure("Header.TButton",
                    font=FONT_BODY_BOLD,
                    background=COLOR_VERDE_OSCURO,
                    foreground="white",
                    padding=6)
    style.map("Header.TButton",
              background=[("active", COLOR_VERDE_CLARO)])

    style.configure("Modern.TButton",
                    font=FONT_BODY_BOLD,
                    background=COLOR_VERDE_CLARO,
                    foreground="white",
                    relief="flat",
                    padding=6)
    style.map("Modern.TButton",
              background=[("active", COLOR_VERDE_OSCURO)])
