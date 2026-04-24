"""
Caching layer for Sputnikmusic audit results.
Stores audit results in database to avoid repeated scraping.
"""

import json
from datetime import datetime, timedelta
from typing import Optional, List
from sqlmodel import SQLModel, Field, Session
from sqlalchemy import Column, String, JSON, DateTime


class AuditResultCache(SQLModel, table=True):
    """Cache store for audit results."""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    artist_id: int = Field(foreign_key="artist.id", index=True)
    artist_name: str = Field(index=True)
    
    # Cached audit result
    result_json: str  # Serialized AuditResult
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime  # When cache should be refreshed
    
    # Status
    is_valid: bool = True  # False if scrape failed


class AuditCacheManager:
    """Manage audit result caching."""
    
    CACHE_TTL_HOURS = 24  # Cache for 24 hours
    
    @staticmethod
    def get_cached_result(
        session: Session,
        artist_id: int,
    ) -> Optional[dict]:
        """
        Get cached audit result if it exists and hasn't expired.
        
        Returns:
            Deserialized audit result or None
        """
        cache = session.query(AuditResultCache).filter(
            AuditResultCache.artist_id == artist_id,
            AuditResultCache.is_valid == True,
        ).order_by(AuditResultCache.updated_at.desc()).first()
        
        if not cache:
            return None
        
        # Check if expired
        if datetime.utcnow() > cache.expires_at:
            cache.is_valid = False
            session.add(cache)
            session.commit()
            return None
        
        # Return cached result
        try:
            return json.loads(cache.result_json)
        except json.JSONDecodeError:
            cache.is_valid = False
            session.add(cache)
            session.commit()
            return None
    
    @staticmethod
    def cache_result(
        session: Session,
        artist_id: int,
        artist_name: str,
        result: dict,
    ):
        """
        Cache audit result for future use.
        
        Args:
            session: Database session
            artist_id: ID of artist
            artist_name: Name of artist
            result: Audit result dictionary
        """
        now = datetime.utcnow()
        expires_at = now + timedelta(hours=AuditCacheManager.CACHE_TTL_HOURS)
        
        cache_entry = AuditResultCache(
            artist_id=artist_id,
            artist_name=artist_name,
            result_json=json.dumps(result),
            created_at=now,
            updated_at=now,
            expires_at=expires_at,
            is_valid=True,
        )
        
        session.add(cache_entry)
        session.commit()
    
    @staticmethod
    def invalidate_cache(session: Session, artist_id: int):
        """
        Manually invalidate cache for an artist (e.g., after manual import).
        """
        caches = session.query(AuditResultCache).filter(
            AuditResultCache.artist_id == artist_id
        ).all()
        
        for cache in caches:
            cache.is_valid = False
        
        session.commit()
    
    @staticmethod
    def clear_expired_cache(session: Session):
        """
        Clean up expired cache entries (maintenance task).
        """
        now = datetime.utcnow()
        session.query(AuditResultCache).filter(
            AuditResultCache.expires_at < now
        ).delete()
        session.commit()
