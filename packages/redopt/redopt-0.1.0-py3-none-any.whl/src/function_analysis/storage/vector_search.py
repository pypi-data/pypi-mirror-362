"""
Vector similarity search for function embeddings.
"""

from typing import Any, Dict, List, Optional

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from ..core.models import SimilarityResult
from .redis_client import RedisClient


class VectorSearch:
    """Vector similarity search for function embeddings."""

    def __init__(self, redis_client: RedisClient):
        """
        Initialize vector search.

        Args:
            redis_client: Redis client for data access
        """
        self.redis_client = redis_client

    def find_similar_functions(
        self,
        query_embedding: List[float],
        top_k: int = 10,
        threshold: float = 0.7,
        exclude_ids: Optional[List[str]] = None,
    ) -> List[SimilarityResult]:
        """
        Find functions similar to the query embedding.

        Args:
            query_embedding: Query embedding vector
            top_k: Number of top results to return
            threshold: Minimum similarity threshold
            exclude_ids: Function IDs to exclude from results

        Returns:
            List of SimilarityResult objects
        """
        try:
            # Get all function embeddings
            all_embeddings = self.redis_client.get_function_embeddings()

            if not all_embeddings:
                return []

            # Filter out excluded IDs
            if exclude_ids:
                all_embeddings = {
                    k: v for k, v in all_embeddings.items() if k not in exclude_ids
                }

            # Calculate similarities
            similarities = []
            query_vector = np.array(query_embedding).reshape(1, -1)

            for function_id, embedding in all_embeddings.items():
                try:
                    embedding_vector = np.array(embedding).reshape(1, -1)

                    # Ensure same dimensionality
                    if embedding_vector.shape[1] != query_vector.shape[1]:
                        continue

                    # Calculate cosine similarity
                    similarity = cosine_similarity(query_vector, embedding_vector)[0][0]

                    if similarity >= threshold:
                        similarities.append((function_id, similarity))

                except Exception as e:
                    print(f"Error calculating similarity for {function_id}: {e}")
                    continue

            # Sort by similarity (descending)
            similarities.sort(key=lambda x: x[1], reverse=True)

            # Get top-k results
            top_similarities = similarities[:top_k]

            # Convert to SimilarityResult objects
            results = []
            for function_id, similarity in top_similarities:
                analysis = self.redis_client.get_function_analysis(function_id)
                if analysis:
                    result = SimilarityResult(
                        function_id=function_id,
                        function_name=analysis.metadata.name,
                        similarity_score=float(similarity),
                        code_snippet=self._get_code_snippet(analysis.code),
                        metadata=analysis.metadata,
                    )
                    results.append(result)

            return results

        except Exception as e:
            print(f"Error in similarity search: {e}")
            return []

    def find_similar_by_function_id(
        self, function_id: str, top_k: int = 10, threshold: float = 0.7
    ) -> List[SimilarityResult]:
        """
        Find functions similar to a given function ID.

        Args:
            function_id: ID of the function to find similarities for
            top_k: Number of top results to return
            threshold: Minimum similarity threshold

        Returns:
            List of SimilarityResult objects
        """
        try:
            # Get the function's embedding
            embeddings = self.redis_client.get_function_embeddings([function_id])

            if function_id not in embeddings:
                return []

            query_embedding = embeddings[function_id]

            # Find similar functions (excluding the query function itself)
            return self.find_similar_functions(
                query_embedding=query_embedding,
                top_k=top_k,
                threshold=threshold,
                exclude_ids=[function_id],
            )

        except Exception as e:
            print(f"Error finding similar functions: {e}")
            return []

    def batch_similarity_search(
        self,
        query_embeddings: List[List[float]],
        top_k: int = 10,
        threshold: float = 0.7,
    ) -> List[List[SimilarityResult]]:
        """
        Perform batch similarity search for multiple queries.

        Args:
            query_embeddings: List of query embedding vectors
            top_k: Number of top results per query
            threshold: Minimum similarity threshold

        Returns:
            List of lists of SimilarityResult objects
        """
        results = []
        for embedding in query_embeddings:
            similar_functions = self.find_similar_functions(
                query_embedding=embedding, top_k=top_k, threshold=threshold
            )
            results.append(similar_functions)

        return results

    def get_function_clusters(
        self, threshold: float = 0.8, min_cluster_size: int = 2
    ) -> List[List[str]]:
        """
        Find clusters of similar functions.

        Args:
            threshold: Similarity threshold for clustering
            min_cluster_size: Minimum size for a cluster

        Returns:
            List of clusters, where each cluster is a list of function IDs
        """
        try:
            # Get all embeddings
            all_embeddings = self.redis_client.get_function_embeddings()

            if len(all_embeddings) < min_cluster_size:
                return []

            function_ids = list(all_embeddings.keys())
            embeddings_matrix = np.array([all_embeddings[fid] for fid in function_ids])

            # Calculate pairwise similarities
            similarities = cosine_similarity(embeddings_matrix)

            # Simple clustering: group functions that are similar enough
            clusters = []
            used_functions = set()

            for i, function_id in enumerate(function_ids):
                if function_id in used_functions:
                    continue

                # Find all functions similar to this one
                cluster = [function_id]
                used_functions.add(function_id)

                for j, other_function_id in enumerate(function_ids):
                    if (
                        i != j
                        and other_function_id not in used_functions
                        and similarities[i][j] >= threshold
                    ):
                        cluster.append(other_function_id)
                        used_functions.add(other_function_id)

                # Only keep clusters that meet minimum size
                if len(cluster) >= min_cluster_size:
                    clusters.append(cluster)

            return clusters

        except Exception as e:
            print(f"Error finding clusters: {e}")
            return []

    def _get_code_snippet(self, code: str, max_lines: int = 10) -> str:
        """
        Get a snippet of the function code.

        Args:
            code: Full function code
            max_lines: Maximum number of lines to include

        Returns:
            Code snippet
        """
        lines = code.strip().split("\n")
        if len(lines) <= max_lines:
            return code

        # Take first few lines and add ellipsis
        snippet_lines = lines[:max_lines]
        snippet = "\n".join(snippet_lines)

        if len(lines) > max_lines:
            snippet += "\n..."

        return snippet

    def get_embedding_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the embeddings in the database.

        Returns:
            Dictionary with embedding statistics
        """
        try:
            all_embeddings = self.redis_client.get_function_embeddings()

            if not all_embeddings:
                return {
                    "total_embeddings": 0,
                    "embedding_dimension": 0,
                    "average_norm": 0.0,
                    "std_norm": 0.0,
                }

            embeddings_matrix = np.array(list(all_embeddings.values()))

            # Calculate norms
            norms = np.linalg.norm(embeddings_matrix, axis=1)

            return {
                "total_embeddings": len(all_embeddings),
                "embedding_dimension": embeddings_matrix.shape[1],
                "average_norm": float(np.mean(norms)),
                "std_norm": float(np.std(norms)),
                "min_norm": float(np.min(norms)),
                "max_norm": float(np.max(norms)),
            }

        except Exception as e:
            print(f"Error getting embedding statistics: {e}")
            return {"total_embeddings": 0, "embedding_dimension": 0, "error": str(e)}
