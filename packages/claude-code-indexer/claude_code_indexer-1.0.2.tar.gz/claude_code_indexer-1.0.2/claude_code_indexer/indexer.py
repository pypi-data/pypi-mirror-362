#!/usr/bin/env python3
"""
Code Graph Indexer using Ensmallen
"""

import ast
import os
import sqlite3
import json
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional
import networkx as nx
import pandas as pd
from ensmallen import Graph


class CodeGraphIndexer:
    """Main code indexing class using Ensmallen graph database"""
    
    def __init__(self, db_path: str = "code_index.db"):
        self.db_path = db_path
        self.nodes = {}  # node_id -> node_info
        self.edges = []  # List of (source, target, edge_type)
        self.node_counter = 0
        self.init_db()
    
    def init_db(self):
        """Initialize SQLite database with schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS code_nodes (
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
        CREATE TABLE IF NOT EXISTS relationships (
            source_id INTEGER,
            target_id INTEGER,
            relationship_type TEXT,
            weight REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (source_id) REFERENCES code_nodes(id),
            FOREIGN KEY (target_id) REFERENCES code_nodes(id)
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS indexing_metadata (
            key TEXT PRIMARY KEY,
            value TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def parse_python_file(self, file_path: str) -> Dict:
        """Parse a Python file and extract code entities"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            # Try different encodings
            for encoding in ['latin-1', 'cp1252', 'utf-8-sig']:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            else:
                print(f"Warning: Could not decode {file_path}, skipping")
                return {}
        
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            print(f"Warning: Syntax error in {file_path}: {e}")
            return {}
        
        # Create file node
        file_node_id = self._create_node(
            node_type='file',
            name=os.path.basename(file_path),
            path=file_path,
            summary=f"Python file: {os.path.basename(file_path)}"
        )
        
        # Extract imports, classes, and functions
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    import_node_id = self._create_node(
                        node_type='import',
                        name=alias.name,
                        path=file_path,
                        summary=f"Import: {alias.name}"
                    )
                    self.edges.append((file_node_id, import_node_id, 'imports'))
            
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    import_node_id = self._create_node(
                        node_type='import',
                        name=node.module,
                        path=file_path,
                        summary=f"Import from: {node.module}"
                    )
                    self.edges.append((file_node_id, import_node_id, 'imports'))
            
            elif isinstance(node, ast.ClassDef):
                class_node_id = self._create_node(
                    node_type='class',
                    name=node.name,
                    path=file_path,
                    summary=f"Class: {node.name}"
                )
                self.edges.append((file_node_id, class_node_id, 'contains'))
                
                # Extract methods
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        method_node_id = self._create_node(
                            node_type='method',
                            name=f"{node.name}.{item.name}",
                            path=file_path,
                            summary=f"Method: {node.name}.{item.name}"
                        )
                        self.edges.append((class_node_id, method_node_id, 'contains'))
            
            elif isinstance(node, ast.FunctionDef):
                func_node_id = self._create_node(
                    node_type='function',
                    name=node.name,
                    path=file_path,
                    summary=f"Function: {node.name}"
                )
                self.edges.append((file_node_id, func_node_id, 'contains'))
        
        return self.nodes
    
    def _create_node(self, node_type: str, name: str, path: str, summary: str) -> int:
        """Create a node and return its ID"""
        node_id = self.node_counter
        self.nodes[node_id] = {
            'id': node_id,
            'node_type': node_type,
            'name': name,
            'path': path,
            'summary': summary,
            'importance_score': 0.0,
            'relevance_tags': []
        }
        self.node_counter += 1
        return node_id
    
    def build_graph(self) -> nx.DiGraph:
        """Build NetworkX graph from nodes and edges"""
        nx_graph = nx.DiGraph()
        
        # Add nodes
        for node_id, node_info in self.nodes.items():
            nx_graph.add_node(
                node_id,
                node_type=node_info['node_type'],
                name=node_info['name']
            )
        
        # Add edges
        for source, target, edge_type in self.edges:
            nx_graph.add_edge(source, target, edge_type=edge_type)
        
        return nx_graph
    
    def build_ensmallen_graph(self) -> Optional[Graph]:
        """Build Ensmallen graph for advanced analysis"""
        if not self.edges:
            return None
        
        # Prepare edge data
        edges_data = []
        for source, target, edge_type in self.edges:
            edges_data.append([f"node_{source}", f"node_{target}"])
        
        # Save to temporary file
        edges_df = pd.DataFrame(edges_data, columns=["source", "destination"])
        temp_file = "temp_edges.tsv"
        edges_df.to_csv(temp_file, index=False, sep="\t", header=False)
        
        try:
            # Create ensmallen graph
            graph = Graph.from_csv(
                edge_path=temp_file,
                directed=True,
                verbose=False
            )
            return graph
        except Exception as e:
            print(f"Warning: Could not create Ensmallen graph: {e}")
            return None
        finally:
            # Clean up
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def calculate_importance_scores(self, graph: nx.DiGraph):
        """Calculate importance scores for nodes using graph metrics"""
        # Calculate various centrality measures
        in_degree_centrality = nx.in_degree_centrality(graph)
        out_degree_centrality = nx.out_degree_centrality(graph)
        
        # Calculate PageRank for importance
        try:
            pagerank = nx.pagerank(graph, alpha=0.85)
        except:
            pagerank = {node: 0.0 for node in graph.nodes()}
        
        # Update node importance scores
        for node_id in self.nodes:
            if node_id in graph:
                # Combine different metrics
                in_score = in_degree_centrality.get(node_id, 0.0)
                out_score = out_degree_centrality.get(node_id, 0.0)
                pr_score = pagerank.get(node_id, 0.0)
                
                # Weighted importance score
                importance_score = (
                    0.4 * in_score +  # How many depend on this
                    0.2 * out_score + # Complexity
                    0.4 * pr_score    # Overall importance
                )
                
                self.nodes[node_id]['importance_score'] = min(importance_score, 1.0)
                
                # Add relevance tags
                tags = []
                if self.nodes[node_id]['node_type'] == 'class':
                    tags.append('structural')
                if graph.in_degree(node_id) > 3:
                    tags.append('highly-used')
                if graph.out_degree(node_id) > 3:
                    tags.append('complex')
                if 'test' in self.nodes[node_id]['name'].lower():
                    tags.append('test')
                if self.nodes[node_id]['node_type'] == 'file':
                    tags.append('module')
                
                self.nodes[node_id]['relevance_tags'] = tags
            else:
                self.nodes[node_id]['importance_score'] = 0.0
                self.nodes[node_id]['relevance_tags'] = []
    
    def save_to_db(self):
        """Save nodes and relationships to SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Clear existing data
        cursor.execute("DELETE FROM relationships")
        cursor.execute("DELETE FROM code_nodes")
        
        # Insert nodes
        for node_id, node_info in self.nodes.items():
            cursor.execute('''
            INSERT INTO code_nodes (id, node_type, name, path, summary, importance_score, relevance_tags)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                node_info['id'],
                node_info['node_type'],
                node_info['name'],
                node_info['path'],
                node_info['summary'],
                node_info['importance_score'],
                json.dumps(node_info['relevance_tags'])
            ))
        
        # Insert edges
        for source, target, edge_type in self.edges:
            cursor.execute('''
            INSERT INTO relationships (source_id, target_id, relationship_type, weight)
            VALUES (?, ?, ?, ?)
            ''', (source, target, edge_type, 1.0))
        
        # Update metadata
        cursor.execute('''
        INSERT OR REPLACE INTO indexing_metadata (key, value)
        VALUES ('last_indexed', datetime('now'))
        ''')
        
        cursor.execute('''
        INSERT OR REPLACE INTO indexing_metadata (key, value)
        VALUES ('total_nodes', ?)
        ''', (len(self.nodes),))
        
        cursor.execute('''
        INSERT OR REPLACE INTO indexing_metadata (key, value)
        VALUES ('total_edges', ?)
        ''', (len(self.edges),))
        
        conn.commit()
        conn.close()
    
    def index_directory(self, directory: str, patterns: List[str] = None):
        """Index all Python files in a directory"""
        if patterns is None:
            patterns = ["*.py"]
        
        indexed_files = 0
        for pattern in patterns:
            for file_path in Path(directory).rglob(pattern):
                if file_path.is_file():
                    print(f"Indexing: {file_path}")
                    self.parse_python_file(str(file_path))
                    indexed_files += 1
        
        if indexed_files == 0:
            print(f"No files found matching patterns {patterns} in {directory}")
            return
        
        print("Building graph...")
        graph = self.build_graph()
        
        print("Calculating importance scores...")
        self.calculate_importance_scores(graph)
        
        print("Saving to database...")
        self.save_to_db()
        
        print(f"✓ Indexed {indexed_files} files")
        print(f"✓ Created {len(self.nodes)} nodes and {len(self.edges)} relationships")
        print(f"✓ Data saved to {self.db_path}")
        
        # Try to build Ensmallen graph for advanced features
        ensmallen_graph = self.build_ensmallen_graph()
        if ensmallen_graph:
            print(f"✓ Ensmallen graph ready for advanced analysis")
    
    def query_important_nodes(self, min_score: float = 0.1, limit: int = 20) -> List[Dict]:
        """Query nodes with high importance scores"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT * FROM code_nodes 
        WHERE importance_score >= ? 
        ORDER BY importance_score DESC
        LIMIT ?
        ''', (min_score, limit))
        
        columns = [description[0] for description in cursor.description]
        results = []
        for row in cursor.fetchall():
            node_dict = dict(zip(columns, row))
            node_dict['relevance_tags'] = json.loads(node_dict['relevance_tags'])
            results.append(node_dict)
        
        conn.close()
        return results
    
    def get_stats(self) -> Dict:
        """Get indexing statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # Get metadata
        cursor.execute('SELECT key, value FROM indexing_metadata')
        for key, value in cursor.fetchall():
            stats[key] = value
        
        # Get node type counts
        cursor.execute('SELECT node_type, COUNT(*) FROM code_nodes GROUP BY node_type')
        stats['node_types'] = dict(cursor.fetchall())
        
        # Get relationship type counts
        cursor.execute('SELECT relationship_type, COUNT(*) FROM relationships GROUP BY relationship_type')
        stats['relationship_types'] = dict(cursor.fetchall())
        
        conn.close()
        return stats