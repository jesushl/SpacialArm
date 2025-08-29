#!/usr/bin/env python3
"""
Widget OpenGL para visualización 3D del brazo robótico
"""

import numpy as np
from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QMouseEvent, QWheelEvent
import OpenGL.GL as gl
import OpenGL.GLU as glu

class ArmGLWidget(QOpenGLWidget):
    """Widget OpenGL para renderizar el brazo robótico en 3D"""
    
    # Señales
    view_changed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Parámetros de la cámara
        self.rotation_x = 0
        self.rotation_y = 0
        self.zoom = -15
        self.last_mouse_pos = None
        
        # Datos del brazo
        self.joint_positions = []
        self.target_position = None
        
        # Configuración del widget
        self.setFocusPolicy(Qt.StrongFocus)
        self.setMinimumSize(600, 400)
        
        # Timer para actualización continua
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update)
        self.update_timer.start(16)  # ~60 FPS
    
    def set_joint_positions(self, positions):
        """Establecer posiciones de las articulaciones"""
        self.joint_positions = positions
        self.update()
    
    def set_target_position(self, position):
        """Establecer posición del objetivo"""
        self.target_position = position
        self.update()
    
    def initializeGL(self):
        """Inicializar OpenGL"""
        # Color de fondo
        gl.glClearColor(0.1, 0.1, 0.1, 1.0)
        
        # Habilitar características
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_LIGHTING)
        gl.glEnable(gl.GL_LIGHT0)
        gl.glEnable(gl.GL_COLOR_MATERIAL)
        
        # Configurar iluminación
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
        self._draw_coordinate_axes()
        
        # Dibujar brazo
        if self.joint_positions:
            self._draw_arm()
        
        # Dibujar objetivo
        if self.target_position:
            self._draw_target()
    
    def _draw_coordinate_axes(self):
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
    
    def _draw_arm(self):
        """Dibujar el brazo robótico"""
        if len(self.joint_positions) < 2:
            return
        
        # Dibujar base
        gl.glColor3f(0.5, 0.5, 0.5)
        self._draw_sphere(0, 0, 0, 0.3)
        
        # Dibujar segmentos y articulaciones
        for i in range(len(self.joint_positions) - 1):
            pos1 = self.joint_positions[i]
            pos2 = self.joint_positions[i + 1]
            
            # Dibujar segmento
            gl.glColor3f(0.2, 0.6, 1.0)
            self._draw_segment(pos1, pos2)
            
            # Dibujar articulación
            gl.glColor3f(1.0, 0.8, 0.0)
            self._draw_sphere(pos2[0], pos2[1], pos2[2], 0.2)
        
        # Dibujar efector final
        if self.joint_positions:
            final_pos = self.joint_positions[-1]
            gl.glColor3f(1.0, 0.0, 0.0)
            self._draw_sphere(final_pos[0], final_pos[1], final_pos[2], 0.25)
    
    def _draw_target(self):
        """Dibujar punto objetivo"""
        if not self.target_position:
            return
        
        x, y, z = self.target_position['x'], self.target_position['y'], self.target_position['z']
        
        # Dibujar esfera objetivo
        gl.glColor3f(0.0, 1.0, 0.0)
        self._draw_sphere(x, y, z, 0.3)
        
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
    
    def _draw_segment(self, start, end):
        """Dibujar un segmento del brazo"""
        gl.glDisable(gl.GL_LIGHTING)
        gl.glBegin(gl.GL_LINES)
        gl.glVertex3f(start[0], start[1], start[2])
        gl.glVertex3f(end[0], end[1], end[2])
        gl.glEnd()
        gl.glEnable(gl.GL_LIGHTING)
    
    def _draw_sphere(self, x, y, z, radius):
        """Dibujar una esfera"""
        gl.glPushMatrix()
        gl.glTranslatef(x, y, z)
        quad = glu.gluNewQuadric()
        glu.gluSphere(quad, radius, 16, 16)
        glu.gluDeleteQuadric(quad)
        gl.glPopMatrix()
    
    def mousePressEvent(self, event: QMouseEvent):
        """Manejar clic del mouse"""
        self.last_mouse_pos = event.pos()
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """Manejar movimiento del mouse"""
        if self.last_mouse_pos is None:
            return
        
        dx = event.x() - self.last_mouse_pos.x()
        dy = event.y() - self.last_mouse_pos.y()
        
        if event.buttons() & Qt.LeftButton:
            self.rotation_y += dx
            self.rotation_x += dy
            self.view_changed.emit()
            self.update()
        
        self.last_mouse_pos = event.pos()
    
    def wheelEvent(self, event: QWheelEvent):
        """Manejar rueda del mouse"""
        delta = event.angleDelta().y()
        self.zoom += delta / 120.0
        self.zoom = max(-30, min(-5, self.zoom))
        self.view_changed.emit()
        self.update()
    
    def reset_view(self):
        """Resetear vista"""
        self.rotation_x = 0
        self.rotation_y = 0
        self.zoom = -15
        self.view_changed.emit()
        self.update()
