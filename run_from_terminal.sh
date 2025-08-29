#!/bin/bash

# Script para ejecutar la aplicación desde el terminal del sistema
# Evita problemas con el ambiente de Cursor

echo "🚀 Ejecutando SpacialArm desde terminal del sistema..."
echo "=================================================="

# Verificar que estamos en el directorio correcto
if [ ! -f "main.py" ]; then
    echo "❌ Error: No se encontró main.py"
    echo "   Asegúrate de ejecutar este script desde el directorio raíz del proyecto"
    exit 1
fi

# Verificar que el ambiente virtual existe
if [ ! -d ".venv" ]; then
    echo "❌ Error: Ambiente virtual no encontrado"
    echo "   Ejecuta primero: ./run.sh"
    exit 1
fi

# Activar ambiente virtual
echo "📦 Activando ambiente virtual..."
source .venv/bin/activate

# Verificar que las dependencias estén instaladas
echo "🔍 Verificando dependencias..."
if ! python -c "import PyQt5, OpenGL, numpy" 2>/dev/null; then
    echo "❌ Error: Dependencias no instaladas"
    echo "   Ejecuta: uv pip install PyOpenGL PyOpenGL_accelerate PyQt5 numpy"
    exit 1
fi

# Verificar archivos necesarios
echo "🔍 Verificando archivos del proyecto..."
required_files=("window/main.ui" "window/mainInterface.py" "window/glWidget.py" "Arm.py" "Vector.py" "ImprovedGeneticSolver.py")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Error: No se encontró el archivo $file"
        exit 1
    fi
done

echo "✅ Todos los archivos verificados"

# Ejecutar la aplicación
echo "🎮 Iniciando visualización 3D..."
echo ""
echo "Controles de la aplicación:"
echo "- Mouse izquierdo: Rotar vista"
echo "- Mouse derecho: Zoom"
echo "- Rueda del mouse: Zoom"
echo "- Sliders: Controlar ángulos del brazo"
echo "- Campos X, Y, Z: Especificar punto objetivo"
echo "- Botón 'Visualizar Movimiento': Ejecutar algoritmo genético"
echo ""

# Ejecutar con el Python del ambiente virtual
python main.py
