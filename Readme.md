# SpacialArm - Visualizador 3D del Brazo Robótico

## Descripción

SpacialArm es un simulador y visualizador 3D de un brazo robótico de 3 articulaciones. El proyecto proporciona una interfaz gráfica moderna para visualizar y controlar el movimiento del brazo en tiempo real usando OpenGL y PyQt5.

## Características

- **Visualización 3D en tiempo real** usando OpenGL
- **Control interactivo** de los 6 grados de libertad del brazo (3 articulaciones × 2 ángulos cada una)
- **Interfaz gráfica moderna** con PyQt5
- **Controles de vista** con rotación y zoom
- **Especificación de puntos objetivo** con cinemática inversa básica
- **Renderizado 3D** con iluminación y materiales

## Estructura del Proyecto

```
SpacialArm/
├── Arm.py              # Clase principal del brazo robótico
├── Vector.py           # Clase para manejo de vectores 3D
├── ArmSolver.py        # Solucionador de cinemática
├── GeneticSolver.py    # Solucionador genético
├── main.py             # Punto de entrada principal
├── requirements.txt    # Dependencias del proyecto
├── window/
│   ├── glWidget.py     # Widget OpenGL para visualización 3D
│   ├── mainInterface.py # Interfaz principal de la aplicación
│   └── main.ui         # Archivo de diseño de interfaz
└── Readme.md           # Este archivo
```

## Instalación

### Requisitos del Sistema

- Python 3.7 o superior
- OpenGL compatible
- Sistema operativo: Linux, Windows, macOS

### Instalación de Dependencias

```bash
pip install -r requirements.txt
```

### Dependencias Principales

- **PyOpenGL**: Renderizado 3D con OpenGL
- **PyQt5**: Interfaz gráfica de usuario
- **numpy**: Cálculos matemáticos

## Uso

### Ejecutar la Aplicación

```bash
python main.py
```

### Controles de la Interfaz

#### Controles de Vista
- **Mouse izquierdo + arrastrar**: Rotar la vista
- **Mouse derecho + arrastrar**: Zoom
- **Rueda del mouse**: Zoom
- **Botón "Reset Vista"**: Restaurar vista inicial
- **Botón "Rotación Automática"**: Activar rotación automática

#### Control del Brazo
- **Sliders de ángulos**: Controlar los ángulos theta y gamma de cada articulación
- **Rango**: -180° a +180° para cada ángulo
- **Botón "Try me"**: Resetear el brazo a posición inicial

#### Punto Objetivo
- **Campos X, Y, Z**: Especificar coordenadas del punto objetivo
- **Botón "Ir al Punto"**: Intentar mover el brazo al punto especificado

## Arquitectura del Brazo

El brazo robótico tiene 3 articulaciones principales:

1. **Articulación 1**: Base del brazo (theta1, gamma1)
2. **Articulación 2**: Codo (theta2, gamma2)  
3. **Articulación 3**: Muñeca (theta3, gamma3)

Cada articulación tiene dos grados de libertad:
- **Theta**: Ángulo en el plano XY
- **Gamma**: Ángulo de elevación

## Características Técnicas

### Visualización 3D
- Renderizado con OpenGL
- Iluminación dinámica
- Materiales y colores diferenciados por segmento
- Ejes de coordenadas de referencia

### Cinemática
- Cinemática directa implementada
- Cinemática inversa básica para puntos objetivo
- Cálculos de vectores 3D optimizados

### Interfaz de Usuario
- Diseño modular y extensible
- Controles intuitivos
- Actualización en tiempo real
- Información de estado del brazo

## Desarrollo

### Agregar Nuevas Funcionalidades

1. **Nuevos controles**: Modificar `mainInterface.py`
2. **Efectos visuales**: Extender `glWidget.py`
3. **Algoritmos de movimiento**: Implementar en `ArmSolver.py`

### Estructura de Código

- **Separación de responsabilidades**: Lógica del brazo, visualización e interfaz están separadas
- **Modularidad**: Cada componente es independiente y reutilizable
- **Extensibilidad**: Fácil agregar nuevas características

## Solución de Problemas

### Problemas Comunes

1. **Error de OpenGL**: Verificar que el sistema soporte OpenGL
2. **Dependencias faltantes**: Ejecutar `pip install -r requirements.txt`
3. **Rendimiento lento**: Reducir la frecuencia de actualización en el timer

### Compatibilidad

- **Linux**: Probado en Ubuntu 20.04+
- **Windows**: Requiere drivers de OpenGL actualizados
- **macOS**: Compatible con versiones recientes

## Licencia

Este proyecto está disponible bajo licencia de código abierto.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, asegúrate de:
1. Probar los cambios en diferentes sistemas
2. Mantener la compatibilidad con las dependencias existentes
3. Documentar nuevas funcionalidades

---

**Nota**: Este proyecto reemplazó las visualizaciones basadas en matplotlib por una interfaz OpenGL moderna y más eficiente.
