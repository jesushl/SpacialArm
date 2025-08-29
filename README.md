# Visualizador 3D del Brazo Robótico - MVC

Aplicación de visualización 3D de un brazo robótico implementada con el patrón MVC (Modelo-Vista-Controlador).

## 🏗️ Estructura del Proyecto

```
SpacialArm/
├── models/                 # Modelos (lógica de negocio)
│   ├── __init__.py
│   ├── arm_model.py       # Modelo del brazo robótico
│   └── genetic_solver.py  # Solver genético para cinemática inversa
├── views/                  # Vistas (interfaz de usuario)
│   ├── __init__.py
│   ├── gl_widget.py       # Widget OpenGL para visualización 3D
│   └── main_window.py     # Ventana principal
├── controllers/            # Controladores (coordinación)
│   ├── __init__.py
│   └── main_controller.py # Controlador principal
├── utils/                  # Utilidades (futuras extensiones)
├── main.py                # Punto de entrada de la aplicación
├── requirements.txt       # Dependencias
└── README.md             # Este archivo
```

## 🎯 Características

- **Patrón MVC**: Separación clara de responsabilidades
- **Visualización 3D**: Renderizado con OpenGL
- **Algoritmo Genético**: Cinemática inversa optimizada
- **Interfaz Moderna**: PyQt5 con controles intuitivos
- **Threading**: Algoritmos genéticos sin bloquear la UI

## 🚀 Instalación

1. **Crear ambiente virtual**:
   ```bash
   uv venv
   source .venv/bin/activate
   ```

2. **Instalar dependencias**:
   ```bash
   uv pip install -r requirements.txt
   ```

3. **Ejecutar aplicación**:
   ```bash
   python main.py
   ```

## 🎮 Controles

- **Mouse izquierdo**: Rotar vista 3D
- **Rueda del mouse**: Zoom in/out
- **Sliders**: Controlar ángulos del brazo
- **Campos X, Y, Z**: Especificar punto objetivo
- **Botón "Visualizar Movimiento"**: Animar hacia el objetivo

## 📐 Arquitectura MVC

### Modelo (models/)
- **ArmModel**: Lógica del brazo robótico, cálculos de cinemática
- **GeneticSolver**: Algoritmo genético para cinemática inversa

### Vista (views/)
- **MainWindow**: Interfaz principal con controles
- **ArmGLWidget**: Widget OpenGL para visualización 3D

### Controlador (controllers/)
- **MainController**: Coordina modelo y vista, maneja eventos

## 🧬 Algoritmo Genético

El solver genético implementa:
- **Población**: 100 individuos
- **Generaciones**: 200 máximo
- **Selección**: Torneo
- **Cruce**: Uniforme
- **Mutación**: Gaussiana
- **Elitismo**: Mantiene los mejores individuos

## 🎨 Visualización 3D

- **Ejes de coordenadas**: X (rojo), Y (verde), Z (azul)
- **Brazo robótico**: Segmentos azules, articulaciones amarillas
- **Efector final**: Esfera roja
- **Objetivo**: Esfera verde con línea punteada

## 🔧 Tecnologías

- **Python 3.12+**
- **PyQt5**: Interfaz gráfica
- **OpenGL**: Renderizado 3D
- **NumPy**: Cálculos matemáticos
- **uv**: Gestión de dependencias

## 📝 Licencia

Este proyecto está bajo licencia MIT.
