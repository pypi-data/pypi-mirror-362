"""
Graph2Vec implementation for encoding graphs as vectors.
Simplified implementation using graph features and embeddings.
"""

from collections import Counter
from typing import List

import networkx as nx
import numpy as np
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer


class Graph2VecEncoder:
    """
    Graph2Vec encoder for converting graphs to vector embeddings.
    Uses a simplified approach based on graph features and structural patterns.
    """

    def __init__(self, embedding_dim: int = 128):
        """
        Initialize the Graph2Vec encoder.

        Args:
            embedding_dim: Dimension of the output embedding vectors
        """
        self.embedding_dim = embedding_dim
        self.vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 3))
        self.pca = PCA(n_components=embedding_dim)
        self.is_fitted = False

    def fit(self, graphs: List[nx.DiGraph]) -> None:
        """
        Fit the encoder on a collection of graphs.

        Args:
            graphs: List of NetworkX graphs to fit on
        """
        # Extract features from all graphs
        all_features = []
        for graph in graphs:
            features = self._extract_graph_features(graph)
            all_features.append(features)

        # Fit TF-IDF vectorizer on graph features
        feature_texts = [" ".join(features) for features in all_features]
        tfidf_features = self.vectorizer.fit_transform(feature_texts)

        # Fit PCA for dimensionality reduction
        if tfidf_features.shape[1] > self.embedding_dim:
            self.pca.fit(tfidf_features.toarray())
        else:
            # If features are already low-dimensional, adjust PCA
            self.pca = PCA(
                n_components=min(self.embedding_dim, tfidf_features.shape[1])
            )
            self.pca.fit(tfidf_features.toarray())

        self.is_fitted = True

    def encode(self, graph: nx.DiGraph) -> List[float]:
        """
        Encode a single graph as a vector.

        Args:
            graph: NetworkX graph to encode

        Returns:
            Vector embedding as list of floats
        """
        if not self.is_fitted:
            # If not fitted, use a simple encoding
            return self._simple_encode(graph)

        # Extract features
        features = self._extract_graph_features(graph)
        feature_text = " ".join(features)

        # Transform with TF-IDF
        tfidf_vector = self.vectorizer.transform([feature_text])

        # Apply PCA
        if hasattr(self.pca, "components_"):
            embedding = self.pca.transform(tfidf_vector.toarray())[0]
        else:
            # Fallback if PCA not properly fitted
            embedding = tfidf_vector.toarray()[0][: self.embedding_dim]

        # Ensure correct dimensionality
        if len(embedding) < self.embedding_dim:
            # Pad with zeros
            embedding = np.pad(embedding, (0, self.embedding_dim - len(embedding)))
        elif len(embedding) > self.embedding_dim:
            # Truncate
            embedding = embedding[: self.embedding_dim]

        return embedding.tolist()

    def _simple_encode(self, graph: nx.DiGraph) -> List[float]:
        """
        Simple encoding for when the encoder is not fitted.
        Uses basic graph statistics.
        """
        features = []

        # Basic graph statistics
        features.extend(
            [
                len(graph.nodes()),  # Number of nodes
                len(graph.edges()),  # Number of edges
                nx.density(graph) if len(graph.nodes()) > 1 else 0.0,  # Density
            ]
        )

        # Degree statistics
        if len(graph.nodes()) > 0:
            degrees = [graph.degree(n) for n in graph.nodes()]
            features.extend(
                [
                    np.mean(degrees),
                    np.std(degrees) if len(degrees) > 1 else 0.0,
                    max(degrees) if degrees else 0,
                ]
            )
        else:
            features.extend([0.0, 0.0, 0])

        # Node type distribution
        node_types = [graph.nodes[n].get("kind", "unknown") for n in graph.nodes()]
        type_counts = Counter(node_types)

        # Add top node types as features
        common_types = [
            "FUNCTION_DECL",
            "COMPOUND_STMT",
            "IF_STMT",
            "WHILE_STMT",
            "FOR_STMT",
            "BINARY_OPERATOR",
            "CALL_EXPR",
            "DECL_REF_EXPR",
        ]

        for node_type in common_types:
            features.append(type_counts.get(node_type, 0))

        # Structural features
        if len(graph.nodes()) > 0:
            try:
                # Average clustering coefficient
                clustering = nx.average_clustering(graph.to_undirected())
                features.append(clustering)
            except:
                features.append(0.0)

            # Number of strongly connected components
            try:
                scc_count = nx.number_strongly_connected_components(graph)
                features.append(scc_count)
            except:
                features.append(1)
        else:
            features.extend([0.0, 0])

        # Pad or truncate to desired dimension
        while len(features) < self.embedding_dim:
            features.append(0.0)

        return features[: self.embedding_dim]

    def _extract_graph_features(self, graph: nx.DiGraph) -> List[str]:
        """
        Extract textual features from a graph for TF-IDF processing.

        Args:
            graph: NetworkX graph

        Returns:
            List of feature strings
        """
        features = []

        # Node type features
        for node in graph.nodes():
            node_data = graph.nodes[node]
            kind = node_data.get("kind", "unknown")
            features.append(f"node_{kind}")

            # Add spelling/label if available
            spelling = node_data.get("spelling", "")
            if spelling:
                features.append(f"spell_{spelling}")

        # Edge features
        for source, target in graph.edges():
            source_kind = graph.nodes[source].get("kind", "unknown")
            target_kind = graph.nodes[target].get("kind", "unknown")
            features.append(f"edge_{source_kind}_{target_kind}")

        # Structural patterns
        features.extend(self._extract_structural_patterns(graph))

        # Path features (limited to avoid explosion)
        features.extend(self._extract_path_features(graph))

        return features

    def _extract_structural_patterns(self, graph: nx.DiGraph) -> List[str]:
        """Extract structural patterns from the graph."""
        patterns = []

        # Degree patterns
        degree_sequence = sorted([graph.degree(n) for n in graph.nodes()], reverse=True)
        if degree_sequence:
            patterns.append(f"max_degree_{degree_sequence[0]}")
            patterns.append(f"min_degree_{degree_sequence[-1]}")

        # Subgraph patterns (simple motifs)
        for node in graph.nodes():
            neighbors = list(graph.neighbors(node))
            if len(neighbors) == 1:
                patterns.append("chain_pattern")
            elif len(neighbors) > 2:
                patterns.append("hub_pattern")

        # Control flow patterns
        for node in graph.nodes():
            kind = graph.nodes[node].get("kind", "")
            if kind in ["IF_STMT", "WHILE_STMT", "FOR_STMT"]:
                out_degree = graph.out_degree(node)
                patterns.append(f"control_{kind}_{out_degree}")

        return patterns

    def _extract_path_features(
        self, graph: nx.DiGraph, max_paths: int = 50
    ) -> List[str]:
        """Extract path-based features from the graph."""
        paths = []

        # Find some simple paths (limited to avoid complexity explosion)
        nodes = list(graph.nodes())
        path_count = 0

        for i, start in enumerate(nodes):
            if path_count >= max_paths:
                break
            for j, end in enumerate(nodes[i + 1 :], i + 1):
                if path_count >= max_paths:
                    break
                try:
                    if nx.has_path(graph, start, end):
                        path = nx.shortest_path(graph, start, end)
                        if len(path) <= 4:  # Only short paths
                            path_kinds = [
                                graph.nodes[n].get("kind", "unknown") for n in path
                            ]
                            paths.append(f"path_{'_'.join(path_kinds)}")
                            path_count += 1
                except:
                    continue

        return paths
