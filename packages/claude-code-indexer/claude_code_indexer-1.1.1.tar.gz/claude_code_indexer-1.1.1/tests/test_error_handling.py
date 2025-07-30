#!/usr/bin/env python3
"""
Test cases for error handling and robustness
"""

import unittest
import tempfile
import os
import shutil
from pathlib import Path

from claude_code_indexer.indexer import CodeGraphIndexer
from claude_code_indexer.pattern_detector import PatternDetector
from claude_code_indexer.library_detector import LibraryDetector
from claude_code_indexer.infrastructure_detector import InfrastructureDetector
from claude_code_indexer.weight_calculator import WeightCalculator


class TestErrorHandling(unittest.TestCase):
    """Test error handling across all components"""

    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.test_db = os.path.join(self.test_dir, "test_error.db")
        self.indexer = CodeGraphIndexer(self.test_db)
        
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir)

    def test_invalid_python_file(self):
        """Test handling of invalid Python files"""
        # Create invalid Python file
        invalid_file = os.path.join(self.test_dir, "invalid.py")
        with open(invalid_file, 'w') as f:
            f.write("This is not valid Python syntax {{{")
        
        # Should handle gracefully
        result = self.indexer.parse_python_file(invalid_file)
        self.assertEqual(result, {}, "Should return empty dict for invalid Python")

    def test_binary_file_handling(self):
        """Test handling of binary files"""
        # Create binary file with .py extension
        binary_file = os.path.join(self.test_dir, "binary.py")
        with open(binary_file, 'wb') as f:
            f.write(b'\x00\x01\x02\x03\xff\xfe\xfd')
        
        # Should handle gracefully
        result = self.indexer.parse_python_file(binary_file)
        self.assertEqual(result, {}, "Should return empty dict for binary files")

    def test_empty_file_handling(self):
        """Test handling of empty files"""
        empty_file = os.path.join(self.test_dir, "empty.py")
        Path(empty_file).touch()
        
        # Should handle gracefully
        result = self.indexer.parse_python_file(empty_file)
        self.assertIsInstance(result, dict, "Should return dict for empty file")

    def test_large_file_handling(self):
        """Test handling of very large files"""
        large_file = os.path.join(self.test_dir, "large.py")
        
        # Create large file with repeated content
        with open(large_file, 'w') as f:
            f.write('# Large file test\n')
            for i in range(10000):
                f.write(f'def function_{i}():\n    pass\n\n')
        
        # Should handle without crashing
        try:
            result = self.indexer.parse_python_file(large_file)
            self.assertIsInstance(result, dict, "Should handle large files")
        except MemoryError:
            self.skipTest("System doesn't have enough memory for this test")

    def test_unicode_file_handling(self):
        """Test handling of files with various encodings"""
        # Test UTF-8 with BOM
        utf8_bom_file = os.path.join(self.test_dir, "utf8_bom.py")
        with open(utf8_bom_file, 'wb') as f:
            f.write('\ufeff# UTF-8 with BOM\ndef test(): pass\n'.encode('utf-8-sig'))
        
        result = self.indexer.parse_python_file(utf8_bom_file)
        self.assertIsInstance(result, dict, "Should handle UTF-8 BOM files")
        
        # Test Latin-1 encoding
        latin1_file = os.path.join(self.test_dir, "latin1.py")
        with open(latin1_file, 'wb') as f:
            f.write('# Latin-1 encoding\ndef test(): pass\n'.encode('latin-1'))
        
        result = self.indexer.parse_python_file(latin1_file)
        self.assertIsInstance(result, dict, "Should handle Latin-1 files")

    def test_nonexistent_directory(self):
        """Test indexing nonexistent directory"""
        nonexistent = os.path.join(self.test_dir, "nonexistent")
        
        # Should handle gracefully
        self.indexer.index_directory(nonexistent)
        # Should not crash

    def test_empty_directory(self):
        """Test indexing empty directory"""
        empty_dir = os.path.join(self.test_dir, "empty")
        os.makedirs(empty_dir)
        
        # Should handle gracefully
        self.indexer.index_directory(empty_dir)
        # Should not crash

    def test_pattern_detector_error_handling(self):
        """Test pattern detector with malformed AST"""
        detector = PatternDetector()
        
        # Test with None AST
        patterns = detector.detect_patterns(None, "test.py")
        self.assertEqual(patterns, [], "Should return empty list for None AST")

    def test_library_detector_error_handling(self):
        """Test library detector with malformed input"""
        detector = LibraryDetector()
        
        # Test with empty content
        libraries = detector.detect_libraries(None, "test.py", "")
        self.assertIsInstance(libraries, dict, "Should return dict even with empty input")

    def test_infrastructure_detector_error_handling(self):
        """Test infrastructure detector with malformed input"""
        detector = InfrastructureDetector()
        
        # Test with None AST
        infrastructure = detector.detect_infrastructure(None, "test.py", "")
        self.assertIsInstance(infrastructure, dict, "Should return dict even with None AST")

    def test_weight_calculator_error_handling(self):
        """Test weight calculator with malformed input"""
        calculator = WeightCalculator()
        
        # Test with empty inputs
        weighted_nodes, weighted_edges = calculator.calculate_weights({}, [], {})
        self.assertIsInstance(weighted_nodes, dict, "Should return dict for empty input")
        self.assertIsInstance(weighted_edges, list, "Should return list for empty input")

    def test_graph_building_with_no_edges(self):
        """Test graph building when no relationships exist"""
        # Create indexer with no edges
        indexer = CodeGraphIndexer(self.test_db)
        
        # Add a single node
        node_id = indexer._create_node(
            node_type='isolated',
            name='isolated_node',
            path='/test/isolated.py',
            summary='Isolated node'
        )
        
        # Build graph
        graph = indexer.build_graph()
        self.assertEqual(graph.number_of_nodes(), 1, "Should have one node")
        self.assertEqual(graph.number_of_edges(), 0, "Should have no edges")

    def test_importance_calculation_with_empty_graph(self):
        """Test importance calculation with empty graph"""
        indexer = CodeGraphIndexer(self.test_db)
        
        # Create empty graph
        import networkx as nx
        empty_graph = nx.DiGraph()
        
        # Should not crash
        indexer.calculate_importance_scores(empty_graph)

    def test_concurrent_access(self):
        """Test handling of concurrent database access"""
        # Create two indexers pointing to same database
        indexer1 = CodeGraphIndexer(self.test_db)
        indexer2 = CodeGraphIndexer(self.test_db)
        
        # Add data to both
        indexer1._create_node('test1', 'node1', '/path1', 'Test 1')
        indexer2._create_node('test2', 'node2', '/path2', 'Test 2')
        
        # Both should be able to save (second one overwrites)
        result1 = indexer1.save_to_db()
        result2 = indexer2.save_to_db()
        
        self.assertTrue(result1 or result2, "At least one save should succeed")


class TestRecoveryScenarios(unittest.TestCase):
    """Test recovery from various failure scenarios"""

    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.test_db = os.path.join(self.test_dir, "test_recovery.db")
        
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir)

    def test_partial_indexing_recovery(self):
        """Test recovery from partial indexing failure"""
        indexer = CodeGraphIndexer(self.test_db)
        
        # Create test files
        test_files = []
        for i in range(5):
            test_file = os.path.join(self.test_dir, f"test_{i}.py")
            with open(test_file, 'w') as f:
                if i == 2:  # Make one file invalid
                    f.write("Invalid Python {{{")
                else:
                    f.write(f"def function_{i}(): pass\n")
            test_files.append(test_file)
        
        # Should handle partial failures
        for test_file in test_files:
            indexer.parse_python_file(test_file)
        
        # Should have indexed valid files
        self.assertGreater(len(indexer.nodes), 0, "Should have indexed some files")

    def test_database_recovery_after_corruption(self):
        """Test recovery after database corruption"""
        # Create valid database first
        indexer1 = CodeGraphIndexer(self.test_db)
        indexer1._create_node('test', 'node', '/path', 'Test')
        indexer1.save_to_db()
        
        # Simulate corruption by writing invalid data
        with open(self.test_db, 'a') as f:
            f.write("CORRUPTED DATA")
        
        # New indexer should handle corruption gracefully
        try:
            indexer2 = CodeGraphIndexer(self.test_db)
            # May fail, but should not crash the application
        except Exception as e:
            self.assertIsInstance(e, (sqlite3.DatabaseError, sqlite3.Error))


if __name__ == '__main__':
    unittest.main()