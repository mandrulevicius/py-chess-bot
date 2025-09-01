#!/usr/bin/env python3
"""
PyChessBot Simple Dependency Analyzer

A lightweight dependency analysis tool that works without external visualization libraries.
Generates text-based reports and data structures for the project overview.
"""

import os
import sys
from typing import Dict, List, Tuple, Set
from collections import defaultdict, Counter

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from dependency_graph_data import (
    NODES, EDGES, CATEGORY_COLORS, 
    get_nodes_by_category, get_high_activity_files, get_dependency_graph
)

def create_adjacency_representation() -> Dict[str, Dict]:
    """Create adjacency list representation of the dependency graph"""
    adj_list = defaultdict(lambda: {'incoming': [], 'outgoing': [], 'details': {}})
    
    # Add all nodes
    for node in NODES:
        adj_list[node.short_name]['details'] = {
            'path': node.path,
            'description': node.description,
            'category': node.category,
            'git_stats': node.git_stats
        }
    
    # Add edges
    for edge in EDGES:
        source_name = next(n.short_name for n in NODES if n.path == edge.source)
        target_name = next(n.short_name for n in NODES if n.path == edge.target)
        
        adj_list[source_name]['outgoing'].append({
            'target': target_name,
            'reason': edge.reason,
            'type': edge.edge_type
        })
        
        adj_list[target_name]['incoming'].append({
            'source': source_name,
            'reason': edge.reason,
            'type': edge.edge_type
        })
    
    return dict(adj_list)

def analyze_dependencies():
    """Perform comprehensive dependency analysis"""
    adj = create_adjacency_representation()
    
    # Calculate metrics
    in_degrees = {name: len(data['incoming']) for name, data in adj.items()}
    out_degrees = {name: len(data['outgoing']) for name, data in adj.items()}
    
    # Find important files
    most_depended_on = sorted(in_degrees.items(), key=lambda x: x[1], reverse=True)[:5]
    most_dependent = sorted(out_degrees.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Analyze by category
    category_stats = defaultdict(lambda: {'count': 0, 'total_deps': 0})
    for name, data in adj.items():
        category = data['details']['category']
        category_stats[category]['count'] += 1
        category_stats[category]['total_deps'] += len(data['outgoing'])
    
    return {
        'adjacency': adj,
        'in_degrees': in_degrees,
        'out_degrees': out_degrees,
        'most_depended_on': most_depended_on,
        'most_dependent': most_dependent,
        'category_stats': dict(category_stats)
    }

def print_detailed_report():
    """Generate and print comprehensive analysis report"""
    analysis = analyze_dependencies()
    adj = analysis['adjacency']
    
    print("=" * 80)
    print("🐍 PYCHESSBOT PROJECT DEPENDENCY ANALYSIS")
    print("=" * 80)
    print()
    
    # Basic project metrics
    print("📊 PROJECT OVERVIEW")
    print("-" * 40)
    print(f"Total files analyzed: {len(NODES)}")
    print(f"Total dependencies: {len(EDGES)}")
    print(f"Component categories: {len(set(n.category for n in NODES))}")
    print()
    
    # Category breakdown
    categories = get_nodes_by_category()
    print("📁 COMPONENT BREAKDOWN")
    print("-" * 40)
    for category, nodes in categories.items():
        stats = analysis['category_stats'][category]
        avg_deps = stats['total_deps'] / stats['count'] if stats['count'] > 0 else 0
        print(f"  {category.upper():<12} : {len(nodes):>2} files, avg {avg_deps:.1f} dependencies each")
    print()
    
    # Git activity analysis
    high_activity = get_high_activity_files(threshold=0.7)
    print("🔥 HIGH ACTIVITY FILES (activity score ≥ 0.7)")
    print("-" * 40)
    for node in sorted(high_activity, key=lambda x: x.git_stats.recent_activity, reverse=True):
        deps_in = len(adj[node.short_name]['incoming'])
        deps_out = len(adj[node.short_name]['outgoing'])
        print(f"  {node.short_name:<20} : activity={node.git_stats.recent_activity:.1f}, "
              f"commits={node.git_stats.commit_count:>2}, "
              f"deps_in={deps_in}, deps_out={deps_out}")
    print()
    
    # Dependency analysis
    print("🔗 DEPENDENCY PATTERNS")
    print("-" * 40)
    print("  Most depended-on files (potential bottlenecks):")
    for name, count in analysis['most_depended_on']:
        if count > 0:
            category = adj[name]['details']['category']
            print(f"    {name:<20} : {count} dependents ({category})")
    
    print("\\n  Most dependency-heavy files:")
    for name, count in analysis['most_dependent']:
        if count > 0:
            category = adj[name]['details']['category']
            print(f"    {name:<20} : {count} dependencies ({category})")
    print()
    
    # Architecture insights
    print("🏗️ ARCHITECTURE INSIGHTS")
    print("-" * 40)
    
    # Entry points (high out-degree, low in-degree)
    entry_points = [name for name, out_deg in analysis['out_degrees'].items() 
                   if out_deg >= 5 and analysis['in_degrees'][name] <= 1]
    if entry_points:
        print(f"  Entry points: {', '.join(entry_points)}")
    
    # Core utilities (high in-degree)
    core_utils = [name for name, in_deg in analysis['in_degrees'].items() if in_deg >= 3]
    if core_utils:
        print(f"  Core utilities: {', '.join(core_utils)}")
    
    # Leaf nodes (no outgoing dependencies)
    leaves = [name for name, out_deg in analysis['out_degrees'].items() if out_deg == 0]
    if leaves:
        print(f"  Leaf nodes: {', '.join(leaves[:5])}{'...' if len(leaves) > 5 else ''}")
    
    print()

def create_ascii_dependency_tree(root_node: str = "main", max_depth: int = 3):
    """Create ASCII art dependency tree"""
    adj = create_adjacency_representation()
    
    def print_tree(node: str, depth: int = 0, prefix: str = "", visited: Set[str] = None):
        if visited is None:
            visited = set()
        
        if depth > max_depth or node in visited:
            return
        
        visited.add(node)
        
        # Print current node
        details = adj[node]['details']
        activity = details['git_stats'].recent_activity if details['git_stats'] else 0
        activity_indicator = "🔥" if activity >= 0.8 else "🟡" if activity >= 0.5 else "🔵"
        
        print(f"{prefix}{activity_indicator} {node} ({details['category']})")
        
        # Print dependencies
        outgoing = adj[node]['outgoing']
        for i, dep in enumerate(outgoing):
            is_last = i == len(outgoing) - 1
            new_prefix = prefix + ("    " if is_last else "│   ")
            connector = "└── " if is_last else "├── "
            
            print(f"{prefix}{connector}{dep['target']} [{dep['type']}]")
            
            # Recursively print sub-dependencies
            if depth < max_depth:
                sub_prefix = prefix + ("    " if is_last else "│   ")
                print_tree(dep['target'], depth + 1, sub_prefix, visited.copy())
    
    print("🌳 DEPENDENCY TREE")
    print("-" * 40)
    print("Legend: 🔥 High activity (≥0.8)  🟡 Medium (≥0.5)  🔵 Low (<0.5)")
    print()
    
    print_tree(root_node)
    print()

def export_data_for_external_tools():
    """Export data in formats suitable for external visualization tools"""
    adj = create_adjacency_representation()
    
    # DOT format for Graphviz
    dot_file = "/workspace/PyChessBot/docs/overview/dependency_graph.dot"
    with open(dot_file, 'w') as f:
        f.write("digraph PyChessBot {\\n")
        f.write('  rankdir=TB;\\n')
        f.write('  node [shape=ellipse, style=filled];\\n\\n')
        
        # Add nodes with colors and labels
        for name, data in adj.items():
            details = data['details']
            color = CATEGORY_COLORS.get(details['category'], '#CCCCCC')
            activity = details['git_stats'].recent_activity if details['git_stats'] else 0
            
            f.write(f'  "{name}" [fillcolor="{color}", ')
            f.write(f'label="{name}\\\\n({details["category"]})\\\\nActivity: {activity:.1f}"];\\n')
        
        f.write('\\n')
        
        # Add edges
        for name, data in adj.items():
            for dep in data['outgoing']:
                edge_style = "dashed" if dep['type'] == 'dynamic_import' else "solid"
                f.write(f'  "{name}" -> "{dep["target"]}" [style={edge_style}];\\n')
        
        f.write('}\\n')
    
    print(f"📄 Exported DOT file: {dot_file}")
    print("   To generate PNG: dot -Tpng dependency_graph.dot -o dependency_graph.png")
    
    # CSV format for spreadsheet analysis
    csv_file = "/workspace/PyChessBot/docs/overview/dependency_data.csv"
    with open(csv_file, 'w') as f:
        f.write("File,Category,Dependencies_In,Dependencies_Out,Activity,Commits,Lines_Changed\\n")
        
        for name, data in adj.items():
            details = data['details']
            git_stats = details['git_stats']
            
            deps_in = len(data['incoming'])
            deps_out = len(data['outgoing'])
            activity = git_stats.recent_activity if git_stats else 0
            commits = git_stats.commit_count if git_stats else 0
            lines = (git_stats.lines_added + git_stats.lines_deleted) if git_stats else 0
            
            f.write(f"{name},{details['category']},{deps_in},{deps_out},{activity},{commits},{lines}\\n")
    
    print(f"📊 Exported CSV file: {csv_file}")
    print()

def main():
    """Main function"""
    print_detailed_report()
    create_ascii_dependency_tree()
    export_data_for_external_tools()
    
    print("✅ Analysis complete!")
    print("\\nGenerated files:")
    print("  • dependency_graph.dot - Graphviz DOT format")
    print("  • dependency_data.csv - CSV data for analysis")
    print("\\nTo generate visual graph:")
    print("  apt install graphviz  # or brew install graphviz")
    print("  dot -Tpng docs/overview/dependency_graph.dot -o docs/overview/dependency_graph.png")

if __name__ == "__main__":
    main()