#!/usr/bin/env python3
"""
Ventana independiente para visualización 3D del brazo robótico
"""

import sys
import os
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QPushButton, QLabel, QSlider, QGroupBox, 
                             QGridLayout, QLineEdit, QMessageBox)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt5.QtGui import QFont
import OpenGL.GL as gl
import OpenGL.GLU as glu
from PyQt5.QtOpenGL import QOpenGLWidget

# Agregar el directorio padre al path para importar los módulos del proyecto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Arm import Arm
from ImprovedGeneticSolver import ImprovedGeneticSolver

class ArmGLWidget(QOpenGLWidget):
    """Widget OpenGL para renderizar el brazo robótico"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.arm = None
        self.rotation_x = 0
        self.rotation_y = 0
        self.zoom = -15
        self.last_pos = None
        self.target_point = None
        
        # Timer para actualización continua
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(16)  # ~60 FPS
        
        # Configurar el widget
        self.setFocusPolicy(Qt.StrongFocus)
        self.setMinimumSize(600, 400)
        
    def set_arm(self, arm):
        """Establecer el brazo a visualizar"""
        self.arm = arm
        self.update()
        
    def set_target_point(self, x, y, z):
        """Establecer punto objetivo para visualizar"""
        self.target_point = (x, y, z)
        self.update()
        
    def initializeGL(self):
        """Inicializar OpenGL"""
        gl.glClearColor(0.1, 0.1, 0.1, 1.0)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_LIGHTING)
        gl.glEnable(gl.GL_LIGHT0)
        gl.glEnable(gl.GL_COLOR_MATERIAL)
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, [1, 1, 1, 0])
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_AMBIENT, [0.2, 0.2, 0.2, 1])
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE, [0.8, 0.8, 0.8, 1])
        
    def resizeGL(self, width, height):
        """Manejar cambio de tamaño"""
        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluPerspective(45, width / height, 0.1, 100.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        
    def paintGL(self):
        """Renderizar la escena"""
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glLoadIdentity()
        
        # Posicionar cámara
        gl.glTranslatef(0.0, 0.0, self.zoom)
        gl.glRotatef(self.rotation_x, 1.0, 0.0, 0.0)
        gl.glRotatef(self.rotation_y, 0.0, 1.0, 0.0)
        
        # Dibujar ejes de coordenadas
        self.draw_coordinate_axes()
        
        # Dibujar brazo si existe
        if self.arm:
            self.draw_arm()
            
        # Dibujar punto objetivo si existe
        if self.target_point:
            self.draw_target_point()
            
    def draw_coordinate_axes(self):
        """Dibujar ejes de coordenadas"""
        gl.glDisable(gl.GL_LIGHTING)
        gl.glBegin(gl.GL_LINES)
        
        # Eje X (rojo)
        gl.glColor3f(1.0, 0.0, 0.0)
        gl.glVertex3f(0, 0, 0)
        gl.glVertex3f(5, 0, 0)
        
        # Eje Y (verde)
        gl.glColor3f(0.0, 1.0, 0.0)
        gl.glVertex3f(0, 0, 0)
        gl.glVertex3f(0, 5, 0)
        
        # Eje Z (azul)
        gl.glColor3f(0.0, 0.0, 1.0)
        gl.glVertex3f(0, 0, 0)
        gl.glVertex3f(0, 0, 5)
        
        gl.glEnd()
        gl.glEnable(gl.GL_LIGHTING)
        
    def draw_arm(self):
        """Dibujar el brazo robótico"""
        if not self.arm:
            return
            
        # Obtener puntos del brazo
        arm_points = self.arm.getArmPoints()
        
        if not arm_points:
            return
            
        # Dibujar base
        gl.glColor3f(0.5, 0.5, 0.5)
        self.draw_sphere(0, 0, 0, 0.3)
        
        # Dibujar segmentos del brazo
        for i, point in enumerate(arm_points):
            if i == 0:
                # Primer segmento desde la base
                prev_point = (0, 0, 0)
            else:
                prev_point = arm_points[i-1]
                
            # Dibujar segmento
            gl.glColor3f(0.2, 0.6, 1.0)
            self.draw_segment(prev_point, point)
            
            # Dibujar articulación
            gl.glColor3f(1.0, 0.8, 0.0)
            self.draw_sphere(point[0], point[1], point[2], 0.2)
            
        # Dibujar efector final
        final_point = self.arm.getArmFinalPoint()
        gl.glColor3f(1.0, 0.0, 0.0)
        self.draw_sphere(final_point['x'], final_point['y'], final_point['z'], 0.25)
        
    def draw_segment(self, start, end):
        """Dibujar un segmento del brazo"""
        gl.glDisable(gl.GL_LIGHTING)
        gl.glBegin(gl.GL_LINES)
        gl.glVertex3f(start[0], start[1], start[2])
        gl.glVertex3f(end[0], end[1], end[2])
        gl.glEnd()
        gl.glEnable(gl.GL_LIGHTING)
        
    def draw_sphere(self, x, y, z, radius):
        """Dibujar una esfera en la posición especificada"""
        gl.glPushMatrix()
        gl.glTranslatef(x, y, z)
        quad = glu.gluNewQuadric()
        glu.gluSphere(quad, radius, 16, 16)
        glu.gluDeleteQuadric(quad)
        gl.glPopMatrix()
        
    def draw_target_point(self):
        """Dibujar punto objetivo"""
        if not self.target_point:
            return
            
        x, y, z = self.target_point
        gl.glColor3f(0.0, 1.0, 0.0)
        self.draw_sphere(x, y, z, 0.3)
        
        # Dibujar línea punteada desde el origen
        gl.glDisable(gl.GL_LIGHTING)
        gl.glEnable(gl.GL_LINE_STIPPLE)
        gl.glLineStipple(2, 0xAAAA)
        gl.glBegin(gl.GL_LINES)
        gl.glVertex3f(0, 0, 0)
        gl.glVertex3f(x, y, z)
        gl.glEnd()
        gl.glDisable(gl.GL_LINE_STIPPLE)
        gl.glEnable(gl.GL_LIGHTING)
        
    def mousePressEvent(self, event):
        """Manejar clic del mouse"""
        self.last_pos = event.pos()
        
    def mouseMoveEvent(self, event):
        """Manejar movimiento del mouse"""
        if self.last_pos is None:
            return
            
        dx = event.x() - self.last_pos.x()
        dy = event.y() - self.last_pos.y()
        
        if event.buttons() & Qt.LeftButton:
            self.rotation_y += dx
            self.rotation_x += dy
            self.update()
            
        self.last_pos = event.pos()
        
    def wheelEvent(self, event):
        """Manejar rueda del mouse para zoom"""
        delta = event.angleDelta().y()
        self.zoom += delta / 120.0
        self.zoom = max(-30, min(-5, self.zoom))
        self.update()
        
    def reset_view(self):
        """Resetear vista a posición inicial"""
        self.rotation_x = 0
        self.rotation_y = 0
        self.zoom = -15
        self.update()

class AnimationThread(QThread):
    """Thread para ejecutar el algoritmo genético sin bloquear la UI"""
    progress = pyqtSignal(dict)
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, arm_solver, target_point):
        super().__init__()
        self.arm_solver = arm_solver
        self.target_point = target_point
        self.is_running = True
        
    def run(self):
        """Ejecutar algoritmo genético"""
        try:
            solution = self.arm_solver.solve_with_animation(
                callback=lambda sol, fit, gen: self.progress.emit(sol)
            )
            if solution:
                self.finished.emit(solution)
            else:
                self.error.emit("No se encontró solución para el punto objetivo")
        except Exception as e:
            self.error.emit(f"Error en algoritmo genético: {str(e)}")

class ArmVisualizerWindow(QMainWindow):
    """Ventana principal para visualización del brazo"""
    
    def __init__(self):
        super().__init__()
        self.arm = None
        self.animation_thread = None
        self.init_ui()
        self.init_arm()
        
    def init_ui(self):
        """Inicializar interfaz de usuario"""
        self.setWindowTitle("Visualizador 3D del Brazo Robótico - SpacialArm")
        self.setGeometry(100, 100, 1400, 900)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        
        # Widget OpenGL para visualización
        self.gl_widget = ArmGLWidget()
        main_layout.addWidget(self.gl_widget)
        
        # Layout para controles
        controls_layout = QHBoxLayout()
        main_layout.addLayout(controls_layout)
        
        # Grupo: Punto Objetivo
        target_group = QGroupBox("Punto Objetivo")
        target_layout = QVBoxLayout(target_group)
        
        # Grid para coordenadas
        coord_grid = QGridLayout()
        self.x_input = QLineEdit("2.0")
        self.y_input = QLineEdit("1.0")
        self.z_input = QLineEdit("2.0")
        
        coord_grid.addWidget(QLabel("X:"), 0, 0)
        coord_grid.addWidget(self.x_input, 0, 1)
        coord_grid.addWidget(QLabel("Y:"), 1, 0)
        coord_grid.addWidget(self.y_input, 1, 1)
        coord_grid.addWidget(QLabel("Z:"), 2, 0)
        coord_grid.addWidget(self.z_input, 2, 1)
        
        target_layout.addLayout(coord_grid)
        
        # Botón de visualización
        self.visualize_btn = QPushButton("Visualizar Movimiento")
        self.visualize_btn.clicked.connect(self.start_visualization)
        target_layout.addWidget(self.visualize_btn)
        
        controls_layout.addWidget(target_group)
        
        # Grupo: Control de Ángulos
        angle_group = QGroupBox("Control de Ángulos")
        angle_layout = QVBoxLayout(angle_group)
        
        # Sliders para los 6 ángulos
        self.angle_sliders = {}
        self.angle_labels = {}
        
        angles = [
            ('theta1', 'Θ₁', -180, 180),
            ('gamma1', 'γ₁', -180, 180),
            ('theta2', 'Θ₂', -180, 180),
            ('gamma2', 'γ₂', -180, 180),
            ('theta3', 'Θ₃', -180, 180),
            ('gamma3', 'γ₃', -180, 180)
        ]
        
        for angle_name, angle_symbol, min_val, max_val in angles:
            slider_layout = QHBoxLayout()
            
            # Etiqueta del ángulo
            label = QLabel(f"{angle_symbol}:")
            slider_layout.addWidget(label)
            
            # Slider
            slider = QSlider(Qt.Horizontal)
            slider.setRange(min_val, max_val)
            slider.setValue(0)
            slider.valueChanged.connect(self.update_arm_angles)
            self.angle_sliders[angle_name] = slider
            slider_layout.addWidget(slider)
            
            # Etiqueta de valor
            value_label = QLabel("0°")
            self.angle_labels[angle_name] = value_label
            slider_layout.addWidget(value_label)
            
            angle_layout.addLayout(slider_layout)
            
        controls_layout.addWidget(angle_group)
        
        # Grupo: Información
        info_group = QGroupBox("Información")
        info_layout = QVBoxLayout(info_group)
        
        self.current_pos_label = QLabel("Posición actual: (0.00, 0.00, 0.00)")
        self.target_pos_label = QLabel("Objetivo: (2.00, 1.00, 2.00)")
        self.distance_label = QLabel("Distancia: 0.00")
        self.status_label = QLabel("Estado: Listo")
        
        info_layout.addWidget(self.current_pos_label)
        info_layout.addWidget(self.target_pos_label)
        info_layout.addWidget(self.distance_label)
        info_layout.addWidget(self.status_label)
        
        # Botones de control
        reset_arm_btn = QPushButton("Reset Brazo")
        reset_arm_btn.clicked.connect(self.reset_arm)
        info_layout.addWidget(reset_arm_btn)
        
        reset_view_btn = QPushButton("Reset Vista")
        reset_view_btn.clicked.connect(self.gl_widget.reset_view)
        info_layout.addWidget(reset_view_btn)
        
        controls_layout.addWidget(info_group)
        
        # Conectar señales
        self.x_input.textChanged.connect(self.update_target_info)
        self.y_input.textChanged.connect(self.update_target_info)
        self.z_input.textChanged.connect(self.update_target_info)
        
        # Actualizar información inicial
        self.update_target_info()
        
    def init_arm(self):
        """Inicializar el brazo robótico"""
        try:
            self.arm = Arm(3.0, 2.5, 2.0)
            self.gl_widget.set_arm(self.arm)
            self.initialize_arm_on_axes()
            self.update_info_display()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al inicializar el brazo: {str(e)}")
            
    def initialize_arm_on_axes(self):
        """Inicializar el brazo sobre los ejes X, Y, Z"""
        try:
            # Configurar ángulos iniciales para que el brazo esté sobre los ejes
            self.arm.actualizeArm(
                {'gama': 90, 'theta': 0},   # Primer segmento
                {'gama': 0, 'theta': 0},    # Segundo segmento
                {'gama': 0, 'theta': 0}     # Tercer segmento
            )
            
            # Actualizar sliders
            self.angle_sliders['gamma1'].setValue(90)
            self.angle_sliders['theta1'].setValue(0)
            self.angle_sliders['gamma2'].setValue(0)
            self.angle_sliders['theta2'].setValue(0)
            self.angle_sliders['gamma3'].setValue(0)
            self.angle_sliders['theta3'].setValue(0)
            
            self.update_info_display()
            
        except Exception as e:
            QMessageBox.warning(self, "Advertencia", f"Error al inicializar posición: {str(e)}")
            
    def update_arm_angles(self):
        """Actualizar ángulos del brazo basado en los sliders"""
        try:
            if not self.arm:
                return
                
            # Obtener valores de los sliders
            gamma1 = self.angle_sliders['gamma1'].value()
            theta1 = self.angle_sliders['theta1'].value()
            gamma2 = self.angle_sliders['gamma2'].value()
            theta2 = self.angle_sliders['theta2'].value()
            gamma3 = self.angle_sliders['gamma3'].value()
            theta3 = self.angle_sliders['theta3'].value()
            
            # Actualizar etiquetas
            self.angle_labels['gamma1'].setText(f"{gamma1}°")
            self.angle_labels['theta1'].setText(f"{theta1}°")
            self.angle_labels['gamma2'].setText(f"{gamma2}°")
            self.angle_labels['theta2'].setText(f"{theta2}°")
            self.angle_labels['gamma3'].setText(f"{gamma3}°")
            self.angle_labels['theta3'].setText(f"{theta3}°")
            
            # Actualizar brazo
            self.arm.actualizeArm(
                {'gama': gamma1, 'theta': theta1},
                {'gama': gamma2, 'theta': theta2},
                {'gama': gamma3, 'theta': theta3}
            )
            
            self.update_info_display()
            
        except Exception as e:
            self.status_label.setText(f"Estado: Error - {str(e)}")
            
    def update_target_info(self):
        """Actualizar información del punto objetivo"""
        try:
            x = float(self.x_input.text() or "0")
            y = float(self.y_input.text() or "0")
            z = float(self.z_input.text() or "0")
            
            self.target_pos_label.setText(f"Objetivo: ({x:.2f}, {y:.2f}, {z:.2f})")
            
            # Actualizar punto objetivo en visualización
            self.gl_widget.set_target_point(x, y, z)
            
            # Calcular distancia si el brazo existe
            if self.arm:
                final_pos = self.arm.getArmFinalPoint()
                distance = ((final_pos['x'] - x)**2 + (final_pos['y'] - y)**2 + (final_pos['z'] - z)**2)**0.5
                self.distance_label.setText(f"Distancia: {distance:.2f}")
                
        except ValueError:
            self.target_pos_label.setText("Objetivo: (inválido)")
            self.distance_label.setText("Distancia: N/A")
            
    def update_info_display(self):
        """Actualizar toda la información mostrada"""
        if not self.arm:
            return
            
        try:
            final_pos = self.arm.getArmFinalPoint()
            self.current_pos_label.setText(f"Posición actual: ({final_pos['x']:.2f}, {final_pos['y']:.2f}, {final_pos['z']:.2f})")
            
            # Actualizar distancia
            try:
                x = float(self.x_input.text() or "0")
                y = float(self.y_input.text() or "0")
                z = float(self.z_input.text() or "0")
                distance = ((final_pos['x'] - x)**2 + (final_pos['y'] - y)**2 + (final_pos['z'] - z)**2)**0.5
                self.distance_label.setText(f"Distancia: {distance:.2f}")
            except ValueError:
                self.distance_label.setText("Distancia: N/A")
                
        except Exception as e:
            self.current_pos_label.setText("Posición actual: Error")
            self.distance_label.setText("Distancia: Error")
            
    def start_visualization(self):
        """Iniciar visualización del movimiento hacia el punto objetivo"""
        try:
            x = float(self.x_input.text() or "0")
            y = float(self.y_input.text() or "0")
            z = float(self.z_input.text() or "0")
            target_point = {'x': x, 'y': y, 'z': z}
            
            # Crear solver genético
            arm_solver = ImprovedGeneticSolver(
                arm1Len=3.0, arm2Len=2.5, arm3Len=2.0, goalPoint=target_point
            )
            
            # Verificar si el punto es alcanzable
            if not arm_solver.is_possible_shot():
                self.status_label.setText("Estado: Punto fuera del alcance")
                QMessageBox.warning(self, "Advertencia", "El punto objetivo está fuera del alcance del brazo")
                return
                
            self.status_label.setText("Estado: Calculando movimiento...")
            self.visualize_btn.setEnabled(False)
            
            # Crear y ejecutar thread de animación
            self.animation_thread = AnimationThread(arm_solver, target_point)
            self.animation_thread.progress.connect(self.update_animation_progress)
            self.animation_thread.finished.connect(self.animation_finished)
            self.animation_thread.error.connect(self.animation_error)
            self.animation_thread.start()
            
        except ValueError:
            self.status_label.setText("Estado: Valores inválidos")
            QMessageBox.warning(self, "Error", "Por favor ingresa valores numéricos válidos")
        except Exception as e:
            self.status_label.setText(f"Estado: Error - {str(e)}")
            QMessageBox.critical(self, "Error", f"Error al iniciar visualización: {str(e)}")
            
    def update_animation_progress(self, solution):
        """Actualizar progreso de la animación"""
        try:
            # Actualizar ángulos del brazo
            gamma1 = solution.get('gamma1', 0)
            theta1 = solution.get('theta1', 0)
            gamma2 = solution.get('gamma2', 0)
            theta2 = solution.get('theta2', 0)
            gamma3 = solution.get('gamma3', 0)
            theta3 = solution.get('theta3', 0)
            
            # Actualizar sliders
            self.angle_sliders['gamma1'].setValue(int(gamma1))
            self.angle_sliders['theta1'].setValue(int(theta1))
            self.angle_sliders['gamma2'].setValue(int(gamma2))
            self.angle_sliders['theta2'].setValue(int(theta2))
            self.angle_sliders['gamma3'].setValue(int(gamma3))
            self.angle_sliders['theta3'].setValue(int(theta3))
            
            # Actualizar brazo
            self.arm.actualizeArm(
                {'gama': gamma1, 'theta': theta1},
                {'gama': gamma2, 'theta': theta2},
                {'gama': gamma3, 'theta': theta3}
            )
            
            self.update_info_display()
            
        except Exception as e:
            self.status_label.setText(f"Estado: Error en animación - {str(e)}")
            
    def animation_finished(self, solution):
        """Animación completada"""
        self.status_label.setText("Estado: Movimiento completado")
        self.visualize_btn.setEnabled(True)
        self.update_animation_progress(solution)
        
    def animation_error(self, error_msg):
        """Error en la animación"""
        self.status_label.setText(f"Estado: Error - {error_msg}")
        self.visualize_btn.setEnabled(True)
        QMessageBox.warning(self, "Error", error_msg)
        
    def reset_arm(self):
        """Resetear el brazo a posición inicial"""
        self.initialize_arm_on_axes()

def main():
    """Función principal"""
    app = QApplication(sys.argv)
    
    # Configurar estilo
    app.setStyle('Fusion')
    
    # Crear y mostrar ventana
    window = ArmVisualizerWindow()
    window.show()
    
    # Ejecutar aplicación
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
