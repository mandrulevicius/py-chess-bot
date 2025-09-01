#!/usr/bin/env python3
"""
PyChessBot Dependency Graph Visualizer

This script creates interactive and static visualizations of the project's
dependency graph with git change heatmap overlays.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
from typing import Dict, List, Tuple, Optional
import numpy as np
from datetime import datetime, timedelta
import os
import sys

# Add project root to path to import our data
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from dependency_graph_data import (
    NODES, EDGES, CATEGORY_COLORS, 
    get_nodes_by_category, get_high_activity_files, get_dependency_graph
)

def create_networkx_graph() -> nx.DiGraph:
    """Create NetworkX graph from our data"""
    G = nx.DiGraph()
    
    # Add nodes with attributes
    for node in NODES:
        activity_score = node.git_stats.recent_activity if node.git_stats else 0.0
        lines_changed = (node.git_stats.lines_added + node.git_stats.lines_deleted 
                        if node.git_stats else 0)
        
        G.add_node(node.short_name, 
                  path=node.path,
                  description=node.description,
                  category=node.category,
                  activity_score=activity_score,
                  lines_changed=lines_changed,
                  commit_count=node.git_stats.commit_count if node.git_stats else 0)
    
    # Add edges
    for edge in EDGES:
        source_name = next(n.short_name for n in NODES if n.path == edge.source)
        target_name = next(n.short_name for n in NODES if n.path == edge.target)
        
        G.add_edge(source_name, target_name,
                  reason=edge.reason,
                  edge_type=edge.edge_type)
    
    return G

def plot_dependency_graph_with_heatmap(save_path: str = None, show: bool = True):
    """Create the main dependency graph visualization with git heatmap"""
    G = create_networkx_graph()
    
    # Create figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 12))
    
    # Layout for better visualization
    pos = nx.spring_layout(G, k=3, iterations=50, seed=42)
    
    # Get node attributes for coloring
    activity_scores = [G.nodes[node]['activity_score'] for node in G.nodes()]
    lines_changed = [G.nodes[node]['lines_changed'] for node in G.nodes()]
    categories = [G.nodes[node]['category'] for node in G.nodes()]
    
    # Plot 1: Category-based coloring
    ax1.set_title("PyChessBot Dependency Graph\n(Colored by Component Category)", 
                  fontsize=16, fontweight='bold', pad=20)
    
    node_colors_cat = [CATEGORY_COLORS[cat] for cat in categories]
    node_sizes_cat = [max(300, G.nodes[node]['commit_count'] * 100) for node in G.nodes()]
    
    nx.draw_networkx_nodes(G, pos, ax=ax1, 
                          node_color=node_colors_cat, 
                          node_size=node_sizes_cat,
                          alpha=0.8, edgecolors='black', linewidths=1)
    
    nx.draw_networkx_labels(G, pos, ax=ax1, font_size=8, font_weight='bold')
    
    # Draw edges with different styles for different types
    import_edges = [(u, v) for u, v, d in G.edges(data=True) if d['edge_type'] == 'import']
    dynamic_edges = [(u, v) for u, v, d in G.edges(data=True) if d['edge_type'] == 'dynamic_import']
    
    nx.draw_networkx_edges(G, pos, ax=ax1, edgelist=import_edges, 
                          edge_color='#666666', arrows=True, arrowsize=20, 
                          width=1.5, alpha=0.7)
    nx.draw_networkx_edges(G, pos, ax=ax1, edgelist=dynamic_edges,
                          edge_color='#FF6B6B', arrows=True, arrowsize=20,
                          width=2, alpha=0.8, style='dashed')
    
    # Plot 2: Git activity heatmap
    ax2.set_title("PyChessBot Files by Change Activity\n(Size = commits, Color = recent activity)", 
                  fontsize=16, fontweight='bold', pad=20)
    
    # Create heatmap coloring based on activity
    activity_norm = plt.Normalize(vmin=0, vmax=1)
    activity_cmap = plt.cm.YlOrRd
    node_colors_heat = [activity_cmap(activity_norm(score)) for score in activity_scores]
    node_sizes_heat = [max(300, size) for size in node_sizes_cat]
    
    nx.draw_networkx_nodes(G, pos, ax=ax2,
                          node_color=node_colors_heat,
                          node_size=node_sizes_heat,
                          alpha=0.8, edgecolors='black', linewidths=1)
    
    nx.draw_networkx_labels(G, pos, ax=ax2, font_size=8, font_weight='bold')
    nx.draw_networkx_edges(G, pos, ax=ax2, 
                          edge_color='#CCCCCC', arrows=True, arrowsize=15, 
                          width=1, alpha=0.5)
    
    # Add legends
    # Category legend
    category_patches = [mpatches.Patch(color=color, label=category.capitalize()) 
                       for category, color in CATEGORY_COLORS.items()]
    ax1.legend(handles=category_patches, loc='upper left', bbox_to_anchor=(1.02, 1))
    
    # Activity legend
    sm = plt.cm.ScalarMappable(cmap=activity_cmap, norm=activity_norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax2, fraction=0.046, pad=0.04)
    cbar.set_label('Recent Activity Score', rotation=270, labelpad=15)
    
    # Remove axes
    ax1.set_axis_off()
    ax2.set_axis_off()
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Graph saved to: {save_path}")
    
    if show:
        plt.show()
    
    return fig

def create_metrics_report():
    """Generate textual metrics report"""
    G = create_networkx_graph()
    
    print("=== PyChessBot Project Dependency Analysis ===\\n")
    
    # Basic metrics
    print(f"📊 BASIC METRICS")
    print(f"   • Total files: {len(G.nodes())}")
    print(f"   • Total dependencies: {len(G.edges())}")
    print(f"   • Components: {len(set(n['category'] for n in G.nodes().values()))}")
    print()
    
    # Category breakdown
    categories = get_nodes_by_category()
    print(f"📁 COMPONENT BREAKDOWN")
    for category, nodes in categories.items():
        print(f"   • {category.capitalize()}: {len(nodes)} files")
    print()
    
    # High activity files
    high_activity = get_high_activity_files()
    print(f"🔥 HIGH ACTIVITY FILES (recent_activity >= 0.8)")
    for node in sorted(high_activity, key=lambda x: x.git_stats.recent_activity, reverse=True):
        print(f"   • {node.short_name}: {node.git_stats.recent_activity:.1f} activity, "
              f"{node.git_stats.commit_count} commits, "
              f"{node.git_stats.lines_added + node.git_stats.lines_deleted} lines changed")
    print()
    
    # Dependency analysis
    print(f"🔗 DEPENDENCY ANALYSIS")
    in_degrees = dict(G.in_degree())
    out_degrees = dict(G.out_degree())
    
    most_depended_on = sorted(in_degrees.items(), key=lambda x: x[1], reverse=True)[:5]
    most_dependent = sorted(out_degrees.items(), key=lambda x: x[1], reverse=True)[:5]
    
    print(f"   Most depended-on files:")
    for name, count in most_depended_on:
        if count > 0:
            print(f"     - {name}: {count} incoming dependencies")
    
    print(f"   Most dependent files:")
    for name, count in most_dependent:
        if count > 0:
            print(f"     - {name}: {count} outgoing dependencies")
    print()
    
    # Architecture insights
    print(f"🏗️  ARCHITECTURE INSIGHTS")
    
    # Find potential bottlenecks (high in-degree)
    bottlenecks = [name for name, degree in in_degrees.items() if degree >= 3]
    if bottlenecks:
        print(f"   • Potential bottleneck files (≥3 dependents): {', '.join(bottlenecks)}")
    
    # Find leaf nodes (no dependencies)
    leaves = [name for name, degree in out_degrees.items() if degree == 0]
    if leaves:
        print(f"   • Leaf files (no outgoing deps): {', '.join(leaves)}")
    
    # Check for circular dependencies
    try:
        cycles = list(nx.simple_cycles(G))
        if cycles:
            print(f"   • ⚠️  Circular dependencies found: {len(cycles)}")
        else:
            print(f"   • ✅ No circular dependencies detected")
    except:
        print(f"   • Could not analyze circular dependencies")
    
    print()

def create_interactive_html_visualization(save_path: str = "dependency_graph.html"):
    """Create an interactive HTML visualization using a simple template"""
    
    G = create_networkx_graph()
    
    # Generate node data for JavaScript
    nodes_js = []
    for node in G.nodes():
        data = G.nodes[node]
        nodes_js.append({
            'id': node,
            'label': node,
            'title': f"{data['path']}\\n{data['description']}\\nCommits: {data['commit_count']}\\nActivity: {data['activity_score']:.1f}",
            'color': CATEGORY_COLORS[data['category']],
            'size': max(20, data['commit_count'] * 3),
            'category': data['category']
        })
    
    # Generate edge data
    edges_js = []
    for source, target in G.edges():
        edge_data = G[source][target]
        edges_js.append({
            'from': source,
            'to': target,
            'title': edge_data['reason'],
            'color': '#999999' if edge_data['edge_type'] == 'import' else '#FF6B6B'
        })
    
    # Create HTML template
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>PyChessBot Dependency Graph</title>
        <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
        <style>
            #mynetworkid {{
                width: 100%;
                height: 800px;
                border: 1px solid lightgray;
            }}
            .legend {{
                position: absolute;
                top: 10px;
                right: 10px;
                background: white;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }}
            .legend-item {{
                display: flex;
                align-items: center;
                margin: 5px 0;
            }}
            .legend-color {{
                width: 20px;
                height: 20px;
                margin-right: 10px;
                border-radius: 3px;
            }}
        </style>
    </head>
    <body>
        <h1>PyChessBot Project Dependency Graph</h1>
        <p>Interactive visualization of file dependencies. Hover over nodes and edges for details.</p>
        
        <div class="legend">
            <h3>Component Categories</h3>
            {''.join([f'<div class="legend-item"><div class="legend-color" style="background-color: {color}"></div><span>{category.capitalize()}</span></div>' for category, color in CATEGORY_COLORS.items()])}
        </div>
        
        <div id="mynetworkid"></div>

        <script type="text/javascript">
            var nodes = new vis.DataSet({nodes_js});
            var edges = new vis.DataSet({edges_js});
            var container = document.getElementById('mynetworkid');
            var data = {{ nodes: nodes, edges: edges }};
            var options = {{
                nodes: {{
                    shape: 'dot',
                    scaling: {{
                        min: 10,
                        max: 30
                    }},
                    font: {{ size: 12, face: 'Tahoma' }}
                }},
                edges: {{
                    width: 0.15,
                    color: {{ inherit: 'from' }},
                    smooth: {{
                        type: 'continuous'
                    }},
                    arrows: {{ to: true }}
                }},
                physics: {{
                    stabilization: {{ iterations: 150 }},
                    barnesHut: {{
                        gravitationalConstant: -80000,
                        springConstant: 0.001,
                        springLength: 200
                    }}
                }},
                interaction: {{
                    tooltipDelay: 200,
                    hideEdgesOnDrag: true,
                    hideNodesOnDrag: true
                }}
            }};
            var network = new vis.Network(container, data, options);
        </script>
    </body>
    </html>
    """
    
    with open(save_path, 'w') as f:
        f.write(html_content)
    
    print(f"Interactive visualization saved to: {save_path}")

def main():
    """Main function to generate all visualizations"""
    
    print("🔍 Generating PyChessBot dependency analysis...\\n")
    
    try:
        # Use current directory or create local output directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(script_dir, "output") if "/workspace/" in script_dir else "."
        
        print(f"📁 Output directory: {os.path.abspath(output_dir)}")
        
        # Test write permissions
        test_file = os.path.join(output_dir, ".write_test")
        try:
            os.makedirs(output_dir, exist_ok=True)
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
            print("✅ Write permissions confirmed")
        except (OSError, PermissionError) as e:
            print(f"❌ ERROR: Cannot write to {output_dir}")
            print(f"   Reason: {e}")
            print(f"   Try running from a writable directory or check permissions")
            return
        
        # Generate textual report
        create_metrics_report()
        
        # Generate static visualization
        static_path = os.path.join(output_dir, "dependency_graph.png")
        print(f"📊 Creating static visualization...")
        try:
            plot_dependency_graph_with_heatmap(save_path=static_path, show=False)
            print(f"✅ Saved: {static_path}")
        except Exception as e:
            print(f"❌ Failed to create PNG: {e}")
        
        # Generate interactive visualization
        interactive_path = os.path.join(output_dir, "dependency_graph.html")
        print(f"🌐 Creating interactive visualization...")
        try:
            create_interactive_html_visualization(save_path=interactive_path)
            print(f"✅ Saved: {interactive_path}")
        except Exception as e:
            print(f"❌ Failed to create HTML: {e}")
        
        print(f"\\n✅ Analysis complete!")
        
    except Exception as e:
        print(f"❌ FATAL ERROR: {e}")
        print(f"   Current directory: {os.getcwd()}")
        print(f"   Script location: {__file__}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()