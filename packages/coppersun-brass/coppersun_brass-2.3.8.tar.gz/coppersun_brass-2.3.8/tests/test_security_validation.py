"""
Security testing for Universal Issue Resolution Detection feature.

Tests focus on SQL injection prevention, parameter validation, and 
secure handling of user-provided data in the resolution detection system.
"""

import unittest
import tempfile
import json
import sqlite3
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from coppersun_brass.core.storage import BrassStorage
from coppersun_brass.core.output_generator import OutputGenerator
from coppersun_brass.core.constants import RESOLVABLE_TYPES
from coppersun_brass.config import BrassConfig


class TestSecurityValidation(unittest.TestCase):
    """Security-focused test suite for Universal Issue Resolution Detection."""

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

    def test_sql_injection_protection_in_type_filtering(self):
        """Test protection against SQL injection in observation type filtering."""
        # Attempt to inject malicious SQL through observation_type parameter
        malicious_types = [
            "'; DROP TABLE observations; --",
            "todo'; DELETE FROM observations WHERE 1=1; --",
            "todo' UNION SELECT * FROM sqlite_master --",
            "todo\"; INSERT INTO observations VALUES(1,'malicious','test',50,'{}',datetime('now'),0,0,NULL); --"
        ]
        
        for malicious_type in malicious_types:
            with self.subTest(malicious_type=malicious_type):
                try:
                    # This should not cause any database damage
                    result = self.storage.detect_resolved_issues([], malicious_type)
                    # Should return 0 safely (no issues to resolve)
                    self.assertEqual(result, 0)
                    
                    # Verify database integrity is maintained
                    with self.storage.transaction() as conn:
                        # Check that observations table still exists and is intact
                        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='observations'")
                        table_exists = cursor.fetchone()
                        self.assertIsNotNone(table_exists, "Observations table should still exist")
                        
                        # Check no malicious data was inserted
                        cursor = conn.execute("SELECT COUNT(*) FROM observations WHERE source_agent = 'test'")
                        malicious_count = cursor.fetchone()[0]
                        self.assertEqual(malicious_count, 0, "No malicious data should be inserted")
                        
                except Exception as e:
                    # Should not raise exceptions from SQL injection attempts
                    self.fail(f"SQL injection attempt caused unexpected exception: {e}")

    def test_sql_injection_protection_in_batch_queries(self):
        """Test protection against SQL injection in batch query construction."""
        # Add legitimate observation
        obs_id = self.storage.add_observation('todo', {
            'file_path': 'test.py',
            'line_number': 10,
            'content': 'Test TODO'
        }, 'scout', 50)
        
        # Test with manipulated RESOLVABLE_TYPES (simulating attack)
        original_resolvable_types = RESOLVABLE_TYPES.copy()
        
        try:
            # Monkey-patch RESOLVABLE_TYPES with malicious content
            import coppersun_brass.core.constants as constants
            constants.RESOLVABLE_TYPES = [
                "todo'; DROP TABLE observations; --",
                "security_issue"
            ]
            
            # This should not cause database damage due to parameterized queries
            result = self.storage.detect_resolved_issues([])
            
            # Verify database integrity
            with self.storage.transaction() as conn:
                cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='observations'")
                table_exists = cursor.fetchone()
                self.assertIsNotNone(table_exists, "Observations table should still exist")
                
                # Check the legitimate observation still exists
                cursor = conn.execute("SELECT COUNT(*) FROM observations WHERE id = ?", (obs_id,))
                count = cursor.fetchone()[0]
                self.assertEqual(count, 1, "Legitimate observation should still exist")
                
        finally:
            # Restore original RESOLVABLE_TYPES
            import coppersun_brass.core.constants as constants
            constants.RESOLVABLE_TYPES = original_resolvable_types

    def test_malicious_json_data_handling(self):
        """Test handling of malicious JSON data in observations."""
        malicious_payloads = [
            '{"file_path": "../../../etc/passwd", "line_number": 1}',  # Path traversal
            '{"file_path": "test.py", "line_number": "1; DROP TABLE observations; --"}',  # SQL in data
            '{"file_path": "' + 'A' * 10000 + '", "line_number": 1}',  # Oversized data
            '{"file_path": "test.py", "line_number": -999999999}',  # Extreme negative number
            '{"file_path": "", "line_number": null}',  # Null values
            '{"file_path": {"nested": "object"}, "line_number": [1,2,3]}',  # Wrong data types
        ]
        
        for i, payload in enumerate(malicious_payloads):
            with self.subTest(payload_index=i):
                try:
                    # Directly insert malicious data into database
                    with self.storage.transaction() as conn:
                        conn.execute("""
                            INSERT INTO observations (type, source_agent, priority, data)
                            VALUES (?, ?, ?, ?)
                        """, ('todo', 'test', 50, payload))
                    
                    # Resolution detection should handle malicious data gracefully
                    result = self.storage.detect_resolved_issues([])
                    
                    # Should not crash and should return 0 (skip malicious data)
                    self.assertIsInstance(result, int)
                    self.assertGreaterEqual(result, 0)
                    
                except Exception as e:
                    # Should handle malicious data gracefully, not crash
                    self.assertIsInstance(e, (json.JSONDecodeError, sqlite3.Error, ValueError, TypeError))

    def test_input_sanitization_file_paths(self):
        """Test that file paths are properly validated and sanitized."""
        dangerous_paths = [
            "../../../etc/passwd",
            "/etc/shadow", 
            "C:\\Windows\\System32\\config\\SAM",
            "test.py'; DELETE FROM observations; --",
            "\x00\x01\x02",  # Null bytes and control characters
            "test\nfile.py",  # Newlines
            "test\tfile.py",  # Tabs
        ]
        
        for dangerous_path in dangerous_paths:
            with self.subTest(path=dangerous_path):
                # Add observation with dangerous path
                obs_id = self.storage.add_observation('todo', {
                    'file_path': dangerous_path,
                    'line_number': 10,
                    'content': 'Test TODO'
                }, 'scout', 50)
                
                # Resolution detection should handle safely
                result = self.storage.detect_resolved_issues([])
                
                # Should not cause database corruption
                with self.storage.transaction() as conn:
                    cursor = conn.execute("SELECT COUNT(*) FROM observations")
                    count = cursor.fetchone()[0]
                    self.assertGreater(count, 0, "Database should still contain observations")

    def test_parameter_validation_edge_cases(self):
        """Test parameter validation with edge cases and boundary values."""
        edge_cases = [
            (None, None),  # None values
            ([], None),    # Empty list with None type
            ([], ""),      # Empty list with empty string type
            ([], "nonexistent_type"),  # Invalid observation type
            ([Mock()], "todo"),  # Mock objects without required attributes
        ]
        
        for current_findings, obs_type in edge_cases:
            with self.subTest(findings=str(current_findings), obs_type=obs_type):
                try:
                    result = self.storage.detect_resolved_issues(current_findings, obs_type)
                    # Should handle edge cases gracefully
                    self.assertIsInstance(result, int)
                    self.assertGreaterEqual(result, 0)
                except Exception as e:
                    # Should not raise unexpected exceptions
                    self.assertIsInstance(e, (ValueError, TypeError, AttributeError))

    def test_concurrent_access_security(self):
        """Test that concurrent access doesn't create security vulnerabilities."""
        # Add test observation
        obs_id = self.storage.add_observation('todo', {
            'file_path': 'test.py',
            'line_number': 10,
            'content': 'Test TODO'
        }, 'scout', 50)
        
        import threading
        import time
        results = []
        errors = []
        
        def concurrent_resolution_attempt():
            try:
                # Simulate concurrent resolution detection
                result = self.storage.detect_resolved_issues([])
                results.append(result)
            except Exception as e:
                errors.append(str(e))
        
        # Run multiple concurrent attempts
        threads = [threading.Thread(target=concurrent_resolution_attempt) for _ in range(10)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        
        # Verify no race conditions caused security issues
        self.assertLessEqual(len(errors), 1, "Should have minimal concurrent access errors")
        
        # Verify database integrity after concurrent access
        with self.storage.transaction() as conn:
            cursor = conn.execute("SELECT resolved FROM observations WHERE id = ?", (obs_id,))
            row = cursor.fetchone()
            self.assertIsNotNone(row, "Observation should still exist")
            # Should be marked as resolved (TRUE/1) by at least one thread
            self.assertIn(row[0], [True, 1], "Should be properly resolved")

    def test_memory_exhaustion_protection(self):
        """Test protection against memory exhaustion attacks."""
        # Try to create very large number of observations
        large_batch_size = 1000
        
        for i in range(large_batch_size):
            self.storage.add_observation('todo', {
                'file_path': f'test_{i}.py',
                'line_number': i + 1,
                'content': f'TODO {i}' * 100  # Larger content
            }, 'scout', 50)
        
        # Resolution detection should handle large dataset efficiently
        import time
        start_time = time.time()
        result = self.storage.detect_resolved_issues([])
        end_time = time.time()
        
        # Should complete in reasonable time (protect against DoS)
        self.assertLess(end_time - start_time, 10.0, "Should complete within 10 seconds")
        self.assertEqual(result, large_batch_size, "Should resolve all observations")

    def test_privilege_escalation_protection(self):
        """Test that the system doesn't allow privilege escalation through data manipulation."""
        # Try to manipulate observation data to gain unauthorized access
        malicious_data = {
            'file_path': 'test.py',
            'line_number': 10,
            'admin': True,  # Try to set admin flag
            'execute': 'rm -rf /',  # Try to inject system commands
            'sql_query': 'UPDATE users SET admin=1',  # Try to inject SQL
            'content': 'TODO with embedded script <script>alert("xss")</script>'
        }
        
        obs_id = self.storage.add_observation('todo', malicious_data, 'scout', 50)
        
        # Resolution detection should only use safe fields
        result = self.storage.detect_resolved_issues([])
        
        # Verify that malicious data is handled safely
        with self.storage.transaction() as conn:
            cursor = conn.execute("SELECT data FROM observations WHERE id = ?", (obs_id,))
            stored_data = json.loads(cursor.fetchone()[0])
            
            # Data should be stored as-is but not executed
            self.assertIn('admin', stored_data)  # Data preserved
            self.assertIn('execute', stored_data)  # Data preserved
            # But system should not have executed any commands or granted privileges


if __name__ == '__main__':
    unittest.main()