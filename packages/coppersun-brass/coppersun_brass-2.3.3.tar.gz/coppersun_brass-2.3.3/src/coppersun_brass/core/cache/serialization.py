"""
SerializationCache - Thread-safe serialization memoization

Performance optimization for Enhanced Cache Manager by eliminating
redundant JSON serialization of repeated data structures.
"""

import json
import hashlib
import threading
from collections import OrderedDict
from typing import Dict, Any, Optional


class SerializationCache:
    """Thread-safe serialization memoization cache"""
    
    def __init__(self, max_size: int = 1000):
        """
        Initialize serialization cache
        
        Args:
            max_size: Maximum number of cached serializations
        """
        self._cache: Dict[str, str] = {}
        self._access_order: OrderedDict[str, bool] = OrderedDict()
        self._max_size = max_size
        self._lock = threading.RLock()
        self._hits = 0
        self._misses = 0
    
    def get_serialized(self, value: Any) -> str:
        """
        Get serialized value with caching
        
        Args:
            value: Value to serialize
            
        Returns:
            JSON serialized string
        """
        # Generate consistent hash for the value
        value_hash = self._generate_hash(value)
        
        with self._lock:
            if value_hash in self._cache:
                # Cache hit - move to end (LRU)
                self._access_order.move_to_end(value_hash)
                self._hits += 1
                return self._cache[value_hash]
            
            # Cache miss - serialize and store
            self._misses += 1
            serialized = json.dumps(value)
            
            # Evict if necessary
            while len(self._cache) >= self._max_size:
                oldest = next(iter(self._access_order))
                del self._cache[oldest]
                del self._access_order[oldest]
            
            # Store new value
            self._cache[value_hash] = serialized
            self._access_order[value_hash] = True
            
            return serialized
    
    def _generate_hash(self, value: Any) -> str:
        """
        Generate consistent hash for any value
        
        Args:
            value: Value to hash
            
        Returns:
            Consistent hash string
        """
        try:
            # Use json.dumps for consistent serialization, then hash
            normalized = json.dumps(value, sort_keys=True)
            return hashlib.sha256(normalized.encode()).hexdigest()[:16]
        except (TypeError, ValueError):
            # Fallback for non-serializable objects
            return hashlib.sha256(str(value).encode()).hexdigest()[:16]
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics
        
        Returns:
            Dictionary with hit/miss stats and metrics
        """
        with self._lock:
            total = self._hits + self._misses
            hit_rate = self._hits / total if total > 0 else 0.0
            return {
                'hits': self._hits,
                'misses': self._misses,
                'hit_rate': hit_rate,
                'cache_size': len(self._cache),
                'max_size': self._max_size
            }
    
    def clear(self) -> None:
        """Clear the serialization cache"""
        with self._lock:
            self._cache.clear()
            self._access_order.clear()
            self._hits = 0
            self._misses = 0