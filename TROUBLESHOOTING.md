# Solución de Problemas - SpacialArm

## Errores Comunes y Soluciones

### ❌ Error: `FileNotFoundError: [Errno 2] No existe el archivo o el directorio: 'main.ui'`

**Causa**: El archivo `main.ui` no se encuentra en la ruta esperada.

**Solución**:
1. Verifica que estás ejecutando desde el directorio raíz del proyecto:
   ```bash
   pwd  # Debe mostrar /ruta/a/SpacialArm
   ls window/main.ui  # Debe existir este archivo
   ```

2. Usa el script automático:
   ```bash
   ./run.sh
   ```

3. O ejecuta manualmente con el ambiente activado:
   ```bash
   source .venv/bin/activate
   python main.py
   ```

### ❌ Error: `ModuleNotFoundError: No module named 'PyQt5'`

**Causa**: Las dependencias no están instaladas.

**Solución**:
```bash
# Recrear ambiente virtual
rm -rf .venv
uv venv --python python3.12
source .venv/bin/activate
uv pip install PyOpenGL PyOpenGL_accelerate PyQt5 numpy
```

### ❌ Error: `No module named 'encodings'`

**Causa**: Problema con Python 3.14 o ambiente virtual corrupto.

**Solución**:
```bash
# Usar Python 3.12 en lugar de 3.14
rm -rf .venv
uv venv --python python3.12
source .venv/bin/activate
uv pip install PyOpenGL PyOpenGL_accelerate PyQt5 numpy
```

### ❌ Error: `ImportError: No module named 'OpenGL'`

**Causa**: PyOpenGL no está instalado correctamente.

**Solución**:
```bash
source .venv/bin/activate
uv pip install --upgrade PyOpenGL PyOpenGL_accelerate
```

### ❌ Error: `Fatal Python error: Failed to import encodings module`

**Causa**: Problema con el ambiente de desarrollo (Cursor, VS Code, etc.).

**Solución**:
1. Ejecutar desde terminal del sistema (no desde el IDE):
   ```bash
   cd /home/jesus/SpacialArm
   ./run.sh
   ```

2. O usar el script Python:
   ```bash
   python run_visualization.py
   ```

### ❌ Error: `Could not find platform independent libraries`

**Causa**: Problema con la configuración de Python en el IDE.

**Solución**:
1. Usar terminal del sistema operativo
2. Verificar que el ambiente virtual esté activado:
   ```bash
   which python  # Debe mostrar .venv/bin/python
   ```

### ❌ Error: `GLXBadContext` o problemas de OpenGL

**Causa**: Problemas con drivers de OpenGL o configuración de X11.

**Solución**:
1. Verificar soporte de OpenGL:
   ```bash
   glxinfo | grep "OpenGL version"
   ```

2. En sistemas con NVIDIA:
   ```bash
   export __GL_SYNC_TO_VBLANK=0
   python main.py
   ```

3. En sistemas con Intel/AMD:
   ```bash
   export MESA_GL_VERSION_OVERRIDE=3.3
   python main.py
   ```

## Verificación del Sistema

### Comandos de Diagnóstico

```bash
# Verificar Python
python --version

# Verificar ambiente virtual
which python
echo $VIRTUAL_ENV

# Verificar dependencias
python -c "import PyQt5; print('PyQt5 OK')"
python -c "import OpenGL; print('OpenGL OK')"
python -c "import numpy; print('NumPy OK')"

# Verificar archivos del proyecto
ls -la window/
ls -la *.py
```

### Verificación de OpenGL

```bash
# Verificar versión de OpenGL
glxinfo | grep "OpenGL version"

# Verificar extensiones
glxinfo | grep "OpenGL extensions"

# Verificar renderizador
glxinfo | grep "OpenGL renderer"
```

## Configuración de Entorno

### Variables de Entorno Útiles

```bash
# Para problemas de OpenGL
export __GL_SYNC_TO_VBLANK=0
export MESA_GL_VERSION_OVERRIDE=3.3

# Para problemas de Qt
export QT_DEBUG_PLUGINS=1

# Para problemas de Python
export PYTHONPATH="${PYTHONPATH}:/ruta/a/SpacialArm"
```

### Configuración de IDE

Si usas VS Code, Cursor u otro IDE:

1. **Seleccionar intérprete correcto**:
   - Buscar: `Ctrl+Shift+P` → "Python: Select Interpreter"
   - Seleccionar: `.venv/bin/python`

2. **Configurar terminal**:
   - Usar terminal integrado del IDE
   - Activar ambiente virtual: `source .venv/bin/activate`

## Recuperación Completa

Si nada funciona, recrea todo el proyecto:

```bash
# 1. Limpiar todo
rm -rf .venv
rm -f uv.lock

# 2. Recrear ambiente
uv venv --python python3.12
source .venv/bin/activate

# 3. Instalar dependencias
uv pip install PyOpenGL PyOpenGL_accelerate PyQt5 numpy

# 4. Generar lock file
uv lock

# 5. Ejecutar
python main.py
```

## Contacto y Soporte

Si los problemas persisten:

1. Verificar la versión del sistema operativo
2. Verificar la versión de Python (recomendado 3.12)
3. Verificar que uv esté actualizado: `uv --version`
4. Revisar logs del sistema: `journalctl -f`

---

**Nota**: La mayoría de problemas se resuelven usando Python 3.12 en lugar de 3.14 y ejecutando desde terminal del sistema operativo.
