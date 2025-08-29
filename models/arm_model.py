#!/usr/bin/env python3
"""
Modelo del brazo robótico - Maneja la lógica de negocio y datos del brazo
"""

import math
import numpy as np
from typing import Dict, List, Tuple, Optional

class ArmModel:
    """Modelo del brazo robótico con 3 segmentos"""
    
    def __init__(self, arm1_length: float = 3.0, arm2_length: float = 2.5, arm3_length: float = 2.0):
        """
        Inicializar el modelo del brazo
        
        Args:
            arm1_length: Longitud del primer segmento
            arm2_length: Longitud del segundo segmento  
            arm3_length: Longitud del tercer segmento
        """
        self.arm1_length = arm1_length
        self.arm2_length = arm2_length
        self.arm3_length = arm3_length
        
        # Ángulos actuales (en radianes)
        self.angles = {
            'theta1': 0.0,  # Rotación en XY
            'gamma1': 0.0,  # Elevación
            'theta2': 0.0,  # Rotación en XY
            'gamma2': 0.0,  # Elevación
            'theta3': 0.0,  # Rotación en XY
            'gamma3': 0.0   # Elevación
        }
        
        # Posiciones de las articulaciones
        self.joint_positions = []
        self.end_effector_position = {'x': 0.0, 'y': 0.0, 'z': 0.0}
        
        # Calcular posición inicial
        self.update_positions()
    
    def set_angles(self, angles: Dict[str, float]) -> None:
        """
        Establecer los ángulos del brazo
        
        Args:
            angles: Diccionario con los ángulos en grados
        """
        for key, value in angles.items():
            if key in self.angles:
                self.angles[key] = math.radians(value)
        
        self.update_positions()
    
    def get_angles(self) -> Dict[str, float]:
        """
        Obtener los ángulos actuales en grados
        
        Returns:
            Diccionario con los ángulos en grados
        """
        return {key: math.degrees(value) for key, value in self.angles.items()}
    
    def update_positions(self) -> None:
        """Calcular las posiciones de todas las articulaciones"""
        # Posición base (origen)
        base_pos = np.array([0.0, 0.0, 0.0])
        
        # Matriz de transformación acumulativa
        transform = np.eye(4)
        
        # Primer segmento
        transform = self._apply_rotation(transform, self.angles['theta1'], 'z')
        transform = self._apply_rotation(transform, self.angles['gamma1'], 'y')
        joint1_pos = transform @ np.array([self.arm1_length, 0.0, 0.0, 1.0])
        
        # Segundo segmento
        transform = self._apply_translation(transform, [self.arm1_length, 0.0, 0.0])
        transform = self._apply_rotation(transform, self.angles['theta2'], 'z')
        transform = self._apply_rotation(transform, self.angles['gamma2'], 'y')
        joint2_pos = transform @ np.array([self.arm2_length, 0.0, 0.0, 1.0])
        
        # Tercer segmento
        transform = self._apply_translation(transform, [self.arm2_length, 0.0, 0.0])
        transform = self._apply_rotation(transform, self.angles['theta3'], 'z')
        transform = self._apply_rotation(transform, self.angles['gamma3'], 'y')
        end_effector_pos = transform @ np.array([self.arm3_length, 0.0, 0.0, 1.0])
        
        # Guardar posiciones
        self.joint_positions = [
            base_pos,
            joint1_pos[:3],
            joint2_pos[:3],
            end_effector_pos[:3]
        ]
        
        self.end_effector_position = {
            'x': float(end_effector_pos[0]),
            'y': float(end_effector_pos[1]),
            'z': float(end_effector_pos[2])
        }
    
    def _apply_rotation(self, transform: np.ndarray, angle: float, axis: str) -> np.ndarray:
        """Aplicar rotación a la matriz de transformación"""
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        
        if axis == 'x':
            rotation = np.array([
                [1, 0, 0, 0],
                [0, cos_a, -sin_a, 0],
                [0, sin_a, cos_a, 0],
                [0, 0, 0, 1]
            ])
        elif axis == 'y':
            rotation = np.array([
                [cos_a, 0, sin_a, 0],
                [0, 1, 0, 0],
                [-sin_a, 0, cos_a, 0],
                [0, 0, 0, 1]
            ])
        elif axis == 'z':
            rotation = np.array([
                [cos_a, -sin_a, 0, 0],
                [sin_a, cos_a, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ])
        
        return transform @ rotation
    
    def _apply_translation(self, transform: np.ndarray, translation: List[float]) -> np.ndarray:
        """Aplicar traslación a la matriz de transformación"""
        translation_matrix = np.eye(4)
        translation_matrix[:3, 3] = translation
        return transform @ translation_matrix
    
    def get_joint_positions(self) -> List[np.ndarray]:
        """Obtener posiciones de todas las articulaciones"""
        return self.joint_positions
    
    def get_end_effector_position(self) -> Dict[str, float]:
        """Obtener posición del efector final"""
        return self.end_effector_position
    
    def calculate_distance_to_target(self, target: Dict[str, float]) -> float:
        """
        Calcular distancia al punto objetivo
        
        Args:
            target: Punto objetivo {'x': float, 'y': float, 'z': float}
            
        Returns:
            Distancia al objetivo
        """
        dx = self.end_effector_position['x'] - target['x']
        dy = self.end_effector_position['y'] - target['y']
        dz = self.end_effector_position['z'] - target['z']
        
        return math.sqrt(dx*dx + dy*dy + dz*dz)
    
    def is_target_reachable(self, target: Dict[str, float]) -> bool:
        """
        Verificar si el objetivo es alcanzable
        
        Args:
            target: Punto objetivo
            
        Returns:
            True si es alcanzable
        """
        # Distancia desde el origen al objetivo
        target_distance = math.sqrt(
            target['x']**2 + target['y']**2 + target['z']**2
        )
        
        # Suma de longitudes de los segmentos
        max_reach = self.arm1_length + self.arm2_length + self.arm3_length
        
        return target_distance <= max_reach
    
    def reset_to_default_position(self) -> None:
        """Resetear el brazo a posición por defecto"""
        self.angles = {
            'theta1': 0.0,
            'gamma1': math.radians(90),  # Apuntar hacia arriba
            'theta2': 0.0,
            'gamma2': 0.0,
            'theta3': 0.0,
            'gamma3': 0.0
        }
        self.update_positions()
