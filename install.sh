#!/bin/bash

echo "🚀 Instalando Visualizador 3D del Brazo Robótico - MVC"
echo "=" * 60

# Verificar si uv está instalado
if ! command -v uv &> /dev/null; then
    echo "❌ Error: uv no está instalado"
    echo "   Instala uv desde: https://docs.astral.sh/uv/getting-started/installation/"
    exit 1
fi

# Verificar si Python 3.12+ está disponible
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
if [[ $(echo "$python_version >= 3.12" | bc -l) -eq 0 ]]; then
    echo "❌ Error: Se requiere Python 3.12 o superior"
    echo "   Versión actual: $python_version"
    exit 1
fi

echo "✅ Python $python_version detectado"

# Eliminar ambiente virtual existente si existe
if [ -d ".venv" ]; then
    echo "🗑️  Eliminando ambiente virtual existente..."
    rm -rf .venv
fi

# Crear nuevo ambiente virtual
echo "🔧 Creando ambiente virtual..."
uv venv

if [ $? -ne 0 ]; then
    echo "❌ Error al crear el ambiente virtual"
    exit 1
fi

# Activar ambiente virtual
echo "🔧 Activando ambiente virtual..."
source .venv/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ Error al activar el ambiente virtual"
    exit 1
fi

# Instalar dependencias
echo "📦 Instalando dependencias..."
uv pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Error al instalar dependencias"
    exit 1
fi

# Verificar instalación
echo "🔍 Verificando instalación..."
python3 -c "
import sys
print(f'✅ Python {sys.version}')

try:
    import PyQt5
    print('✅ PyQt5 instalado correctamente')
except ImportError:
    print('❌ Error: PyQt5 no se pudo importar')
    sys.exit(1)

try:
    import OpenGL
    print('✅ OpenGL instalado correctamente')
except ImportError:
    print('❌ Error: OpenGL no se pudo importar')
    sys.exit(1)

try:
    import numpy
    print('✅ NumPy instalado correctamente')
except ImportError:
    print('❌ Error: NumPy no se pudo importar')
    sys.exit(1)

print('✅ Todas las dependencias están instaladas correctamente')
"

if [ $? -ne 0 ]; then
    echo "❌ Error en la verificación de dependencias"
    exit 1
fi

echo ""
echo "🎉 ¡Instalación completada exitosamente!"
echo ""
echo "📋 Para ejecutar la aplicación:"
echo "   source .venv/bin/activate"
echo "   python3 main.py"
echo ""
echo "🎮 Controles:"
echo "   - Mouse izquierdo: Rotar vista 3D"
echo "   - Rueda del mouse: Zoom in/out"
echo "   - Sliders: Controlar ángulos del brazo"
echo "   - Campos X, Y, Z: Especificar punto objetivo"
echo "   - Botón 'Visualizar Movimiento': Animar hacia el objetivo"
echo ""
echo "📐 Arquitectura MVC implementada:"
echo "   - models/: Lógica del brazo y algoritmo genético"
echo "   - views/: Interfaz gráfica y visualización 3D"
echo "   - controllers/: Coordinación entre modelo y vista"
echo ""
