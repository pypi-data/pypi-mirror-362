"""
SE-AGI: Self-Evolving General AI
Main system class that orchestrates all components
"""

import asyncio
import logging
import time
from typing import Dict, List, Optional, Any, Callable, Union
from dataclasses import dataclass
import uuid
from datetime import datetime
import json

from ..core.config import SEAGIConfig, AgentConfig, SafetyLevel
from ..core.meta_learner import MetaLearner
from ..core.reflection import ReflectionEngine
from ..agents.base import BaseAgent
from ..agents.meta_agent import MetaAgent
from ..reasoning.multimodal import MultiModalReasoner
from ..memory.episodic import EpisodicMemory
from ..memory.semantic import SemanticMemory
from ..memory.working import WorkingMemory
from ..evolution.capability_evolution import CapabilityEvolver
from ..safety.monitor import SafetyMonitor
from ..safety.alignment import AlignmentChecker
from ..utils.logging import setup_logging
from ..utils.metrics import MetricsCollector
from ..licensing.decorators import requires_license, licensed_capability
from ..licensing.validation import validate_seagi_license, check_agent_limit, is_evolution_enabled


@dataclass
class SEAGIResponse:
    """Response from SE-AGI system"""
    content: str
    reasoning: Optional[str] = None
    confidence: float = 0.0
    agent_contributions: Dict[str, Any] = None
    metadata: Dict[str, Any] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.agent_contributions is None:
            self.agent_contributions = {}
        if self.metadata is None:
            self.metadata = {}


@dataclass
class Task:
    """Task representation for SE-AGI"""
    id: str
    description: str
    priority: int = 1
    deadline: Optional[datetime] = None
    context: Dict[str, Any] = None
    requirements: List[str] = None
    success_criteria: List[str] = None
    
    def __post_init__(self):
        if self.context is None:
            self.context = {}
        if self.requirements is None:
            self.requirements = []
        if self.success_criteria is None:
            self.success_criteria = []


class SEAGI:
    """
    Self-Evolving General AI System
    
    The main orchestrator that coordinates all subsystems:
    - Meta-learning and adaptation
    - Multi-agent coordination
    - Self-reflection and improvement
    - Memory management
    - Safety monitoring
    - Capability evolution
    """
    
    def __init__(self, config: Optional[SEAGIConfig] = None):
        """Initialize SE-AGI system"""
        self.config = config or SEAGIConfig()
        self.instance_id = str(uuid.uuid4())
        self.start_time = datetime.now()
        self.is_initialized = False
        self.is_running = False
        
        # Setup logging
        self.logger = setup_logging(f"SEAGI-{self.instance_id}")
        self.logger.info(f"Initializing SE-AGI system {self.instance_id}")
        
        # Core components
        self.meta_learner: Optional[MetaLearner] = None
        self.reflection_engine: Optional[ReflectionEngine] = None
        self.multimodal_reasoner: Optional[MultiModalReasoner] = None
        self.capability_evolver: Optional[CapabilityEvolver] = None
        self.safety_monitor: Optional[SafetyMonitor] = None
        self.alignment_checker: Optional[AlignmentChecker] = None
        
        # Memory systems
        self.working_memory: Optional[WorkingMemory] = None
        self.episodic_memory: Optional[EpisodicMemory] = None
        self.semantic_memory: Optional[SemanticMemory] = None
        
        # Agent management
        self.agents: Dict[str, BaseAgent] = {}
        self.meta_agent: Optional[MetaAgent] = None
        
        # Task management
        self.task_queue: asyncio.Queue = asyncio.Queue()
        self.active_tasks: Dict[str, Task] = {}
        self.completed_tasks: List[Task] = []
        
        # Metrics and monitoring
        self.metrics = MetricsCollector()
        self.performance_history: List[Dict[str, Any]] = []
        
        # Evolution tracking
        self.generation = 0
        self.capability_history: List[Dict[str, Any]] = []
        
    async def initialize(self) -> None:
        """Initialize all system components"""
        if self.is_initialized:
            self.logger.warning("System already initialized")
            return
            
        self.logger.info("Starting system initialization...")
        
        # Validate license before initialization
        try:
            validate_seagi_license(["core"])
            self.logger.info("✅ License validated successfully")
        except Exception as e:
            self.logger.warning(f"License validation failed: {e}")
        
        try:
            # Initialize memory systems
            await self._initialize_memory_systems()
            
            # Initialize core components
            await self._initialize_core_components()
            
            # Initialize safety systems
            await self._initialize_safety_systems()
            
            # Initialize agents
            await self._initialize_agents()
            
            # Start background tasks
            await self._start_background_tasks()
            
            self.is_initialized = True
            self.logger.info("SE-AGI system initialization complete")
            
        except Exception as e:
            self.logger.error(f"Initialization failed: {e}")
            raise
    
    async def _initialize_memory_systems(self) -> None:
        """Initialize memory subsystems"""
        self.logger.info("Initializing memory systems...")
        
        self.working_memory = WorkingMemory(
            capacity=self.config.memory.working_memory_size
        )
        
        self.episodic_memory = EpisodicMemory(
            capacity=self.config.memory.episodic_memory_size,
            consolidation_enabled=self.config.memory.consolidation_enabled
        )
        
        self.semantic_memory = SemanticMemory(
            capacity=self.config.memory.semantic_memory_size,
            similarity_threshold=self.config.memory.similarity_threshold
        )
        
        await self.working_memory.initialize()
        await self.episodic_memory.initialize()
        await self.semantic_memory.initialize()
    
    async def _initialize_core_components(self) -> None:
        """Initialize core processing components"""
        self.logger.info("Initializing core components...")
        
        # Meta-learning system
        if self.config.meta_learning.enabled:
            self.meta_learner = MetaLearner(
                config=self.config.meta_learning,
                memory_system=self.episodic_memory
            )
            await self.meta_learner.initialize()
        
        # Self-reflection engine
        if self.config.reflection.enabled:
            self.reflection_engine = ReflectionEngine(
                config=self.config.reflection,
                memory_system=self.episodic_memory
            )
            await self.reflection_engine.initialize()
        
        # Multi-modal reasoning
        self.multimodal_reasoner = MultiModalReasoner()
        await self.multimodal_reasoner.initialize()
        
        # Capability evolution
        if self.config.evolution.enabled:
            self.capability_evolver = CapabilityEvolver(
                config=self.config.evolution,
                meta_learner=self.meta_learner
            )
            await self.capability_evolver.initialize()
    
    async def _initialize_safety_systems(self) -> None:
        """Initialize safety and alignment systems"""
        self.logger.info("Initializing safety systems...")
        
        self.safety_monitor = SafetyMonitor(
            config=self.config.safety,
            memory_system=self.episodic_memory
        )
        
        self.alignment_checker = AlignmentChecker(
            config=self.config.safety,
            constitutional_rules=self.config.safety.constitutional_rules
        )
        
        await self.safety_monitor.initialize()
        await self.alignment_checker.initialize()
    
    async def _initialize_agents(self) -> None:
        """Initialize agent ecosystem"""
        self.logger.info("Initializing agents...")
        
        # Create meta-agent for coordination
        self.meta_agent = MetaAgent(
            config=AgentConfig(name="meta_agent", agent_type="meta"),
            memory_systems={
                "working": self.working_memory,
                "episodic": self.episodic_memory,
                "semantic": self.semantic_memory
            }
        )
        await self.meta_agent.initialize()
        
        # Initialize configured agents
        for agent_name, agent_config in self.config.agents.items():
            await self.add_agent_from_config(agent_config)
    
    async def _start_background_tasks(self) -> None:
        """Start background processing tasks"""
        self.logger.info("Starting background tasks...")
        
        # Task processing loop
        asyncio.create_task(self._task_processing_loop())
        
        # Memory consolidation
        if self.config.memory.consolidation_enabled:
            asyncio.create_task(self._memory_consolidation_loop())
        
        # Self-reflection loop
        if self.reflection_engine:
            asyncio.create_task(self._reflection_loop())
        
        # Evolution loop
        if self.capability_evolver:
            asyncio.create_task(self._evolution_loop())
        
        # Safety monitoring
        asyncio.create_task(self._safety_monitoring_loop())
        
        # Metrics collection
        asyncio.create_task(self._metrics_collection_loop())
    
    async def process(self, 
                     input_text: str, 
                     context: Optional[Dict[str, Any]] = None,
                     modalities: Optional[List[str]] = None) -> SEAGIResponse:
        """
        Process input and generate response
        
        Args:
            input_text: Input text to process
            context: Additional context information
            modalities: List of modalities to consider (text, vision, audio, etc.)
            
        Returns:
            SEAGIResponse with generated content and metadata
        """
        if not self.is_initialized:
            raise RuntimeError("System not initialized. Call initialize() first.")
        
        start_time = time.time()
        task_id = str(uuid.uuid4())
        
        # Safety check
        safety_result = await self.safety_monitor.check_input(input_text, context)
        if not safety_result.is_safe:
            return SEAGIResponse(
                content="I cannot process this request due to safety concerns.",
                reasoning=safety_result.reason,
                confidence=1.0,
                metadata={"safety_blocked": True}
            )
        
        try:
            # Store in working memory
            await self.working_memory.store({
                "type": "input",
                "content": input_text,
                "context": context or {},
                "timestamp": datetime.now(),
                "task_id": task_id
            })
            
            # Multi-modal analysis
            modality_results = {}
            if modalities:
                for modality in modalities:
                    result = await self.multimodal_reasoner.process_modality(
                        modality, input_text, context
                    )
                    modality_results[modality] = result
            
            # Agent coordination for processing
            agent_contributions = {}
            if self.meta_agent:
                coordination_plan = await self.meta_agent.plan_task_execution(
                    input_text, context, self.agents
                )
                
                for agent_name, subtask in coordination_plan.items():
                    if agent_name in self.agents:
                        agent_result = await self.agents[agent_name].process(
                            subtask, context
                        )
                        agent_contributions[agent_name] = agent_result
            
            # Synthesize response
            response_content = await self._synthesize_response(
                input_text, agent_contributions, modality_results, context
            )
            
            # Meta-learning update
            if self.meta_learner:
                await self.meta_learner.update_from_interaction(
                    input_text, response_content, agent_contributions
                )
            
            # Store in episodic memory
            await self.episodic_memory.store_episode({
                "task_id": task_id,
                "input": input_text,
                "output": response_content,
                "context": context,
                "agent_contributions": agent_contributions,
                "processing_time": time.time() - start_time,
                "timestamp": datetime.now()
            })
            
            # Calculate confidence
            confidence = await self._calculate_confidence(
                response_content, agent_contributions
            )
            
            # Create response
            response = SEAGIResponse(
                content=response_content,
                confidence=confidence,
                agent_contributions=agent_contributions,
                metadata={
                    "task_id": task_id,
                    "processing_time": time.time() - start_time,
                    "modalities_used": list(modality_results.keys()),
                    "agents_involved": list(agent_contributions.keys())
                }
            )
            
            # Alignment check
            alignment_result = await self.alignment_checker.check_response(response)
            if not alignment_result.is_aligned:
                response.content = "I need to reconsider my response to ensure proper alignment."
                response.metadata["alignment_issue"] = alignment_result.issues
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error processing input: {e}")
            return SEAGIResponse(
                content="I encountered an error while processing your request.",
                confidence=0.0,
                metadata={"error": str(e)}
            )
    
    async def _synthesize_response(self, 
                                  input_text: str,
                                  agent_contributions: Dict[str, Any],
                                  modality_results: Dict[str, Any],
                                  context: Optional[Dict[str, Any]]) -> str:
        """Synthesize final response from all inputs"""
        if self.meta_agent:
            return await self.meta_agent.synthesize_response(
                input_text, agent_contributions, modality_results, context
            )
        
        # Fallback synthesis
        parts = []
        for agent_name, contribution in agent_contributions.items():
            if hasattr(contribution, 'content'):
                parts.append(f"{agent_name}: {contribution.content}")
            else:
                parts.append(f"{agent_name}: {str(contribution)}")
        
        return "\n".join(parts) if parts else "I need more information to provide a helpful response."
    
    async def _calculate_confidence(self, 
                                   response: str,
                                   agent_contributions: Dict[str, Any]) -> float:
        """Calculate confidence score for response"""
        if not agent_contributions:
            return 0.5
        
        # Simple confidence calculation based on agent agreement
        confidences = []
        for contribution in agent_contributions.values():
            if hasattr(contribution, 'confidence'):
                confidences.append(contribution.confidence)
        
        return sum(confidences) / len(confidences) if confidences else 0.5
    
    async def add_agent(self, agent: BaseAgent) -> None:
        """Add an agent to the system"""
        # Check agent limits based on license
        current_agent_count = len(self.agents)
        if not check_agent_limit(current_agent_count + 1):
            from ..licensing.exceptions import FeatureNotLicensedError
            raise FeatureNotLicensedError(
                feature="additional_agents",
                required_tier="pro",
                current_tier="basic"
            )
        
        await agent.initialize()
        self.agents[agent.name] = agent
        self.logger.info(f"Added agent: {agent.name}")
    
    async def add_agent_from_config(self, config: AgentConfig) -> None:
        """Create and add agent from configuration"""
        # Dynamic agent creation based on type
        agent_class = self._get_agent_class(config.agent_type)
        agent = agent_class(
            config=config,
            memory_systems={
                "working": self.working_memory,
                "episodic": self.episodic_memory,
                "semantic": self.semantic_memory
            }
        )
        await self.add_agent(agent)
    
    def _get_agent_class(self, agent_type: str):
        """Get agent class based on type"""
        from ..agents.research_agent import ResearchAgent
        from ..agents.creative_agent import CreativeAgent
        from ..agents.analysis_agent import AnalysisAgent
        from ..agents.tool_agent import ToolAgent
        
        agent_classes = {
            "research": ResearchAgent,
            "creative": CreativeAgent,
            "analysis": AnalysisAgent,
            "tool": ToolAgent,
            "base": BaseAgent
        }
        
        return agent_classes.get(agent_type, BaseAgent)
    
    async def evolve(self) -> None:
        """Trigger system evolution"""
        # Check if evolution is enabled in license
        if not is_evolution_enabled():
            from ..licensing.exceptions import FeatureNotLicensedError
            raise FeatureNotLicensedError(
                feature="capability_evolution",
                required_tier="pro",
                current_tier="basic"
            )
        
        if not self.capability_evolver:
            self.logger.warning("Evolution not enabled")
            return
        
        self.logger.info("Starting capability evolution...")
        evolution_result = await self.capability_evolver.evolve()
        
        if evolution_result.success:
            self.generation += 1
            self.capability_history.append({
                "generation": self.generation,
                "timestamp": datetime.now(),
                "improvements": evolution_result.improvements,
                "new_capabilities": evolution_result.new_capabilities
            })
            self.logger.info(f"Evolution complete. Generation: {self.generation}")
    
    async def shutdown(self) -> None:
        """Gracefully shutdown the system"""
        self.logger.info("Shutting down SE-AGI system...")
        self.is_running = False
        
        # Save checkpoints
        if self.config.save_checkpoints:
            await self._save_checkpoint()
        
        # Shutdown components
        for agent in self.agents.values():
            await agent.shutdown()
        
        if self.meta_agent:
            await self.meta_agent.shutdown()
        
        self.logger.info("SE-AGI system shutdown complete")
    
    async def _save_checkpoint(self) -> None:
        """Save system state checkpoint"""
        checkpoint_data = {
            "instance_id": self.instance_id,
            "generation": self.generation,
            "start_time": self.start_time.isoformat(),
            "timestamp": datetime.now().isoformat(),
            "performance_history": self.performance_history,
            "capability_history": self.capability_history,
            "config": self.config.dict()
        }
        
        # Save to file (implement based on storage preference)
        checkpoint_path = f"checkpoints/seagi_{self.instance_id}_{self.generation}.json"
        import os
        os.makedirs(os.path.dirname(checkpoint_path), exist_ok=True)
        
        with open(checkpoint_path, 'w') as f:
            json.dump(checkpoint_data, f, indent=2, default=str)
        
        self.logger.info(f"Checkpoint saved: {checkpoint_path}")
    
    # Background task loops
    async def _task_processing_loop(self) -> None:
        """Background task processing loop"""
        while self.is_running:
            try:
                # Process queued tasks
                if not self.task_queue.empty():
                    task = await self.task_queue.get()
                    await self._process_task(task)
                else:
                    await asyncio.sleep(1)
            except Exception as e:
                self.logger.error(f"Error in task processing loop: {e}")
    
    async def _memory_consolidation_loop(self) -> None:
        """Background memory consolidation loop"""
        while self.is_running:
            try:
                await asyncio.sleep(self.config.memory.consolidation_interval)
                await self.episodic_memory.consolidate()
                await self.semantic_memory.consolidate()
            except Exception as e:
                self.logger.error(f"Error in memory consolidation: {e}")
    
    async def _reflection_loop(self) -> None:
        """Background self-reflection loop"""
        while self.is_running:
            try:
                if self.reflection_engine:
                    await self.reflection_engine.reflect()
                await asyncio.sleep(3600)  # Reflect every hour
            except Exception as e:
                self.logger.error(f"Error in reflection loop: {e}")
    
    async def _evolution_loop(self) -> None:
        """Background evolution loop"""
        while self.is_running:
            try:
                await asyncio.sleep(86400)  # Evolve daily
                await self.evolve()
            except Exception as e:
                self.logger.error(f"Error in evolution loop: {e}")
    
    async def _safety_monitoring_loop(self) -> None:
        """Background safety monitoring loop"""
        while self.is_running:
            try:
                await self.safety_monitor.monitor_system_state(self)
                await asyncio.sleep(60)  # Monitor every minute
            except Exception as e:
                self.logger.error(f"Error in safety monitoring: {e}")
    
    async def _metrics_collection_loop(self) -> None:
        """Background metrics collection loop"""
        while self.is_running:
            try:
                metrics = self.metrics.collect_system_metrics(self)
                self.performance_history.append(metrics)
                await asyncio.sleep(300)  # Collect every 5 minutes
            except Exception as e:
                self.logger.error(f"Error in metrics collection: {e}")
    
    async def _process_task(self, task: Task) -> None:
        """Process a single task"""
        self.active_tasks[task.id] = task
        try:
            result = await self.process(task.description, task.context)
            task.metadata = {"result": result, "completed_at": datetime.now()}
            self.completed_tasks.append(task)
        finally:
            self.active_tasks.pop(task.id, None)
    
    # Public API methods
    def get_status(self) -> Dict[str, Any]:
        """Get current system status"""
        return {
            "instance_id": self.instance_id,
            "generation": self.generation,
            "is_initialized": self.is_initialized,
            "is_running": self.is_running,
            "uptime": (datetime.now() - self.start_time).total_seconds(),
            "agents_count": len(self.agents),
            "active_tasks": len(self.active_tasks),
            "completed_tasks": len(self.completed_tasks),
            "safety_level": self.config.safety.safety_level.value,
            "evolution_enabled": self.config.evolution.enabled
        }
    
    def get_capabilities(self) -> List[str]:
        """Get list of current system capabilities"""
        capabilities = set()
        
        for agent in self.agents.values():
            capabilities.update(agent.get_capabilities())
        
        # Add core system capabilities
        capabilities.update([
            "meta_learning",
            "self_reflection", 
            "multi_modal_reasoning",
            "memory_management",
            "safety_monitoring",
            "capability_evolution"
        ])
        
        return sorted(list(capabilities))
    
    async def run_continuous(self) -> None:
        """Run system in continuous mode"""
        if not self.is_initialized:
            await self.initialize()
        
        self.is_running = True
        self.logger.info("SE-AGI system running in continuous mode")
        
        try:
            while self.is_running:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("Received shutdown signal")
        finally:
            await self.shutdown()
