"""
Capability Evolution System for SE-AGI
Manages the evolution and improvement of system capabilities
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json
import uuid
from enum import Enum
import random
import math


class EvolutionStrategy(Enum):
    """Evolution strategies"""
    RANDOM_MUTATION = "random_mutation"
    GRADIENT_ASCENT = "gradient_ascent"
    GENETIC_ALGORITHM = "genetic_algorithm"
    REINFORCEMENT_LEARNING = "reinforcement_learning"
    CURRICULUM_LEARNING = "curriculum_learning"


@dataclass
class Capability:
    """Represents a system capability"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    category: str = "general"
    version: str = "1.0.0"
    parameters: Dict[str, Any] = field(default_factory=dict)
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    fitness_score: float = 0.0
    generation: int = 0
    parent_ids: List[str] = field(default_factory=list)
    mutation_history: List[Dict[str, Any]] = field(default_factory=list)
    usage_count: int = 0
    success_rate: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert capability to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'version': self.version,
            'parameters': self.parameters,
            'performance_metrics': self.performance_metrics,
            'dependencies': self.dependencies,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'fitness_score': self.fitness_score,
            'generation': self.generation,
            'parent_ids': self.parent_ids,
            'mutation_history': self.mutation_history,
            'usage_count': self.usage_count,
            'success_rate': self.success_rate,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Capability':
        """Create capability from dictionary"""
        data = data.copy()
        if 'created_at' in data and isinstance(data['created_at'], str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        if 'updated_at' in data and isinstance(data['updated_at'], str):
            data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        return cls(**data)


@dataclass
class EvolutionExperiment:
    """Represents an evolution experiment"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    strategy: EvolutionStrategy = EvolutionStrategy.RANDOM_MUTATION
    target_capabilities: List[str] = field(default_factory=list)
    fitness_function: Optional[Callable] = None
    generation_count: int = 0
    population_size: int = 10
    mutation_rate: float = 0.1
    crossover_rate: float = 0.7
    selection_pressure: float = 0.5
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    status: str = "pending"  # pending, running, completed, failed
    best_fitness: float = 0.0
    generation_history: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class CapabilityEvolver:
    """
    Capability Evolution System that manages the evolution and improvement
    of system capabilities through various strategies
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize capability evolver"""
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Capability storage
        self.capabilities: Dict[str, Capability] = {}
        self.experiments: Dict[str, EvolutionExperiment] = {}
        
        # Evolution state
        self.current_generation = 0
        self.evolution_history: List[Dict[str, Any]] = []
        
        # Population management
        self.population: List[str] = []  # Capability IDs
        self.elite: List[str] = []  # Best performing capability IDs
        
        # Configuration
        self.max_population_size = self.config.get('max_population_size', 100)
        self.elite_size = self.config.get('elite_size', 10)
        self.mutation_strategies = self.config.get('mutation_strategies', [
            'parameter_tweak', 'add_parameter', 'remove_parameter', 'combine_capabilities'
        ])
        
        # Performance tracking
        self.performance_history: Dict[str, List[float]] = {}
        self.fitness_functions: Dict[str, Callable] = {}
        
        # Evolution parameters
        self.default_mutation_rate = self.config.get('default_mutation_rate', 0.1)
        self.default_crossover_rate = self.config.get('default_crossover_rate', 0.7)
        self.adaptation_rate = self.config.get('adaptation_rate', 0.01)
        
        self.logger.info("CapabilityEvolver initialized")
    
    async def register_capability(self, 
                                 name: str,
                                 description: str = "",
                                 category: str = "general",
                                 parameters: Optional[Dict[str, Any]] = None,
                                 dependencies: Optional[List[str]] = None) -> str:
        """
        Register a new capability for evolution
        
        Args:
            name: Name of the capability
            description: Description of the capability
            category: Category of the capability
            parameters: Initial parameters
            dependencies: List of dependency capability IDs
            
        Returns:
            Capability ID
        """
        capability = Capability(
            name=name,
            description=description,
            category=category,
            parameters=parameters or {},
            dependencies=dependencies or []
        )
        
        self.capabilities[capability.id] = capability
        self.population.append(capability.id)
        
        # Initialize performance tracking
        self.performance_history[capability.id] = []
        
        self.logger.info(f"Registered capability '{name}' with ID {capability.id}")
        return capability.id
    
    async def register_fitness_function(self, 
                                       name: str, 
                                       fitness_func: Callable[[Capability], float]) -> None:
        """Register a fitness function for capability evaluation"""
        self.fitness_functions[name] = fitness_func
        self.logger.info(f"Registered fitness function '{name}'")
    
    async def evolve_capability(self, 
                               capability_id: str,
                               strategy: EvolutionStrategy = EvolutionStrategy.RANDOM_MUTATION,
                               generations: int = 1,
                               fitness_function: Optional[str] = None) -> List[str]:
        """
        Evolve a specific capability
        
        Args:
            capability_id: ID of the capability to evolve
            strategy: Evolution strategy to use
            generations: Number of generations to evolve
            fitness_function: Name of fitness function to use
            
        Returns:
            List of evolved capability IDs
        """
        if capability_id not in self.capabilities:
            return []
        
        base_capability = self.capabilities[capability_id]
        evolved_capabilities = []
        
        for generation in range(generations):
            self.current_generation += 1
            
            if strategy == EvolutionStrategy.RANDOM_MUTATION:
                evolved_id = await self._mutate_capability(capability_id)
                if evolved_id:
                    evolved_capabilities.append(evolved_id)
            
            elif strategy == EvolutionStrategy.GENETIC_ALGORITHM:
                # Create offspring through crossover and mutation
                if len(self.population) > 1:
                    parent2_id = random.choice([cid for cid in self.population if cid != capability_id])
                    offspring_id = await self._crossover_capabilities(capability_id, parent2_id)
                    if offspring_id:
                        mutated_id = await self._mutate_capability(offspring_id)
                        evolved_capabilities.append(mutated_id or offspring_id)
            
            elif strategy == EvolutionStrategy.GRADIENT_ASCENT:
                improved_id = await self._gradient_improve_capability(capability_id, fitness_function)
                if improved_id:
                    evolved_capabilities.append(improved_id)
            
            elif strategy == EvolutionStrategy.CURRICULUM_LEARNING:
                curriculum_id = await self._curriculum_evolve_capability(capability_id)
                if curriculum_id:
                    evolved_capabilities.append(curriculum_id)
        
        # Evaluate fitness of evolved capabilities
        if fitness_function and fitness_function in self.fitness_functions:
            fitness_func = self.fitness_functions[fitness_function]
            for cap_id in evolved_capabilities:
                if cap_id in self.capabilities:
                    capability = self.capabilities[cap_id]
                    capability.fitness_score = await self._evaluate_fitness(capability, fitness_func)
        
        self.logger.info(f"Evolved capability {capability_id} through {generations} generations, "
                        f"created {len(evolved_capabilities)} variants")
        
        return evolved_capabilities
    
    async def evolve_population(self, 
                               strategy: EvolutionStrategy = EvolutionStrategy.GENETIC_ALGORITHM,
                               generations: int = 10,
                               fitness_function: Optional[str] = None) -> Dict[str, Any]:
        """
        Evolve the entire population of capabilities
        
        Args:
            strategy: Evolution strategy to use
            generations: Number of generations to evolve
            fitness_function: Name of fitness function to use
            
        Returns:
            Evolution results and statistics
        """
        if not self.population:
            return {'error': 'No capabilities in population'}
        
        initial_population_size = len(self.population)
        generation_stats = []
        
        for generation in range(generations):
            self.current_generation += 1
            generation_start = datetime.now()
            
            # Evaluate fitness of current population
            if fitness_function and fitness_function in self.fitness_functions:
                await self._evaluate_population_fitness(fitness_function)
            
            # Selection
            selected = await self._select_capabilities(strategy)
            
            # Reproduction
            offspring = []
            if strategy == EvolutionStrategy.GENETIC_ALGORITHM:
                offspring = await self._genetic_reproduction(selected)
            elif strategy == EvolutionStrategy.RANDOM_MUTATION:
                offspring = await self._mutation_reproduction(selected)
            
            # Replacement
            self.population = await self._replace_population(offspring)
            
            # Update elite
            await self._update_elite()
            
            # Record statistics
            generation_end = datetime.now()
            stats = await self._calculate_generation_stats()
            stats.update({
                'generation': self.current_generation,
                'duration': (generation_end - generation_start).total_seconds(),
                'population_size': len(self.population),
                'offspring_count': len(offspring)
            })
            generation_stats.append(stats)
            
            self.logger.info(f"Generation {self.current_generation}: "
                           f"pop_size={len(self.population)}, "
                           f"avg_fitness={stats.get('avg_fitness', 0):.3f}")
        
        # Record evolution history
        evolution_record = {
            'strategy': strategy.value,
            'generations': generations,
            'initial_population_size': initial_population_size,
            'final_population_size': len(self.population),
            'generation_stats': generation_stats,
            'elite_capabilities': self.elite.copy(),
            'timestamp': datetime.now().isoformat()
        }
        self.evolution_history.append(evolution_record)
        
        return evolution_record
    
    async def _mutate_capability(self, capability_id: str) -> Optional[str]:
        """Create a mutated version of a capability"""
        if capability_id not in self.capabilities:
            return None
        
        base_capability = self.capabilities[capability_id]
        
        # Create mutated copy
        mutated = Capability(
            name=f"{base_capability.name}_mutated",
            description=base_capability.description,
            category=base_capability.category,
            parameters=base_capability.parameters.copy(),
            dependencies=base_capability.dependencies.copy(),
            generation=base_capability.generation + 1,
            parent_ids=[capability_id]
        )
        
        # Apply mutations
        mutation_applied = False
        mutation_record = {
            'timestamp': datetime.now().isoformat(),
            'mutations': []
        }
        
        # Parameter tweaking
        if random.random() < self.default_mutation_rate:
            for param_name, param_value in mutated.parameters.items():
                if isinstance(param_value, (int, float)):
                    if random.random() < 0.3:  # 30% chance to mutate each parameter
                        mutation_factor = random.uniform(0.8, 1.2)
                        old_value = param_value
                        mutated.parameters[param_name] = param_value * mutation_factor
                        
                        mutation_record['mutations'].append({
                            'type': 'parameter_tweak',
                            'parameter': param_name,
                            'old_value': old_value,
                            'new_value': mutated.parameters[param_name]
                        })
                        mutation_applied = True
        
        # Add new parameter
        if random.random() < 0.1:  # 10% chance
            new_param_name = f"param_{random.randint(1000, 9999)}"
            new_param_value = random.uniform(0.1, 1.0)
            mutated.parameters[new_param_name] = new_param_value
            
            mutation_record['mutations'].append({
                'type': 'add_parameter',
                'parameter': new_param_name,
                'value': new_param_value
            })
            mutation_applied = True
        
        # Remove parameter (but keep at least one)
        if len(mutated.parameters) > 1 and random.random() < 0.05:  # 5% chance
            param_to_remove = random.choice(list(mutated.parameters.keys()))
            removed_value = mutated.parameters.pop(param_to_remove)
            
            mutation_record['mutations'].append({
                'type': 'remove_parameter',
                'parameter': param_to_remove,
                'removed_value': removed_value
            })
            mutation_applied = True
        
        if mutation_applied:
            mutated.mutation_history.append(mutation_record)
            self.capabilities[mutated.id] = mutated
            self.population.append(mutated.id)
            self.performance_history[mutated.id] = []
            
            self.logger.debug(f"Created mutated capability {mutated.id} from {capability_id}")
            return mutated.id
        
        return None
    
    async def _crossover_capabilities(self, parent1_id: str, parent2_id: str) -> Optional[str]:
        """Create offspring through crossover of two capabilities"""
        if parent1_id not in self.capabilities or parent2_id not in self.capabilities:
            return None
        
        parent1 = self.capabilities[parent1_id]
        parent2 = self.capabilities[parent2_id]
        
        # Create offspring
        offspring = Capability(
            name=f"{parent1.name}_{parent2.name}_offspring",
            description=f"Crossover of {parent1.name} and {parent2.name}",
            category=parent1.category,  # Inherit from first parent
            generation=max(parent1.generation, parent2.generation) + 1,
            parent_ids=[parent1_id, parent2_id]
        )
        
        # Crossover parameters
        all_params = set(parent1.parameters.keys()) | set(parent2.parameters.keys())
        
        for param_name in all_params:
            if param_name in parent1.parameters and param_name in parent2.parameters:
                # Both parents have this parameter - blend or choose
                if random.random() < self.default_crossover_rate:
                    # Blend if numeric
                    p1_val = parent1.parameters[param_name]
                    p2_val = parent2.parameters[param_name]
                    
                    if isinstance(p1_val, (int, float)) and isinstance(p2_val, (int, float)):
                        alpha = random.random()
                        offspring.parameters[param_name] = alpha * p1_val + (1 - alpha) * p2_val
                    else:
                        # Choose randomly
                        offspring.parameters[param_name] = random.choice([p1_val, p2_val])
                else:
                    # Choose from first parent
                    offspring.parameters[param_name] = parent1.parameters[param_name]
            
            elif param_name in parent1.parameters:
                # Only first parent has this parameter
                if random.random() < 0.5:
                    offspring.parameters[param_name] = parent1.parameters[param_name]
            
            elif param_name in parent2.parameters:
                # Only second parent has this parameter
                if random.random() < 0.5:
                    offspring.parameters[param_name] = parent2.parameters[param_name]
        
        # Crossover dependencies
        offspring.dependencies = list(set(parent1.dependencies) | set(parent2.dependencies))
        
        # Store offspring
        self.capabilities[offspring.id] = offspring
        self.population.append(offspring.id)
        self.performance_history[offspring.id] = []
        
        self.logger.debug(f"Created offspring {offspring.id} from {parent1_id} and {parent2_id}")
        return offspring.id
    
    async def _gradient_improve_capability(self, capability_id: str, 
                                         fitness_function: Optional[str]) -> Optional[str]:
        """Improve capability using gradient-like optimization"""
        if capability_id not in self.capabilities:
            return None
        
        if not fitness_function or fitness_function not in self.fitness_functions:
            return None
        
        base_capability = self.capabilities[capability_id]
        fitness_func = self.fitness_functions[fitness_function]
        
        # Current fitness
        current_fitness = await self._evaluate_fitness(base_capability, fitness_func)
        
        # Try small improvements in each parameter
        best_improvement = None
        best_fitness = current_fitness
        
        for param_name, param_value in base_capability.parameters.items():
            if isinstance(param_value, (int, float)):
                # Try increasing
                test_capability = Capability(
                    name=f"{base_capability.name}_gradient_test",
                    parameters=base_capability.parameters.copy()
                )
                test_capability.parameters[param_name] = param_value * 1.1
                
                test_fitness = await self._evaluate_fitness(test_capability, fitness_func)
                if test_fitness > best_fitness:
                    best_fitness = test_fitness
                    best_improvement = (param_name, param_value * 1.1, 'increase')
                
                # Try decreasing
                test_capability.parameters[param_name] = param_value * 0.9
                test_fitness = await self._evaluate_fitness(test_capability, fitness_func)
                if test_fitness > best_fitness:
                    best_fitness = test_fitness
                    best_improvement = (param_name, param_value * 0.9, 'decrease')
        
        # Apply best improvement if found
        if best_improvement:
            param_name, new_value, direction = best_improvement
            
            improved = Capability(
                name=f"{base_capability.name}_improved",
                description=base_capability.description,
                category=base_capability.category,
                parameters=base_capability.parameters.copy(),
                dependencies=base_capability.dependencies.copy(),
                generation=base_capability.generation + 1,
                parent_ids=[capability_id],
                fitness_score=best_fitness
            )
            
            improved.parameters[param_name] = new_value
            improved.mutation_history.append({
                'timestamp': datetime.now().isoformat(),
                'mutations': [{
                    'type': 'gradient_improvement',
                    'parameter': param_name,
                    'direction': direction,
                    'old_value': base_capability.parameters[param_name],
                    'new_value': new_value,
                    'fitness_improvement': best_fitness - current_fitness
                }]
            })
            
            self.capabilities[improved.id] = improved
            self.population.append(improved.id)
            self.performance_history[improved.id] = [best_fitness]
            
            self.logger.debug(f"Created improved capability {improved.id} with fitness {best_fitness:.3f}")
            return improved.id
        
        return None
    
    async def _curriculum_evolve_capability(self, capability_id: str) -> Optional[str]:
        """Evolve capability using curriculum learning approach"""
        if capability_id not in self.capabilities:
            return None
        
        base_capability = self.capabilities[capability_id]
        
        # Create a curriculum-evolved version with progressive difficulty
        evolved = Capability(
            name=f"{base_capability.name}_curriculum",
            description=f"Curriculum evolved version of {base_capability.description}",
            category=base_capability.category,
            parameters=base_capability.parameters.copy(),
            dependencies=base_capability.dependencies.copy(),
            generation=base_capability.generation + 1,
            parent_ids=[capability_id]
        )
        
        # Apply curriculum-based modifications
        # Start with easier tasks (lower complexity) and gradually increase
        complexity_factor = min(1.0, base_capability.generation * 0.1 + 0.1)
        
        for param_name, param_value in evolved.parameters.items():
            if isinstance(param_value, (int, float)):
                # Gradually increase complexity/capability
                evolved.parameters[param_name] = param_value * (1 + complexity_factor * 0.1)
        
        # Add curriculum metadata
        evolved.metadata['curriculum_level'] = complexity_factor
        evolved.metadata['curriculum_generation'] = base_capability.generation
        
        evolved.mutation_history.append({
            'timestamp': datetime.now().isoformat(),
            'mutations': [{
                'type': 'curriculum_evolution',
                'complexity_factor': complexity_factor,
                'modifications': 'Progressive difficulty increase'
            }]
        })
        
        self.capabilities[evolved.id] = evolved
        self.population.append(evolved.id)
        self.performance_history[evolved.id] = []
        
        self.logger.debug(f"Created curriculum-evolved capability {evolved.id}")
        return evolved.id
    
    async def _evaluate_fitness(self, capability: Capability, fitness_func: Callable) -> float:
        """Evaluate the fitness of a capability"""
        try:
            fitness = fitness_func(capability)
            
            # Store fitness score
            capability.fitness_score = fitness
            
            # Update performance history
            if capability.id in self.performance_history:
                self.performance_history[capability.id].append(fitness)
                
                # Keep only recent history
                if len(self.performance_history[capability.id]) > 100:
                    self.performance_history[capability.id] = self.performance_history[capability.id][-100:]
            
            return fitness
            
        except Exception as e:
            self.logger.error(f"Error evaluating fitness for capability {capability.id}: {str(e)}")
            return 0.0
    
    async def _evaluate_population_fitness(self, fitness_function: str) -> None:
        """Evaluate fitness for all capabilities in population"""
        if fitness_function not in self.fitness_functions:
            return
        
        fitness_func = self.fitness_functions[fitness_function]
        
        for capability_id in self.population:
            if capability_id in self.capabilities:
                capability = self.capabilities[capability_id]
                await self._evaluate_fitness(capability, fitness_func)
    
    async def _select_capabilities(self, strategy: EvolutionStrategy) -> List[str]:
        """Select capabilities for reproduction"""
        if not self.population:
            return []
        
        # Get capabilities with fitness scores
        capabilities_with_fitness = []
        for cap_id in self.population:
            if cap_id in self.capabilities:
                cap = self.capabilities[cap_id]
                capabilities_with_fitness.append((cap.fitness_score, cap_id))
        
        # Sort by fitness (descending)
        capabilities_with_fitness.sort(reverse=True)
        
        # Selection based on strategy
        if strategy == EvolutionStrategy.GENETIC_ALGORITHM:
            # Tournament selection
            selected = []
            tournament_size = min(5, len(capabilities_with_fitness))
            
            for _ in range(min(self.max_population_size // 2, len(capabilities_with_fitness))):
                tournament = random.sample(capabilities_with_fitness, tournament_size)
                winner = max(tournament, key=lambda x: x[0])
                selected.append(winner[1])
            
            return selected
        
        else:
            # Select top performers
            selection_size = min(self.max_population_size // 2, len(capabilities_with_fitness))
            return [cap_id for _, cap_id in capabilities_with_fitness[:selection_size]]
    
    async def _genetic_reproduction(self, selected: List[str]) -> List[str]:
        """Create offspring through genetic operations"""
        offspring = []
        
        for i in range(0, len(selected) - 1, 2):
            parent1_id = selected[i]
            parent2_id = selected[i + 1] if i + 1 < len(selected) else selected[0]
            
            # Crossover
            if random.random() < self.default_crossover_rate:
                offspring_id = await self._crossover_capabilities(parent1_id, parent2_id)
                if offspring_id:
                    offspring.append(offspring_id)
            
            # Mutation
            if random.random() < self.default_mutation_rate:
                mutated_id = await self._mutate_capability(parent1_id)
                if mutated_id:
                    offspring.append(mutated_id)
        
        return offspring
    
    async def _mutation_reproduction(self, selected: List[str]) -> List[str]:
        """Create offspring through mutation"""
        offspring = []
        
        for cap_id in selected:
            if random.random() < self.default_mutation_rate:
                mutated_id = await self._mutate_capability(cap_id)
                if mutated_id:
                    offspring.append(mutated_id)
        
        return offspring
    
    async def _replace_population(self, offspring: List[str]) -> List[str]:
        """Replace population with new generation"""
        # Combine current population and offspring
        combined = self.population + offspring
        
        # Get fitness scores
        capabilities_with_fitness = []
        for cap_id in combined:
            if cap_id in self.capabilities:
                cap = self.capabilities[cap_id]
                capabilities_with_fitness.append((cap.fitness_score, cap_id))
        
        # Sort by fitness and select best
        capabilities_with_fitness.sort(reverse=True)
        new_population = [cap_id for _, cap_id in capabilities_with_fitness[:self.max_population_size]]
        
        # Remove capabilities not in new population
        removed_capabilities = set(combined) - set(new_population)
        for cap_id in removed_capabilities:
            if cap_id in self.capabilities and cap_id not in self.elite:
                # Keep a few generations of history
                capability = self.capabilities[cap_id]
                if capability.generation < self.current_generation - 5:
                    del self.capabilities[cap_id]
                    if cap_id in self.performance_history:
                        del self.performance_history[cap_id]
        
        return new_population
    
    async def _update_elite(self) -> None:
        """Update elite capabilities"""
        # Get best performing capabilities
        capabilities_with_fitness = []
        for cap_id in self.population:
            if cap_id in self.capabilities:
                cap = self.capabilities[cap_id]
                capabilities_with_fitness.append((cap.fitness_score, cap_id))
        
        capabilities_with_fitness.sort(reverse=True)
        self.elite = [cap_id for _, cap_id in capabilities_with_fitness[:self.elite_size]]
    
    async def _calculate_generation_stats(self) -> Dict[str, Any]:
        """Calculate statistics for current generation"""
        if not self.population:
            return {}
        
        fitness_scores = []
        for cap_id in self.population:
            if cap_id in self.capabilities:
                fitness_scores.append(self.capabilities[cap_id].fitness_score)
        
        if not fitness_scores:
            return {}
        
        return {
            'avg_fitness': sum(fitness_scores) / len(fitness_scores),
            'max_fitness': max(fitness_scores),
            'min_fitness': min(fitness_scores),
            'fitness_std': math.sqrt(sum((f - sum(fitness_scores) / len(fitness_scores)) ** 2 
                                       for f in fitness_scores) / len(fitness_scores)),
            'diversity': len(set(fitness_scores)) / len(fitness_scores)
        }
    
    def get_best_capabilities(self, count: int = 10, category: Optional[str] = None) -> List[Capability]:
        """Get the best performing capabilities"""
        candidates = []
        
        for cap_id in self.population:
            if cap_id in self.capabilities:
                cap = self.capabilities[cap_id]
                if category is None or cap.category == category:
                    candidates.append(cap)
        
        candidates.sort(key=lambda x: x.fitness_score, reverse=True)
        return candidates[:count]
    
    def get_capability_lineage(self, capability_id: str) -> Dict[str, Any]:
        """Get the evolutionary lineage of a capability"""
        if capability_id not in self.capabilities:
            return {}
        
        capability = self.capabilities[capability_id]
        lineage = {
            'capability_id': capability_id,
            'generation': capability.generation,
            'fitness_score': capability.fitness_score,
            'parents': [],
            'mutations': capability.mutation_history
        }
        
        # Recursively get parent lineages
        for parent_id in capability.parent_ids:
            if parent_id in self.capabilities:
                parent_lineage = self.get_capability_lineage(parent_id)
                lineage['parents'].append(parent_lineage)
        
        return lineage
    
    def get_evolution_statistics(self) -> Dict[str, Any]:
        """Get comprehensive evolution statistics"""
        total_capabilities = len(self.capabilities)
        
        if total_capabilities == 0:
            return {'total_capabilities': 0}
        
        # Fitness statistics
        fitness_scores = [cap.fitness_score for cap in self.capabilities.values()]
        
        # Generation statistics
        generations = [cap.generation for cap in self.capabilities.values()]
        
        # Category distribution
        categories = {}
        for cap in self.capabilities.values():
            categories[cap.category] = categories.get(cap.category, 0) + 1
        
        return {
            'total_capabilities': total_capabilities,
            'current_generation': self.current_generation,
            'population_size': len(self.population),
            'elite_size': len(self.elite),
            'avg_fitness': sum(fitness_scores) / len(fitness_scores),
            'max_fitness': max(fitness_scores),
            'min_fitness': min(fitness_scores),
            'avg_generation': sum(generations) / len(generations),
            'max_generation': max(generations),
            'category_distribution': categories,
            'evolution_experiments': len(self.experiments),
            'total_mutations': sum(len(cap.mutation_history) for cap in self.capabilities.values())
        }
    
    async def export_evolution_data(self, file_path: str = None) -> Dict[str, Any]:
        """Export evolution data"""
        capabilities_data = {}
        for cap_id, capability in self.capabilities.items():
            capabilities_data[cap_id] = capability.to_dict()
        
        export_data = {
            'capabilities': capabilities_data,
            'population': self.population,
            'elite': self.elite,
            'current_generation': self.current_generation,
            'evolution_history': self.evolution_history,
            'performance_history': self.performance_history,
            'statistics': self.get_evolution_statistics(),
            'export_timestamp': datetime.now().isoformat()
        }
        
        if file_path:
            with open(file_path, 'w') as f:
                json.dump(export_data, f, indent=2)
        
        return export_data
    
    async def import_evolution_data(self, data: Dict[str, Any]) -> Dict[str, int]:
        """Import evolution data"""
        imported_counts = {'capabilities': 0, 'experiments': 0}
        
        # Import capabilities
        if 'capabilities' in data:
            for cap_id, cap_data in data['capabilities'].items():
                try:
                    capability = Capability.from_dict(cap_data)
                    self.capabilities[capability.id] = capability
                    imported_counts['capabilities'] += 1
                except Exception as e:
                    self.logger.error(f"Failed to import capability {cap_id}: {str(e)}")
        
        # Import other data
        if 'population' in data:
            self.population = data['population']
        
        if 'elite' in data:
            self.elite = data['elite']
        
        if 'current_generation' in data:
            self.current_generation = data['current_generation']
        
        if 'evolution_history' in data:
            self.evolution_history = data['evolution_history']
        
        if 'performance_history' in data:
            self.performance_history = data['performance_history']
        
        self.logger.info(f"Imported {imported_counts['capabilities']} capabilities")
        return imported_counts
