"""
Episodic Memory System for SE-AGI
Stores and retrieves specific experiences and events
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json
import uuid
from collections import defaultdict


@dataclass
class Episode:
    """Represents a single episodic memory"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    content: str = ""
    context: Dict[str, Any] = field(default_factory=dict)
    emotions: Dict[str, float] = field(default_factory=dict)
    importance: float = 0.5
    tags: List[str] = field(default_factory=list)
    related_episodes: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert episode to dictionary"""
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'content': self.content,
            'context': self.context,
            'emotions': self.emotions,
            'importance': self.importance,
            'tags': self.tags,
            'related_episodes': self.related_episodes,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Episode':
        """Create episode from dictionary"""
        data = data.copy()
        if 'timestamp' in data and isinstance(data['timestamp'], str):
            data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)


@dataclass
class EpisodicQuery:
    """Query structure for episodic memory retrieval"""
    content_keywords: List[str] = field(default_factory=list)
    time_range: Optional[Tuple[datetime, datetime]] = None
    context_filters: Dict[str, Any] = field(default_factory=dict)
    emotion_filters: Dict[str, float] = field(default_factory=dict)
    importance_threshold: float = 0.0
    tags: List[str] = field(default_factory=list)
    max_results: int = 10
    similarity_threshold: float = 0.3


class EpisodicMemory:
    """
    Episodic Memory System that stores and retrieves specific experiences
    and events with temporal and contextual information
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize episodic memory system"""
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Memory storage
        self.episodes: Dict[str, Episode] = {}
        self.episodes_by_time: List[Tuple[datetime, str]] = []  # (timestamp, episode_id)
        self.episodes_by_importance: List[Tuple[float, str]] = []  # (importance, episode_id)
        
        # Indexing structures
        self.tag_index: Dict[str, List[str]] = defaultdict(list)  # tag -> episode_ids
        self.context_index: Dict[str, Dict[str, List[str]]] = defaultdict(lambda: defaultdict(list))
        self.emotion_index: Dict[str, List[Tuple[float, str]]] = defaultdict(list)  # emotion -> [(value, episode_id)]
        
        # Configuration
        self.max_episodes = self.config.get('max_episodes', 10000)
        self.auto_cleanup = self.config.get('auto_cleanup', True)
        self.cleanup_threshold = self.config.get('cleanup_threshold', 0.8)
        
        # Memory consolidation
        self.consolidation_enabled = self.config.get('consolidation_enabled', True)
        self.consolidation_interval = self.config.get('consolidation_interval', 3600)  # 1 hour
        self.last_consolidation = datetime.now()
        
        self.logger.info("EpisodicMemory initialized")
    
    async def store_episode(self, 
                           content: str,
                           context: Optional[Dict[str, Any]] = None,
                           emotions: Optional[Dict[str, float]] = None,
                           importance: float = 0.5,
                           tags: Optional[List[str]] = None) -> str:
        """
        Store a new episode in memory
        
        Args:
            content: The main content of the episode
            context: Contextual information
            emotions: Emotional associations
            importance: Importance score (0.0 to 1.0)
            tags: Associated tags
            
        Returns:
            Episode ID
        """
        episode = Episode(
            content=content,
            context=context or {},
            emotions=emotions or {},
            importance=max(0.0, min(1.0, importance)),
            tags=tags or []
        )
        
        # Store episode
        self.episodes[episode.id] = episode
        
        # Update indexes
        await self._update_indexes(episode)
        
        # Check for memory capacity
        if self.auto_cleanup and len(self.episodes) > self.max_episodes:
            await self._cleanup_memory()
        
        # Check for consolidation
        if self.consolidation_enabled:
            await self._check_consolidation()
        
        self.logger.debug(f"Stored episode {episode.id}")
        return episode.id
    
    async def retrieve_episodes(self, query: EpisodicQuery) -> List[Episode]:
        """
        Retrieve episodes matching the query
        
        Args:
            query: Query parameters
            
        Returns:
            List of matching episodes
        """
        candidates = set(self.episodes.keys())
        
        # Filter by content keywords
        if query.content_keywords:
            content_matches = set()
            for episode_id in candidates:
                episode = self.episodes[episode_id]
                if any(keyword.lower() in episode.content.lower() 
                      for keyword in query.content_keywords):
                    content_matches.add(episode_id)
            candidates &= content_matches
        
        # Filter by time range
        if query.time_range:
            start_time, end_time = query.time_range
            time_matches = set()
            for episode_id in candidates:
                episode = self.episodes[episode_id]
                if start_time <= episode.timestamp <= end_time:
                    time_matches.add(episode_id)
            candidates &= time_matches
        
        # Filter by context
        if query.context_filters:
            context_matches = set()
            for episode_id in candidates:
                episode = self.episodes[episode_id]
                if self._matches_context_filter(episode.context, query.context_filters):
                    context_matches.add(episode_id)
            candidates &= context_matches
        
        # Filter by emotions
        if query.emotion_filters:
            emotion_matches = set()
            for episode_id in candidates:
                episode = self.episodes[episode_id]
                if self._matches_emotion_filter(episode.emotions, query.emotion_filters):
                    emotion_matches.add(episode_id)
            candidates &= emotion_matches
        
        # Filter by importance
        if query.importance_threshold > 0:
            importance_matches = set()
            for episode_id in candidates:
                episode = self.episodes[episode_id]
                if episode.importance >= query.importance_threshold:
                    importance_matches.add(episode_id)
            candidates &= importance_matches
        
        # Filter by tags
        if query.tags:
            tag_matches = set()
            for tag in query.tags:
                if tag in self.tag_index:
                    tag_matches.update(self.tag_index[tag])
            candidates &= tag_matches
        
        # Get episodes and calculate relevance scores
        scored_episodes = []
        for episode_id in candidates:
            episode = self.episodes[episode_id]
            score = await self._calculate_relevance_score(episode, query)
            if score >= query.similarity_threshold:
                scored_episodes.append((score, episode))
        
        # Sort by relevance and return top results
        scored_episodes.sort(key=lambda x: x[0], reverse=True)
        return [episode for _, episode in scored_episodes[:query.max_results]]
    
    async def get_episode_by_id(self, episode_id: str) -> Optional[Episode]:
        """Get a specific episode by ID"""
        return self.episodes.get(episode_id)
    
    async def get_recent_episodes(self, count: int = 10, 
                                 time_window: Optional[timedelta] = None) -> List[Episode]:
        """Get recent episodes"""
        cutoff_time = None
        if time_window:
            cutoff_time = datetime.now() - time_window
        
        recent_episodes = []
        for timestamp, episode_id in sorted(self.episodes_by_time, reverse=True):
            if cutoff_time and timestamp < cutoff_time:
                break
            recent_episodes.append(self.episodes[episode_id])
            if len(recent_episodes) >= count:
                break
        
        return recent_episodes
    
    async def get_important_episodes(self, count: int = 10, 
                                   threshold: float = 0.7) -> List[Episode]:
        """Get most important episodes"""
        important_episodes = []
        for importance, episode_id in sorted(self.episodes_by_importance, reverse=True):
            if importance < threshold:
                break
            important_episodes.append(self.episodes[episode_id])
            if len(important_episodes) >= count:
                break
        
        return important_episodes
    
    async def update_episode_importance(self, episode_id: str, importance: float) -> bool:
        """Update the importance of an episode"""
        if episode_id not in self.episodes:
            return False
        
        old_importance = self.episodes[episode_id].importance
        self.episodes[episode_id].importance = max(0.0, min(1.0, importance))
        
        # Update importance index
        self.episodes_by_importance = [
            (imp, eid) for imp, eid in self.episodes_by_importance 
            if eid != episode_id
        ]
        self.episodes_by_importance.append((importance, episode_id))
        self.episodes_by_importance.sort()
        
        self.logger.debug(f"Updated importance of episode {episode_id}: {old_importance} -> {importance}")
        return True
    
    async def add_episode_tags(self, episode_id: str, tags: List[str]) -> bool:
        """Add tags to an episode"""
        if episode_id not in self.episodes:
            return False
        
        episode = self.episodes[episode_id]
        for tag in tags:
            if tag not in episode.tags:
                episode.tags.append(tag)
                self.tag_index[tag].append(episode_id)
        
        return True
    
    async def link_episodes(self, episode_id1: str, episode_id2: str) -> bool:
        """Create a bidirectional link between two episodes"""
        if episode_id1 not in self.episodes or episode_id2 not in self.episodes:
            return False
        
        episode1 = self.episodes[episode_id1]
        episode2 = self.episodes[episode_id2]
        
        if episode_id2 not in episode1.related_episodes:
            episode1.related_episodes.append(episode_id2)
        
        if episode_id1 not in episode2.related_episodes:
            episode2.related_episodes.append(episode_id1)
        
        return True
    
    async def consolidate_memories(self) -> Dict[str, Any]:
        """Consolidate memories by strengthening important ones and forgetting less important ones"""
        if not self.consolidation_enabled:
            return {'status': 'disabled'}
        
        initial_count = len(self.episodes)
        consolidated_count = 0
        forgotten_count = 0
        
        # Strengthen frequently accessed and important memories
        for episode in self.episodes.values():
            if episode.importance > 0.8:
                episode.importance = min(1.0, episode.importance * 1.05)  # Slight boost
                consolidated_count += 1
        
        # Forget very low importance memories
        if len(self.episodes) > self.max_episodes * 0.5:
            to_forget = []
            for episode_id, episode in self.episodes.items():
                if episode.importance < 0.1 and len(episode.related_episodes) == 0:
                    to_forget.append(episode_id)
            
            for episode_id in to_forget[:100]:  # Limit forgetting rate
                await self._remove_episode(episode_id)
                forgotten_count += 1
        
        self.last_consolidation = datetime.now()
        
        result = {
            'status': 'completed',
            'initial_count': initial_count,
            'consolidated_count': consolidated_count,
            'forgotten_count': forgotten_count,
            'final_count': len(self.episodes)
        }
        
        self.logger.info(f"Memory consolidation completed: {result}")
        return result
    
    async def _update_indexes(self, episode: Episode) -> None:
        """Update all indexes for a new episode"""
        # Time index
        self.episodes_by_time.append((episode.timestamp, episode.id))
        self.episodes_by_time.sort()
        
        # Importance index
        self.episodes_by_importance.append((episode.importance, episode.id))
        self.episodes_by_importance.sort()
        
        # Tag index
        for tag in episode.tags:
            self.tag_index[tag].append(episode.id)
        
        # Context index
        for key, value in episode.context.items():
            value_str = str(value)
            self.context_index[key][value_str].append(episode.id)
        
        # Emotion index
        for emotion, value in episode.emotions.items():
            self.emotion_index[emotion].append((value, episode.id))
            self.emotion_index[emotion].sort()
    
    async def _remove_episode(self, episode_id: str) -> None:
        """Remove an episode and update all indexes"""
        if episode_id not in self.episodes:
            return
        
        episode = self.episodes[episode_id]
        
        # Remove from main storage
        del self.episodes[episode_id]
        
        # Update indexes
        self.episodes_by_time = [(ts, eid) for ts, eid in self.episodes_by_time if eid != episode_id]
        self.episodes_by_importance = [(imp, eid) for imp, eid in self.episodes_by_importance if eid != episode_id]
        
        # Tag index
        for tag in episode.tags:
            if tag in self.tag_index:
                self.tag_index[tag] = [eid for eid in self.tag_index[tag] if eid != episode_id]
                if not self.tag_index[tag]:
                    del self.tag_index[tag]
        
        # Context index
        for key, value in episode.context.items():
            value_str = str(value)
            if key in self.context_index and value_str in self.context_index[key]:
                self.context_index[key][value_str] = [
                    eid for eid in self.context_index[key][value_str] if eid != episode_id
                ]
                if not self.context_index[key][value_str]:
                    del self.context_index[key][value_str]
                if not self.context_index[key]:
                    del self.context_index[key]
        
        # Emotion index
        for emotion in episode.emotions:
            if emotion in self.emotion_index:
                self.emotion_index[emotion] = [
                    (val, eid) for val, eid in self.emotion_index[emotion] if eid != episode_id
                ]
                if not self.emotion_index[emotion]:
                    del self.emotion_index[emotion]
    
    async def _cleanup_memory(self) -> None:
        """Clean up memory when capacity is exceeded"""
        if len(self.episodes) <= self.max_episodes:
            return
        
        # Remove least important episodes
        target_size = int(self.max_episodes * self.cleanup_threshold)
        episodes_to_remove = len(self.episodes) - target_size
        
        # Sort by importance and remove lowest
        episodes_by_importance = [(ep.importance, ep.id) for ep in self.episodes.values()]
        episodes_by_importance.sort()
        
        for i in range(min(episodes_to_remove, len(episodes_by_importance))):
            _, episode_id = episodes_by_importance[i]
            await self._remove_episode(episode_id)
        
        self.logger.info(f"Cleaned up {episodes_to_remove} episodes")
    
    async def _check_consolidation(self) -> None:
        """Check if memory consolidation is needed"""
        if not self.consolidation_enabled:
            return
        
        time_since_last = datetime.now() - self.last_consolidation
        if time_since_last.total_seconds() >= self.consolidation_interval:
            await self.consolidate_memories()
    
    def _matches_context_filter(self, context: Dict[str, Any], filters: Dict[str, Any]) -> bool:
        """Check if context matches the filters"""
        for key, value in filters.items():
            if key not in context:
                return False
            if context[key] != value:
                return False
        return True
    
    def _matches_emotion_filter(self, emotions: Dict[str, float], filters: Dict[str, float]) -> bool:
        """Check if emotions match the filters"""
        for emotion, threshold in filters.items():
            if emotion not in emotions:
                return False
            if emotions[emotion] < threshold:
                return False
        return True
    
    async def _calculate_relevance_score(self, episode: Episode, query: EpisodicQuery) -> float:
        """Calculate relevance score for an episode given a query"""
        score = 0.0
        
        # Content keyword matching
        if query.content_keywords:
            content_lower = episode.content.lower()
            matching_keywords = sum(1 for kw in query.content_keywords 
                                  if kw.lower() in content_lower)
            score += (matching_keywords / len(query.content_keywords)) * 0.4
        
        # Importance score
        score += episode.importance * 0.3
        
        # Recency score (more recent = higher score)
        time_diff = datetime.now() - episode.timestamp
        recency_score = max(0, 1 - (time_diff.total_seconds() / (7 * 24 * 3600)))  # Week scale
        score += recency_score * 0.2
        
        # Tag matching
        if query.tags:
            matching_tags = len(set(episode.tags) & set(query.tags))
            score += (matching_tags / len(query.tags)) * 0.1
        
        return min(1.0, score)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get memory statistics"""
        if not self.episodes:
            return {'total_episodes': 0}
        
        importances = [ep.importance for ep in self.episodes.values()]
        
        return {
            'total_episodes': len(self.episodes),
            'avg_importance': sum(importances) / len(importances),
            'max_importance': max(importances),
            'min_importance': min(importances),
            'total_tags': len(self.tag_index),
            'last_consolidation': self.last_consolidation.isoformat(),
            'memory_usage_percent': len(self.episodes) / self.max_episodes * 100
        }
    
    async def export_episodes(self, file_path: str = None) -> Dict[str, Any]:
        """Export episodes to dictionary format"""
        episodes_data = {}
        for episode_id, episode in self.episodes.items():
            episodes_data[episode_id] = episode.to_dict()
        
        export_data = {
            'episodes': episodes_data,
            'statistics': self.get_statistics(),
            'export_timestamp': datetime.now().isoformat()
        }
        
        if file_path:
            with open(file_path, 'w') as f:
                json.dump(export_data, f, indent=2)
        
        return export_data
    
    async def import_episodes(self, data: Dict[str, Any]) -> int:
        """Import episodes from dictionary format"""
        if 'episodes' not in data:
            return 0
        
        imported_count = 0
        for episode_id, episode_data in data['episodes'].items():
            try:
                episode = Episode.from_dict(episode_data)
                self.episodes[episode.id] = episode
                await self._update_indexes(episode)
                imported_count += 1
            except Exception as e:
                self.logger.error(f"Failed to import episode {episode_id}: {str(e)}")
        
        self.logger.info(f"Imported {imported_count} episodes")
        return imported_count
