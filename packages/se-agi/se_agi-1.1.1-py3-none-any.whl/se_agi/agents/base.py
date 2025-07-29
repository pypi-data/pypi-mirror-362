"""
Base Agent class for SE-AGI
Provides foundation for all specialized agents
"""

import asyncio
import logging
import uuid
from typing import Dict, List, Optional, Any, Union, Callable
from dataclasses import dataclass
from datetime import datetime
from abc import ABC, abstractmethod
from enum import Enum

from ..core.config import AgentConfig


class AgentState(Enum):
    """Agent operational states"""
    INACTIVE = "inactive"
    INITIALIZING = "initializing"
    ACTIVE = "active"
    BUSY = "busy"
    ERROR = "error"
    SHUTDOWN = "shutdown"


class MessageType(Enum):
    """Types of inter-agent messages"""
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"
    BROADCAST = "broadcast"
    COORDINATION = "coordination"


@dataclass
class AgentMessage:
    """Message between agents"""
    id: str
    sender_id: str
    recipient_id: Optional[str]  # None for broadcast
    message_type: MessageType
    content: Any
    timestamp: datetime
    priority: int = 1
    context: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.context is None:
            self.context = {}


@dataclass
class AgentResponse:
    """Response from agent processing"""
    content: str
    confidence: float
    reasoning: Optional[str] = None
    metadata: Dict[str, Any] = None
    timestamp: datetime = None
    success: bool = True
    error_message: Optional[str] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.metadata is None:
            self.metadata = {}


@dataclass
class AgentCapability:
    """Represents an agent capability"""
    name: str
    description: str
    input_types: List[str]
    output_types: List[str]
    confidence_level: float
    prerequisites: List[str] = None
    
    def __post_init__(self):
        if self.prerequisites is None:
            self.prerequisites = []


class BaseAgent(ABC):
    """
    Base class for all SE-AGI agents
    
    Provides common functionality:
    - Message handling and communication
    - Memory integration
    - State management
    - Capability registration
    - Performance monitoring
    """
    
    def __init__(self, 
                 config: AgentConfig,
                 memory_systems: Optional[Dict[str, Any]] = None):
        self.config = config
        self.name = config.name
        self.agent_type = config.agent_type
        self.agent_id = str(uuid.uuid4())
        
        # State management
        self.state = AgentState.INACTIVE
        self.creation_time = datetime.now()
        self.last_activity = datetime.now()
        
        # Memory systems
        self.memory_systems = memory_systems or {}
        
        # Communication
        self.message_queue = asyncio.Queue()
        self.message_handlers: Dict[MessageType, Callable] = {}
        self.subscriptions: List[str] = []  # Message types subscribed to
        
        # Capabilities
        self.capabilities: Dict[str, AgentCapability] = {}
        self._register_capabilities()
        
        # Performance tracking
        self.task_count = 0
        self.success_count = 0
        self.error_count = 0
        self.average_response_time = 0.0
        self.performance_history: List[Dict[str, Any]] = []
        
        # Learning and adaptation
        self.learning_enabled = True
        self.adaptation_data = {}
        
        # Setup logging
        self.logger = logging.getLogger(f"{__name__}.{self.name}")
        
        # Setup message handlers
        self._setup_message_handlers()
    
    async def initialize(self) -> None:
        """Initialize the agent"""
        self.state = AgentState.INITIALIZING
        self.logger.info(f"Initializing agent {self.name} ({self.agent_type})")
        
        try:
            # Initialize memory connections
            await self._initialize_memory_connections()
            
            # Initialize agent-specific components
            await self._initialize_agent_specifics()
            
            # Start message processing
            asyncio.create_task(self._message_processing_loop())
            
            self.state = AgentState.ACTIVE
            self.logger.info(f"Agent {self.name} initialized successfully")
            
        except Exception as e:
            self.state = AgentState.ERROR
            self.logger.error(f"Failed to initialize agent {self.name}: {e}")
            raise
    
    @abstractmethod
    async def _initialize_agent_specifics(self) -> None:
        """Initialize agent-specific components (to be implemented by subclasses)"""
        pass
    
    @abstractmethod
    async def _process_task(self, 
                           task_description: str, 
                           context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        """Process a task (to be implemented by subclasses)"""
        pass
    
    @abstractmethod
    def _register_capabilities(self) -> None:
        """Register agent capabilities (to be implemented by subclasses)"""
        pass
    
    async def process(self, 
                     input_text: str, 
                     context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        """
        Main processing method for the agent
        
        Args:
            input_text: Input to process
            context: Additional context information
            
        Returns:
            AgentResponse with results
        """
        if self.state != AgentState.ACTIVE:
            return AgentResponse(
                content="Agent not available",
                confidence=0.0,
                success=False,
                error_message=f"Agent state is {self.state.value}"
            )
        
        start_time = datetime.now()
        self.state = AgentState.BUSY
        self.task_count += 1
        
        try:
            # Store input in working memory
            await self._store_in_memory("working", {
                "type": "input",
                "content": input_text,
                "context": context,
                "timestamp": start_time
            })
            
            # Process the task
            response = await self._process_task(input_text, context)
            
            # Update performance metrics
            processing_time = (datetime.now() - start_time).total_seconds()
            await self._update_performance_metrics(processing_time, response.success)
            
            # Store results in memory
            await self._store_in_memory("episodic", {
                "type": "task_completion",
                "input": input_text,
                "output": response.content,
                "context": context,
                "processing_time": processing_time,
                "success": response.success,
                "timestamp": datetime.now()
            })
            
            # Learn from interaction if enabled
            if self.learning_enabled:
                await self._learn_from_interaction(input_text, response, context)
            
            self.success_count += 1 if response.success else 0
            self.error_count += 0 if response.success else 1
            
            self.state = AgentState.ACTIVE
            self.last_activity = datetime.now()
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error processing task: {e}")
            self.error_count += 1
            self.state = AgentState.ACTIVE
            
            return AgentResponse(
                content="I encountered an error while processing your request.",
                confidence=0.0,
                success=False,
                error_message=str(e)
            )
    
    async def send_message(self, 
                          recipient_id: Optional[str],
                          message_type: MessageType,
                          content: Any,
                          priority: int = 1,
                          context: Optional[Dict[str, Any]] = None) -> str:
        """Send a message to another agent or broadcast"""
        message = AgentMessage(
            id=str(uuid.uuid4()),
            sender_id=self.agent_id,
            recipient_id=recipient_id,
            message_type=message_type,
            content=content,
            timestamp=datetime.now(),
            priority=priority,
            context=context or {}
        )
        
        # For now, just log the message (would integrate with communication system)
        self.logger.info(f"Sending message {message.id} to {recipient_id or 'broadcast'}")
        
        return message.id
    
    async def receive_message(self, message: AgentMessage) -> None:
        """Receive a message from another agent"""
        await self.message_queue.put(message)
    
    async def _message_processing_loop(self) -> None:
        """Background loop for processing messages"""
        while self.state != AgentState.SHUTDOWN:
            try:
                # Get message with timeout
                message = await asyncio.wait_for(
                    self.message_queue.get(), 
                    timeout=1.0
                )
                
                # Process message
                await self._handle_message(message)
                
            except asyncio.TimeoutError:
                # No message received, continue
                continue
            except Exception as e:
                self.logger.error(f"Error in message processing loop: {e}")
    
    async def _handle_message(self, message: AgentMessage) -> None:
        """Handle incoming message"""
        handler = self.message_handlers.get(message.message_type)
        if handler:
            try:
                await handler(message)
            except Exception as e:
                self.logger.error(f"Error handling message {message.id}: {e}")
        else:
            self.logger.warning(f"No handler for message type {message.message_type}")
    
    def _setup_message_handlers(self) -> None:
        """Setup default message handlers"""
        self.message_handlers = {
            MessageType.REQUEST: self._handle_request,
            MessageType.RESPONSE: self._handle_response,
            MessageType.NOTIFICATION: self._handle_notification,
            MessageType.BROADCAST: self._handle_broadcast,
            MessageType.COORDINATION: self._handle_coordination
        }
    
    async def _handle_request(self, message: AgentMessage) -> None:
        """Handle request message"""
        # Process the request and send response
        response = await self.process(str(message.content), message.context)
        
        # Send response back
        await self.send_message(
            recipient_id=message.sender_id,
            message_type=MessageType.RESPONSE,
            content=response,
            context={"original_message_id": message.id}
        )
    
    async def _handle_response(self, message: AgentMessage) -> None:
        """Handle response message"""
        # Store response for correlation with original request
        self.logger.info(f"Received response from {message.sender_id}")
        
        # Store in memory
        await self._store_in_memory("episodic", {
            "type": "response_received",
            "sender": message.sender_id,
            "content": message.content,
            "timestamp": message.timestamp
        })
    
    async def _handle_notification(self, message: AgentMessage) -> None:
        """Handle notification message"""
        self.logger.info(f"Received notification: {message.content}")
        
        # Store in memory
        await self._store_in_memory("working", {
            "type": "notification",
            "content": message.content,
            "sender": message.sender_id,
            "timestamp": message.timestamp
        })
    
    async def _handle_broadcast(self, message: AgentMessage) -> None:
        """Handle broadcast message"""
        self.logger.info(f"Received broadcast: {message.content}")
        
        # Process broadcast based on content
        if message.content.get("type") == "system_update":
            await self._handle_system_update(message.content)
        elif message.content.get("type") == "capability_announcement":
            await self._handle_capability_announcement(message.content)
    
    async def _handle_coordination(self, message: AgentMessage) -> None:
        """Handle coordination message"""
        coordination_type = message.content.get("type")
        
        if coordination_type == "task_assignment":
            await self._handle_task_assignment(message.content)
        elif coordination_type == "capability_request":
            await self._handle_capability_request(message.content, message.sender_id)
        elif coordination_type == "performance_sync":
            await self._handle_performance_sync(message.content)
    
    async def _handle_system_update(self, content: Dict[str, Any]) -> None:
        """Handle system update broadcast"""
        update_type = content.get("update_type")
        
        if update_type == "config_change":
            await self._apply_config_changes(content.get("changes", {}))
        elif update_type == "capability_evolution":
            await self._adapt_to_capability_evolution(content.get("evolution_data", {}))
    
    async def _handle_capability_announcement(self, content: Dict[str, Any]) -> None:
        """Handle capability announcement from other agents"""
        announcing_agent = content.get("agent_id")
        new_capabilities = content.get("capabilities", [])
        
        # Update knowledge of other agents' capabilities
        await self._store_in_memory("semantic", {
            "type": "agent_capabilities",
            "agent_id": announcing_agent,
            "capabilities": new_capabilities,
            "timestamp": datetime.now()
        })
    
    async def _handle_task_assignment(self, content: Dict[str, Any]) -> None:
        """Handle task assignment from coordinator"""
        task = content.get("task")
        if task and self._can_handle_task(task):
            await self.process(task.get("description", ""), task.get("context", {}))
    
    async def _handle_capability_request(self, content: Dict[str, Any], requester_id: str) -> None:
        """Handle capability request from another agent"""
        requested_capability = content.get("capability")
        
        if requested_capability in self.capabilities:
            # Send capability information
            await self.send_message(
                recipient_id=requester_id,
                message_type=MessageType.RESPONSE,
                content={
                    "capability": self.capabilities[requested_capability],
                    "available": True
                }
            )
        else:
            # Capability not available
            await self.send_message(
                recipient_id=requester_id,
                message_type=MessageType.RESPONSE,
                content={
                    "capability": requested_capability,
                    "available": False
                }
            )
    
    async def _handle_performance_sync(self, content: Dict[str, Any]) -> None:
        """Handle performance synchronization request"""
        # Share performance metrics
        performance_data = {
            "agent_id": self.agent_id,
            "task_count": self.task_count,
            "success_rate": self.success_count / max(self.task_count, 1),
            "average_response_time": self.average_response_time,
            "capabilities": list(self.capabilities.keys())
        }
        
        # Broadcast performance data
        await self.send_message(
            recipient_id=None,  # Broadcast
            message_type=MessageType.BROADCAST,
            content={
                "type": "performance_data",
                "data": performance_data
            }
        )
    
    def _can_handle_task(self, task: Dict[str, Any]) -> bool:
        """Check if agent can handle a specific task"""
        required_capabilities = task.get("required_capabilities", [])
        return all(cap in self.capabilities for cap in required_capabilities)
    
    async def _initialize_memory_connections(self) -> None:
        """Initialize connections to memory systems"""
        for memory_type, memory_system in self.memory_systems.items():
            if hasattr(memory_system, 'add_subscriber'):
                await memory_system.add_subscriber(self.agent_id)
    
    async def _store_in_memory(self, memory_type: str, data: Dict[str, Any]) -> None:
        """Store data in specified memory system"""
        memory_system = self.memory_systems.get(memory_type)
        if memory_system and hasattr(memory_system, 'store'):
            try:
                await memory_system.store(data)
            except Exception as e:
                self.logger.error(f"Failed to store in {memory_type} memory: {e}")
    
    async def _retrieve_from_memory(self, 
                                   memory_type: str, 
                                   query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Retrieve data from specified memory system"""
        memory_system = self.memory_systems.get(memory_type)
        if memory_system and hasattr(memory_system, 'retrieve'):
            try:
                return await memory_system.retrieve(query)
            except Exception as e:
                self.logger.error(f"Failed to retrieve from {memory_type} memory: {e}")
        return []
    
    async def _update_performance_metrics(self, processing_time: float, success: bool) -> None:
        """Update agent performance metrics"""
        # Update average response time
        if self.task_count > 1:
            self.average_response_time = (
                (self.average_response_time * (self.task_count - 1) + processing_time) / 
                self.task_count
            )
        else:
            self.average_response_time = processing_time
        
        # Store performance data point
        performance_point = {
            "timestamp": datetime.now(),
            "processing_time": processing_time,
            "success": success,
            "task_count": self.task_count
        }
        
        self.performance_history.append(performance_point)
        
        # Keep only recent history (last 100 data points)
        if len(self.performance_history) > 100:
            self.performance_history = self.performance_history[-100:]
    
    async def _learn_from_interaction(self, 
                                    input_text: str, 
                                    response: AgentResponse, 
                                    context: Optional[Dict[str, Any]]) -> None:
        """Learn from interaction (basic implementation)"""
        # Store learning data
        learning_data = {
            "input": input_text,
            "response_quality": response.confidence,
            "success": response.success,
            "context": context,
            "timestamp": datetime.now()
        }
        
        # Update adaptation data
        if response.success:
            # Reinforce successful patterns
            input_type = self._classify_input_type(input_text)
            if input_type not in self.adaptation_data:
                self.adaptation_data[input_type] = {"success_count": 0, "patterns": []}
            
            self.adaptation_data[input_type]["success_count"] += 1
            self.adaptation_data[input_type]["patterns"].append({
                "input_length": len(input_text),
                "response_confidence": response.confidence,
                "processing_successful": True
            })
        
        # Store in episodic memory for meta-learning
        await self._store_in_memory("episodic", {
            "type": "learning_interaction",
            "agent_id": self.agent_id,
            "learning_data": learning_data,
            "timestamp": datetime.now()
        })
    
    def _classify_input_type(self, input_text: str) -> str:
        """Classify input type for learning purposes"""
        # Simple classification based on keywords and patterns
        text_lower = input_text.lower()
        
        if any(word in text_lower for word in ["question", "what", "how", "why", "when", "where"]):
            return "question"
        elif any(word in text_lower for word in ["analyze", "research", "investigate", "study"]):
            return "analysis"
        elif any(word in text_lower for word in ["create", "generate", "make", "build", "design"]):
            return "creation"
        elif any(word in text_lower for word in ["help", "assist", "support"]):
            return "assistance"
        else:
            return "general"
    
    async def _apply_config_changes(self, changes: Dict[str, Any]) -> None:
        """Apply configuration changes"""
        for key, value in changes.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
                self.logger.info(f"Applied config change: {key} = {value}")
    
    async def _adapt_to_capability_evolution(self, evolution_data: Dict[str, Any]) -> None:
        """Adapt to capability evolution"""
        new_capabilities = evolution_data.get("new_capabilities", [])
        
        for capability_data in new_capabilities:
            if self._should_adopt_capability(capability_data):
                await self._adopt_new_capability(capability_data)
    
    def _should_adopt_capability(self, capability_data: Dict[str, Any]) -> bool:
        """Check if agent should adopt a new capability"""
        # Simple heuristic - adopt if it aligns with agent type
        capability_type = capability_data.get("type", "")
        return capability_type in self.config.capabilities
    
    async def _adopt_new_capability(self, capability_data: Dict[str, Any]) -> None:
        """Adopt a new capability"""
        capability = AgentCapability(
            name=capability_data.get("name", ""),
            description=capability_data.get("description", ""),
            input_types=capability_data.get("input_types", []),
            output_types=capability_data.get("output_types", []),
            confidence_level=capability_data.get("confidence_level", 0.5),
            prerequisites=capability_data.get("prerequisites", [])
        )
        
        self.capabilities[capability.name] = capability
        self.logger.info(f"Adopted new capability: {capability.name}")
        
        # Announce new capability
        await self.send_message(
            recipient_id=None,  # Broadcast
            message_type=MessageType.BROADCAST,
            content={
                "type": "capability_announcement",
                "agent_id": self.agent_id,
                "capabilities": [capability.name]
            }
        )
    
    # Public API methods
    
    def get_capabilities(self) -> List[str]:
        """Get list of agent capabilities"""
        return list(self.capabilities.keys())
    
    def get_detailed_capabilities(self) -> Dict[str, AgentCapability]:
        """Get detailed capability information"""
        return self.capabilities.copy()
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        uptime = (datetime.now() - self.creation_time).total_seconds()
        success_rate = self.success_count / max(self.task_count, 1)
        
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "type": self.agent_type,
            "state": self.state.value,
            "uptime_seconds": uptime,
            "task_count": self.task_count,
            "success_count": self.success_count,
            "error_count": self.error_count,
            "success_rate": success_rate,
            "average_response_time": self.average_response_time,
            "capabilities_count": len(self.capabilities),
            "last_activity": self.last_activity
        }
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        if not self.performance_history:
            return {"status": "no_performance_data"}
        
        recent_performance = self.performance_history[-10:]  # Last 10 tasks
        recent_success_rate = sum(1 for p in recent_performance if p["success"]) / len(recent_performance)
        recent_avg_time = sum(p["processing_time"] for p in recent_performance) / len(recent_performance)
        
        return {
            "overall_success_rate": self.success_count / max(self.task_count, 1),
            "recent_success_rate": recent_success_rate,
            "average_response_time": self.average_response_time,
            "recent_average_time": recent_avg_time,
            "total_tasks": self.task_count,
            "performance_trend": self._analyze_performance_trend()
        }
    
    def _analyze_performance_trend(self) -> str:
        """Analyze performance trend"""
        if len(self.performance_history) < 5:
            return "insufficient_data"
        
        # Simple trend analysis
        first_half = self.performance_history[:len(self.performance_history)//2]
        second_half = self.performance_history[len(self.performance_history)//2:]
        
        first_half_success = sum(1 for p in first_half if p["success"]) / len(first_half)
        second_half_success = sum(1 for p in second_half if p["success"]) / len(second_half)
        
        if second_half_success > first_half_success + 0.1:
            return "improving"
        elif second_half_success < first_half_success - 0.1:
            return "declining"
        else:
            return "stable"
    
    async def shutdown(self) -> None:
        """Shutdown the agent"""
        self.logger.info(f"Shutting down agent {self.name}")
        self.state = AgentState.SHUTDOWN
        
        # Save final state
        await self._save_agent_state()
        
        self.logger.info(f"Agent {self.name} shutdown complete")
    
    async def _save_agent_state(self) -> None:
        """Save agent state for persistence"""
        state_data = {
            "agent_id": self.agent_id,
            "name": self.name,
            "type": self.agent_type,
            "capabilities": {name: cap.__dict__ for name, cap in self.capabilities.items()},
            "performance_metrics": {
                "task_count": self.task_count,
                "success_count": self.success_count,
                "error_count": self.error_count,
                "average_response_time": self.average_response_time
            },
            "adaptation_data": self.adaptation_data,
            "shutdown_time": datetime.now()
        }
        
        # Store in semantic memory for persistence
        await self._store_in_memory("semantic", {
            "type": "agent_state_snapshot",
            "agent_data": state_data,
            "timestamp": datetime.now()
        })
