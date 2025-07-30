import click
import os
import sys
from upstash_redis import Redis
from cadro import CADRO
import json
from argparse import ArgumentParser
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from cadro import CADRO
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../GraphNexus')))


def get_redis():
    """Create Redis client from environment when needed."""
    return Redis.from_env()




@click.group()
def cli():
    pass


@cli.command()
@click.option('--new-cues', type=str, help='New contextual cues to update (JSON format)')
def update_contextual_cues(new_cues):
    cadro = CADRO()
    try:
        parsed_cues = json.loads(new_cues) if new_cues else None
        cadro.update_contextual_cues(parsed_cues)
        click.echo("Contextual cues updated.")
    except json.JSONDecodeError as e:
        click.echo(f"Error: Invalid JSON format - {e}")
        sys.exit(1)


@cli.command()
def optimize_dynamic_response():
    cadro = CADRO()
    cadro.optimize_dynamic_response()
    click.echo("Dynamic response optimized.")


@cli.command()
@click.option('--feedback', type=str,
              help='User feedback for real-time adaptation (JSON format)')
def integrate_real_time_feedback(feedback):
    cadro = CADRO()
    try:
        parsed_feedback = json.loads(feedback) if feedback else None
        cadro.integrate_real_time_feedback(parsed_feedback)
        click.echo("Real-time feedback integrated.")
    except json.JSONDecodeError as e:
        click.echo(f"Error: Invalid JSON format - {e}")
        sys.exit(1)


@cli.command()
@click.option('--response', type=str,
              help='Response to check for unwanted narrative triggers')
def identify_triggers_for_unwanted_narrative(response):
    cadro = CADRO()
    result = cadro.identify_triggers_for_unwanted_narrative(response)
    click.echo(f"Unwanted narrative triggers identified: {result}")


@cli.command()
@click.option('--conflicting-cues', type=str,
              help='Conflicting contextual cues to handle (JSON format)')
def handle_conflicting_contextual_cues(conflicting_cues):
    cadro = CADRO()
    try:
        parsed_cues = json.loads(conflicting_cues) if conflicting_cues else None
        cadro.handle_conflicting_contextual_cues(parsed_cues)
        click.echo("Conflicting contextual cues handled.")
    except json.JSONDecodeError as e:
        click.echo(f"Error: Invalid JSON format - {e}")
        sys.exit(1)

    
def load_traces(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)['data']

def create_full_graph(traces):
    from graph_builder import GraphBuilder
    builder = GraphBuilder()
    for trace in traces:
        trace_id = trace['id']
        trace_name = trace['name']
        node_type = trace.get('type', 'default')  # Assume traces might have a 'type' field
        
        if node_type == 'EchoNode':
            builder.integrate_echonodes([{'id': trace_id, 'label': trace_name, 'connections': trace.get('linked_traces', [])}])
        elif node_type == 'RedStone':
            builder.integrate_red_stones([{'id': trace_id, 'label': trace_name, 'connections': trace.get('relatedIssues', [])}])
        else:
            builder.add_node(trace_id, trace_name)
            # Add edges for related issues
            for issue in trace.get('metadata', {}).get('relatedIssues', []):
                builder.add_edge(trace_id, issue)
            # Add edges for linked traces
            input_data = trace.get('input', {})
            linked_traces = input_data.get('linked_traces', []) if isinstance(input_data, dict) else []
            for linked_trace in linked_traces:
                builder.add_edge(trace_id, linked_trace)
    
    return builder.graph

def draw_graph(G, labels=None, title='Graph Representation'):
    import matplotlib.pyplot as plt
    import networkx as nx
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42)  # Fixed seed for reproducibility
    node_colors = []
    for node in G.nodes:
        if 'EchoNode' in G.nodes[node].get('label', ''):
            node_colors.append('green')
        elif 'RedStone' in G.nodes[node].get('label', ''):
            node_colors.append('red')
        else:
            node_colors.append('lightblue')
    nx.draw(G, pos, with_labels=True, labels=labels, node_size=500, node_color=node_colors, edge_color='gray', font_size=8)
    plt.title(title)
    plt.show()

def main():
    parser = ArgumentParser(description='Graph generator from trace JSON files')
    parser.add_argument('file', help='Path to JSON trace file')
    parser.add_argument('--mode', choices=['full', 'selective', 'formatted', 'short'], default='full', help='Graph generation mode')
    args = parser.parse_args()

    traces = load_traces(args.file)
    G = None
    labels = None

    if args.mode == 'full':
        G = create_full_graph(traces)
        labels = {trace['id']: split_title(trace['name'], words_per_line=2) for trace in traces}
        draw_graph(G, labels, title='Graph Representation of Traces and Relationships')
    
    # Other modes remain similar, just update G = create_full_graph(traces) where needed
    elif args.mode == 'selective':
        G, nodes = create_selective_graph(traces)  # Update this if needed
        labels = {k: split_title(v, words_per_line=2) for k, v in nodes.items()}
        draw_graph(G, labels, title='Selective Graph Representation of Tracing Data')
    
    elif args.mode == 'formatted':
        G = create_full_graph(traces)
        labels = {trace['id']: format_title(trace['name']) for trace in traces}
        draw_graph(G, labels, title='Graph Representation of Traces (Formatted Titles)')
    
    elif args.mode == 'short':
        G = create_full_graph(traces)
        labels = {
            trace['id']: 
            (split_title(trace['name'], words_per_line=2)[:20] + '...' 
             if len(split_title(trace['name'], words_per_line=2)) > 20 
             else split_title(trace['name'], words_per_line=2)) 
            for trace in traces
        }
        draw_graph(G, labels, title='Graph Representation of Traces (Shortened Titles)')

    

@cli.command()
def list_keys():
    """List all Redis keys."""
    redis = get_redis()
    keys = redis.keys('*')
    for key in keys:
        click.echo(key)


@cli.command()
@click.argument('context_name')
@click.argument('keys', nargs=-1)
def create_context(context_name, keys):
    """Create a context scenario with a group of keys."""
    context_key = f"context:{context_name}"
    redis = get_redis()
    redis.sadd(context_key, *keys)
    click.echo(
        f"Context '{context_name}' created with keys: {', '.join(keys)}")

@cli.command()
@click.option('--narrative-data', type=str, help='Narrative data to add (JSON format)')
def add_narrative_driven_learning(narrative_data):
    cadro = CADRO()
    try:
        parsed_data = json.loads(narrative_data) if narrative_data else None
        cadro.add_narrative_driven_learning(parsed_data)
        click.echo("Narrative-driven learning added.")
    except json.JSONDecodeError as e:
        click.echo(f"Error: Invalid JSON format - {e}")
        sys.exit(1)

@cli.command()
@click.option('--feedback', type=str, help='Real-time feedback to integrate (JSON format)')
def integrate_real_time_feedback_mechanisms(feedback):
    cadro = CADRO()
    try:
        parsed_feedback = json.loads(feedback) if feedback else None
        cadro.integrate_real_time_feedback_mechanisms(parsed_feedback)
        click.echo("Real-time feedback mechanisms integrated.")
    except json.JSONDecodeError as e:
        click.echo(f"Error: Invalid JSON format - {e}")
        sys.exit(1)

if __name__ == "__main__":
    cli()

