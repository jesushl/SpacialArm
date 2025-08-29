#!/bin/bash

# Script para ejecutar la ventana independiente del visualizador 3D del brazo robótico

echo "🚀 Iniciando Visualizador 3D Independiente del Brazo Robótico..."
echo "============================================================"

# Verificar que estamos en el directorio correcto
if [ ! -f "window/armVisualizer.py" ]; then
    echo "❌ Error: No se encontró el archivo armVisualizer.py"
    echo "   Asegúrate de ejecutar este script desde el directorio raíz del proyecto"
    exit 1
fi

# Verificar archivos requeridos
required_files=("Arm.py" "ImprovedGeneticSolver.py" "Vector.py")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Error: No se encontró $file"
        exit 1
    fi
done

echo "✅ Archivos del proyecto encontrados"

# Verificar si existe el ambiente virtual
if [ ! -d ".venv" ]; then
    echo "⚠️  Ambiente virtual no encontrado. Creando uno nuevo..."
    uv venv python3.12
    if [ $? -ne 0 ]; then
        echo "❌ Error al crear el ambiente virtual"
        exit 1
    fi
fi

# Activar ambiente virtual
echo "🔧 Activando ambiente virtual..."
source .venv/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ Error al activar el ambiente virtual"
    exit 1
fi

# Verificar dependencias
echo "📦 Verificando dependencias..."
python -c "import PyQt5, OpenGL, numpy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Dependencias faltantes. Instalando..."
    uv pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Error al instalar dependencias"
        exit 1
    fi
fi

echo "✅ Dependencias verificadas"

# Ejecutar el visualizador
echo "🎮 Iniciando visualizador..."
echo ""
echo "Controles:"
echo "- Mouse izquierdo: Rotar vista"
echo "- Rueda del mouse: Zoom"
echo "- Sliders: Controlar ángulos del brazo"
echo "- Campos X, Y, Z: Especificar punto objetivo"
echo "- Botón 'Visualizar Movimiento': Animar hacia el objetivo"
echo ""
echo "============================================================"

python run_visualizer.py

# Verificar si la ejecución fue exitosa
if [ $? -eq 0 ]; then
    echo "✅ Visualizador cerrado correctamente"
else
    echo "❌ Error al ejecutar el visualizador"
    exit 1
fi
