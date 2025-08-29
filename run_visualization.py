#!/usr/bin/env python3
"""
Script para ejecutar la visualización 3D del brazo robótico
Maneja automáticamente las rutas y dependencias
"""

import sys
import os
import subprocess

def main():
    # Obtener el directorio del script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Cambiar al directorio del proyecto
    os.chdir(script_dir)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("window/main.ui"):
        print("❌ Error: No se encontró el archivo window/main.ui")
        print("   Asegúrate de ejecutar este script desde el directorio raíz del proyecto")
        return 1
    
    # Verificar que el ambiente virtual existe
    if not os.path.exists(".venv"):
        print("❌ Error: Ambiente virtual no encontrado")
        print("   Ejecuta primero: ./run.sh")
        return 1
    
    # Activar ambiente virtual y ejecutar
    try:
        # En sistemas Unix/Linux
        if os.name == 'posix':
            activate_script = os.path.join(script_dir, ".venv", "bin", "activate")
            if os.path.exists(activate_script):
                # Usar subprocess para ejecutar con el ambiente activado
                cmd = f"source {activate_script} && python main.py"
                subprocess.run(cmd, shell=True, executable="/bin/bash")
            else:
                print("❌ Error: No se encontró el script de activación del ambiente virtual")
                return 1
        else:
            # En Windows
            activate_script = os.path.join(script_dir, ".venv", "Scripts", "activate.bat")
            if os.path.exists(activate_script):
                cmd = f"{activate_script} && python main.py"
                subprocess.run(cmd, shell=True)
            else:
                print("❌ Error: No se encontró el script de activación del ambiente virtual")
                return 1
                
    except Exception as e:
        print(f"❌ Error al ejecutar la aplicación: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
