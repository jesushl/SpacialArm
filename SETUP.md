# Configuración del Ambiente SpacialArm con uv

## Requisitos Previos

- **uv**: Gestor de paquetes Python moderno
- **Python 3.12**: Versión estable de Python
- **Sistema operativo**: Linux, Windows, macOS

## Instalación Rápida

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd SpacialArm
```

### 2. Ejecutar con script automático
```bash
chmod +x run.sh
./run.sh
```

## Instalación Manual

### 1. Crear ambiente virtual
```bash
uv venv --python python3.12
```

### 2. Activar ambiente virtual
```bash
source .venv/bin/activate
```

### 3. Instalar dependencias
```bash
uv pip install PyOpenGL PyOpenGL_accelerate PyQt5 numpy
```

### 4. Ejecutar aplicación
```bash
python main.py
```

## Estructura de Archivos

```
SpacialArm/
├── pyproject.toml      # Configuración del proyecto para uv
├── requirements.txt    # Dependencias (alternativo)
├── run.sh             # Script de ejecución automática
├── main.py            # Punto de entrada principal
├── uv.lock            # Archivo de lock de dependencias
└── window/            # Módulos de la interfaz gráfica
```

## Dependencias Principales

- **PyOpenGL**: Renderizado 3D con OpenGL
- **PyQt5**: Interfaz gráfica de usuario
- **numpy**: Cálculos matemáticos

## Comandos Útiles

### Generar archivo de lock
```bash
uv lock
```

### Instalar dependencias de desarrollo
```bash
uv pip install -e ".[dev]"
```

### Actualizar dependencias
```bash
uv pip install --upgrade PyOpenGL PyQt5 numpy
```

### Verificar instalación
```bash
python -c "import PyQt5, OpenGL, numpy; print('✅ Todas las dependencias instaladas correctamente')"
```

## Solución de Problemas

### Error de Python 3.14
Si tienes problemas con Python 3.14, usa Python 3.12:
```bash
uv venv --python python3.12
```

### Error de dependencias
Si hay problemas con las dependencias:
```bash
rm -rf .venv
uv venv --python python3.12
source .venv/bin/activate
uv pip install PyOpenGL PyOpenGL_accelerate PyQt5 numpy
```

### Error de OpenGL
Verificar que el sistema soporte OpenGL:
```bash
glxinfo | grep "OpenGL version"
```

## Desarrollo

### Agregar nuevas dependencias
1. Editar `pyproject.toml`
2. Ejecutar `uv lock`
3. Instalar con `uv pip install`

### Ambiente de desarrollo
```bash
uv pip install -e ".[dev]"
```

## Notas

- El proyecto usa **uv** como gestor de paquetes principal
- **Python 3.12** es la versión recomendada para estabilidad
- El script `run.sh` automatiza todo el proceso de setup
- Las dependencias están optimizadas para rendimiento 3D
