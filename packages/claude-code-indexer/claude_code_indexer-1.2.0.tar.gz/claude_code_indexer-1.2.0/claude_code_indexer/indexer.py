#!/usr/bin/env python3
"""
Code Graph Indexer using Ensmallen
"""

import ast
import os
import sqlite3
import json
import time
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional
import networkx as nx
import pandas as pd
from ensmallen import Graph
from .pattern_detector import PatternDetector
from .library_detector import LibraryDetector
from .infrastructure_detector import InfrastructureDetector
from .weight_calculator import WeightCalculator
from .db_optimizer import OptimizedDatabase, time_it
from .parallel_processor import ParallelFileProcessor, ProcessingStats
from .cache_manager import CacheManager, IncrementalIndexer


class CodeGraphIndexer:
    """Main code indexing class using Ensmallen graph database"""
    
    def __init__(self, db_path: str = "code_index.db", use_cache: bool = True, 
                 parallel_workers: int = None, enable_optimizations: bool = True):
        self.db_path = db_path
        self.nodes = {}  # node_id -> node_info
        self.edges = []  # List of (source, target, edge_type)
        self.node_counter = 0
        self.pattern_detector = PatternDetector()
        self.library_detector = LibraryDetector()
        self.infrastructure_detector = InfrastructureDetector()
        self.weight_calculator = WeightCalculator()
        self.all_files_content = {}  # Store file contents for weight calculation
        
        # Performance optimizations
        self.use_cache = use_cache
        self.enable_optimizations = enable_optimizations
        
        if self.use_cache:
            self.cache_manager = CacheManager()
            self.incremental_indexer = IncrementalIndexer(self.cache_manager)
        
        if self.enable_optimizations:
            self.optimized_db = OptimizedDatabase(db_path)
        
        self.parallel_processor = ParallelFileProcessor(max_workers=parallel_workers)
        self.processing_stats = ProcessingStats()
        
        self.init_db()
    
    def init_db(self):
        """Initialize SQLite database with schema and handle migrations"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if database exists and needs migration
        self._migrate_database_schema(cursor)
        
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
            weight REAL,
            frequency_score REAL,
            usage_stats TEXT,
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
        
        # Patterns table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS patterns (
            id INTEGER PRIMARY KEY,
            file_path TEXT,
            pattern_type TEXT,
            confidence REAL,
            description TEXT,
            nodes TEXT,
            location TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Libraries table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS libraries (
            id INTEGER PRIMARY KEY,
            file_path TEXT,
            name TEXT,
            version TEXT,
            category TEXT,
            usage_count INTEGER,
            usage_contexts TEXT,
            import_statements TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Infrastructure table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS infrastructure (
            id INTEGER PRIMARY KEY,
            file_path TEXT,
            component_type TEXT,
            name TEXT,
            technology TEXT,
            configuration TEXT,
            usage_frequency INTEGER,
            connections TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def _integrate_cached_result(self, cached_result):
        """Integrate cached processing result into current indexing session"""
        try:
            # Store file content for weight calculation
            with open(cached_result.file_path, 'r', encoding='utf-8') as f:
                self.all_files_content[cached_result.file_path] = f.read()
            
            # Integrate nodes
            for node_id, node_data in cached_result.nodes.items():
                new_id = self.node_counter
                self.nodes[new_id] = node_data.copy()
                self.nodes[new_id]['id'] = new_id
                self.node_counter += 1
            
            # Integrate edges (need to remap node IDs)
            node_id_mapping = {}
            start_id = self.node_counter - len(cached_result.nodes)
            for i, old_id in enumerate(cached_result.nodes.keys()):
                node_id_mapping[old_id] = start_id + i
            
            for edge in cached_result.edges:
                source, target, edge_type = edge
                if source in node_id_mapping and target in node_id_mapping:
                    self.edges.append((
                        node_id_mapping[source], 
                        node_id_mapping[target], 
                        edge_type
                    ))
        except Exception as e:
            print(f"Warning: Failed to integrate cached result for {cached_result.file_path}: {e}")
    
    def _integrate_processing_result(self, result):
        """Integrate parallel processing result into current indexing session"""
        # Store file content
        try:
            with open(result.file_path, 'r', encoding='utf-8') as f:
                self.all_files_content[result.file_path] = f.read()
        except:
            pass
        
        # Integrate nodes
        node_id_mapping = {}
        for old_id, node_data in result.nodes.items():
            new_id = self.node_counter
            self.nodes[new_id] = node_data.copy()
            self.nodes[new_id]['id'] = new_id
            node_id_mapping[old_id] = new_id
            self.node_counter += 1
        
        # Integrate edges with remapped IDs
        for edge in result.edges:
            source, target, edge_type = edge
            if source in node_id_mapping and target in node_id_mapping:
                self.edges.append((
                    node_id_mapping[source], 
                    node_id_mapping[target], 
                    edge_type
                ))
    
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
        
        # Store content for weight calculation
        self.all_files_content[file_path] = content
        
        # Check for null bytes (binary files)
        if '\x00' in content:
            print(f"Warning: Binary file detected {file_path}, skipping")
            return {}
        
        try:
            tree = ast.parse(content)
        except (SyntaxError, ValueError) as e:
            print(f"Warning: Cannot parse {file_path}: {e}")
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
        
        # Detect patterns
        patterns = self.pattern_detector.detect_patterns(tree, file_path)
        self._store_patterns(patterns, file_path)
        
        # Detect libraries
        libraries = self.library_detector.detect_libraries(tree, file_path, content)
        self._store_libraries(libraries, file_path)
        
        # Detect infrastructure
        infrastructure = self.infrastructure_detector.detect_infrastructure(tree, file_path, content)
        self._store_infrastructure(infrastructure, file_path)
        
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
        """Save nodes and relationships to SQLite database with error handling"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
        except sqlite3.Error as e:
            print(f"❌ Error connecting to database: {e}")
            return False
        
        try:
            # Clear existing data safely
            tables_to_clear = ["relationships", "code_nodes", "patterns", "libraries", "infrastructure"]
            for table in tables_to_clear:
                try:
                    cursor.execute(f"DELETE FROM {table}")
                except sqlite3.Error as e:
                    print(f"Warning: Could not clear table {table}: {e}")
            
            # Insert nodes with error handling
            for node_id, node_info in self.nodes.items():
                try:
                    cursor.execute('''
                    INSERT INTO code_nodes (id, node_type, name, path, summary, importance_score, relevance_tags, weight, frequency_score, usage_stats)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        node_info['id'],
                        node_info['node_type'],
                        node_info['name'],
                        node_info['path'],
                        node_info['summary'],
                        node_info['importance_score'],
                        json.dumps(node_info['relevance_tags']),
                        node_info.get('weight', 0.0),
                        node_info.get('frequency_score', 0.0),
                        json.dumps(node_info.get('usage_stats', {}))
                    ))
                except sqlite3.Error as e:
                    print(f"Warning: Could not insert node {node_id}: {e}")
                    # Try fallback insertion without new columns
                    try:
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
                    except sqlite3.Error as fallback_error:
                        print(f"Error: Could not insert node {node_id} even with fallback: {fallback_error}")
        
            # Insert edges with error handling
            for source, target, edge_type in self.edges:
                try:
                    cursor.execute('''
                    INSERT INTO relationships (source_id, target_id, relationship_type, weight)
                    VALUES (?, ?, ?, ?)
                    ''', (source, target, edge_type, 1.0))
                except sqlite3.Error as e:
                    print(f"Warning: Could not insert edge {source}->{target}: {e}")
            
            # Update metadata with error handling
            metadata_updates = [
                ('last_indexed', 'datetime("now")'),
                ('total_nodes', str(len(self.nodes))),
                ('total_edges', str(len(self.edges))),
                ('schema_version', '1.1.0')
            ]
            
            for key, value in metadata_updates:
                try:
                    if key == 'last_indexed':
                        cursor.execute('''
                        INSERT OR REPLACE INTO indexing_metadata (key, value)
                        VALUES (?, datetime('now'))
                        ''', (key,))
                    else:
                        cursor.execute('''
                        INSERT OR REPLACE INTO indexing_metadata (key, value)
                        VALUES (?, ?)
                        ''', (key, value))
                except sqlite3.Error as e:
                    print(f"Warning: Could not update metadata {key}: {e}")
            
            conn.commit()
            print("✅ Data saved successfully")
            return True
            
        except sqlite3.Error as e:
            print(f"❌ Database error during save: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error during save: {e}")
            return False
        finally:
            try:
                conn.close()
            except:
                pass
    
    @time_it
    def index_directory(self, directory: str, patterns: List[str] = None, force_reindex: bool = False):
        """Index all Python files in a directory with performance optimizations"""
        if patterns is None:
            patterns = ["*.py"]
        
        start_time = time.time()
        
        # Collect all Python files
        all_files = []
        for pattern in patterns:
            for file_path in Path(directory).rglob(pattern):
                if file_path.is_file():
                    all_files.append(str(file_path))
        
        if not all_files:
            print(f"No files found matching patterns {patterns} in {directory}")
            return
        
        print(f"🔍 Found {len(all_files)} Python files")
        
        # Use incremental indexing if cache is enabled
        files_to_process = all_files
        cached_results = []
        
        if self.use_cache and not force_reindex:
            print("📋 Checking cache for unchanged files...")
            cached_files, files_to_process = self.incremental_indexer.get_files_to_process(all_files)
            
            if cached_files:
                print(f"💾 Loading {len(cached_files)} files from cache")
                cached_results = self.incremental_indexer.load_cached_results(cached_files)
                
                # Integrate cached results
                for cached_result in cached_results:
                    self._integrate_cached_result(cached_result)
            
            print(f"🔄 Processing {len(files_to_process)} new/modified files")
        
        # Process files with parallel processing or sequentially
        if files_to_process:
            if len(files_to_process) > 3 and hasattr(self, 'parallel_processor'):
                # Use parallel processing for multiple files
                processing_results = self.parallel_processor.process_files_parallel(files_to_process)
                self.processing_stats.update(processing_results)
                
                # Integrate parallel results and cache them
                for result in processing_results:
                    if result.success:
                        self._integrate_processing_result(result)
                        
                        # Cache the result if caching is enabled
                        if self.use_cache:
                            self.cache_manager.cache_file_result(
                                result.file_path, result.nodes, result.edges,
                                result.patterns, result.libraries, result.infrastructure
                            )
            else:
                # Sequential processing for small number of files
                for file_path in files_to_process:
                    self.parse_python_file(file_path)
        
        total_indexed = len(all_files)
        
        if total_indexed == 0:
            print("No files to index")
            return
        
        print("🔗 Building graph...")
        graph = self.build_graph()
        
        print("⚖️  Calculating importance scores...")
        self.calculate_importance_scores(graph)
        
        print("📊 Calculating weights based on usage frequency...")
        weighted_nodes, weighted_edges = self.weight_calculator.calculate_weights(
            self.nodes, self.edges, self.all_files_content
        )
        
        # Update nodes with weight information
        for node_id, weighted_node in weighted_nodes.items():
            self.nodes[node_id].update(weighted_node)
        
        print("💾 Saving to database...")
        if not self.save_to_db():
            print("❌ Failed to save data to database")
            return False
        
        # Print performance stats
        processing_time = time.time() - start_time
        
        print(f"\n✅ Indexing Complete!")
        print(f"   📁 Total files: {total_indexed}")
        print(f"   💾 From cache: {len(cached_results)}")
        print(f"   🔄 Processed: {len(files_to_process)}")
        print(f"   🔗 Nodes: {len(self.nodes)}")
        print(f"   ↔️  Edges: {len(self.edges)}")
        print(f"   ⏱️  Time: {processing_time:.2f}s")
        print(f"   🚀 Speed: {total_indexed/processing_time:.1f} files/sec")
        print(f"   💾 Database: {self.db_path}")
        
        # Print processing stats if available
        if hasattr(self.processing_stats, 'print_stats') and files_to_process:
            self.processing_stats.print_stats()
        
        # Print cache stats if enabled
        if self.use_cache:
            self.cache_manager.print_cache_stats()
        
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
    
    def _store_patterns(self, patterns: List, file_path: str):
        """Store detected patterns in database"""
        if not patterns:
            return
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for pattern in patterns:
            cursor.execute('''
            INSERT INTO patterns (file_path, pattern_type, confidence, description, nodes, location)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                file_path,
                pattern.pattern_type,
                pattern.confidence,
                pattern.description,
                json.dumps(pattern.nodes),
                pattern.location
            ))
        
        conn.commit()
        conn.close()
    
    def _store_libraries(self, libraries: Dict, file_path: str):
        """Store detected libraries in database"""
        if not libraries:
            return
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for lib_name, lib_usage in libraries.items():
            cursor.execute('''
            INSERT INTO libraries (file_path, name, version, category, usage_count, usage_contexts, import_statements)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                file_path,
                lib_usage.name,
                lib_usage.version,
                lib_usage.category,
                lib_usage.usage_count,
                json.dumps(lib_usage.usage_contexts),
                json.dumps(lib_usage.import_statements)
            ))
        
        conn.commit()
        conn.close()
    
    def _store_infrastructure(self, infrastructure: Dict, file_path: str):
        """Store detected infrastructure in database"""
        if not infrastructure:
            return
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for category, components in infrastructure.items():
            for component in components:
                cursor.execute('''
                INSERT INTO infrastructure (file_path, component_type, name, technology, configuration, usage_frequency, connections)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    file_path,
                    component.component_type,
                    component.name,
                    component.technology,
                    json.dumps(component.configuration),
                    component.usage_frequency,
                    json.dumps(component.connections)
                ))
        
        conn.commit()
        conn.close()
    
    def _migrate_database_schema(self, cursor):
        """Migrate existing database schema to support new columns"""
        try:
            # Check if table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='code_nodes'")
            if not cursor.fetchone():
                return  # New database, no migration needed
            
            # Check existing columns
            cursor.execute("PRAGMA table_info(code_nodes)")
            existing_columns = [column[1] for column in cursor.fetchall()]
            
            # Add missing columns for v1.1.0
            new_columns = {
                'weight': 'REAL DEFAULT 0.0',
                'frequency_score': 'REAL DEFAULT 0.0', 
                'usage_stats': 'TEXT DEFAULT "{}"'
            }
            
            for column_name, column_def in new_columns.items():
                if column_name not in existing_columns:
                    try:
                        cursor.execute(f"ALTER TABLE code_nodes ADD COLUMN {column_name} {column_def}")
                        print(f"✓ Added column '{column_name}' to code_nodes table")
                    except sqlite3.Error as e:
                        print(f"Warning: Could not add column '{column_name}': {e}")
            
            # Migrate other tables if needed
            self._migrate_new_tables(cursor)
            
        except sqlite3.Error as e:
            print(f"Warning: Database migration failed: {e}")
    
    def _migrate_new_tables(self, cursor):
        """Create new tables introduced in v1.1.0"""
        new_tables = {
            'patterns': '''
                CREATE TABLE IF NOT EXISTS patterns (
                    id INTEGER PRIMARY KEY,
                    file_path TEXT,
                    pattern_type TEXT,
                    confidence REAL,
                    description TEXT,
                    nodes TEXT,
                    location TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'libraries': '''
                CREATE TABLE IF NOT EXISTS libraries (
                    id INTEGER PRIMARY KEY,
                    file_path TEXT,
                    name TEXT,
                    version TEXT,
                    category TEXT,
                    usage_count INTEGER,
                    usage_contexts TEXT,
                    import_statements TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'infrastructure': '''
                CREATE TABLE IF NOT EXISTS infrastructure (
                    id INTEGER PRIMARY KEY,
                    file_path TEXT,
                    component_type TEXT,
                    name TEXT,
                    technology TEXT,
                    configuration TEXT,
                    usage_frequency INTEGER,
                    connections TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            '''
        }
        
        for table_name, create_sql in new_tables.items():
            try:
                cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
                if not cursor.fetchone():
                    cursor.execute(create_sql)
                    print(f"✓ Created new table '{table_name}'")
            except sqlite3.Error as e:
                print(f"Warning: Could not create table '{table_name}': {e}")
    
    def _safe_database_operation(self, operation_func, *args, **kwargs):
        """Execute database operation with error handling"""
        try:
            return operation_func(*args, **kwargs)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None