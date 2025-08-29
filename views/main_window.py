#!/usr/bin/env python3
"""
Ventana principal de la aplicación
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QGroupBox, QLabel, QSlider, QLineEdit, QPushButton,
                             QSplitter, QGridLayout)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

from views.gl_widget import ArmGLWidget

class MainWindow(QMainWindow):
    """Ventana principal de la aplicación"""
    
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()
    
    def init_ui(self):
        """Inicializar la interfaz de usuario"""
        self.setWindowTitle("Visualizador 3D del Brazo Robótico - MVC")
        self.setGeometry(100, 100, 1400, 900)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Splitter para distribución 5:3
        splitter = QSplitter(Qt.Vertical)
        main_layout.addWidget(splitter)
        
        # Sección de visualización (5/8)
        self.gl_widget = ArmGLWidget()
        splitter.addWidget(self.gl_widget)
        
        # Sección de controles (3/8)
        controls_widget = self.create_controls_widget()
        splitter.addWidget(controls_widget)
        
        # Configurar proporciones del splitter
        splitter.setSizes([625, 375])  # 5:3 ratio
        
        # Conectar señales
        self.connect_signals()
    
    def create_controls_widget(self):
        """Crear widget de controles"""
        controls_widget = QWidget()
        controls_layout = QHBoxLayout(controls_widget)
        controls_layout.setSpacing(15)
        
        # Grupo: Punto Objetivo
        target_group = self.create_target_group()
        controls_layout.addWidget(target_group)
        
        # Grupo: Control de Ángulos
        angle_group = self.create_angle_group()
        controls_layout.addWidget(angle_group)
        
        # Grupo: Información
        info_group = self.create_info_group()
        controls_layout.addWidget(info_group)
        
        return controls_widget
    
    def create_target_group(self):
        """Crear grupo de punto objetivo"""
        group = QGroupBox("🎯 Punto Objetivo")
        group.setFont(QFont("Arial", 10, QFont.Bold))
        
        layout = QVBoxLayout(group)
        layout.setSpacing(10)
        
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
        
        layout.addLayout(coord_grid)
        
        # Botón de visualización
        self.visualize_btn = QPushButton("🚀 Visualizar Movimiento")
        self.visualize_btn.setFont(QFont("Arial", 11, QFont.Bold))
        layout.addWidget(self.visualize_btn)
        
        return group
    
    def create_angle_group(self):
        """Crear grupo de control de ángulos"""
        group = QGroupBox("🎛️ Control de Ángulos")
        group.setFont(QFont("Arial", 10, QFont.Bold))
        
        layout = QVBoxLayout(group)
        layout.setSpacing(8)
        
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
            label.setMinimumWidth(30)
            slider_layout.addWidget(label)
            
            # Slider
            slider = QSlider(Qt.Horizontal)
            slider.setRange(min_val, max_val)
            slider.setValue(0)
            self.angle_sliders[angle_name] = slider
            slider_layout.addWidget(slider)
            
            # Etiqueta de valor
            value_label = QLabel("0°")
            value_label.setMinimumWidth(35)
            value_label.setAlignment(Qt.AlignRight)
            self.angle_labels[angle_name] = value_label
            slider_layout.addWidget(value_label)
            
            layout.addLayout(slider_layout)
        
        return group
    
    def create_info_group(self):
        """Crear grupo de información"""
        group = QGroupBox("📊 Información")
        group.setFont(QFont("Arial", 10, QFont.Bold))
        
        layout = QVBoxLayout(group)
        layout.setSpacing(8)
        
        self.current_pos_label = QLabel("📍 Posición actual: (0.00, 0.00, 0.00)")
        layout.addWidget(self.current_pos_label)
        
        self.target_pos_label = QLabel("🎯 Objetivo: (2.00, 1.00, 2.00)")
        layout.addWidget(self.target_pos_label)
        
        self.distance_label = QLabel("📏 Distancia: 0.00")
        layout.addWidget(self.distance_label)
        
        self.status_label = QLabel("✅ Estado: Listo")
        layout.addWidget(self.status_label)
        
        # Botones de control
        reset_arm_btn = QPushButton("🔄 Reset Brazo")
        layout.addWidget(reset_arm_btn)
        
        reset_view_btn = QPushButton("👁️ Reset Vista")
        layout.addWidget(reset_view_btn)
        
        return group
    
    def connect_signals(self):
        """Conectar señales de la interfaz"""
        # Conectar sliders
        for slider in self.angle_sliders.values():
            slider.valueChanged.connect(self.controller.on_angle_changed)
        
        # Conectar campos de entrada
        self.x_input.textChanged.connect(self.controller.on_target_changed)
        self.y_input.textChanged.connect(self.controller.on_target_changed)
        self.z_input.textChanged.connect(self.controller.on_target_changed)
        
        # Conectar botones
        self.visualize_btn.clicked.connect(self.controller.on_visualize_clicked)
    
    def update_arm_display(self, joint_positions):
        """Actualizar visualización del brazo"""
        self.gl_widget.set_joint_positions(joint_positions)
    
    def update_target_display(self, target_position):
        """Actualizar visualización del objetivo"""
        self.gl_widget.set_target_position(target_position)
    
    def update_angle_labels(self, angles):
        """Actualizar etiquetas de ángulos"""
        for angle_name, value in angles.items():
            if angle_name in self.angle_labels:
                self.angle_labels[angle_name].setText(f"{value:.1f}°")
    
    def update_info_labels(self, current_pos, target_pos, distance, status):
        """Actualizar etiquetas de información"""
        self.current_pos_label.setText(f"📍 Posición actual: ({current_pos['x']:.2f}, {current_pos['y']:.2f}, {current_pos['z']:.2f})")
        self.target_pos_label.setText(f"🎯 Objetivo: ({target_pos['x']:.2f}, {target_pos['y']:.2f}, {target_pos['z']:.2f})")
        self.distance_label.setText(f"📏 Distancia: {distance:.2f}")
        self.status_label.setText(f"✅ Estado: {status}")
    
    def get_target_values(self):
        """Obtener valores del objetivo"""
        try:
            x = float(self.x_input.text() or "0")
            y = float(self.y_input.text() or "0")
            z = float(self.z_input.text() or "0")
            return {'x': x, 'y': y, 'z': z}
        except ValueError:
            return {'x': 0, 'y': 0, 'z': 0}
    
    def get_angle_values(self):
        """Obtener valores de los ángulos"""
        return {name: slider.value() for name, slider in self.angle_sliders.items()}
    
    def set_angle_values(self, angles):
        """Establecer valores de los ángulos"""
        for name, value in angles.items():
            if name in self.angle_sliders:
                self.angle_sliders[name].setValue(int(value))
    
    def set_visualize_enabled(self, enabled):
        """Habilitar/deshabilitar botón de visualización"""
        self.visualize_btn.setEnabled(enabled)
