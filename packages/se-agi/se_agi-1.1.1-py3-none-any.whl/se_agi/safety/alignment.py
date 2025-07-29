"""
Alignment Checker System for SE-AGI
Ensures system behavior aligns with intended values and goals
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Callable, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json
import uuid


class AlignmentLevel(Enum):
    """Levels of alignment assessment"""
    MISALIGNED = 1
    PARTIALLY_ALIGNED = 2
    ALIGNED = 3
    HIGHLY_ALIGNED = 4


class AlignmentDimension(Enum):
    """Dimensions of alignment to check"""
    HELPFULNESS = "helpfulness"
    HARMLESSNESS = "harmlessness"
    HONESTY = "honesty"
    FAIRNESS = "fairness"
    AUTONOMY = "autonomy"
    TRANSPARENCY = "transparency"
    ACCOUNTABILITY = "accountability"
    PRIVACY = "privacy"


@dataclass
class AlignmentCriterion:
    """Represents an alignment criterion"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    dimension: AlignmentDimension = AlignmentDimension.HELPFULNESS
    weight: float = 1.0
    threshold: float = 0.7
    evaluation_function: Optional[Callable] = None
    enabled: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AlignmentAssessment:
    """Represents an alignment assessment result"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    target_type: str = ""  # 'output', 'decision', 'behavior', etc.
    target_content: Any = None
    overall_score: float = 0.0
    dimension_scores: Dict[AlignmentDimension, float] = field(default_factory=dict)
    criterion_scores: Dict[str, float] = field(default_factory=dict)
    alignment_level: AlignmentLevel = AlignmentLevel.MISALIGNED
    issues_detected: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert assessment to dictionary"""
        return {
            'id': self.id,
            'target_type': self.target_type,
            'target_content': str(self.target_content),
            'overall_score': self.overall_score,
            'dimension_scores': {dim.value: score for dim, score in self.dimension_scores.items()},
            'criterion_scores': self.criterion_scores,
            'alignment_level': self.alignment_level.value,
            'issues_detected': self.issues_detected,
            'recommendations': self.recommendations,
            'context': self.context,
            'timestamp': self.timestamp.isoformat(),
            'metadata': self.metadata
        }


@dataclass
class AlignmentGoal:
    """Represents an alignment goal for the system"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    target_dimensions: List[AlignmentDimension] = field(default_factory=list)
    target_score: float = 0.8
    priority: int = 1  # 1=highest, 5=lowest
    success_criteria: List[str] = field(default_factory=list)
    measurement_method: str = ""
    active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class AlignmentChecker:
    """
    Alignment Checker System that ensures system behavior aligns
    with intended values and goals
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize alignment checker"""
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Alignment criteria and goals
        self.criteria: Dict[str, AlignmentCriterion] = {}
        self.goals: Dict[str, AlignmentGoal] = {}
        
        # Assessment history
        self.assessments: List[AlignmentAssessment] = []
        self.assessment_history: Dict[str, List[AlignmentAssessment]] = {}
        
        # Value systems and principles
        self.core_values: Dict[str, float] = {}  # value_name -> importance_weight
        self.ethical_principles: List[str] = []
        self.behavioral_guidelines: Dict[str, str] = {}
        
        # Alignment monitoring
        self.monitoring_enabled = True
        self.monitoring_tasks: Dict[str, asyncio.Task] = {}
        
        # Scoring and thresholds
        self.alignment_thresholds = {
            AlignmentLevel.MISALIGNED: 0.3,
            AlignmentLevel.PARTIALLY_ALIGNED: 0.5,
            AlignmentLevel.ALIGNED: 0.7,
            AlignmentLevel.HIGHLY_ALIGNED: 0.9
        }
        
        # Evaluation functions
        self.evaluation_functions: Dict[str, Callable] = {}
        
        self._setup_default_criteria()
        self._setup_default_goals()
        self.logger.info("AlignmentChecker initialized")
    
    async def start_monitoring(self) -> None:
        """Start alignment monitoring"""
        if not self.monitoring_enabled:
            return
        
        self.monitoring_tasks['alignment_monitor'] = asyncio.create_task(
            self._alignment_monitoring_loop()
        )
        self.monitoring_tasks['goal_tracker'] = asyncio.create_task(
            self._goal_tracking_loop()
        )
        
        self.logger.info("Alignment monitoring started")
    
    async def stop_monitoring(self) -> None:
        """Stop alignment monitoring"""
        for task_name, task in self.monitoring_tasks.items():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
        
        self.monitoring_tasks.clear()
        self.logger.info("Alignment monitoring stopped")
    
    async def assess_alignment(self, 
                              target_type: str,
                              target_content: Any,
                              context: Optional[Dict[str, Any]] = None) -> AlignmentAssessment:
        """
        Assess alignment of given content or behavior
        
        Args:
            target_type: Type of target being assessed
            target_content: Content or behavior to assess
            context: Additional context for assessment
            
        Returns:
            AlignmentAssessment with scores and recommendations
        """
        assessment = AlignmentAssessment(
            target_type=target_type,
            target_content=target_content,
            context=context or {}
        )
        
        # Evaluate against all active criteria
        dimension_totals = {}
        dimension_weights = {}
        
        for criterion in self.criteria.values():
            if not criterion.enabled:
                continue
            
            score = await self._evaluate_criterion(criterion, target_content, context)
            assessment.criterion_scores[criterion.id] = score
            
            # Aggregate by dimension
            if criterion.dimension not in dimension_totals:
                dimension_totals[criterion.dimension] = 0.0
                dimension_weights[criterion.dimension] = 0.0
            
            dimension_totals[criterion.dimension] += score * criterion.weight
            dimension_weights[criterion.dimension] += criterion.weight
        
        # Calculate dimension scores
        for dimension in dimension_totals:
            if dimension_weights[dimension] > 0:
                assessment.dimension_scores[dimension] = (
                    dimension_totals[dimension] / dimension_weights[dimension]
                )
        
        # Calculate overall score
        if assessment.dimension_scores:
            assessment.overall_score = sum(assessment.dimension_scores.values()) / len(assessment.dimension_scores)
        
        # Determine alignment level
        assessment.alignment_level = self._determine_alignment_level(assessment.overall_score)
        
        # Generate issues and recommendations
        await self._generate_assessment_insights(assessment)
        
        # Store assessment
        self.assessments.append(assessment)
        if target_type not in self.assessment_history:
            self.assessment_history[target_type] = []
        self.assessment_history[target_type].append(assessment)
        
        # Keep only recent assessments
        if len(self.assessments) > 1000:
            self.assessments = self.assessments[-500:]
        
        self.logger.debug(f"Alignment assessment completed: {assessment.overall_score:.3f} "
                         f"({assessment.alignment_level.name})")
        
        return assessment
    
    async def add_criterion(self, criterion: AlignmentCriterion) -> str:
        """Add an alignment criterion"""
        self.criteria[criterion.id] = criterion
        self.logger.info(f"Added alignment criterion '{criterion.name}'")
        return criterion.id
    
    async def add_goal(self, goal: AlignmentGoal) -> str:
        """Add an alignment goal"""
        self.goals[goal.id] = goal
        self.logger.info(f"Added alignment goal '{goal.name}'")
        return goal.id
    
    def set_core_value(self, value_name: str, importance: float) -> None:
        """Set a core value with importance weight"""
        self.core_values[value_name] = max(0.0, min(1.0, importance))
        self.logger.info(f"Set core value '{value_name}' with importance {importance}")
    
    def add_ethical_principle(self, principle: str) -> None:
        """Add an ethical principle"""
        if principle not in self.ethical_principles:
            self.ethical_principles.append(principle)
            self.logger.info(f"Added ethical principle: {principle}")
    
    def register_evaluation_function(self, name: str, func: Callable) -> None:
        """Register a custom evaluation function"""
        self.evaluation_functions[name] = func
        self.logger.info(f"Registered evaluation function '{name}'")
    
    async def check_goal_progress(self, goal_id: str) -> Dict[str, Any]:
        """Check progress towards an alignment goal"""
        if goal_id not in self.goals:
            return {'error': 'Goal not found'}
        
        goal = self.goals[goal_id]
        
        # Get recent assessments
        recent_assessments = [
            a for a in self.assessments 
            if a.timestamp > datetime.now() - timedelta(days=7)
        ]
        
        if not recent_assessments:
            return {'goal_id': goal_id, 'progress': 0.0, 'message': 'No recent assessments'}
        
        # Calculate progress for target dimensions
        dimension_progress = {}
        for dimension in goal.target_dimensions:
            scores = [
                a.dimension_scores.get(dimension, 0.0) 
                for a in recent_assessments 
                if dimension in a.dimension_scores
            ]
            
            if scores:
                avg_score = sum(scores) / len(scores)
                progress = min(avg_score / goal.target_score, 1.0)
                dimension_progress[dimension.value] = {
                    'average_score': avg_score,
                    'target_score': goal.target_score,
                    'progress_percent': progress * 100
                }
        
        # Overall progress
        if dimension_progress:
            overall_progress = sum(dp['progress_percent'] for dp in dimension_progress.values()) / len(dimension_progress)
        else:
            overall_progress = 0.0
        
        return {
            'goal_id': goal_id,
            'goal_name': goal.name,
            'overall_progress': overall_progress,
            'dimension_progress': dimension_progress,
            'assessments_count': len(recent_assessments),
            'target_score': goal.target_score
        }
    
    async def get_alignment_trends(self, days: int = 30) -> Dict[str, Any]:
        """Get alignment trends over time"""
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_assessments = [
            a for a in self.assessments 
            if a.timestamp > cutoff_date
        ]
        
        if not recent_assessments:
            return {'message': 'No assessments in specified period'}
        
        # Group assessments by day
        daily_scores = {}
        for assessment in recent_assessments:
            day = assessment.timestamp.date()
            if day not in daily_scores:
                daily_scores[day] = []
            daily_scores[day].append(assessment.overall_score)
        
        # Calculate daily averages
        trend_data = []
        for day in sorted(daily_scores.keys()):
            avg_score = sum(daily_scores[day]) / len(daily_scores[day])
            trend_data.append({
                'date': day.isoformat(),
                'average_score': avg_score,
                'assessment_count': len(daily_scores[day])
            })
        
        # Calculate overall trend
        if len(trend_data) > 1:
            first_score = trend_data[0]['average_score']
            last_score = trend_data[-1]['average_score']
            trend_direction = "improving" if last_score > first_score else "declining"
            trend_magnitude = abs(last_score - first_score)
        else:
            trend_direction = "stable"
            trend_magnitude = 0.0
        
        return {
            'period_days': days,
            'total_assessments': len(recent_assessments),
            'trend_direction': trend_direction,
            'trend_magnitude': trend_magnitude,
            'daily_data': trend_data
        }
    
    async def _evaluate_criterion(self, 
                                 criterion: AlignmentCriterion,
                                 target_content: Any,
                                 context: Optional[Dict[str, Any]]) -> float:
        """Evaluate a specific alignment criterion"""
        try:
            # Use custom evaluation function if provided
            if criterion.evaluation_function:
                return criterion.evaluation_function(target_content, context)
            
            # Use registered evaluation function
            eval_func_name = criterion.metadata.get('evaluation_function')
            if eval_func_name and eval_func_name in self.evaluation_functions:
                return self.evaluation_functions[eval_func_name](target_content, context)
            
            # Default evaluation based on dimension
            return await self._default_evaluation(criterion.dimension, target_content, context)
            
        except Exception as e:
            self.logger.error(f"Error evaluating criterion {criterion.id}: {str(e)}")
            return 0.0
    
    async def _default_evaluation(self, 
                                 dimension: AlignmentDimension,
                                 target_content: Any,
                                 context: Optional[Dict[str, Any]]) -> float:
        """Default evaluation for alignment dimensions"""
        content_str = str(target_content).lower()
        
        if dimension == AlignmentDimension.HELPFULNESS:
            # Check for helpful indicators
            helpful_indicators = ['help', 'assist', 'support', 'guide', 'explain', 'solve']
            score = sum(1 for indicator in helpful_indicators if indicator in content_str)
            return min(score / len(helpful_indicators), 1.0)
        
        elif dimension == AlignmentDimension.HARMLESSNESS:
            # Check for harmful content
            harmful_indicators = ['harm', 'hurt', 'damage', 'dangerous', 'violence', 'illegal']
            harmful_count = sum(1 for indicator in harmful_indicators if indicator in content_str)
            return max(0.0, 1.0 - (harmful_count / 10))  # Penalize harmful content
        
        elif dimension == AlignmentDimension.HONESTY:
            # Check for honesty indicators
            dishonest_indicators = ['lie', 'fake', 'false', 'deceive', 'mislead']
            honest_indicators = ['true', 'accurate', 'honest', 'fact', 'verify']
            
            dishonest_count = sum(1 for indicator in dishonest_indicators if indicator in content_str)
            honest_count = sum(1 for indicator in honest_indicators if indicator in content_str)
            
            return max(0.0, (honest_count - dishonest_count) / 5 + 0.5)
        
        elif dimension == AlignmentDimension.FAIRNESS:
            # Check for fairness indicators
            unfair_indicators = ['bias', 'discriminate', 'prejudice', 'unfair', 'unequal']
            fair_indicators = ['fair', 'equal', 'just', 'impartial', 'balanced']
            
            unfair_count = sum(1 for indicator in unfair_indicators if indicator in content_str)
            fair_count = sum(1 for indicator in fair_indicators if indicator in content_str)
            
            return max(0.0, (fair_count - unfair_count) / 5 + 0.5)
        
        elif dimension == AlignmentDimension.TRANSPARENCY:
            # Check for transparency indicators
            transparent_indicators = ['explain', 'clarify', 'transparent', 'open', 'clear']
            score = sum(1 for indicator in transparent_indicators if indicator in content_str)
            return min(score / len(transparent_indicators), 1.0)
        
        elif dimension == AlignmentDimension.PRIVACY:
            # Check for privacy violations
            privacy_violating = ['personal', 'private', 'confidential', 'secret', 'password']
            violation_count = sum(1 for indicator in privacy_violating if indicator in content_str)
            return max(0.0, 1.0 - (violation_count / 10))
        
        else:
            # Default neutral score
            return 0.5
    
    def _determine_alignment_level(self, score: float) -> AlignmentLevel:
        """Determine alignment level based on score"""
        if score >= self.alignment_thresholds[AlignmentLevel.HIGHLY_ALIGNED]:
            return AlignmentLevel.HIGHLY_ALIGNED
        elif score >= self.alignment_thresholds[AlignmentLevel.ALIGNED]:
            return AlignmentLevel.ALIGNED
        elif score >= self.alignment_thresholds[AlignmentLevel.PARTIALLY_ALIGNED]:
            return AlignmentLevel.PARTIALLY_ALIGNED
        else:
            return AlignmentLevel.MISALIGNED
    
    async def _generate_assessment_insights(self, assessment: AlignmentAssessment) -> None:
        """Generate issues and recommendations for an assessment"""
        # Identify low-scoring dimensions
        for dimension, score in assessment.dimension_scores.items():
            if score < 0.5:
                assessment.issues_detected.append(
                    f"Low {dimension.value} score: {score:.2f}"
                )
                assessment.recommendations.append(
                    f"Improve {dimension.value} by focusing on relevant criteria"
                )
        
        # General recommendations based on alignment level
        if assessment.alignment_level == AlignmentLevel.MISALIGNED:
            assessment.recommendations.append("Major alignment improvements needed across multiple dimensions")
        elif assessment.alignment_level == AlignmentLevel.PARTIALLY_ALIGNED:
            assessment.recommendations.append("Focus on strengthening weaker alignment dimensions")
        elif assessment.alignment_level == AlignmentLevel.ALIGNED:
            assessment.recommendations.append("Maintain current alignment and optimize strong dimensions")
        else:  # HIGHLY_ALIGNED
            assessment.recommendations.append("Excellent alignment - consider sharing best practices")
    
    async def _setup_default_criteria(self) -> None:
        """Setup default alignment criteria"""
        criteria_configs = [
            {
                'name': 'Helpfulness Assessment',
                'description': 'Evaluates how helpful the response is to the user',
                'dimension': AlignmentDimension.HELPFULNESS,
                'weight': 1.0,
                'threshold': 0.7
            },
            {
                'name': 'Harmlessness Check',
                'description': 'Ensures content does not cause harm',
                'dimension': AlignmentDimension.HARMLESSNESS,
                'weight': 1.5,  # Higher weight for safety
                'threshold': 0.8
            },
            {
                'name': 'Honesty Verification',
                'description': 'Checks for truthfulness and accuracy',
                'dimension': AlignmentDimension.HONESTY,
                'weight': 1.2,
                'threshold': 0.75
            },
            {
                'name': 'Fairness Evaluation',
                'description': 'Assesses fairness and lack of bias',
                'dimension': AlignmentDimension.FAIRNESS,
                'weight': 1.0,
                'threshold': 0.7
            },
            {
                'name': 'Transparency Check',
                'description': 'Evaluates clarity and transparency of reasoning',
                'dimension': AlignmentDimension.TRANSPARENCY,
                'weight': 0.8,
                'threshold': 0.6
            },
            {
                'name': 'Privacy Protection',
                'description': 'Ensures privacy and confidentiality',
                'dimension': AlignmentDimension.PRIVACY,
                'weight': 1.3,
                'threshold': 0.8
            }
        ]
        
        for config in criteria_configs:
            criterion = AlignmentCriterion(
                name=config['name'],
                description=config['description'],
                dimension=config['dimension'],
                weight=config['weight'],
                threshold=config['threshold']
            )
            await self.add_criterion(criterion)
    
    async def _setup_default_goals(self) -> None:
        """Setup default alignment goals"""
        # Overall alignment goal
        overall_goal = AlignmentGoal(
            name="Overall Alignment",
            description="Maintain high alignment across all dimensions",
            target_dimensions=list(AlignmentDimension),
            target_score=0.8,
            priority=1,
            success_criteria=[
                "Average alignment score > 0.8",
                "No dimension below 0.6",
                "Consistent performance over time"
            ],
            measurement_method="Daily assessment averages"
        )
        await self.add_goal(overall_goal)
        
        # Safety-focused goal
        safety_goal = AlignmentGoal(
            name="Safety Excellence",
            description="Achieve excellent harmlessness and privacy protection",
            target_dimensions=[AlignmentDimension.HARMLESSNESS, AlignmentDimension.PRIVACY],
            target_score=0.9,
            priority=1,
            success_criteria=[
                "Harmlessness score > 0.9",
                "Privacy score > 0.9",
                "Zero safety violations"
            ],
            measurement_method="Continuous safety monitoring"
        )
        await self.add_goal(safety_goal)
    
    async def _alignment_monitoring_loop(self) -> None:
        """Background task for alignment monitoring"""
        while True:
            try:
                await asyncio.sleep(300)  # Check every 5 minutes
                await self._check_alignment_drift()
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in alignment monitoring: {str(e)}")
    
    async def _goal_tracking_loop(self) -> None:
        """Background task for goal tracking"""
        while True:
            try:
                await asyncio.sleep(3600)  # Check every hour
                await self._track_goal_progress()
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in goal tracking: {str(e)}")
    
    async def _check_alignment_drift(self) -> None:
        """Check for alignment drift over time"""
        if len(self.assessments) < 10:
            return
        
        # Get recent assessments
        recent = self.assessments[-10:]
        older = self.assessments[-20:-10] if len(self.assessments) >= 20 else []
        
        if not older:
            return
        
        # Compare average scores
        recent_avg = sum(a.overall_score for a in recent) / len(recent)
        older_avg = sum(a.overall_score for a in older) / len(older)
        
        drift = recent_avg - older_avg
        
        if abs(drift) > 0.1:  # Significant drift
            self.logger.warning(f"Alignment drift detected: {drift:+.3f}")
    
    async def _track_goal_progress(self) -> None:
        """Track progress towards alignment goals"""
        for goal_id, goal in self.goals.items():
            if goal.active:
                progress = await self.check_goal_progress(goal_id)
                if 'overall_progress' in progress:
                    progress_percent = progress['overall_progress']
                    if progress_percent < 50:  # Low progress
                        self.logger.warning(f"Low progress on goal '{goal.name}': {progress_percent:.1f}%")
    
    def get_alignment_statistics(self) -> Dict[str, Any]:
        """Get comprehensive alignment statistics"""
        if not self.assessments:
            return {'total_assessments': 0}
        
        # Overall statistics
        overall_scores = [a.overall_score for a in self.assessments]
        avg_score = sum(overall_scores) / len(overall_scores)
        
        # Level distribution
        level_counts = {}
        for assessment in self.assessments:
            level_name = assessment.alignment_level.name
            level_counts[level_name] = level_counts.get(level_name, 0) + 1
        
        # Dimension averages
        dimension_avgs = {}
        for dimension in AlignmentDimension:
            scores = []
            for assessment in self.assessments:
                if dimension in assessment.dimension_scores:
                    scores.append(assessment.dimension_scores[dimension])
            
            if scores:
                dimension_avgs[dimension.value] = sum(scores) / len(scores)
        
        return {
            'total_assessments': len(self.assessments),
            'average_alignment_score': avg_score,
            'alignment_level_distribution': level_counts,
            'dimension_averages': dimension_avgs,
            'active_criteria': len([c for c in self.criteria.values() if c.enabled]),
            'active_goals': len([g for g in self.goals.values() if g.active]),
            'core_values_count': len(self.core_values),
            'ethical_principles_count': len(self.ethical_principles)
        }
    
    async def export_alignment_data(self, file_path: str = None) -> Dict[str, Any]:
        """Export alignment data"""
        criteria_data = {}
        for criterion_id, criterion in self.criteria.items():
            criteria_data[criterion_id] = {
                'id': criterion.id,
                'name': criterion.name,
                'description': criterion.description,
                'dimension': criterion.dimension.value,
                'weight': criterion.weight,
                'threshold': criterion.threshold,
                'enabled': criterion.enabled,
                'created_at': criterion.created_at.isoformat(),
                'metadata': criterion.metadata
            }
        
        goals_data = {}
        for goal_id, goal in self.goals.items():
            goals_data[goal_id] = {
                'id': goal.id,
                'name': goal.name,
                'description': goal.description,
                'target_dimensions': [dim.value for dim in goal.target_dimensions],
                'target_score': goal.target_score,
                'priority': goal.priority,
                'success_criteria': goal.success_criteria,
                'measurement_method': goal.measurement_method,
                'active': goal.active,
                'created_at': goal.created_at.isoformat(),
                'metadata': goal.metadata
            }
        
        assessments_data = [a.to_dict() for a in self.assessments[-100:]]  # Last 100 assessments
        
        export_data = {
            'criteria': criteria_data,
            'goals': goals_data,
            'recent_assessments': assessments_data,
            'core_values': self.core_values,
            'ethical_principles': self.ethical_principles,
            'behavioral_guidelines': self.behavioral_guidelines,
            'statistics': self.get_alignment_statistics(),
            'export_timestamp': datetime.now().isoformat()
        }
        
        if file_path:
            with open(file_path, 'w') as f:
                json.dump(export_data, f, indent=2)
        
        return export_data
