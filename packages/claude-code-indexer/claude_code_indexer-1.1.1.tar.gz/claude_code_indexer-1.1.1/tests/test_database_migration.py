#!/usr/bin/env python3
"""
Test cases for database migration and error handling
"""

import unittest
import sqlite3
import tempfile
import os
import shutil
from pathlib import Path

from claude_code_indexer.indexer import CodeGraphIndexer


class TestDatabaseMigration(unittest.TestCase):
    """Test database migration functionality"""

    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.test_db = os.path.join(self.test_dir, "test_db.db")
        
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir)

    def test_new_database_creation(self):
        """Test creating a new database with all tables"""
        indexer = CodeGraphIndexer(self.test_db)
        
        # Check if all tables exist
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        expected_tables = ['code_nodes', 'relationships', 'indexing_metadata', 
                          'patterns', 'libraries', 'infrastructure']
        
        for table in expected_tables:
            self.assertIn(table, tables, f"Table {table} should exist")
        
        conn.close()

    def test_old_database_migration(self):
        """Test migrating old database schema"""
        # Create old database with missing columns
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        
        # Create old schema (v1.0.2)
        cursor.execute('''
        CREATE TABLE code_nodes (
            id INTEGER PRIMARY KEY,
            node_type TEXT,
            name TEXT,
            path TEXT,
            summary TEXT,
            importance_score REAL,
            relevance_tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE relationships (
            source_id INTEGER,
            target_id INTEGER,
            relationship_type TEXT,
            weight REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE indexing_metadata (
            key TEXT PRIMARY KEY,
            value TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()
        conn.close()
        
        # Now initialize with new indexer (should trigger migration)
        indexer = CodeGraphIndexer(self.test_db)
        
        # Check if new columns were added
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA table_info(code_nodes)")
        columns = [column[1] for column in cursor.fetchall()]
        
        expected_new_columns = ['weight', 'frequency_score', 'usage_stats']
        for column in expected_new_columns:
            self.assertIn(column, columns, f"Column {column} should be added during migration")
        
        # Check if new tables were created
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        expected_new_tables = ['patterns', 'libraries', 'infrastructure']
        for table in expected_new_tables:
            self.assertIn(table, tables, f"Table {table} should be created during migration")
        
        conn.close()

    def test_corrupted_database_handling(self):
        """Test handling of corrupted database"""
        # Create a corrupted database file
        with open(self.test_db, 'w') as f:
            f.write("This is not a valid SQLite database")
        
        # Should handle gracefully
        try:
            indexer = CodeGraphIndexer(self.test_db)
            # Should either recover or fail gracefully
        except Exception as e:
            # Should not crash the application
            self.assertIsInstance(e, (sqlite3.DatabaseError, sqlite3.Error))

    def test_database_permissions(self):
        """Test handling of database permission issues"""
        # Create a read-only directory
        readonly_dir = os.path.join(self.test_dir, "readonly")
        os.makedirs(readonly_dir)
        os.chmod(readonly_dir, 0o444)  # Read-only
        
        readonly_db = os.path.join(readonly_dir, "readonly.db")
        
        try:
            # Should handle permission error gracefully
            indexer = CodeGraphIndexer(readonly_db)
        except (PermissionError, sqlite3.OperationalError):
            pass  # Expected behavior
        finally:
            # Restore permissions for cleanup
            os.chmod(readonly_dir, 0o755)

    def test_save_with_missing_columns(self):
        """Test save operation when database has missing columns"""
        # Create database with old schema
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE code_nodes (
            id INTEGER PRIMARY KEY,
            node_type TEXT,
            name TEXT,
            path TEXT,
            summary TEXT,
            importance_score REAL,
            relevance_tags TEXT
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE relationships (
            source_id INTEGER,
            target_id INTEGER,
            relationship_type TEXT,
            weight REAL
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE indexing_metadata (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        ''')
        
        conn.commit()
        conn.close()
        
        # Create indexer and add some test data
        indexer = CodeGraphIndexer(self.test_db)
        
        # Add test node
        node_id = indexer._create_node(
            node_type='test',
            name='test_node', 
            path='/test/path',
            summary='Test node'
        )
        
        # Should be able to save even with missing columns
        result = indexer.save_to_db()
        self.assertTrue(result, "Should be able to save with fallback")
        
        # Verify data was saved
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM code_nodes")
        count = cursor.fetchone()[0]
        self.assertGreater(count, 0, "Should have saved at least one node")
        conn.close()


if __name__ == '__main__':
    unittest.main()