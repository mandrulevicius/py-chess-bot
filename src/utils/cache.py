"""Simple caching utilities for performance optimization."""

import time
from typing import Any, Dict, Optional, Tuple
from functools import wraps


class TTLCache:
    """Time-To-Live cache with automatic expiration."""
    
    def __init__(self, max_size: int = 100, ttl_seconds: float = 300.0):
        """
        Initialize TTL cache.
        
        Args:
            max_size: Maximum number of items to cache
            ttl_seconds: Time to live in seconds (default: 5 minutes)
        """
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self._cache: Dict[Any, Tuple[Any, float]] = {}
    
    def get(self, key: Any) -> Optional[Any]:
        """Get value from cache if not expired."""
        if key not in self._cache:
            return None
        
        value, timestamp = self._cache[key]
        
        # Check if expired
        if time.time() - timestamp > self.ttl_seconds:
            del self._cache[key]
            return None
        
        return value
    
    def set(self, key: Any, value: Any) -> None:
        """Set value in cache with current timestamp."""
        # Clean up if at max size
        if len(self._cache) >= self.max_size:
            # Remove oldest item
            oldest_key = min(self._cache.keys(), key=lambda k: self._cache[k][1])
            del self._cache[oldest_key]
        
        self._cache[key] = (value, time.time())
    
    def clear(self) -> None:
        """Clear all cached items."""
        self._cache.clear()
    
    def size(self) -> int:
        """Get current cache size."""
        return len(self._cache)


def cached_evaluation(ttl_seconds: float = 300.0):
    """
    Decorator to cache position evaluations.
    
    Args:
        ttl_seconds: Cache TTL in seconds
    """
    cache = TTLCache(max_size=50, ttl_seconds=ttl_seconds)
    
    def decorator(func):
        @wraps(func)
        def wrapper(game, ai, *args, **kwargs):
            # Create cache key from FEN position
            from ..game.board_state import get_board_fen
            fen = get_board_fen(game['board'])
            cache_key = (fen, ai.get('difficulty', 0))
            
            # Try to get from cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                # Add cache hit indicator
                result = cached_result.copy()
                result['cached'] = True
                return result
            
            # Not in cache, compute and store
            result = func(game, ai, *args, **kwargs)
            
            # Only cache successful evaluations
            if result.get('evaluation_type') != 'error':
                cache.set(cache_key, result)
            
            result['cached'] = False
            return result
        
        # Add cache management methods
        wrapper.clear_cache = cache.clear
        wrapper.cache_size = cache.size
        
        return wrapper
    
    return decorator