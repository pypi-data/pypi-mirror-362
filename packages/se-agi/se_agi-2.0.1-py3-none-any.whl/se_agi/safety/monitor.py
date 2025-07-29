"""
Safety Monitor System for SE-AGI
Monitors system behavior and prevents harmful actions
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Callable, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json
import uuid


class SafetyLevel(Enum):
    """Safety levels for different types of operations"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class ViolationType(Enum):
    """Types of safety violations"""
    HARMFUL_OUTPUT = "harmful_output"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    RESOURCE_ABUSE = "resource_abuse"
    INFINITE_LOOP = "infinite_loop"
    MEMORY_OVERFLOW = "memory_overflow"
    UNSAFE_OPERATION = "unsafe_operation"
    ETHICAL_VIOLATION = "ethical_violation"
    PRIVACY_BREACH = "privacy_breach"


@dataclass
class SafetyRule:
    """Represents a safety rule"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    rule_type: str = "content_filter"
    pattern: str = ""
    action: str = "block"  # block, warn, log
    severity: SafetyLevel = SafetyLevel.MEDIUM
    enabled: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SafetyViolation:
    """Represents a safety violation"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    violation_type: ViolationType = ViolationType.UNSAFE_OPERATION
    severity: SafetyLevel = SafetyLevel.MEDIUM
    message: str = ""
    context: Dict[str, Any] = field(default_factory=dict)
    triggered_rules: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    source: str = ""
    resolved: bool = False
    resolution_action: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert violation to dictionary"""
        return {
            'id': self.id,
            'violation_type': self.violation_type.value,
            'severity': self.severity.value,
            'message': self.message,
            'context': self.context,
            'triggered_rules': self.triggered_rules,
            'timestamp': self.timestamp.isoformat(),
            'source': self.source,
            'resolved': self.resolved,
            'resolution_action': self.resolution_action,
            'metadata': self.metadata
        }


@dataclass
class SafetyCheck:
    """Represents a safety check to be performed"""
    check_type: str
    content: Any
    context: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class SafetyMonitor:
    """
    Safety Monitor System that continuously monitors system behavior
    and prevents harmful or unsafe operations
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize safety monitor"""
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Safety rules and violations
        self.rules: Dict[str, SafetyRule] = {}
        self.violations: List[SafetyViolation] = []
        
        # Monitoring state
        self.monitoring_enabled = True
        self.monitoring_tasks: Dict[str, asyncio.Task] = {}
        
        # Content filters
        self.content_filters: Dict[str, Callable] = {}
        self.behavior_monitors: Dict[str, Callable] = {}
        
        # Thresholds and limits
        self.resource_limits = self.config.get('resource_limits', {
            'max_memory_mb': 1000,
            'max_cpu_percent': 80,
            'max_requests_per_minute': 1000,
            'max_operation_duration': 300  # 5 minutes
        })
        
        # Rate limiting
        self.request_history: List[datetime] = []
        self.operation_history: Dict[str, datetime] = {}
        
        # Violation tracking
        self.violation_counts: Dict[ViolationType, int] = {vt: 0 for vt in ViolationType}
        self.violation_history: List[SafetyViolation] = []
        
        # Emergency protocols
        self.emergency_enabled = True
        self.emergency_threshold = 5  # violations before emergency response
        self.emergency_actions = ['log', 'alert', 'shutdown']
        
        self._setup_default_rules()
        self.logger.info("SafetyMonitor initialized")
    
    async def start_monitoring(self) -> None:
        """Start safety monitoring"""
        if not self.monitoring_enabled:
            return
        
        # Start monitoring tasks
        self.monitoring_tasks['resource_monitor'] = asyncio.create_task(
            self._resource_monitoring_loop()
        )
        self.monitoring_tasks['violation_monitor'] = asyncio.create_task(
            self._violation_monitoring_loop()
        )
        
        self.logger.info("Safety monitoring started")
    
    async def stop_monitoring(self) -> None:
        """Stop safety monitoring"""
        for task_name, task in self.monitoring_tasks.items():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
        
        self.monitoring_tasks.clear()
        self.logger.info("Safety monitoring stopped")
    
    async def check_safety(self, check: SafetyCheck) -> Tuple[bool, Optional[SafetyViolation]]:
        """
        Perform a safety check
        
        Args:
            check: Safety check to perform
            
        Returns:
            Tuple of (is_safe, violation_if_any)
        """
        if not self.monitoring_enabled:
            return True, None
        
        # Check against all applicable rules
        violations = []
        
        for rule in self.rules.values():
            if not rule.enabled:
                continue
            
            violation = await self._check_rule(rule, check)
            if violation:
                violations.append(violation)
        
        # Check specific content filters
        if check.check_type in self.content_filters:
            filter_func = self.content_filters[check.check_type]
            filter_result = await self._run_content_filter(filter_func, check)
            if filter_result:
                violations.append(filter_result)
        
        # Check behavior monitors
        if check.check_type in self.behavior_monitors:
            monitor_func = self.behavior_monitors[check.check_type]
            monitor_result = await self._run_behavior_monitor(monitor_func, check)
            if monitor_result:
                violations.append(monitor_result)
        
        # Process violations
        if violations:
            # Take the most severe violation
            most_severe = max(violations, key=lambda v: v.severity.value)
            await self._process_violation(most_severe)
            return False, most_severe
        
        return True, None
    
    async def add_safety_rule(self, rule: SafetyRule) -> str:
        """Add a new safety rule"""
        self.rules[rule.id] = rule
        self.logger.info(f"Added safety rule '{rule.name}' with ID {rule.id}")
        return rule.id
    
    async def remove_safety_rule(self, rule_id: str) -> bool:
        """Remove a safety rule"""
        if rule_id in self.rules:
            rule = self.rules[rule_id]
            del self.rules[rule_id]
            self.logger.info(f"Removed safety rule '{rule.name}'")
            return True
        return False
    
    async def enable_rule(self, rule_id: str) -> bool:
        """Enable a safety rule"""
        if rule_id in self.rules:
            self.rules[rule_id].enabled = True
            return True
        return False
    
    async def disable_rule(self, rule_id: str) -> bool:
        """Disable a safety rule"""
        if rule_id in self.rules:
            self.rules[rule_id].enabled = False
            return True
        return False
    
    def register_content_filter(self, check_type: str, filter_func: Callable) -> None:
        """Register a content filter function"""
        self.content_filters[check_type] = filter_func
        self.logger.info(f"Registered content filter for '{check_type}'")
    
    def register_behavior_monitor(self, monitor_type: str, monitor_func: Callable) -> None:
        """Register a behavior monitoring function"""
        self.behavior_monitors[monitor_type] = monitor_func
        self.logger.info(f"Registered behavior monitor for '{monitor_type}'")
    
    async def report_violation(self, 
                              violation_type: ViolationType,
                              message: str,
                              severity: SafetyLevel = SafetyLevel.MEDIUM,
                              context: Optional[Dict[str, Any]] = None,
                              source: str = "") -> str:
        """Manually report a safety violation"""
        violation = SafetyViolation(
            violation_type=violation_type,
            severity=severity,
            message=message,
            context=context or {},
            source=source
        )
        
        await self._process_violation(violation)
        return violation.id
    
    async def resolve_violation(self, violation_id: str, resolution_action: str) -> bool:
        """Mark a violation as resolved"""
        for violation in self.violations:
            if violation.id == violation_id:
                violation.resolved = True
                violation.resolution_action = resolution_action
                self.logger.info(f"Resolved violation {violation_id}: {resolution_action}")
                return True
        return False
    
    async def get_violations(self, 
                            severity: Optional[SafetyLevel] = None,
                            violation_type: Optional[ViolationType] = None,
                            resolved: Optional[bool] = None,
                            limit: int = 100) -> List[SafetyViolation]:
        """Get violations matching criteria"""
        filtered_violations = []
        
        for violation in self.violations:
            if severity and violation.severity != severity:
                continue
            if violation_type and violation.violation_type != violation_type:
                continue
            if resolved is not None and violation.resolved != resolved:
                continue
            
            filtered_violations.append(violation)
        
        # Sort by timestamp (most recent first)
        filtered_violations.sort(key=lambda v: v.timestamp, reverse=True)
        return filtered_violations[:limit]
    
    async def check_rate_limit(self, operation_type: str = "general") -> bool:
        """Check if operation is within rate limits"""
        now = datetime.now()
        
        # Clean old requests (keep only last minute)
        cutoff = now - timedelta(minutes=1)
        self.request_history = [ts for ts in self.request_history if ts > cutoff]
        
        # Check rate limit
        requests_per_minute = len(self.request_history)
        max_requests = self.resource_limits.get('max_requests_per_minute', 1000)
        
        if requests_per_minute >= max_requests:
            await self.report_violation(
                ViolationType.RESOURCE_ABUSE,
                f"Rate limit exceeded: {requests_per_minute}/{max_requests} requests per minute",
                SafetyLevel.HIGH,
                {'operation_type': operation_type, 'requests_count': requests_per_minute}
            )
            return False
        
        # Record this request
        self.request_history.append(now)
        return True
    
    async def check_operation_duration(self, operation_id: str, duration: float) -> bool:
        """Check if operation duration is within limits"""
        max_duration = self.resource_limits.get('max_operation_duration', 300)
        
        if duration > max_duration:
            await self.report_violation(
                ViolationType.INFINITE_LOOP,
                f"Operation duration exceeded: {duration:.2f}s > {max_duration}s",
                SafetyLevel.HIGH,
                {'operation_id': operation_id, 'duration': duration}
            )
            return False
        
        return True
    
    async def _setup_default_rules(self) -> None:
        """Setup default safety rules"""
        # Harmful content filter
        harmful_content_rule = SafetyRule(
            name="Harmful Content Filter",
            description="Block content that could be harmful or dangerous",
            rule_type="content_filter",
            pattern="harmful|dangerous|violence|weapons|illegal",
            action="block",
            severity=SafetyLevel.HIGH
        )
        await self.add_safety_rule(harmful_content_rule)
        
        # Privacy protection
        privacy_rule = SafetyRule(
            name="Privacy Protection",
            description="Prevent exposure of personal information",
            rule_type="content_filter",
            pattern="ssn|social security|credit card|password|email",
            action="block",
            severity=SafetyLevel.CRITICAL
        )
        await self.add_safety_rule(privacy_rule)
        
        # Resource usage limit
        resource_rule = SafetyRule(
            name="Resource Usage Limit",
            description="Prevent excessive resource consumption",
            rule_type="resource_monitor",
            action="warn",
            severity=SafetyLevel.MEDIUM
        )
        await self.add_safety_rule(resource_rule)
    
    async def _check_rule(self, rule: SafetyRule, check: SafetyCheck) -> Optional[SafetyViolation]:
        """Check a specific rule against content"""
        try:
            content_str = str(check.content).lower()
            
            if rule.rule_type == "content_filter" and rule.pattern:
                # Simple pattern matching (in real implementation, use regex or ML)
                if any(word in content_str for word in rule.pattern.lower().split('|')):
                    return SafetyViolation(
                        violation_type=ViolationType.HARMFUL_OUTPUT,
                        severity=rule.severity,
                        message=f"Content violated rule: {rule.name}",
                        context={'rule_id': rule.id, 'content_type': check.check_type},
                        triggered_rules=[rule.id],
                        source=check.context.get('source', 'unknown')
                    )
            
            elif rule.rule_type == "resource_monitor":
                # Check resource usage (placeholder)
                return None
            
        except Exception as e:
            self.logger.error(f"Error checking rule {rule.id}: {str(e)}")
        
        return None
    
    async def _run_content_filter(self, filter_func: Callable, 
                                 check: SafetyCheck) -> Optional[SafetyViolation]:
        """Run a content filter function"""
        try:
            result = filter_func(check.content, check.context)
            if result and isinstance(result, dict):
                return SafetyViolation(
                    violation_type=ViolationType(result.get('violation_type', 'harmful_output')),
                    severity=SafetyLevel(result.get('severity', SafetyLevel.MEDIUM.value)),
                    message=result.get('message', 'Content filter violation'),
                    context=result.get('context', {}),
                    source=check.context.get('source', 'content_filter')
                )
        except Exception as e:
            self.logger.error(f"Error running content filter: {str(e)}")
        
        return None
    
    async def _run_behavior_monitor(self, monitor_func: Callable, 
                                   check: SafetyCheck) -> Optional[SafetyViolation]:
        """Run a behavior monitoring function"""
        try:
            result = monitor_func(check.content, check.context)
            if result and isinstance(result, dict):
                return SafetyViolation(
                    violation_type=ViolationType(result.get('violation_type', 'unsafe_operation')),
                    severity=SafetyLevel(result.get('severity', SafetyLevel.MEDIUM.value)),
                    message=result.get('message', 'Behavior monitor violation'),
                    context=result.get('context', {}),
                    source=check.context.get('source', 'behavior_monitor')
                )
        except Exception as e:
            self.logger.error(f"Error running behavior monitor: {str(e)}")
        
        return None
    
    async def _process_violation(self, violation: SafetyViolation) -> None:
        """Process a safety violation"""
        # Add to violations list
        self.violations.append(violation)
        self.violation_history.append(violation)
        
        # Update counts
        self.violation_counts[violation.violation_type] += 1
        
        # Log violation
        self.logger.warning(f"Safety violation detected: {violation.message} "
                          f"(Type: {violation.violation_type.value}, "
                          f"Severity: {violation.severity.name})")
        
        # Check for emergency response
        if self.emergency_enabled:
            await self._check_emergency_response(violation)
        
        # Keep only recent violations
        if len(self.violations) > 1000:
            self.violations = self.violations[-500:]
    
    async def _check_emergency_response(self, violation: SafetyViolation) -> None:
        """Check if emergency response is needed"""
        # Count recent high-severity violations
        recent_time = datetime.now() - timedelta(minutes=5)
        recent_severe_violations = sum(
            1 for v in self.violations 
            if v.timestamp > recent_time and v.severity.value >= SafetyLevel.HIGH.value
        )
        
        if recent_severe_violations >= self.emergency_threshold:
            self.logger.critical(f"EMERGENCY: {recent_severe_violations} severe violations in 5 minutes")
            
            # Execute emergency actions
            for action in self.emergency_actions:
                if action == 'log':
                    self.logger.critical("Emergency logging activated")
                elif action == 'alert':
                    # In real implementation, send alerts to administrators
                    self.logger.critical("Emergency alert sent")
                elif action == 'shutdown':
                    # In real implementation, initiate safe shutdown
                    self.logger.critical("Emergency shutdown initiated")
    
    async def _resource_monitoring_loop(self) -> None:
        """Background task for resource monitoring"""
        while True:
            try:
                await asyncio.sleep(10)  # Check every 10 seconds
                await self._check_system_resources()
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in resource monitoring: {str(e)}")
    
    async def _violation_monitoring_loop(self) -> None:
        """Background task for violation pattern monitoring"""
        while True:
            try:
                await asyncio.sleep(60)  # Check every minute
                await self._analyze_violation_patterns()
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in violation monitoring: {str(e)}")
    
    async def _check_system_resources(self) -> None:
        """Check system resource usage"""
        # In a real implementation, this would check actual system resources
        # For now, it's a placeholder that could trigger resource abuse violations
        
        # Simulate memory check
        # if memory_usage > self.resource_limits['max_memory_mb']:
        #     await self.report_violation(
        #         ViolationType.MEMORY_OVERFLOW,
        #         f"Memory usage exceeded: {memory_usage}MB",
        #         SafetyLevel.HIGH
        #     )
        
        pass
    
    async def _analyze_violation_patterns(self) -> None:
        """Analyze patterns in violations for trends"""
        if len(self.violation_history) < 10:
            return
        
        # Analyze recent violations for patterns
        recent_violations = [v for v in self.violation_history 
                           if v.timestamp > datetime.now() - timedelta(hours=1)]
        
        if len(recent_violations) > 20:  # Many violations in short time
            await self.report_violation(
                ViolationType.UNSAFE_OPERATION,
                f"High violation rate detected: {len(recent_violations)} violations in 1 hour",
                SafetyLevel.HIGH,
                {'pattern': 'high_rate', 'violation_count': len(recent_violations)}
            )
    
    def get_safety_statistics(self) -> Dict[str, Any]:
        """Get comprehensive safety statistics"""
        total_violations = len(self.violations)
        
        if total_violations == 0:
            return {'total_violations': 0, 'monitoring_enabled': self.monitoring_enabled}
        
        # Count by type
        violation_type_counts = {vt.value: count for vt, count in self.violation_counts.items()}
        
        # Count by severity
        severity_counts = {}
        for violation in self.violations:
            severity_name = violation.severity.name
            severity_counts[severity_name] = severity_counts.get(severity_name, 0) + 1
        
        # Resolution rate
        resolved_count = sum(1 for v in self.violations if v.resolved)
        resolution_rate = resolved_count / total_violations if total_violations > 0 else 0
        
        return {
            'total_violations': total_violations,
            'resolved_violations': resolved_count,
            'resolution_rate': resolution_rate,
            'violation_types': violation_type_counts,
            'severity_distribution': severity_counts,
            'active_rules': len([r for r in self.rules.values() if r.enabled]),
            'total_rules': len(self.rules),
            'monitoring_enabled': self.monitoring_enabled,
            'emergency_enabled': self.emergency_enabled,
            'content_filters': len(self.content_filters),
            'behavior_monitors': len(self.behavior_monitors)
        }
    
    async def export_safety_data(self, file_path: str = None) -> Dict[str, Any]:
        """Export safety data"""
        rules_data = {}
        for rule_id, rule in self.rules.items():
            rules_data[rule_id] = {
                'id': rule.id,
                'name': rule.name,
                'description': rule.description,
                'rule_type': rule.rule_type,
                'pattern': rule.pattern,
                'action': rule.action,
                'severity': rule.severity.value,
                'enabled': rule.enabled,
                'created_at': rule.created_at.isoformat(),
                'metadata': rule.metadata
            }
        
        violations_data = [v.to_dict() for v in self.violations]
        
        export_data = {
            'rules': rules_data,
            'violations': violations_data,
            'violation_counts': {vt.value: count for vt, count in self.violation_counts.items()},
            'resource_limits': self.resource_limits,
            'statistics': self.get_safety_statistics(),
            'export_timestamp': datetime.now().isoformat()
        }
        
        if file_path:
            with open(file_path, 'w') as f:
                json.dump(export_data, f, indent=2)
        
        return export_data
