"""
DCP Adapter - Makes existing agents work with new SQLite storage

This adapter provides a DCPManager-compatible interface while using the
new SQLite storage backend. This allows us to fix the agents with minimal changes.
"""
from pathlib import Path
from typing import Dict, List, Any, Optional
import json
import logging
import threading
from datetime import datetime
from contextlib import contextmanager

from .storage import BrassStorage

logger = logging.getLogger(__name__)


class DCPAdapter:
    """Adapter that mimics DCPManager interface but uses SQLite storage.
    
    This allows existing agents to work with minimal changes - just replace
    DCPManager with DCPAdapter in their __init__ methods.
    """
    
    def __init__(self, storage: Optional[BrassStorage] = None, 
                 dcp_path: Optional[str] = None):
        """Initialize adapter with storage backend.
        
        Supports both old DCPManager and new DCPAdapter calling conventions:
        
        Old style (DCPManager compatibility):
            DCPAdapter("/path/to/dcp")  # First arg is string path
            DCPAdapter(dcp_path="/path/to/dcp")  # Named path argument
            
        New style (DCPAdapter preferred):
            DCPAdapter(storage=brass_storage)  # BrassStorage object
            DCPAdapter()  # Use default storage
        
        Args:
            storage: BrassStorage instance (preferred) OR legacy path string
            dcp_path: Legacy parameter for compatibility
        """
        # Handle backward compatibility with old DCPManager calling convention
        if isinstance(storage, str):
            # Old style: DCPAdapter("/path/to/dcp") - first arg is path string
            logger.debug(f"DCPAdapter called with legacy path string: {storage}")
            dcp_path = storage
            storage = None
        elif storage is not None and not hasattr(storage, 'add_observation'):
            # Safety check: if storage doesn't look like BrassStorage, treat as path
            logger.warning(f"DCPAdapter received non-BrassStorage object, treating as path: {storage}")
            dcp_path = str(storage)
            storage = None
            
        if storage is None:
            # Create default storage if not provided
            from ..config import BrassConfig
            config = BrassConfig()
            
            # Use provided path or default
            if dcp_path:
                # Convert path to storage location
                from pathlib import Path
                path_obj = Path(dcp_path)
                if path_obj.is_dir():
                    # If directory provided, use default filename
                    db_path = path_obj / "brass_storage.db"
                else:
                    # If file provided, use as-is (with .db extension if missing)
                    db_path = path_obj.with_suffix('.db') if not path_obj.suffix else path_obj
            else:
                # Use default from config
                db_path = config.db_path
                
            storage = BrassStorage(db_path)
            logger.debug(f"Created BrassStorage at: {db_path}")
            
        self.storage = storage
        self._context_cache = {}
        self._lock = threading.RLock()  # Reentrant lock for thread safety
        
        # Log that we're using the adapter
        logger.info("Using DCPAdapter for SQLite-based storage")
    
    def add_observation(self, *args, **kwargs):
        """Add observation to storage with backward compatibility.
        
        Supports both DCPManager and DCPAdapter API styles:
        
        DCPManager style (old):
            add_observation({'type': 'startup_time', 'data': {...}}, source_agent='agent')
            add_observation({'type': 'startup_time', 'data': {...}}, 'agent')
            
        DCPAdapter style (new):
            add_observation(obs_type='startup_time', data={...}, source_agent='agent', priority=50)
            
        Returns:
            String observation ID for compatibility (converts from int)
        """
        try:
            # Detect calling style by examining first argument
            if len(args) >= 1 and isinstance(args[0], dict):
                # Old DCPManager style: first arg is observation dictionary
                obs_dict = args[0]
                
                # Extract source_agent from args or kwargs
                if len(args) >= 2:
                    source_agent = args[1]
                else:
                    source_agent = kwargs.get('source_agent', 'unknown')
                
                # Extract observation details from dict
                obs_type = obs_dict.get('type', obs_dict.get('observation_type', 'unknown'))
                priority = obs_dict.get('priority', 50)
                
                # For old style, the entire dict becomes the data
                data = obs_dict
                
                logger.debug(f"DCPManager-style add_observation call: type={obs_type}, agent={source_agent}")
                
            else:
                # New DCPAdapter style: use individual parameters
                if len(args) >= 3:
                    obs_type, data, source_agent = args[0], args[1], args[2]
                    priority = args[3] if len(args) >= 4 else kwargs.get('priority', 50)
                else:
                    obs_type = args[0] if len(args) >= 1 else kwargs.get('obs_type', 'unknown')
                    data = args[1] if len(args) >= 2 else kwargs.get('data', {})
                    source_agent = kwargs.get('source_agent', 'unknown')
                    priority = kwargs.get('priority', 50)
                
                logger.debug(f"DCPAdapter-style add_observation call: type={obs_type}, agent={source_agent}")
            
            # Call the underlying storage with the new API
            obs_id = self.storage.add_observation(
                obs_type=obs_type,
                data=data,
                source_agent=source_agent,
                priority=priority
            )
            
            logger.debug(f"Added observation {obs_id}: {obs_type} from {source_agent}")
            
            # Convert int ID to string for DCPManager compatibility
            return str(obs_id) if obs_id is not None else None
            
        except Exception as e:
            logger.error(f"Failed to add observation: {e}")
            # Don't raise - agents should continue working
            return None
    
    def update_metadata(self, updates: Dict[str, Any]) -> None:
        """Update context metadata (compatibility method).
        
        Args:
            updates: Metadata updates to apply
        """
        try:
            # Store as context snapshot
            current = self.storage.get_latest_context_snapshot('metadata') or {}
            current.update(updates)
            current['last_updated'] = datetime.utcnow().isoformat()
            
            self.storage.save_context_snapshot('metadata', current)
            
            # Update cache
            self._context_cache.update(updates)
            
        except Exception as e:
            logger.error(f"Failed to update metadata: {e}")
    
    def get_observations(self, *args, **kwargs) -> List[Dict[str, Any]]:
        """Get observations with filters and backward compatibility.
        
        Supports both DCPManager and DCPAdapter API styles:
        
        DCPManager style (old):
            get_observations()  # No filters
            get_observations({'type': 'feedback_entry', 'since': cutoff, 'limit': 100})
            get_observations(filters={'type': 'feedback_entry'})
            
        DCPAdapter style (new):
            get_observations(source_agent='agent', obs_type='type', since=datetime)
            
        Returns:
            List of observation dictionaries
        """
        try:
            # Detect calling style
            if len(args) == 0 and len(kwargs) == 0:
                # No arguments - return all observations (DCPManager style)
                logger.debug("DCPManager-style get_observations call: no filters")
                return self.storage.get_observations(processed=False)
                
            elif len(args) == 1 and isinstance(args[0], dict):
                # Old DCPManager style: filters dictionary
                filters = args[0]
                logger.debug(f"DCPManager-style get_observations call: filters={filters}")
                
                # Extract common filter fields
                source_agent = filters.get('agent', filters.get('source_agent'))
                obs_type = filters.get('type', filters.get('obs_type', filters.get('observation_type')))
                since = filters.get('since')
                limit = filters.get('limit', 1000)  # Default limit if not specified
                
            elif 'filters' in kwargs:
                # DCPManager style with filters kwarg
                filters = kwargs['filters']
                logger.debug(f"DCPManager-style get_observations call: filters kwarg={filters}")
                
                source_agent = filters.get('agent', filters.get('source_agent'))
                obs_type = filters.get('type', filters.get('obs_type', filters.get('observation_type')))
                since = filters.get('since')
                limit = filters.get('limit', 1000)  # Default limit if not specified
                
            else:
                # New DCPAdapter style: individual parameters
                logger.debug("DCPAdapter-style get_observations call")
                source_agent = args[0] if len(args) >= 1 else kwargs.get('source_agent')
                obs_type = args[1] if len(args) >= 2 else kwargs.get('obs_type')
                since = args[2] if len(args) >= 3 else kwargs.get('since')
                limit = kwargs.get('limit', 1000)  # Default limit if not specified
            
            
            # Call the underlying storage
            result = self.storage.get_observations(
                source_agent=source_agent,
                obs_type=obs_type,
                since=since,
                limit=limit,
                processed=False  # Only unprocessed by default
            )
            
            # Convert field names for compatibility: 'type' -> 'obs_type'
            compatible_result = []
            for obs in result:
                compatible_obs = obs.copy()
                # Add obs_type field for DCPManager compatibility
                if 'type' in compatible_obs:
                    compatible_obs['obs_type'] = compatible_obs['type']
                compatible_result.append(compatible_obs)
            
            logger.debug(f"Retrieved {len(compatible_result)} observations")
            return compatible_result
            
        except Exception as e:
            logger.error(f"Failed to get observations: {e}")
            return []
    
    def read_dcp(self, validate: bool = True) -> Dict[str, Any]:
        """Read DCP context (compatibility method).
        
        This method provides compatibility with DCPManager interface by calling
        the existing load_context() method. The validate parameter is accepted
        for compatibility but ignored since DCPAdapter uses SQLite storage.
        
        Args:
            validate: Validation flag (ignored for compatibility)
            
        Returns:
            Context dictionary with observations and metadata
        """
        try:
            logger.debug(f"read_dcp() called with validate={validate} (parameter ignored)")
            return self.load_context()
        except Exception as e:
            logger.error(f"Failed to read DCP context: {e}")
            return {'observations': [], 'metadata': {}, 'version': '2.0'}
    
    def load_context(self) -> Dict[str, Any]:
        """Load context (compatibility method).
        
        Returns:
            Context dictionary with observations and metadata
        """
        try:
            # Get recent observations
            observations = self.storage.get_observations(limit=100)
            
            # Get latest metadata
            metadata = self.storage.get_latest_context_snapshot('metadata') or {}
            
            # Get project info
            project_info = self.storage.get_latest_context_snapshot('project_info') or {}
            
            context = {
                'observations': observations,
                'metadata': metadata,
                'project_info': project_info,
                'version': '2.0'  # Indicate new storage version
            }
            
            return context
            
        except Exception as e:
            logger.error(f"Failed to load context: {e}")
            return {'observations': [], 'metadata': {}, 'version': '2.0'}
    
    def get_section(self, section: str, default: Any = None) -> Any:
        """Get a specific section from context (compatibility method).
        
        Args:
            section: Section name (e.g., 'metadata', 'project_info')
            default: Default value if section not found
            
        Returns:
            Section data or default
        """
        try:
            if section == 'observations':
                return self.storage.get_observations(limit=100)
            elif section == 'metadata':
                return self.storage.get_latest_context_snapshot('metadata') or default
            elif section == 'project_info':
                return self.storage.get_latest_context_snapshot('project_info') or default
            else:
                # Check if it's a nested path (e.g., 'metadata.version')
                parts = section.split('.')
                data = self.load_context()
                
                for part in parts:
                    if isinstance(data, dict) and part in data:
                        data = data[part]
                    else:
                        return default
                        
                return data
                
        except Exception as e:
            logger.error(f"Failed to get section {section}: {e}")
            return default
    
    def update_section(self, section: str, data: Any) -> None:
        """Update a specific section (compatibility method).
        
        Args:
            section: Section name to update
            data: New data for the section
        """
        try:
            # Handle different section types
            if section.startswith('observations'):
                # Can't directly update observations - log warning
                logger.warning("Cannot update observations section directly")
                
            elif section in ['metadata', 'project_info']:
                # Save as context snapshot
                self.storage.save_context_snapshot(section, data)
                
            else:
                # Handle nested paths
                if '.' in section:
                    # For nested updates, load current context, update, and save
                    parts = section.split('.')
                    root_section = parts[0]
                    
                    if root_section in ['metadata', 'project_info']:
                        current = self.storage.get_latest_context_snapshot(root_section) or {}
                        
                        # Navigate to nested location
                        target = current
                        for part in parts[1:-1]:
                            if part not in target:
                                target[part] = {}
                            target = target[part]
                            
                        # Set the value
                        target[parts[-1]] = data
                        
                        # Save updated snapshot
                        self.storage.save_context_snapshot(root_section, current)
                        
        except Exception as e:
            logger.error(f"Failed to update section {section}: {e}")
    
    def get_project_type(self) -> str:
        """Get detected project type (compatibility method).
        
        Returns:
            Project type string
        """
        project_info = self.get_section('project_info', {})
        return project_info.get('project_type', 'unknown')
    
    def get_recent_changes(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent file changes (compatibility method).
        
        Args:
            limit: Maximum number of changes to return
            
        Returns:
            List of file change observations
        """
        return self.storage.get_observations(
            obs_type='file_modified',
            limit=limit
        )
    
    def get_current_sprint(self) -> str:
        """Get current sprint identifier (compatibility method).
        
        Returns:
            Sprint identifier or 'unknown'
        """
        metadata = self.get_section('metadata', {})
        return metadata.get('current_sprint', 'unknown')
    
    def get_patterns_for_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Get patterns detected in a specific file.
        
        Args:
            file_path: File to get patterns for
            
        Returns:
            List of patterns
        """
        try:
            all_patterns = self.storage.get_patterns()
            return [
                p for p in all_patterns 
                if p.get('file_path') == str(file_path)
            ]
        except Exception as e:
            logger.error(f"Failed to get patterns for {file_path}: {e}")
            return []
    
    def get_complexity_history(self, file_path: Path) -> List[int]:
        """Get complexity history for a file.
        
        Args:
            file_path: File to get history for
            
        Returns:
            List of complexity values (most recent last)
        """
        try:
            # For now, return current complexity as single-item list
            # Could be enhanced to track history over time
            metrics = self.storage.get_file_metrics()
            for metric in metrics:
                if metric['file_path'] == str(file_path):
                    return [metric.get('complexity', 0)]
            return []
            
        except Exception as e:
            logger.error(f"Failed to get complexity history: {e}")
            return []
    
    def get_file_change_patterns(self) -> List[Dict[str, Any]]:
        """Get patterns of files that change together.
        
        Returns:
            List of file change correlation patterns
        """
        try:
            # Get file change observations
            changes = self.storage.get_observations(
                obs_type='file_modified',
                limit=1000
            )
            
            # Group by timestamp proximity (simplified)
            # In production, would use more sophisticated correlation
            patterns = []
            
            # Group changes within 5-minute windows
            from collections import defaultdict
            time_groups = defaultdict(list)
            
            for change in changes:
                # Round to 5-minute window
                timestamp = change['created_at']
                if isinstance(timestamp, str):
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                else:
                    dt = timestamp
                    
                window = dt.replace(minute=(dt.minute // 5) * 5, second=0, microsecond=0)
                time_groups[window].append(change['data'].get('file', ''))
            
            # Find files that frequently change together
            for window, files in time_groups.items():
                if len(files) > 1:
                    patterns.append({
                        'files': list(set(files)),
                        'correlation': 0.8,  # Simplified
                        'occurrences': 1
                    })
                    
            return patterns
            
        except Exception as e:
            logger.error(f"Failed to get file change patterns: {e}")
            return []
    
    def cleanup(self):
        """Cleanup old data (maintenance method)."""
        try:
            self.storage.cleanup_old_data(days=30)
            logger.info("Cleaned up old data")
        except Exception as e:
            logger.error(f"Failed to cleanup: {e}")
    
    @contextmanager
    def lock(self):
        """Provide thread-safe lock context (mimics DCPManager.lock()).
        
        Usage:
            with dcp_adapter.lock():
                # Thread-safe operations here
                pass
        """
        with self._lock:
            yield
    
    def add_observations(self, observations: List[Dict[str, Any]], 
                        source_agent: str = "unknown") -> Dict[str, int]:
        """Add multiple observations in batch (mimics DCPManager.add_observations()).
        
        Args:
            observations: List of observation dictionaries
            source_agent: Agent creating the observations
            
        Returns:
            Dictionary with 'succeeded' and 'failed' counts
        """
        succeeded = 0
        failed = 0
        
        for obs in observations:
            try:
                # Extract observation data from the expected format
                obs_type = obs.get('observation_type', 'unknown')
                data = obs.get('data', obs)  # Use 'data' field or entire obs
                priority = obs.get('priority', 50)
                
                # Add the observation
                obs_id = self.add_observation(
                    obs_type=obs_type,
                    data=data,
                    source_agent=source_agent,
                    priority=priority
                )
                
                if obs_id is not None:
                    succeeded += 1
                else:
                    failed += 1
                    
            except Exception as e:
                logger.error(f"Failed to add observation: {e}")
                failed += 1
        
        logger.info(f"Batch observation storage: {succeeded} succeeded, {failed} failed")
        return {
            'succeeded': succeeded,
            'failed': failed
        }
    
    # Convenience properties for backward compatibility
    @property
    def dcp_path(self) -> str:
        """Legacy property for compatibility."""
        return str(self.storage.db_path)
    
    def __repr__(self) -> str:
        """String representation."""
        return f"DCPAdapter(storage={self.storage.db_path})"