"""
Genetic algorithm engine for meme evolution.

This module implements sophisticated genetic algorithms combined with LLM-powered
mutations to evolve memes across generations with selection pressure and diversity.
"""

import random
import time
from typing import List, Dict, Callable, Optional, Tuple, Any
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
import asyncio

import numpy as np
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import openai

from .meme import Meme, MemeMetadata


@dataclass
class EvolutionParameters:
    """Parameters controlling meme evolution."""
    
    population_size: int = 50
    generations: int = 10
    mutation_rate: float = 0.1
    crossover_rate: float = 0.7
    elitism_rate: float = 0.1
    selection_pressure: float = 2.0
    diversity_weight: float = 0.3
    llm_mutation_rate: float = 0.2
    max_content_length: int = 500


class FitnessEvaluator:
    """Evaluates meme fitness using multiple criteria."""
    
    def __init__(self, weights: Optional[Dict[str, float]] = None):
        self.weights = weights or {
            "novelty": 0.3,
            "coherence": 0.25,
            "virality": 0.25,
            "diversity": 0.2
        }
    
    def evaluate(self, meme: Meme, population: List[Meme]) -> float:
        """Evaluate overall fitness of a meme."""
        scores = {
            "novelty": self._novelty_score(meme),
            "coherence": self._coherence_score(meme),
            "virality": self._virality_score(meme),
            "diversity": self._diversity_score(meme, population)
        }
        
        # Weighted combination
        fitness = sum(
            self.weights[criterion] * score
            for criterion, score in scores.items()
        )
        
        return max(0.0, min(1.0, fitness))
    
    def _novelty_score(self, meme: Meme) -> float:
        """Score based on novelty and uniqueness."""
        # Simple heuristic: longer, more complex content tends to be more novel
        content_complexity = len(set(meme.content.split())) / len(meme.content.split())
        length_factor = min(1.0, len(meme.content) / 200)
        
        return (content_complexity * 0.7 + length_factor * 0.3)
    
    def _coherence_score(self, meme: Meme) -> float:
        """Score based on semantic coherence."""
        if not meme.vector:
            return 0.5
        
        # Use vector magnitude as coherence proxy
        magnitude = np.linalg.norm(meme.vector.content_embedding)
        normalized_magnitude = min(1.0, magnitude / 100)
        
        return normalized_magnitude
    
    def _virality_score(self, meme: Meme) -> float:
        """Score based on potential for viral spread."""
        virality_keywords = [
            "amazing", "incredible", "shocking", "breakthrough", "revolutionary",
            "discover", "secret", "truth", "future", "quantum", "ai", "new"
        ]
        
        content_lower = meme.content.lower()
        keyword_count = sum(1 for keyword in virality_keywords if keyword in content_lower)
        
        # Factor in propagation history
        propagation_factor = min(1.0, meme.metadata.propagation_count / 100)
        keyword_factor = min(1.0, keyword_count / 5)
        
        return (keyword_factor * 0.7 + propagation_factor * 0.3)
    
    def _diversity_score(self, meme: Meme, population: List[Meme]) -> float:
        """Score based on diversity within population."""
        if not meme.vector or len(population) <= 1:
            return 0.5
        
        similarities = []
        for other_meme in population:
            if other_meme.meme_id != meme.meme_id and other_meme.vector:
                similarity = meme.vector.similarity(other_meme.vector)
                similarities.append(similarity)
        
        if not similarities:
            return 1.0
        
        # Higher diversity = lower average similarity
        avg_similarity = np.mean(similarities)
        diversity = 1.0 - avg_similarity
        
        return max(0.0, diversity)


class LLMMutator:
    """Uses LLMs to perform intelligent mutations on meme content."""
    
    def __init__(self, model_name: str = "gpt-3.5-turbo", use_local: bool = False):
        self.model_name = model_name
        self.use_local = use_local
        
        if use_local:
            self.tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
            self.model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
            self.generator = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)
    
    async def mutate_content(self, content: str, mutation_type: str = "creative") -> str:
        """Use LLM to mutate meme content intelligently."""
        mutation_prompts = {
            "creative": f"Rewrite this idea in a more creative and engaging way: {content}",
            "scientific": f"Express this concept using more scientific terminology: {content}",
            "poetic": f"Transform this into a more poetic or metaphorical expression: {content}",
            "simplified": f"Simplify this idea for broader understanding: {content}",
            "expanded": f"Expand on this concept with additional insights: {content}",
            "contrarian": f"Present a thoughtful alternative perspective on: {content}",
        }
        
        prompt = mutation_prompts.get(mutation_type, mutation_prompts["creative"])
        
        if self.use_local:
            return self._mutate_with_local_model(prompt)
        else:
            return await self._mutate_with_openai(prompt)
    
    def _mutate_with_local_model(self, prompt: str) -> str:
        """Mutate using local transformer model."""
        try:
            result = self.generator(prompt, max_length=150, num_return_sequences=1)
            return result[0]['generated_text'].replace(prompt, "").strip()
        except Exception as e:
            # Fallback to simple mutations
            return self._simple_mutation(prompt.split(": ")[-1])
    
    async def _mutate_with_openai(self, prompt: str) -> str:
        """Mutate using OpenAI API."""
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a creative AI that helps evolve ideas. Provide concise, engaging responses."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.8
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            # Fallback to simple mutations
            return self._simple_mutation(prompt.split(": ")[-1])
    
    def _simple_mutation(self, content: str) -> str:
        """Simple fallback mutation methods."""
        mutations = [
            lambda x: f"What if {x.lower()}?",
            lambda x: f"The future of {x.lower()}",
            lambda x: f"Rethinking {x.lower()}",
            lambda x: f"{x} - a new perspective",
            lambda x: f"Beyond {x.lower()}: next steps"
        ]
        
        mutation_func = random.choice(mutations)
        return mutation_func(content)


class GeneticEvolver:
    """
    Main genetic algorithm engine for meme evolution.
    
    Combines traditional genetic algorithms with LLM-powered mutations
    to evolve populations of memes over multiple generations.
    """
    
    def __init__(
        self,
        parameters: Optional[EvolutionParameters] = None,
        fitness_evaluator: Optional[FitnessEvaluator] = None,
        llm_mutator: Optional[LLMMutator] = None
    ):
        self.params = parameters or EvolutionParameters()
        self.fitness_evaluator = fitness_evaluator or FitnessEvaluator()
        self.llm_mutator = llm_mutator or LLMMutator()
        
        # Evolution history
        self.evolution_history: List[Dict[str, Any]] = []
        self.generation_stats: List[Dict[str, float]] = []
    
    async def evolve_population(
        self, 
        initial_memes: List[Meme],
        target_fitness: Optional[float] = None
    ) -> List[Meme]:
        """
        Evolve a population of memes over multiple generations.
        
        Args:
            initial_memes: Starting population
            target_fitness: Stop evolution if this fitness is reached
            
        Returns:
            Final evolved population
        """
        # Initialize population
        population = initial_memes.copy()
        
        # Pad population if needed
        while len(population) < self.params.population_size:
            # Clone and mutate existing memes
            base_meme = random.choice(initial_memes)
            mutated = base_meme.mutate(mutation_strength=0.2)
            population.append(mutated)
        
        # Evolution loop
        for generation in range(self.params.generations):
            print(f"Evolution Generation {generation + 1}/{self.params.generations}")
            
            # Evaluate fitness
            fitness_scores = []
            for meme in population:
                fitness = self.fitness_evaluator.evaluate(meme, population)
                meme.update_fitness(fitness)
                fitness_scores.append(fitness)
            
            # Record generation statistics
            gen_stats = {
                "generation": generation,
                "max_fitness": max(fitness_scores),
                "avg_fitness": np.mean(fitness_scores),
                "min_fitness": min(fitness_scores),
                "diversity": self._calculate_population_diversity(population)
            }
            self.generation_stats.append(gen_stats)
            
            # Check termination condition
            if target_fitness and gen_stats["max_fitness"] >= target_fitness:
                print(f"Target fitness {target_fitness} reached in generation {generation}")
                break
            
            # Selection
            selected_parents = self._selection(population, fitness_scores)
            
            # Create next generation
            next_generation = await self._create_next_generation(selected_parents)
            
            # Replace population
            population = next_generation
            
            # Record evolution step
            self.evolution_history.append({
                "generation": generation,
                "population_size": len(population),
                "stats": gen_stats,
                "best_meme_id": population[np.argmax(fitness_scores)].meme_id
            })
        
        return population
    
    def _selection(self, population: List[Meme], fitness_scores: List[float]) -> List[Meme]:
        """Select parents for reproduction using tournament selection."""
        num_parents = int(self.params.population_size * 0.8)  # 80% selected as parents
        selected = []
        
        # Elitism: always keep the best individuals
        num_elite = int(self.params.population_size * self.params.elitism_rate)
        if num_elite > 0:
            elite_indices = np.argsort(fitness_scores)[-num_elite:]
            selected.extend([population[i] for i in elite_indices])
        
        # Tournament selection for the rest
        tournament_size = max(2, int(self.params.selection_pressure))
        
        while len(selected) < num_parents:
            # Select random individuals for tournament
            tournament_indices = random.sample(range(len(population)), tournament_size)
            tournament_fitness = [fitness_scores[i] for i in tournament_indices]
            
            # Winner is the one with highest fitness
            winner_idx = tournament_indices[np.argmax(tournament_fitness)]
            selected.append(population[winner_idx])
        
        return selected
    
    async def _create_next_generation(self, parents: List[Meme]) -> List[Meme]:
        """Create next generation through crossover and mutation."""
        next_gen = []
        
        # Keep elite parents
        num_elite = int(len(parents) * self.params.elitism_rate)
        if num_elite > 0:
            elite_parents = sorted(parents, key=lambda m: m.vector.fitness_score if m.vector else 0, reverse=True)
            next_gen.extend(elite_parents[:num_elite])
        
        # Generate offspring
        while len(next_gen) < self.params.population_size:
            # Select two parents
            parent1, parent2 = random.sample(parents, 2)
            
            # Crossover
            if random.random() < self.params.crossover_rate:
                child = parent1.crossover(parent2)
            else:
                child = random.choice([parent1, parent2])
            
            # Standard mutation
            if random.random() < self.params.mutation_rate:
                child = child.mutate(mutation_strength=0.1)
            
            # LLM-powered mutation
            if random.random() < self.params.llm_mutation_rate:
                child = await self._llm_mutate(child)
            
            next_gen.append(child)
        
        return next_gen[:self.params.population_size]
    
    async def _llm_mutate(self, meme: Meme) -> Meme:
        """Apply LLM-powered mutation to a meme."""
        mutation_types = ["creative", "scientific", "poetic", "simplified", "expanded"]
        mutation_type = random.choice(mutation_types)
        
        try:
            new_content = await self.llm_mutator.mutate_content(meme.content, mutation_type)
            
            # Create new metadata
            new_metadata = MemeMetadata(
                author=meme.metadata.author,
                domain=meme.metadata.domain,
                generation=meme.metadata.generation + 1,
                parent_ids=[meme.meme_id],
                mutation_type=f"llm_{mutation_type}",
                tags=meme.metadata.tags.copy()
            )
            
            # Create mutated meme
            mutated_meme = Meme(
                content=new_content[:self.params.max_content_length],
                metadata=new_metadata
            )
            
            return mutated_meme
            
        except Exception as e:
            # Fallback to standard mutation
            return meme.mutate()
    
    def _calculate_population_diversity(self, population: List[Meme]) -> float:
        """Calculate average diversity of the population."""
        if len(population) <= 1:
            return 0.0
        
        similarities = []
        for i, meme1 in enumerate(population):
            for meme2 in population[i+1:]:
                if meme1.vector and meme2.vector:
                    similarity = meme1.vector.similarity(meme2.vector)
                    similarities.append(similarity)
        
        if not similarities:
            return 0.0
        
        # Diversity is inverse of average similarity
        avg_similarity = np.mean(similarities)
        return 1.0 - avg_similarity
    
    def get_evolution_summary(self) -> Dict[str, Any]:
        """Get summary of evolution process."""
        if not self.generation_stats:
            return {}
        
        return {
            "total_generations": len(self.generation_stats),
            "initial_fitness": self.generation_stats[0]["avg_fitness"],
            "final_fitness": self.generation_stats[-1]["avg_fitness"],
            "fitness_improvement": (
                self.generation_stats[-1]["avg_fitness"] - 
                self.generation_stats[0]["avg_fitness"]
            ),
            "peak_fitness": max(stat["max_fitness"] for stat in self.generation_stats),
            "final_diversity": self.generation_stats[-1]["diversity"],
            "convergence_rate": self._calculate_convergence_rate()
        }
    
    def _calculate_convergence_rate(self) -> float:
        """Calculate how quickly the population converged."""
        if len(self.generation_stats) < 2:
            return 0.0
        
        fitness_changes = []
        for i in range(1, len(self.generation_stats)):
            change = abs(
                self.generation_stats[i]["avg_fitness"] - 
                self.generation_stats[i-1]["avg_fitness"]
            )
            fitness_changes.append(change)
        
        # Convergence rate is average change per generation
        return np.mean(fitness_changes)
    
    def export_evolution_data(self) -> Dict[str, Any]:
        """Export complete evolution data for analysis."""
        return {
            "parameters": self.params.__dict__,
            "generation_stats": self.generation_stats,
            "evolution_history": self.evolution_history,
            "summary": self.get_evolution_summary()
        }
