"""
Convert Clang AST to NetworkX graphs for analysis.
"""

from typing import Any, Dict, List, Tuple

import networkx as nx

from .models import GraphData


class GraphConverter:
    """Convert Clang AST to NetworkX graphs."""

    def __init__(self):
        """Initialize the graph converter."""
        pass

    def ast_to_graph(self, ast_data: Dict[str, Any]) -> nx.DiGraph:
        """
        Convert AST data to a directed graph.

        Args:
            ast_data: AST data from Clang parser

        Returns:
            NetworkX directed graph representing the AST
        """
        graph = nx.DiGraph()
        self._add_ast_nodes(graph, ast_data, parent_id=None)
        return graph

    def _add_ast_nodes(
        self,
        graph: nx.DiGraph,
        node: Dict[str, Any],
        parent_id: str = None,
        node_counter: List[int] = None,
    ) -> str:
        """
        Recursively add AST nodes to the graph.

        Args:
            graph: NetworkX graph to add nodes to
            node: Current AST node
            parent_id: ID of parent node
            node_counter: Counter for unique node IDs

        Returns:
            ID of the current node
        """
        if node_counter is None:
            node_counter = [0]

        # Create unique node ID
        node_id = f"node_{node_counter[0]}"
        node_counter[0] += 1

        # Add node with attributes
        graph.add_node(
            node_id,
            **{
                "kind": node.get("kind", ""),
                "spelling": node.get("spelling", ""),
                "type": node.get("type", ""),
                "label": self._create_node_label(node),
            },
        )

        # Add edge from parent if exists
        if parent_id:
            graph.add_edge(parent_id, node_id)

        # Recursively add children
        for child in node.get("children", []):
            self._add_ast_nodes(graph, child, node_id, node_counter)

        return node_id

    def _create_node_label(self, node: Dict[str, Any]) -> str:
        """Create a descriptive label for the node."""
        kind = node.get("kind", "")
        spelling = node.get("spelling", "")
        node_type = node.get("type", "")

        if spelling:
            return f"{kind}:{spelling}"
        elif node_type:
            return f"{kind}:{node_type}"
        else:
            return kind

    def create_cfg(self, ast_data: Dict[str, Any]) -> nx.DiGraph:
        """
        Create a Control Flow Graph from AST data.
        Simplified implementation focusing on control flow.

        Args:
            ast_data: AST data from Clang parser

        Returns:
            NetworkX directed graph representing control flow
        """
        cfg = nx.DiGraph()
        self._build_cfg(cfg, ast_data)
        return cfg

    def _build_cfg(
        self,
        cfg: nx.DiGraph,
        node: Dict[str, Any],
        entry_block: str = None,
        exit_block: str = None,
        block_counter: List[int] = None,
    ) -> Tuple[str, str]:
        """
        Build CFG recursively.

        Returns:
            Tuple of (entry_block_id, exit_block_id) for this node
        """
        if block_counter is None:
            block_counter = [0]

        kind = node.get("kind", "")

        # Create basic block for this node
        block_id = f"block_{block_counter[0]}"
        block_counter[0] += 1

        cfg.add_node(
            block_id,
            **{
                "kind": kind,
                "label": self._create_node_label(node),
                "statements": [node.get("spelling", kind)],
            },
        )

        entry = block_id
        exit_node = block_id

        # Handle different control flow constructs
        if kind == "IF_STMT":
            entry, exit_node = self._handle_if_stmt(cfg, node, block_counter)
        elif kind in ["WHILE_STMT", "FOR_STMT"]:
            entry, exit_node = self._handle_loop_stmt(cfg, node, block_counter)
        elif kind == "COMPOUND_STMT":
            entry, exit_node = self._handle_compound_stmt(cfg, node, block_counter)
        else:
            # For other nodes, process children sequentially
            current = entry
            for child in node.get("children", []):
                child_entry, child_exit = self._build_cfg(
                    cfg, child, block_counter=block_counter
                )
                if child_entry:
                    cfg.add_edge(current, child_entry)
                    current = child_exit
            exit_node = current

        return entry, exit_node

    def _handle_if_stmt(
        self, cfg: nx.DiGraph, node: Dict[str, Any], block_counter: List[int]
    ) -> Tuple[str, str]:
        """Handle if statement in CFG."""
        # Create condition block
        cond_block = f"block_{block_counter[0]}"
        block_counter[0] += 1
        cfg.add_node(cond_block, kind="CONDITION", label="if condition")

        # Create merge block
        merge_block = f"block_{block_counter[0]}"
        block_counter[0] += 1
        cfg.add_node(merge_block, kind="MERGE", label="if merge")

        children = node.get("children", [])

        # Process then branch
        if len(children) > 1:
            then_entry, then_exit = self._build_cfg(
                cfg, children[1], block_counter=block_counter
            )
            cfg.add_edge(cond_block, then_entry, label="true")
            cfg.add_edge(then_exit, merge_block)

        # Process else branch if exists
        if len(children) > 2:
            else_entry, else_exit = self._build_cfg(
                cfg, children[2], block_counter=block_counter
            )
            cfg.add_edge(cond_block, else_entry, label="false")
            cfg.add_edge(else_exit, merge_block)
        else:
            # No else branch, condition can go directly to merge
            cfg.add_edge(cond_block, merge_block, label="false")

        return cond_block, merge_block

    def _handle_loop_stmt(
        self, cfg: nx.DiGraph, node: Dict[str, Any], block_counter: List[int]
    ) -> Tuple[str, str]:
        """Handle loop statements in CFG."""
        # Create loop header
        header_block = f"block_{block_counter[0]}"
        block_counter[0] += 1
        cfg.add_node(header_block, kind="LOOP_HEADER", label="loop condition")

        # Create exit block
        exit_block = f"block_{block_counter[0]}"
        block_counter[0] += 1
        cfg.add_node(exit_block, kind="LOOP_EXIT", label="loop exit")

        children = node.get("children", [])

        # Process loop body
        if children:
            body_entry, body_exit = self._build_cfg(
                cfg, children[-1], block_counter=block_counter
            )
            cfg.add_edge(header_block, body_entry, label="true")
            cfg.add_edge(body_exit, header_block)  # Back edge

        # Exit condition
        cfg.add_edge(header_block, exit_block, label="false")

        return header_block, exit_block

    def _handle_compound_stmt(
        self, cfg: nx.DiGraph, node: Dict[str, Any], block_counter: List[int]
    ) -> Tuple[str, str]:
        """Handle compound statements (blocks) in CFG."""
        children = node.get("children", [])
        if not children:
            # Empty block
            block_id = f"block_{block_counter[0]}"
            block_counter[0] += 1
            cfg.add_node(block_id, kind="EMPTY_BLOCK", label="empty")
            return block_id, block_id

        # Process children sequentially
        first_entry, first_exit = self._build_cfg(
            cfg, children[0], block_counter=block_counter
        )
        current_exit = first_exit

        for child in children[1:]:
            child_entry, child_exit = self._build_cfg(
                cfg, child, block_counter=block_counter
            )
            cfg.add_edge(current_exit, child_entry)
            current_exit = child_exit

        return first_entry, current_exit

    def graph_to_data(self, graph: nx.DiGraph) -> GraphData:
        """
        Convert NetworkX graph to GraphData model.

        Args:
            graph: NetworkX graph

        Returns:
            GraphData model
        """
        nodes = []
        for node_id, attrs in graph.nodes(data=True):
            node_data = {"id": node_id}
            node_data.update(attrs)
            nodes.append(node_data)

        edges = []
        for source, target, attrs in graph.edges(data=True):
            edge_data = {"source": source, "target": target}
            edge_data.update(attrs)
            edges.append(edge_data)

        return GraphData(
            nodes=nodes,
            edges=edges,
            graph_type="ast",  # Will be set appropriately by caller
        )
