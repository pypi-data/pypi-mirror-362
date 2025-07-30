#!/usr/bin/env python3
"""
Parallel processing for faster file indexing
"""

import asyncio
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Tuple
import ast
import os
from pathlib import Path
import time
from dataclasses import dataclass

from .pattern_detector import PatternDetector
from .library_detector import LibraryDetector
from .infrastructure_detector import InfrastructureDetector


@dataclass
class FileProcessingResult:
    """Result from processing a single file"""
    file_path: str
    nodes: Dict[int, Dict]
    edges: List[Tuple]
    patterns: List
    libraries: Dict
    infrastructure: Dict
    processing_time: float
    success: bool
    error_message: str = ""


class ParallelFileProcessor:
    """Process multiple files in parallel"""
    
    def __init__(self, max_workers: int = None):
        self.max_workers = max_workers or min(mp.cpu_count(), 8)
        self.pattern_detector = PatternDetector()
        self.library_detector = LibraryDetector()
        self.infrastructure_detector = InfrastructureDetector()
    
    def process_files_parallel(self, file_paths: List[str]) -> List[FileProcessingResult]:
        """Process multiple files in parallel using multiprocessing"""
        if len(file_paths) <= 2:
            # For small numbers, sequential is faster due to overhead
            return [self._process_single_file(fp) for fp in file_paths]
        
        print(f"🚀 Processing {len(file_paths)} files with {self.max_workers} workers...")
        
        # Split into chunks for better load balancing
        chunk_size = max(1, len(file_paths) // self.max_workers)
        file_chunks = [file_paths[i:i + chunk_size] 
                      for i in range(0, len(file_paths), chunk_size)]
        
        results = []
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_chunk = {
                executor.submit(process_file_chunk, chunk): chunk 
                for chunk in file_chunks
            }
            
            for future in as_completed(future_to_chunk):
                chunk_results = future.result()
                results.extend(chunk_results)
        
        return results
    
    async def process_files_async(self, file_paths: List[str]) -> List[FileProcessingResult]:
        """Process files asynchronously (for I/O bound operations)"""
        print(f"⚡ Processing {len(file_paths)} files asynchronously...")
        
        semaphore = asyncio.Semaphore(self.max_workers)
        
        async def process_with_semaphore(file_path):
            async with semaphore:
                return await asyncio.get_event_loop().run_in_executor(
                    None, self._process_single_file, file_path
                )
        
        tasks = [process_with_semaphore(fp) for fp in file_paths]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions
        valid_results = [r for r in results if isinstance(r, FileProcessingResult)]
        return valid_results
    
    def _process_single_file(self, file_path: str) -> FileProcessingResult:
        """Process a single Python file"""
        start_time = time.time()
        
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for binary files
            if '\x00' in content:
                return FileProcessingResult(
                    file_path=file_path,
                    nodes={}, edges=[], patterns=[], libraries={}, infrastructure={},
                    processing_time=time.time() - start_time,
                    success=False,
                    error_message="Binary file detected"
                )
            
            # Parse AST
            try:
                tree = ast.parse(content)
            except (SyntaxError, ValueError) as e:
                return FileProcessingResult(
                    file_path=file_path,
                    nodes={}, edges=[], patterns=[], libraries={}, infrastructure={},
                    processing_time=time.time() - start_time,
                    success=False,
                    error_message=f"Parse error: {e}"
                )
            
            # Extract basic nodes and edges
            nodes, edges = self._extract_nodes_and_edges(tree, file_path)
            
            # Run detectors
            patterns = self.pattern_detector.detect_patterns(tree, file_path)
            libraries = self.library_detector.detect_libraries(tree, file_path, content)
            infrastructure = self.infrastructure_detector.detect_infrastructure(tree, file_path, content)
            
            return FileProcessingResult(
                file_path=file_path,
                nodes=nodes,
                edges=edges,
                patterns=patterns,
                libraries=libraries,
                infrastructure=infrastructure,
                processing_time=time.time() - start_time,
                success=True
            )
            
        except Exception as e:
            return FileProcessingResult(
                file_path=file_path,
                nodes={}, edges=[], patterns=[], libraries={}, infrastructure={},
                processing_time=time.time() - start_time,
                success=False,
                error_message=f"Unexpected error: {e}"
            )
    
    def _extract_nodes_and_edges(self, tree: ast.AST, file_path: str) -> Tuple[Dict, List]:
        """Extract nodes and edges from AST (optimized version)"""
        nodes = {}
        edges = []
        node_counter = 0
        
        # Create file node
        file_node_id = node_counter
        nodes[file_node_id] = {
            'id': file_node_id,
            'node_type': 'file',
            'name': os.path.basename(file_path),
            'path': file_path,
            'summary': f"Python file: {os.path.basename(file_path)}",
            'importance_score': 0.0,
            'relevance_tags': []
        }
        node_counter += 1
        
        # Fast AST traversal
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    import_node_id = node_counter
                    nodes[import_node_id] = {
                        'id': import_node_id,
                        'node_type': 'import',
                        'name': alias.name,
                        'path': file_path,
                        'summary': f"Import: {alias.name}",
                        'importance_score': 0.0,
                        'relevance_tags': []
                    }
                    edges.append((file_node_id, import_node_id, 'imports'))
                    node_counter += 1
            
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    import_node_id = node_counter
                    nodes[import_node_id] = {
                        'id': import_node_id,
                        'node_type': 'import',
                        'name': node.module,
                        'path': file_path,
                        'summary': f"Import from: {node.module}",
                        'importance_score': 0.0,
                        'relevance_tags': []
                    }
                    edges.append((file_node_id, import_node_id, 'imports'))
                    node_counter += 1
            
            elif isinstance(node, ast.ClassDef):
                class_node_id = node_counter
                nodes[class_node_id] = {
                    'id': class_node_id,
                    'node_type': 'class',
                    'name': node.name,
                    'path': file_path,
                    'summary': f"Class: {node.name}",
                    'importance_score': 0.0,
                    'relevance_tags': []
                }
                edges.append((file_node_id, class_node_id, 'contains'))
                node_counter += 1
                
                # Extract methods
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        method_node_id = node_counter
                        nodes[method_node_id] = {
                            'id': method_node_id,
                            'node_type': 'method',
                            'name': f"{node.name}.{item.name}",
                            'path': file_path,
                            'summary': f"Method: {node.name}.{item.name}",
                            'importance_score': 0.0,
                            'relevance_tags': []
                        }
                        edges.append((class_node_id, method_node_id, 'contains'))
                        node_counter += 1
            
            elif isinstance(node, ast.FunctionDef):
                func_node_id = node_counter
                nodes[func_node_id] = {
                    'id': func_node_id,
                    'node_type': 'function',
                    'name': node.name,
                    'path': file_path,
                    'summary': f"Function: {node.name}",
                    'importance_score': 0.0,
                    'relevance_tags': []
                }
                edges.append((file_node_id, func_node_id, 'contains'))
                node_counter += 1
        
        return nodes, edges


def process_file_chunk(file_paths: List[str]) -> List[FileProcessingResult]:
    """Process a chunk of files (for multiprocessing)"""
    processor = ParallelFileProcessor()
    return [processor._process_single_file(fp) for fp in file_paths]


class ProcessingStats:
    """Track processing statistics"""
    
    def __init__(self):
        self.total_files = 0
        self.successful_files = 0
        self.failed_files = 0
        self.total_time = 0.0
        self.files_per_second = 0.0
    
    def update(self, results: List[FileProcessingResult]):
        """Update stats from processing results"""
        self.total_files = len(results)
        self.successful_files = sum(1 for r in results if r.success)
        self.failed_files = self.total_files - self.successful_files
        self.total_time = sum(r.processing_time for r in results)
        
        if self.total_time > 0:
            self.files_per_second = self.total_files / self.total_time
    
    def print_stats(self):
        """Print processing statistics"""
        print(f"📊 Processing Stats:")
        print(f"   Total files: {self.total_files}")
        print(f"   Successful: {self.successful_files}")
        print(f"   Failed: {self.failed_files}")
        print(f"   Total time: {self.total_time:.2f}s")
        print(f"   Speed: {self.files_per_second:.1f} files/sec")