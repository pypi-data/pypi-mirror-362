"""
Noosphere visualization system for Q-Memetic AI.

Creates beautiful, interactive visualizations of the global mind map
showing meme evolution, entanglement networks, and idea propagation.
"""

import json
import time
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import logging

import numpy as np
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.offline as pyo


class NoosphereVisualizer:
    """
    Advanced visualization engine for the memetic noosphere.
    
    Creates interactive visualizations including:
    - Force-directed network graphs
    - Quantum entanglement strength heatmaps
    - Evolution timeline trees
    - Real-time propagation animations
    - Multi-dimensional embeddings
    """
    
    def __init__(self, theme: str = "dark", output_dir: str = "./visualizations"):
        """
        Initialize the visualizer.
        
        Args:
            theme: Visualization theme ("dark", "light", "quantum")
            output_dir: Directory to save visualizations
        """
        self.theme = theme
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.logger = logging.getLogger("NoosphereVisualizer")
        
        # Theme configurations
        self.themes = {
            "dark": {
                "bg_color": "#0a0a0a",
                "paper_color": "#1a1a1a", 
                "text_color": "#ffffff",
                "node_colors": ["#ff6b6b", "#4ecdc4", "#45b7d1", "#96ceb4", "#ffd93d"],
                "edge_color": "#555555",
                "highlight_color": "#ff6b6b"
            },
            "light": {
                "bg_color": "#ffffff",
                "paper_color": "#f8f9fa",
                "text_color": "#333333",
                "node_colors": ["#e74c3c", "#3498db", "#2ecc71", "#f39c12", "#9b59b6"],
                "edge_color": "#cccccc",
                "highlight_color": "#e74c3c"
            },
            "quantum": {
                "bg_color": "#000011",
                "paper_color": "#001122",
                "text_color": "#00ffff",
                "node_colors": ["#ff00ff", "#00ffff", "#ffff00", "#ff0080", "#80ff00"],
                "edge_color": "#003366",
                "highlight_color": "#ff00ff"
            }
        }
        
        self.current_theme = self.themes.get(theme, self.themes["dark"])
    
    def create_noosphere_visualization(
        self,
        network_data: Dict[str, Any],
        layout: str = "force_directed",
        save_path: Optional[str] = None,
        interactive: bool = True,
        width: int = 1200,
        height: int = 800
    ) -> str:
        """
        Create main noosphere visualization.
        
        Args:
            network_data: Entanglement network data
            layout: Layout algorithm ("force_directed", "circular", "hierarchical")
            save_path: Path to save visualization
            interactive: Create interactive visualization
            width: Visualization width
            height: Visualization height
            
        Returns:
            Path to created visualization file
        """
        if save_path is None:
            timestamp = int(time.time())
            save_path = self.output_dir / f"noosphere_{timestamp}.html"
        
        # Extract nodes and edges
        nodes = network_data.get("nodes", [])
        edges = network_data.get("edges", [])
        
        if not nodes:
            self.logger.warning("No nodes in network data")
            return str(save_path)
        
        # Create NetworkX graph for layout calculation
        G = self._create_networkx_graph(nodes, edges)
        
        # Calculate layout positions
        pos = self._calculate_layout(G, layout)
        
        # Create Plotly visualization
        fig = self._create_plotly_network(G, pos, nodes, edges, width, height)
        
        # Add title and styling
        self._apply_theme_styling(fig, "Q-Memetic AI Noosphere")
        
        # Save visualization
        if interactive:
            pyo.plot(fig, filename=str(save_path), auto_open=False)
        else:
            fig.write_image(str(save_path.with_suffix('.png')))
        
        self.logger.info(f"Noosphere visualization saved to: {save_path}")
        return str(save_path)
    
    def create_evolution_timeline(
        self,
        memes: List[Dict],
        save_path: Optional[str] = None,
        width: int = 1400,
        height: int = 600
    ) -> str:
        """
        Create evolution timeline visualization.
        
        Args:
            memes: List of meme data with evolution information
            save_path: Path to save visualization
            width: Visualization width
            height: Visualization height
            
        Returns:
            Path to created visualization file
        """
        if save_path is None:
            timestamp = int(time.time())
            save_path = self.output_dir / f"evolution_timeline_{timestamp}.html"
        
        # Prepare timeline data
        timeline_data = self._prepare_timeline_data(memes)
        
        # Create subplot layout
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=("Meme Evolution Tree", "Fitness Over Time"),
            vertical_spacing=0.15,
            row_heights=[0.7, 0.3]
        )
        
        # Add evolution tree
        tree_traces = self._create_evolution_tree(timeline_data)
        for trace in tree_traces:
            fig.add_trace(trace, row=1, col=1)
        
        # Add fitness timeline
        fitness_trace = self._create_fitness_timeline(timeline_data)
        fig.add_trace(fitness_trace, row=2, col=1)
        
        # Update layout
        fig.update_layout(
            width=width,
            height=height,
            showlegend=True
        )
        
        self._apply_theme_styling(fig, "Meme Evolution Timeline")
        
        # Save visualization
        pyo.plot(fig, filename=str(save_path), auto_open=False)
        
        self.logger.info(f"Evolution timeline saved to: {save_path}")
        return str(save_path)
    
    def create_entanglement_heatmap(
        self,
        entanglement_matrix: np.ndarray,
        meme_labels: List[str],
        save_path: Optional[str] = None,
        width: int = 800,
        height: int = 800
    ) -> str:
        """
        Create entanglement strength heatmap.
        
        Args:
            entanglement_matrix: Matrix of entanglement strengths
            meme_labels: Labels for memes
            save_path: Path to save visualization
            width: Visualization width
            height: Visualization height
            
        Returns:
            Path to created visualization file
        """
        if save_path is None:
            timestamp = int(time.time())
            save_path = self.output_dir / f"entanglement_heatmap_{timestamp}.html"
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=entanglement_matrix,
            x=meme_labels,
            y=meme_labels,
            colorscale='Viridis',
            hoverongaps=False,
            hovertemplate='<b>%{y}</b><br>' +
                         '<b>%{x}</b><br>' +
                         'Entanglement: %{z:.3f}<extra></extra>'
        ))
        
        fig.update_layout(
            title="Quantum Entanglement Strength Matrix",
            width=width,
            height=height,
            xaxis_title="Memes",
            yaxis_title="Memes"
        )
        
        self._apply_theme_styling(fig, "Entanglement Heatmap")
        
        # Save visualization
        pyo.plot(fig, filename=str(save_path), auto_open=False)
        
        self.logger.info(f"Entanglement heatmap saved to: {save_path}")
        return str(save_path)
    
    def create_cognitive_landscape(
        self,
        meme_embeddings: np.ndarray,
        meme_labels: List[str],
        fitness_scores: List[float],
        save_path: Optional[str] = None,
        width: int = 1000,
        height: int = 700
    ) -> str:
        """
        Create 3D cognitive landscape visualization.
        
        Args:
            meme_embeddings: High-dimensional meme embeddings (will be reduced to 3D)
            meme_labels: Labels for memes
            fitness_scores: Fitness scores for color mapping
            save_path: Path to save visualization
            width: Visualization width
            height: Visualization height
            
        Returns:
            Path to created visualization file
        """
        if save_path is None:
            timestamp = int(time.time())
            save_path = self.output_dir / f"cognitive_landscape_{timestamp}.html"
        
        # Reduce dimensionality to 3D using PCA
        from sklearn.decomposition import PCA
        
        pca = PCA(n_components=3)
        embeddings_3d = pca.fit_transform(meme_embeddings)
        
        # Create 3D scatter plot
        fig = go.Figure(data=go.Scatter3d(
            x=embeddings_3d[:, 0],
            y=embeddings_3d[:, 1],
            z=embeddings_3d[:, 2],
            mode='markers+text',
            marker=dict(
                size=8,
                color=fitness_scores,
                colorscale='Viridis',
                colorbar=dict(title="Fitness Score"),
                opacity=0.8
            ),
            text=meme_labels,
            textposition="top center",
            hovertemplate='<b>%{text}</b><br>' +
                         'X: %{x:.2f}<br>' +
                         'Y: %{y:.2f}<br>' +
                         'Z: %{z:.2f}<br>' +
                         'Fitness: %{marker.color:.3f}<extra></extra>'
        ))
        
        fig.update_layout(
            title="Cognitive Landscape - 3D Meme Space",
            scene=dict(
                xaxis_title="PC1",
                yaxis_title="PC2",
                zaxis_title="PC3"
            ),
            width=width,
            height=height
        )
        
        self._apply_theme_styling(fig, "Cognitive Landscape")
        
        # Save visualization
        pyo.plot(fig, filename=str(save_path), auto_open=False)
        
        self.logger.info(f"Cognitive landscape saved to: {save_path}")
        return str(save_path)
    
    def create_propagation_animation(
        self,
        network_data: Dict[str, Any],
        propagation_steps: List[Dict],
        save_path: Optional[str] = None,
        width: int = 1000,
        height: int = 700
    ) -> str:
        """
        Create animated visualization of meme propagation.
        
        Args:
            network_data: Network structure
            propagation_steps: List of propagation steps with timestamps
            save_path: Path to save visualization
            width: Visualization width
            height: Visualization height
            
        Returns:
            Path to created visualization file
        """
        if save_path is None:
            timestamp = int(time.time())
            save_path = self.output_dir / f"propagation_animation_{timestamp}.html"
        
        # Create base network
        nodes = network_data.get("nodes", [])
        edges = network_data.get("edges", [])
        
        G = self._create_networkx_graph(nodes, edges)
        pos = self._calculate_layout(G, "force_directed")
        
        # Create animation frames
        frames = []
        for step_idx, step in enumerate(propagation_steps):
            frame_data = self._create_propagation_frame(G, pos, step, step_idx)
            frames.append(go.Frame(
                data=frame_data,
                name=str(step_idx)
            ))
        
        # Create initial frame
        initial_data = self._create_propagation_frame(G, pos, propagation_steps[0], 0)
        
        fig = go.Figure(
            data=initial_data,
            frames=frames
        )
        
        # Add animation controls
        fig.update_layout(
            updatemenus=[{
                "type": "buttons",
                "showactive": False,
                "buttons": [
                    {
                        "label": "Play",
                        "method": "animate",
                        "args": [None, {
                            "frame": {"duration": 500, "redraw": True},
                            "fromcurrent": True
                        }]
                    },
                    {
                        "label": "Pause",
                        "method": "animate",
                        "args": [[None], {
                            "frame": {"duration": 0, "redraw": False},
                            "mode": "immediate",
                            "transition": {"duration": 0}
                        }]
                    }
                ]
            }],
            sliders=[{
                "steps": [
                    {
                        "args": [[str(i)], {
                            "frame": {"duration": 300, "redraw": True},
                            "mode": "immediate",
                            "transition": {"duration": 300}
                        }],
                        "label": f"Step {i}",
                        "method": "animate"
                    }
                    for i in range(len(propagation_steps))
                ],
                "active": 0,
                "currentvalue": {"prefix": "Step: "},
                "len": 0.9,
                "x": 0.1,
                "xanchor": "left",
                "y": 0,
                "yanchor": "top"
            }],
            width=width,
            height=height
        )
        
        self._apply_theme_styling(fig, "Meme Propagation Animation")
        
        # Save visualization
        pyo.plot(fig, filename=str(save_path), auto_open=False)
        
        self.logger.info(f"Propagation animation saved to: {save_path}")
        return str(save_path)
    
    def _create_networkx_graph(self, nodes: List[Dict], edges: List[Dict]) -> nx.Graph:
        """Create NetworkX graph from node and edge data."""
        G = nx.Graph()
        
        # Add nodes
        for node in nodes:
            G.add_node(
                node["id"],
                **node.get("data", {})
            )
        
        # Add edges
        for edge in edges:
            G.add_edge(
                edge["source"],
                edge["target"],
                **edge.get("data", {})
            )
        
        return G
    
    def _calculate_layout(self, G: nx.Graph, layout: str) -> Dict[str, Tuple[float, float]]:
        """Calculate node positions using specified layout algorithm."""
        if layout == "force_directed":
            return nx.spring_layout(G, k=1, iterations=50)
        elif layout == "circular":
            return nx.circular_layout(G)
        elif layout == "hierarchical":
            return nx.kamada_kawai_layout(G)
        else:
            return nx.spring_layout(G)
    
    def _create_plotly_network(
        self,
        G: nx.Graph,
        pos: Dict,
        nodes: List[Dict],
        edges: List[Dict],
        width: int,
        height: int
    ) -> go.Figure:
        """Create Plotly network visualization."""
        # Prepare edge traces
        edge_traces = []
        
        for edge in edges:
            source_id = edge["source"]
            target_id = edge["target"]
            
            if source_id in pos and target_id in pos:
                x0, y0 = pos[source_id]
                x1, y1 = pos[target_id]
                
                # Edge line
                edge_trace = go.Scatter(
                    x=[x0, x1, None],
                    y=[y0, y1, None],
                    line=dict(width=edge.get("data", {}).get("weight", 0.5) * 3, 
                             color=self.current_theme["edge_color"]),
                    hoverinfo='none',
                    mode='lines',
                    showlegend=False
                )
                edge_traces.append(edge_trace)
        
        # Prepare node trace
        node_x = []
        node_y = []
        node_text = []
        node_colors = []
        node_sizes = []
        
        for node in nodes:
            node_id = node["id"]
            if node_id in pos:
                x, y = pos[node_id]
                node_x.append(x)
                node_y.append(y)
                
                # Node info for hover
                node_data = node.get("data", {})
                fitness = node_data.get("fitness", 0)
                generation = node_data.get("generation", 0)
                content = node_data.get("content", "")[:50] + "..."
                
                node_text.append(f"ID: {node_id}<br>" +
                               f"Fitness: {fitness:.3f}<br>" +
                               f"Generation: {generation}<br>" +
                               f"Content: {content}")
                
                # Node styling
                node_colors.append(fitness)
                node_sizes.append(max(10, fitness * 20 + 10))
        
        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=node_text,
            marker=dict(
                showscale=True,
                colorscale='Viridis',
                reversescale=True,
                color=node_colors,
                size=node_sizes,
                colorbar=dict(
                    thickness=15,
                    len=0.5,
                    x=1.02,
                    title="Fitness"
                ),
                line=dict(width=2, color=self.current_theme["text_color"])
            ),
            showlegend=False
        )
        
        # Create figure
        fig = go.Figure(data=edge_traces + [node_trace])
        
        fig.update_layout(
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            annotations=[ 
                dict(
                    text="Interactive Noosphere - Click and drag to explore",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002,
                    xanchor='left', yanchor='bottom',
                    font=dict(color=self.current_theme["text_color"], size=12)
                )
            ],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            width=width,
            height=height
        )
        
        return fig
    
    def _prepare_timeline_data(self, memes: List[Dict]) -> Dict[str, Any]:
        """Prepare data for timeline visualization."""
        # Sort memes by generation and timestamp
        sorted_memes = sorted(memes, key=lambda m: (
            m.get("metadata", {}).get("generation", 0),
            m.get("metadata", {}).get("timestamp", 0)
        ))
        
        timeline_data = {
            "memes": sorted_memes,
            "generations": {},
            "fitness_over_time": []
        }
        
        # Group by generation
        for meme in sorted_memes:
            gen = meme.get("metadata", {}).get("generation", 0)
            if gen not in timeline_data["generations"]:
                timeline_data["generations"][gen] = []
            timeline_data["generations"][gen].append(meme)
        
        # Fitness over time
        for i, meme in enumerate(sorted_memes):
            fitness = meme.get("vector", {}).get("fitness_score", 0)
            timeline_data["fitness_over_time"].append({
                "step": i,
                "fitness": fitness,
                "meme_id": meme.get("meme_id", f"meme_{i}"),
                "generation": meme.get("metadata", {}).get("generation", 0)
            })
        
        return timeline_data
    
    def _create_evolution_tree(self, timeline_data: Dict) -> List[go.Scatter]:
        """Create evolution tree traces."""
        traces = []
        
        # This is a simplified tree - in practice would calculate proper tree layout
        generations = timeline_data["generations"]
        
        for gen, memes in generations.items():
            x_positions = list(range(len(memes)))
            y_positions = [gen] * len(memes)
            
            trace = go.Scatter(
                x=x_positions,
                y=y_positions,
                mode='markers+text',
                text=[f"G{gen}-{i}" for i in range(len(memes))],
                textposition="top center",
                marker=dict(
                    size=12,
                    color=self.current_theme["node_colors"][gen % len(self.current_theme["node_colors"])],
                    line=dict(width=1, color=self.current_theme["text_color"])
                ),
                name=f"Generation {gen}",
                hovertemplate='<b>Generation %{y}</b><br>' +
                             'Position: %{x}<br>' +
                             '<extra></extra>'
            )
            traces.append(trace)
        
        return traces
    
    def _create_fitness_timeline(self, timeline_data: Dict) -> go.Scatter:
        """Create fitness timeline trace."""
        fitness_data = timeline_data["fitness_over_time"]
        
        return go.Scatter(
            x=[d["step"] for d in fitness_data],
            y=[d["fitness"] for d in fitness_data],
            mode='lines+markers',
            name='Average Fitness',
            line=dict(color=self.current_theme["highlight_color"], width=2),
            marker=dict(size=6),
            hovertemplate='<b>Step %{x}</b><br>' +
                         'Fitness: %{y:.3f}<br>' +
                         '<extra></extra>'
        )
    
    def _create_propagation_frame(
        self,
        G: nx.Graph,
        pos: Dict,
        step_data: Dict,
        step_idx: int
    ) -> List[go.Scatter]:
        """Create single frame for propagation animation."""
        # This is a simplified implementation
        # In practice, would show actual propagation paths and timing
        
        traces = []
        
        # Base network
        edge_trace = go.Scatter(
            x=[],
            y=[],
            line=dict(width=0.5, color=self.current_theme["edge_color"]),
            hoverinfo='none',
            mode='lines',
            showlegend=False
        )
        
        # Add edges
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace['x'] += (x0, x1, None)
            edge_trace['y'] += (y0, y1, None)
        
        traces.append(edge_trace)
        
        # Animated nodes
        active_nodes = step_data.get("active_nodes", list(G.nodes())[:step_idx+1])
        
        node_trace = go.Scatter(
            x=[pos[node][0] for node in active_nodes],
            y=[pos[node][1] for node in active_nodes],
            mode='markers',
            marker=dict(
                size=[15 if node in step_data.get("new_nodes", []) else 10 for node in active_nodes],
                color=self.current_theme["highlight_color"],
                line=dict(width=2, color=self.current_theme["text_color"])
            ),
            text=active_nodes,
            hoverinfo='text',
            showlegend=False
        )
        
        traces.append(node_trace)
        
        return traces
    
    def _apply_theme_styling(self, fig: go.Figure, title: str):
        """Apply theme styling to figure."""
        fig.update_layout(
            title=dict(
                text=title,
                font=dict(color=self.current_theme["text_color"], size=20),
                x=0.5
            ),
            plot_bgcolor=self.current_theme["bg_color"],
            paper_bgcolor=self.current_theme["paper_color"],
            font=dict(color=self.current_theme["text_color"])
        )
