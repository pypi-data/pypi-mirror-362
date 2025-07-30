#!/usr/bin/env python3
"""
Integration tests for the complete indexing workflow
"""

import unittest
import tempfile
import os
import shutil
from pathlib import Path

from claude_code_indexer.indexer import CodeGraphIndexer


class TestIntegration(unittest.TestCase):
    """Test complete indexing workflow"""

    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.test_db = os.path.join(self.test_dir, "test_integration.db")
        self.indexer = CodeGraphIndexer(self.test_db)
        
        # Create test project structure
        self.create_test_project()
        
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir)

    def create_test_project(self):
        """Create a realistic test project structure"""
        # Main module
        main_py = os.path.join(self.test_dir, "main.py")
        with open(main_py, 'w') as f:
            f.write('''
import os
import json
from utils import helper_function
from models import User, Product

class Application:
    def __init__(self):
        self.users = []
        self.products = []
    
    def run(self):
        user = User("test")
        product = Product("item", 10.0)
        helper_function(user, product)

if __name__ == "__main__":
    app = Application()
    app.run()
''')
        
        # Utils module
        utils_py = os.path.join(self.test_dir, "utils.py")
        with open(utils_py, 'w') as f:
            f.write('''
import logging
from typing import List, Dict

def helper_function(user, product):
    """Helper function for processing"""
    logging.info(f"Processing {user} and {product}")
    return True

class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

class DataProcessor:
    def process(self, data: List[Dict]) -> Dict:
        return {"processed": len(data)}
''')
        
        # Models module
        models_py = os.path.join(self.test_dir, "models.py")
        with open(models_py, 'w') as f:
            f.write('''
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class User:
    name: str
    email: str = ""
    
    def get_info(self):
        return f"User: {self.name}"

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price
    
    def __str__(self):
        return f"Product({self.name}, ${self.price})"

class Observer(ABC):
    @abstractmethod
    def update(self, data):
        pass

class UserObserver(Observer):
    def update(self, user_data):
        print(f"User updated: {user_data}")
''')
        
        # Database module
        database_py = os.path.join(self.test_dir, "database.py")
        with open(database_py, 'w') as f:
            f.write('''
import sqlite3
import psycopg2
from redis import Redis

class DatabaseManager:
    def __init__(self):
        self.sqlite_conn = sqlite3.connect("app.db")
        self.postgres_conn = psycopg2.connect("postgresql://user:pass@localhost/db")
        self.redis_client = Redis(host='localhost', port=6379)
    
    def save_user(self, user):
        cursor = self.sqlite_conn.cursor()
        cursor.execute("INSERT INTO users VALUES (?, ?)", (user.name, user.email))
        self.sqlite_conn.commit()
''')
        
        # API module
        api_py = os.path.join(self.test_dir, "api.py")
        with open(api_py, 'w') as f:
            f.write('''
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify({"users": []})

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    return jsonify({"created": True})

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
    
    def get(self, endpoint):
        response = requests.get(f"{self.base_url}/{endpoint}")
        return response.json()
''')
        
        # Test module
        test_py = os.path.join(self.test_dir, "test_example.py")
        with open(test_py, 'w') as f:
            f.write('''
import unittest
from unittest.mock import Mock, patch
from models import User, Product

class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User("test_user")
    
    def test_user_creation(self):
        self.assertEqual(self.user.name, "test_user")
    
    @patch('models.User.get_info')
    def test_user_info(self, mock_info):
        mock_info.return_value = "mocked"
        result = self.user.get_info()
        self.assertEqual(result, "mocked")

if __name__ == '__main__':
    unittest.main()
''')

    def test_complete_indexing_workflow(self):
        """Test the complete indexing workflow"""
        # Index the test project
        self.indexer.index_directory(self.test_dir)
        
        # Verify basic structure
        self.assertGreater(len(self.indexer.nodes), 0, "Should have indexed nodes")
        self.assertGreater(len(self.indexer.edges), 0, "Should have relationships")
        
        # Check specific node types
        node_types = [node['node_type'] for node in self.indexer.nodes.values()]
        expected_types = ['file', 'class', 'function', 'method', 'import']
        
        for expected_type in expected_types:
            self.assertIn(expected_type, node_types, f"Should have {expected_type} nodes")

    def test_pattern_detection_integration(self):
        """Test that patterns are detected and stored"""
        self.indexer.index_directory(self.test_dir)
        
        # Check if Singleton pattern was detected
        import sqlite3
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM patterns WHERE pattern_type = 'Singleton'")
        singleton_patterns = cursor.fetchall()
        
        # Should detect Singleton pattern in utils.py
        self.assertGreater(len(singleton_patterns), 0, "Should detect Singleton pattern")
        
        conn.close()

    def test_library_detection_integration(self):
        """Test that libraries are detected and categorized"""
        self.indexer.index_directory(self.test_dir)
        
        import sqlite3
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        
        cursor.execute("SELECT DISTINCT category FROM libraries")
        categories = [row[0] for row in cursor.fetchall()]
        
        # Should detect different library categories
        expected_categories = ['web', 'database', 'testing']
        for category in expected_categories:
            if category in categories:
                break
        else:
            self.fail("Should detect at least one known library category")
        
        conn.close()

    def test_infrastructure_detection_integration(self):
        """Test that infrastructure components are detected"""
        self.indexer.index_directory(self.test_dir)
        
        import sqlite3
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        
        cursor.execute("SELECT DISTINCT component_type FROM infrastructure")
        components = [row[0] for row in cursor.fetchall()]
        
        # Should detect database and API components
        expected_components = ['database', 'api']
        for component in expected_components:
            if component in components:
                break
        else:
            self.fail("Should detect infrastructure components")
        
        conn.close()

    def test_importance_scoring_integration(self):
        """Test that importance scores are calculated correctly"""
        self.indexer.index_directory(self.test_dir)
        
        # Find highly used components
        important_nodes = []
        for node in self.indexer.nodes.values():
            if node['importance_score'] > 0.1:
                important_nodes.append(node)
        
        self.assertGreater(len(important_nodes), 0, "Should have important nodes")
        
        # Check that classes have structural tag
        structural_nodes = []
        for node in self.indexer.nodes.values():
            if 'structural' in node['relevance_tags']:
                structural_nodes.append(node)
        
        self.assertGreater(len(structural_nodes), 0, "Should have structural nodes")

    def test_weight_calculation_integration(self):
        """Test that weights are calculated based on usage"""
        self.indexer.index_directory(self.test_dir)
        
        # Check that nodes have weight information
        weighted_nodes = []
        for node in self.indexer.nodes.values():
            if 'weight' in node and node['weight'] > 0:
                weighted_nodes.append(node)
        
        # Should have at least some weighted nodes
        self.assertGreater(len(weighted_nodes), 0, "Should have nodes with weights")

    def test_query_functionality_integration(self):
        """Test querying functionality after indexing"""
        self.indexer.index_directory(self.test_dir)
        
        # Test querying important nodes
        important_nodes = self.indexer.query_important_nodes(min_score=0.0, limit=10)
        self.assertGreater(len(important_nodes), 0, "Should return important nodes")
        
        # Test getting stats
        stats = self.indexer.get_stats()
        self.assertIn('total_nodes', stats, "Stats should include node count")
        self.assertIn('total_edges', stats, "Stats should include edge count")
        self.assertIn('node_types', stats, "Stats should include node types")

    def test_database_persistence_integration(self):
        """Test that data persists across indexer instances"""
        # Index with first indexer
        self.indexer.index_directory(self.test_dir)
        initial_stats = self.indexer.get_stats()
        
        # Create new indexer instance
        new_indexer = CodeGraphIndexer(self.test_db)
        new_stats = new_indexer.get_stats()
        
        # Data should persist
        self.assertEqual(
            initial_stats.get('total_nodes'),
            new_stats.get('total_nodes'),
            "Node count should persist"
        )

    def test_incremental_indexing_simulation(self):
        """Test behavior when indexing the same directory multiple times"""
        # Index once
        self.indexer.index_directory(self.test_dir)
        first_stats = self.indexer.get_stats()
        
        # Index again (should replace data)
        self.indexer.index_directory(self.test_dir)
        second_stats = self.indexer.get_stats()
        
        # Should have consistent results
        self.assertEqual(
            first_stats.get('total_nodes'),
            second_stats.get('total_nodes'),
            "Should have consistent results on re-indexing"
        )


if __name__ == '__main__':
    unittest.main()