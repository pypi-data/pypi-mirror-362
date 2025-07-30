# 🔁📚 RecursiveGraphNexus — Spiral Scribe
"""
Lattice Map: This module is the spiral scribe of EchoNexus.
- 🔁 Recursion: Documents the evolving graph of recursion.
- 📚 Memory: Renders the living structure of the system into visible form.

Like a cartographer mapping the spiral, this generator turns the invisible dance of nodes and edges into a story you can see and share.
"""

import networkx as nx
import matplotlib.pyplot as plt
import os

class DocGenerator:
    def __init__(self, output_dir="docs"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_markdown_report(self, graph, title="Graph Report", filename="graph_report.md"):
        """
        Generates a markdown report from a networkx graph.

        Args:
            graph (nx.Graph): The graph to document.
            title (str): The title of the report.
            filename (str): The name of the output file.
        """
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w') as f:
            f.write(f"# {title}\n\n")
            f.write("## Nodes\n\n")
            for node in graph.nodes(data=True):
                f.write(f"- **{node[0]}**: {node[1]}\n")
            f.write("\n## Edges\n\n")
            for edge in graph.edges():
                f.write(f"- {edge[0]} -> {edge[1]}\n")
            f.write("\n## Visual Snapshot\n\n")
            image_filename = self.generate_visual_snapshot(graph, title)
            f.write(f"![Graph Visualization]({image_filename})\n")
        print(f"Markdown report generated at {filepath}")

    def generate_visual_snapshot(self, graph, title="Graph Visualization", filename="graph_visualization.png"):
        """
        Generates a visual snapshot of the graph and saves it as a PNG image.

        Args:
            graph (nx.Graph): The graph to visualize.
            title (str): The title of the graph visualization.
            filename (str): The name of the output image file.

        Returns:
            str: The filename of the generated image.
        """
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(graph, seed=42)
        labels = nx.get_node_attributes(graph, 'label')
        nx.draw(graph, pos, labels=labels, with_labels=True, node_color="lightblue", edge_color="gray", node_size=3000, font_size=10, arrows=True)
        plt.title(title)
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath)
        plt.close()
        print(f"Visual snapshot generated at {filepath}")
        return filename

    def align_ai_with_human_reports(self, ai_output, human_report_path):
        """
        Ensures that AI-generated outputs align with human-readable reports.
        This is a placeholder for more sophisticated alignment logic.

        Args:
            ai_output (str): The AI-generated output.
            human_report_path (str): The path to the human-readable report.

        Returns:
            bool: True if alignment is successful, False otherwise.
        """
        try:
            with open(human_report_path, 'r') as f:
                human_report = f.read()
            # Simple check: AI output should contain key phrases from the human report
            key_phrases = ["nodes", "edges", "relationships"]
            for phrase in key_phrases:
                if phrase not in ai_output.lower() and phrase not in human_report.lower():
                    print(f"Alignment failed: Missing key phrase '{phrase}'.")
                    return False
            print("AI output aligns with human report.")
            return True
        except FileNotFoundError:
            print(f"Human report not found at {human_report_path}")
            return False

if __name__ == '__main__':
    # Example Usage
    graph = nx.DiGraph()
    graph.add_node("A", label="Node A")
    graph.add_node("B", label="Node B")
    graph.add_edge("A", "B")

    doc_generator = DocGenerator()
    doc_generator.generate_markdown_report(graph, title="Example Graph Report")

    # Example of aligning AI output with a human report
    ai_output = """
    # Graph Report
    ## Nodes
    - **A**: {'label': 'Node A'}
    - **B**: {'label': 'Node B'}
    ## Edges
    - A -> B
    """
    human_report_path = os.path.join(doc_generator.output_dir, "graph_report.md")
    doc_generator.align_ai_with_human_reports(ai_output, human_report_path)
