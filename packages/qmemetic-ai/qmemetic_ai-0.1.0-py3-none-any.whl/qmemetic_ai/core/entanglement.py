"""
Quantum-inspired entanglement system for memes.

This module implements quantum-style entanglement between memes using
probabilistic graph networks, attention mechanisms, and correlation analysis.
"""

import math
import random
from typing import Dict, List, Tuple, Set, Optional
from collections import defaultdict

import numpy as np
import networkx as nx
from scipy.spatial.distance import cosine
from sklearn.cluster import SpectralClustering
from dataclasses import dataclass
from time import time

from .meme import Meme, MemeVector


@dataclass
class EntanglementEdge:
    """Represents an entanglement connection between two memes."""
    
    source_id: str
    target_id: str
    strength: float
    correlation_type: str
    confidence: float
    timestamp: float
    metadata: Dict = None


class QuantumEntangler:
    """
    Quantum-inspired entanglement engine for meme networks.
    
    Implements probabilistic entanglement using:
    - Attention-weighted similarity
    - Quantum walk algorithms
    - Spectral clustering for entanglement groups
    """
    
    def __init__(
        self,
        entanglement_threshold: float = 0.6,
        max_entanglements_per_meme: int = 10,
        decay_rate: float = 0.95,
        quantum_noise: float = 0.1
    ):
        self.entanglement_threshold = entanglement_threshold
        self.max_entanglements_per_meme = max_entanglements_per_meme
        self.decay_rate = decay_rate
        self.quantum_noise = quantum_noise
        
        # Entanglement network
        self.graph = nx.Graph()
        self.entanglement_history: List[EntanglementEdge] = []
        self.correlation_cache: Dict[Tuple[str, str], float] = {}
    
    def entangle_memes(
        self, 
        memes: List[Meme], 
        force_recalculate: bool = False
    ) -> nx.Graph:
        """
        Create entanglement network between memes.
        
        Args:
            memes: List of memes to entangle
            force_recalculate: Whether to recalculate existing entanglements
            
        Returns:
            NetworkX graph with entanglement relationships
        """
        # Add memes as nodes
        for meme in memes:
            if meme.meme_id not in self.graph:
                self.graph.add_node(
                    meme.meme_id,
                    content=meme.content,
                    fitness=meme.vector.fitness_score if meme.vector else 0,
                    generation=meme.metadata.generation,
                    domain=meme.metadata.domain
                )
        
        # Calculate pairwise entanglements
        for i, meme1 in enumerate(memes):
            for j, meme2 in enumerate(memes[i+1:], i+1):
                edge_key = (meme1.meme_id, meme2.meme_id)
                
                if not force_recalculate and edge_key in self.correlation_cache:
                    entanglement_strength = self.correlation_cache[edge_key]
                else:
                    entanglement_strength = self._calculate_entanglement(meme1, meme2)
                    self.correlation_cache[edge_key] = entanglement_strength
                
                if entanglement_strength > self.entanglement_threshold:
                    self._create_entanglement(meme1, meme2, entanglement_strength)
        
        return self.graph
    
    def _calculate_entanglement(self, meme1: Meme, meme2: Meme) -> float:
        """Calculate quantum-inspired entanglement strength between two memes."""
        if not meme1.vector or not meme2.vector:
            return 0.0
        
        # Base similarity
        base_similarity = meme1.vector.similarity(meme2.vector)
        
        # Attention mechanism - weight by fitness and generation
        attention_weight = self._calculate_attention_weight(meme1, meme2)
        
        # Quantum coherence factor
        coherence = self._calculate_quantum_coherence(meme1, meme2)
        
        # Historical correlation
        historical_factor = self._get_historical_correlation(meme1.meme_id, meme2.meme_id)
        
        # Combine factors with quantum-inspired formula
        entanglement = (
            base_similarity * 0.4 +
            attention_weight * 0.3 +
            coherence * 0.2 +
            historical_factor * 0.1
        )
        
        # Add quantum noise
        noise = np.random.normal(0, self.quantum_noise)
        entanglement = max(0, min(1, entanglement + noise))
        
        return entanglement
    
    def _calculate_attention_weight(self, meme1: Meme, meme2: Meme) -> float:
        """Calculate attention-based weighting between memes."""
        # Fitness-based attention
        fitness1 = meme1.vector.fitness_score if meme1.vector else 0
        fitness2 = meme2.vector.fitness_score if meme2.vector else 0
        fitness_attention = (fitness1 + fitness2) / 2
        
        # Generation proximity (newer generations have higher attention)
        gen_diff = abs(meme1.metadata.generation - meme2.metadata.generation)
        generation_attention = math.exp(-gen_diff / 10)  # Exponential decay
        
        # Domain similarity
        domain_attention = 1.0 if meme1.metadata.domain == meme2.metadata.domain else 0.5
        
        return (fitness_attention * 0.5 + generation_attention * 0.3 + domain_attention * 0.2)
    
    def _calculate_quantum_coherence(self, meme1: Meme, meme2: Meme) -> float:
        """Calculate quantum coherence between meme states."""
        if not meme1.vector or not meme2.vector:
            return 0.0
        
        # Phase alignment (simplified quantum-inspired calculation)
        vec1 = np.array(meme1.vector.content_embedding)
        vec2 = np.array(meme2.vector.content_embedding)
        
        # Calculate phase difference
        phase_diff = np.angle(np.sum(vec1 * np.exp(1j * vec2)))
        coherence = math.cos(phase_diff) ** 2  # Probability amplitude squared
        
        return coherence
    
    def _get_historical_correlation(self, meme_id1: str, meme_id2: str) -> float:
        """Get historical correlation factor between two memes."""
        # Count previous interactions
        interactions = 0
        for edge in self.entanglement_history:
            if ((edge.source_id == meme_id1 and edge.target_id == meme_id2) or
                (edge.source_id == meme_id2 and edge.target_id == meme_id1)):
                interactions += 1
        
        # Convert to correlation factor with diminishing returns
        return min(1.0, interactions / 10)
    
    def _create_entanglement(self, meme1: Meme, meme2: Meme, strength: float):
        """Create entanglement edge between two memes."""
        # Determine correlation type
        correlation_type = self._classify_correlation(meme1, meme2, strength)
        
        # Create entanglement edge
        edge = EntanglementEdge(
            source_id=meme1.meme_id,
            target_id=meme2.meme_id,
            strength=strength,
            correlation_type=correlation_type,
            confidence=min(1.0, strength * 1.2),
            timestamp=time.time(),
            metadata={
                "fitness_diff": abs(
                    (meme1.vector.fitness_score if meme1.vector else 0) -
                    (meme2.vector.fitness_score if meme2.vector else 0)
                ),
                "generation_diff": abs(meme1.metadata.generation - meme2.metadata.generation),
                "domain_match": meme1.metadata.domain == meme2.metadata.domain
            }
        )
        
        # Add to graph
        self.graph.add_edge(
            meme1.meme_id,
            meme2.meme_id,
            weight=strength,
            correlation_type=correlation_type,
            confidence=edge.confidence,
            timestamp=edge.timestamp
        )
        
        # Store in history
        self.entanglement_history.append(edge)
        
        # Update meme entanglement counts
        meme1.metadata.entanglement_count += 1
        meme2.metadata.entanglement_count += 1
    
    def _classify_correlation(self, meme1: Meme, meme2: Meme, strength: float) -> str:
        """Classify the type of correlation between memes."""
        if strength > 0.9:
            return "quantum_superposition"
        elif strength > 0.8:
            return "strong_entanglement"
        elif strength > 0.7:
            return "resonance"
        elif strength > 0.6:
            return "weak_correlation"
        else:
            return "background_noise"
    
    def quantum_walk(
        self, 
        start_meme_id: str, 
        steps: int = 100, 
        teleport_probability: float = 0.15
    ) -> List[str]:
        """
        Perform quantum walk on entanglement network.
        
        Args:
            start_meme_id: Starting meme for the walk
            steps: Number of walk steps
            teleport_probability: Probability of quantum teleportation
            
        Returns:
            List of visited meme IDs
        """
        if start_meme_id not in self.graph:
            raise ValueError(f"Meme {start_meme_id} not in entanglement network")
        
        walk_path = [start_meme_id]
        current_meme = start_meme_id
        
        for _ in range(steps):
            # Quantum teleportation (random jump)
            if random.random() < teleport_probability:
                current_meme = random.choice(list(self.graph.nodes()))
                walk_path.append(current_meme)
                continue
            
            # Get neighbors with entanglement weights
            neighbors = list(self.graph.neighbors(current_meme))
            if not neighbors:
                # No neighbors, random teleport
                current_meme = random.choice(list(self.graph.nodes()))
                walk_path.append(current_meme)
                continue
            
            # Weight neighbors by entanglement strength
            weights = []
            for neighbor in neighbors:
                edge_data = self.graph[current_meme][neighbor]
                weights.append(edge_data.get('weight', 0.5))
            
            # Quantum probability distribution
            probabilities = np.array(weights) ** 2  # Quantum amplitude squared
            probabilities /= probabilities.sum()
            
            # Choose next meme
            current_meme = np.random.choice(neighbors, p=probabilities)
            walk_path.append(current_meme)
        
        return walk_path
    
    def find_entanglement_clusters(
        self, 
        n_clusters: int = 5, 
        min_cluster_size: int = 3
    ) -> Dict[int, List[str]]:
        """
        Find clusters of strongly entangled memes using spectral clustering.
        
        Args:
            n_clusters: Number of clusters to find
            min_cluster_size: Minimum size for a valid cluster
            
        Returns:
            Dictionary mapping cluster ID to list of meme IDs
        """
        if len(self.graph.nodes()) < n_clusters:
            return {}
        
        # Create adjacency matrix
        nodes = list(self.graph.nodes())
        node_to_idx = {node: i for i, node in enumerate(nodes)}
        
        adjacency_matrix = np.zeros((len(nodes), len(nodes)))
        for edge in self.graph.edges(data=True):
            i, j = node_to_idx[edge[0]], node_to_idx[edge[1]]
            weight = edge[2].get('weight', 0.5)
            adjacency_matrix[i][j] = weight
            adjacency_matrix[j][i] = weight
        
        # Spectral clustering
        clustering = SpectralClustering(
            n_clusters=n_clusters,
            affinity='precomputed',
            random_state=42
        )
        
        cluster_labels = clustering.fit_predict(adjacency_matrix)
        
        # Group memes by cluster
        clusters = defaultdict(list)
        for node, cluster_id in zip(nodes, cluster_labels):
            clusters[cluster_id].append(node)
        
        # Filter by minimum cluster size
        valid_clusters = {
            cluster_id: memes for cluster_id, memes in clusters.items()
            if len(memes) >= min_cluster_size
        }
        
        return valid_clusters
    
    def get_entanglement_strength(self, meme_id1: str, meme_id2: str) -> float:
        """Get entanglement strength between two specific memes."""
        if self.graph.has_edge(meme_id1, meme_id2):
            return self.graph[meme_id1][meme_id2].get('weight', 0.0)
        return 0.0
    
    def get_most_entangled_memes(self, n: int = 10) -> List[Tuple[str, float]]:
        """Get memes with highest total entanglement strength."""
        meme_entanglement = defaultdict(float)
        
        for edge in self.graph.edges(data=True):
            weight = edge[2].get('weight', 0.5)
            meme_entanglement[edge[0]] += weight
            meme_entanglement[edge[1]] += weight
        
        # Sort by total entanglement
        sorted_memes = sorted(
            meme_entanglement.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return sorted_memes[:n]
    
    def decay_entanglements(self):
        """Apply time-based decay to entanglement strengths."""
        edges_to_remove = []
        
        for edge in self.graph.edges(data=True):
            current_weight = edge[2].get('weight', 0.5)
            new_weight = current_weight * self.decay_rate
            
            if new_weight < self.entanglement_threshold:
                edges_to_remove.append((edge[0], edge[1]))
            else:
                self.graph[edge[0]][edge[1]]['weight'] = new_weight
        
        # Remove weak entanglements
        self.graph.remove_edges_from(edges_to_remove)
    
    def export_entanglement_data(self) -> Dict:
        """Export entanglement network data for visualization."""
        return {
            "nodes": [
                {
                    "id": node,
                    "data": data
                }
                for node, data in self.graph.nodes(data=True)
            ],
            "edges": [
                {
                    "source": edge[0],
                    "target": edge[1],
                    "data": edge[2]
                }
                for edge in self.graph.edges(data=True)
            ],
            "statistics": {
                "total_nodes": len(self.graph.nodes()),
                "total_edges": len(self.graph.edges()),
                "average_entanglement": np.mean([
                    edge[2].get('weight', 0) for edge in self.graph.edges(data=True)
                ]) if self.graph.edges() else 0,
                "clustering_coefficient": nx.average_clustering(self.graph),
                "density": nx.density(self.graph)
            }
        }
