"""
Semantic Memory System for SE-AGI
Stores and retrieves conceptual knowledge and relationships
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime
import json
import uuid
from collections import defaultdict
import math


@dataclass
class Concept:
    """Represents a concept in semantic memory"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    definition: str = ""
    properties: Dict[str, Any] = field(default_factory=dict)
    relationships: Dict[str, List[str]] = field(default_factory=dict)  # relation_type -> [concept_ids]
    importance: float = 0.5
    confidence: float = 1.0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert concept to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'definition': self.definition,
            'properties': self.properties,
            'relationships': self.relationships,
            'importance': self.importance,
            'confidence': self.confidence,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'access_count': self.access_count,
            'tags': self.tags,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Concept':
        """Create concept from dictionary"""
        data = data.copy()
        if 'created_at' in data and isinstance(data['created_at'], str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        if 'updated_at' in data and isinstance(data['updated_at'], str):
            data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        return cls(**data)


@dataclass
class Relationship:
    """Represents a relationship between concepts"""
    source_id: str
    target_id: str
    relation_type: str
    strength: float = 1.0
    properties: Dict[str, Any] = field(default_factory=dict)
    bidirectional: bool = False
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class SemanticQuery:
    """Query structure for semantic memory"""
    concept_name: Optional[str] = None
    keywords: List[str] = field(default_factory=list)
    properties: Dict[str, Any] = field(default_factory=dict)
    relationships: Dict[str, List[str]] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    importance_threshold: float = 0.0
    confidence_threshold: float = 0.0
    max_results: int = 10
    include_related: bool = False
    max_depth: int = 2


class SemanticMemory:
    """
    Semantic Memory System that stores and retrieves conceptual knowledge,
    facts, and relationships between concepts
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize semantic memory system"""
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Core storage
        self.concepts: Dict[str, Concept] = {}
        self.relationships: List[Relationship] = []
        
        # Indexing structures
        self.name_index: Dict[str, str] = {}  # concept_name -> concept_id
        self.property_index: Dict[str, Dict[str, List[str]]] = defaultdict(lambda: defaultdict(list))
        self.tag_index: Dict[str, List[str]] = defaultdict(list)  # tag -> concept_ids
        self.relationship_index: Dict[str, Dict[str, List[Relationship]]] = defaultdict(lambda: defaultdict(list))
        
        # Configuration
        self.max_concepts = self.config.get('max_concepts', 50000)
        self.auto_cleanup = self.config.get('auto_cleanup', True)
        self.relationship_decay = self.config.get('relationship_decay', 0.999)
        
        # Knowledge organization
        self.knowledge_domains: Dict[str, Set[str]] = defaultdict(set)  # domain -> concept_ids
        self.concept_hierarchies: Dict[str, Dict[str, List[str]]] = defaultdict(lambda: defaultdict(list))
        
        self.logger.info("SemanticMemory initialized")
    
    async def store_concept(self, 
                           name: str,
                           definition: str = "",
                           properties: Optional[Dict[str, Any]] = None,
                           tags: Optional[List[str]] = None,
                           importance: float = 0.5,
                           confidence: float = 1.0) -> str:
        """
        Store a new concept in semantic memory
        
        Args:
            name: Name of the concept
            definition: Definition or description
            properties: Associated properties
            tags: Tags for categorization
            importance: Importance score (0.0 to 1.0)
            confidence: Confidence in the concept (0.0 to 1.0)
            
        Returns:
            Concept ID
        """
        # Check if concept already exists
        existing_id = self.name_index.get(name.lower())
        if existing_id:
            # Update existing concept
            return await self.update_concept(existing_id, definition=definition, 
                                           properties=properties, tags=tags,
                                           importance=importance, confidence=confidence)
        
        concept = Concept(
            name=name,
            definition=definition,
            properties=properties or {},
            tags=tags or [],
            importance=max(0.0, min(1.0, importance)),
            confidence=max(0.0, min(1.0, confidence))
        )
        
        # Store concept
        self.concepts[concept.id] = concept
        
        # Update indexes
        await self._update_concept_indexes(concept)
        
        # Auto-organize into domains
        await self._auto_organize_concept(concept)
        
        self.logger.debug(f"Stored concept '{name}' with ID {concept.id}")
        return concept.id
    
    async def get_concept(self, concept_id: str) -> Optional[Concept]:
        """Get a concept by ID"""
        concept = self.concepts.get(concept_id)
        if concept:
            concept.access_count += 1
            concept.updated_at = datetime.now()
        return concept
    
    async def get_concept_by_name(self, name: str) -> Optional[Concept]:
        """Get a concept by name"""
        concept_id = self.name_index.get(name.lower())
        if concept_id:
            return await self.get_concept(concept_id)
        return None
    
    async def search_concepts(self, query: SemanticQuery) -> List[Concept]:
        """
        Search for concepts matching the query
        
        Args:
            query: Search query parameters
            
        Returns:
            List of matching concepts
        """
        candidates = set(self.concepts.keys())
        
        # Filter by concept name
        if query.concept_name:
            name_matches = set()
            for name, concept_id in self.name_index.items():
                if query.concept_name.lower() in name:
                    name_matches.add(concept_id)
            candidates &= name_matches
        
        # Filter by keywords
        if query.keywords:
            keyword_matches = set()
            for concept_id in candidates:
                concept = self.concepts[concept_id]
                concept_text = f"{concept.name} {concept.definition}".lower()
                if any(keyword.lower() in concept_text for keyword in query.keywords):
                    keyword_matches.add(concept_id)
            candidates &= keyword_matches
        
        # Filter by properties
        if query.properties:
            property_matches = set()
            for concept_id in candidates:
                concept = self.concepts[concept_id]
                if self._matches_properties(concept.properties, query.properties):
                    property_matches.add(concept_id)
            candidates &= property_matches
        
        # Filter by tags
        if query.tags:
            tag_matches = set()
            for tag in query.tags:
                if tag in self.tag_index:
                    tag_matches.update(self.tag_index[tag])
            candidates &= tag_matches
        
        # Filter by importance and confidence
        filtered_candidates = []
        for concept_id in candidates:
            concept = self.concepts[concept_id]
            if (concept.importance >= query.importance_threshold and 
                concept.confidence >= query.confidence_threshold):
                filtered_candidates.append(concept)
        
        # Calculate relevance scores
        scored_concepts = []
        for concept in filtered_candidates:
            score = await self._calculate_semantic_relevance(concept, query)
            scored_concepts.append((score, concept))
        
        # Sort by relevance
        scored_concepts.sort(key=lambda x: x[0], reverse=True)
        results = [concept for _, concept in scored_concepts[:query.max_results]]
        
        # Include related concepts if requested
        if query.include_related:
            related_concepts = await self._get_related_concepts(results, query.max_depth)
            results.extend(related_concepts)
            results = list({c.id: c for c in results}.values())  # Remove duplicates
        
        return results
    
    async def add_relationship(self, 
                              source_concept: str, 
                              target_concept: str,
                              relation_type: str,
                              strength: float = 1.0,
                              properties: Optional[Dict[str, Any]] = None,
                              bidirectional: bool = False) -> bool:
        """
        Add a relationship between two concepts
        
        Args:
            source_concept: Source concept ID or name
            target_concept: Target concept ID or name
            relation_type: Type of relationship (e.g., 'is_a', 'part_of', 'related_to')
            strength: Strength of the relationship (0.0 to 1.0)
            properties: Additional properties of the relationship
            bidirectional: Whether the relationship is bidirectional
            
        Returns:
            True if relationship was added successfully
        """
        # Resolve concept IDs
        source_id = await self._resolve_concept_id(source_concept)
        target_id = await self._resolve_concept_id(target_concept)
        
        if not source_id or not target_id:
            return False
        
        if source_id == target_id:
            return False  # No self-relationships
        
        # Create relationship
        relationship = Relationship(
            source_id=source_id,
            target_id=target_id,
            relation_type=relation_type,
            strength=max(0.0, min(1.0, strength)),
            properties=properties or {},
            bidirectional=bidirectional
        )
        
        # Store relationship
        self.relationships.append(relationship)
        
        # Update concept relationships
        source_concept_obj = self.concepts[source_id]
        if relation_type not in source_concept_obj.relationships:
            source_concept_obj.relationships[relation_type] = []
        source_concept_obj.relationships[relation_type].append(target_id)
        
        if bidirectional:
            target_concept_obj = self.concepts[target_id]
            if relation_type not in target_concept_obj.relationships:
                target_concept_obj.relationships[relation_type] = []
            target_concept_obj.relationships[relation_type].append(source_id)
        
        # Update relationship index
        self.relationship_index[source_id][relation_type].append(relationship)
        if bidirectional:
            self.relationship_index[target_id][relation_type].append(relationship)
        
        self.logger.debug(f"Added relationship: {source_id} --{relation_type}--> {target_id}")
        return True
    
    async def get_related_concepts(self, 
                                  concept_id: str, 
                                  relation_types: Optional[List[str]] = None,
                                  max_depth: int = 1) -> Dict[str, List[Concept]]:
        """
        Get concepts related to a given concept
        
        Args:
            concept_id: ID of the source concept
            relation_types: Types of relationships to follow (None for all)
            max_depth: Maximum depth to traverse
            
        Returns:
            Dictionary mapping relation types to lists of related concepts
        """
        if concept_id not in self.concepts:
            return {}
        
        related = defaultdict(list)
        visited = set()
        queue = [(concept_id, 0)]  # (concept_id, depth)
        
        while queue:
            current_id, depth = queue.pop(0)
            if current_id in visited or depth >= max_depth:
                continue
            
            visited.add(current_id)
            current_concept = self.concepts[current_id]
            
            for rel_type, target_ids in current_concept.relationships.items():
                if relation_types is None or rel_type in relation_types:
                    for target_id in target_ids:
                        if target_id in self.concepts and target_id not in visited:
                            target_concept = self.concepts[target_id]
                            related[rel_type].append(target_concept)
                            
                            if depth + 1 < max_depth:
                                queue.append((target_id, depth + 1))
        
        return dict(related)
    
    async def update_concept(self, 
                            concept_id: str,
                            name: Optional[str] = None,
                            definition: Optional[str] = None,
                            properties: Optional[Dict[str, Any]] = None,
                            tags: Optional[List[str]] = None,
                            importance: Optional[float] = None,
                            confidence: Optional[float] = None) -> bool:
        """Update an existing concept"""
        if concept_id not in self.concepts:
            return False
        
        concept = self.concepts[concept_id]
        old_name = concept.name
        
        # Update fields
        if name is not None:
            concept.name = name
        if definition is not None:
            concept.definition = definition
        if properties is not None:
            concept.properties.update(properties)
        if tags is not None:
            concept.tags = list(set(concept.tags + tags))
        if importance is not None:
            concept.importance = max(0.0, min(1.0, importance))
        if confidence is not None:
            concept.confidence = max(0.0, min(1.0, confidence))
        
        concept.updated_at = datetime.now()
        
        # Update indexes if name changed
        if name and name != old_name:
            if old_name.lower() in self.name_index:
                del self.name_index[old_name.lower()]
            self.name_index[name.lower()] = concept_id
        
        await self._update_concept_indexes(concept)
        
        return True
    
    async def remove_concept(self, concept_id: str) -> bool:
        """Remove a concept and all its relationships"""
        if concept_id not in self.concepts:
            return False
        
        concept = self.concepts[concept_id]
        
        # Remove from name index
        if concept.name.lower() in self.name_index:
            del self.name_index[concept.name.lower()]
        
        # Remove from other indexes
        for tag in concept.tags:
            if tag in self.tag_index:
                self.tag_index[tag] = [cid for cid in self.tag_index[tag] if cid != concept_id]
                if not self.tag_index[tag]:
                    del self.tag_index[tag]
        
        # Remove relationships
        self.relationships = [rel for rel in self.relationships 
                            if rel.source_id != concept_id and rel.target_id != concept_id]
        
        # Remove from other concepts' relationships
        for other_concept in self.concepts.values():
            for rel_type, target_ids in other_concept.relationships.items():
                other_concept.relationships[rel_type] = [tid for tid in target_ids if tid != concept_id]
        
        # Remove from concept storage
        del self.concepts[concept_id]
        
        self.logger.debug(f"Removed concept {concept_id}")
        return True
    
    async def get_concept_hierarchy(self, root_concept_id: str, 
                                   relation_type: str = 'is_a') -> Dict[str, Any]:
        """Get hierarchical structure starting from a root concept"""
        if root_concept_id not in self.concepts:
            return {}
        
        def build_hierarchy(concept_id: str, visited: Set[str]) -> Dict[str, Any]:
            if concept_id in visited:
                return {'id': concept_id, 'name': self.concepts[concept_id].name, 'circular': True}
            
            visited.add(concept_id)
            concept = self.concepts[concept_id]
            
            hierarchy = {
                'id': concept_id,
                'name': concept.name,
                'definition': concept.definition,
                'children': []
            }
            
            if relation_type in concept.relationships:
                for child_id in concept.relationships[relation_type]:
                    if child_id in self.concepts:
                        child_hierarchy = build_hierarchy(child_id, visited.copy())
                        hierarchy['children'].append(child_hierarchy)
            
            return hierarchy
        
        return build_hierarchy(root_concept_id, set())
    
    async def find_concept_path(self, source_id: str, target_id: str,
                               max_depth: int = 5) -> Optional[List[Tuple[str, str]]]:
        """Find a path between two concepts"""
        if source_id not in self.concepts or target_id not in self.concepts:
            return None
        
        if source_id == target_id:
            return []
        
        # BFS to find shortest path
        queue = [(source_id, [])]  # (current_id, path)
        visited = {source_id}
        
        while queue:
            current_id, path = queue.pop(0)
            
            if len(path) >= max_depth:
                continue
            
            current_concept = self.concepts[current_id]
            
            for rel_type, target_ids in current_concept.relationships.items():
                for next_id in target_ids:
                    if next_id == target_id:
                        return path + [(current_id, rel_type)]
                    
                    if next_id not in visited and next_id in self.concepts:
                        visited.add(next_id)
                        queue.append((next_id, path + [(current_id, rel_type)]))
        
        return None
    
    async def _resolve_concept_id(self, concept_identifier: str) -> Optional[str]:
        """Resolve concept ID from either ID or name"""
        # Check if it's already an ID
        if concept_identifier in self.concepts:
            return concept_identifier
        
        # Check if it's a name
        concept_id = self.name_index.get(concept_identifier.lower())
        return concept_id
    
    async def _update_concept_indexes(self, concept: Concept) -> None:
        """Update indexes for a concept"""
        # Name index
        self.name_index[concept.name.lower()] = concept.id
        
        # Property index
        for prop_name, prop_value in concept.properties.items():
            prop_value_str = str(prop_value)
            self.property_index[prop_name][prop_value_str].append(concept.id)
        
        # Tag index
        for tag in concept.tags:
            if concept.id not in self.tag_index[tag]:
                self.tag_index[tag].append(concept.id)
    
    async def _auto_organize_concept(self, concept: Concept) -> None:
        """Automatically organize concept into knowledge domains"""
        # Simple domain classification based on tags and properties
        domains = set()
        
        # Extract domains from tags
        for tag in concept.tags:
            domains.add(tag.lower())
        
        # Extract domains from properties
        if 'domain' in concept.properties:
            domains.add(str(concept.properties['domain']).lower())
        
        if 'category' in concept.properties:
            domains.add(str(concept.properties['category']).lower())
        
        # Default domain if none found
        if not domains:
            domains.add('general')
        
        # Add to knowledge domains
        for domain in domains:
            self.knowledge_domains[domain].add(concept.id)
    
    def _matches_properties(self, concept_props: Dict[str, Any], 
                           query_props: Dict[str, Any]) -> bool:
        """Check if concept properties match query properties"""
        for key, value in query_props.items():
            if key not in concept_props:
                return False
            if concept_props[key] != value:
                return False
        return True
    
    async def _calculate_semantic_relevance(self, concept: Concept, 
                                          query: SemanticQuery) -> float:
        """Calculate semantic relevance score"""
        score = 0.0
        
        # Name matching
        if query.concept_name:
            if query.concept_name.lower() == concept.name.lower():
                score += 0.5
            elif query.concept_name.lower() in concept.name.lower():
                score += 0.3
        
        # Keyword matching
        if query.keywords:
            concept_text = f"{concept.name} {concept.definition}".lower()
            matching_keywords = sum(1 for kw in query.keywords 
                                  if kw.lower() in concept_text)
            score += (matching_keywords / len(query.keywords)) * 0.3
        
        # Property matching
        if query.properties:
            matching_props = sum(1 for key, value in query.properties.items()
                               if key in concept.properties and concept.properties[key] == value)
            score += (matching_props / len(query.properties)) * 0.2
        
        # Tag matching
        if query.tags:
            matching_tags = len(set(concept.tags) & set(query.tags))
            score += (matching_tags / len(query.tags)) * 0.1
        
        # Importance and confidence
        score += concept.importance * 0.1
        score += concept.confidence * 0.05
        
        # Access frequency (popularity)
        max_access = max((c.access_count for c in self.concepts.values()), default=1)
        access_score = concept.access_count / max_access if max_access > 0 else 0
        score += access_score * 0.05
        
        return min(1.0, score)
    
    async def _get_related_concepts(self, concepts: List[Concept], 
                                   max_depth: int) -> List[Concept]:
        """Get concepts related to the given concepts"""
        related = []
        seen_ids = {c.id for c in concepts}
        
        for concept in concepts:
            related_dict = await self.get_related_concepts(concept.id, max_depth=max_depth)
            for rel_concepts in related_dict.values():
                for rel_concept in rel_concepts:
                    if rel_concept.id not in seen_ids:
                        related.append(rel_concept)
                        seen_ids.add(rel_concept.id)
        
        return related
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get semantic memory statistics"""
        if not self.concepts:
            return {'total_concepts': 0, 'total_relationships': 0}
        
        importances = [c.importance for c in self.concepts.values()]
        confidences = [c.confidence for c in self.concepts.values()]
        access_counts = [c.access_count for c in self.concepts.values()]
        
        return {
            'total_concepts': len(self.concepts),
            'total_relationships': len(self.relationships),
            'avg_importance': sum(importances) / len(importances),
            'avg_confidence': sum(confidences) / len(confidences),
            'total_domains': len(self.knowledge_domains),
            'total_tags': len(self.tag_index),
            'avg_access_count': sum(access_counts) / len(access_counts),
            'max_access_count': max(access_counts) if access_counts else 0
        }
    
    async def export_knowledge(self, file_path: str = None) -> Dict[str, Any]:
        """Export semantic knowledge to dictionary format"""
        concepts_data = {}
        for concept_id, concept in self.concepts.items():
            concepts_data[concept_id] = concept.to_dict()
        
        relationships_data = []
        for rel in self.relationships:
            relationships_data.append({
                'source_id': rel.source_id,
                'target_id': rel.target_id,
                'relation_type': rel.relation_type,
                'strength': rel.strength,
                'properties': rel.properties,
                'bidirectional': rel.bidirectional,
                'created_at': rel.created_at.isoformat()
            })
        
        export_data = {
            'concepts': concepts_data,
            'relationships': relationships_data,
            'knowledge_domains': {k: list(v) for k, v in self.knowledge_domains.items()},
            'statistics': self.get_statistics(),
            'export_timestamp': datetime.now().isoformat()
        }
        
        if file_path:
            with open(file_path, 'w') as f:
                json.dump(export_data, f, indent=2)
        
        return export_data
    
    async def import_knowledge(self, data: Dict[str, Any]) -> Tuple[int, int]:
        """Import semantic knowledge from dictionary format"""
        concepts_imported = 0
        relationships_imported = 0
        
        # Import concepts
        if 'concepts' in data:
            for concept_id, concept_data in data['concepts'].items():
                try:
                    concept = Concept.from_dict(concept_data)
                    self.concepts[concept.id] = concept
                    await self._update_concept_indexes(concept)
                    await self._auto_organize_concept(concept)
                    concepts_imported += 1
                except Exception as e:
                    self.logger.error(f"Failed to import concept {concept_id}: {str(e)}")
        
        # Import relationships
        if 'relationships' in data:
            for rel_data in data['relationships']:
                try:
                    relationship = Relationship(
                        source_id=rel_data['source_id'],
                        target_id=rel_data['target_id'],
                        relation_type=rel_data['relation_type'],
                        strength=rel_data.get('strength', 1.0),
                        properties=rel_data.get('properties', {}),
                        bidirectional=rel_data.get('bidirectional', False),
                        created_at=datetime.fromisoformat(rel_data['created_at'])
                    )
                    self.relationships.append(relationship)
                    relationships_imported += 1
                except Exception as e:
                    self.logger.error(f"Failed to import relationship: {str(e)}")
        
        self.logger.info(f"Imported {concepts_imported} concepts and {relationships_imported} relationships")
        return concepts_imported, relationships_imported
