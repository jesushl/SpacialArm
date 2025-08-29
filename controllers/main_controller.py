#!/usr/bin/env python3
"""
Controlador principal - Coordina modelo y vista
"""

from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from typing import Dict, Optional

from models.arm_model import ArmModel
from models.genetic_solver import GeneticSolver
from views.main_window import MainWindow

class GeneticThread(QThread):
    """Thread para ejecutar algoritmo genético sin bloquear la UI"""
    
    progress = pyqtSignal(dict)  # Emite solución intermedia
    finished = pyqtSignal(dict)  # Emite solución final
    error = pyqtSignal(str)      # Emite error
    
    def __init__(self, solver: GeneticSolver):
        super().__init__()
        self.solver = solver
        self.is_running = True
    
    def run(self):
        """Ejecutar algoritmo genético"""
        try:
            solution = self.solver.solve(
                callback=lambda sol, fit, gen: self.progress.emit(sol) if sol else None
            )
            if solution:
                self.finished.emit(solution)
            else:
                self.error.emit("No se encontró solución")
        except Exception as e:
            self.error.emit(str(e))
    
    def stop(self):
        """Detener el thread"""
        self.is_running = False

class MainController:
    """Controlador principal de la aplicación"""
    
    def __init__(self):
        # Modelos
        self.arm_model = ArmModel()
        self.genetic_solver = None
        self.genetic_thread = None
        
        # Vista
        self.view = MainWindow(self)
        
        # Estado
        self.target_position = {'x': 2.0, 'y': 1.0, 'z': 2.0}
        self.is_animating = False
        
        # Timer para actualización de UI
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_ui)
        self.update_timer.start(50)  # 20 FPS
        
        # Inicializar
        self.initialize()
    
    def initialize(self):
        """Inicializar la aplicación"""
        # Resetear brazo a posición por defecto
        self.arm_model.reset_to_default_position()
        
        # Actualizar vista inicial
        self.update_view()
    
    def update_view(self):
        """Actualizar toda la vista"""
        # Obtener datos del modelo
        joint_positions = self.arm_model.get_joint_positions()
        end_effector_pos = self.arm_model.get_end_effector_position()
        angles = self.arm_model.get_angles()
        distance = self.arm_model.calculate_distance_to_target(self.target_position)
        
        # Actualizar vista
        self.view.update_arm_display(joint_positions)
        self.view.update_target_display(self.target_position)
        self.view.update_angle_labels(angles)
        self.view.update_info_labels(
            end_effector_pos,
            self.target_position,
            distance,
            "Listo" if not self.is_animating else "Calculando..."
        )
    
    def update_ui(self):
        """Actualizar UI (llamado por timer)"""
        if not self.is_animating:
            self.update_view()
    
    def on_angle_changed(self):
        """Manejador para cambio de ángulos"""
        if self.is_animating:
            return
        
        # Obtener ángulos de la vista
        angles = self.view.get_angle_values()
        
        # Actualizar modelo
        self.arm_model.set_angles(angles)
        
        # Actualizar vista
        self.update_view()
    
    def on_target_changed(self):
        """Manejador para cambio de objetivo"""
        if self.is_animating:
            return
        
        # Obtener objetivo de la vista
        self.target_position = self.view.get_target_values()
        
        # Actualizar vista
        self.update_view()
    
    def on_visualize_clicked(self):
        """Manejador para clic en botón de visualización"""
        if self.is_animating:
            return
        
        # Verificar si el objetivo es alcanzable
        if not self.arm_model.is_target_reachable(self.target_position):
            self.view.update_info_labels(
                self.arm_model.get_end_effector_position(),
                self.target_position,
                self.arm_model.calculate_distance_to_target(self.target_position),
                "Objetivo fuera de alcance"
            )
            return
        
        # Crear solver genético
        self.genetic_solver = GeneticSolver(
            self.arm_model,
            self.target_position,
            population_size=100,
            generations=200
        )
        
        # Crear y ejecutar thread
        self.genetic_thread = GeneticThread(self.genetic_solver)
        self.genetic_thread.progress.connect(self.on_genetic_progress)
        self.genetic_thread.finished.connect(self.on_genetic_finished)
        self.genetic_thread.error.connect(self.on_genetic_error)
        
        # Iniciar animación
        self.is_animating = True
        self.view.set_visualize_enabled(False)
        self.view.update_info_labels(
            self.arm_model.get_end_effector_position(),
            self.target_position,
            self.arm_model.calculate_distance_to_target(self.target_position),
            "Calculando movimiento..."
        )
        
        self.genetic_thread.start()
    
    def on_genetic_progress(self, solution: Dict[str, float]):
        """Manejador para progreso del algoritmo genético"""
        if not self.is_animating:
            return
        
        # Aplicar solución al modelo
        self.arm_model.set_angles(solution)
        
        # Actualizar vista
        self.update_view()
    
    def on_genetic_finished(self, solution: Dict[str, float]):
        """Manejador para finalización del algoritmo genético"""
        # Aplicar solución final
        self.arm_model.set_angles(solution)
        self.view.set_angle_values(solution)
        
        # Finalizar animación
        self.is_animating = False
        self.view.set_visualize_enabled(True)
        
        # Actualizar vista
        self.update_view()
    
    def on_genetic_error(self, error_msg: str):
        """Manejador para error del algoritmo genético"""
        # Finalizar animación
        self.is_animating = False
        self.view.set_visualize_enabled(True)
        
        # Mostrar error
        self.view.update_info_labels(
            self.arm_model.get_end_effector_position(),
            self.target_position,
            self.arm_model.calculate_distance_to_target(self.target_position),
            f"Error: {error_msg}"
        )
    
    def reset_arm(self):
        """Resetear brazo a posición por defecto"""
        if self.is_animating:
            return
        
        self.arm_model.reset_to_default_position()
        self.view.set_angle_values(self.arm_model.get_angles())
        self.update_view()
    
    def reset_view(self):
        """Resetear vista 3D"""
        self.view.gl_widget.reset_view()
    
    def show(self):
        """Mostrar la ventana"""
        self.view.show()
