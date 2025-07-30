"""
Main Q-Memetic AI Engine.

This is the central orchestrator that combines meme evolution, entanglement,
licensing, and visualization into a unified quantum-inspired memetic system.

🔐 STRICT LICENSING: QuantumMeta license required for all operations
Grace Period: 24 hours only
Support: bajpaikrishna715@gmail.com
"""

import asyncio
import time
from typing import List, Dict, Optional, Any, Union
from pathlib import Path
import logging

import numpy as np
import networkx as nx

from ..licensing.manager import (
    LicenseManager, 
    QMemeticLicenseError,
    requires_license,
    validate_qmemetic_license
)
from ..core.meme import Meme, MemeMetadata
from ..core.entanglement import QuantumEntangler
from ..core.evolution import GeneticEvolver, EvolutionParameters
from ..federation.client import FederatedClient
from ..visualization.noosphere import NoosphereVisualizer
from ..cognitive.models import CognitiveFingerprint
from ..utils.security import SecurityManager
from ..utils.persistence import DataPersistence


@LicenseManager.licensed_class(tier_required="core")
class MemeticEngine:
    """
    Main Q-Memetic AI Engine.
    
    🔐 STRICT LICENSING ENFORCED
    - Core tier: Basic evolution, visualization
    - Pro tier: Entanglement, quantum walks, federation
    - Enterprise tier: Multimodal, custom plugins, unlimited scale
    
    Grace period: 24 hours only
    License required for ALL operations
    """
    
    def __init__(
        self,
        license_key: Optional[str] = None,
        federated_mode: bool = False,
        data_dir: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize the Q-Memetic AI Engine.
        
        🔐 LICENSE REQUIRED: QuantumMeta license validated on initialization
        
        Args:
            license_key: QuantumMeta license key (REQUIRED)
            federated_mode: Enable federated learning (requires Pro+ license)
            data_dir: Directory for data persistence
            **kwargs: Additional configuration parameters
            
        Raises:
            QMemeticLicenseError: If license validation fails
        """
        # Validate license immediately - STRICT ENFORCEMENT
        validate_qmemetic_license()
        
        # Configuration
        self.federated_mode = federated_mode
        self.config = kwargs
        
        # Initialize logging
        self._setup_logging()
        
        # License manager with strict enforcement
        self.license_manager = LicenseManager(license_key=license_key)
        
        # Check federation license if requested
        if federated_mode:
            self.license_manager.require_feature("federation_basic")
        
        # Initialize data persistence
        self.data_persistence = DataPersistence(data_dir or "./qmemetic_data")
        
        # Core engines (license-protected)
        self.entangler = QuantumEntangler(**kwargs.get("entanglement_config", {}))
        self.evolver = GeneticEvolver()
        self.visualizer = NoosphereVisualizer()
        
        # Federated components (Pro+ license required)
        self.federated_client = None
        if federated_mode:
            self.federated_client = FederatedClient(**kwargs.get("federation_config", {}))
        
        # Security
        self.security_manager = SecurityManager()
        
        # Internal state
        self.meme_registry: Dict[str, Meme] = {}
        self.session_id = self.security_manager.generate_session_id()
        self.cognitive_models: Dict[str, CognitiveFingerprint] = {}
        
        # Show license status
        self.license_manager.show_license_info()
        
        # Load persisted data
        self._load_persisted_data()
        
        logging.info(f"Q-Memetic AI Engine initialized (Session: {self.session_id[:8]})")
    
    def _setup_logging(self):
        """Setup logging configuration."""
        log_level = logging.INFO
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger("QMemeticAI")
    
    def _validate_license(self):
        """Validate license and set feature availability."""
        try:
            self.license_info = self.license_manager.get_license_status()
            self.logger.info(f"License validated: {self.license_info.get('tier', 'unknown')}")
        except QMemeticLicenseError as e:
            self.logger.error(f"License validation failed: {e}")
            raise e
    
    def _load_persisted_data(self):
        """Load previously saved memes and models."""
        try:
            saved_memes = self.data_persistence.load_memes()
            for meme_data in saved_memes:
                meme = Meme.from_dict(meme_data)
                self.meme_registry[meme.meme_id] = meme
            
            saved_models = self.data_persistence.load_cognitive_models()
            self.cognitive_models.update(saved_models)
            
            self.logger.info(f"Loaded {len(self.meme_registry)} memes and {len(self.cognitive_models)} cognitive models")
        except Exception as e:
            self.logger.warning(f"Could not load persisted data: {e}")
    
    @requires_license(features=["basic_evolution"])
    def create_meme(
        self,
        content: str,
        author: Optional[str] = None,
        domain: Optional[str] = None,
        tags: Optional[List[str]] = None,
        **metadata_kwargs
    ) -> Meme:
        """
        Create a new meme with automatic vector generation.
        
        🔐 LICENSE: Core tier required
        
        Args:
            content: The meme content
            author: Author identifier
            domain: Domain/category of the meme
            tags: List of tags
            **metadata_kwargs: Additional metadata
            
        Returns:
            Created Meme object
            
        Raises:
            QMemeticLicenseError: If Core license not available
        """
        metadata = MemeMetadata(
            author=author,
            domain=domain,
            tags=tags or [],
            network_id=self.session_id,
            **metadata_kwargs
        )
        
        meme = Meme(content=content, metadata=metadata)
        self.meme_registry[meme.meme_id] = meme
        
        # Save to persistence
        self.data_persistence.save_meme(meme)
        
        self.logger.info(f"Created meme: {meme.meme_id}")
        return meme
    
    @requires_license(features=["basic_evolution"])
    def evolve(
        self,
        memes: Union[List[Meme], Meme],
        generations: int = 5,
        population_size: int = 20,
        **evolution_kwargs
    ) -> List[Meme]:
        """
        Evolve memes using genetic algorithms.
        
        Args:
            memes: Initial memes (single meme or list)
            generations: Number of evolution generations
            population_size: Size of evolution population
            **evolution_kwargs: Additional evolution parameters
            
        Returns:
            List of evolved memes
        """
        if isinstance(memes, Meme):
            memes = [memes]
        
        # Setup evolution parameters
        params = EvolutionParameters(
            generations=generations,
            population_size=population_size,
            **evolution_kwargs
        )
        
        evolver = GeneticEvolver(parameters=params)
        
        # Run evolution
        evolved_memes = asyncio.run(evolver.evolve_population(memes))
        
        # Register evolved memes
        for meme in evolved_memes:
            self.meme_registry[meme.meme_id] = meme
            self.data_persistence.save_meme(meme)
        
        self.logger.info(f"Evolution complete: {len(evolved_memes)} memes in final population")
        return evolved_memes
    
    @requires_license(features=["entanglement"])
    def entangle(
        self,
        memes: Optional[List[Meme]] = None,
        force_recalculate: bool = False
    ) -> Dict[str, Any]:
        """
        Create quantum-inspired entanglement network between memes.
        
        🔐 LICENSE: Pro tier required (entanglement feature)
        
        Args:
            memes: Memes to entangle (defaults to all registered memes)
            force_recalculate: Force recalculation of entanglements
            
        Returns:
            Entanglement network data
            
        Raises:
            QMemeticLicenseError: If Pro license not available
        """
        if memes is None:
            memes = list(self.meme_registry.values())
        
        # Create entanglement network
        graph = self.entangler.entangle_memes(memes, force_recalculate)
        
        # Export network data
        network_data = self.entangler.export_entanglement_data()
        
        self.logger.info(f"Entanglement network created: {len(graph.nodes())} nodes, {len(graph.edges())} edges")
        return network_data
    
    @requires_license(features=["quantum_walk"])
    def quantum_walk(
        self,
        start_meme: Union[str, Meme],
        steps: int = 100,
        teleport_probability: float = 0.15
    ) -> List[str]:
        """
        Perform quantum walk through entanglement network.
        
        🔐 LICENSE: Pro tier required (quantum walk feature)
        
        Args:
            start_meme: Starting meme (ID or object)
            steps: Number of walk steps
            teleport_probability: Quantum teleportation probability
            
        Returns:
            List of visited meme IDs
            
        Raises:
            QMemeticLicenseError: If Pro license not available
        """
        start_id = start_meme.meme_id if isinstance(start_meme, Meme) else start_meme
        
        walk_path = self.entangler.quantum_walk(
            start_meme_id=start_id,
            steps=steps,
            teleport_probability=teleport_probability
        )
        
        self.logger.info(f"Quantum walk completed: {len(walk_path)} steps")
        return walk_path
    
    @requires_license(features=["visualization"])
    def visualize_noosphere(
        self,
        network_data: Optional[Dict] = None,
        layout: str = "force_directed",
        save_path: Optional[str] = None,
        interactive: bool = True
    ) -> str:
        """
        Visualize the noosphere (global mind map).
        
        🔐 LICENSE: Core tier required (visualization feature)
        
        Args:
            network_data: Entanglement network data
            layout: Visualization layout algorithm
            save_path: Path to save visualization
            interactive: Create interactive visualization
            
        Returns:
            Path to generated visualization
            
        Raises:
            QMemeticLicenseError: If Core license not available
        """
        if network_data is None:
            network_data = self.entangle()
        
        viz_path = self.visualizer.create_noosphere_visualization(
            network_data=network_data,
            layout=layout,
            save_path=save_path,
            interactive=interactive
        )
        
        self.logger.info(f"Noosphere visualization created: {viz_path}")
        return viz_path
    
    @requires_license(features=["federation_advanced"])
    async def federated_sync(
        self,
        node_id: Optional[str] = None,
        sync_mode: str = "bidirectional"
    ) -> Dict[str, Any]:
        """
        Synchronize with federated memetic network.
        
        🔐 LICENSE: Enterprise tier required (advanced federation)
        
        Args:
            node_id: Target node ID (None for all)
            sync_mode: Synchronization mode
            
        Returns:
            Synchronization results
            
        Raises:
            QMemeticLicenseError: If Enterprise license not available
        """
        if not self.federated_client:
            raise ValueError("Federated mode not enabled")
        
        sync_results = await self.federated_client.sync_network(
            local_memes=list(self.meme_registry.values()),
            node_id=node_id,
            sync_mode=sync_mode
        )
        
        # Update local registry with synchronized memes
        for meme_data in sync_results.get("received_memes", []):
            meme = Meme.from_dict(meme_data)
            self.meme_registry[meme.meme_id] = meme
            self.data_persistence.save_meme(meme)
        
        self.logger.info(f"Federated sync completed: {sync_results}")
        return sync_results
    
    def add_cognitive_model(
        self,
        user_id: str,
        cognitive_data: Dict[str, Any]
    ) -> CognitiveFingerprint:
        """
        Add or update cognitive model for a user.
        
        Args:
            user_id: User identifier
            cognitive_data: Cognitive fingerprint data
            
        Returns:
            Created CognitiveFingerprint
        """
        fingerprint = CognitiveFingerprint(user_id=user_id, **cognitive_data)
        self.cognitive_models[user_id] = fingerprint
        
        # Save to persistence
        self.data_persistence.save_cognitive_model(user_id, fingerprint)
        
        self.logger.info(f"Cognitive model added for user: {user_id}")
        return fingerprint
    
    def personalized_diffusion(
        self,
        meme: Meme,
        user_id: str,
        adaptation_strength: float = 0.5
    ) -> Meme:
        """
        Adapt meme for personalized diffusion based on cognitive model.
        
        Args:
            meme: Original meme
            user_id: Target user
            adaptation_strength: Strength of adaptation
            
        Returns:
            Adapted meme
        """
        if user_id not in self.cognitive_models:
            self.logger.warning(f"No cognitive model for user {user_id}, returning original meme")
            return meme
        
        cognitive_model = self.cognitive_models[user_id]
        adapted_meme = cognitive_model.adapt_meme(meme, adaptation_strength)
        
        # Register adapted meme
        self.meme_registry[adapted_meme.meme_id] = adapted_meme
        self.data_persistence.save_meme(adapted_meme)
        
        self.logger.info(f"Meme adapted for user {user_id}: {adapted_meme.meme_id}")
        return adapted_meme
    
    def get_meme_analytics(self, meme_id: str) -> Dict[str, Any]:
        """Get comprehensive analytics for a specific meme."""
        if meme_id not in self.meme_registry:
            raise ValueError(f"Meme {meme_id} not found")
        
        meme = self.meme_registry[meme_id]
        
        analytics = {
            "basic_info": {
                "meme_id": meme.meme_id,
                "content_length": len(meme.content),
                "generation": meme.metadata.generation,
                "author": meme.metadata.author,
                "domain": meme.metadata.domain,
                "age_hours": (time.time() - meme.metadata.timestamp) / 3600,
            },
            "fitness_metrics": {
                "current_fitness": meme.vector.fitness_score if meme.vector else 0,
                "propagation_count": meme.metadata.propagation_count,
                "entanglement_count": meme.metadata.entanglement_count,
            },
            "network_position": self._analyze_network_position(meme_id),
            "evolution_lineage": self._trace_evolution_lineage(meme_id),
        }
        
        return analytics
    
    def _analyze_network_position(self, meme_id: str) -> Dict[str, Any]:
        """Analyze meme's position in entanglement network."""
        if meme_id not in self.entangler.graph:
            return {"status": "not_entangled"}
        
        graph = self.entangler.graph
        
        return {
            "degree": graph.degree(meme_id),
            "clustering_coefficient": nx.clustering(graph, meme_id),
            "betweenness_centrality": nx.betweenness_centrality(graph).get(meme_id, 0),
            "pagerank": nx.pagerank(graph).get(meme_id, 0),
            "neighbors": list(graph.neighbors(meme_id)),
        }
    
    def _trace_evolution_lineage(self, meme_id: str) -> Dict[str, Any]:
        """Trace the evolutionary lineage of a meme."""
        if meme_id not in self.meme_registry:
            return {}
        
        meme = self.meme_registry[meme_id]
        
        # Find ancestors
        ancestors = []
        for parent_id in meme.metadata.parent_ids:
            if parent_id in self.meme_registry:
                ancestors.append({
                    "meme_id": parent_id,
                    "content_preview": self.meme_registry[parent_id].content[:50] + "...",
                    "generation": self.meme_registry[parent_id].metadata.generation,
                })
        
        # Find descendants
        descendants = []
        for other_meme in self.meme_registry.values():
            if meme_id in other_meme.metadata.parent_ids:
                descendants.append({
                    "meme_id": other_meme.meme_id,
                    "content_preview": other_meme.content[:50] + "...",
                    "generation": other_meme.metadata.generation,
                })
        
        return {
            "ancestors": ancestors,
            "descendants": descendants,
            "family_size": len(ancestors) + len(descendants) + 1,
            "mutation_type": meme.metadata.mutation_type,
        }
    
    def export_session_data(self, file_path: Optional[str] = None) -> str:
        """Export complete session data for backup or analysis."""
        export_data = {
            "session_info": {
                "session_id": self.session_id,
                "federated_mode": self.federated_mode,
                "timestamp": time.time(),
            },
            "memes": [meme.to_dict() for meme in self.meme_registry.values()],
            "entanglement_network": self.entangler.export_entanglement_data(),
            "cognitive_models": {
                user_id: model.to_dict() 
                for user_id, model in self.cognitive_models.items()
            },
            "license_info": self.license_info.to_dict() if hasattr(self.license_info, 'to_dict') else str(self.license_info),
        }
        
        if file_path is None:
            file_path = f"qmemetic_session_{self.session_id[:8]}_{int(time.time())}.json"
        
        self.data_persistence.export_data(export_data, file_path)
        
        self.logger.info(f"Session data exported to: {file_path}")
        return file_path
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status and health metrics."""
        return {
            "system_info": {
                "session_id": self.session_id,
                "uptime_seconds": time.time() - getattr(self, '_start_time', time.time()),
                "federated_mode": self.federated_mode,
            },
            "license_status": {
                "tier": self.license_info.tier if hasattr(self.license_info, 'tier') else 'unknown',
                "valid": True,  # If we got this far, license is valid
                "features_available": self.license_manager.get_available_features(),
            },
            "data_metrics": {
                "total_memes": len(self.meme_registry),
                "entanglement_edges": len(self.entangler.graph.edges()),
                "cognitive_models": len(self.cognitive_models),
                "average_fitness": np.mean([
                    meme.vector.fitness_score for meme in self.meme_registry.values()
                    if meme.vector
                ]) if self.meme_registry else 0,
            },
            "network_health": {
                "graph_density": nx.density(self.entangler.graph) if self.entangler.graph.nodes() else 0,
                "connected_components": nx.number_connected_components(self.entangler.graph),
                "average_clustering": nx.average_clustering(self.entangler.graph),
            }
        }
    
    def __enter__(self):
        """Context manager entry."""
        self._start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup."""
        try:
            # Save session data
            self.export_session_data()
            
            # Close federated connections
            if self.federated_client:
                asyncio.run(self.federated_client.disconnect())
            
            self.logger.info("Q-Memetic AI Engine session ended")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
    
    def __repr__(self) -> str:
        return (
            f"MemeticEngine(session={self.session_id[:8]}, "
            f"memes={len(self.meme_registry)}, "
            f"entanglements={len(self.entangler.graph.edges())})"
        )
