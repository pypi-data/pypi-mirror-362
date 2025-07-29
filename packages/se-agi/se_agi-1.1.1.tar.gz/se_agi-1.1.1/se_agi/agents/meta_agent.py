"""
Meta-Agent for SE-AGI
Coordinates and orchestrates other agents
"""

import asyncio
import logging
import numpy as np
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass
from datetime import datetime
import json
from enum import Enum

from .base import BaseAgent, AgentResponse, AgentCapability, MessageType
from ..core.config import AgentConfig


class CoordinationStrategy(Enum):
    """Coordination strategies for multi-agent tasks"""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    HIERARCHICAL = "hierarchical"
    COLLABORATIVE = "collaborative"
    COMPETITIVE = "competitive"


class TaskDecomposition(Enum):
    """Task decomposition strategies"""
    DOMAIN_BASED = "domain_based"
    SKILL_BASED = "skill_based"
    COMPLEXITY_BASED = "complexity_based"
    TEMPORAL_BASED = "temporal_based"


@dataclass
class TaskAssignment:
    """Represents a task assignment to an agent"""
    agent_id: str
    subtask_description: str
    priority: int
    estimated_duration: float
    required_capabilities: List[str]
    dependencies: List[str] = None
    context: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.context is None:
            self.context = {}


@dataclass
class CoordinationPlan:
    """Represents a coordination plan for multi-agent execution"""
    plan_id: str
    task_description: str
    strategy: CoordinationStrategy
    assignments: List[TaskAssignment]
    estimated_total_duration: float
    success_criteria: List[str]
    fallback_plans: List[str] = None
    
    def __post_init__(self):
        if self.fallback_plans is None:
            self.fallback_plans = []


class MetaAgent(BaseAgent):
    """
    Meta-Agent for SE-AGI system
    
    Responsibilities:
    - Coordinate multiple agents
    - Decompose complex tasks
    - Optimize agent utilization
    - Synthesize multi-agent responses
    - Monitor system-wide performance
    - Adapt coordination strategies
    """
    
    def __init__(self, 
                 config: AgentConfig,
                 memory_systems: Optional[Dict[str, Any]] = None):
        
        # Initialize with meta-agent specific config
        config.agent_type = "meta"
        config.capabilities.extend([
            "task_decomposition",
            "agent_coordination", 
            "response_synthesis",
            "performance_optimization",
            "strategic_planning"
        ])
        
        super().__init__(config, memory_systems)
        
        # Meta-agent specific attributes
        self.available_agents: Dict[str, Dict[str, Any]] = {}
        self.agent_performance: Dict[str, Dict[str, float]] = {}
        self.coordination_history: List[CoordinationPlan] = []
        self.active_plans: Dict[str, CoordinationPlan] = {}
        
        # Strategy learning
        self.strategy_effectiveness: Dict[CoordinationStrategy, List[float]] = {
            strategy: [] for strategy in CoordinationStrategy
        }
        
        # Task decomposition models
        self.decomposition_patterns: Dict[str, List[str]] = {}
        
        # Response synthesis models
        self.synthesis_strategies: Dict[str, Any] = {}
        
    async def _initialize_agent_specifics(self) -> None:
        """Initialize meta-agent specific components"""
        self.logger.info("Initializing meta-agent specifics...")
        
        # Load coordination patterns
        await self._load_coordination_patterns()
        
        # Initialize synthesis strategies
        await self._initialize_synthesis_strategies()
        
        # Setup performance monitoring
        await self._setup_performance_monitoring()
        
        self.logger.info("Meta-agent initialization complete")
    
    def _register_capabilities(self) -> None:
        """Register meta-agent capabilities"""
        self.capabilities = {
            "task_decomposition": AgentCapability(
                name="task_decomposition",
                description="Break down complex tasks into manageable subtasks",
                input_types=["text", "structured_task"],
                output_types=["task_list", "coordination_plan"],
                confidence_level=0.9
            ),
            "agent_coordination": AgentCapability(
                name="agent_coordination",
                description="Coordinate multiple agents for task execution",
                input_types=["task_list", "agent_pool"],
                output_types=["coordination_plan", "execution_results"],
                confidence_level=0.85
            ),
            "response_synthesis": AgentCapability(
                name="response_synthesis",
                description="Synthesize responses from multiple agents",
                input_types=["agent_responses", "context"],
                output_types=["synthesized_response"],
                confidence_level=0.8
            ),
            "performance_optimization": AgentCapability(
                name="performance_optimization",
                description="Optimize agent performance and coordination",
                input_types=["performance_data", "coordination_history"],
                output_types=["optimization_plan"],
                confidence_level=0.75
            ),
            "strategic_planning": AgentCapability(
                name="strategic_planning",
                description="Plan strategic approaches for complex problems",
                input_types=["problem_description", "available_resources"],
                output_types=["strategic_plan"],
                confidence_level=0.8
            )
        }
    
    async def _process_task(self, 
                           task_description: str, 
                           context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        """Process task by coordinating other agents"""
        try:
            # Analyze task complexity
            task_complexity = await self._analyze_task_complexity(task_description, context)
            
            if task_complexity["requires_coordination"]:
                # Multi-agent coordination required
                response = await self._coordinate_multi_agent_task(task_description, context)
            else:
                # Simple task - handle directly or delegate to single agent
                response = await self._handle_simple_task(task_description, context)
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error in meta-agent task processing: {e}")
            return AgentResponse(
                content="I encountered an error while coordinating the task.",
                confidence=0.0,
                success=False,
                error_message=str(e)
            )
    
    async def _analyze_task_complexity(self, 
                                     task_description: str, 
                                     context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze task complexity to determine coordination needs"""
        complexity_indicators = {
            "requires_coordination": False,
            "estimated_agents_needed": 1,
            "complexity_score": 0.0,
            "required_capabilities": [],
            "estimated_duration": 60.0  # seconds
        }
        
        task_lower = task_description.lower()
        
        # Check for multi-domain requirements
        domains = ["research", "creative", "analysis", "technical", "communication"]
        domain_matches = sum(1 for domain in domains if domain in task_lower)
        
        if domain_matches > 1:
            complexity_indicators["requires_coordination"] = True
            complexity_indicators["estimated_agents_needed"] = min(domain_matches, 4)
        
        # Check for complexity keywords
        complex_keywords = [
            "comprehensive", "detailed", "thorough", "multi-step", 
            "analyze and create", "research and develop", "complex", "intricate"
        ]
        
        complexity_score = sum(1 for keyword in complex_keywords if keyword in task_lower)
        complexity_indicators["complexity_score"] = complexity_score / len(complex_keywords)
        
        if complexity_score > 2:
            complexity_indicators["requires_coordination"] = True
        
        # Estimate required capabilities
        capability_patterns = {
            "research": ["research", "investigate", "study", "analyze", "examine"],
            "creative": ["create", "generate", "design", "innovate", "imagine"],
            "analysis": ["analyze", "evaluate", "assess", "compare", "interpret"],
            "technical": ["implement", "code", "technical", "system", "algorithm"],
            "communication": ["explain", "communicate", "present", "summarize"]
        }
        
        for capability, patterns in capability_patterns.items():
            if any(pattern in task_lower for pattern in patterns):
                complexity_indicators["required_capabilities"].append(capability)
        
        # Estimate duration based on complexity
        base_duration = 60.0  # 1 minute
        if complexity_indicators["complexity_score"] > 0.5:
            base_duration *= (1 + complexity_indicators["complexity_score"]) * 2
        
        complexity_indicators["estimated_duration"] = min(base_duration, 1800.0)  # Max 30 minutes
        
        return complexity_indicators
    
    async def _coordinate_multi_agent_task(self, 
                                         task_description: str, 
                                         context: Optional[Dict[str, Any]]) -> AgentResponse:
        """Coordinate multiple agents for complex task execution"""
        # Create coordination plan
        plan = await self.plan_task_execution(task_description, context, self.available_agents)
        
        if not plan:
            return AgentResponse(
                content="I was unable to create a coordination plan for this task.",
                confidence=0.0,
                success=False,
                error_message="No suitable coordination plan found"
            )
        
        # Execute coordination plan
        execution_results = await self._execute_coordination_plan(plan)
        
        # Synthesize final response
        synthesized_response = await self._synthesize_multi_agent_response(
            task_description, execution_results, context
        )
        
        # Learn from coordination
        await self._learn_from_coordination(plan, execution_results, synthesized_response)
        
        return synthesized_response
    
    async def plan_task_execution(self, 
                                task_description: str, 
                                context: Optional[Dict[str, Any]],
                                available_agents: Dict[str, Any]) -> Dict[str, Any]:
        """
        Plan task execution across multiple agents
        
        Returns:
            Dictionary mapping agent names to their assigned subtasks
        """
        if not available_agents:
            return {}
        
        # Decompose task into subtasks
        subtasks = await self._decompose_task(task_description, context)
        
        # Select coordination strategy
        strategy = await self._select_coordination_strategy(subtasks, available_agents)
        
        # Assign tasks to agents
        assignments = await self._assign_tasks_to_agents(subtasks, available_agents, strategy)
        
        # Create execution plan
        execution_plan = {}
        for assignment in assignments:
            agent_name = self._get_agent_name_by_id(assignment.agent_id, available_agents)
            if agent_name:
                execution_plan[agent_name] = assignment.subtask_description
        
        return execution_plan
    
    async def _decompose_task(self, 
                            task_description: str, 
                            context: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Decompose complex task into subtasks"""
        subtasks = []
        
        # Analyze task for decomposition patterns
        task_type = await self._classify_task_type(task_description)
        
        if task_type == "research_and_create":
            subtasks = [
                {
                    "description": f"Research background information for: {task_description}",
                    "type": "research",
                    "priority": 1,
                    "estimated_duration": 180.0
                },
                {
                    "description": f"Analyze research findings and identify key insights",
                    "type": "analysis", 
                    "priority": 2,
                    "estimated_duration": 120.0,
                    "dependencies": ["research"]
                },
                {
                    "description": f"Create solution based on analysis: {task_description}",
                    "type": "creative",
                    "priority": 3,
                    "estimated_duration": 240.0,
                    "dependencies": ["analysis"]
                }
            ]
        
        elif task_type == "analyze_and_recommend":
            subtasks = [
                {
                    "description": f"Collect and organize data for: {task_description}",
                    "type": "research",
                    "priority": 1,
                    "estimated_duration": 120.0
                },
                {
                    "description": f"Perform detailed analysis of collected data",
                    "type": "analysis",
                    "priority": 2,
                    "estimated_duration": 180.0,
                    "dependencies": ["research"]
                },
                {
                    "description": f"Generate recommendations based on analysis",
                    "type": "synthesis",
                    "priority": 3,
                    "estimated_duration": 120.0,
                    "dependencies": ["analysis"]
                }
            ]
        
        elif task_type == "comprehensive_solution":
            subtasks = [
                {
                    "description": f"Research domain knowledge for: {task_description}",
                    "type": "research",
                    "priority": 1,
                    "estimated_duration": 200.0
                },
                {
                    "description": f"Generate creative approaches to: {task_description}",
                    "type": "creative",
                    "priority": 2,
                    "estimated_duration": 180.0
                },
                {
                    "description": f"Analyze feasibility and trade-offs of approaches",
                    "type": "analysis",
                    "priority": 3,
                    "estimated_duration": 150.0,
                    "dependencies": ["creative"]
                },
                {
                    "description": f"Synthesize comprehensive solution for: {task_description}",
                    "type": "synthesis",
                    "priority": 4,
                    "estimated_duration": 200.0,
                    "dependencies": ["research", "analysis"]
                }
            ]
        
        else:
            # Default decomposition
            subtasks = [
                {
                    "description": task_description,
                    "type": "general",
                    "priority": 1,
                    "estimated_duration": 120.0
                }
            ]
        
        return subtasks
    
    async def _classify_task_type(self, task_description: str) -> str:
        """Classify task type for appropriate decomposition"""
        task_lower = task_description.lower()
        
        # Pattern matching for task types
        if any(word in task_lower for word in ["research", "investigate"]) and \
           any(word in task_lower for word in ["create", "develop", "design"]):
            return "research_and_create"
        
        elif any(word in task_lower for word in ["analyze", "evaluate"]) and \
             any(word in task_lower for word in ["recommend", "suggest", "propose"]):
            return "analyze_and_recommend"
        
        elif any(word in task_lower for word in ["comprehensive", "complete", "thorough"]):
            return "comprehensive_solution"
        
        elif any(word in task_lower for word in ["compare", "contrast", "evaluate"]):
            return "comparative_analysis"
        
        else:
            return "general"
    
    async def _select_coordination_strategy(self, 
                                          subtasks: List[Dict[str, Any]], 
                                          available_agents: Dict[str, Any]) -> CoordinationStrategy:
        """Select optimal coordination strategy"""
        
        # Analyze task dependencies
        has_dependencies = any(subtask.get("dependencies") for subtask in subtasks)
        
        # Analyze task types diversity
        task_types = set(subtask.get("type", "general") for subtask in subtasks)
        type_diversity = len(task_types)
        
        # Consider available agents
        agent_count = len(available_agents)
        
        # Strategy selection logic
        if has_dependencies:
            if type_diversity > 2 and agent_count >= 3:
                return CoordinationStrategy.HIERARCHICAL
            else:
                return CoordinationStrategy.SEQUENTIAL
        
        elif type_diversity > 2 and agent_count >= len(subtasks):
            return CoordinationStrategy.PARALLEL
        
        elif len(subtasks) <= 2:
            return CoordinationStrategy.COLLABORATIVE
        
        else:
            return CoordinationStrategy.SEQUENTIAL
    
    async def _assign_tasks_to_agents(self, 
                                    subtasks: List[Dict[str, Any]], 
                                    available_agents: Dict[str, Any],
                                    strategy: CoordinationStrategy) -> List[TaskAssignment]:
        """Assign subtasks to appropriate agents"""
        assignments = []
        
        # Score agents for each subtask
        for i, subtask in enumerate(subtasks):
            best_agent = await self._select_best_agent_for_task(subtask, available_agents)
            
            if best_agent:
                assignment = TaskAssignment(
                    agent_id=best_agent["id"],
                    subtask_description=subtask["description"],
                    priority=subtask.get("priority", 1),
                    estimated_duration=subtask.get("estimated_duration", 120.0),
                    required_capabilities=[subtask.get("type", "general")],
                    dependencies=subtask.get("dependencies", [])
                )
                assignments.append(assignment)
        
        return assignments
    
    async def _select_best_agent_for_task(self, 
                                        subtask: Dict[str, Any], 
                                        available_agents: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Select the best agent for a specific subtask"""
        task_type = subtask.get("type", "general")
        
        # Score each agent for this task
        agent_scores = []
        
        for agent_name, agent_info in available_agents.items():
            score = await self._score_agent_for_task(agent_info, subtask)
            agent_scores.append((agent_name, agent_info, score))
        
        # Sort by score and return best agent
        if agent_scores:
            agent_scores.sort(key=lambda x: x[2], reverse=True)
            best_agent_name, best_agent_info, best_score = agent_scores[0]
            
            if best_score > 0.3:  # Minimum acceptable score
                return {
                    "id": best_agent_info.get("agent_id", best_agent_name),
                    "name": best_agent_name,
                    "info": best_agent_info,
                    "score": best_score
                }
        
        return None
    
    async def _score_agent_for_task(self, 
                                  agent_info: Dict[str, Any], 
                                  subtask: Dict[str, Any]) -> float:
        """Score an agent's suitability for a specific subtask"""
        score = 0.0
        task_type = subtask.get("type", "general")
        
        # Check capability match
        agent_capabilities = agent_info.get("capabilities", [])
        if task_type in agent_capabilities:
            score += 0.4
        
        # Check agent type alignment
        agent_type = agent_info.get("agent_type", "")
        type_alignments = {
            "research": ["research", "analysis"],
            "creative": ["creative", "design"],
            "analysis": ["analysis", "research"],
            "synthesis": ["meta", "analysis"],
            "general": ["meta", "base"]
        }
        
        if agent_type in type_alignments.get(task_type, []):
            score += 0.3
        
        # Consider agent performance history
        agent_id = agent_info.get("agent_id", "")
        if agent_id in self.agent_performance:
            avg_performance = np.mean(list(self.agent_performance[agent_id].values()))
            score += avg_performance * 0.2
        
        # Consider agent availability (simplified)
        if agent_info.get("state", "active") == "active":
            score += 0.1
        
        return min(score, 1.0)
    
    def _get_agent_name_by_id(self, agent_id: str, available_agents: Dict[str, Any]) -> Optional[str]:
        """Get agent name by agent ID"""
        for name, info in available_agents.items():
            if info.get("agent_id") == agent_id:
                return name
        return None
    
    async def _execute_coordination_plan(self, plan: Dict[str, Any]) -> Dict[str, AgentResponse]:
        """Execute coordination plan and collect results"""
        results = {}
        
        # For now, simulate agent responses (would integrate with actual agents)
        for agent_name, subtask in plan.items():
            # Simulate agent processing
            response = AgentResponse(
                content=f"Completed subtask: {subtask}",
                confidence=0.8,
                reasoning=f"Processed by {agent_name}",
                metadata={"agent": agent_name, "subtask": subtask}
            )
            results[agent_name] = response
        
        return results
    
    async def synthesize_response(self, 
                                input_text: str,
                                agent_contributions: Dict[str, Any],
                                modality_results: Dict[str, Any],
                                context: Optional[Dict[str, Any]]) -> str:
        """Synthesize final response from multiple inputs"""
        
        # Collect all input sources
        synthesis_inputs = {
            "original_query": input_text,
            "agent_contributions": agent_contributions,
            "modality_results": modality_results,
            "context": context or {}
        }
        
        # Determine synthesis strategy
        strategy = await self._select_synthesis_strategy(synthesis_inputs)
        
        # Apply synthesis strategy
        if strategy == "hierarchical":
            return await self._hierarchical_synthesis(synthesis_inputs)
        elif strategy == "weighted_combination":
            return await self._weighted_combination_synthesis(synthesis_inputs)
        elif strategy == "narrative_integration":
            return await self._narrative_integration_synthesis(synthesis_inputs)
        else:
            return await self._default_synthesis(synthesis_inputs)
    
    async def _synthesize_multi_agent_response(self,
                                             task_description: str,
                                             execution_results: Dict[str, AgentResponse],
                                             context: Optional[Dict[str, Any]]) -> AgentResponse:
        """Synthesize response from multiple agent results"""
        
        if not execution_results:
            return AgentResponse(
                content="No agent responses to synthesize.",
                confidence=0.0,
                success=False
            )
        
        # Collect agent responses
        agent_responses = []
        total_confidence = 0.0
        successful_responses = 0
        
        for agent_name, response in execution_results.items():
            if response.success:
                agent_responses.append(f"**{agent_name}**: {response.content}")
                total_confidence += response.confidence
                successful_responses += 1
        
        if successful_responses == 0:
            return AgentResponse(
                content="All agent responses failed.",
                confidence=0.0,
                success=False
            )
        
        # Synthesize responses based on task type
        task_type = await self._classify_task_type(task_description)
        
        if task_type == "research_and_create":
            synthesized_content = await self._synthesize_research_and_create(agent_responses, task_description)
        elif task_type == "analyze_and_recommend":
            synthesized_content = await self._synthesize_analyze_and_recommend(agent_responses, task_description)
        else:
            synthesized_content = await self._synthesize_general(agent_responses, task_description)
        
        # Calculate overall confidence
        avg_confidence = total_confidence / successful_responses
        
        return AgentResponse(
            content=synthesized_content,
            confidence=avg_confidence,
            reasoning=f"Synthesized from {successful_responses} agent responses",
            metadata={
                "agents_involved": list(execution_results.keys()),
                "synthesis_type": task_type,
                "successful_responses": successful_responses
            },
            success=True
        )
    
    async def _synthesize_research_and_create(self, 
                                            agent_responses: List[str],
                                            task_description: str) -> str:
        """Synthesize research and creation responses"""
        synthesis = f"# Response to: {task_description}\n\n"
        
        # Organize responses by type
        research_content = []
        analysis_content = []
        creative_content = []
        
        for response in agent_responses:
            if "research" in response.lower():
                research_content.append(response)
            elif "analysis" in response.lower() or "analyze" in response.lower():
                analysis_content.append(response)
            else:
                creative_content.append(response)
        
        # Structure the synthesis
        if research_content:
            synthesis += "## Research Findings\n"
            synthesis += "\n".join(research_content) + "\n\n"
        
        if analysis_content:
            synthesis += "## Analysis\n"
            synthesis += "\n".join(analysis_content) + "\n\n"
        
        if creative_content:
            synthesis += "## Solution\n"
            synthesis += "\n".join(creative_content) + "\n\n"
        
        synthesis += "## Conclusion\n"
        synthesis += "Based on the collaborative effort above, this represents a comprehensive approach to your request."
        
        return synthesis
    
    async def _synthesize_analyze_and_recommend(self, 
                                              agent_responses: List[str],
                                              task_description: str) -> str:
        """Synthesize analysis and recommendation responses"""
        synthesis = f"# Analysis and Recommendations: {task_description}\n\n"
        
        synthesis += "## Analysis Results\n"
        for i, response in enumerate(agent_responses):
            synthesis += f"{i+1}. {response}\n"
        
        synthesis += "\n## Integrated Recommendations\n"
        synthesis += "Based on the analysis above, here are the key recommendations:\n"
        synthesis += "- Comprehensive approach incorporating multiple perspectives\n"
        synthesis += "- Evidence-based decision making\n"
        synthesis += "- Collaborative implementation strategy\n"
        
        return synthesis
    
    async def _synthesize_general(self, 
                                agent_responses: List[str],
                                task_description: str) -> str:
        """General purpose synthesis"""
        synthesis = f"# Response to: {task_description}\n\n"
        
        for i, response in enumerate(agent_responses):
            synthesis += f"## Perspective {i+1}\n{response}\n\n"
        
        synthesis += "## Summary\n"
        synthesis += "The above represents a multi-faceted approach to your request, "
        synthesis += "incorporating different perspectives and capabilities to provide a comprehensive response."
        
        return synthesis
    
    async def _select_synthesis_strategy(self, synthesis_inputs: Dict[str, Any]) -> str:
        """Select appropriate synthesis strategy"""
        agent_count = len(synthesis_inputs.get("agent_contributions", {}))
        modality_count = len(synthesis_inputs.get("modality_results", {}))
        
        if agent_count > 3 or modality_count > 2:
            return "hierarchical"
        elif agent_count > 1:
            return "weighted_combination"
        else:
            return "narrative_integration"
    
    async def _hierarchical_synthesis(self, synthesis_inputs: Dict[str, Any]) -> str:
        """Hierarchical synthesis strategy"""
        return "Hierarchical synthesis of multiple agent and modality inputs."
    
    async def _weighted_combination_synthesis(self, synthesis_inputs: Dict[str, Any]) -> str:
        """Weighted combination synthesis strategy"""
        return "Weighted combination of agent contributions."
    
    async def _narrative_integration_synthesis(self, synthesis_inputs: Dict[str, Any]) -> str:
        """Narrative integration synthesis strategy"""
        return "Narrative integration of available inputs."
    
    async def _default_synthesis(self, synthesis_inputs: Dict[str, Any]) -> str:
        """Default synthesis strategy"""
        query = synthesis_inputs.get("original_query", "")
        contributions = synthesis_inputs.get("agent_contributions", {})
        
        if not contributions:
            return "I need more information to provide a helpful response."
        
        # Simple concatenation of contributions
        response_parts = []
        for agent, contribution in contributions.items():
            if hasattr(contribution, 'content'):
                response_parts.append(contribution.content)
            else:
                response_parts.append(str(contribution))
        
        return "\n\n".join(response_parts)
    
    async def _handle_simple_task(self, 
                                task_description: str, 
                                context: Optional[Dict[str, Any]]) -> AgentResponse:
        """Handle simple task that doesn't require coordination"""
        # For simple tasks, provide direct meta-level response
        return AgentResponse(
            content=f"As the meta-agent, I'm processing: {task_description}. "
                   f"This appears to be a straightforward task that can be handled directly.",
            confidence=0.7,
            reasoning="Task classified as simple, handling directly",
            metadata={"coordination_required": False}
        )
    
    async def _learn_from_coordination(self, 
                                     plan: Dict[str, Any], 
                                     results: Dict[str, AgentResponse],
                                     final_response: AgentResponse) -> None:
        """Learn from coordination experience"""
        
        # Calculate coordination success metrics
        successful_agents = sum(1 for r in results.values() if r.success)
        total_agents = len(results)
        coordination_success = successful_agents / max(total_agents, 1)
        
        # Store coordination outcome
        coordination_data = {
            "plan": plan,
            "success_rate": coordination_success,
            "final_confidence": final_response.confidence,
            "agents_involved": list(results.keys()),
            "timestamp": datetime.now()
        }
        
        # Update strategy effectiveness
        # (This would be more sophisticated in practice)
        strategy = CoordinationStrategy.COLLABORATIVE  # Default for now
        if strategy not in self.strategy_effectiveness:
            self.strategy_effectiveness[strategy] = []
        
        self.strategy_effectiveness[strategy].append(coordination_success)
        
        # Store in memory for future learning
        await self._store_in_memory("episodic", {
            "type": "coordination_experience",
            "data": coordination_data,
            "timestamp": datetime.now()
        })
    
    # Helper methods for initialization
    
    async def _load_coordination_patterns(self) -> None:
        """Load coordination patterns from memory or defaults"""
        # Load from memory if available
        patterns = await self._retrieve_from_memory("semantic", {
            "type": "coordination_patterns"
        })
        
        if patterns:
            self.decomposition_patterns = patterns[0].get("patterns", {})
        else:
            # Default patterns
            self.decomposition_patterns = {
                "research_task": ["gather_info", "analyze_sources", "synthesize_findings"],
                "creative_task": ["brainstorm", "develop_concepts", "refine_ideas"],
                "analysis_task": ["collect_data", "process_data", "draw_conclusions"],
                "complex_task": ["decompose", "assign", "coordinate", "synthesize"]
            }
    
    async def _initialize_synthesis_strategies(self) -> None:
        """Initialize response synthesis strategies"""
        self.synthesis_strategies = {
            "sequential": self._sequential_synthesis,
            "parallel": self._parallel_synthesis,
            "hierarchical": self._hierarchical_synthesis_impl,
            "collaborative": self._collaborative_synthesis
        }
    
    async def _setup_performance_monitoring(self) -> None:
        """Setup performance monitoring for agents"""
        # Initialize performance tracking
        self.agent_performance = {}
        
        # Load historical performance data
        performance_data = await self._retrieve_from_memory("semantic", {
            "type": "agent_performance_history"
        })
        
        if performance_data:
            self.agent_performance = performance_data[0].get("performance", {})
    
    # Synthesis strategy implementations
    
    async def _sequential_synthesis(self, responses: List[str]) -> str:
        """Sequential synthesis of responses"""
        return "\n\n".join(f"Step {i+1}: {response}" for i, response in enumerate(responses))
    
    async def _parallel_synthesis(self, responses: List[str]) -> str:
        """Parallel synthesis of responses"""
        return "\n\n".join(f"Perspective {i+1}: {response}" for i, response in enumerate(responses))
    
    async def _hierarchical_synthesis_impl(self, responses: List[str]) -> str:
        """Hierarchical synthesis implementation"""
        if not responses:
            return "No responses to synthesize."
        
        # Organize responses by importance/quality
        # For now, simple concatenation with hierarchy
        result = "# Synthesized Response\n\n"
        result += "## Primary Analysis\n" + responses[0] + "\n\n"
        
        if len(responses) > 1:
            result += "## Supporting Perspectives\n"
            for i, response in enumerate(responses[1:], 1):
                result += f"### Perspective {i}\n{response}\n\n"
        
        return result
    
    async def _collaborative_synthesis(self, responses: List[str]) -> str:
        """Collaborative synthesis of responses"""
        return "Collaborative synthesis: " + " | ".join(responses)
    
    # Public API methods
    
    def register_agent(self, agent_name: str, agent_info: Dict[str, Any]) -> None:
        """Register an agent with the meta-agent"""
        self.available_agents[agent_name] = agent_info
        self.logger.info(f"Registered agent: {agent_name}")
    
    def unregister_agent(self, agent_name: str) -> None:
        """Unregister an agent"""
        if agent_name in self.available_agents:
            del self.available_agents[agent_name]
            self.logger.info(f"Unregistered agent: {agent_name}")
    
    def get_coordination_summary(self) -> Dict[str, Any]:
        """Get summary of coordination activities"""
        return {
            "available_agents": len(self.available_agents),
            "coordination_history": len(self.coordination_history),
            "active_plans": len(self.active_plans),
            "strategy_effectiveness": {
                strategy.value: np.mean(scores) if scores else 0.0
                for strategy, scores in self.strategy_effectiveness.items()
            }
        }
    
    async def optimize_coordination(self) -> Dict[str, Any]:
        """Optimize coordination strategies based on performance"""
        optimization_results = {}
        
        # Analyze strategy effectiveness
        best_strategy = None
        best_score = 0.0
        
        for strategy, scores in self.strategy_effectiveness.items():
            if scores:
                avg_score = np.mean(scores)
                if avg_score > best_score:
                    best_score = avg_score
                    best_strategy = strategy
        
        optimization_results["recommended_strategy"] = best_strategy.value if best_strategy else "collaborative"
        optimization_results["best_score"] = best_score
        
        # Analyze agent performance
        agent_rankings = []
        for agent_id, performance in self.agent_performance.items():
            avg_performance = np.mean(list(performance.values())) if performance else 0.0
            agent_rankings.append((agent_id, avg_performance))
        
        agent_rankings.sort(key=lambda x: x[1], reverse=True)
        optimization_results["top_performing_agents"] = agent_rankings[:3]
        
        return optimization_results
