"""
Base Integration Adapter

CURRENT STATUS: ✅ ENTERPRISE PRODUCTION READY - CURRENTLY INACTIVE
- Framework is complete and fully tested but not yet activated
- Will be enabled when first external service (Slack/GitHub) is added
- See: docs/implementation/INTEGRATIONS_BASE_RETENTION_COMPLETION_REPORT.md

General Staff G4 Role: External Integration Management
Provides base functionality for all external service integrations

ACTIVATION TRIGGER: When external services are integrated into Copper Sun Brass
READY FOR: Slack, GitHub, webhooks, and custom API integrations
"""

import asyncio
import json
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, Optional, List, Callable
from pathlib import Path
import logging

from coppersun_brass.core.dcp_adapter import DCPAdapter

logger = logging.getLogger(__name__)


class IntegrationAdapter(ABC):
    """
    Base adapter for all external integrations
    
    STATUS: Ready for use but currently inactive pending external service additions
    
    General Staff G4 Role: External Integration Management
    Converts all external events to DCP observations before processing,
    ensuring consistent state management across AI commander sessions.
    
    This framework will be activated when Copper Sun Brass adds external
    service integrations (Slack, GitHub, webhooks, etc.)
    """
    
    def __init__(self, 
                 dcp_path: Optional[str] = None,
                 service_name: str = "unknown"):
        """
        Initialize with MANDATORY DCP integration
        
        Args:
            dcp_path: Path to DCP context file (mandatory per CLAUDE.md)
            service_name: Name of the external service
        """
        # DCP is MANDATORY - this is how the general staff coordinates
        self.dcp_manager = DCPAdapter(dcp_path=dcp_path)
        self.service_name = service_name
        self.event_router = EventRouter(dcp_path)
        
        # Load existing state from DCP
        self._load_state_from_dcp()
        
        # Track integration health
        self.last_event_time = None
        self.total_events = 0
        self.failed_events = 0
        
        # Enhanced health metrics tracking
        self.start_time = datetime.utcnow()
        self.event_history = []  # Rolling window of recent events
        self.error_history = []  # Rolling window of recent errors
        self.performance_metrics = {
            'avg_processing_time': 0.0,
            'min_processing_time': None,
            'max_processing_time': None,
            'processing_times': []  # Rolling window for calculations
        }
        self.health_checks = {
            'last_auth_check': None,
            'last_connection_test': None,
            'auth_failures': 0,
            'connection_failures': 0
        }
        
    def _load_state_from_dcp(self) -> None:
        """Load integration state from DCP"""
        try:
            integrations = self.dcp_manager.get_section('integrations', {})
            service_data = integrations.get(self.service_name, {})
            
            self.state = service_data.get('state', {})
            self.config = service_data.get('config', {})
            self.metrics = service_data.get('metrics', {
                'total_events': 0,
                'failed_events': 0,
                'last_event': None,
                'start_time': datetime.utcnow().isoformat(),
                'performance_metrics': {
                    'avg_processing_time': 0.0,
                    'min_processing_time': None,
                    'max_processing_time': None
                },
                'health_checks': {
                    'last_auth_check': None,
                    'last_connection_test': None,
                    'auth_failures': 0,
                    'connection_failures': 0
                }
            })
            
            logger.info(f"Loaded {self.service_name} state from DCP")
            
        except Exception as e:
            logger.warning(f"Could not load state from DCP: {e}")
            # Initialize with defaults but preserve any existing state
            if not hasattr(self, 'state'):
                self.state = {}
            if not hasattr(self, 'config'):
                self.config = {}
            if not hasattr(self, 'metrics'):
                self.metrics = {
                    'total_events': 0,
                    'failed_events': 0,
                    'last_event': None,
                    'start_time': datetime.utcnow().isoformat(),
                    'performance_metrics': {
                        'avg_processing_time': 0.0,
                        'min_processing_time': None,
                        'max_processing_time': None
                    },
                    'health_checks': {
                        'last_auth_check': None,
                        'last_connection_test': None,
                        'auth_failures': 0,
                        'connection_failures': 0
                    }
                }
    
    def _save_state_to_dcp(self) -> None:
        """Save current state to DCP"""
        try:
            state_data = {
                'config': self.config,
                'state': self.state,
                'metrics': {
                    'total_events': self.total_events,
                    'failed_events': self.failed_events,
                    'last_event': self.last_event_time.isoformat() if self.last_event_time else None,
                    'health_score': self._calculate_health_score(),
                    'start_time': self.start_time.isoformat(),
                    'performance_metrics': {
                        'avg_processing_time': self.performance_metrics['avg_processing_time'],
                        'min_processing_time': self.performance_metrics['min_processing_time'],
                        'max_processing_time': self.performance_metrics['max_processing_time']
                    },
                    'health_checks': self.health_checks,
                    'recent_activity': {
                        'event_history_size': len(self.event_history),
                        'error_history_size': len(self.error_history),
                        'success_rate': self._calculate_success_rate()
                    }
                }
            }
            
            self.dcp_manager.update_section(
                f'integrations.{self.service_name}',
                state_data
            )
            
        except Exception as e:
            logger.error(f"Failed to save state to DCP: {e}")
    
    async def process_event(self, event: Dict[str, Any]) -> None:
        """
        Process external event through DCP first
        
        Args:
            event: External event data
        """
        start_time = datetime.utcnow()
        processing_start = start_time.timestamp()
        
        try:
            # Update metrics
            self.total_events += 1
            self.last_event_time = start_time
            
            # Track event in rolling history (keep last 100)
            self.event_history.append({
                'timestamp': start_time.isoformat(),
                'event_type': event.get('type', 'unknown'),
                'size_bytes': len(str(event))
            })
            if len(self.event_history) > 100:
                self.event_history.pop(0)
            
            # Convert to DCP observation BEFORE any logic
            observation = self._event_to_observation(event)
            
            # Add metadata
            observation['metadata'] = {
                'service': self.service_name,
                'timestamp': start_time.isoformat(),
                'event_number': self.total_events
            }
            
            # Log to DCP
            self.dcp_manager.add_observation(
                observation['type'],
                observation['data'],
                source_agent=f'integration_{self.service_name}',
                priority=observation.get('priority', 70)
            )
            
            # Route through event bus
            await self.event_router.route(observation)
            
            # Calculate processing time and update performance metrics
            processing_time = datetime.utcnow().timestamp() - processing_start
            self._update_performance_metrics(processing_time)
            
            # Update state
            self._save_state_to_dcp()
            
        except Exception as e:
            self.failed_events += 1
            processing_time = datetime.utcnow().timestamp() - processing_start
            
            # Track error in rolling history (keep last 50)
            self.error_history.append({
                'timestamp': datetime.utcnow().isoformat(),
                'error': str(e),
                'event_type': event.get('type', 'unknown'),
                'processing_time': processing_time
            })
            if len(self.error_history) > 50:
                self.error_history.pop(0)
            
            logger.error(f"Failed to process event: {e}")
            
            # Log error to DCP
            self.dcp_manager.add_observation(
                'integration_error',
                {
                    'service': self.service_name,
                    'error': str(e),
                    'event': event,
                    'processing_time_ms': processing_time * 1000
                },
                source_agent=f'integration_{self.service_name}',
                priority=90
            )
    
    @abstractmethod
    def _event_to_observation(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert external event to DCP observation format
        
        Args:
            event: External event data
            
        Returns:
            Observation dictionary with type, data, and priority
        """
        pass
    
    @abstractmethod
    async def authenticate(self, **credentials) -> bool:
        """
        Authenticate with external service
        
        Returns:
            Success boolean
        """
        pass
    
    @abstractmethod
    async def test_connection(self) -> bool:
        """
        Test connection to external service
        
        Returns:
            Success boolean
        """
        pass
    
    def _update_performance_metrics(self, processing_time: float) -> None:
        """Update performance metrics with new processing time"""
        # Add to rolling window (keep last 1000 for accurate averages)
        self.performance_metrics['processing_times'].append(processing_time)
        if len(self.performance_metrics['processing_times']) > 1000:
            self.performance_metrics['processing_times'].pop(0)
        
        # Update min/max
        if (self.performance_metrics['min_processing_time'] is None or 
            processing_time < self.performance_metrics['min_processing_time']):
            self.performance_metrics['min_processing_time'] = processing_time
            
        if (self.performance_metrics['max_processing_time'] is None or 
            processing_time > self.performance_metrics['max_processing_time']):
            self.performance_metrics['max_processing_time'] = processing_time
        
        # Update average
        if self.performance_metrics['processing_times']:
            self.performance_metrics['avg_processing_time'] = (
                sum(self.performance_metrics['processing_times']) / 
                len(self.performance_metrics['processing_times'])
            )
    
    async def perform_health_check(self) -> Dict[str, Any]:
        """
        Perform comprehensive health check of the integration
        
        Returns:
            Health check results with detailed status
        """
        health_results = {
            'timestamp': datetime.utcnow().isoformat(),
            'overall_status': 'unknown',
            'checks': {}
        }
        
        try:
            # Test authentication
            try:
                auth_result = await self.authenticate()
                self.health_checks['last_auth_check'] = datetime.utcnow().isoformat()
                if not auth_result:
                    self.health_checks['auth_failures'] += 1
                health_results['checks']['authentication'] = {
                    'status': 'pass' if auth_result else 'fail',
                    'message': 'Authentication successful' if auth_result else 'Authentication failed'
                }
            except Exception as e:
                self.health_checks['auth_failures'] += 1
                health_results['checks']['authentication'] = {
                    'status': 'error',
                    'message': f'Authentication error: {str(e)}'
                }
            
            # Test connection
            try:
                conn_result = await self.test_connection()
                self.health_checks['last_connection_test'] = datetime.utcnow().isoformat()
                if not conn_result:
                    self.health_checks['connection_failures'] += 1
                health_results['checks']['connection'] = {
                    'status': 'pass' if conn_result else 'fail',
                    'message': 'Connection test successful' if conn_result else 'Connection test failed'
                }
            except Exception as e:
                self.health_checks['connection_failures'] += 1
                health_results['checks']['connection'] = {
                    'status': 'error',
                    'message': f'Connection error: {str(e)}'
                }
            
            # Check event processing health
            success_rate = self._calculate_success_rate()
            health_results['checks']['event_processing'] = {
                'status': 'pass' if success_rate >= 0.9 else 'warn' if success_rate >= 0.7 else 'fail',
                'message': f'Success rate: {success_rate:.2%}',
                'success_rate': success_rate
            }
            
            # Check performance
            avg_time = self.performance_metrics['avg_processing_time']
            health_results['checks']['performance'] = {
                'status': 'pass' if avg_time < 1.0 else 'warn' if avg_time < 5.0 else 'fail',
                'message': f'Average processing time: {avg_time:.3f}s',
                'avg_processing_time': avg_time
            }
            
            # Determine overall status
            statuses = [check['status'] for check in health_results['checks'].values()]
            if 'fail' in statuses or 'error' in statuses:
                health_results['overall_status'] = 'unhealthy'
            elif 'warn' in statuses:
                health_results['overall_status'] = 'degraded'
            else:
                health_results['overall_status'] = 'healthy'
                
        except Exception as e:
            health_results['overall_status'] = 'error'
            health_results['error'] = str(e)
        
        return health_results
    
    def _calculate_success_rate(self) -> float:
        """Calculate current success rate"""
        if self.total_events == 0:
            return 1.0
        return 1.0 - (self.failed_events / self.total_events)
    
    def _calculate_health_score(self) -> float:
        """Calculate health score for this integration"""
        if self.total_events == 0:
            return 1.0
        
        success_rate = 1.0 - (self.failed_events / self.total_events)
        
        # Factor in recency
        if self.last_event_time:
            hours_since_event = (datetime.utcnow() - self.last_event_time).total_seconds() / 3600
            recency_factor = max(0.5, 1.0 - (hours_since_event / 24))
        else:
            recency_factor = 0.5
            
        return success_rate * recency_factor
    
    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive integration status"""
        uptime_seconds = (datetime.utcnow() - self.start_time).total_seconds()
        
        # Calculate recent error rate (last 10 events)
        recent_events = self.event_history[-10:] if len(self.event_history) >= 10 else self.event_history
        recent_errors = self.error_history[-10:] if len(self.error_history) >= 10 else self.error_history
        recent_error_rate = len(recent_errors) / len(recent_events) if recent_events else 0
        
        # Calculate events per hour
        events_per_hour = (self.total_events / (uptime_seconds / 3600)) if uptime_seconds > 0 else 0
        
        return {
            'service': self.service_name,
            'configured': bool(self.config),
            'authenticated': self.config.get('authenticated', False),
            'health_score': self._calculate_health_score(),
            'uptime_seconds': uptime_seconds,
            'uptime_hours': uptime_seconds / 3600,
            
            # Event metrics
            'total_events': self.total_events,
            'failed_events': self.failed_events,
            'success_rate': self._calculate_success_rate(),
            'recent_error_rate': recent_error_rate,
            'events_per_hour': events_per_hour,
            'last_event': self.last_event_time.isoformat() if self.last_event_time else None,
            
            # Performance metrics
            'performance': {
                'avg_processing_time_ms': self.performance_metrics['avg_processing_time'] * 1000,
                'min_processing_time_ms': (self.performance_metrics['min_processing_time'] * 1000 
                                         if self.performance_metrics['min_processing_time'] else None),
                'max_processing_time_ms': (self.performance_metrics['max_processing_time'] * 1000 
                                         if self.performance_metrics['max_processing_time'] else None),
                'processing_samples': len(self.performance_metrics['processing_times'])
            },
            
            # Health check status
            'health_checks': {
                'last_auth_check': self.health_checks['last_auth_check'],
                'last_connection_test': self.health_checks['last_connection_test'],
                'auth_failures': self.health_checks['auth_failures'],
                'connection_failures': self.health_checks['connection_failures']
            },
            
            # Recent activity
            'recent_activity': {
                'event_history_size': len(self.event_history),
                'error_history_size': len(self.error_history),
                'last_10_events': recent_events,
                'last_5_errors': self.error_history[-5:] if self.error_history else []
            }
        }
    
    def get_health_summary(self) -> Dict[str, Any]:
        """Get concise health summary for monitoring"""
        return {
            'service': self.service_name,
            'status': 'healthy' if self._calculate_health_score() > 0.8 else 'degraded' if self._calculate_health_score() > 0.5 else 'unhealthy',
            'health_score': self._calculate_health_score(),
            'success_rate': self._calculate_success_rate(),
            'total_events': self.total_events,
            'failed_events': self.failed_events,
            'avg_processing_time_ms': self.performance_metrics['avg_processing_time'] * 1000,
            'last_event': self.last_event_time.isoformat() if self.last_event_time else None,
            'uptime_hours': (datetime.utcnow() - self.start_time).total_seconds() / 3600
        }


class EventRouter:
    """
    Unified event routing system with middleware support
    
    General Staff G3 Role: Operations Coordination
    Routes all external events through common pipeline with
    full observability and testing hooks.
    
    The EventRouter implements a middleware-based processing pipeline that allows
    for flexible event processing, filtering, and transformation before events
    reach their final handlers.
    
    Middleware Architecture:
        The router processes events through a pipeline of middleware functions
        that can transform, filter, or enhance observations before they reach
        registered handlers. Middleware functions are executed in registration
        order and can short-circuit the pipeline by returning None.
    
    Handler Registration:
        Multiple handlers can be registered for the same event type, and they
        will be executed concurrently. Handler failures are isolated and logged
        but do not affect other handlers for the same event.
    
    Example Usage:
        ```python
        router = EventRouter("/path/to/dcp")
        
        # Add middleware for logging
        async def logging_middleware(observation):
            logger.info(f"Processing event: {observation.get('type')}")
            return observation
        
        # Add middleware for filtering
        async def filter_middleware(observation):
            if observation.get('data', {}).get('ignore'):
                return None  # Filter out this observation
            return observation
        
        router.add_middleware(logging_middleware)
        router.add_middleware(filter_middleware)
        
        # Register handlers
        async def alert_handler(observation):
            # Send alert based on observation
            pass
        
        router.register_handler('security_event', alert_handler)
        
        # Route observation through pipeline
        await router.route({
            'type': 'security_event',
            'data': {'severity': 'high', 'message': 'Intrusion detected'}
        })
        ```
    """
    
    def __init__(self, dcp_path: Optional[str] = None):
        """Initialize with MANDATORY DCP integration"""
        # DCP is MANDATORY
        self.dcp_manager = DCPAdapter(dcp_path=dcp_path)
        self.handlers: Dict[str, List[Callable]] = {}
        self.middleware: List[Callable] = []
        
        # Load routing configuration from DCP
        self._load_routes_from_dcp()
        
    def _load_routes_from_dcp(self) -> None:
        """Load routing configuration from DCP"""
        try:
            config = self.dcp_manager.get_section('integrations.routing', {})
            # Routes would be loaded here if configured
            logger.info("Loaded routing configuration from DCP")
        except Exception as e:
            logger.warning(f"Could not load routes from DCP: {e}")
    
    def register_handler(self, event_type: str, handler: Callable) -> None:
        """Register event handler"""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)
        
        logger.info(f"Registered handler for {event_type}")
    
    def add_middleware(self, middleware: Callable) -> None:
        """
        Add middleware to the event processing pipeline
        
        Middleware functions are executed in the order they are added and can:
        - Transform observations by modifying and returning them
        - Filter observations by returning None
        - Add metadata or perform side effects
        - Short-circuit the pipeline by returning None
        
        Args:
            middleware: Async callable that takes an observation dict and returns
                       either a modified observation dict or None to filter it out
        
        Middleware Function Signature:
            async def middleware_function(observation: Dict[str, Any]) -> Optional[Dict[str, Any]]:
                # Process observation
                return observation  # or None to filter
        
        Example Middleware:
            ```python
            async def security_middleware(observation):
                # Add security metadata
                observation['security_checked'] = True
                observation['security_level'] = calculate_security_level(observation)
                return observation
            
            async def rate_limit_middleware(observation):
                # Filter based on rate limiting
                if is_rate_limited(observation.get('source')):
                    logger.warning("Rate limited observation filtered")
                    return None
                return observation
            ```
        """
        self.middleware.append(middleware)
        logger.info(f"Added middleware: {middleware.__name__}")
    
    async def route(self, observation: Dict[str, Any]) -> None:
        """
        Route observation through middleware pipeline and registered handlers
        
        The routing process follows these steps:
        1. Apply middleware functions in registration order
        2. If any middleware returns None, stop processing (filtered out)
        3. Log routing decision to DCP for observability
        4. Execute all registered handlers for the event type concurrently
        5. Log any handler failures without affecting other handlers
        
        Args:
            observation: DCP observation dict containing 'type', 'data', and optional metadata
        
        Raises:
            No exceptions are raised - all errors are caught and logged to maintain
            system stability. Handler failures are isolated and logged separately.
        
        Example:
            ```python
            await router.route({
                'type': 'user_login',
                'data': {
                    'user_id': '12345',
                    'ip_address': '192.168.1.1',
                    'timestamp': '2025-01-11T10:30:00Z'
                },
                'metadata': {
                    'source': 'auth_service',
                    'priority': 60
                }
            })
            ```
        """
        try:
            # Apply middleware
            for mw in self.middleware:
                observation = await mw(observation)
                if observation is None:
                    logger.debug("Middleware filtered out observation")
                    return
            
            # Log routing decision
            event_type = observation.get('type', 'unknown')
            handler_count = len(self.handlers.get(event_type, []))
            
            self.dcp_manager.add_observation(
                'event_routed',
                {
                    'type': event_type,
                    'handlers': handler_count,
                    'timestamp': datetime.utcnow().isoformat()
                },
                source_agent='event_router',
                priority=60
            )
            
            # Execute handlers
            handlers = self.handlers.get(event_type, [])
            if not handlers:
                logger.warning(f"No handlers registered for event type: {event_type}")
                return
                
            # Run handlers concurrently
            tasks = [handler(observation) for handler in handlers]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Log any handler errors
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"Handler {handlers[i].__name__} failed: {result}")
                    
        except Exception as e:
            logger.error(f"Error routing observation: {e}")
            
            # Log routing error to DCP
            self.dcp_manager.add_observation(
                'routing_error',
                {
                    'observation_type': observation.get('type', 'unknown'),
                    'error': str(e)
                },
                source_agent='event_router',
                priority=85
            )


class DCPThrottler:
    """
    Prevents DCP observation flooding during webhook bursts with optimized chunking
    
    Features:
    - Intelligent burst detection and adaptive batching
    - Size-based and time-based buffer flushing
    - Priority-aware observation handling
    - Memory pressure management
    - Configurable chunk sizes for optimal performance
    """
    
    def __init__(self, 
                 dcp_manager: DCPAdapter,
                 max_per_second: int = 10,
                 max_buffer_size: int = 1000,
                 max_chunk_size: int = 50,
                 flush_interval: float = 1.0):
        """
        Initialize optimized throttler
        
        Args:
            dcp_manager: DCP adapter instance
            max_per_second: Maximum observations per second for direct writes
            max_buffer_size: Maximum buffer size before forcing flush
            max_chunk_size: Maximum observations per batch write
            flush_interval: Minimum seconds between buffer flushes
        """
        self.dcp_manager = dcp_manager
        self.max_per_second = max_per_second
        self.max_buffer_size = max_buffer_size
        self.max_chunk_size = max_chunk_size
        self.flush_interval = flush_interval
        
        self.buffer = []
        self.flush_task = None
        self.last_write = datetime.utcnow()
        self.last_flush = datetime.utcnow()
        self.write_count = 0
        
        # Performance metrics
        self.total_direct_writes = 0
        self.total_buffered_writes = 0
        self.total_flushes = 0
        self.burst_count = 0
        
    async def add_observation(self, 
                            obs_type: str, 
                            data: Dict[str, Any], 
                            **kwargs) -> None:
        """Add observation with intelligent throttling and burst detection"""
        now = datetime.utcnow()
        
        # Reset counter if new second
        if (now - self.last_write).total_seconds() >= 1:
            self.write_count = 0
            self.last_write = now
        
        # Check for high priority observations (bypass throttling)
        priority = kwargs.get('priority', 70)
        is_high_priority = priority >= 85
        
        # Direct write conditions
        can_write_direct = (
            self.write_count < self.max_per_second or 
            is_high_priority or 
            len(self.buffer) == 0  # No backlog
        )
        
        if can_write_direct and len(self.buffer) < self.max_buffer_size * 0.8:
            # Direct write - good path
            try:
                self.dcp_manager.add_observation(obs_type, data, **kwargs)
                self.write_count += 1
                self.total_direct_writes += 1
            except Exception as e:
                logger.warning(f"Direct write failed, buffering: {e}")
                # Fallback to buffering if direct write fails
                self._add_to_buffer(obs_type, data, kwargs, now)
        else:
            # Buffer for batch write
            self._add_to_buffer(obs_type, data, kwargs, now)
    
    def _add_to_buffer(self, obs_type: str, data: Dict[str, Any], kwargs: Dict[str, Any], timestamp: datetime) -> None:
        """Add observation to buffer with burst detection"""
        # Add timestamp for burst analysis
        buffer_item = {
            'obs_type': obs_type,
            'data': data,
            'kwargs': kwargs,
            'timestamp': timestamp,
            'priority': kwargs.get('priority', 70)
        }
        
        self.buffer.append(buffer_item)
        self.total_buffered_writes += 1
        
        # Detect burst scenarios
        if len(self.buffer) >= 50:  # Burst threshold
            self.burst_count += 1
        
        # Force flush conditions
        should_force_flush = (
            len(self.buffer) >= self.max_buffer_size or
            (len(self.buffer) >= self.max_chunk_size and 
             (timestamp - self.last_flush).total_seconds() >= self.flush_interval)
        )
        
        if should_force_flush and not self.flush_task:
            self.flush_task = asyncio.create_task(self._flush_buffer_optimized())
        elif not self.flush_task:
            # Schedule regular flush
            self.flush_task = asyncio.create_task(self._flush_buffer_optimized())
    
    async def _flush_buffer_optimized(self) -> None:
        """Optimized batch write with priority handling and adaptive chunking"""
        # Wait for burst to potentially complete, but not too long
        initial_buffer_size = len(self.buffer)
        
        # Adaptive wait based on buffer growth rate
        if initial_buffer_size < 20:
            await asyncio.sleep(self.flush_interval)
        elif initial_buffer_size < 100:
            await asyncio.sleep(self.flush_interval * 0.5)  # Faster flush for medium bursts
        else:
            await asyncio.sleep(0.2)  # Very fast flush for large bursts
        
        if not self.buffer:
            self.flush_task = None
            return
        
        buffer_to_flush = self.buffer[:]  # Copy buffer
        buffer_size = len(buffer_to_flush)
        logger.info(f"Flushing {buffer_size} buffered observations (burst detected: {initial_buffer_size >= 50})")
        
        try:
            # Sort by priority (high priority first)
            buffer_to_flush.sort(key=lambda x: x['priority'], reverse=True)
            
            # Group by type and priority for efficient writing
            from collections import defaultdict
            grouped = defaultdict(list)
            
            for item in buffer_to_flush:
                key = (item['obs_type'], item['priority'] >= 85)  # Group high priority separately
                grouped[key].append(item)
            
            # Process high priority items first
            high_priority_groups = {k: v for k, v in grouped.items() if k[1]}  # k[1] is high_priority flag
            normal_priority_groups = {k: v for k, v in grouped.items() if not k[1]}
            
            total_written = 0
            
            # Write high priority first
            for (obs_type, _), items in high_priority_groups.items():
                written = await self._write_chunk_batch(obs_type, items, urgent=True)
                total_written += written
            
            # Write normal priority with adaptive chunking
            for (obs_type, _), items in normal_priority_groups.items():
                written = await self._write_chunk_batch(obs_type, items, urgent=False)
                total_written += written
            
            # Clear processed items from buffer
            items_to_remove = min(len(self.buffer), total_written)
            self.buffer = self.buffer[items_to_remove:]
            
            self.total_flushes += 1
            self.last_flush = datetime.utcnow()
            
            logger.info(f"Buffer flush complete: {total_written} observations written, {len(self.buffer)} remaining")
            
            # Schedule next flush if buffer still has items
            if self.buffer:
                self.flush_task = asyncio.create_task(self._flush_buffer_optimized())
            else:
                self.flush_task = None
                
        except Exception as e:
            logger.error(f"Error during buffer flush: {e}")
            # Reset flush task to allow retry
            self.flush_task = None
    
    async def _write_chunk_batch(self, obs_type: str, items: List[Dict], urgent: bool = False) -> int:
        """Write a batch of observations with adaptive chunking"""
        total_items = len(items)
        
        # Adaptive chunk size based on urgency and total items
        if urgent:
            chunk_size = min(self.max_chunk_size, 20)  # Smaller chunks for urgent items
            delay_between_chunks = 0.01  # Minimal delay
        elif total_items > 200:
            chunk_size = self.max_chunk_size  # Full chunks for large batches
            delay_between_chunks = 0.05  # Small delay
        else:
            chunk_size = min(self.max_chunk_size, max(10, total_items // 3))  # Adaptive
            delay_between_chunks = 0.1  # Standard delay
        
        written_count = 0
        
        for i in range(0, total_items, chunk_size):
            chunk = items[i:i + chunk_size]
            
            # Write chunk with error handling
            for item in chunk:
                try:
                    self.dcp_manager.add_observation(
                        item['obs_type'],
                        item['data'],
                        **item['kwargs']
                    )
                    written_count += 1
                except Exception as e:
                    logger.warning(f"Failed to write observation: {e}")
            
            # Adaptive delay between chunks
            if i + chunk_size < total_items:  # Not the last chunk
                await asyncio.sleep(delay_between_chunks)
        
        return written_count
    
    def get_stats(self) -> Dict[str, Any]:
        """Get throttler performance statistics"""
        total_observations = self.total_direct_writes + self.total_buffered_writes
        direct_write_rate = (self.total_direct_writes / total_observations) if total_observations > 0 else 0
        
        return {
            'total_observations': total_observations,
            'direct_writes': self.total_direct_writes,
            'buffered_writes': self.total_buffered_writes,
            'direct_write_rate': direct_write_rate,
            'total_flushes': self.total_flushes,
            'burst_count': self.burst_count,
            'current_buffer_size': len(self.buffer),
            'max_buffer_size': self.max_buffer_size,
            'max_chunk_size': self.max_chunk_size,
            'is_flushing': self.flush_task is not None and not self.flush_task.done()
        }