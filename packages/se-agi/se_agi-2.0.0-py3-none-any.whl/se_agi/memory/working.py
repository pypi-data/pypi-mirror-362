"""
Working Memory System for SE-AGI
Manages temporary, active information and cognitive processing
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json
import uuid
from collections import deque
from enum import Enum


class Priority(Enum):
    """Priority levels for working memory items"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class WorkingMemoryItem:
    """Represents an item in working memory"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    content: Any = None
    item_type: str = "general"
    priority: Priority = Priority.NORMAL
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    last_accessed: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    context: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    source: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_expired(self) -> bool:
        """Check if the item has expired"""
        if self.expires_at is None:
            return False
        return datetime.now() > self.expires_at
    
    def access(self) -> None:
        """Mark item as accessed"""
        self.last_accessed = datetime.now()
        self.access_count += 1
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'content': self.content,
            'item_type': self.item_type,
            'priority': self.priority.value,
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'last_accessed': self.last_accessed.isoformat(),
            'access_count': self.access_count,
            'context': self.context,
            'tags': self.tags,
            'source': self.source,
            'metadata': self.metadata
        }


@dataclass
class CognitiveOperation:
    """Represents a cognitive operation in working memory"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    operation_type: str = ""
    inputs: List[str] = field(default_factory=list)  # Working memory item IDs
    outputs: List[str] = field(default_factory=list)  # Working memory item IDs
    status: str = "pending"  # pending, running, completed, failed
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    progress: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class WorkingMemory:
    """
    Working Memory System that manages temporary, active information
    and supports cognitive processing
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize working memory system"""
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Memory storage
        self.items: Dict[str, WorkingMemoryItem] = {}
        self.operations: Dict[str, CognitiveOperation] = {}
        
        # Processing queues
        self.processing_queue: deque = deque()
        self.active_operations: Dict[str, CognitiveOperation] = {}
        
        # Attention and focus
        self.focus_items: List[str] = []  # Item IDs currently in focus
        self.attention_weights: Dict[str, float] = {}  # Item ID -> attention weight
        
        # Configuration
        self.max_capacity = self.config.get('max_capacity', 100)
        self.default_ttl = self.config.get('default_ttl', 3600)  # 1 hour in seconds
        self.cleanup_interval = self.config.get('cleanup_interval', 300)  # 5 minutes
        self.max_focus_items = self.config.get('max_focus_items', 7)  # Miller's number
        
        # Processing limits
        self.max_concurrent_operations = self.config.get('max_concurrent_operations', 3)
        
        # Indexing
        self.type_index: Dict[str, List[str]] = {}  # item_type -> item_ids
        self.tag_index: Dict[str, List[str]] = {}   # tag -> item_ids
        self.source_index: Dict[str, List[str]] = {}  # source -> item_ids
        
        # Background tasks
        self.cleanup_task: Optional[asyncio.Task] = None
        self.processing_task: Optional[asyncio.Task] = None
        
        self.logger.info("WorkingMemory initialized")
    
    async def start(self) -> None:
        """Start background tasks"""
        if self.cleanup_task is None:
            self.cleanup_task = asyncio.create_task(self._cleanup_loop())
        
        if self.processing_task is None:
            self.processing_task = asyncio.create_task(self._processing_loop())
        
        self.logger.info("WorkingMemory background tasks started")
    
    async def stop(self) -> None:
        """Stop background tasks"""
        if self.cleanup_task:
            self.cleanup_task.cancel()
            try:
                await self.cleanup_task
            except asyncio.CancelledError:
                pass
            self.cleanup_task = None
        
        if self.processing_task:
            self.processing_task.cancel()
            try:
                await self.processing_task
            except asyncio.CancelledError:
                pass
            self.processing_task = None
        
        self.logger.info("WorkingMemory background tasks stopped")
    
    async def store(self, 
                   content: Any,
                   item_type: str = "general",
                   priority: Priority = Priority.NORMAL,
                   ttl: Optional[int] = None,
                   context: Optional[Dict[str, Any]] = None,
                   tags: Optional[List[str]] = None,
                   source: str = "",
                   metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Store an item in working memory
        
        Args:
            content: The content to store
            item_type: Type of the item
            priority: Priority level
            ttl: Time to live in seconds (None for default)
            context: Contextual information
            tags: Tags for categorization
            source: Source of the information
            metadata: Additional metadata
            
        Returns:
            Item ID
        """
        # Calculate expiry time
        expires_at = None
        if ttl is not None:
            expires_at = datetime.now() + timedelta(seconds=ttl)
        elif self.default_ttl > 0:
            expires_at = datetime.now() + timedelta(seconds=self.default_ttl)
        
        item = WorkingMemoryItem(
            content=content,
            item_type=item_type,
            priority=priority,
            expires_at=expires_at,
            context=context or {},
            tags=tags or [],
            source=source,
            metadata=metadata or {}
        )
        
        # Store item
        self.items[item.id] = item
        
        # Update indexes
        await self._update_indexes(item)
        
        # Manage capacity
        if len(self.items) > self.max_capacity:
            await self._enforce_capacity()
        
        # Auto-focus high priority items
        if priority in [Priority.HIGH, Priority.CRITICAL]:
            await self.add_to_focus(item.id)
        
        self.logger.debug(f"Stored item {item.id} of type '{item_type}' with priority {priority.name}")
        return item.id
    
    async def retrieve(self, item_id: str) -> Optional[WorkingMemoryItem]:
        """Retrieve an item from working memory"""
        item = self.items.get(item_id)
        if item:
            if item.is_expired():
                await self.remove(item_id)
                return None
            item.access()
            await self._update_attention(item_id)
        return item
    
    async def update(self, 
                    item_id: str,
                    content: Optional[Any] = None,
                    priority: Optional[Priority] = None,
                    context: Optional[Dict[str, Any]] = None,
                    tags: Optional[List[str]] = None,
                    metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Update an existing item"""
        if item_id not in self.items:
            return False
        
        item = self.items[item_id]
        
        if content is not None:
            item.content = content
        if priority is not None:
            item.priority = priority
        if context is not None:
            item.context.update(context)
        if tags is not None:
            item.tags = list(set(item.tags + tags))
        if metadata is not None:
            item.metadata.update(metadata)
        
        item.access()
        await self._update_indexes(item)
        
        return True
    
    async def remove(self, item_id: str) -> bool:
        """Remove an item from working memory"""
        if item_id not in self.items:
            return False
        
        item = self.items[item_id]
        
        # Remove from indexes
        await self._remove_from_indexes(item)
        
        # Remove from focus if present
        if item_id in self.focus_items:
            self.focus_items.remove(item_id)
        
        # Remove attention weight
        if item_id in self.attention_weights:
            del self.attention_weights[item_id]
        
        # Remove from storage
        del self.items[item_id]
        
        self.logger.debug(f"Removed item {item_id}")
        return True
    
    async def search(self, 
                    query: str = "",
                    item_type: Optional[str] = None,
                    tags: Optional[List[str]] = None,
                    source: Optional[str] = None,
                    priority: Optional[Priority] = None,
                    max_results: int = 10) -> List[WorkingMemoryItem]:
        """Search for items in working memory"""
        candidates = []
        
        for item in self.items.values():
            # Check expiry
            if item.is_expired():
                continue
            
            # Apply filters
            if item_type and item.item_type != item_type:
                continue
            
            if priority and item.priority != priority:
                continue
            
            if source and item.source != source:
                continue
            
            if tags and not any(tag in item.tags for tag in tags):
                continue
            
            # Text search in content
            if query:
                content_str = str(item.content).lower()
                if query.lower() not in content_str:
                    continue
            
            candidates.append(item)
        
        # Sort by relevance (priority, recency, access frequency)
        def relevance_score(item: WorkingMemoryItem) -> float:
            score = 0.0
            score += item.priority.value * 0.4
            
            # Recency score
            time_diff = datetime.now() - item.last_accessed
            recency = max(0, 1 - (time_diff.total_seconds() / 3600))  # 1-hour scale
            score += recency * 0.3
            
            # Access frequency
            max_access = max((i.access_count for i in self.items.values()), default=1)
            freq_score = item.access_count / max_access if max_access > 0 else 0
            score += freq_score * 0.2
            
            # Attention weight
            attention = self.attention_weights.get(item.id, 0.0)
            score += attention * 0.1
            
            return score
        
        candidates.sort(key=relevance_score, reverse=True)
        return candidates[:max_results]
    
    async def add_to_focus(self, item_id: str, weight: float = 1.0) -> bool:
        """Add an item to the focus of attention"""
        if item_id not in self.items:
            return False
        
        if item_id in self.focus_items:
            # Update weight
            self.attention_weights[item_id] = weight
            return True
        
        # Add to focus
        self.focus_items.append(item_id)
        self.attention_weights[item_id] = weight
        
        # Maintain focus capacity
        if len(self.focus_items) > self.max_focus_items:
            # Remove least attended item
            least_attended = min(self.focus_items, 
                               key=lambda x: self.attention_weights.get(x, 0.0))
            await self.remove_from_focus(least_attended)
        
        # Mark item as accessed
        item = self.items[item_id]
        item.access()
        
        self.logger.debug(f"Added item {item_id} to focus with weight {weight}")
        return True
    
    async def remove_from_focus(self, item_id: str) -> bool:
        """Remove an item from focus"""
        if item_id not in self.focus_items:
            return False
        
        self.focus_items.remove(item_id)
        if item_id in self.attention_weights:
            del self.attention_weights[item_id]
        
        self.logger.debug(f"Removed item {item_id} from focus")
        return True
    
    async def get_focus_items(self) -> List[WorkingMemoryItem]:
        """Get all items currently in focus"""
        focus_items = []
        for item_id in self.focus_items:
            if item_id in self.items:
                item = self.items[item_id]
                if not item.is_expired():
                    focus_items.append(item)
                else:
                    await self.remove(item_id)
        
        # Sort by attention weight
        focus_items.sort(key=lambda x: self.attention_weights.get(x.id, 0.0), reverse=True)
        return focus_items
    
    async def start_operation(self, 
                             operation_type: str,
                             input_items: List[str],
                             operation_func: Callable,
                             metadata: Optional[Dict[str, Any]] = None) -> str:
        """Start a cognitive operation"""
        operation = CognitiveOperation(
            operation_type=operation_type,
            inputs=input_items,
            metadata=metadata or {}
        )
        
        self.operations[operation.id] = operation
        
        # Add to processing queue
        self.processing_queue.append((operation.id, operation_func))
        
        self.logger.debug(f"Started operation {operation.id} of type '{operation_type}'")
        return operation.id
    
    async def get_operation_status(self, operation_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of a cognitive operation"""
        if operation_id not in self.operations:
            return None
        
        operation = self.operations[operation_id]
        return {
            'id': operation.id,
            'type': operation.operation_type,
            'status': operation.status,
            'progress': operation.progress,
            'started_at': operation.started_at.isoformat() if operation.started_at else None,
            'completed_at': operation.completed_at.isoformat() if operation.completed_at else None,
            'inputs': operation.inputs,
            'outputs': operation.outputs,
            'metadata': operation.metadata
        }
    
    async def _update_indexes(self, item: WorkingMemoryItem) -> None:
        """Update indexes for an item"""
        # Type index
        if item.item_type not in self.type_index:
            self.type_index[item.item_type] = []
        if item.id not in self.type_index[item.item_type]:
            self.type_index[item.item_type].append(item.id)
        
        # Tag index
        for tag in item.tags:
            if tag not in self.tag_index:
                self.tag_index[tag] = []
            if item.id not in self.tag_index[tag]:
                self.tag_index[tag].append(item.id)
        
        # Source index
        if item.source:
            if item.source not in self.source_index:
                self.source_index[item.source] = []
            if item.id not in self.source_index[item.source]:
                self.source_index[item.source].append(item.id)
    
    async def _remove_from_indexes(self, item: WorkingMemoryItem) -> None:
        """Remove item from all indexes"""
        # Type index
        if item.item_type in self.type_index:
            self.type_index[item.item_type] = [
                id for id in self.type_index[item.item_type] if id != item.id
            ]
            if not self.type_index[item.item_type]:
                del self.type_index[item.item_type]
        
        # Tag index
        for tag in item.tags:
            if tag in self.tag_index:
                self.tag_index[tag] = [
                    id for id in self.tag_index[tag] if id != item.id
                ]
                if not self.tag_index[tag]:
                    del self.tag_index[tag]
        
        # Source index
        if item.source and item.source in self.source_index:
            self.source_index[item.source] = [
                id for id in self.source_index[item.source] if id != item.id
            ]
            if not self.source_index[item.source]:
                del self.source_index[item.source]
    
    async def _update_attention(self, item_id: str) -> None:
        """Update attention weights based on access patterns"""
        if item_id in self.attention_weights:
            # Boost attention for accessed items
            self.attention_weights[item_id] = min(1.0, self.attention_weights[item_id] * 1.1)
        
        # Decay attention for other items
        for other_id in self.attention_weights:
            if other_id != item_id:
                self.attention_weights[other_id] *= 0.99
    
    async def _enforce_capacity(self) -> None:
        """Enforce memory capacity by removing least important items"""
        if len(self.items) <= self.max_capacity:
            return
        
        # Calculate importance scores
        items_with_scores = []
        for item in self.items.values():
            score = 0.0
            
            # Priority weight
            score += item.priority.value * 0.4
            
            # Recency weight
            time_diff = datetime.now() - item.last_accessed
            recency = max(0, 1 - (time_diff.total_seconds() / 3600))
            score += recency * 0.3
            
            # Access frequency weight
            max_access = max((i.access_count for i in self.items.values()), default=1)
            freq_score = item.access_count / max_access if max_access > 0 else 0
            score += freq_score * 0.2
            
            # Focus weight
            if item.id in self.focus_items:
                score += 0.1
            
            items_with_scores.append((score, item.id))
        
        # Sort by importance (lowest first)
        items_with_scores.sort()
        
        # Remove least important items
        items_to_remove = len(self.items) - self.max_capacity
        for i in range(items_to_remove):
            _, item_id = items_with_scores[i]
            await self.remove(item_id)
        
        self.logger.info(f"Enforced capacity: removed {items_to_remove} items")
    
    async def _cleanup_loop(self) -> None:
        """Background task to clean up expired items"""
        while True:
            try:
                await asyncio.sleep(self.cleanup_interval)
                await self._cleanup_expired_items()
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in cleanup loop: {str(e)}")
    
    async def _cleanup_expired_items(self) -> None:
        """Remove expired items"""
        expired_items = []
        
        for item_id, item in self.items.items():
            if item.is_expired():
                expired_items.append(item_id)
        
        for item_id in expired_items:
            await self.remove(item_id)
        
        if expired_items:
            self.logger.debug(f"Cleaned up {len(expired_items)} expired items")
    
    async def _processing_loop(self) -> None:
        """Background task to process cognitive operations"""
        while True:
            try:
                if self.processing_queue and len(self.active_operations) < self.max_concurrent_operations:
                    operation_id, operation_func = self.processing_queue.popleft()
                    
                    if operation_id in self.operations:
                        asyncio.create_task(self._execute_operation(operation_id, operation_func))
                
                await asyncio.sleep(0.1)  # Small delay to prevent busy waiting
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in processing loop: {str(e)}")
    
    async def _execute_operation(self, operation_id: str, operation_func: Callable) -> None:
        """Execute a cognitive operation"""
        operation = self.operations[operation_id]
        operation.status = "running"
        operation.started_at = datetime.now()
        self.active_operations[operation_id] = operation
        
        try:
            # Get input items
            input_items = []
            for item_id in operation.inputs:
                item = await self.retrieve(item_id)
                if item:
                    input_items.append(item)
            
            # Execute operation
            result = await operation_func(input_items)
            
            # Store result if it's not None
            if result is not None:
                result_id = await self.store(
                    content=result,
                    item_type=f"{operation.operation_type}_result",
                    source=f"operation_{operation_id}",
                    priority=Priority.NORMAL
                )
                operation.outputs.append(result_id)
            
            operation.status = "completed"
            operation.progress = 1.0
            
        except Exception as e:
            operation.status = "failed"
            operation.metadata['error'] = str(e)
            self.logger.error(f"Operation {operation_id} failed: {str(e)}")
        
        finally:
            operation.completed_at = datetime.now()
            if operation_id in self.active_operations:
                del self.active_operations[operation_id]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get working memory statistics"""
        if not self.items:
            return {'total_items': 0}
        
        # Count by priority
        priority_counts = {p.name: 0 for p in Priority}
        for item in self.items.values():
            priority_counts[item.priority.name] += 1
        
        # Count by type
        type_counts = {}
        for item in self.items.values():
            type_counts[item.item_type] = type_counts.get(item.item_type, 0) + 1
        
        return {
            'total_items': len(self.items),
            'focus_items': len(self.focus_items),
            'active_operations': len(self.active_operations),
            'queued_operations': len(self.processing_queue),
            'capacity_usage': len(self.items) / self.max_capacity * 100,
            'priority_distribution': priority_counts,
            'type_distribution': type_counts,
            'total_types': len(self.type_index),
            'total_tags': len(self.tag_index),
            'total_sources': len(self.source_index)
        }
    
    async def clear(self) -> None:
        """Clear all working memory"""
        self.items.clear()
        self.operations.clear()
        self.focus_items.clear()
        self.attention_weights.clear()
        self.processing_queue.clear()
        self.active_operations.clear()
        
        # Clear indexes
        self.type_index.clear()
        self.tag_index.clear()
        self.source_index.clear()
        
        self.logger.info("Working memory cleared")
