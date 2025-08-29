#!/usr/bin/env python3
"""
Aplicación principal del Visualizador 3D del Brazo Robótico SpacialArm
Interfaz completamente programática con distribución 5:3
"""

import sys
import os

def main():
    """Función principal de la aplicación"""
    print("🚀 Iniciando Visualizador 3D del Brazo Robótico...")
    print("=" * 60)
    print("📐 Distribución 5:3 - Visualización prioritaria")
    print("=" * 60)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("window/mainInterface.py"):
        print("❌ Error: No se encontró el archivo mainInterface.py")
        print("   Asegúrate de ejecutar este script desde el directorio raíz del proyecto")
        return False
    
    # Verificar archivos requeridos
    required_files = [
        "Arm.py",
        "ImprovedGeneticSolver.py", 
        "Vector.py",
        "window/glWidget.py"
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Error: No se encontró {file}")
            return False
    
    print("✅ Archivos del proyecto encontrados")
    
    try:
        # Agregar el directorio actual al path
        sys.path.insert(0, os.getcwd())
        
        # Importar la interfaz principal
        from window.mainInterface import main as interface_main
        print("✅ Interfaz cargada correctamente")
        print("\n🎮 Controles:")
        print("- Mouse izquierdo: Rotar vista 3D")
        print("- Rueda del mouse: Zoom in/out")
        print("- Sliders: Controlar ángulos del brazo")
        print("- Campos X, Y, Z: Especificar punto objetivo")
        print("- Botón 'Visualizar Movimiento': Animar hacia el objetivo")
        print("\n📐 Distribución:")
        print("- 5/8 de la ventana: Visualización 3D (prioritaria)")
        print("- 3/8 de la ventana: Controles e información")
        print("\n" + "=" * 60)
        
        # Ejecutar la aplicación
        interface_main()
        return True
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("   Verifica que todas las dependencias estén instaladas:")
        print("   source .venv/bin/activate")
        print("   uv pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
