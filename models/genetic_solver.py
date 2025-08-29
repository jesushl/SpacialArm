#!/usr/bin/env python3
"""
Modelo del solver genético para cinemática inversa
"""

import random
import math
from typing import Dict, List, Callable, Optional
from models.arm_model import ArmModel

class GeneticSolver:
    """Solver genético para cinemática inversa"""
    
    def __init__(self, arm_model: ArmModel, target: Dict[str, float], 
                 population_size: int = 100, generations: int = 200):
        """
        Inicializar el solver genético
        
        Args:
            arm_model: Modelo del brazo
            target: Punto objetivo
            population_size: Tamaño de la población
            generations: Número de generaciones
        """
        self.arm_model = arm_model
        self.target = target
        self.population_size = population_size
        self.generations = generations
        
        # Parámetros del algoritmo genético
        self.mutation_rate = 0.1
        self.crossover_rate = 0.8
        self.elite_size = 5
        
    def solve(self, callback: Optional[Callable] = None) -> Optional[Dict[str, float]]:
        """
        Resolver cinemática inversa
        
        Args:
            callback: Función de callback para progreso
            
        Returns:
            Mejor solución encontrada o None
        """
        # Generar población inicial
        population = self._generate_initial_population()
        
        best_solution = None
        best_fitness = float('inf')
        
        for generation in range(self.generations):
            # Evaluar fitness
            fitness_scores = []
            for individual in population:
                fitness = self._evaluate_fitness(individual)
                fitness_scores.append((fitness, individual))
                
                # Actualizar mejor solución
                if fitness < best_fitness:
                    best_fitness = fitness
                    best_solution = individual.copy()
            
            # Ordenar por fitness
            fitness_scores.sort(key=lambda x: x[0])
            
            # Verificar convergencia
            if best_fitness < 0.01:  # Tolerancia de 1cm
                break
            
            # Crear nueva población
            new_population = []
            
            # Elitismo: mantener los mejores
            for i in range(self.elite_size):
                new_population.append(fitness_scores[i][1])
            
            # Generar resto de la población
            while len(new_population) < self.population_size:
                # Selección de padres
                parent1 = self._tournament_selection(fitness_scores)
                parent2 = self._tournament_selection(fitness_scores)
                
                # Cruce
                if random.random() < self.crossover_rate:
                    child = self._crossover(parent1, parent2)
                else:
                    child = parent1.copy()
                
                # Mutación
                if random.random() < self.mutation_rate:
                    child = self._mutate(child)
                
                new_population.append(child)
            
            population = new_population
            
            # Callback para progreso
            if callback:
                callback(best_solution, best_fitness, generation)
        
        return best_solution
    
    def _generate_initial_population(self) -> List[Dict[str, float]]:
        """Generar población inicial"""
        population = []
        
        for _ in range(self.population_size):
            individual = {}
            for angle_name in self.arm_model.angles.keys():
                # Generar ángulos aleatorios
                if 'gamma' in angle_name:
                    # Ángulos gamma entre 0 y 180 grados
                    individual[angle_name] = random.uniform(0, 180)
                else:
                    # Ángulos theta entre -180 y 180 grados
                    individual[angle_name] = random.uniform(-180, 180)
            
            population.append(individual)
        
        return population
    
    def _evaluate_fitness(self, individual: Dict[str, float]) -> float:
        """Evaluar fitness de un individuo"""
        # Aplicar ángulos al modelo
        self.arm_model.set_angles(individual)
        
        # Calcular distancia al objetivo
        distance = self.arm_model.calculate_distance_to_target(self.target)
        
        return distance
    
    def _tournament_selection(self, fitness_scores: List[tuple], tournament_size: int = 3) -> Dict[str, float]:
        """Selección por torneo"""
        tournament = random.sample(fitness_scores, tournament_size)
        return min(tournament, key=lambda x: x[0])[1]
    
    def _crossover(self, parent1: Dict[str, float], parent2: Dict[str, float]) -> Dict[str, float]:
        """Cruzar dos padres"""
        child = {}
        
        for angle_name in parent1.keys():
            if random.random() < 0.5:
                child[angle_name] = parent1[angle_name]
            else:
                child[angle_name] = parent2[angle_name]
        
        return child
    
    def _mutate(self, individual: Dict[str, float]) -> Dict[str, float]:
        """Mutar un individuo"""
        mutated = individual.copy()
        
        for angle_name in mutated.keys():
            if random.random() < 0.1:  # 10% de probabilidad de mutar cada gen
                if 'gamma' in angle_name:
                    # Mutación para ángulos gamma
                    mutated[angle_name] += random.gauss(0, 10)
                    mutated[angle_name] = max(0, min(180, mutated[angle_name]))
                else:
                    # Mutación para ángulos theta
                    mutated[angle_name] += random.gauss(0, 15)
                    mutated[angle_name] = max(-180, min(180, mutated[angle_name]))
        
        return mutated
