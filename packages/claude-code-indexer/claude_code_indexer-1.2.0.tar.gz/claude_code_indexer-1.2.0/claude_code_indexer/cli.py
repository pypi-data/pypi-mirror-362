#!/usr/bin/env python3
"""
Command-line interface for Claude Code Indexer
"""

import click
import os
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from rich.text import Text

from .indexer import CodeGraphIndexer
from .updater import Updater, check_and_notify_update
from . import __version__


console = Console()


@click.group()
@click.version_option(version=__version__)
def cli():
    """Claude Code Indexer - Index source code as graph database"""
    pass


@cli.command()
@click.option('--force', is_flag=True, help='Force overwrite existing files')
def init(force):
    """Initialize Claude Code Indexer in current directory"""
    cwd = Path.cwd()
    claude_md_path = cwd / "CLAUDE.md"
    
    console.print("🚀 [bold blue]Initializing Claude Code Indexer...[/bold blue]")
    
    # Check if CLAUDE.md exists
    if claude_md_path.exists():
        console.print(f"✓ Found existing CLAUDE.md at {claude_md_path}")
        
        # Read existing content
        with open(claude_md_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()
        
        # Check if our section already exists
        if "## Code Indexing with Graph Database" in existing_content:
            if not force:
                console.print("⚠️  Code indexing section already exists in CLAUDE.md")
                console.print("Use --force to overwrite, or manually remove the section")
                return
            else:
                console.print("🔄 Updating existing section...")
                # Remove existing section
                lines = existing_content.split('\n')
                new_lines = []
                skip_section = False
                
                for line in lines:
                    if line.strip() == "## Code Indexing with Graph Database":
                        skip_section = True
                        continue
                    elif skip_section and line.startswith("## ") and "Code Indexing" not in line:
                        skip_section = False
                        new_lines.append(line)
                    elif not skip_section:
                        new_lines.append(line)
                
                existing_content = '\n'.join(new_lines)
        
        # Append our template
        template_path = Path(__file__).parent / "templates" / "claude_md_template.md"
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Combine content
        updated_content = existing_content.rstrip() + '\n\n' + template_content
        
        # Write back
        with open(claude_md_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        console.print("✓ Updated CLAUDE.md with code indexing instructions")
    
    else:
        console.print("⚠️  CLAUDE.md not found")
        create_new = click.confirm("Create new CLAUDE.md with code indexing setup?")
        
        if create_new:
            # Create new CLAUDE.md with basic structure
            template_path = Path(__file__).parent / "templates" / "claude_md_template.md"
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            basic_header = """# Claude Coding Assistant - Setup Rules

## Core Workflow Rules

1. **First think through the problem**, read the codebase for relevant files, and write a plan.
2. **Make every task and code change as simple as possible**.
3. **Prioritize simplicity over complexity**.

"""
            
            full_content = basic_header + template_content
            
            with open(claude_md_path, 'w', encoding='utf-8') as f:
                f.write(full_content)
            
            console.print(f"✓ Created new CLAUDE.md at {claude_md_path}")
        else:
            console.print("❌ Initialization cancelled")
            return
    
    # Create initial database
    indexer = CodeGraphIndexer()
    console.print("✓ Initialized code index database")
    
    # Create .gitignore entry
    gitignore_path = cwd / ".gitignore"
    gitignore_entry = "code_index.db"
    
    if gitignore_path.exists():
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            gitignore_content = f.read()
        
        if gitignore_entry not in gitignore_content:
            with open(gitignore_path, 'a', encoding='utf-8') as f:
                f.write(f"\n# Claude Code Indexer\n{gitignore_entry}\n")
            console.print("✓ Added code_index.db to .gitignore")
    else:
        with open(gitignore_path, 'w', encoding='utf-8') as f:
            f.write(f"# Claude Code Indexer\n{gitignore_entry}\n")
        console.print("✓ Created .gitignore with code_index.db")
    
    console.print("\n🎉 [bold green]Initialization complete![/bold green]")
    console.print("Next steps:")
    console.print("1. Run [bold]claude-code-indexer index .[/bold] to index current directory")
    console.print("2. Run [bold]claude-code-indexer query --important[/bold] to see key components")
    console.print("3. Run [bold]claude-code-indexer stats[/bold] to view indexing statistics")


@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--patterns', default="*.py", help='File patterns to index (comma-separated)')
@click.option('--db', default="code_index.db", help='Database file path')
@click.option('--no-cache', is_flag=True, help='Disable caching for faster re-indexing')
@click.option('--force', is_flag=True, help='Force re-index all files (ignore cache)')
@click.option('--workers', type=int, help='Number of parallel workers (default: auto)')
@click.option('--no-optimize', is_flag=True, help='Disable database optimizations')
@click.option('--benchmark', is_flag=True, help='Run performance benchmark')
def index(path, patterns, db, no_cache, force, workers, no_optimize, benchmark):
    """Index source code in the specified directory with performance optimizations"""
    console.print(f"📁 [bold blue]Indexing code in {path}...[/bold blue]")
    
    # Parse patterns
    pattern_list = [p.strip() for p in patterns.split(',')]
    
    # Show performance settings
    if not no_cache:
        console.print("💾 [green]Caching enabled[/green] - unchanged files will be skipped")
    if not no_optimize:
        console.print("🚀 [green]Database optimizations enabled[/green] - using APSW and connection pooling")
    if workers:
        console.print(f"⚡ [green]Parallel processing enabled[/green] - using {workers} workers")
    elif not no_optimize:
        console.print("⚡ [green]Auto parallel processing enabled[/green] - workers will be determined automatically")
    
    # Run benchmark if requested
    if benchmark:
        from .db_optimizer import DatabaseBenchmark
        console.print("🔥 [yellow]Running performance benchmark...[/yellow]")
        DatabaseBenchmark.benchmark_insert_performance(db + "_benchmark")
    
    # Create indexer with performance options
    indexer = CodeGraphIndexer(
        db_path=db,
        use_cache=not no_cache,
        parallel_workers=workers,
        enable_optimizations=not no_optimize
    )
    
    # Index with progress
    with Progress() as progress:
        task = progress.add_task("Indexing files...", total=None)
        
        try:
            indexer.index_directory(path, patterns=pattern_list, force_reindex=force)
            progress.update(task, completed=100)
        except Exception as e:
            console.print(f"❌ [bold red]Error during indexing: {e}[/bold red]")
            sys.exit(1)
    
    console.print(f"✅ [bold green]Indexing complete![/bold green]")


@cli.command()
@click.option('--important', is_flag=True, help='Show only important nodes')
@click.option('--type', help='Filter by node type (file, class, method, function)')
@click.option('--limit', default=20, help='Maximum number of results')
@click.option('--db', default="code_index.db", help='Database file path')
def query(important, type, limit, db):
    """Query indexed code entities"""
    if not os.path.exists(db):
        console.print("❌ [bold red]Database not found. Run 'claude-code-indexer index' first.[/bold red]")
        sys.exit(1)
    
    indexer = CodeGraphIndexer(db_path=db)
    
    if important:
        console.print("🔍 [bold blue]Most important code entities:[/bold blue]")
        nodes = indexer.query_important_nodes(min_score=0.1, limit=limit)
    else:
        console.print("📋 [bold blue]All code entities:[/bold blue]")
        nodes = indexer.query_important_nodes(min_score=0.0, limit=limit)
    
    if type:
        nodes = [n for n in nodes if n['node_type'] == type]
    
    if not nodes:
        console.print("No entities found matching criteria.")
        return
    
    # Create table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Name", style="bold")
    table.add_column("Type", style="cyan")
    table.add_column("Importance", style="green")
    table.add_column("Tags", style="yellow")
    table.add_column("Path", style="dim")
    
    for node in nodes:
        importance = f"{node['importance_score']:.3f}"
        tags = ", ".join(node['relevance_tags']) if node['relevance_tags'] else "-"
        table.add_row(
            node['name'],
            node['node_type'],
            importance,
            tags,
            node['path']
        )
    
    console.print(table)


@cli.command()
@click.argument('term')
@click.option('--db', default="code_index.db", help='Database file path')
def search(term, db):
    """Search for code entities by name"""
    if not os.path.exists(db):
        console.print("❌ [bold red]Database not found. Run 'claude-code-indexer index' first.[/bold red]")
        sys.exit(1)
    
    import sqlite3
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT name, node_type, path, importance_score, relevance_tags
    FROM code_nodes
    WHERE name LIKE ? OR summary LIKE ?
    ORDER BY importance_score DESC
    LIMIT 20
    ''', (f'%{term}%', f'%{term}%'))
    
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        console.print(f"No entities found matching '{term}'")
        return
    
    console.print(f"🔍 [bold blue]Search results for '{term}':[/bold blue]")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Name", style="bold")
    table.add_column("Type", style="cyan")
    table.add_column("Importance", style="green")
    table.add_column("Path", style="dim")
    
    for name, node_type, path, importance, tags in results:
        table.add_row(
            name,
            node_type,
            f"{importance:.3f}",
            path
        )
    
    console.print(table)


@cli.command()
@click.option('--db', default="code_index.db", help='Database file path')
@click.option('--cache', is_flag=True, help='Show cache statistics')
def stats(db, cache):
    """Show indexing statistics"""
    if not os.path.exists(db):
        console.print("❌ [bold red]Database not found. Run 'claude-code-indexer index' first.[/bold red]")
        sys.exit(1)
    
    # Show cache stats if requested
    if cache:
        from .cache_manager import CacheManager
        cache_manager = CacheManager()
        cache_manager.print_cache_stats()
        console.print()  # Add spacing
    
    indexer = CodeGraphIndexer(db_path=db)
    stats = indexer.get_stats()
    
    console.print("📊 [bold blue]Code Indexing Statistics[/bold blue]")
    
    # Basic stats
    info_table = Table(show_header=False, box=None)
    info_table.add_column("Metric", style="cyan")
    info_table.add_column("Value", style="bold green")
    
    info_table.add_row("Last indexed", stats.get('last_indexed', 'Never'))
    info_table.add_row("Total nodes", stats.get('total_nodes', '0'))
    info_table.add_row("Total edges", stats.get('total_edges', '0'))
    
    console.print(info_table)
    
    # Node types
    if 'node_types' in stats:
        console.print("\n📋 [bold blue]Node Types:[/bold blue]")
        type_table = Table(show_header=True, header_style="bold magenta")
        type_table.add_column("Type", style="cyan")
        type_table.add_column("Count", style="bold green")
        
        for node_type, count in stats['node_types'].items():
            type_table.add_row(node_type, str(count))
        
        console.print(type_table)
    
    # Relationship types
    if 'relationship_types' in stats:
        console.print("\n🔗 [bold blue]Relationship Types:[/bold blue]")
        rel_table = Table(show_header=True, header_style="bold magenta")
        rel_table.add_column("Type", style="cyan")
        rel_table.add_column("Count", style="bold green")
        
        for rel_type, count in stats['relationship_types'].items():
            rel_table.add_row(rel_type, str(count))
        
        console.print(rel_table)


@cli.command()
@click.option('--clear', is_flag=True, help='Clear old cache entries (older than 30 days)')
@click.option('--days', type=int, default=30, help='Days threshold for clearing cache')
def cache(clear, days):
    """Manage indexing cache for faster re-indexing"""
    from .cache_manager import CacheManager
    
    cache_manager = CacheManager()
    
    if clear:
        console.print(f"🗑️ [yellow]Clearing cache entries older than {days} days...[/yellow]")
        cache_manager.clear_cache(older_than_days=days)
        console.print("✅ [green]Cache cleared successfully![/green]")
    
    console.print("💾 [bold blue]Cache Statistics[/bold blue]")
    cache_manager.print_cache_stats()


@cli.command()
@click.option('--records', type=int, default=1000, help='Number of test records')
def benchmark(records):
    """Run performance benchmarks"""
    from .db_optimizer import DatabaseBenchmark
    
    console.print(f"🔥 [bold blue]Running performance benchmark with {records} records...[/bold blue]")
    
    sqlite3_time, optimized_time = DatabaseBenchmark.benchmark_insert_performance(
        "benchmark_test.db", num_records=records
    )
    
    console.print(f"\n📊 [bold blue]Benchmark Results:[/bold blue]")
    
    benchmark_table = Table(show_header=True, header_style="bold magenta")
    benchmark_table.add_column("Database Type", style="cyan")
    benchmark_table.add_column("Time (seconds)", style="bold green")
    benchmark_table.add_column("Records/second", style="bold yellow")
    
    benchmark_table.add_row("Standard SQLite3", f"{sqlite3_time:.2f}", f"{records/sqlite3_time:.0f}")
    benchmark_table.add_row("Optimized APSW", f"{optimized_time:.2f}", f"{records/optimized_time:.0f}")
    
    console.print(benchmark_table)
    
    speedup = sqlite3_time / optimized_time
    console.print(f"\n🚀 [bold green]Speedup: {speedup:.1f}x faster with optimizations![/bold green]")


@cli.command()
@click.option('--check-only', is_flag=True, help='Only check for updates without installing')
def update(check_only):
    """Check for and install updates"""
    updater = Updater()
    
    if check_only:
        updater.auto_update(check_only=True)
    else:
        if updater.auto_update(check_only=False):
            # Also sync CLAUDE.md after update
            updater.sync_claude_md()
            console.print("\n🎉 [bold green]Update complete![/bold green]")
            console.print("Restart your terminal or run [bold]hash -r[/bold] to use the new version")


@cli.command()
def sync():
    """Sync CLAUDE.md with latest template"""
    updater = Updater()
    if updater.sync_claude_md(force=True):
        console.print("✅ [bold green]CLAUDE.md synchronized![/bold green]")
    else:
        console.print("✓ CLAUDE.md is already up to date")


def main():
    """Main CLI entry point"""
    # Check for updates on startup (non-blocking)
    check_and_notify_update()
    cli()


if __name__ == "__main__":
    main()