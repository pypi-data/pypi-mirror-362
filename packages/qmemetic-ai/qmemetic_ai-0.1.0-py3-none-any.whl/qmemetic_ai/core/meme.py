"""
Core Meme representation with quantum-inspired properties.

Memes are the fundamental units of cultural evolution in Q-Memetic AI.
Each meme contains content, intent vectors, fitness scores, and metadata
that enable quantum-style entanglement and evolution.
"""

import uuid
import time
import hashlib
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
import librosa

import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from pydantic import BaseModel, Field

# Optional imports for multimodal support
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import librosa
    LIBROSA_AVAILABLE = True
except ImportError:
    LIBROSA_AVAILABLE = False

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False


class MemeVector(BaseModel):
    """High-dimensional representation of meme content and intent."""
    
    content_embedding: List[float] = Field(description="Content semantic embedding")
    intent_vector: List[float] = Field(description="Intent/purpose vector")
    fitness_score: float = Field(default=0.0, description="Evolutionary fitness")
    dimension: int = Field(description="Vector dimensionality")
    
    def __init__(self, **data):
        super().__init__(**data)
        if not self.dimension:
            self.dimension = len(self.content_embedding)
    
    def similarity(self, other: "MemeVector") -> float:
        """Calculate cosine similarity with another meme vector."""
        if self.dimension != other.dimension:
            raise ValueError("Vector dimensions must match")
        
        vec1 = np.array(self.content_embedding)
        vec2 = np.array(other.content_embedding)
        
        return float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
    
    def entanglement_strength(self, other: "MemeVector") -> float:
        """Calculate quantum-inspired entanglement strength."""
        content_sim = self.similarity(other)
        intent_sim = np.dot(self.intent_vector, other.intent_vector)
        fitness_correlation = min(self.fitness_score, other.fitness_score) / max(
            self.fitness_score, other.fitness_score, 1e-6
        )
        
        # Quantum-inspired entanglement formula
        return (content_sim * 0.5 + intent_sim * 0.3 + fitness_correlation * 0.2)


@dataclass
class MemeMetadata:
    """Comprehensive metadata for meme tracking and evolution."""
    
    author: Optional[str] = None
    timestamp: float = field(default_factory=time.time)
    domain: Optional[str] = None
    network_id: Optional[str] = None
    generation: int = 0
    parent_ids: List[str] = field(default_factory=list)
    mutation_type: Optional[str] = None
    propagation_count: int = 0
    entanglement_count: int = 0
    tags: List[str] = field(default_factory=list)
    cognitive_signature: Optional[Dict[str, float]] = None


class Meme:
    """
    Core Meme class representing a unit of cultural evolution.
    
    A meme contains:
    - Content (text, multimodal data)
    - High-dimensional vector representation
    - Evolutionary metadata
    - Quantum-inspired properties
    """
    
    def __init__(
        self,
        content: str,
        meme_id: Optional[str] = None,
        metadata: Optional[MemeMetadata] = None,
        vector: Optional[MemeVector] = None,
        embedding_model: Optional[str] = "all-MiniLM-L6-v2",
    ):
        self.meme_id = meme_id or self._generate_id(content)
        self.content = content
        self.metadata = metadata or MemeMetadata()
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        
        # Initialize embedding model if needed
        self._embedding_model = None
        if embedding_model and vector is None:
            self._embedding_model = SentenceTransformer(embedding_model)
            self.vector = self._create_vector()
        else:
            self.vector = vector
    
    def _generate_id(self, content: str) -> str:
        """Generate unique meme ID based on content hash."""
        hash_obj = hashlib.sha256(content.encode())
        return f"meme_{hash_obj.hexdigest()[:12]}"
    
    def _create_vector(self) -> MemeVector:
        """Create vector representation using embedding model."""
        if not self._embedding_model:
            raise ValueError("No embedding model available")
        
        # Generate content embedding
        content_embedding = self._embedding_model.encode(self.content).tolist()
        
        # Generate intent vector (simplified - could be more sophisticated)
        intent_keywords = ["create", "learn", "share", "discover", "innovate"]
        intent_vector = []
        for keyword in intent_keywords:
            intent_vector.append(float(keyword.lower() in self.content.lower()))
        
        return MemeVector(
            content_embedding=content_embedding,
            intent_vector=intent_vector,
            dimension=len(content_embedding)
        )
    
    def mutate(self, mutation_strength: float = 0.1) -> "Meme":
        """Create a mutated version of this meme."""
        if not self.vector:
            raise ValueError("Cannot mutate meme without vector representation")
        
        # Add gaussian noise to vector
        noise = np.random.normal(0, mutation_strength, len(self.vector.content_embedding))
        mutated_embedding = (np.array(self.vector.content_embedding) + noise).tolist()
        
        # Create new metadata
        new_metadata = MemeMetadata(
            author=self.metadata.author,
            domain=self.metadata.domain,
            network_id=self.metadata.network_id,
            generation=self.metadata.generation + 1,
            parent_ids=[self.meme_id],
            mutation_type="gaussian_noise",
            tags=self.metadata.tags.copy()
        )
        
        # Create mutated vector
        mutated_vector = MemeVector(
            content_embedding=mutated_embedding,
            intent_vector=self.vector.intent_vector.copy(),
            fitness_score=self.vector.fitness_score * 0.9,  # Slight fitness penalty
            dimension=self.vector.dimension
        )
        
        return Meme(
            content=f"{self.content} [mutated]",
            metadata=new_metadata,
            vector=mutated_vector
        )
    
    def crossover(self, other: "Meme", crossover_rate: float = 0.5) -> "Meme":
        """Create offspring through genetic crossover with another meme."""
        if not self.vector or not other.vector:
            raise ValueError("Both memes must have vector representations")
        
        if self.vector.dimension != other.vector.dimension:
            raise ValueError("Memes must have same vector dimension for crossover")
        
        # Perform crossover on embeddings
        mask = np.random.random(self.vector.dimension) < crossover_rate
        child_embedding = np.where(
            mask,
            self.vector.content_embedding,
            other.vector.content_embedding
        ).tolist()
        
        # Blend intent vectors
        child_intent = (
            np.array(self.vector.intent_vector) * crossover_rate +
            np.array(other.vector.intent_vector) * (1 - crossover_rate)
        ).tolist()
        
        # Create child metadata
        child_metadata = MemeMetadata(
            author=f"{self.metadata.author}+{other.metadata.author}",
            domain=self.metadata.domain or other.metadata.domain,
            generation=max(self.metadata.generation, other.metadata.generation) + 1,
            parent_ids=[self.meme_id, other.meme_id],
            mutation_type="crossover",
            tags=list(set(self.metadata.tags + other.metadata.tags))
        )
        
        # Create child vector
        child_vector = MemeVector(
            content_embedding=child_embedding,
            intent_vector=child_intent,
            fitness_score=max(self.vector.fitness_score, other.vector.fitness_score),
            dimension=self.vector.dimension
        )
        
        return Meme(
            content=f"Fusion of: {self.content[:50]}... & {other.content[:50]}...",
            metadata=child_metadata,
            vector=child_vector
        )
    
    def update_fitness(self, fitness_score: float):
        """Update the fitness score of this meme."""
        if self.vector:
            self.vector.fitness_score = fitness_score
        self.updated_at = datetime.now()
    
    def add_tag(self, tag: str):
        """Add a tag to this meme."""
        if tag not in self.metadata.tags:
            self.metadata.tags.append(tag)
            self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert meme to dictionary representation."""
        return {
            "meme_id": self.meme_id,
            "content": self.content,
            "vector": self.vector.dict() if self.vector else None,
            "metadata": self.metadata.__dict__,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Meme":
        """Create meme from dictionary representation."""
        vector = None
        if data.get("vector"):
            vector = MemeVector(**data["vector"])
        
        metadata = MemeMetadata(**data["metadata"])
        
        meme = cls(
            content=data["content"],
            meme_id=data["meme_id"],
            metadata=metadata,
            vector=vector
        )
        
        meme.created_at = datetime.fromisoformat(data["created_at"])
        meme.updated_at = datetime.fromisoformat(data["updated_at"])
        
        return meme
    
    def __str__(self) -> str:
        return f"Meme({self.meme_id[:8]}...): {self.content[:100]}..."
    
    def __repr__(self) -> str:
        return (
            f"Meme(id={self.meme_id}, content_len={len(self.content)}, "
            f"fitness={self.vector.fitness_score if self.vector else 'N/A'}, "
            f"generation={self.metadata.generation})"
        )


class MultimodalMeme(Meme):
    """Extended meme class supporting multimodal content."""
    
    # Supported media types and their requirements
    SUPPORTED_MEDIA_TYPES = {
        "text": None,
        "image": PIL_AVAILABLE,
        "audio": LIBROSA_AVAILABLE,
        "video": CV2_AVAILABLE,
        "multimodal": True,
    }
    
    def __init__(
        self,
        content: str,
        media_type: str = "text",
        media_data: Optional[bytes] = None,
        **kwargs
    ):
        # Validate media type
        if media_type not in self.SUPPORTED_MEDIA_TYPES:
            raise ValueError(f"Unsupported media type: {media_type}")
        
        # Check if required libraries are available
        if media_type != "text" and media_type != "multimodal":
            if not self.SUPPORTED_MEDIA_TYPES[media_type]:
                raise ImportError(
                    f"Required libraries for {media_type} processing are not available. "
                    f"Install appropriate dependencies or use media_type='text'"
                )
        
        super().__init__(content, **kwargs)
        self.media_type = media_type
        self.media_data = media_data
    
    @classmethod
    def get_available_media_types(cls) -> List[str]:
        """Get list of currently available media types based on installed libraries."""
        available = ["text", "multimodal"]  # Always available
        
        if PIL_AVAILABLE:
            available.append("image")
        if LIBROSA_AVAILABLE:
            available.append("audio")
        if CV2_AVAILABLE:
            available.append("video")
            
        return available
    
    def is_media_type_supported(self, media_type: str) -> bool:
        """Check if a specific media type is supported."""
        return media_type in self.get_available_media_types()
    
    def get_media_info(self) -> Dict[str, Any]:
        """Get information about the media content."""
        info = {
            "media_type": self.media_type,
            "has_media_data": self.media_data is not None,
            "media_size_bytes": len(self.media_data) if self.media_data else 0,
            "content_length": len(self.content),
        }
        
        # Add media-specific information
        if self.media_type == "image" and self.media_data and PIL_AVAILABLE:
            try:
                import io
                image = Image.open(io.BytesIO(self.media_data))
                info.update({
                    "image_size": image.size,
                    "image_mode": image.mode,
                    "image_format": image.format,
                })
            except Exception:
                pass
        
        return info
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert multimodal meme to dictionary representation."""
        data = super().to_dict()
        data.update({
            "media_type": self.media_type,
            "media_data": self.media_data.hex() if self.media_data else None,
            "media_info": self.get_media_info(),
        })
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MultimodalMeme":
        """Create multimodal meme from dictionary representation."""
        media_data = None
        if data.get("media_data"):
            media_data = bytes.fromhex(data["media_data"])
        
        # Extract base meme data
        base_data = {k: v for k, v in data.items() 
                    if k not in ["media_type", "media_data", "media_info"]}
        
        # Create vector if present
        vector = None
        if base_data.get("vector"):
            vector = MemeVector(**base_data["vector"])
            base_data.pop("vector")
        
        # Create metadata
        metadata = MemeMetadata(**base_data["metadata"])
        base_data.pop("metadata")
        
        meme = cls(
            content=base_data["content"],
            meme_id=base_data["meme_id"],
            media_type=data.get("media_type", "text"),
            media_data=media_data,
            metadata=metadata,
            vector=vector
        )
        
        meme.created_at = datetime.fromisoformat(base_data["created_at"])
        meme.updated_at = datetime.fromisoformat(base_data["updated_at"])
        
        return meme
