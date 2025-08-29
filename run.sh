#!/bin/bash

# Script para ejecutar SpacialArm con ambiente virtual uv
# Autor: SpacialArm Team

echo "🚀 Iniciando SpacialArm - Visualizador 3D del Brazo Robótico"
echo "=========================================================="

# Verificar si existe el ambiente virtual
if [ ! -d ".venv" ]; then
    echo "❌ Ambiente virtual no encontrado. Creando uno nuevo..."
    uv venv --python python3.12
fi

# Activar ambiente virtual
echo "📦 Activando ambiente virtual..."
source .venv/bin/activate

# Verificar si las dependencias están instaladas
if ! python -c "import PyQt5, OpenGL, numpy" 2>/dev/null; then
    echo "📥 Instalando dependencias..."
    uv pip install PyOpenGL PyOpenGL_accelerate PyQt5 numpy
fi

# Verificar que los archivos necesarios existen
echo "🔍 Verificando archivos del proyecto..."
required_files=("window/main.ui" "window/mainInterface.py" "window/glWidget.py" "Arm.py" "Vector.py")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Error: No se encontró el archivo $file"
        echo "   Asegúrate de ejecutar este script desde el directorio raíz del proyecto"
        exit 1
    fi
done

# Ejecutar la aplicación
echo "🎮 Iniciando visualización 3D..."
echo ""
echo "Controles de la aplicación:"
echo "- Mouse izquierdo: Rotar vista"
echo "- Mouse derecho: Zoom"
echo "- Rueda del mouse: Zoom"
echo "- Sliders: Controlar ángulos del brazo"
echo "- Campos X, Y, Z: Especificar punto objetivo"
echo ""

# Ejecutar con manejo de errores
if python main.py; then
    echo "✅ Aplicación cerrada correctamente"
else
    echo "❌ Error al ejecutar la aplicación"
    exit 1
fi
