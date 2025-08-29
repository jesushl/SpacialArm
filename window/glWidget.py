import sys
import numpy as np
from PyQt5.QtWidgets import QOpenGLWidget, QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor
import OpenGL.GL as gl
from OpenGL.GLU import *
from OpenGL.GLUT import *

class ArmGLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.arm = None
        self.rotation_x = 0
        self.rotation_y = 0
        self.zoom = -10
        self.last_pos = None
        
        # Timer para animación
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(16)  # ~60 FPS
        
    def set_arm(self, arm):
        """Establece el brazo robótico a visualizar"""
        self.arm = arm
        self.update()
    
    def initializeGL(self):
        """Inicialización de OpenGL"""
        gl.glClearColor(0.1, 0.1, 0.1, 1.0)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_LIGHTING)
        gl.glEnable(gl.GL_LIGHT0)
        gl.glEnable(gl.GL_COLOR_MATERIAL)
        
        # Configurar luz
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, [1, 1, 1, 0])
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_AMBIENT, [0.2, 0.2, 0.2, 1])
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE, [0.8, 0.8, 0.8, 1])
    
    def resizeGL(self, width, height):
        """Manejo del redimensionamiento de la ventana"""
        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        aspect = width / float(height)
        gluPerspective(45.0, aspect, 0.1, 100.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
    
    def paintGL(self):
        """Renderizado principal"""
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glLoadIdentity()
        
        # Posicionar cámara
        gl.glTranslatef(0.0, 0.0, self.zoom)
        gl.glRotatef(self.rotation_x, 1.0, 0.0, 0.0)
        gl.glRotatef(self.rotation_y, 0.0, 1.0, 0.0)
        
        # Dibujar ejes de coordenadas
        self.draw_coordinate_axes()
        
        # Dibujar el brazo si está disponible
        if self.arm:
            self.draw_arm()
    
    def draw_coordinate_axes(self):
        """Dibuja los ejes de coordenadas"""
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
        """Dibuja el brazo robótico"""
        if not self.arm:
            return
            
        # Dibujar base del brazo
        gl.glColor3f(0.5, 0.5, 0.5)
        self.draw_cylinder(0, 0, 0, 0.5, 0.2)
        
        # Dibujar primer segmento
        gl.glColor3f(0.8, 0.2, 0.2)
        self.draw_segment(
            self.arm.armCore['x'], self.arm.armCore['y'], self.arm.armCore['z'],
            self.arm.vector1.x, self.arm.vector1.y, self.arm.vector1.z,
            0.1
        )
        
        # Dibujar segundo segmento
        gl.glColor3f(0.2, 0.8, 0.2)
        self.draw_segment(
            self.arm.vector1.x, self.arm.vector1.y, self.arm.vector1.z,
            self.arm.vector2.x, self.arm.vector2.y, self.arm.vector2.z,
            0.08
        )
        
        # Dibujar tercer segmento
        gl.glColor3f(0.2, 0.2, 0.8)
        self.draw_segment(
            self.arm.vector2.x, self.arm.vector2.y, self.arm.vector2.z,
            self.arm.vector3.x, self.arm.vector3.y, self.arm.vector3.z,
            0.06
        )
        
        # Dibujar articulaciones
        gl.glColor3f(1.0, 1.0, 0.0)
        self.draw_sphere(self.arm.armCore['x'], self.arm.armCore['y'], self.arm.armCore['z'], 0.15)
        self.draw_sphere(self.arm.vector1.x, self.arm.vector1.y, self.arm.vector1.z, 0.12)
        self.draw_sphere(self.arm.vector2.x, self.arm.vector2.y, self.arm.vector2.z, 0.10)
        
        # Dibujar punto final
        gl.glColor3f(1.0, 0.0, 1.0)
        self.draw_sphere(self.arm.vector3.x, self.arm.vector3.y, self.arm.vector3.z, 0.08)
    
    def draw_segment(self, x1, y1, z1, x2, y2, z2, radius):
        """Dibuja un segmento del brazo como cilindro"""
        # Calcular dirección del segmento
        dx = x2 - x1
        dy = y2 - y1
        dz = z2 - z1
        length = np.sqrt(dx*dx + dy*dy + dz*dz)
        
        if length == 0:
            return
            
        # Normalizar dirección
        dx /= length
        dy /= length
        dz /= length
        
        # Calcular ángulos de rotación
        if abs(dz) < 0.999:
            rot_y = np.arctan2(dx, dz) * 180 / np.pi
            rot_x = np.arcsin(-dy) * 180 / np.pi
        else:
            rot_y = 0
            rot_x = 90 if dy < 0 else -90
        
        gl.glPushMatrix()
        gl.glTranslatef(x1, y1, z1)
        gl.glRotatef(rot_y, 0, 1, 0)
        gl.glRotatef(rot_x, 1, 0, 0)
        self.draw_cylinder(0, 0, 0, length, radius)
        gl.glPopMatrix()
    
    def draw_cylinder(self, x, y, z, height, radius):
        """Dibuja un cilindro"""
        gl.glPushMatrix()
        gl.glTranslatef(x, y, z)
        
        # Dibujar cilindro usando quads
        segments = 16
        gl.glBegin(gl.GL_QUADS)
        
        for i in range(segments):
            angle1 = 2 * np.pi * i / segments
            angle2 = 2 * np.pi * (i + 1) / segments
            
            x1 = radius * np.cos(angle1)
            y1 = radius * np.sin(angle1)
            x2 = radius * np.cos(angle2)
            y2 = radius * np.sin(angle2)
            
            # Cara lateral
            gl.glNormal3f(np.cos(angle1), np.sin(angle1), 0)
            gl.glVertex3f(x1, y1, 0)
            gl.glVertex3f(x1, y1, height)
            gl.glVertex3f(x2, y2, height)
            gl.glVertex3f(x2, y2, 0)
        
        gl.glEnd()
        
        # Tapas del cilindro
        gl.glBegin(gl.GL_TRIANGLE_FAN)
        gl.glNormal3f(0, 0, -1)
        gl.glVertex3f(0, 0, 0)
        for i in range(segments + 1):
            angle = 2 * np.pi * i / segments
            gl.glVertex3f(radius * np.cos(angle), radius * np.sin(angle), 0)
        gl.glEnd()
        
        gl.glBegin(gl.GL_TRIANGLE_FAN)
        gl.glNormal3f(0, 0, 1)
        gl.glVertex3f(0, 0, height)
        for i in range(segments + 1):
            angle = 2 * np.pi * i / segments
            gl.glVertex3f(radius * np.cos(angle), radius * np.sin(angle), height)
        gl.glEnd()
        
        gl.glPopMatrix()
    
    def draw_sphere(self, x, y, z, radius):
        """Dibuja una esfera"""
        gl.glPushMatrix()
        gl.glTranslatef(x, y, z)
        
        # Usar GLU para dibujar esfera
        quad = gluNewQuadric()
        gluSphere(quad, radius, 16, 16)
        gluDeleteQuadric(quad)
        
        gl.glPopMatrix()
    
    def mousePressEvent(self, event):
        """Manejo del evento de presionar el mouse"""
        self.last_pos = event.pos()
    
    def mouseMoveEvent(self, event):
        """Manejo del evento de mover el mouse"""
        if self.last_pos is None:
            return
            
        dx = event.x() - self.last_pos.x()
        dy = event.y() - self.last_pos.y()
        
        if event.buttons() & Qt.LeftButton:
            self.rotation_y += dx
            self.rotation_x += dy
        elif event.buttons() & Qt.RightButton:
            self.zoom += dy * 0.1
            
        self.last_pos = event.pos()
        self.update()
    
    def wheelEvent(self, event):
        """Manejo del evento de la rueda del mouse para zoom"""
        self.zoom += event.angleDelta().y() * 0.1
        self.update()
