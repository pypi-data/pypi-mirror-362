"""
Cognitive models for personalized meme diffusion.

This module implements cognitive fingerprinting and adaptive diffusion
based on user psychology, memory patterns, and belief systems.
"""

import time
import json
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging

import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from ..core.meme import Meme, MemeMetadata, MemeVector


class CognitiveTraits(Enum):
    """Enumeration of cognitive traits."""
    OPENNESS = "openness"
    CONSCIENTIOUSNESS = "conscientiousness"
    EXTRAVERSION = "extraversion"
    AGREEABLENESS = "agreeableness"
    NEUROTICISM = "neuroticism"
    NOVELTY_SEEKING = "novelty_seeking"
    BELIEF_RIGIDITY = "belief_rigidity"
    MEMORY_DEPTH = "memory_depth"
    SOCIAL_INFLUENCE = "social_influence"
    ATTENTION_SPAN = "attention_span"


@dataclass
class CognitiveProfile:
    """Individual cognitive trait profile."""
    
    traits: Dict[CognitiveTraits, float] = field(default_factory=dict)
    preferences: Dict[str, float] = field(default_factory=dict)
    interaction_history: List[Dict] = field(default_factory=list)
    adaptation_rate: float = 0.1
    confidence_level: float = 0.5
    
    def __post_init__(self):
        # Initialize default trait values if not provided
        for trait in CognitiveTraits:
            if trait not in self.traits:
                self.traits[trait] = 0.5  # Neutral default


@dataclass
class InteractionEvent:
    """Record of user interaction with a meme."""
    
    meme_id: str
    interaction_type: str  # "view", "share", "like", "comment", "skip"
    duration_seconds: float
    timestamp: float
    context: Dict[str, Any] = field(default_factory=dict)
    emotional_response: Optional[str] = None
    feedback_score: Optional[float] = None


class CognitiveFingerprint:
    """
    Comprehensive cognitive fingerprint for personalized meme diffusion.
    
    Tracks and models:
    - Personality traits (Big Five + custom)
    - Content preferences and patterns
    - Interaction behaviors
    - Learning and adaptation rates
    - Social influence factors
    """
    
    def __init__(
        self,
        user_id: str,
        initial_profile: Optional[CognitiveProfile] = None,
        learning_rate: float = 0.1,
        decay_rate: float = 0.95
    ):
        """
        Initialize cognitive fingerprint.
        
        Args:
            user_id: Unique user identifier
            initial_profile: Initial cognitive profile
            learning_rate: Rate of learning from interactions
            decay_rate: Rate of decay for old patterns
        """
        self.user_id = user_id
        self.profile = initial_profile or CognitiveProfile()
        self.learning_rate = learning_rate
        self.decay_rate = decay_rate
        
        self.logger = logging.getLogger(f"CognitiveFingerprint.{user_id}")
        
        # Interaction tracking
        self.interaction_history: List[InteractionEvent] = []
        self.preference_vectors: Dict[str, np.ndarray] = {}
        
        # Learning models
        self.content_clusterer = None
        self.preference_scaler = StandardScaler()
        
        # Dynamic adaptation
        self.adaptation_history: List[Dict] = []
        self.last_update_time = time.time()
        
        # Cached computations
        self._cached_preferences = {}
        self._cache_timestamp = 0
    
    def record_interaction(
        self,
        meme: Meme,
        interaction_type: str,
        duration_seconds: float = 0.0,
        emotional_response: Optional[str] = None,
        feedback_score: Optional[float] = None,
        context: Optional[Dict] = None
    ):
        """
        Record user interaction with a meme.
        
        Args:
            meme: The meme that was interacted with
            interaction_type: Type of interaction
            duration_seconds: Time spent viewing/interacting
            emotional_response: Emotional response category
            feedback_score: Explicit feedback score (0-1)
            context: Additional context information
        """
        event = InteractionEvent(
            meme_id=meme.meme_id,
            interaction_type=interaction_type,
            duration_seconds=duration_seconds,
            timestamp=time.time(),
            context=context or {},
            emotional_response=emotional_response,
            feedback_score=feedback_score
        )
        
        self.interaction_history.append(event)
        self.profile.interaction_history.append(event.__dict__)
        
        # Update preferences based on interaction
        self._update_preferences_from_interaction(meme, event)
        
        # Adapt cognitive profile
        self._adapt_cognitive_profile(meme, event)
        
        self.logger.debug(f"Recorded {interaction_type} interaction with {meme.meme_id}")
    
    def _update_preferences_from_interaction(self, meme: Meme, event: InteractionEvent):
        """Update preference vectors based on interaction."""
        if not meme.vector:
            return
        
        # Calculate preference update based on interaction type and feedback
        preference_weight = self._calculate_preference_weight(event)
        
        # Update domain preferences
        if meme.metadata.domain:
            domain = meme.metadata.domain
            if domain not in self.profile.preferences:
                self.profile.preferences[domain] = 0.5
            
            self.profile.preferences[domain] += preference_weight * self.learning_rate
            self.profile.preferences[domain] = np.clip(self.profile.preferences[domain], 0, 1)
        
        # Update content vector preferences
        content_key = "content_preference"
        if content_key not in self.preference_vectors:
            self.preference_vectors[content_key] = np.zeros_like(meme.vector.content_embedding)
        
        # Weighted update of preference vector
        embedding_array = np.array(meme.vector.content_embedding)
        self.preference_vectors[content_key] += preference_weight * self.learning_rate * embedding_array
        
        # Normalize to prevent unbounded growth
        norm = np.linalg.norm(self.preference_vectors[content_key])
        if norm > 0:
            self.preference_vectors[content_key] /= norm
    
    def _calculate_preference_weight(self, event: InteractionEvent) -> float:
        """Calculate preference weight from interaction event."""
        weights = {
            "view": 0.1,
            "like": 0.7,
            "share": 0.9,
            "comment": 0.8,
            "skip": -0.3,
            "dislike": -0.7,
            "report": -1.0
        }
        
        base_weight = weights.get(event.interaction_type, 0.0)
        
        # Adjust based on duration (longer engagement = higher preference)
        if event.duration_seconds > 0:
            duration_factor = min(2.0, event.duration_seconds / 30.0)  # Cap at 30 seconds
            base_weight *= duration_factor
        
        # Adjust based on explicit feedback
        if event.feedback_score is not None:
            base_weight = (base_weight + event.feedback_score) / 2
        
        # Adjust based on emotional response
        emotional_weights = {
            "positive": 0.3,
            "negative": -0.3,
            "neutral": 0.0,
            "excited": 0.5,
            "bored": -0.4
        }
        
        if event.emotional_response:
            emotional_factor = emotional_weights.get(event.emotional_response, 0.0)
            base_weight += emotional_factor
        
        return np.clip(base_weight, -1.0, 1.0)
    
    def _adapt_cognitive_profile(self, meme: Meme, event: InteractionEvent):
        """Adapt cognitive profile based on interaction patterns."""
        # Update novelty seeking based on content generation
        if meme.metadata.generation > 5:  # Novel/evolved content
            if event.interaction_type in ["like", "share"]:
                self.profile.traits[CognitiveTraits.NOVELTY_SEEKING] += 0.01
            elif event.interaction_type in ["skip", "dislike"]:
                self.profile.traits[CognitiveTraits.NOVELTY_SEEKING] -= 0.01
        
        # Update attention span based on interaction duration
        if event.duration_seconds > 0:
            expected_duration = 15.0  # seconds
            duration_ratio = event.duration_seconds / expected_duration
            
            if duration_ratio > 1.5:  # Long engagement
                self.profile.traits[CognitiveTraits.ATTENTION_SPAN] += 0.01
            elif duration_ratio < 0.5:  # Short engagement
                self.profile.traits[CognitiveTraits.ATTENTION_SPAN] -= 0.01
        
        # Update social influence based on sharing behavior
        if event.interaction_type == "share":
            self.profile.traits[CognitiveTraits.SOCIAL_INFLUENCE] += 0.02
        
        # Ensure traits stay within bounds
        for trait in self.profile.traits:
            self.profile.traits[trait] = np.clip(self.profile.traits[trait], 0.0, 1.0)
        
        # Update confidence based on interaction consistency
        self._update_confidence_level()
    
    def _update_confidence_level(self):
        """Update confidence level based on interaction consistency."""
        if len(self.interaction_history) < 5:
            return
        
        # Calculate consistency of recent interactions
        recent_interactions = self.interaction_history[-10:]
        positive_interactions = sum(1 for event in recent_interactions 
                                  if event.interaction_type in ["like", "share", "comment"])
        
        consistency_ratio = positive_interactions / len(recent_interactions)
        
        # Update confidence based on consistency
        target_confidence = 0.5 + 0.4 * abs(consistency_ratio - 0.5)
        self.profile.confidence_level += 0.1 * (target_confidence - self.profile.confidence_level)
        self.profile.confidence_level = np.clip(self.profile.confidence_level, 0.1, 0.9)
    
    def predict_interest(self, meme: Meme) -> float:
        """
        Predict user interest in a meme based on cognitive profile.
        
        Args:
            meme: Meme to evaluate
            
        Returns:
            Interest score (0-1)
        """
        if not meme.vector:
            return 0.5  # Neutral for memes without vectors
        
        interest_score = 0.5  # Base neutral interest
        
        # Content similarity to preferences
        if "content_preference" in self.preference_vectors:
            content_similarity = np.dot(
                self.preference_vectors["content_preference"],
                meme.vector.content_embedding
            )
            interest_score += 0.3 * content_similarity
        
        # Domain preference
        if meme.metadata.domain in self.profile.preferences:
            domain_preference = self.profile.preferences[meme.metadata.domain]
            interest_score += 0.2 * (domain_preference - 0.5)
        
        # Novelty factor based on generation and novelty seeking
        novelty_factor = min(1.0, meme.metadata.generation / 10.0)
        novelty_preference = self.profile.traits[CognitiveTraits.NOVELTY_SEEKING]
        interest_score += 0.15 * novelty_factor * novelty_preference
        
        # Fitness factor (higher fitness = higher interest for most users)
        fitness_factor = meme.vector.fitness_score
        interest_score += 0.2 * fitness_factor
        
        # Social influence factor
        if meme.metadata.propagation_count > 0:
            social_factor = min(1.0, meme.metadata.propagation_count / 100.0)
            social_influence = self.profile.traits[CognitiveTraits.SOCIAL_INFLUENCE]
            interest_score += 0.15 * social_factor * social_influence
        
        return np.clip(interest_score, 0.0, 1.0)
    
    def adapt_meme(self, meme: Meme, adaptation_strength: float = 0.5) -> Meme:
        """
        Adapt a meme for this user's cognitive profile.
        
        Args:
            meme: Original meme
            adaptation_strength: Strength of adaptation (0-1)
            
        Returns:
            Adapted meme
        """
        if not meme.vector or adaptation_strength <= 0:
            return meme
        
        # Create adapted content based on cognitive traits
        adapted_content = self._adapt_content(meme.content, adaptation_strength)
        
        # Create adapted vector
        adapted_embedding = self._adapt_embedding(meme.vector, adaptation_strength)
        
        # Create adapted metadata
        adapted_metadata = MemeMetadata(
            author=meme.metadata.author,
            domain=meme.metadata.domain,
            generation=meme.metadata.generation,
            parent_ids=meme.metadata.parent_ids + [meme.meme_id],
            mutation_type="cognitive_adaptation",
            tags=meme.metadata.tags + [f"adapted_for_{self.user_id}"],
            cognitive_signature=self.get_cognitive_signature()
        )
        
        # Create adapted vector
        adapted_vector = MemeVector(
            content_embedding=adapted_embedding.tolist(),
            intent_vector=meme.vector.intent_vector.copy(),
            fitness_score=meme.vector.fitness_score,
            dimension=meme.vector.dimension
        )
        
        # Create adapted meme
        adapted_meme = Meme(
            content=adapted_content,
            metadata=adapted_metadata,
            vector=adapted_vector
        )
        
        return adapted_meme
    
    def _adapt_content(self, original_content: str, strength: float) -> str:
        """Adapt content based on cognitive traits."""
        adapted_content = original_content
        
        # Adapt based on attention span
        attention_span = self.profile.traits[CognitiveTraits.ATTENTION_SPAN]
        if attention_span < 0.5 and len(adapted_content) > 100:
            # Shorten content for users with low attention span
            adapted_content = adapted_content[:int(100 * (1 - strength))] + "..."
        
        # Adapt based on openness to experience
        openness = self.profile.traits[CognitiveTraits.OPENNESS]
        if openness > 0.7:
            # Add more creative/abstract elements for open users
            if strength > 0.5:
                adapted_content += " 🌟 [Explore new perspectives]"
        
        # Adapt based on social influence
        social_influence = self.profile.traits[CognitiveTraits.SOCIAL_INFLUENCE]
        if social_influence > 0.6:
            # Add social elements for socially influenced users
            adapted_content += " 💬 Join the conversation!"
        
        return adapted_content
    
    def _adapt_embedding(self, original_vector: MemeVector, strength: float) -> np.ndarray:
        """Adapt embedding vector based on preferences."""
        original_embedding = np.array(original_vector.content_embedding)
        
        if "content_preference" not in self.preference_vectors:
            return original_embedding
        
        preference_vector = self.preference_vectors["content_preference"]
        
        # Blend original embedding with preference vector
        adapted_embedding = (
            (1 - strength) * original_embedding +
            strength * preference_vector * np.linalg.norm(original_embedding)
        )
        
        return adapted_embedding
    
    def get_cognitive_signature(self) -> Dict[str, float]:
        """Get compact cognitive signature for this user."""
        return {
            trait.value: self.profile.traits[trait]
            for trait in CognitiveTraits
        }
    
    def get_user_analytics(self) -> Dict[str, Any]:
        """Get comprehensive user analytics."""
        total_interactions = len(self.interaction_history)
        
        if total_interactions == 0:
            return {"error": "No interaction data available"}
        
        # Interaction type distribution
        interaction_types = {}
        total_duration = 0
        
        for event in self.interaction_history:
            interaction_types[event.interaction_type] = interaction_types.get(event.interaction_type, 0) + 1
            total_duration += event.duration_seconds
        
        # Content preferences
        domain_preferences = dict(self.profile.preferences)
        
        # Engagement metrics
        positive_interactions = sum(1 for event in self.interaction_history 
                                  if event.interaction_type in ["like", "share", "comment"])
        
        engagement_rate = positive_interactions / total_interactions
        average_duration = total_duration / total_interactions if total_interactions > 0 else 0
        
        return {
            "user_id": self.user_id,
            "total_interactions": total_interactions,
            "engagement_rate": engagement_rate,
            "average_duration_seconds": average_duration,
            "interaction_distribution": interaction_types,
            "cognitive_traits": self.get_cognitive_signature(),
            "domain_preferences": domain_preferences,
            "confidence_level": self.profile.confidence_level,
            "learning_rate": self.learning_rate,
            "last_interaction": self.interaction_history[-1].timestamp if self.interaction_history else None
        }
    
    def export_profile(self) -> Dict[str, Any]:
        """Export complete cognitive profile."""
        return {
            "user_id": self.user_id,
            "cognitive_profile": {
                "traits": {trait.value: score for trait, score in self.profile.traits.items()},
                "preferences": dict(self.profile.preferences),
                "adaptation_rate": self.profile.adaptation_rate,
                "confidence_level": self.profile.confidence_level
            },
            "interaction_summary": {
                "total_interactions": len(self.interaction_history),
                "recent_interactions": [
                    event.__dict__ for event in self.interaction_history[-10:]
                ]
            },
            "preference_vectors": {
                key: vector.tolist() for key, vector in self.preference_vectors.items()
            },
            "learning_parameters": {
                "learning_rate": self.learning_rate,
                "decay_rate": self.decay_rate,
                "last_update": self.last_update_time
            }
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return self.export_profile()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CognitiveFingerprint":
        """Create instance from dictionary."""
        user_id = data["user_id"]
        
        # Reconstruct cognitive profile
        profile_data = data.get("cognitive_profile", {})
        profile = CognitiveProfile(
            traits={CognitiveTraits(k): v for k, v in profile_data.get("traits", {}).items()},
            preferences=profile_data.get("preferences", {}),
            adaptation_rate=profile_data.get("adaptation_rate", 0.1),
            confidence_level=profile_data.get("confidence_level", 0.5)
        )
        
        # Create instance
        instance = cls(
            user_id=user_id,
            initial_profile=profile,
            learning_rate=data.get("learning_parameters", {}).get("learning_rate", 0.1),
            decay_rate=data.get("learning_parameters", {}).get("decay_rate", 0.95)
        )
        
        # Restore preference vectors
        preference_vectors = data.get("preference_vectors", {})
        for key, vector_list in preference_vectors.items():
            instance.preference_vectors[key] = np.array(vector_list)
        
        # Restore interaction history
        interaction_data = data.get("interaction_summary", {}).get("recent_interactions", [])
        for event_data in interaction_data:
            event = InteractionEvent(**event_data)
            instance.interaction_history.append(event)
        
        instance.last_update_time = data.get("learning_parameters", {}).get("last_update", time.time())
        
        return instance
