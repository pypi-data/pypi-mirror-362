"""
Configuration system for SE-AGI
Manages all system settings and hyperparameters
"""

from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field, validator
from enum import Enum
import yaml
import os


class SafetyLevel(str, Enum):
    """Safety levels for the AGI system"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    MAXIMUM = "maximum"


class LearningAlgorithm(str, Enum):
    """Available meta-learning algorithms"""
    MAML = "maml"
    REPTILE = "reptile"
    TRANSFORMER_XL = "transformer_xl"
    NEURAL_ODE = "neural_ode"
    HYPERNETWORK = "hypernetwork"


class MemoryType(str, Enum):
    """Memory system types"""
    WORKING = "working"
    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    PROCEDURAL = "procedural"


class AgentConfig(BaseModel):
    """Configuration for individual agents"""
    
    name: str = Field(default="base_agent", description="Agent name")
    agent_type: str = Field(default="base", description="Type of agent")
    capabilities: List[str] = Field(default_factory=list, description="Agent capabilities")
    max_memory_size: int = Field(default=10000, description="Maximum memory entries")
    learning_rate: float = Field(default=1e-4, description="Learning rate")
    temperature: float = Field(default=0.7, description="Generation temperature")
    max_tokens: int = Field(default=2048, description="Maximum token length")
    
    # Specialization parameters
    domain_expertise: Optional[str] = Field(default=None, description="Domain of expertise")
    reasoning_depth: int = Field(default=3, description="Reasoning depth")
    creativity_level: float = Field(default=0.5, description="Creativity level (0-1)")
    
    @validator('creativity_level')
    def validate_creativity(cls, v):
        if not 0 <= v <= 1:
            raise ValueError('Creativity level must be between 0 and 1')
        return v


class MetaLearningConfig(BaseModel):
    """Configuration for meta-learning system"""
    
    enabled: bool = Field(default=True, description="Enable meta-learning")
    algorithm: LearningAlgorithm = Field(default=LearningAlgorithm.TRANSFORMER_XL)
    adaptation_steps: int = Field(default=5, description="Steps for task adaptation")
    meta_batch_size: int = Field(default=32, description="Meta-batch size")
    inner_learning_rate: float = Field(default=1e-3, description="Inner loop learning rate")
    outer_learning_rate: float = Field(default=1e-4, description="Outer loop learning rate")
    
    # Advanced settings
    gradient_clipping: float = Field(default=1.0, description="Gradient clipping threshold")
    use_second_order: bool = Field(default=True, description="Use second-order gradients")
    task_distribution_sampling: str = Field(default="uniform", description="Task sampling strategy")


class ReflectionConfig(BaseModel):
    """Configuration for self-reflection system"""
    
    enabled: bool = Field(default=True, description="Enable self-reflection")
    frequency: str = Field(default="continuous", description="Reflection frequency")
    depth_levels: int = Field(default=3, description="Levels of reflection depth")
    
    # Reflection types
    performance_reflection: bool = Field(default=True, description="Reflect on performance")
    strategy_reflection: bool = Field(default=True, description="Reflect on strategies")
    goal_reflection: bool = Field(default=True, description="Reflect on goals")
    ethical_reflection: bool = Field(default=True, description="Reflect on ethics")
    
    # Thresholds
    improvement_threshold: float = Field(default=0.05, description="Threshold for triggering improvement")
    confidence_threshold: float = Field(default=0.8, description="Confidence threshold for actions")


class MemoryConfig(BaseModel):
    """Configuration for memory systems"""
    
    # Memory capacities
    working_memory_size: int = Field(default=1000, description="Working memory capacity")
    episodic_memory_size: int = Field(default=100000, description="Episodic memory capacity")
    semantic_memory_size: int = Field(default=1000000, description="Semantic memory capacity")
    
    # Consolidation settings
    consolidation_enabled: bool = Field(default=True, description="Enable memory consolidation")
    consolidation_interval: int = Field(default=3600, description="Consolidation interval (seconds)")
    forgetting_rate: float = Field(default=0.01, description="Memory forgetting rate")
    
    # Retrieval settings
    retrieval_algorithm: str = Field(default="semantic_similarity", description="Memory retrieval method")
    similarity_threshold: float = Field(default=0.7, description="Similarity threshold for retrieval")


class EvolutionConfig(BaseModel):
    """Configuration for capability evolution"""
    
    enabled: bool = Field(default=True, description="Enable capability evolution")
    evolution_rate: float = Field(default=0.1, description="Rate of evolution")
    mutation_rate: float = Field(default=0.05, description="Mutation rate for evolution")
    
    # Evolution strategies
    architecture_search: bool = Field(default=True, description="Enable architecture search")
    prompt_evolution: bool = Field(default=True, description="Enable prompt evolution")
    tool_discovery: bool = Field(default=True, description="Enable tool discovery")
    knowledge_distillation: bool = Field(default=True, description="Enable knowledge distillation")
    
    # Selection criteria
    fitness_function: str = Field(default="multi_objective", description="Fitness evaluation function")
    population_size: int = Field(default=50, description="Evolution population size")
    elite_ratio: float = Field(default=0.1, description="Ratio of elite individuals to preserve")


class SafetyConfig(BaseModel):
    """Configuration for safety and alignment"""
    
    safety_level: SafetyLevel = Field(default=SafetyLevel.HIGH)
    alignment_checking: bool = Field(default=True, description="Enable alignment checking")
    human_oversight: bool = Field(default=True, description="Require human oversight")
    
    # Monitoring settings
    capability_monitoring: bool = Field(default=True, description="Monitor capability changes")
    behavior_logging: bool = Field(default=True, description="Log all behaviors")
    intervention_threshold: float = Field(default=0.9, description="Threshold for safety intervention")
    
    # Constitutional AI settings
    constitutional_rules: List[str] = Field(
        default_factory=lambda: [
            "Always prioritize human welfare and safety",
            "Be honest and transparent in all communications",
            "Respect human autonomy and decision-making",
            "Avoid causing harm or enabling harmful activities",
            "Preserve human values and ethical principles"
        ],
        description="Constitutional rules for behavior"
    )


class SEAGIConfig(BaseModel):
    """Main configuration class for SE-AGI system"""
    
    # System identification
    system_name: str = Field(default="SE-AGI", description="System name")
    version: str = Field(default="0.1.0", description="System version")
    instance_id: str = Field(default="default", description="Instance identifier")
    
    # Core configurations
    meta_learning: MetaLearningConfig = Field(default_factory=MetaLearningConfig)
    reflection: ReflectionConfig = Field(default_factory=ReflectionConfig)
    memory: MemoryConfig = Field(default_factory=MemoryConfig)
    evolution: EvolutionConfig = Field(default_factory=EvolutionConfig)
    safety: SafetyConfig = Field(default_factory=SafetyConfig)
    
    # Agent configurations
    agents: Dict[str, AgentConfig] = Field(default_factory=dict, description="Agent configurations")
    
    # Runtime settings
    max_concurrent_agents: int = Field(default=10, description="Maximum concurrent agents")
    communication_protocol: str = Field(default="async_message_passing", description="Agent communication protocol")
    coordination_strategy: str = Field(default="hierarchical", description="Agent coordination strategy")
    
    # Resource limits
    max_memory_usage: int = Field(default=8192, description="Maximum memory usage (MB)")
    max_compute_time: int = Field(default=3600, description="Maximum compute time per task (seconds)")
    max_api_calls: int = Field(default=10000, description="Maximum API calls per hour")
    
    # Persistence settings
    save_checkpoints: bool = Field(default=True, description="Save system checkpoints")
    checkpoint_interval: int = Field(default=1800, description="Checkpoint interval (seconds)")
    backup_enabled: bool = Field(default=True, description="Enable system backups")
    
    @classmethod
    def from_yaml(cls, file_path: str) -> "SEAGIConfig":
        """Load configuration from YAML file"""
        with open(file_path, 'r') as f:
            config_data = yaml.safe_load(f)
        return cls(**config_data)
    
    def to_yaml(self, file_path: str) -> None:
        """Save configuration to YAML file"""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            yaml.safe_dump(self.dict(), f, default_flow_style=False, indent=2)
    
    def add_agent(self, agent_config: AgentConfig) -> None:
        """Add an agent configuration"""
        self.agents[agent_config.name] = agent_config
    
    def get_agent_config(self, agent_name: str) -> Optional[AgentConfig]:
        """Get configuration for a specific agent"""
        return self.agents.get(agent_name)
    
    def update_safety_level(self, level: SafetyLevel) -> None:
        """Update system safety level"""
        self.safety.safety_level = level
        
        # Adjust other settings based on safety level
        if level == SafetyLevel.MAXIMUM:
            self.safety.human_oversight = True
            self.safety.intervention_threshold = 0.5
            self.evolution.enabled = False
        elif level == SafetyLevel.HIGH:
            self.safety.human_oversight = True
            self.safety.intervention_threshold = 0.7
        elif level == SafetyLevel.MEDIUM:
            self.safety.intervention_threshold = 0.8
        else:  # LOW
            self.safety.intervention_threshold = 0.9


# Default configurations for different use cases
class ConfigPresets:
    """Predefined configuration presets"""
    
    @staticmethod
    def research_focused() -> SEAGIConfig:
        """Configuration optimized for research tasks"""
        config = SEAGIConfig()
        config.meta_learning.algorithm = LearningAlgorithm.MAML
        config.reflection.depth_levels = 5
        config.evolution.architecture_search = True
        config.safety.safety_level = SafetyLevel.HIGH
        return config
    
    @staticmethod
    def creative_mode() -> SEAGIConfig:
        """Configuration optimized for creative tasks"""
        config = SEAGIConfig()
        config.meta_learning.algorithm = LearningAlgorithm.NEURAL_ODE
        config.evolution.mutation_rate = 0.1
        config.safety.safety_level = SafetyLevel.MEDIUM
        return config
    
    @staticmethod
    def production_safe() -> SEAGIConfig:
        """Configuration for production deployment with maximum safety"""
        config = SEAGIConfig()
        config.safety.safety_level = SafetyLevel.MAXIMUM
        config.safety.human_oversight = True
        config.evolution.enabled = False
        config.meta_learning.use_second_order = False
        return config
    
    @staticmethod
    def experimental() -> SEAGIConfig:
        """Configuration for experimental research with fewer constraints"""
        config = SEAGIConfig()
        config.safety.safety_level = SafetyLevel.LOW
        config.evolution.evolution_rate = 0.2
        config.meta_learning.algorithm = LearningAlgorithm.HYPERNETWORK
        config.reflection.frequency = "aggressive"
        return config
