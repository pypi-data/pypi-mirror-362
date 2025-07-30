"""
Data persistence utilities for Q-Memetic AI.

Handles saving and loading of memes, cognitive models, and system state
with support for multiple storage backends.
"""

import json
import pickle
import os
import time
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
import logging
import sqlite3
from contextlib import contextmanager

from ..core.meme import Meme
from ..cognitive.models import CognitiveFingerprint


class DataPersistence:
    """
    Comprehensive data persistence manager.
    
    Supports:
    - File-based storage (JSON, pickle)
    - SQLite database
    - Backup and recovery
    - Data migration
    - Compression
    """
    
    def __init__(
        self,
        data_dir: str = "./qmemetic_data",
        storage_backend: str = "sqlite",
        auto_backup: bool = True,
        backup_interval: int = 3600  # 1 hour
    ):
        """
        Initialize data persistence.
        
        Args:
            data_dir: Directory for data storage
            storage_backend: "sqlite", "json", or "pickle"
            auto_backup: Enable automatic backups
            backup_interval: Backup interval in seconds
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.storage_backend = storage_backend
        self.auto_backup = auto_backup
        self.backup_interval = backup_interval
        
        self.logger = logging.getLogger("DataPersistence")
        
        # Create subdirectories
        self.memes_dir = self.data_dir / "memes"
        self.models_dir = self.data_dir / "cognitive_models"
        self.backups_dir = self.data_dir / "backups"
        
        for dir_path in [self.memes_dir, self.models_dir, self.backups_dir]:
            dir_path.mkdir(exist_ok=True)
        
        # Initialize storage backend
        if storage_backend == "sqlite":
            self.db_path = self.data_dir / "qmemetic.db"
            self._init_sqlite()
        
        # Track last backup time
        self.last_backup_time = 0
        
        self.logger.info(f"Data persistence initialized with {storage_backend} backend")
    
    def _init_sqlite(self):
        """Initialize SQLite database schema."""
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Memes table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS memes (
                    meme_id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    vector_data TEXT,
                    metadata TEXT,
                    created_at REAL,
                    updated_at REAL
                )
            """)
            
            # Cognitive models table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cognitive_models (
                    user_id TEXT PRIMARY KEY,
                    profile_data TEXT NOT NULL,
                    created_at REAL,
                    updated_at REAL
                )
            """)
            
            # System state table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS system_state (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    updated_at REAL
                )
            """)
            
            # Entanglement network table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS entanglements (
                    source_id TEXT,
                    target_id TEXT,
                    strength REAL,
                    correlation_type TEXT,
                    created_at REAL,
                    PRIMARY KEY (source_id, target_id)
                )
            """)
            
            conn.commit()
            
        self.logger.info("SQLite database initialized")
    
    @contextmanager
    def _get_db_connection(self):
        """Get SQLite database connection with context management."""
        conn = sqlite3.connect(str(self.db_path))
        try:
            yield conn
        finally:
            conn.close()
    
    def save_meme(self, meme: Meme) -> bool:
        """
        Save meme to storage.
        
        Args:
            meme: Meme object to save
            
        Returns:
            True if saved successfully
        """
        try:
            if self.storage_backend == "sqlite":
                return self._save_meme_sqlite(meme)
            elif self.storage_backend == "json":
                return self._save_meme_json(meme)
            elif self.storage_backend == "pickle":
                return self._save_meme_pickle(meme)
            else:
                raise ValueError(f"Unknown storage backend: {self.storage_backend}")
        except Exception as e:
            self.logger.error(f"Failed to save meme {meme.meme_id}: {e}")
            return False
    
    def _save_meme_sqlite(self, meme: Meme) -> bool:
        """Save meme to SQLite database."""
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO memes 
                (meme_id, content, vector_data, metadata, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                meme.meme_id,
                meme.content,
                json.dumps(meme.vector.dict()) if meme.vector else None,
                json.dumps(meme.metadata.__dict__),
                meme.created_at.timestamp(),
                meme.updated_at.timestamp()
            ))
            
            conn.commit()
        
        return True
    
    def _save_meme_json(self, meme: Meme) -> bool:
        """Save meme to JSON file."""
        file_path = self.memes_dir / f"{meme.meme_id}.json"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(meme.to_dict(), f, indent=2, ensure_ascii=False)
        
        return True
    
    def _save_meme_pickle(self, meme: Meme) -> bool:
        """Save meme to pickle file."""
        file_path = self.memes_dir / f"{meme.meme_id}.pkl"
        
        with open(file_path, 'wb') as f:
            pickle.dump(meme, f)
        
        return True
    
    def load_meme(self, meme_id: str) -> Optional[Meme]:
        """
        Load meme from storage.
        
        Args:
            meme_id: ID of meme to load
            
        Returns:
            Meme object if found, None otherwise
        """
        try:
            if self.storage_backend == "sqlite":
                return self._load_meme_sqlite(meme_id)
            elif self.storage_backend == "json":
                return self._load_meme_json(meme_id)
            elif self.storage_backend == "pickle":
                return self._load_meme_pickle(meme_id)
            else:
                raise ValueError(f"Unknown storage backend: {self.storage_backend}")
        except Exception as e:
            self.logger.error(f"Failed to load meme {meme_id}: {e}")
            return None
    
    def _load_meme_sqlite(self, meme_id: str) -> Optional[Meme]:
        """Load meme from SQLite database."""
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT meme_id, content, vector_data, metadata, created_at, updated_at
                FROM memes WHERE meme_id = ?
            """, (meme_id,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            # Reconstruct meme from database row
            meme_data = {
                "meme_id": row[0],
                "content": row[1],
                "vector": json.loads(row[2]) if row[2] else None,
                "metadata": json.loads(row[3]),
                "created_at": row[4],
                "updated_at": row[5]
            }
            
            return Meme.from_dict(meme_data)
    
    def _load_meme_json(self, meme_id: str) -> Optional[Meme]:
        """Load meme from JSON file."""
        file_path = self.memes_dir / f"{meme_id}.json"
        
        if not file_path.exists():
            return None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            meme_data = json.load(f)
        
        return Meme.from_dict(meme_data)
    
    def _load_meme_pickle(self, meme_id: str) -> Optional[Meme]:
        """Load meme from pickle file."""
        file_path = self.memes_dir / f"{meme_id}.pkl"
        
        if not file_path.exists():
            return None
        
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    
    def load_memes(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Load multiple memes from storage.
        
        Args:
            limit: Maximum number of memes to load
            
        Returns:
            List of meme dictionaries
        """
        try:
            if self.storage_backend == "sqlite":
                return self._load_memes_sqlite(limit)
            elif self.storage_backend == "json":
                return self._load_memes_json(limit)
            elif self.storage_backend == "pickle":
                return self._load_memes_pickle(limit)
            else:
                raise ValueError(f"Unknown storage backend: {self.storage_backend}")
        except Exception as e:
            self.logger.error(f"Failed to load memes: {e}")
            return []
    
    def _load_memes_sqlite(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Load memes from SQLite database."""
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            
            query = "SELECT meme_id, content, vector_data, metadata, created_at, updated_at FROM memes ORDER BY created_at DESC"
            if limit:
                query += f" LIMIT {limit}"
            
            cursor.execute(query)
            rows = cursor.fetchall()
            
            memes = []
            for row in rows:
                meme_data = {
                    "meme_id": row[0],
                    "content": row[1],
                    "vector": json.loads(row[2]) if row[2] else None,
                    "metadata": json.loads(row[3]),
                    "created_at": row[4],
                    "updated_at": row[5]
                }
                memes.append(meme_data)
            
            return memes
    
    def _load_memes_json(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Load memes from JSON files."""
        memes = []
        json_files = list(self.memes_dir.glob("*.json"))
        
        # Sort by modification time (newest first)
        json_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
        
        if limit:
            json_files = json_files[:limit]
        
        for file_path in json_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    meme_data = json.load(f)
                    memes.append(meme_data)
            except Exception as e:
                self.logger.warning(f"Failed to load {file_path}: {e}")
        
        return memes
    
    def _load_memes_pickle(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Load memes from pickle files."""
        memes = []
        pickle_files = list(self.memes_dir.glob("*.pkl"))
        
        # Sort by modification time (newest first)
        pickle_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
        
        if limit:
            pickle_files = pickle_files[:limit]
        
        for file_path in pickle_files:
            try:
                with open(file_path, 'rb') as f:
                    meme = pickle.load(f)
                    memes.append(meme.to_dict())
            except Exception as e:
                self.logger.warning(f"Failed to load {file_path}: {e}")
        
        return memes
    
    def save_cognitive_model(self, user_id: str, model: CognitiveFingerprint) -> bool:
        """
        Save cognitive model to storage.
        
        Args:
            user_id: User identifier
            model: Cognitive fingerprint model
            
        Returns:
            True if saved successfully
        """
        try:
            if self.storage_backend == "sqlite":
                return self._save_cognitive_model_sqlite(user_id, model)
            else:
                # Fall back to JSON for other backends
                return self._save_cognitive_model_json(user_id, model)
        except Exception as e:
            self.logger.error(f"Failed to save cognitive model for {user_id}: {e}")
            return False
    
    def _save_cognitive_model_sqlite(self, user_id: str, model: CognitiveFingerprint) -> bool:
        """Save cognitive model to SQLite database."""
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO cognitive_models 
                (user_id, profile_data, created_at, updated_at)
                VALUES (?, ?, ?, ?)
            """, (
                user_id,
                json.dumps(model.to_dict()),
                time.time(),
                time.time()
            ))
            
            conn.commit()
        
        return True
    
    def _save_cognitive_model_json(self, user_id: str, model: CognitiveFingerprint) -> bool:
        """Save cognitive model to JSON file."""
        file_path = self.models_dir / f"{user_id}.json"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(model.to_dict(), f, indent=2, ensure_ascii=False)
        
        return True
    
    def load_cognitive_models(self) -> Dict[str, CognitiveFingerprint]:
        """
        Load all cognitive models from storage.
        
        Returns:
            Dictionary mapping user_id to CognitiveFingerprint
        """
        try:
            if self.storage_backend == "sqlite":
                return self._load_cognitive_models_sqlite()
            else:
                return self._load_cognitive_models_json()
        except Exception as e:
            self.logger.error(f"Failed to load cognitive models: {e}")
            return {}
    
    def _load_cognitive_models_sqlite(self) -> Dict[str, CognitiveFingerprint]:
        """Load cognitive models from SQLite database."""
        models = {}
        
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT user_id, profile_data FROM cognitive_models")
            rows = cursor.fetchall()
            
            for row in rows:
                user_id, profile_data = row
                try:
                    model_dict = json.loads(profile_data)
                    model = CognitiveFingerprint.from_dict(model_dict)
                    models[user_id] = model
                except Exception as e:
                    self.logger.warning(f"Failed to load model for {user_id}: {e}")
        
        return models
    
    def _load_cognitive_models_json(self) -> Dict[str, CognitiveFingerprint]:
        """Load cognitive models from JSON files."""
        models = {}
        
        for file_path in self.models_dir.glob("*.json"):
            user_id = file_path.stem
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    model_dict = json.load(f)
                    model = CognitiveFingerprint.from_dict(model_dict)
                    models[user_id] = model
            except Exception as e:
                self.logger.warning(f"Failed to load model for {user_id}: {e}")
        
        return models
    
    def export_data(self, data: Dict[str, Any], file_path: str) -> bool:
        """
        Export data to file.
        
        Args:
            data: Data to export
            file_path: Path to export file
            
        Returns:
            True if exported successfully
        """
        try:
            export_path = Path(file_path)
            export_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            
            self.logger.info(f"Data exported to: {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to export data: {e}")
            return False
    
    def create_backup(self, backup_name: Optional[str] = None) -> str:
        """
        Create backup of all data.
        
        Args:
            backup_name: Optional backup name
            
        Returns:
            Path to backup file
        """
        if backup_name is None:
            timestamp = int(time.time())
            backup_name = f"backup_{timestamp}"
        
        backup_path = self.backups_dir / f"{backup_name}.json"
        
        # Collect all data
        backup_data = {
            "timestamp": time.time(),
            "backend": self.storage_backend,
            "memes": self.load_memes(),
            "cognitive_models": {
                user_id: model.to_dict()
                for user_id, model in self.load_cognitive_models().items()
            }
        }
        
        # Save backup
        success = self.export_data(backup_data, str(backup_path))
        
        if success:
            self.last_backup_time = time.time()
            self.logger.info(f"Backup created: {backup_path}")
        
        return str(backup_path)
    
    def restore_from_backup(self, backup_path: str) -> bool:
        """
        Restore data from backup file.
        
        Args:
            backup_path: Path to backup file
            
        Returns:
            True if restored successfully
        """
        try:
            with open(backup_path, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            # Restore memes
            memes_data = backup_data.get("memes", [])
            for meme_data in memes_data:
                meme = Meme.from_dict(meme_data)
                self.save_meme(meme)
            
            # Restore cognitive models
            models_data = backup_data.get("cognitive_models", {})
            for user_id, model_data in models_data.items():
                model = CognitiveFingerprint.from_dict(model_data)
                self.save_cognitive_model(user_id, model)
            
            self.logger.info(f"Data restored from backup: {backup_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to restore from backup: {e}")
            return False
    
    def cleanup_old_backups(self, keep_count: int = 10):
        """
        Clean up old backup files, keeping only the most recent ones.
        
        Args:
            keep_count: Number of backups to keep
        """
        backup_files = list(self.backups_dir.glob("backup_*.json"))
        backup_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
        
        # Remove old backups
        for old_backup in backup_files[keep_count:]:
            try:
                old_backup.unlink()
                self.logger.info(f"Removed old backup: {old_backup}")
            except Exception as e:
                self.logger.warning(f"Failed to remove backup {old_backup}: {e}")
    
    def get_storage_stats(self) -> Dict[str, Any]:
        """Get storage statistics."""
        stats = {
            "backend": self.storage_backend,
            "data_dir": str(self.data_dir),
            "last_backup": self.last_backup_time,
        }
        
        if self.storage_backend == "sqlite":
            stats["database_size"] = self.db_path.stat().st_size if self.db_path.exists() else 0
            
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("SELECT COUNT(*) FROM memes")
                stats["meme_count"] = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM cognitive_models")
                stats["model_count"] = cursor.fetchone()[0]
        else:
            stats["meme_files"] = len(list(self.memes_dir.glob("*")))
            stats["model_files"] = len(list(self.models_dir.glob("*")))
        
        stats["backup_files"] = len(list(self.backups_dir.glob("*.json")))
        
        return stats
    
    def auto_backup_check(self):
        """Check if auto backup is needed and perform if necessary."""
        if not self.auto_backup:
            return
        
        current_time = time.time()
        if current_time - self.last_backup_time >= self.backup_interval:
            self.create_backup()
            self.cleanup_old_backups()
