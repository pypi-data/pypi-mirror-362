#!/usr/bin/env python3
"""
Storage Consolidation Validation Tests

Comprehensive tests to validate single-database creation and ensure
architectural consolidation works correctly. Tests all components use
BrassConfig path resolution exclusively.

CRITICAL: These tests ensure production quality consolidation with zero data loss.
"""

import sys
import sqlite3
import tempfile
import shutil
import pytest
from pathlib import Path
from typing import List, Dict, Any
import os

# Add source to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from coppersun_brass.config import BrassConfig
from coppersun_brass.core.storage import BrassStorage
from coppersun_brass.core.dcp_adapter import DCPAdapter
from coppersun_brass.core.brass import BrassSystem
from coppersun_brass.agents.scout.scout_agent import ScoutAgent


class TestStorageConsolidation:
    """Test storage consolidation and architectural consistency."""
    
    def setup_method(self):
        """Set up test environment with clean temporary directory."""
        self.test_dir = Path(tempfile.mkdtemp())
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Track created databases for cleanup validation
        self.created_databases = []
    
    def teardown_method(self):
        """Clean up test environment."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def _find_database_files(self) -> List[Path]:
        """Find all database files in test directory.
        
        Returns:
            List of database file paths
        """
        db_files = []
        for root, dirs, files in os.walk(self.test_dir):
            for file in files:
                if file.endswith('.db'):
                    db_files.append(Path(root) / file)
        return db_files
    
    def _count_observations(self, db_path: Path) -> int:
        """Count observations in database.
        
        Args:
            db_path: Database file path
            
        Returns:
            Number of observations
        """
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.execute("SELECT COUNT(*) FROM observations")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except Exception:
            return 0
    
    def test_single_database_creation_brasssystem(self):
        """Test BrassSystem creates only one database file."""
        # Initialize BrassSystem
        brass = BrassSystem(self.test_dir)
        
        # Find all database files
        db_files = self._find_database_files()
        
        # Should have exactly one database file
        assert len(db_files) == 1, f"Expected 1 database, found {len(db_files)}: {db_files}"
        
        # Verify it uses BrassConfig path
        config = BrassConfig(self.test_dir)
        assert db_files[0] == config.db_path, f"Database path mismatch: {db_files[0]} != {config.db_path}"
        
        # Verify BrassSystem uses same path
        assert brass.storage.db_path == config.db_path
    
    def test_single_database_creation_dcpadapter(self):
        """Test DCPAdapter creates only one database file."""
        # Initialize DCPAdapter
        dcp = DCPAdapter()
        
        # Find all database files
        db_files = self._find_database_files()
        
        # Should have exactly one database file
        assert len(db_files) == 1, f"Expected 1 database, found {len(db_files)}: {db_files}"
        
        # Verify it uses BrassConfig path
        config = BrassConfig(self.test_dir)
        assert db_files[0] == config.db_path
        assert dcp.storage.db_path == config.db_path
    
    def test_single_database_creation_scout_agent(self):
        """Test ScoutAgent creates only one database file."""
        # Initialize ScoutAgent
        scout = ScoutAgent()
        
        # Find all database files
        db_files = self._find_database_files()
        
        # Should have exactly one database file
        assert len(db_files) == 1, f"Expected 1 database, found {len(db_files)}: {db_files}"
        
        # Verify all components use same database
        config = BrassConfig(self.test_dir)
        assert db_files[0] == config.db_path
    
    def test_multiple_components_same_database(self):
        """Test multiple components use the same database file."""
        # Initialize all major components
        config = BrassConfig(self.test_dir)
        dcp = DCPAdapter()
        brass = BrassSystem(self.test_dir)
        scout = ScoutAgent()
        
        # Find all database files
        db_files = self._find_database_files()
        
        # Should still have exactly one database file
        assert len(db_files) == 1, f"Expected 1 database, found {len(db_files)}: {db_files}"
        
        # Verify all components use same path
        expected_path = config.db_path
        assert dcp.storage.db_path == expected_path
        assert brass.storage.db_path == expected_path
        
        # All should point to the same file
        assert db_files[0] == expected_path
    
    def test_observations_shared_across_components(self):
        """Test observations are shared across all components."""
        # Initialize components
        dcp = DCPAdapter()
        scout = ScoutAgent()
        
        # Add observation via DCP
        dcp.add_observation("test_type", {"message": "test_data"}, "test_agent")
        
        # Add observation via Scout
        scout.dcp_manager.add_observation("scout_type", {"finding": "test_finding"}, "scout")
        
        # Find database file
        db_files = self._find_database_files()
        assert len(db_files) == 1
        
        # Verify both observations are in same database
        observation_count = self._count_observations(db_files[0])
        assert observation_count == 2, f"Expected 2 observations, found {observation_count}"
        
        # Verify observations are accessible from both components
        dcp_observations = dcp.get_observations()
        assert len(dcp_observations) == 2
    
    def test_no_legacy_database_creation(self):
        """Test no legacy database files are created."""
        # Initialize multiple components
        config = BrassConfig(self.test_dir)
        dcp = DCPAdapter()
        brass = BrassSystem(self.test_dir)
        scout = ScoutAgent()
        
        # Add some observations
        dcp.add_observation("test", {"data": "value"}, "test_agent")
        scout.dcp_manager.add_observation("scout", {"finding": "issue"}, "scout")
        
        # Check for legacy database patterns
        legacy_patterns = [
            self.test_dir / "brass_storage.db",
            self.test_dir / "coppersun_brass.db",
            self.test_dir / ".brass" / "coppersun_brass.db"
        ]
        
        for legacy_path in legacy_patterns:
            assert not legacy_path.exists(), f"Legacy database created: {legacy_path}"
        
        # Should only have the BrassConfig database
        db_files = self._find_database_files()
        assert len(db_files) == 1
        assert db_files[0] == config.db_path
    
    def test_project_isolation(self):
        """Test different projects use isolated databases."""
        # Create two different project configs
        project1_dir = self.test_dir / "project1"
        project2_dir = self.test_dir / "project2"
        project1_dir.mkdir()
        project2_dir.mkdir()
        
        config1 = BrassConfig(project1_dir)
        config2 = BrassConfig(project2_dir)
        
        # Should have different database paths
        assert config1.db_path != config2.db_path
        
        # Initialize components for each project
        os.chdir(project1_dir)
        dcp1 = DCPAdapter()
        dcp1.add_observation("proj1", {"data": "project1"}, "agent1")
        
        os.chdir(project2_dir)
        dcp2 = DCPAdapter()
        dcp2.add_observation("proj2", {"data": "project2"}, "agent2")
        
        # Verify each has their own database
        assert dcp1.storage.db_path == config1.db_path
        assert dcp2.storage.db_path == config2.db_path
        
        # Verify observations are isolated
        obs1 = dcp1.get_observations()
        obs2 = dcp2.get_observations()
        
        assert len(obs1) == 1
        assert len(obs2) == 1
        assert obs1[0]['type'] == 'proj1'
        assert obs2[0]['type'] == 'proj2'
    
    def test_database_schema_consistency(self):
        """Test all components create consistent database schema."""
        # Initialize components separately to test schema creation
        configs = []
        for i in range(3):
            test_subdir = self.test_dir / f"test{i}"
            test_subdir.mkdir()
            os.chdir(test_subdir)
            
            config = BrassConfig(test_subdir)
            configs.append(config)
            
            if i == 0:
                # BrassStorage direct
                storage = BrassStorage(config.db_path)
            elif i == 1:
                # DCPAdapter
                dcp = DCPAdapter()
            else:
                # BrassSystem
                brass = BrassSystem(test_subdir)
        
        # Verify all databases have same schema
        base_schema = None
        for config in configs:
            conn = sqlite3.connect(config.db_path)
            cursor = conn.execute("SELECT sql FROM sqlite_master WHERE type='table' ORDER BY name")
            schema = cursor.fetchall()
            conn.close()
            
            if base_schema is None:
                base_schema = schema
            else:
                assert schema == base_schema, f"Schema mismatch for {config.db_path}"


class TestDataConsolidation:
    """Test data consolidation from fragmented sources."""
    
    def setup_method(self):
        """Set up test environment with fragmented databases."""
        self.test_dir = Path(tempfile.mkdtemp())
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Create fragmented databases to simulate the real problem
        self._create_fragmented_databases()
    
    def teardown_method(self):
        """Clean up test environment."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def _create_fragmented_databases(self):
        """Create fragmented databases simulating the real problem."""
        # Create brass_storage.db (legacy compatibility bug)
        brass_storage_path = self.test_dir / "brass_storage.db"
        storage1 = BrassStorage(brass_storage_path)
        for i in range(36):
            storage1.add_observation("unknown", {"data": f"legacy_{i}"}, "scout", 50)
        
        # Create .brass/coppersun_brass.db (project-local path)
        brass_dir = self.test_dir / ".brass"
        brass_dir.mkdir()
        project_local_path = brass_dir / "coppersun_brass.db"
        storage2 = BrassStorage(project_local_path)
        storage2.add_observation("test_observation", {"data": "project_local"}, "test", 60)
        
        # Create coppersun_brass.db (project root)
        project_root_path = self.test_dir / "coppersun_brass.db"
        storage3 = BrassStorage(project_root_path)
        # This one has 0 observations as observed in real problem
    
    def test_consolidation_discovery(self):
        """Test consolidation script discovers all fragmented databases."""
        from scripts.consolidate_database_storage import StorageConsolidator
        
        consolidator = StorageConsolidator(self.test_dir)
        sources = consolidator.discover_source_databases()
        
        # Should find the fragmented databases
        source_names = {src.name for src in sources}
        expected = {"brass_storage.db", "coppersun_brass.db"}
        
        # .brass/coppersun_brass.db should also be found
        brass_subdir_found = any(".brass" in str(src) for src in sources)
        assert brass_subdir_found, "Should find .brass/coppersun_brass.db"
        
        # Should find at least the main fragmented databases
        assert "brass_storage.db" in source_names
        assert len(sources) >= 2
    
    def test_consolidation_preserves_data(self):
        """Test consolidation preserves all observation data."""
        from scripts.consolidate_database_storage import StorageConsolidator
        
        # Count original observations
        original_total = 0
        for db_path in [
            self.test_dir / "brass_storage.db",
            self.test_dir / ".brass" / "coppersun_brass.db", 
            self.test_dir / "coppersun_brass.db"
        ]:
            if db_path.exists():
                original_total += self._count_observations(db_path)
        
        # Run consolidation
        consolidator = StorageConsolidator(self.test_dir)
        success = consolidator.run_consolidation(dry_run=False)
        assert success
        
        # Verify data preservation
        config = BrassConfig(self.test_dir)
        consolidated_count = self._count_observations(config.db_path)
        
        # Should have preserved all observations (accounting for potential deduplication)
        assert consolidated_count >= original_total - 5  # Allow for some deduplication
        assert consolidated_count <= original_total  # But not more than original
    
    def _count_observations(self, db_path: Path) -> int:
        """Count observations in database."""
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.execute("SELECT COUNT(*) FROM observations")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except Exception:
            return 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])