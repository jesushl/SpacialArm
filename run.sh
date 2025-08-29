#!/bin/bash

echo "🚀 Ejecutando Visualizador 3D del Brazo Robótico - MVC"
echo "=" * 60

# Verificar si el ambiente virtual existe
if [ ! -d ".venv" ]; then
    echo "❌ Ambiente virtual no encontrado"
    echo "   Ejecuta primero: ./install.sh"
    exit 1
fi

# Activar ambiente virtual
echo "🔧 Activando ambiente virtual..."
source .venv/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ Error al activar el ambiente virtual"
    exit 1
fi

# Verificar que main.py existe
if [ ! -f "main.py" ]; then
    echo "❌ Error: No se encontró main.py"
    exit 1
fi

# Verificar estructura MVC
echo "🔍 Verificando estructura MVC..."
if [ ! -d "models" ] || [ ! -d "views" ] || [ ! -d "controllers" ]; then
    echo "❌ Error: Estructura MVC incompleta"
    echo "   Verifica que existan los directorios: models/, views/, controllers/"
    exit 1
fi

echo "✅ Estructura MVC verificada"

# Ejecutar aplicación
echo "🎯 Iniciando aplicación..."
echo ""
echo "🎮 Controles:"
echo "   - Mouse izquierdo: Rotar vista 3D"
echo "   - Rueda del mouse: Zoom in/out"
echo "   - Sliders: Controlar ángulos del brazo"
echo "   - Campos X, Y, Z: Especificar punto objetivo"
echo "   - Botón 'Visualizar Movimiento': Animar hacia el objetivo"
echo ""
echo "📐 Distribución:"
echo "   - 5/8 de la ventana: Visualización 3D (prioritaria)"
echo "   - 3/8 de la ventana: Controles e información"
echo ""
echo "=" * 60

python3 main.py
