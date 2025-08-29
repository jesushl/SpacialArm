#!/usr/bin/env python3
"""
Aplicación principal del Visualizador 3D del Brazo Robótico
Patrón MVC - Modelo-Vista-Controlador
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# Agregar directorios al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from controllers.main_controller import MainController

def main():
    """Función principal de la aplicación"""
    print("🚀 Iniciando Visualizador 3D del Brazo Robótico - MVC")
    print("=" * 60)
    print("📐 Patrón MVC implementado")
    print("🎯 Visualización 3D con OpenGL")
    print("🧬 Algoritmo genético para cinemática inversa")
    print("=" * 60)
    
    # Crear aplicación Qt
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Crear controlador principal
    controller = MainController()
    
    # Mostrar ventana
    controller.show()
    
    # Ejecutar aplicación
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
