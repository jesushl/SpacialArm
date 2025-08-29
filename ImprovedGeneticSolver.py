import math
import random
import time
from Arm import Arm

class ImprovedGeneticSolver:
    """Solver genético mejorado para cinemática inversa del brazo robótico"""
    
    def __init__(self, arm1Len=3.0, arm2Len=2.5, arm3Len=2.0, goalPoint={'x': 0, 'y': 0, 'z': 0}):
        self.arm = Arm(arm1Len, arm2Len, arm3Len)
        self.goalPoint = goalPoint
        self.maximumReach = arm1Len + arm2Len + arm3Len
        self.population_size = 50
        self.generations = 100
        self.mutation_rate = 0.1
        self.crossover_rate = 0.8
        
    def is_possible_shot(self):
        """Verifica si el punto objetivo está dentro del alcance"""
        distance = math.sqrt(
            self.goalPoint['x']**2 + 
            self.goalPoint['y']**2 + 
            self.goalPoint['z']**2
        )
        return distance <= self.maximumReach
    
    def generate_random_individual(self):
        """Genera un individuo aleatorio con ángulos válidos"""
        return {
            'arm1': {
                'theta': random.uniform(-180, 180),
                'gama': random.uniform(0, 180)
            },
            'arm2': {
                'theta': random.uniform(-180, 180),
                'gama': random.uniform(0, 180)
            },
            'arm3': {
                'theta': random.uniform(-180, 180),
                'gama': random.uniform(0, 180)
            }
        }
    
    def evaluate_fitness(self, individual):
        """Evalúa la aptitud de un individuo (distancia al objetivo)"""
        try:
            # Aplicar ángulos al brazo
            self.arm.actualizeArm(
                individual['arm1'],
                individual['arm2'],
                individual['arm3']
            )
            
            # Obtener posición final
            final_pos = self.arm.getArmFinalPoint()
            
            # Calcular distancia al objetivo
            distance = math.sqrt(
                (final_pos['x'] - self.goalPoint['x'])**2 +
                (final_pos['y'] - self.goalPoint['y'])**2 +
                (final_pos['z'] - self.goalPoint['z'])**2
            )
            
            return distance
        except:
            return float('inf')  # Penalizar individuos inválidos
    
    def crossover(self, parent1, parent2):
        """Realiza el cruce entre dos padres"""
        if random.random() > self.crossover_rate:
            return parent1.copy()
        
        child = {}
        for arm_key in ['arm1', 'arm2', 'arm3']:
            child[arm_key] = {}
            for angle_key in ['theta', 'gama']:
                # Cruce uniforme
                if random.random() < 0.5:
                    child[arm_key][angle_key] = parent1[arm_key][angle_key]
                else:
                    child[arm_key][angle_key] = parent2[arm_key][angle_key]
        
        return child
    
    def mutate(self, individual):
        """Aplica mutación a un individuo"""
        mutated = individual.copy()
        
        for arm_key in ['arm1', 'arm2', 'arm3']:
            for angle_key in ['theta', 'gama']:
                if random.random() < self.mutation_rate:
                    # Mutación gaussiana
                    current_value = mutated[arm_key][angle_key]
                    mutation = random.gauss(0, 30)  # Desviación estándar de 30 grados
                    new_value = current_value + mutation
                    
                    # Mantener dentro de rangos válidos
                    if angle_key == 'gama':
                        new_value = max(0, min(180, new_value))
                    else:
                        new_value = max(-180, min(180, new_value))
                    
                    mutated[arm_key][angle_key] = new_value
        
        return mutated
    
    def select_parents(self, population, fitnesses):
        """Selecciona padres usando torneo"""
        tournament_size = 3
        parent1_idx = min(random.sample(range(len(population)), tournament_size), 
                         key=lambda i: fitnesses[i])
        parent2_idx = min(random.sample(range(len(population)), tournament_size), 
                         key=lambda i: fitnesses[i])
        
        return population[parent1_idx], population[parent2_idx]
    
    def solve(self, callback=None):
        """Resuelve el problema de cinemática inversa usando algoritmo genético"""
        if not self.is_possible_shot():
            return None
        
        # Generar población inicial
        population = [self.generate_random_individual() for _ in range(self.population_size)]
        best_solution = None
        best_fitness = float('inf')
        
        for generation in range(self.generations):
            # Evaluar población
            fitnesses = [self.evaluate_fitness(ind) for ind in population]
            
            # Encontrar mejor individuo
            min_fitness_idx = fitnesses.index(min(fitnesses))
            if fitnesses[min_fitness_idx] < best_fitness:
                best_fitness = fitnesses[min_fitness_idx]
                best_solution = population[min_fitness_idx].copy()
            
            # Verificar si encontramos una solución suficientemente buena
            if best_fitness < 0.1:  # Tolerancia de 0.1 unidades
                break
            
            # Llamar callback si está disponible
            if callback and generation % 10 == 0:
                callback(best_solution, best_fitness, generation)
            
            # Crear nueva población
            new_population = []
            
            # Elitismo: mantener el mejor individuo
            new_population.append(best_solution)
            
            # Generar resto de la población
            while len(new_population) < self.population_size:
                # Seleccionar padres
                parent1, parent2 = self.select_parents(population, fitnesses)
                
                # Crear hijo
                child = self.crossover(parent1, parent2)
                
                # Mutar hijo
                child = self.mutate(child)
                
                new_population.append(child)
            
            population = new_population
        
        return best_solution
    
    def solve_with_animation(self, callback=None):
        """Resuelve con animación paso a paso"""
        if not self.is_possible_shot():
            return None
        
        # Generar población inicial
        population = [self.generate_random_individual() for _ in range(self.population_size)]
        best_solution = None
        best_fitness = float('inf')
        
        for generation in range(self.generations):
            # Evaluar población
            fitnesses = [self.evaluate_fitness(ind) for ind in population]
            
            # Encontrar mejor individuo
            min_fitness_idx = fitnesses.index(min(fitnesses))
            if fitnesses[min_fitness_idx] < best_fitness:
                best_fitness = fitnesses[min_fitness_idx]
                best_solution = population[min_fitness_idx].copy()
                
                # Llamar callback para animación
                if callback:
                    callback(best_solution, best_fitness, generation)
            
            # Verificar si encontramos una solución suficientemente buena
            if best_fitness < 0.1:
                break
            
            # Crear nueva población
            new_population = []
            new_population.append(best_solution)  # Elitismo
            
            while len(new_population) < self.population_size:
                parent1, parent2 = self.select_parents(population, fitnesses)
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)
                new_population.append(child)
            
            population = new_population
        
        return best_solution
