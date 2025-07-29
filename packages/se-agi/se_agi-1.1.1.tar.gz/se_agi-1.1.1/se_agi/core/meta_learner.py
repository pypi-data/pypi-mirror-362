"""
Meta-Learning Engine for SE-AGI
Implements learning how to learn capabilities
"""

import asyncio
import logging
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass
from datetime import datetime
import json
import pickle
from abc import ABC, abstractmethod

from ..core.config import MetaLearningConfig


@dataclass
class TaskData:
    """Represents a learning task"""
    task_id: str
    description: str
    input_data: Any
    target_output: Any
    task_type: str
    domain: str
    difficulty: float = 0.5
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class LearningEpisode:
    """Represents a learning episode"""
    episode_id: str
    task: TaskData
    adaptation_steps: List[Dict[str, Any]]
    performance_metrics: Dict[str, float]
    learned_parameters: Dict[str, Any]
    timestamp: datetime
    success: bool


class MetaLearningAlgorithm(ABC):
    """Abstract base class for meta-learning algorithms"""
    
    @abstractmethod
    async def meta_train(self, tasks: List[TaskData]) -> Dict[str, Any]:
        """Perform meta-training on a batch of tasks"""
        pass
    
    @abstractmethod
    async def adapt(self, task: TaskData, steps: int = 5) -> Dict[str, Any]:
        """Adapt to a new task"""
        pass
    
    @abstractmethod
    def get_parameters(self) -> Dict[str, Any]:
        """Get current model parameters"""
        pass
    
    @abstractmethod
    def set_parameters(self, parameters: Dict[str, Any]) -> None:
        """Set model parameters"""
        pass


class MAML(MetaLearningAlgorithm):
    """Model-Agnostic Meta-Learning implementation"""
    
    def __init__(self, 
                 model_architecture: nn.Module,
                 inner_lr: float = 1e-3,
                 outer_lr: float = 1e-4,
                 adaptation_steps: int = 5):
        self.model = model_architecture
        self.inner_lr = inner_lr
        self.outer_lr = outer_lr
        self.adaptation_steps = adaptation_steps
        self.meta_optimizer = optim.Adam(self.model.parameters(), lr=outer_lr)
        self.logger = logging.getLogger(__name__)
    
    async def meta_train(self, tasks: List[TaskData]) -> Dict[str, Any]:
        """MAML meta-training step"""
        self.meta_optimizer.zero_grad()
        
        total_loss = 0.0
        meta_gradients = []
        
        for task in tasks:
            # Inner loop adaptation
            adapted_params = await self._inner_loop_adaptation(task)
            
            # Compute meta-gradient
            meta_loss = await self._compute_meta_loss(task, adapted_params)
            meta_grad = torch.autograd.grad(
                meta_loss, 
                self.model.parameters(),
                create_graph=True
            )
            meta_gradients.append(meta_grad)
            total_loss += meta_loss.item()
        
        # Aggregate meta-gradients
        aggregated_gradients = self._aggregate_gradients(meta_gradients)
        
        # Update meta-parameters
        for param, grad in zip(self.model.parameters(), aggregated_gradients):
            param.grad = grad
        
        self.meta_optimizer.step()
        
        return {
            "meta_loss": total_loss / len(tasks),
            "tasks_processed": len(tasks),
            "adaptation_successful": True
        }
    
    async def adapt(self, task: TaskData, steps: int = None) -> Dict[str, Any]:
        """Adapt to new task using inner loop optimization"""
        steps = steps or self.adaptation_steps
        
        # Create temporary model copy for adaptation
        adapted_model = self._create_model_copy()
        optimizer = optim.SGD(adapted_model.parameters(), lr=self.inner_lr)
        
        adaptation_history = []
        
        for step in range(steps):
            optimizer.zero_grad()
            
            # Compute task-specific loss
            loss = await self._compute_task_loss(task, adapted_model)
            loss.backward()
            optimizer.step()
            
            adaptation_history.append({
                "step": step,
                "loss": loss.item(),
                "timestamp": datetime.now()
            })
        
        # Extract adapted parameters
        adapted_params = {
            name: param.clone().detach() 
            for name, param in adapted_model.named_parameters()
        }
        
        return {
            "adapted_parameters": adapted_params,
            "adaptation_history": adaptation_history,
            "final_loss": adaptation_history[-1]["loss"] if adaptation_history else float('inf'),
            "steps_taken": steps
        }
    
    async def _inner_loop_adaptation(self, task: TaskData) -> Dict[str, torch.Tensor]:
        """Perform inner loop adaptation for MAML"""
        # Clone model parameters for inner loop
        fast_weights = {
            name: param.clone() 
            for name, param in self.model.named_parameters()
        }
        
        for _ in range(self.adaptation_steps):
            # Compute loss with fast weights
            loss = await self._compute_task_loss_with_weights(task, fast_weights)
            
            # Compute gradients
            gradients = torch.autograd.grad(
                loss, 
                fast_weights.values(),
                create_graph=True
            )
            
            # Update fast weights
            for (name, param), grad in zip(fast_weights.items(), gradients):
                fast_weights[name] = param - self.inner_lr * grad
        
        return fast_weights
    
    async def _compute_meta_loss(self, 
                                task: TaskData, 
                                adapted_params: Dict[str, torch.Tensor]) -> torch.Tensor:
        """Compute meta-loss for outer loop optimization"""
        return await self._compute_task_loss_with_weights(task, adapted_params)
    
    async def _compute_task_loss(self, 
                                task: TaskData, 
                                model: nn.Module) -> torch.Tensor:
        """Compute loss for a specific task"""
        # Convert task data to tensors
        inputs = self._prepare_inputs(task.input_data)
        targets = self._prepare_targets(task.target_output)
        
        # Forward pass
        outputs = model(inputs)
        
        # Compute loss based on task type
        if task.task_type == "classification":
            loss_fn = nn.CrossEntropyLoss()
        elif task.task_type == "regression":
            loss_fn = nn.MSELoss()
        else:
            loss_fn = nn.MSELoss()  # Default
        
        return loss_fn(outputs, targets)
    
    async def _compute_task_loss_with_weights(self, 
                                            task: TaskData,
                                            weights: Dict[str, torch.Tensor]) -> torch.Tensor:
        """Compute task loss using specific weights"""
        # Temporarily set model weights
        original_weights = {}
        for name, param in self.model.named_parameters():
            original_weights[name] = param.clone()
            param.data = weights[name]
        
        try:
            loss = await self._compute_task_loss(task, self.model)
        finally:
            # Restore original weights
            for name, param in self.model.named_parameters():
                param.data = original_weights[name]
        
        return loss
    
    def _create_model_copy(self) -> nn.Module:
        """Create a copy of the model for adaptation"""
        model_copy = type(self.model)()
        model_copy.load_state_dict(self.model.state_dict())
        return model_copy
    
    def _aggregate_gradients(self, gradients_list: List) -> List[torch.Tensor]:
        """Aggregate gradients from multiple tasks"""
        if not gradients_list:
            return []
        
        aggregated = []
        for grad_idx in range(len(gradients_list[0])):
            grad_sum = sum(grads[grad_idx] for grads in gradients_list)
            aggregated.append(grad_sum / len(gradients_list))
        
        return aggregated
    
    def _prepare_inputs(self, input_data: Any) -> torch.Tensor:
        """Prepare input data as tensor"""
        if isinstance(input_data, torch.Tensor):
            return input_data
        elif isinstance(input_data, np.ndarray):
            return torch.from_numpy(input_data).float()
        elif isinstance(input_data, (list, tuple)):
            return torch.tensor(input_data, dtype=torch.float32)
        else:
            # For text or other data, would need appropriate encoding
            return torch.randn(1, 128)  # Placeholder
    
    def _prepare_targets(self, target_data: Any) -> torch.Tensor:
        """Prepare target data as tensor"""
        return self._prepare_inputs(target_data)
    
    def get_parameters(self) -> Dict[str, Any]:
        """Get current model parameters"""
        return {
            "model_state": self.model.state_dict(),
            "optimizer_state": self.meta_optimizer.state_dict(),
            "inner_lr": self.inner_lr,
            "outer_lr": self.outer_lr
        }
    
    def set_parameters(self, parameters: Dict[str, Any]) -> None:
        """Set model parameters"""
        if "model_state" in parameters:
            self.model.load_state_dict(parameters["model_state"])
        if "optimizer_state" in parameters:
            self.meta_optimizer.load_state_dict(parameters["optimizer_state"])


class TransformerXLMetaLearner(MetaLearningAlgorithm):
    """Transformer-XL based meta-learning for sequence tasks"""
    
    def __init__(self, 
                 vocab_size: int = 10000,
                 d_model: int = 512,
                 n_layers: int = 6,
                 n_heads: int = 8,
                 memory_length: int = 512):
        
        self.vocab_size = vocab_size
        self.d_model = d_model
        self.memory_length = memory_length
        
        # Build Transformer-XL model
        self.model = self._build_transformer_xl(vocab_size, d_model, n_layers, n_heads)
        self.optimizer = optim.AdamW(self.model.parameters(), lr=1e-4)
        self.memory = None
        self.logger = logging.getLogger(__name__)
    
    def _build_transformer_xl(self, vocab_size, d_model, n_layers, n_heads):
        """Build Transformer-XL architecture"""
        # Simplified Transformer-XL implementation
        class TransformerXL(nn.Module):
            def __init__(self):
                super().__init__()
                self.embedding = nn.Embedding(vocab_size, d_model)
                self.layers = nn.ModuleList([
                    nn.TransformerEncoderLayer(d_model, n_heads, batch_first=True)
                    for _ in range(n_layers)
                ])
                self.output_projection = nn.Linear(d_model, vocab_size)
                
            def forward(self, x, memory=None):
                x = self.embedding(x)
                
                for layer in self.layers:
                    if memory is not None:
                        # Concatenate with memory for extended context
                        extended_x = torch.cat([memory, x], dim=1)
                        x = layer(extended_x)[:, -x.size(1):]  # Take only new part
                    else:
                        x = layer(x)
                
                return self.output_projection(x), x  # Return output and hidden state
        
        return TransformerXL()
    
    async def meta_train(self, tasks: List[TaskData]) -> Dict[str, Any]:
        """Meta-train on sequence tasks"""
        total_loss = 0.0
        successful_tasks = 0
        
        for task in tasks:
            try:
                # Prepare sequence data
                sequences = self._prepare_sequence_data(task)
                
                for sequence in sequences:
                    self.optimizer.zero_grad()
                    
                    # Forward pass
                    outputs, hidden = self.model(sequence['input'], self.memory)
                    
                    # Compute loss
                    loss = nn.CrossEntropyLoss()(
                        outputs.view(-1, self.vocab_size),
                        sequence['target'].view(-1)
                    )
                    
                    # Backward pass
                    loss.backward()
                    torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
                    self.optimizer.step()
                    
                    total_loss += loss.item()
                
                # Update memory for next task
                if hidden.size(1) > self.memory_length:
                    self.memory = hidden[:, -self.memory_length:].detach()
                else:
                    self.memory = hidden.detach()
                
                successful_tasks += 1
                
            except Exception as e:
                self.logger.error(f"Error in meta-training task {task.task_id}: {e}")
        
        return {
            "meta_loss": total_loss / max(successful_tasks, 1),
            "tasks_processed": successful_tasks,
            "memory_updated": self.memory is not None
        }
    
    async def adapt(self, task: TaskData, steps: int = 5) -> Dict[str, Any]:
        """Adapt to new task using in-context learning"""
        # For Transformer-XL, adaptation is through in-context examples
        adaptation_history = []
        
        # Prepare adaptation examples
        examples = self._prepare_adaptation_examples(task)
        
        for step in range(steps):
            # Create context with examples
            context = self._create_adaptation_context(examples, step)
            
            # Forward pass for adaptation
            outputs, hidden = self.model(context, self.memory)
            
            # Evaluate adaptation quality
            adaptation_score = await self._evaluate_adaptation(task, outputs)
            
            adaptation_history.append({
                "step": step,
                "adaptation_score": adaptation_score,
                "context_length": context.size(1),
                "timestamp": datetime.now()
            })
            
            # Update memory with adaptation context
            if hidden.size(1) > self.memory_length:
                self.memory = hidden[:, -self.memory_length:].detach()
            else:
                self.memory = hidden.detach()
        
        return {
            "adaptation_history": adaptation_history,
            "final_score": adaptation_history[-1]["adaptation_score"],
            "context_examples": len(examples),
            "memory_state": self.memory.clone() if self.memory is not None else None
        }
    
    def _prepare_sequence_data(self, task: TaskData) -> List[Dict[str, torch.Tensor]]:
        """Prepare task data as sequences"""
        # This is a simplified version - would need task-specific preparation
        sequences = []
        
        if isinstance(task.input_data, str):
            # Text sequence
            tokens = self._tokenize_text(task.input_data)
            target_tokens = self._tokenize_text(task.target_output)
            
            sequences.append({
                "input": torch.tensor(tokens[:-1]).unsqueeze(0),
                "target": torch.tensor(target_tokens).unsqueeze(0)
            })
        
        return sequences
    
    def _tokenize_text(self, text: str) -> List[int]:
        """Simple tokenization - would use proper tokenizer in practice"""
        # Simplified: convert characters to ASCII values
        return [min(ord(c), self.vocab_size - 1) for c in text[:512]]
    
    def _prepare_adaptation_examples(self, task: TaskData) -> List[Dict[str, Any]]:
        """Prepare examples for adaptation"""
        # Create few-shot examples for in-context learning
        examples = []
        
        # Add task description as context
        examples.append({
            "input": task.description,
            "output": "Understanding task...",
            "type": "description"
        })
        
        # Add input-output examples if available
        if hasattr(task, "examples"):
            examples.extend(task.examples)
        
        return examples
    
    def _create_adaptation_context(self, examples: List[Dict[str, Any]], step: int) -> torch.Tensor:
        """Create context tensor for adaptation"""
        context_text = ""
        
        # Include examples up to current step
        for i, example in enumerate(examples[:step + 1]):
            context_text += f"Input: {example['input']}\nOutput: {example['output']}\n\n"
        
        # Tokenize context
        context_tokens = self._tokenize_text(context_text)
        return torch.tensor(context_tokens).unsqueeze(0)
    
    async def _evaluate_adaptation(self, task: TaskData, outputs: torch.Tensor) -> float:
        """Evaluate quality of adaptation"""
        # Simple evaluation based on output coherence
        # In practice, would use task-specific metrics
        
        # Check output diversity (not all same token)
        output_probs = torch.softmax(outputs, dim=-1)
        entropy = -(output_probs * torch.log(output_probs + 1e-10)).sum(dim=-1).mean()
        
        # Normalize entropy score
        max_entropy = np.log(self.vocab_size)
        adaptation_score = entropy.item() / max_entropy
        
        return min(max(adaptation_score, 0.0), 1.0)
    
    def get_parameters(self) -> Dict[str, Any]:
        """Get model parameters"""
        return {
            "model_state": self.model.state_dict(),
            "optimizer_state": self.optimizer.state_dict(),
            "memory_state": self.memory.clone() if self.memory is not None else None,
            "vocab_size": self.vocab_size,
            "d_model": self.d_model
        }
    
    def set_parameters(self, parameters: Dict[str, Any]) -> None:
        """Set model parameters"""
        if "model_state" in parameters:
            self.model.load_state_dict(parameters["model_state"])
        if "optimizer_state" in parameters:
            self.optimizer.load_state_dict(parameters["optimizer_state"])
        if "memory_state" in parameters and parameters["memory_state"] is not None:
            self.memory = parameters["memory_state"]


class MetaLearner:
    """
    Main meta-learning engine for SE-AGI
    Coordinates different meta-learning algorithms and strategies
    """
    
    def __init__(self, 
                 config: MetaLearningConfig,
                 memory_system: Optional[Any] = None):
        self.config = config
        self.memory_system = memory_system
        self.logger = logging.getLogger(__name__)
        
        # Initialize meta-learning algorithm
        self.algorithm = self._create_algorithm()
        
        # Learning history
        self.learning_episodes: List[LearningEpisode] = []
        self.task_performance: Dict[str, List[float]] = {}
        
        # Meta-learning state
        self.meta_knowledge = {}
        self.adaptation_strategies = {}
        
    def _create_algorithm(self) -> MetaLearningAlgorithm:
        """Create meta-learning algorithm based on configuration"""
        if self.config.algorithm == "maml":
            # Create simple neural network for MAML
            model = nn.Sequential(
                nn.Linear(128, 256),
                nn.ReLU(),
                nn.Linear(256, 128),
                nn.ReLU(),
                nn.Linear(128, 64)
            )
            return MAML(
                model_architecture=model,
                inner_lr=self.config.inner_learning_rate,
                outer_lr=self.config.outer_learning_rate,
                adaptation_steps=self.config.adaptation_steps
            )
        
        elif self.config.algorithm == "transformer_xl":
            return TransformerXLMetaLearner()
        
        else:
            raise ValueError(f"Unknown meta-learning algorithm: {self.config.algorithm}")
    
    async def initialize(self) -> None:
        """Initialize meta-learning system"""
        self.logger.info("Initializing meta-learning engine...")
        
        # Load any saved meta-knowledge
        await self._load_meta_knowledge()
        
        # Initialize algorithm-specific components
        if hasattr(self.algorithm, 'initialize'):
            await self.algorithm.initialize()
        
        self.logger.info("Meta-learning engine initialized")
    
    async def learn_from_tasks(self, tasks: List[TaskData]) -> Dict[str, Any]:
        """Learn from a batch of tasks"""
        self.logger.info(f"Meta-learning from {len(tasks)} tasks...")
        
        # Meta-train on tasks
        meta_result = await self.algorithm.meta_train(tasks)
        
        # Store learning episodes
        for task in tasks:
            episode = LearningEpisode(
                episode_id=f"ep_{len(self.learning_episodes)}",
                task=task,
                adaptation_steps=[],
                performance_metrics=meta_result,
                learned_parameters=self.algorithm.get_parameters(),
                timestamp=datetime.now(),
                success=meta_result.get("adaptation_successful", False)
            )
            self.learning_episodes.append(episode)
        
        # Update meta-knowledge
        await self._update_meta_knowledge(tasks, meta_result)
        
        return meta_result
    
    async def adapt_to_task(self, task: TaskData) -> Dict[str, Any]:
        """Adapt to a new task"""
        self.logger.info(f"Adapting to task: {task.task_id}")
        
        # Use meta-learned knowledge to adapt
        adaptation_result = await self.algorithm.adapt(task, self.config.adaptation_steps)
        
        # Store adaptation performance
        if task.task_id not in self.task_performance:
            self.task_performance[task.task_id] = []
        
        self.task_performance[task.task_id].append(
            adaptation_result.get("final_score", 0.0)
        )
        
        # Learn adaptation strategy
        await self._learn_adaptation_strategy(task, adaptation_result)
        
        return adaptation_result
    
    async def update_from_interaction(self,
                                    input_text: str,
                                    output_text: str,
                                    agent_contributions: Dict[str, Any]) -> None:
        """Update meta-learning from system interaction"""
        # Create task from interaction
        task = TaskData(
            task_id=f"interaction_{datetime.now().timestamp()}",
            description=input_text,
            input_data=input_text,
            target_output=output_text,
            task_type="interaction",
            domain="general"
        )
        
        # Extract learning signal from agent contributions
        performance_score = self._calculate_interaction_performance(
            input_text, output_text, agent_contributions
        )
        
        # Update meta-knowledge
        await self._update_from_performance(task, performance_score)
    
    def _calculate_interaction_performance(self,
                                        input_text: str,
                                        output_text: str,
                                        agent_contributions: Dict[str, Any]) -> float:
        """Calculate performance score from interaction"""
        # Simple heuristic - would use more sophisticated metrics
        score = 0.5  # Base score
        
        # Factor in agent confidence
        confidences = []
        for contribution in agent_contributions.values():
            if hasattr(contribution, 'confidence'):
                confidences.append(contribution.confidence)
        
        if confidences:
            score += (sum(confidences) / len(confidences)) * 0.3
        
        # Factor in response length/quality
        if len(output_text) > 10:
            score += 0.2
        
        return min(score, 1.0)
    
    async def _update_meta_knowledge(self, 
                                   tasks: List[TaskData], 
                                   result: Dict[str, Any]) -> None:
        """Update meta-knowledge from learning results"""
        # Extract patterns from successful tasks
        successful_tasks = [t for t in tasks if result.get("adaptation_successful", False)]
        
        for task in successful_tasks:
            domain = task.domain
            task_type = task.task_type
            
            # Update domain-specific knowledge
            if domain not in self.meta_knowledge:
                self.meta_knowledge[domain] = {
                    "successful_patterns": [],
                    "common_features": {},
                    "adaptation_strategies": {}
                }
            
            # Store successful patterns
            self.meta_knowledge[domain]["successful_patterns"].append({
                "task_type": task_type,
                "difficulty": task.difficulty,
                "performance": result.get("meta_loss", float('inf')),
                "timestamp": datetime.now()
            })
        
        # Store in persistent memory if available
        if self.memory_system:
            await self.memory_system.store_episode({
                "type": "meta_learning",
                "tasks_count": len(tasks),
                "performance": result,
                "meta_knowledge_update": True,
                "timestamp": datetime.now()
            })
    
    async def _learn_adaptation_strategy(self, 
                                       task: TaskData, 
                                       adaptation_result: Dict[str, Any]) -> None:
        """Learn effective adaptation strategies"""
        strategy_key = f"{task.domain}_{task.task_type}"
        
        if strategy_key not in self.adaptation_strategies:
            self.adaptation_strategies[strategy_key] = {
                "successful_approaches": [],
                "optimal_steps": [],
                "learning_rates": []
            }
        
        # Record successful adaptation approach
        if adaptation_result.get("final_score", 0) > 0.7:
            self.adaptation_strategies[strategy_key]["successful_approaches"].append({
                "steps": adaptation_result.get("steps_taken", 0),
                "score": adaptation_result.get("final_score", 0),
                "approach": adaptation_result.get("approach", "standard")
            })
    
    async def _update_from_performance(self, 
                                     task: TaskData, 
                                     performance: float) -> None:
        """Update meta-learning from performance feedback"""
        # Use performance signal to adjust meta-parameters
        if performance > 0.8:
            # Good performance - reinforce current strategy
            await self._reinforce_strategy(task)
        elif performance < 0.3:
            # Poor performance - explore new strategies
            await self._explore_new_strategy(task)
    
    async def _reinforce_strategy(self, task: TaskData) -> None:
        """Reinforce successful strategies"""
        # Strengthen connections to successful patterns
        domain = task.domain
        if domain in self.meta_knowledge:
            for pattern in self.meta_knowledge[domain]["successful_patterns"]:
                if pattern["task_type"] == task.task_type:
                    pattern["reinforcement"] = pattern.get("reinforcement", 0) + 1
    
    async def _explore_new_strategy(self, task: TaskData) -> None:
        """Explore new adaptation strategies"""
        # Add exploration patterns for failed cases
        domain = task.domain
        if domain not in self.meta_knowledge:
            self.meta_knowledge[domain] = {
                "exploration_needed": [],
                "failed_patterns": [],
                "alternative_approaches": []
            }
        
        self.meta_knowledge[domain]["exploration_needed"].append({
            "task_type": task.task_type,
            "timestamp": datetime.now(),
            "reason": "poor_performance"
        })
    
    async def _load_meta_knowledge(self) -> None:
        """Load saved meta-knowledge"""
        try:
            # Load from file or database
            # Implementation depends on storage backend
            pass
        except Exception as e:
            self.logger.warning(f"Could not load meta-knowledge: {e}")
    
    async def _save_meta_knowledge(self) -> None:
        """Save meta-knowledge"""
        try:
            # Save to file or database
            # Implementation depends on storage backend
            pass
        except Exception as e:
            self.logger.error(f"Could not save meta-knowledge: {e}")
    
    def get_learning_statistics(self) -> Dict[str, Any]:
        """Get meta-learning statistics"""
        return {
            "total_episodes": len(self.learning_episodes),
            "successful_episodes": sum(1 for ep in self.learning_episodes if ep.success),
            "domains_learned": list(self.meta_knowledge.keys()),
            "adaptation_strategies": len(self.adaptation_strategies),
            "average_performance": self._calculate_average_performance(),
            "learning_trends": self._analyze_learning_trends()
        }
    
    def _calculate_average_performance(self) -> float:
        """Calculate average performance across all tasks"""
        all_scores = []
        for scores in self.task_performance.values():
            all_scores.extend(scores)
        return sum(all_scores) / len(all_scores) if all_scores else 0.0
    
    def _analyze_learning_trends(self) -> Dict[str, Any]:
        """Analyze learning trends over time"""
        if len(self.learning_episodes) < 2:
            return {"trend": "insufficient_data"}
        
        # Simple trend analysis
        recent_performance = []
        older_performance = []
        
        mid_point = len(self.learning_episodes) // 2
        
        for i, episode in enumerate(self.learning_episodes):
            perf = episode.performance_metrics.get("meta_loss", float('inf'))
            if i < mid_point:
                older_performance.append(perf)
            else:
                recent_performance.append(perf)
        
        if recent_performance and older_performance:
            recent_avg = sum(recent_performance) / len(recent_performance)
            older_avg = sum(older_performance) / len(older_performance)
            
            if recent_avg < older_avg:  # Lower loss is better
                return {"trend": "improving", "improvement": older_avg - recent_avg}
            else:
                return {"trend": "declining", "decline": recent_avg - older_avg}
        
        return {"trend": "stable"}
    
    async def shutdown(self) -> None:
        """Shutdown meta-learning system"""
        self.logger.info("Shutting down meta-learning engine...")
        
        # Save current meta-knowledge
        await self._save_meta_knowledge()
        
        self.logger.info("Meta-learning engine shutdown complete")
