## Code Indexing with Graph Database

### ⚠️ IMPORTANT: Claude Code Indexer is ALREADY IMPLEMENTED
**DO NOT re-implement code indexing functionality!** The `claude-code-indexer` package provides everything needed.

### Quick Start (Just Use These Commands!)
```bash
# 1. Install the package (if not already installed)
pip install claude-code-indexer

# 2. Initialize in current directory (auto-updates this file)
claude-code-indexer init

# 3. Index the codebase
claude-code-indexer index .

# 4. Use the indexed data
claude-code-indexer query --important  # Show key components
claude-code-indexer search <term>      # Search for specific code
claude-code-indexer stats              # View statistics
```

### What It Does
- **Automatically indexes** Python code using AST parsing
- **Builds graph database** with Ensmallen for relationships
- **Calculates importance** using PageRank and centrality
- **Stores in SQLite** for fast queries
- **No implementation needed** - just use the CLI commands!

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