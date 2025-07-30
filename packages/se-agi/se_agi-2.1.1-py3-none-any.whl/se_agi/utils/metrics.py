"""
Metrics collection and monitoring for SE-AGI
Provides comprehensive system and performance metrics
"""

import asyncio
import logging
import time
import threading
from typing import Dict, List, Optional, Any, Callable, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict, deque
import json
import uuid
from enum import Enum


class MetricType(Enum):
    """Types of metrics"""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    TIMER = "timer"
    RATE = "rate"


@dataclass
class MetricPoint:
    """A single metric data point"""
    timestamp: datetime
    value: Union[int, float]
    tags: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'timestamp': self.timestamp.isoformat(),
            'value': self.value,
            'tags': self.tags,
            'metadata': self.metadata
        }


@dataclass
class Metric:
    """Represents a metric with its configuration and data points"""
    name: str
    metric_type: MetricType
    description: str = ""
    unit: str = ""
    tags: Dict[str, str] = field(default_factory=dict)
    data_points: deque = field(default_factory=lambda: deque(maxlen=1000))
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    
    def add_point(self, value: Union[int, float], tags: Optional[Dict[str, str]] = None):
        """Add a data point to the metric"""
        point = MetricPoint(
            timestamp=datetime.now(),
            value=value,
            tags={**self.tags, **(tags or {})}
        )
        self.data_points.append(point)
        self.last_updated = datetime.now()
    
    def get_latest_value(self) -> Optional[Union[int, float]]:
        """Get the latest metric value"""
        if self.data_points:
            return self.data_points[-1].value
        return None
    
    def get_average(self, time_window: Optional[timedelta] = None) -> Optional[float]:
        """Get average value within time window"""
        if not self.data_points:
            return None
        
        if time_window is None:
            values = [point.value for point in self.data_points]
        else:
            cutoff = datetime.now() - time_window
            values = [point.value for point in self.data_points if point.timestamp > cutoff]
        
        return sum(values) / len(values) if values else None
    
    def get_min_max(self, time_window: Optional[timedelta] = None) -> Optional[tuple]:
        """Get min and max values within time window"""
        if not self.data_points:
            return None
        
        if time_window is None:
            values = [point.value for point in self.data_points]
        else:
            cutoff = datetime.now() - time_window
            values = [point.value for point in self.data_points if point.timestamp > cutoff]
        
        return (min(values), max(values)) if values else None


class Timer:
    """Context manager for timing operations"""
    
    def __init__(self, metrics_collector: 'MetricsCollector', metric_name: str, tags: Optional[Dict[str, str]] = None):
        self.metrics_collector = metrics_collector
        self.metric_name = metric_name
        self.tags = tags or {}
        self.start_time = None
        self.end_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        duration = self.end_time - self.start_time
        self.metrics_collector.record_timer(self.metric_name, duration, self.tags)


class MetricsCollector:
    """
    Comprehensive metrics collection and monitoring system
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize metrics collector"""
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Metrics storage
        self.metrics: Dict[str, Metric] = {}
        
        # Collection settings
        self.enabled = self.config.get('enabled', True)
        self.collection_interval = self.config.get('collection_interval', 60)  # seconds
        self.retention_period = timedelta(days=self.config.get('retention_days', 7))
        
        # Background collection
        self.collection_tasks: List[asyncio.Task] = []
        self.background_collectors: Dict[str, Callable] = {}
        
        # System metrics
        self.system_metrics_enabled = self.config.get('system_metrics', True)
        
        # Performance tracking
        self.operation_timers: Dict[str, float] = {}
        self.rate_counters: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        
        # Alerting
        self.alert_thresholds: Dict[str, Dict[str, float]] = {}
        self.alert_callbacks: Dict[str, List[Callable]] = defaultdict(list)
        
        # Thread safety
        self.lock = threading.RLock()
        
        self._setup_default_metrics()
        self.logger.info("MetricsCollector initialized")
    
    def start_collection(self) -> None:
        """Start background metrics collection"""
        if not self.enabled:
            return
        
        # Start system metrics collection if enabled
        if self.system_metrics_enabled:
            self.collection_tasks.append(
                asyncio.create_task(self._system_metrics_loop())
            )
        
        # Start background collectors
        for name, collector in self.background_collectors.items():
            self.collection_tasks.append(
                asyncio.create_task(self._background_collector_loop(name, collector))
            )
        
        # Start cleanup task
        self.collection_tasks.append(
            asyncio.create_task(self._cleanup_loop())
        )
        
        self.logger.info("Metrics collection started")
    
    def stop_collection(self) -> None:
        """Stop background metrics collection"""
        for task in self.collection_tasks:
            task.cancel()
        
        self.collection_tasks.clear()
        self.logger.info("Metrics collection stopped")
    
    def record_counter(self, name: str, value: Union[int, float] = 1, 
                      tags: Optional[Dict[str, str]] = None, 
                      description: str = "") -> None:
        """Record a counter metric"""
        if not self.enabled:
            return
        
        with self.lock:
            metric = self._get_or_create_metric(name, MetricType.COUNTER, description)
            
            # For counters, add to the current value
            current_value = metric.get_latest_value() or 0
            metric.add_point(current_value + value, tags)
    
    def record_gauge(self, name: str, value: Union[int, float], 
                    tags: Optional[Dict[str, str]] = None, 
                    description: str = "") -> None:
        """Record a gauge metric"""
        if not self.enabled:
            return
        
        with self.lock:
            metric = self._get_or_create_metric(name, MetricType.GAUGE, description)
            metric.add_point(value, tags)
    
    def record_histogram(self, name: str, value: Union[int, float], 
                        tags: Optional[Dict[str, str]] = None, 
                        description: str = "") -> None:
        """Record a histogram metric"""
        if not self.enabled:
            return
        
        with self.lock:
            metric = self._get_or_create_metric(name, MetricType.HISTOGRAM, description)
            metric.add_point(value, tags)
    
    def record_timer(self, name: str, duration: float, 
                    tags: Optional[Dict[str, str]] = None, 
                    description: str = "") -> None:
        """Record a timer metric"""
        if not self.enabled:
            return
        
        with self.lock:
            metric = self._get_or_create_metric(name, MetricType.TIMER, description, "seconds")
            metric.add_point(duration, tags)
    
    def record_rate(self, name: str, count: Union[int, float] = 1, 
                   tags: Optional[Dict[str, str]] = None, 
                   description: str = "") -> None:
        """Record a rate metric (events per second)"""
        if not self.enabled:
            return
        
        with self.lock:
            # Add to rate counter
            self.rate_counters[name].append(datetime.now())
            
            # Calculate current rate (events per second in last minute)
            now = datetime.now()
            cutoff = now - timedelta(minutes=1)
            recent_events = [ts for ts in self.rate_counters[name] if ts > cutoff]
            rate = len(recent_events) / 60.0  # events per second
            
            metric = self._get_or_create_metric(name, MetricType.RATE, description, "events/sec")
            metric.add_point(rate, tags)
    
    def time_operation(self, name: str, tags: Optional[Dict[str, str]] = None) -> Timer:
        """Get a timer context manager for timing operations"""
        return Timer(self, name, tags)
    
    def start_timer(self, name: str) -> None:
        """Start a named timer"""
        self.operation_timers[name] = time.time()
    
    def end_timer(self, name: str, tags: Optional[Dict[str, str]] = None) -> float:
        """End a named timer and record the duration"""
        if name not in self.operation_timers:
            self.logger.warning(f"Timer '{name}' was not started")
            return 0.0
        
        start_time = self.operation_timers.pop(name)
        duration = time.time() - start_time
        self.record_timer(name, duration, tags)
        return duration
    
    def increment(self, name: str, value: Union[int, float] = 1, 
                 tags: Optional[Dict[str, str]] = None) -> None:
        """Increment a counter metric"""
        self.record_counter(name, value, tags)
    
    def set_gauge(self, name: str, value: Union[int, float], 
                 tags: Optional[Dict[str, str]] = None) -> None:
        """Set a gauge metric value"""
        self.record_gauge(name, value, tags)
    
    def get_metric(self, name: str) -> Optional[Metric]:
        """Get a metric by name"""
        with self.lock:
            return self.metrics.get(name)
    
    def get_metric_value(self, name: str) -> Optional[Union[int, float]]:
        """Get the latest value of a metric"""
        metric = self.get_metric(name)
        return metric.get_latest_value() if metric else None
    
    def get_metric_stats(self, name: str, time_window: Optional[timedelta] = None) -> Optional[Dict[str, Any]]:
        """Get statistics for a metric"""
        metric = self.get_metric(name)
        if not metric:
            return None
        
        stats = {
            'name': name,
            'type': metric.metric_type.value,
            'latest_value': metric.get_latest_value(),
            'data_points_count': len(metric.data_points)
        }
        
        if metric.data_points:
            stats['average'] = metric.get_average(time_window)
            min_max = metric.get_min_max(time_window)
            if min_max:
                stats['min'], stats['max'] = min_max
        
        return stats
    
    def get_all_metrics(self) -> Dict[str, Any]:
        """Get all metrics with their current values"""
        with self.lock:
            result = {}
            for name, metric in self.metrics.items():
                result[name] = {
                    'value': metric.get_latest_value(),
                    'type': metric.metric_type.value,
                    'description': metric.description,
                    'unit': metric.unit,
                    'last_updated': metric.last_updated.isoformat()
                }
            return result
    
    def register_background_collector(self, name: str, collector_func: Callable) -> None:
        """Register a background collector function"""
        self.background_collectors[name] = collector_func
        self.logger.info(f"Registered background collector: {name}")
    
    def set_alert_threshold(self, metric_name: str, threshold_type: str, value: float) -> None:
        """Set an alert threshold for a metric"""
        if metric_name not in self.alert_thresholds:
            self.alert_thresholds[metric_name] = {}
        
        self.alert_thresholds[metric_name][threshold_type] = value
        self.logger.info(f"Set {threshold_type} threshold for {metric_name}: {value}")
    
    def register_alert_callback(self, metric_name: str, callback: Callable) -> None:
        """Register a callback for metric alerts"""
        self.alert_callbacks[metric_name].append(callback)
        self.logger.info(f"Registered alert callback for {metric_name}")
    
    def collect_system_metrics(self, system_obj: Any = None) -> Dict[str, Any]:
        """Collect system-wide metrics"""
        metrics = {}
        
        try:
            # Memory metrics
            import psutil
            memory = psutil.virtual_memory()
            metrics['system.memory.used_percent'] = memory.percent
            metrics['system.memory.available_mb'] = memory.available / 1024 / 1024
            
            # CPU metrics
            metrics['system.cpu.usage_percent'] = psutil.cpu_percent(interval=1)
            metrics['system.cpu.load_avg'] = psutil.getloadavg()[0] if hasattr(psutil, 'getloadavg') else 0
            
            # Disk metrics
            disk = psutil.disk_usage('/')
            metrics['system.disk.used_percent'] = (disk.used / disk.total) * 100
            metrics['system.disk.free_gb'] = disk.free / 1024 / 1024 / 1024
            
            # Process metrics
            process = psutil.Process()
            metrics['process.memory.rss_mb'] = process.memory_info().rss / 1024 / 1024
            metrics['process.cpu.percent'] = process.cpu_percent()
            metrics['process.threads'] = process.num_threads()
            
        except ImportError:
            self.logger.debug("psutil not available for system metrics")
        except Exception as e:
            self.logger.error(f"Error collecting system metrics: {e}")
        
        # SE-AGI specific metrics
        if system_obj:
            try:
                metrics['seagi.agents.count'] = len(getattr(system_obj, 'agents', {}))
                metrics['seagi.active_tasks'] = len(getattr(system_obj, 'active_tasks', {}))
                metrics['seagi.completed_tasks'] = len(getattr(system_obj, 'completed_tasks', []))
                metrics['seagi.generation'] = getattr(system_obj, 'generation', 0)
                metrics['seagi.uptime_seconds'] = (
                    datetime.now() - getattr(system_obj, 'start_time', datetime.now())
                ).total_seconds()
            except Exception as e:
                self.logger.error(f"Error collecting SE-AGI metrics: {e}")
        
        # Record all metrics
        for name, value in metrics.items():
            if isinstance(value, (int, float)):
                self.record_gauge(name, value)
        
        return metrics
    
    def _get_or_create_metric(self, name: str, metric_type: MetricType, 
                             description: str = "", unit: str = "") -> Metric:
        """Get existing metric or create new one"""
        if name not in self.metrics:
            self.metrics[name] = Metric(
                name=name,
                metric_type=metric_type,
                description=description,
                unit=unit
            )
        
        return self.metrics[name]
    
    def _setup_default_metrics(self) -> None:
        """Setup default system metrics"""
        default_metrics = [
            ('system.memory.used_percent', MetricType.GAUGE, 'Memory usage percentage', '%'),
            ('system.cpu.usage_percent', MetricType.GAUGE, 'CPU usage percentage', '%'),
            ('system.disk.used_percent', MetricType.GAUGE, 'Disk usage percentage', '%'),
            ('process.memory.rss_mb', MetricType.GAUGE, 'Process RSS memory', 'MB'),
            ('seagi.requests.count', MetricType.COUNTER, 'Total requests processed', 'requests'),
            ('seagi.requests.rate', MetricType.RATE, 'Request rate', 'requests/sec'),
            ('seagi.response.time', MetricType.TIMER, 'Response time', 'seconds'),
            ('seagi.errors.count', MetricType.COUNTER, 'Total errors', 'errors'),
        ]
        
        for name, metric_type, description, unit in default_metrics:
            self._get_or_create_metric(name, metric_type, description, unit)
    
    async def _system_metrics_loop(self) -> None:
        """Background loop for collecting system metrics"""
        while True:
            try:
                await asyncio.sleep(self.collection_interval)
                self.collect_system_metrics()
                await self._check_alerts()
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in system metrics loop: {e}")
    
    async def _background_collector_loop(self, name: str, collector_func: Callable) -> None:
        """Background loop for custom collectors"""
        while True:
            try:
                await asyncio.sleep(self.collection_interval)
                
                if asyncio.iscoroutinefunction(collector_func):
                    await collector_func(self)
                else:
                    collector_func(self)
                    
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in background collector '{name}': {e}")
    
    async def _cleanup_loop(self) -> None:
        """Background loop for cleaning up old metrics"""
        while True:
            try:
                await asyncio.sleep(3600)  # Run every hour
                await self._cleanup_old_data()
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in cleanup loop: {e}")
    
    async def _cleanup_old_data(self) -> None:
        """Clean up old metric data"""
        cutoff_time = datetime.now() - self.retention_period
        
        with self.lock:
            for metric in self.metrics.values():
                # Create new deque with only recent data points
                recent_points = deque(
                    [point for point in metric.data_points if point.timestamp > cutoff_time],
                    maxlen=metric.data_points.maxlen
                )
                metric.data_points = recent_points
        
        self.logger.debug("Cleaned up old metric data")
    
    async def _check_alerts(self) -> None:
        """Check metrics against alert thresholds"""
        for metric_name, thresholds in self.alert_thresholds.items():
            metric = self.get_metric(metric_name)
            if not metric:
                continue
            
            current_value = metric.get_latest_value()
            if current_value is None:
                continue
            
            # Check thresholds
            for threshold_type, threshold_value in thresholds.items():
                alert_triggered = False
                
                if threshold_type == 'max' and current_value > threshold_value:
                    alert_triggered = True
                elif threshold_type == 'min' and current_value < threshold_value:
                    alert_triggered = True
                
                if alert_triggered:
                    # Trigger callbacks
                    for callback in self.alert_callbacks[metric_name]:
                        try:
                            if asyncio.iscoroutinefunction(callback):
                                await callback(metric_name, current_value, threshold_type, threshold_value)
                            else:
                                callback(metric_name, current_value, threshold_type, threshold_value)
                        except Exception as e:
                            self.logger.error(f"Error in alert callback: {e}")
    
    def get_summary_statistics(self) -> Dict[str, Any]:
        """Get summary statistics for all metrics"""
        with self.lock:
            stats = {
                'total_metrics': len(self.metrics),
                'metrics_by_type': {},
                'data_points_total': 0,
                'collection_enabled': self.enabled,
                'retention_days': self.retention_period.days
            }
            
            for metric in self.metrics.values():
                metric_type = metric.metric_type.value
                stats['metrics_by_type'][metric_type] = stats['metrics_by_type'].get(metric_type, 0) + 1
                stats['data_points_total'] += len(metric.data_points)
            
            return stats
    
    def export_metrics(self, format: str = 'json', time_window: Optional[timedelta] = None) -> str:
        """Export metrics in specified format"""
        with self.lock:
            if format.lower() == 'json':
                return self._export_json(time_window)
            elif format.lower() == 'prometheus':
                return self._export_prometheus(time_window)
            else:
                raise ValueError(f"Unsupported export format: {format}")
    
    def _export_json(self, time_window: Optional[timedelta] = None) -> str:
        """Export metrics in JSON format"""
        export_data = {
            'timestamp': datetime.now().isoformat(),
            'time_window': time_window.total_seconds() if time_window else None,
            'metrics': {}
        }
        
        for name, metric in self.metrics.items():
            if time_window:
                cutoff = datetime.now() - time_window
                data_points = [
                    point.to_dict() for point in metric.data_points 
                    if point.timestamp > cutoff
                ]
            else:
                data_points = [point.to_dict() for point in metric.data_points]
            
            export_data['metrics'][name] = {
                'type': metric.metric_type.value,
                'description': metric.description,
                'unit': metric.unit,
                'data_points': data_points
            }
        
        return json.dumps(export_data, indent=2)
    
    def _export_prometheus(self, time_window: Optional[timedelta] = None) -> str:
        """Export metrics in Prometheus format"""
        lines = []
        
        for name, metric in self.metrics.items():
            # Convert metric name to Prometheus format
            prom_name = name.replace('.', '_').replace('-', '_')
            
            # Add help and type comments
            if metric.description:
                lines.append(f"# HELP {prom_name} {metric.description}")
            
            if metric.metric_type == MetricType.COUNTER:
                lines.append(f"# TYPE {prom_name} counter")
            elif metric.metric_type == MetricType.GAUGE:
                lines.append(f"# TYPE {prom_name} gauge")
            
            # Add latest value
            latest_value = metric.get_latest_value()
            if latest_value is not None:
                lines.append(f"{prom_name} {latest_value}")
        
        return '\n'.join(lines)
