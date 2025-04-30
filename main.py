# Ejecutable principal para la aplicación
import os
import sys

# Asegura que el directorio de la aplicación está en el path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.interfaz.menu import raiz

    if __name__ == "__main__": 
        raiz.mainloop()
    
except ImportError as e:
    print(f"Error al importar la interfaz: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Error al iniciar la aplicación: {e}")
    sys.exit(1)