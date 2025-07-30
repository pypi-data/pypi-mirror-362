## Code Indexing with Graph Database

### Using Claude Code Indexer
- **Install**: `pip install claude-code-indexer`
- **Quick start**: `claude-code-indexer init` to setup in current directory
- **Index code**: `claude-code-indexer index .` to index current directory
- **Purpose**: Index source code as a graph structure for better navigation and analysis

### Graph Structure
- **Nodes**: Modules, Files, Classes, Methods, Functions
- **Edges**: Import relationships, Inheritance, Method calls, Dependencies

### Implementation Steps
1. **Install package**: `pip install claude-code-indexer`
2. **Initialize**: `claude-code-indexer init` (creates config and database)
3. **Index codebase**: `claude-code-indexer index /path/to/code`
4. **Query results**: `claude-code-indexer query --important` for key components
5. **View stats**: `claude-code-indexer stats` for overview

### SQLite Database Schema
```sql
-- Nodes table
CREATE TABLE code_nodes (
  id INTEGER PRIMARY KEY,
  node_type TEXT,  -- 'module', 'class', 'method', 'function'
  name TEXT,
  path TEXT,
  summary TEXT,
  importance_score REAL,  -- 0.0 to 1.0
  relevance_tags TEXT,    -- JSON array of tags
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Relationships table
CREATE TABLE relationships (
  source_id INTEGER,
  target_id INTEGER,
  relationship_type TEXT,  -- 'imports', 'calls', 'inherits', 'contains'
  weight REAL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### CLI Commands
- `claude-code-indexer init` - Initialize in current directory
- `claude-code-indexer index <path>` - Index code directory
- `claude-code-indexer query --important` - Show important nodes
- `claude-code-indexer stats` - Show indexing statistics
- `claude-code-indexer search <term>` - Search for code entities

### Node Importance Ranking
- **Degree centrality**: Number of connections (in/out)
- **PageRank**: Overall importance in graph
- **Usage frequency**: How often referenced
- **Centrality measures**: Hub detection

### Relevance Tagging
- **structural**: Classes and core components
- **highly-used**: Nodes with many incoming edges
- **complex**: Nodes with many outgoing edges
- **test**: Test-related code
- **module**: File-level nodes

### Advanced Features
- **Ensmallen integration**: Graph embeddings and similarity
- **Code similarity**: Find similar components
- **Impact analysis**: Trace changes through codebase
- **Architecture visualization**: Understand code structure