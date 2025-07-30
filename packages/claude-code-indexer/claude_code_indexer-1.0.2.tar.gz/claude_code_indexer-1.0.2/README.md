# Claude Code Indexer

A powerful code indexing tool that uses graph databases to analyze and understand code structure. Built specifically for Claude Code assistant workflows.

## Features

- 📊 **Graph-based code analysis** using Ensmallen library
- 🔍 **Intelligent node ranking** based on importance and centrality
- 💾 **SQLite database** for persistent storage
- 🎯 **Relevance tagging** for different code entity types
- 📈 **Network analysis** with PageRank and centrality measures
- 🚀 **Easy CLI interface** for quick setup and usage

## Installation

### From PyPI (Recommended)

```bash
pip install claude-code-indexer
```

### From Source

```bash
git clone https://github.com/anthropics/claude-code-indexer.git
cd claude-code-indexer
pip install -e .
```

### Updating

The package includes auto-update functionality:

```bash
# Check for updates
claude-code-indexer update --check-only

# Update to latest version
claude-code-indexer update

# Sync CLAUDE.md with latest template
claude-code-indexer sync
```

Updates will also be checked automatically when you run any command.

## Quick Start

### 1. Initialize in your project

```bash
cd your-project
claude-code-indexer init
```

This will:
- Create or update your `CLAUDE.md` file with indexing instructions
- Initialize the SQLite database
- Add database to `.gitignore`

### 2. Index your codebase

```bash
# Index current directory
claude-code-indexer index .

# Index specific directory
claude-code-indexer index /path/to/your/code

# Index with custom patterns
claude-code-indexer index . --patterns "*.py,*.js,*.ts"
```

### 3. Query your code

```bash
# Show most important code entities
claude-code-indexer query --important

# Show all entities of specific type
claude-code-indexer query --type class

# Search for specific terms
claude-code-indexer search "UserModel"

# View indexing statistics
claude-code-indexer stats
```

## CLI Commands

### `init`
Initialize Claude Code Indexer in current directory.

```bash
claude-code-indexer init [--force]
```

Options:
- `--force`: Overwrite existing configuration

### `index`
Index source code in specified directory.

```bash
claude-code-indexer index PATH [options]
```

Options:
- `--patterns`: File patterns to index (default: "*.py")
- `--db`: Database file path (default: "code_index.db")

### `query`
Query indexed code entities.

```bash
claude-code-indexer query [options]
```

Options:
- `--important`: Show only important nodes
- `--type`: Filter by node type (file, class, method, function)
- `--limit`: Maximum number of results (default: 20)
- `--db`: Database file path

### `search`
Search for code entities by name.

```bash
claude-code-indexer search TERM [options]
```

### `stats`
Show indexing statistics.

```bash
claude-code-indexer stats [--db DATABASE]
```

## Database Schema

The tool creates a SQLite database with the following structure:

### code_nodes
Stores information about code entities.

```sql
CREATE TABLE code_nodes (
    id INTEGER PRIMARY KEY,
    node_type TEXT,           -- 'file', 'class', 'method', 'function', 'import'
    name TEXT,                -- Entity name
    path TEXT,                -- File path
    summary TEXT,             -- Description
    importance_score REAL,    -- 0.0 to 1.0
    relevance_tags TEXT,      -- JSON array of tags
    created_at TIMESTAMP
);
```

### relationships
Stores relationships between code entities.

```sql
CREATE TABLE relationships (
    source_id INTEGER,
    target_id INTEGER,
    relationship_type TEXT,   -- 'imports', 'contains', 'calls', 'inherits'
    weight REAL,
    created_at TIMESTAMP
);
```

## Integration with Claude Code

After running `claude-code-indexer init`, your `CLAUDE.md` file will include:

- Complete setup instructions
- Database schema documentation
- CLI command reference
- Usage examples for Claude Code workflows

## Graph Analysis Features

### Node Importance Scoring
- **Degree centrality**: Based on number of connections
- **PageRank**: Overall importance in the dependency graph
- **Weighted scoring**: Combines multiple centrality measures

### Relevance Tags
- `structural`: Classes and main components
- `highly-used`: Entities with many incoming dependencies
- `complex`: Entities with many outgoing dependencies
- `test`: Test-related code
- `module`: File-level entities

### Advanced Analysis
- **Hub detection**: Find central components in your architecture
- **Dependency tracking**: Understand code relationships
- **Impact analysis**: Trace how changes propagate
- **Similarity detection**: Find related code patterns

## Examples

### Basic Usage

```python
from claude_code_indexer import CodeGraphIndexer

# Create indexer
indexer = CodeGraphIndexer("my_project.db")

# Index a directory
indexer.index_directory("./src")

# Query important nodes
important_nodes = indexer.query_important_nodes(min_score=0.5)
for node in important_nodes:
    print(f"{node['name']} ({node['node_type']}): {node['importance_score']}")
```

### Advanced Analysis

```python
# Get graph statistics
stats = indexer.get_stats()
print(f"Total nodes: {stats['total_nodes']}")
print(f"Node types: {stats['node_types']}")

# Build NetworkX graph for custom analysis
nx_graph = indexer.build_graph()
import networkx as nx
centrality = nx.betweenness_centrality(nx_graph)
```

## Requirements

- Python 3.8+
- ensmallen >= 0.8.0
- networkx >= 3.0
- pandas >= 1.5.0
- click >= 8.0.0
- rich >= 13.0.0

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

- 📖 [Documentation](https://docs.anthropic.com/claude-code)
- 🐛 [Issues](https://github.com/claude-ai/code-indexer/issues)
- 💬 [Discussions](https://github.com/claude-ai/code-indexer/discussions)