# main.py - Punto de entrada de la aplicación

import os
import sys

# Asegura que el directorio raíz esté en el sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.join(BASE_DIR, "app")
sys.path.insert(0, APP_DIR)

try:
    from app.menu import main  # app/menu.py
except ImportError as e:
    print(f"Error al importar el menú: {e}")
    sys.exit(1)

if __name__ == "__main__":
    main()
