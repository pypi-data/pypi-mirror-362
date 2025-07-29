"""
Creative Agent for SE-AGI System

Handles creative tasks including ideation, design thinking, artistic creation,
innovative problem solving, and creative synthesis.
"""

import asyncio
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum
import random

from .base import BaseAgent, AgentCapability, Message, MessageType


class CreativeTaskType(Enum):
    """Types of creative tasks"""
    IDEATION = "ideation"
    DESIGN_THINKING = "design_thinking"
    ARTISTIC_CREATION = "artistic_creation"
    INNOVATION = "innovation"
    STORY_GENERATION = "story_generation"
    CONCEPT_DEVELOPMENT = "concept_development"
    BRAINSTORMING = "brainstorming"
    CREATIVE_SYNTHESIS = "creative_synthesis"


@dataclass
class CreativePrompt:
    """Creative task prompt"""
    task_type: CreativeTaskType
    description: str
    constraints: List[str] = None
    inspiration_sources: List[str] = None
    target_audience: str = None
    desired_style: str = None
    creativity_level: float = 0.8  # 0-1 scale
    domain: str = "general"
    
    def __post_init__(self):
        if self.constraints is None:
            self.constraints = []
        if self.inspiration_sources is None:
            self.inspiration_sources = []


@dataclass
class CreativeOutput:
    """Creative output from the agent"""
    content: str
    creativity_score: float
    originality_score: float
    feasibility_score: float
    task_type: CreativeTaskType
    metadata: Dict[str, Any]
    variations: List[str] = None
    
    def __post_init__(self):
        if self.variations is None:
            self.variations = []


class CreativeAgent(BaseAgent):
    """Agent specialized in creative tasks and innovative thinking"""
    
    def __init__(self, agent_id: str = "creative_agent"):
        capabilities = [
            AgentCapability("ideation", "Generate creative ideas and concepts"),
            AgentCapability("design_thinking", "Apply design thinking methodology"),
            AgentCapability("artistic_creation", "Create artistic content and expressions"),
            AgentCapability("innovation", "Develop innovative solutions"),
            AgentCapability("story_generation", "Create narratives and stories"),
            AgentCapability("brainstorming", "Facilitate creative brainstorming"),
            AgentCapability("creative_synthesis", "Combine ideas creatively"),
            AgentCapability("concept_development", "Develop and refine concepts")
        ]
        
        super().__init__(
            agent_id=agent_id,
            capabilities=capabilities,
            agent_type="creative"
        )
        
        # Creative thinking patterns
        self.thinking_patterns = {
            "divergent": ["expand", "explore", "generate", "multiply"],
            "convergent": ["focus", "synthesize", "refine", "select"],
            "lateral": ["reframe", "analogize", "invert", "randomize"],
            "associative": ["connect", "relate", "merge", "blend"]
        }
        
        # Creative techniques repository
        self.creative_techniques = {
            "scamper": ["substitute", "combine", "adapt", "modify", "put_to_other_uses", "eliminate", "reverse"],
            "six_hats": ["white", "red", "black", "yellow", "green", "blue"],
            "biomimicry": ["nature_patterns", "biological_systems", "evolutionary_adaptations"],
            "synectics": ["personal_analogy", "direct_analogy", "symbolic_analogy", "fantasy_analogy"]
        }
    
    async def process_message(self, message: Message) -> Message:
        """Process creative task messages"""
        try:
            if message.type == MessageType.TASK:
                creative_prompt = self._parse_creative_prompt(message.content)
                result = await self._execute_creative_task(creative_prompt)
                
                return Message(
                    type=MessageType.RESPONSE,
                    sender=self.agent_id,
                    recipient=message.sender,
                    content=result,
                    metadata={"task_type": creative_prompt.task_type.value}
                )
            else:
                return await super().process_message(message)
                
        except Exception as e:
            return Message(
                type=MessageType.ERROR,
                sender=self.agent_id,
                recipient=message.sender,
                content=f"Creative task failed: {str(e)}"
            )
    
    def _parse_creative_prompt(self, content: Union[str, Dict[str, Any]]) -> CreativePrompt:
        """Parse creative prompt from message content"""
        if isinstance(content, str):
            return CreativePrompt(
                task_type=CreativeTaskType.IDEATION,
                description=content
            )
        
        return CreativePrompt(
            task_type=CreativeTaskType(content.get("task_type", "ideation")),
            description=content["description"],
            constraints=content.get("constraints", []),
            inspiration_sources=content.get("inspiration_sources", []),
            target_audience=content.get("target_audience"),
            desired_style=content.get("desired_style"),
            creativity_level=content.get("creativity_level", 0.8),
            domain=content.get("domain", "general")
        )
    
    async def _execute_creative_task(self, prompt: CreativePrompt) -> CreativeOutput:
        """Execute the creative task based on type"""
        task_handlers = {
            CreativeTaskType.IDEATION: self._handle_ideation,
            CreativeTaskType.DESIGN_THINKING: self._handle_design_thinking,
            CreativeTaskType.ARTISTIC_CREATION: self._handle_artistic_creation,
            CreativeTaskType.INNOVATION: self._handle_innovation,
            CreativeTaskType.STORY_GENERATION: self._handle_story_generation,
            CreativeTaskType.CONCEPT_DEVELOPMENT: self._handle_concept_development,
            CreativeTaskType.BRAINSTORMING: self._handle_brainstorming,
            CreativeTaskType.CREATIVE_SYNTHESIS: self._handle_creative_synthesis
        }
        
        handler = task_handlers.get(prompt.task_type, self._handle_ideation)
        return await handler(prompt)
    
    async def _handle_ideation(self, prompt: CreativePrompt) -> CreativeOutput:
        """Handle ideation tasks"""
        # Use divergent thinking to generate multiple ideas
        ideas = []
        base_concepts = self._extract_concepts(prompt.description)
        
        # Apply creative techniques
        for technique in ["scamper", "lateral_thinking", "association"]:
            technique_ideas = await self._apply_creative_technique(technique, base_concepts, prompt)
            ideas.extend(technique_ideas)
        
        # Generate main content
        content = self._synthesize_ideas(ideas, prompt)
        
        # Create variations
        variations = [self._create_idea_variation(idea, prompt) for idea in ideas[:5]]
        
        return CreativeOutput(
            content=content,
            creativity_score=self._calculate_creativity_score(content, prompt),
            originality_score=self._calculate_originality_score(content),
            feasibility_score=self._calculate_feasibility_score(content, prompt),
            task_type=prompt.task_type,
            metadata={"ideas_generated": len(ideas), "techniques_used": 3},
            variations=variations
        )
    
    async def _handle_design_thinking(self, prompt: CreativePrompt) -> CreativeOutput:
        """Handle design thinking process"""
        # Follow design thinking stages: Empathize, Define, Ideate, Prototype, Test
        stages = {
            "empathize": await self._empathize_stage(prompt),
            "define": await self._define_stage(prompt),
            "ideate": await self._ideate_stage(prompt),
            "prototype": await self._prototype_stage(prompt),
            "test": await self._test_stage(prompt)
        }
        
        content = self._synthesize_design_thinking(stages, prompt)
        
        return CreativeOutput(
            content=content,
            creativity_score=0.85,
            originality_score=0.80,
            feasibility_score=0.90,
            task_type=prompt.task_type,
            metadata={"stages_completed": len(stages), "methodology": "design_thinking"}
        )
    
    async def _handle_artistic_creation(self, prompt: CreativePrompt) -> CreativeOutput:
        """Handle artistic creation tasks"""
        artistic_elements = {
            "style": prompt.desired_style or self._suggest_artistic_style(prompt),
            "theme": self._extract_artistic_theme(prompt.description),
            "medium": self._suggest_artistic_medium(prompt),
            "composition": self._create_composition_guide(prompt)
        }
        
        content = self._create_artistic_content(artistic_elements, prompt)
        
        return CreativeOutput(
            content=content,
            creativity_score=0.95,
            originality_score=0.90,
            feasibility_score=0.75,
            task_type=prompt.task_type,
            metadata=artistic_elements
        )
    
    async def _handle_innovation(self, prompt: CreativePrompt) -> CreativeOutput:
        """Handle innovation and invention tasks"""
        # Analyze problem space
        problem_analysis = self._analyze_innovation_space(prompt)
        
        # Generate innovative solutions
        solutions = []
        for approach in ["technological", "social", "systemic", "hybrid"]:
            approach_solutions = await self._generate_innovative_solutions(approach, prompt)
            solutions.extend(approach_solutions)
        
        content = self._synthesize_innovation(solutions, problem_analysis, prompt)
        
        return CreativeOutput(
            content=content,
            creativity_score=0.90,
            originality_score=0.85,
            feasibility_score=0.70,
            task_type=prompt.task_type,
            metadata={"solutions_generated": len(solutions), "innovation_approaches": 4}
        )
    
    async def _handle_story_generation(self, prompt: CreativePrompt) -> CreativeOutput:
        """Handle story and narrative generation"""
        story_elements = {
            "characters": self._create_characters(prompt),
            "setting": self._create_setting(prompt),
            "plot": self._create_plot_structure(prompt),
            "theme": self._identify_story_theme(prompt),
            "style": prompt.desired_style or "narrative"
        }
        
        content = self._generate_story(story_elements, prompt)
        
        return CreativeOutput(
            content=content,
            creativity_score=0.88,
            originality_score=0.82,
            feasibility_score=0.95,
            task_type=prompt.task_type,
            metadata=story_elements
        )
    
    async def _handle_concept_development(self, prompt: CreativePrompt) -> CreativeOutput:
        """Handle concept development and refinement"""
        initial_concept = self._extract_core_concept(prompt.description)
        
        development_stages = {
            "exploration": self._explore_concept_space(initial_concept, prompt),
            "elaboration": self._elaborate_concept_details(initial_concept, prompt),
            "refinement": self._refine_concept_clarity(initial_concept, prompt),
            "validation": self._validate_concept_viability(initial_concept, prompt)
        }
        
        content = self._synthesize_concept_development(development_stages, prompt)
        
        return CreativeOutput(
            content=content,
            creativity_score=0.75,
            originality_score=0.70,
            feasibility_score=0.85,
            task_type=prompt.task_type,
            metadata={"development_stages": len(development_stages)}
        )
    
    async def _handle_brainstorming(self, prompt: CreativePrompt) -> CreativeOutput:
        """Handle brainstorming sessions"""
        brainstorming_techniques = ["free_association", "mind_mapping", "rapid_ideation", "forced_connections"]
        
        all_ideas = []
        for technique in brainstorming_techniques:
            technique_ideas = await self._apply_brainstorming_technique(technique, prompt)
            all_ideas.extend(technique_ideas)
        
        # Organize and categorize ideas
        organized_ideas = self._organize_brainstormed_ideas(all_ideas, prompt)
        content = self._synthesize_brainstorming_results(organized_ideas, prompt)
        
        return CreativeOutput(
            content=content,
            creativity_score=0.85,
            originality_score=0.80,
            feasibility_score=0.75,
            task_type=prompt.task_type,
            metadata={"total_ideas": len(all_ideas), "techniques_used": len(brainstorming_techniques)}
        )
    
    async def _handle_creative_synthesis(self, prompt: CreativePrompt) -> CreativeOutput:
        """Handle creative synthesis of multiple concepts"""
        source_concepts = prompt.inspiration_sources or self._extract_concepts(prompt.description)
        
        synthesis_methods = ["combinatorial", "transformational", "analogical", "metaphorical"]
        synthesis_results = []
        
        for method in synthesis_methods:
            result = await self._apply_synthesis_method(method, source_concepts, prompt)
            synthesis_results.append(result)
        
        content = self._create_unified_synthesis(synthesis_results, prompt)
        
        return CreativeOutput(
            content=content,
            creativity_score=0.92,
            originality_score=0.88,
            feasibility_score=0.80,
            task_type=prompt.task_type,
            metadata={"synthesis_methods": len(synthesis_methods), "source_concepts": len(source_concepts)}
        )
    
    # Helper methods for creative processing
    
    def _extract_concepts(self, text: str) -> List[str]:
        """Extract key concepts from text"""
        # Simplified concept extraction
        words = text.lower().split()
        concepts = [word for word in words if len(word) > 4]
        return concepts[:10]  # Return top 10 concepts
    
    async def _apply_creative_technique(self, technique: str, concepts: List[str], prompt: CreativePrompt) -> List[str]:
        """Apply a specific creative technique"""
        if technique == "scamper":
            return self._apply_scamper(concepts, prompt)
        elif technique == "lateral_thinking":
            return self._apply_lateral_thinking(concepts, prompt)
        elif technique == "association":
            return self._apply_association(concepts, prompt)
        else:
            return concepts
    
    def _apply_scamper(self, concepts: List[str], prompt: CreativePrompt) -> List[str]:
        """Apply SCAMPER technique"""
        ideas = []
        scamper_actions = self.creative_techniques["scamper"]
        
        for concept in concepts[:3]:  # Apply to top 3 concepts
            for action in scamper_actions:
                idea = f"{action.title()}: {concept} - {self._generate_scamper_idea(action, concept, prompt)}"
                ideas.append(idea)
        
        return ideas
    
    def _generate_scamper_idea(self, action: str, concept: str, prompt: CreativePrompt) -> str:
        """Generate idea using SCAMPER action"""
        templates = {
            "substitute": f"What if we replaced {concept} with something unexpected?",
            "combine": f"How might we merge {concept} with another element?",
            "adapt": f"How could {concept} be adapted for a different context?",
            "modify": f"What if we amplified or minimized aspects of {concept}?",
            "put_to_other_uses": f"How else might {concept} be utilized?",
            "eliminate": f"What if we removed {concept} entirely?",
            "reverse": f"What if we did the opposite of {concept}?"
        }
        return templates.get(action, f"Creative transformation of {concept}")
    
    def _apply_lateral_thinking(self, concepts: List[str], prompt: CreativePrompt) -> List[str]:
        """Apply lateral thinking techniques"""
        ideas = []
        for concept in concepts[:3]:
            # Random word association
            random_words = ["cloud", "spiral", "mirror", "bridge", "fire", "silk"]
            random_word = random.choice(random_words)
            idea = f"Lateral connection: {concept} + {random_word} = {self._create_lateral_connection(concept, random_word, prompt)}"
            ideas.append(idea)
        
        return ideas
    
    def _create_lateral_connection(self, concept1: str, concept2: str, prompt: CreativePrompt) -> str:
        """Create lateral connection between concepts"""
        return f"A novel approach combining the essence of {concept1} with the characteristics of {concept2}"
    
    def _apply_association(self, concepts: List[str], prompt: CreativePrompt) -> List[str]:
        """Apply free association"""
        ideas = []
        for concept in concepts[:3]:
            associations = [f"{concept}-flow", f"{concept}-transformation", f"{concept}-harmony"]
            ideas.extend(associations)
        return ideas
    
    def _synthesize_ideas(self, ideas: List[str], prompt: CreativePrompt) -> str:
        """Synthesize generated ideas into coherent content"""
        synthesis = f"# Creative Ideation: {prompt.description}\n\n"
        synthesis += "## Generated Ideas\n\n"
        
        for i, idea in enumerate(ideas[:10], 1):
            synthesis += f"{i}. {idea}\n"
        
        synthesis += "\n## Creative Synthesis\n"
        synthesis += "The ideation process has generated diverse perspectives and novel approaches. "
        synthesis += "These ideas demonstrate creative potential through unconventional connections "
        synthesis += "and innovative reframings of the original challenge."
        
        return synthesis
    
    def _create_idea_variation(self, idea: str, prompt: CreativePrompt) -> str:
        """Create variation of an idea"""
        return f"Variation: {idea} - explored through a different creative lens"
    
    def _calculate_creativity_score(self, content: str, prompt: CreativePrompt) -> float:
        """Calculate creativity score for content"""
        # Simplified creativity scoring
        novelty_indicators = ["novel", "unique", "innovative", "original", "unexpected"]
        score = prompt.creativity_level
        
        for indicator in novelty_indicators:
            if indicator in content.lower():
                score += 0.1
        
        return min(score, 1.0)
    
    def _calculate_originality_score(self, content: str) -> float:
        """Calculate originality score"""
        # Simplified originality scoring
        return 0.8  # Placeholder
    
    def _calculate_feasibility_score(self, content: str, prompt: CreativePrompt) -> float:
        """Calculate feasibility score"""
        # Consider constraints and practical limitations
        if prompt.constraints:
            return 0.7  # Lower feasibility with constraints
        return 0.8
    
    # Design thinking stage methods
    
    async def _empathize_stage(self, prompt: CreativePrompt) -> str:
        """Empathize stage of design thinking"""
        return f"Understanding user needs and context for: {prompt.description}"
    
    async def _define_stage(self, prompt: CreativePrompt) -> str:
        """Define stage of design thinking"""
        return f"Problem definition: Core challenge identified in {prompt.description}"
    
    async def _ideate_stage(self, prompt: CreativePrompt) -> str:
        """Ideate stage of design thinking"""
        return "Generate wide range of creative solutions"
    
    async def _prototype_stage(self, prompt: CreativePrompt) -> str:
        """Prototype stage of design thinking"""
        return "Create testable representations of ideas"
    
    async def _test_stage(self, prompt: CreativePrompt) -> str:
        """Test stage of design thinking"""
        return "Validate solutions with users and iterate"
    
    def _synthesize_design_thinking(self, stages: Dict[str, str], prompt: CreativePrompt) -> str:
        """Synthesize design thinking process"""
        synthesis = f"# Design Thinking Process: {prompt.description}\n\n"
        
        for stage_name, stage_content in stages.items():
            synthesis += f"## {stage_name.title()} Stage\n"
            synthesis += f"{stage_content}\n\n"
        
        synthesis += "## Process Integration\n"
        synthesis += "The design thinking approach provides a human-centered framework for "
        synthesis += "creative problem solving, ensuring solutions are both innovative and practical."
        
        return synthesis
    
    # Additional helper methods for other creative tasks
    
    def _suggest_artistic_style(self, prompt: CreativePrompt) -> str:
        """Suggest appropriate artistic style"""
        styles = ["abstract", "impressionist", "minimalist", "surreal", "realistic"]
        return random.choice(styles)
    
    def _extract_artistic_theme(self, description: str) -> str:
        """Extract artistic theme from description"""
        return "creative expression"  # Simplified
    
    def _suggest_artistic_medium(self, prompt: CreativePrompt) -> str:
        """Suggest artistic medium"""
        mediums = ["digital", "traditional", "mixed_media", "conceptual"]
        return random.choice(mediums)
    
    def _create_composition_guide(self, prompt: CreativePrompt) -> str:
        """Create composition guide"""
        return "balanced composition with focal point emphasis"
    
    def _create_artistic_content(self, elements: Dict[str, str], prompt: CreativePrompt) -> str:
        """Create artistic content description"""
        content = f"# Artistic Creation: {prompt.description}\n\n"
        content += f"**Style**: {elements['style']}\n"
        content += f"**Theme**: {elements['theme']}\n"
        content += f"**Medium**: {elements['medium']}\n"
        content += f"**Composition**: {elements['composition']}\n\n"
        content += "## Creative Vision\n"
        content += "The artistic creation embodies creative expression through carefully chosen "
        content += "stylistic elements and thematic development."
        
        return content
    
    def _analyze_innovation_space(self, prompt: CreativePrompt) -> Dict[str, Any]:
        """Analyze innovation opportunity space"""
        return {
            "problem_scope": "defined",
            "solution_space": "open",
            "constraints": prompt.constraints,
            "opportunities": ["technological", "social", "economic"]
        }
    
    async def _generate_innovative_solutions(self, approach: str, prompt: CreativePrompt) -> List[str]:
        """Generate innovative solutions by approach"""
        solutions = [f"{approach} innovation approach for {prompt.description}"]
        return solutions
    
    def _synthesize_innovation(self, solutions: List[str], analysis: Dict[str, Any], prompt: CreativePrompt) -> str:
        """Synthesize innovation results"""
        content = f"# Innovation Report: {prompt.description}\n\n"
        content += "## Problem Analysis\n"
        content += f"Scope: {analysis['problem_scope']}\n\n"
        content += "## Innovative Solutions\n"
        for i, solution in enumerate(solutions, 1):
            content += f"{i}. {solution}\n"
        
        return content
    
    # Story generation helpers
    
    def _create_characters(self, prompt: CreativePrompt) -> List[str]:
        """Create story characters"""
        return ["protagonist", "supporting character", "antagonist"]
    
    def _create_setting(self, prompt: CreativePrompt) -> str:
        """Create story setting"""
        return "immersive environment that supports the narrative"
    
    def _create_plot_structure(self, prompt: CreativePrompt) -> str:
        """Create plot structure"""
        return "three-act structure with compelling conflict and resolution"
    
    def _identify_story_theme(self, prompt: CreativePrompt) -> str:
        """Identify story theme"""
        return "universal human experience"
    
    def _generate_story(self, elements: Dict[str, Any], prompt: CreativePrompt) -> str:
        """Generate story content"""
        content = f"# Story: {prompt.description}\n\n"
        content += f"**Characters**: {', '.join(elements['characters'])}\n"
        content += f"**Setting**: {elements['setting']}\n"
        content += f"**Plot**: {elements['plot']}\n"
        content += f"**Theme**: {elements['theme']}\n\n"
        content += "## Narrative\n"
        content += "The story unfolds through carefully developed characters and plot progression..."
        
        return content
    
    # Additional synthesis methods would continue here...
    
    def _extract_core_concept(self, description: str) -> str:
        """Extract core concept for development"""
        return description.split()[0] if description else "concept"
    
    def _explore_concept_space(self, concept: str, prompt: CreativePrompt) -> str:
        """Explore concept space"""
        return f"Exploration of {concept} across multiple dimensions"
    
    def _elaborate_concept_details(self, concept: str, prompt: CreativePrompt) -> str:
        """Elaborate concept details"""
        return f"Detailed elaboration of {concept} components and relationships"
    
    def _refine_concept_clarity(self, concept: str, prompt: CreativePrompt) -> str:
        """Refine concept clarity"""
        return f"Clarification and refinement of {concept} definition"
    
    def _validate_concept_viability(self, concept: str, prompt: CreativePrompt) -> str:
        """Validate concept viability"""
        return f"Viability assessment of {concept} implementation"
    
    def _synthesize_concept_development(self, stages: Dict[str, str], prompt: CreativePrompt) -> str:
        """Synthesize concept development"""
        content = f"# Concept Development: {prompt.description}\n\n"
        for stage_name, stage_content in stages.items():
            content += f"## {stage_name.title()}\n{stage_content}\n\n"
        return content
    
    async def _apply_brainstorming_technique(self, technique: str, prompt: CreativePrompt) -> List[str]:
        """Apply specific brainstorming technique"""
        return [f"{technique} generated idea for {prompt.description}"]
    
    def _organize_brainstormed_ideas(self, ideas: List[str], prompt: CreativePrompt) -> Dict[str, List[str]]:
        """Organize brainstormed ideas"""
        return {"category_1": ideas[:5], "category_2": ideas[5:10]}
    
    def _synthesize_brainstorming_results(self, organized_ideas: Dict[str, List[str]], prompt: CreativePrompt) -> str:
        """Synthesize brainstorming results"""
        content = f"# Brainstorming Session: {prompt.description}\n\n"
        for category, ideas in organized_ideas.items():
            content += f"## {category.replace('_', ' ').title()}\n"
            for idea in ideas:
                content += f"- {idea}\n"
            content += "\n"
        return content
    
    async def _apply_synthesis_method(self, method: str, concepts: List[str], prompt: CreativePrompt) -> str:
        """Apply synthesis method"""
        return f"{method} synthesis of {', '.join(concepts[:3])}"
    
    def _create_unified_synthesis(self, results: List[str], prompt: CreativePrompt) -> str:
        """Create unified synthesis"""
        content = f"# Creative Synthesis: {prompt.description}\n\n"
        for i, result in enumerate(results, 1):
            content += f"## Synthesis Method {i}\n{result}\n\n"
        content += "## Unified Creative Output\n"
        content += "The synthesis process reveals novel connections and innovative possibilities."
        return content
