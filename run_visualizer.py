#!/usr/bin/env python3
"""
Script para ejecutar la ventana independiente del visualizador 3D del brazo robótico
"""

import sys
import os

def main():
    """Función principal"""
    print("🚀 Iniciando Visualizador 3D Independiente del Brazo Robótico...")
    print("=" * 60)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("window/armVisualizer.py"):
        print("❌ Error: No se encontró el archivo armVisualizer.py")
        print("   Asegúrate de ejecutar este script desde el directorio raíz del proyecto")
        return False
    
    # Verificar dependencias
    required_files = [
        "Arm.py",
        "ImprovedGeneticSolver.py",
        "Vector.py"
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Error: No se encontró {file}")
            return False
    
    print("✅ Archivos del proyecto encontrados")
    
    try:
        # Agregar el directorio actual al path
        sys.path.insert(0, os.getcwd())
        
        # Importar y ejecutar el visualizador
        from window.armVisualizer import main as visualizer_main
        print("✅ Visualizador cargado correctamente")
        print("\n🎮 Controles:")
        print("- Mouse izquierdo: Rotar vista")
        print("- Rueda del mouse: Zoom")
        print("- Sliders: Controlar ángulos del brazo")
        print("- Campos X, Y, Z: Especificar punto objetivo")
        print("- Botón 'Visualizar Movimiento': Animar hacia el objetivo")
        print("\n" + "=" * 60)
        
        # Ejecutar la aplicación
        visualizer_main()
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
