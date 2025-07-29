"""
Test DCPAdapter API Compatibility

Tests backward compatibility between DCPManager and DCPAdapter APIs to ensure
the migration works correctly with both old and new calling styles.
"""

import pytest
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
import sys
import os

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from coppersun_brass.core.dcp_adapter import DCPAdapter
from coppersun_brass.core.storage import BrassStorage


class TestDCPAdapterCompatibility:
    """Test DCPAdapter backward compatibility with DCPManager API."""
    
    @pytest.fixture
    def temp_storage(self):
        """Create temporary storage for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "test.db"
            storage = BrassStorage(db_path)
            yield storage
    
    @pytest.fixture
    def adapter(self, temp_storage):
        """Create DCPAdapter instance for testing."""
        return DCPAdapter(storage=temp_storage)
    
    def test_add_observation_dcpmanager_style_with_positional_agent(self, adapter):
        """Test old DCPManager style: add_observation({'type': 'x', ...}, 'agent')"""
        obs_dict = {
            'type': 'startup_time',
            'agent': 'strategist',
            'duration_ms': 1500,
            'is_cold_start': True,
            'priority': 75
        }
        
        # Call in DCPManager style
        result = adapter.add_observation(obs_dict, 'strategist')
        
        # Should return string ID for compatibility
        assert isinstance(result, str)
        assert result is not None
        
        # Verify observation was stored
        observations = adapter.get_observations()
        assert len(observations) == 1
        assert observations[0]['obs_type'] == 'startup_time'
        assert observations[0]['source_agent'] == 'strategist'
    
    def test_add_observation_dcpmanager_style_with_kwarg_agent(self, adapter):
        """Test old DCPManager style: add_observation({'type': 'x', ...}, source_agent='agent')"""
        obs_dict = {
            'type': 'gap_detection',
            'capability': 'authentication',
            'risk_score': 85,
            'priority': 60
        }
        
        # Call in DCPManager style with kwarg
        result = adapter.add_observation(obs_dict, source_agent='gap_detector')
        
        assert isinstance(result, str)
        assert result is not None
        
        observations = adapter.get_observations()
        assert len(observations) == 1
        assert observations[0]['obs_type'] == 'gap_detection'
        assert observations[0]['source_agent'] == 'gap_detector'
    
    def test_add_observation_dcpadapter_style_positional(self, adapter):
        """Test new DCPAdapter style: add_observation(obs_type, data, source_agent, priority)"""
        data = {'message': 'test data', 'confidence': 0.95}
        
        result = adapter.add_observation('test_type', data, 'test_agent', 80)
        
        assert isinstance(result, str)
        assert result is not None
        
        observations = adapter.get_observations()
        assert len(observations) == 1
        assert observations[0]['obs_type'] == 'test_type'
        assert observations[0]['source_agent'] == 'test_agent'
        assert observations[0]['data']['message'] == 'test data'
    
    def test_add_observation_dcpadapter_style_kwargs(self, adapter):
        """Test new DCPAdapter style with kwargs: add_observation(obs_type='x', data={}, ...)"""
        data = {'analysis': 'performance data'}
        
        result = adapter.add_observation(
            obs_type='performance_analysis',
            data=data,
            source_agent='performance_monitor',
            priority=70
        )
        
        assert isinstance(result, str)
        assert result is not None
        
        observations = adapter.get_observations()
        assert len(observations) == 1
        assert observations[0]['obs_type'] == 'performance_analysis'
        assert observations[0]['source_agent'] == 'performance_monitor'
    
    def test_get_observations_no_filters(self, adapter):
        """Test DCPManager style: get_observations() with no filters"""
        # Add some test data
        adapter.add_observation('type1', {'data': 'test1'}, 'agent1')
        adapter.add_observation('type2', {'data': 'test2'}, 'agent2')
        
        # Get all observations
        observations = adapter.get_observations()
        
        assert len(observations) == 2
        obs_types = [obs['obs_type'] for obs in observations]
        assert 'type1' in obs_types
        assert 'type2' in obs_types
    
    def test_get_observations_dcpmanager_filter_dict(self, adapter):
        """Test DCPManager style: get_observations({'type': 'x', 'since': cutoff})"""
        # Add test data
        adapter.add_observation('feedback_entry', {'rating': 5}, 'user')
        adapter.add_observation('startup_time', {'duration': 100}, 'system')
        
        # Filter by type using DCPManager style
        filters = {'type': 'feedback_entry'}
        observations = adapter.get_observations(filters)
        
        assert len(observations) == 1
        assert observations[0]['obs_type'] == 'feedback_entry'
        assert observations[0]['data']['rating'] == 5
    
    def test_get_observations_dcpmanager_filters_kwarg(self, adapter):
        """Test DCPManager style: get_observations(filters={'type': 'x'})"""
        # Add test data
        adapter.add_observation('api_call', {'endpoint': '/test'}, 'api_server')
        adapter.add_observation('user_action', {'action': 'click'}, 'frontend')
        
        # Filter using filters kwarg
        observations = adapter.get_observations(filters={'type': 'api_call'})
        
        assert len(observations) == 1
        assert observations[0]['obs_type'] == 'api_call'
        assert observations[0]['data']['endpoint'] == '/test'
    
    def test_get_observations_dcpadapter_style(self, adapter):
        """Test new DCPAdapter style: get_observations(source_agent='x', obs_type='y')"""
        # Add test data
        adapter.add_observation('metric', {'cpu': 80}, 'monitor1')
        adapter.add_observation('metric', {'memory': 60}, 'monitor2')
        adapter.add_observation('alert', {'level': 'warning'}, 'monitor1')
        
        # Filter by agent and type
        observations = adapter.get_observations(source_agent='monitor1', obs_type='metric')
        
        assert len(observations) == 1
        assert observations[0]['obs_type'] == 'metric'
        assert observations[0]['source_agent'] == 'monitor1'
        assert observations[0]['data']['cpu'] == 80
    
    def test_get_observations_with_since_filter(self, adapter):
        """Test time-based filtering works in both styles"""
        cutoff = datetime.utcnow() - timedelta(minutes=5)
        
        # Add observation
        adapter.add_observation('time_test', {'timestamp': 'now'}, 'timer')
        
        # Test DCPManager style with since
        observations = adapter.get_observations({'since': cutoff})
        assert len(observations) == 1
        
        # Test DCPAdapter style with since
        observations = adapter.get_observations(since=cutoff)
        assert len(observations) == 1
    
    def test_mixed_api_styles_in_sequence(self, adapter):
        """Test that both API styles can be used in the same session"""
        # Add observation using old style
        old_result = adapter.add_observation(
            {'type': 'old_style', 'data': 'test'}, 
            'old_agent'
        )
        
        # Add observation using new style
        new_result = adapter.add_observation(
            obs_type='new_style',
            data={'data': 'test'},
            source_agent='new_agent'
        )
        
        # Both should work
        assert isinstance(old_result, str)
        assert isinstance(new_result, str)
        
        # Get observations using old style
        old_style_obs = adapter.get_observations({'type': 'old_style'})
        assert len(old_style_obs) == 1
        
        # Get observations using new style
        new_style_obs = adapter.get_observations(obs_type='new_style')
        assert len(new_style_obs) == 1
        
        # Get all observations with no filters
        all_obs = adapter.get_observations()
        assert len(all_obs) == 2
    
    def test_error_handling_graceful_degradation(self, adapter):
        """Test that errors are handled gracefully without crashing"""
        # Test with malformed observation dict
        result = adapter.add_observation({}, 'test_agent')
        assert result is None or isinstance(result, str)
        
        # Test with empty filters
        observations = adapter.get_observations({})
        assert isinstance(observations, list)
        
        # Test with invalid filter types
        observations = adapter.get_observations({'invalid_key': 'value'})
        assert isinstance(observations, list)
    
    def test_return_type_compatibility(self, adapter):
        """Test that return types match DCPManager expectations"""
        # add_observation should return string (not int)
        result = adapter.add_observation('test', {'data': 'test'}, 'agent')
        assert isinstance(result, str), f"Expected str, got {type(result)}"
        
        # get_observations should return list of dicts
        observations = adapter.get_observations()
        assert isinstance(observations, list)
        if observations:
            assert isinstance(observations[0], dict)
    
    def test_observation_dict_extraction(self, adapter):
        """Test that observation type is correctly extracted from various dict formats"""
        # Test 'type' key
        result1 = adapter.add_observation({'type': 'test1'}, 'agent')
        assert result1 is not None
        
        # Test 'observation_type' key  
        result2 = adapter.add_observation({'observation_type': 'test2'}, 'agent')
        assert result2 is not None
        
        # Test missing type (should default to 'unknown')
        result3 = adapter.add_observation({'data': 'no_type'}, 'agent')
        assert result3 is not None
        
        # Verify all were stored
        observations = adapter.get_observations()
        assert len(observations) == 3
        
        obs_types = [obs['obs_type'] for obs in observations]
        assert 'test1' in obs_types
        assert 'test2' in obs_types
        assert 'unknown' in obs_types


class TestRealWorldUsagePatterns:
    """Test actual usage patterns found in migrated code."""
    
    @pytest.fixture
    def adapter(self):
        """Create DCPAdapter instance for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "test.db"
            storage = BrassStorage(db_path)
            yield DCPAdapter(storage=storage)
    
    def test_strategist_agent_startup_pattern(self, adapter):
        """Test the exact pattern used in strategist_agent.py"""
        # This is the actual code from strategist_agent.py:259
        result = adapter.add_observation({
            'type': 'startup_time',
            'agent': 'strategist',
            'duration_ms': 1500,
            'is_cold_start': True,
            'observations_loaded': 100,
            'context_categories': ['capability_assessment'],
            'components_initialized': 5
        }, source_agent='strategist')
        
        assert result is not None
        assert isinstance(result, str)
        
        # Verify it was stored correctly
        observations = adapter.get_observations()
        assert len(observations) == 1
        assert observations[0]['obs_type'] == 'startup_time'
        assert observations[0]['source_agent'] == 'strategist'
    
    def test_feedback_collector_pattern(self, adapter):
        """Test the exact pattern used in feedback_collector.py"""
        # Pattern from feedback_collector.py:153
        observations = adapter.get_observations({
            'type': 'recommendation_registry'
        })
        assert isinstance(observations, list)
        
        # Pattern from feedback_collector.py:215
        observation = {
            'type': 'recommendation_registry',
            'priority': 30,
            'summary': 'Test registry',
            'details': {'test': 'data'}
        }
        result = adapter.add_observation(observation, 'feedback_collector')
        assert result is not None
        
        # Verify the filter works
        filtered = adapter.get_observations({
            'type': 'recommendation_registry'
        })
        assert len(filtered) == 1
    
    def test_gap_detector_pattern(self, adapter):
        """Test the exact pattern used in gap_detector.py"""
        # Pattern from gap_detector.py:595
        observation = {
            'type': 'file_analysis',
            'priority': 75,
            'summary': 'Gap analysis complete',
            'details': {
                'gap_analysis_id': 'test_123',
                'total_gaps': 5,
                'critical_gaps': 2
            }
        }
        
        result = adapter.add_observation(observation, source_agent='gap_detector')
        assert result is not None
        assert isinstance(result, str)


if __name__ == "__main__":
    # Run tests if called directly
    pytest.main([__file__, "-v"])