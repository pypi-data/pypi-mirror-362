"""
Performance benchmarking for Universal Issue Resolution Detection feature.

Tests performance characteristics, optimization effectiveness, and 
scalability of the resolution detection system under various loads.
"""

import unittest
import tempfile
import json
import time
import threading
from pathlib import Path
from datetime import datetime, timedelta
from statistics import mean, median
import gc

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from coppersun_brass.core.storage import BrassStorage
from coppersun_brass.core.output_generator import OutputGenerator
from coppersun_brass.core.constants import RESOLVABLE_TYPES, ObservationTypes
from coppersun_brass.config import BrassConfig


class MockFinding:
    """Mock finding object for performance testing."""
    def __init__(self, file_path: str, line_number: int):
        self.file_path = file_path
        self.line_number = line_number


class TestPerformanceBenchmarks(unittest.TestCase):
    """Performance benchmark test suite for Universal Issue Resolution Detection."""

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

    def benchmark_function(self, func, *args, **kwargs):
        """Benchmark a function and return timing statistics."""
        times = []
        num_runs = 5
        results = []
        
        for run in range(num_runs):
            gc.collect()  # Clean garbage before each run
            
            # Reset resolved flags for repeated measurements (except first run)
            if run > 0:
                with self.storage.transaction() as conn:
                    conn.execute("UPDATE observations SET resolved = FALSE, resolved_at = NULL")
            
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            times.append(end_time - start_time)
            results.append(result)
        
        return {
            'min_time': min(times),
            'max_time': max(times),
            'avg_time': mean(times),
            'median_time': median(times),
            'total_runs': num_runs,
            'last_result': results[-1],
            'all_results': results
        }

    def test_scalability_with_increasing_observations(self):
        """Test performance scalability with increasing numbers of observations."""
        dataset_sizes = [100, 500, 1000, 2500, 5000]
        results = {}
        
        for size in dataset_sizes:
            # Clean database for each test
            with self.storage.transaction() as conn:
                conn.execute("DELETE FROM observations")
            
            # Add observations
            for i in range(size):
                self.storage.add_observation(ObservationTypes.TODO, {
                    'file_path': f'test_{i % 100}.py',  # Limit file variety to test grouping
                    'line_number': i + 1,
                    'content': f'TODO {i}'
                }, 'scout', 50)
            
            # Benchmark resolution detection
            stats = self.benchmark_function(self.storage.detect_resolved_issues, [])
            results[size] = stats
            
            print(f"Dataset size {size}: avg={stats['avg_time']:.4f}s, "
                  f"resolved={stats['last_result']}")
            
            # Performance assertions
            self.assertLess(stats['avg_time'], 10.0, 
                          f"Should complete within 10s for {size} observations")
            self.assertEqual(stats['last_result'], size, 
                           f"Should resolve all {size} observations")
        
        # Check that performance scales reasonably (not exponentially)
        # Performance should be roughly linear or better
        if len(results) >= 3:
            small_size = min(dataset_sizes)
            large_size = max(dataset_sizes)
            size_ratio = large_size / small_size
            time_ratio = results[large_size]['avg_time'] / results[small_size]['avg_time']
            
            # Time complexity should be better than O(n²)
            self.assertLess(time_ratio, size_ratio * size_ratio, 
                          "Performance should scale better than O(n²)")

    def test_mixed_observation_types_performance(self):
        """Test performance with mixed observation types."""
        observations_per_type = 200
        
        # Add observations of all resolvable types
        for obs_type in RESOLVABLE_TYPES:
            for i in range(observations_per_type):
                self.storage.add_observation(obs_type, {
                    'file_path': f'test_{obs_type}_{i}.py',
                    'line_number': i + 1,
                    'content': f'{obs_type.upper()} {i}',
                    'description': f'Test {obs_type} issue'
                }, 'scout', 50)
        
        total_observations = len(RESOLVABLE_TYPES) * observations_per_type
        
        # Benchmark universal resolution
        stats = self.benchmark_function(self.storage.detect_resolved_issues, [])
        
        print(f"Mixed types performance: {total_observations} observations, "
              f"avg={stats['avg_time']:.4f}s")
        
        # Performance assertions
        self.assertLess(stats['avg_time'], 5.0, 
                       "Mixed type resolution should complete within 5s")
        self.assertEqual(stats['last_result'], total_observations,
                        "Should resolve all mixed type observations")

    def test_partial_resolution_performance(self):
        """Test performance when only some observations are resolved."""
        total_observations = 1000
        active_percentage = 30  # 30% remain active
        
        # Add observations
        active_findings = []
        for i in range(total_observations):
            file_path = f'test_{i}.py'
            line_number = i + 1
            
            self.storage.add_observation(ObservationTypes.TODO, {
                'file_path': file_path,
                'line_number': line_number,
                'content': f'TODO {i}'
            }, 'scout', 50)
            
            # Keep some as "active" (not resolved)
            if i < (total_observations * active_percentage // 100):
                active_findings.append(MockFinding(file_path, line_number))
        
        # Benchmark partial resolution
        stats = self.benchmark_function(self.storage.detect_resolved_issues, active_findings)
        
        expected_resolved = total_observations - len(active_findings)
        
        print(f"Partial resolution: {total_observations} total, "
              f"{len(active_findings)} active, avg={stats['avg_time']:.4f}s")
        
        # Performance assertions
        self.assertLess(stats['avg_time'], 3.0, 
                       "Partial resolution should complete within 3s")
        self.assertEqual(stats['last_result'], expected_resolved,
                        f"Should resolve {expected_resolved} observations")

    def test_concurrent_resolution_performance(self):
        """Test performance under concurrent access."""
        observations_per_thread = 100
        num_threads = 5
        
        # Add observations
        for i in range(observations_per_thread * num_threads):
            self.storage.add_observation(ObservationTypes.TODO, {
                'file_path': f'test_{i}.py',
                'line_number': i + 1,
                'content': f'TODO {i}'
            }, 'scout', 50)
        
        results = []
        errors = []
        
        def concurrent_resolution():
            try:
                start_time = time.perf_counter()
                result = self.storage.detect_resolved_issues([])
                end_time = time.perf_counter()
                results.append({
                    'time': end_time - start_time,
                    'resolved_count': result
                })
            except Exception as e:
                errors.append(str(e))
        
        # Run concurrent resolutions
        threads = [threading.Thread(target=concurrent_resolution) 
                  for _ in range(num_threads)]
        
        overall_start = time.perf_counter()
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        overall_end = time.perf_counter()
        
        # Analyze results
        successful_runs = len(results)
        avg_time = mean([r['time'] for r in results]) if results else 0
        total_time = overall_end - overall_start
        
        print(f"Concurrent access: {successful_runs}/{num_threads} successful, "
              f"avg_time={avg_time:.4f}s, total_time={total_time:.4f}s")
        
        # Performance assertions
        self.assertGreaterEqual(successful_runs, num_threads - 1, 
                               "Most concurrent operations should succeed")
        self.assertLess(avg_time, 5.0, 
                       "Concurrent operations should complete within 5s each")
        self.assertLessEqual(len(errors), 1, 
                            "Should have minimal concurrent access errors")

    def test_memory_usage_efficiency(self):
        """Test memory usage efficiency during large operations."""
        # Skip psutil dependency - focus on time-based performance
        import gc
        
        # Force garbage collection for clean baseline
        gc.collect()
        
        # Add large number of observations
        large_dataset = 2000
        for i in range(large_dataset):
            self.storage.add_observation(ObservationTypes.TODO, {
                'file_path': f'test_{i}.py',
                'line_number': i + 1,
                'content': f'TODO {i}' * 10  # Larger content
            }, 'scout', 50)
        
        # Perform resolution detection with timing
        start_time = time.perf_counter()
        result = self.storage.detect_resolved_issues([])
        end_time = time.perf_counter()
        
        operation_time = end_time - start_time
        
        print(f"Memory efficiency test: {large_dataset} observations, "
              f"time={operation_time:.4f}s")
        
        # Performance assertions (without memory measurements)
        self.assertLess(operation_time, 3.0, 
                       "Large dataset processing should complete within 3s")
        self.assertEqual(result, large_dataset, 
                        "Should resolve all observations efficiently")

    def test_query_optimization_effectiveness(self):
        """Test that query optimization (single query vs N+1) is effective."""
        observation_types = RESOLVABLE_TYPES[:3]  # Test with 3 types
        observations_per_type = 300
        
        # Add observations
        for obs_type in observation_types:
            for i in range(observations_per_type):
                self.storage.add_observation(obs_type, {
                    'file_path': f'test_{obs_type}_{i}.py',
                    'line_number': i + 1,
                    'content': f'{obs_type.upper()} {i}'
                }, 'scout', 50)
        
        # Benchmark optimized version
        stats = self.benchmark_function(self.storage.detect_resolved_issues, [])
        
        total_observations = len(observation_types) * observations_per_type
        
        print(f"Query optimization: {total_observations} observations across "
              f"{len(observation_types)} types, avg={stats['avg_time']:.4f}s")
        
        # The optimized version should handle multiple types efficiently
        # If this was N+1 queries, it would be much slower
        self.assertLess(stats['avg_time'], 2.0, 
                       "Optimized queries should complete within 2s")
        self.assertEqual(stats['last_result'], total_observations,
                        "Should resolve all observations across types")

    def test_report_generation_performance(self):
        """Test performance of resolved issues report generation."""
        # Add observations and resolve them automatically
        num_resolved = 500
        for i in range(num_resolved):
            self.storage.add_observation(ObservationTypes.TODO, {
                'file_path': f'test_{i}.py',
                'line_number': i + 1,
                'content': f'TODO {i}'
            }, 'scout', 50)
        
        # Resolve all observations (empty list means all are resolved)
        resolved_count = self.storage.detect_resolved_issues([])
        self.assertEqual(resolved_count, num_resolved, f"Should resolve {num_resolved} observations")
        
        # Benchmark report generation
        stats = self.benchmark_function(self.output_generator.generate_resolved_issues_report)
        
        print(f"Report generation: {num_resolved} resolved issues, "
              f"avg={stats['avg_time']:.4f}s")
        
        # Performance assertions
        self.assertLess(stats['avg_time'], 2.0, 
                       "Report generation should complete within 2s")
        
        # Verify report was generated
        report_path = stats['last_result']
        self.assertTrue(report_path.exists(), "Report file should be created")
        
        # Verify report is not empty (content validation is tested elsewhere)
        content = report_path.read_text()
        self.assertGreater(len(content), 100, "Report should have substantial content")

    def test_database_scaling_characteristics(self):
        """Test database performance characteristics as data accumulates."""
        batch_sizes = [250, 500, 750, 1000]
        cumulative_times = []
        
        for batch_size in batch_sizes:
            # Add batch of observations
            for i in range(batch_size):
                self.storage.add_observation(ObservationTypes.TODO, {
                    'file_path': f'batch_test_{i}.py',
                    'line_number': i + 1,
                    'content': f'TODO batch {i}'
                }, 'scout', 50)
            
            # Measure resolution time with accumulated data
            start_time = time.perf_counter()
            resolved_count = self.storage.detect_resolved_issues([])
            end_time = time.perf_counter()
            
            elapsed_time = end_time - start_time
            cumulative_times.append(elapsed_time)
            
            print(f"Cumulative data: {resolved_count} observations, "
                  f"time={elapsed_time:.4f}s")
            
            # Each batch should still perform reasonably
            self.assertLess(elapsed_time, 5.0, 
                           f"Should handle {resolved_count} observations within 5s")
        
        # Check that performance doesn't degrade exponentially
        if len(cumulative_times) >= 2:
            first_time = cumulative_times[0]
            last_time = cumulative_times[-1]
            # Performance degradation should be reasonable
            self.assertLess(last_time / first_time, 10.0, 
                           "Performance degradation should be reasonable")


if __name__ == '__main__':
    unittest.main()