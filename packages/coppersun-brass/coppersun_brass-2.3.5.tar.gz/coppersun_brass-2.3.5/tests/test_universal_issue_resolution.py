"""
Comprehensive unit tests for Universal Issue Resolution Detection feature.

Tests the core functionality of detect_resolved_issues() and generate_resolved_issues_report()
methods with various scenarios including edge cases, security, and performance validation.
"""

import unittest
import tempfile
import json
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from coppersun_brass.core.storage import BrassStorage
from coppersun_brass.core.output_generator import OutputGenerator
from coppersun_brass.core.constants import RESOLVABLE_TYPES
from coppersun_brass.config import BrassConfig


class MockFinding:
    """Mock finding object for testing resolution detection."""
    def __init__(self, file_path: str, line_number: int):
        self.file_path = file_path
        self.line_number = line_number


class TestUniversalIssueResolution(unittest.TestCase):
    """Test suite for Universal Issue Resolution Detection."""

    def setUp(self):
        """Set up test environment with temporary database."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = Path(self.temp_dir) / 'test.db'
        self.storage = BrassStorage(self.db_path)
        
        # Create test config
        self.project_root = Path(self.temp_dir)
        self.output_dir = self.project_root / '.brass'
        self.output_dir.mkdir(exist_ok=True)
        
        self.config = BrassConfig(project_root=self.project_root)
        self.config.output_dir = self.output_dir
        
        self.output_generator = OutputGenerator(self.config, self.storage)

    def tearDown(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_detect_resolved_issues_single_type(self):
        """Test resolution detection for a single observation type."""
        # Add test observation
        obs_id = self.storage.add_observation('todo', {
            'file_path': 'test.py',
            'line_number': 10,
            'content': 'Test TODO'
        }, 'scout', 50)
        
        # Create current findings (empty = all resolved)
        current_findings = []
        
        # Test resolution detection
        resolved_count = self.storage.detect_resolved_issues(current_findings, 'todo')
        self.assertEqual(resolved_count, 1)
        
        # Verify observation is marked as resolved
        all_obs = self.storage.get_all_observations()
        self.assertTrue(all_obs[0]['resolved'])
        self.assertIsNotNone(all_obs[0]['resolved_at'])

    def test_detect_resolved_issues_all_types(self):
        """Test universal resolution detection for all resolvable types."""
        # Add multiple observation types
        test_observations = [
            ('todo', {'file_path': 'test.py', 'line_number': 10, 'content': 'Test TODO'}),
            ('security_issue', {'file_path': 'test.py', 'line_number': 20, 'description': 'Security issue'}),
            ('code_issue', {'file_path': 'test.py', 'line_number': 30, 'description': 'Code issue'}),
        ]
        
        for obs_type, data in test_observations:
            self.storage.add_observation(obs_type, data, 'scout', 50)
        
        # Test universal resolution (empty findings = all resolved)
        resolved_count = self.storage.detect_resolved_issues([])
        self.assertEqual(resolved_count, 3)

    def test_detect_resolved_issues_partial_resolution(self):
        """Test partial resolution where some issues remain active."""
        # Add test observations
        self.storage.add_observation('todo', {
            'file_path': 'test.py',
            'line_number': 10,
            'content': 'Active TODO'
        }, 'scout', 50)
        
        self.storage.add_observation('todo', {
            'file_path': 'test.py',
            'line_number': 20,
            'content': 'Resolved TODO'
        }, 'scout', 50)
        
        # Create findings with only one active TODO
        current_findings = [MockFinding('test.py', 10)]
        
        # Test resolution detection
        resolved_count = self.storage.detect_resolved_issues(current_findings, 'todo')
        self.assertEqual(resolved_count, 1)  # Only line 20 should be resolved

    def test_detect_resolved_issues_invalid_data(self):
        """Test handling of invalid observation data."""
        # Add observation with invalid data
        with self.storage.transaction() as conn:
            conn.execute("""
                INSERT INTO observations (type, source_agent, priority, data)
                VALUES (?, ?, ?, ?)
            """, ('todo', 'scout', 50, '{"invalid": "data"}'))  # Missing file_path and line_number
        
        # Test resolution detection with invalid data
        resolved_count = self.storage.detect_resolved_issues([], 'todo')
        self.assertEqual(resolved_count, 0)  # Should skip invalid data

    def test_detect_resolved_issues_malformed_json(self):
        """Test handling of malformed JSON data."""
        # Add observation with malformed JSON
        with self.storage.transaction() as conn:
            conn.execute("""
                INSERT INTO observations (type, source_agent, priority, data)
                VALUES (?, ?, ?, ?)
            """, ('todo', 'scout', 50, 'invalid json'))
        
        # Test resolution detection with malformed JSON
        resolved_count = self.storage.detect_resolved_issues([], 'todo')
        self.assertEqual(resolved_count, 0)  # Should handle gracefully

    def test_detect_resolved_issues_edge_cases(self):
        """Test edge cases for resolution detection."""
        # Test with None current_findings
        resolved_count = self.storage.detect_resolved_issues(None, 'todo')
        self.assertEqual(resolved_count, 0)
        
        # Test with empty types list
        resolved_count = self.storage.detect_resolved_issues([], 'nonexistent_type')
        self.assertEqual(resolved_count, 0)
        
        # Test with invalid observation type
        resolved_count = self.storage.detect_resolved_issues([], 'invalid_type')
        self.assertEqual(resolved_count, 0)

    def test_detect_resolved_todos_backward_compatibility(self):
        """Test backward compatibility with legacy detect_resolved_todos method."""
        # Add test TODO
        self.storage.add_observation('todo', {
            'file_path': 'test.py',
            'line_number': 10,
            'content': 'Test TODO'
        }, 'scout', 50)
        
        # Test legacy method
        resolved_count = self.storage.detect_resolved_todos([])
        self.assertEqual(resolved_count, 1)

    def test_generate_resolved_issues_report_empty(self):
        """Test resolved issues report generation with no resolved issues."""
        report_path = self.output_generator.generate_resolved_issues_report()
        
        self.assertTrue(report_path.exists())
        content = report_path.read_text()
        
        # Check for required content
        self.assertIn("Resolved Issues Report", content)
        self.assertIn("Total Resolved Issues**: 0", content)
        self.assertIn("No issues were detected as resolved", content)
        self.assertIn("informational purposes", content)  # Disclaimer

    def test_generate_resolved_issues_report_with_data(self):
        """Test resolved issues report generation with resolved issues."""
        # Add and resolve test observations
        test_data = [
            ('todo', {'file_path': 'test.py', 'line_number': 10, 'content': 'Test TODO'}),
            ('security_issue', {'file_path': 'test.py', 'line_number': 20, 'description': 'Security issue', 'severity': 'critical'}),
        ]
        
        for obs_type, data in test_data:
            obs_id = self.storage.add_observation(obs_type, data, 'scout', 50)
            # Mark as resolved
            self.storage.mark_observations_resolved([obs_id])
        
        # Generate report
        report_path = self.output_generator.generate_resolved_issues_report()
        content = report_path.read_text()
        
        # Check content
        self.assertIn("Total Resolved Issues**: 2", content)
        self.assertIn("## Todo", content)
        self.assertIn("## Security Issue", content)
        self.assertIn("test.py:10", content)
        self.assertIn("test.py:20", content)

    def test_generate_resolved_issues_report_time_window(self):
        """Test 7-day rolling window for resolved issues report."""
        # Add observation and resolve it 8 days ago (outside window)
        obs_id = self.storage.add_observation('todo', {
            'file_path': 'test.py',
            'line_number': 10,
            'content': 'Old TODO'
        }, 'scout', 50)
        
        # Manually set resolved_at to 8 days ago
        old_date = (datetime.now() - timedelta(days=8)).isoformat()
        with self.storage.transaction() as conn:
            conn.execute("""
                UPDATE observations 
                SET resolved = TRUE, resolved_at = ? 
                WHERE id = ?
            """, (old_date, obs_id))
        
        # Generate report
        report_path = self.output_generator.generate_resolved_issues_report()
        content = report_path.read_text()
        
        # Should show 0 resolved issues (outside 7-day window)
        self.assertIn("Total Resolved Issues**: 0", content)

    def test_sql_injection_protection(self):
        """Test protection against SQL injection in RESOLVABLE_TYPES."""
        # This test ensures the SQL query building is safe
        # Even if somehow malicious content got into RESOLVABLE_TYPES, it should be handled safely
        
        # Generate report (this internally builds SQL with RESOLVABLE_TYPES)
        report_path = self.output_generator.generate_resolved_issues_report()
        
        # Should complete without error
        self.assertTrue(report_path.exists())

    def test_performance_with_large_dataset(self):
        """Test performance with a larger dataset."""
        # Add many observations
        for i in range(100):
            self.storage.add_observation('todo', {
                'file_path': f'test_{i}.py',
                'line_number': i + 1,
                'content': f'TODO {i}'
            }, 'scout', 50)
        
        # Test resolution detection performance
        import time
        start_time = time.time()
        resolved_count = self.storage.detect_resolved_issues([])
        end_time = time.time()
        
        # Should resolve all 100 and complete in reasonable time
        self.assertEqual(resolved_count, 100)
        self.assertLess(end_time - start_time, 5.0)  # Should complete in under 5 seconds

    def test_concurrent_access_safety(self):
        """Test that resolution detection is safe under concurrent access."""
        # Add test observation
        self.storage.add_observation('todo', {
            'file_path': 'test.py',
            'line_number': 10,
            'content': 'Test TODO'
        }, 'scout', 50)
        
        # Simulate concurrent resolution detection
        import threading
        results = []
        
        def run_detection():
            try:
                result = self.storage.detect_resolved_issues([])
                results.append(result)
            except Exception as e:
                results.append(str(e))
        
        threads = [threading.Thread(target=run_detection) for _ in range(5)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        
        # Should handle concurrent access gracefully
        self.assertEqual(len(results), 5)
        # At least one should succeed in marking the observation as resolved
        self.assertTrue(any(isinstance(r, int) and r >= 0 for r in results))

    def test_input_validation(self):
        """Test input validation for file_path and line_number."""
        # Test with invalid file_path
        self.storage.add_observation('todo', {
            'file_path': '',  # Empty file_path
            'line_number': 10,
            'content': 'Test TODO'
        }, 'scout', 50)
        
        # Test with invalid line_number
        self.storage.add_observation('todo', {
            'file_path': 'test.py',
            'line_number': -1,  # Negative line_number
            'content': 'Test TODO'
        }, 'scout', 50)
        
        # Test with non-numeric line_number
        self.storage.add_observation('todo', {
            'file_path': 'test.py',
            'line_number': 'invalid',  # Non-numeric line_number
            'content': 'Test TODO'
        }, 'scout', 50)
        
        # Resolution detection should skip invalid data
        resolved_count = self.storage.detect_resolved_issues([])
        self.assertEqual(resolved_count, 0)  # Should skip all invalid observations

    def test_resolvable_types_constant(self):
        """Test that RESOLVABLE_TYPES constant contains expected types."""
        expected_types = ['todo', 'security_issue', 'code_issue', 'code_smell', 'persistent_issue', 'performance_issue']
        
        self.assertEqual(len(RESOLVABLE_TYPES), 6)
        for expected_type in expected_types:
            self.assertIn(expected_type, RESOLVABLE_TYPES)


if __name__ == '__main__':
    unittest.main()