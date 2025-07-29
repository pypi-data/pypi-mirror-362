"""Vector Store implementation for Arc Advisor using ChromaDB.

This module provides semantic search capabilities for the Failure Bank,
enabling sophisticated pattern discovery and failure clustering.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime

import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer

logger = logging.getLogger("ArcVectorStore")


class ArcVectorStore:
    """Vector database for semantic search across agent traces.
    
    Implements the Failure Bank component shown in the architecture,
    providing semantic similarity search, pattern discovery, and
    failure clustering capabilities.
    """
    
    def __init__(
        self,
        collection_name: str = "arc_events",
        persist_directory: Optional[str] = None,
        embedding_model: str = "all-MiniLM-L6-v2",
    ):
        """Initialize the vector store.
        
        Args:
            collection_name: Name of the ChromaDB collection.
            persist_directory: Directory to persist the database. 
                             Defaults to ~/.arc/vector_db
            embedding_model: Sentence transformer model for embeddings.
        """
        self.collection_name = collection_name
        self.embedding_model_name = embedding_model
        
        # Set up persistence directory
        if persist_directory is None:
            persist_directory = str(Path.home() / ".arc" / "vector_db")
        Path(persist_directory).mkdir(parents=True, exist_ok=True)
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Initialize sentence transformer for embeddings
        self.sentence_model = SentenceTransformer(embedding_model)
        
        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}  # Use cosine similarity
        )
        
        logger.info(f"Vector store initialized with collection '{collection_name}'")
    
    def _generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text using sentence transformer.
        
        Args:
            text: Text to embed.
            
        Returns:
            Embedding vector as list of floats.
        """
        embedding = self.sentence_model.encode(text, convert_to_tensor=False)
        return embedding.tolist()
    
    def _create_document_text(self, event: Dict[str, Any]) -> str:
        """Create searchable text from an event.
        
        Args:
            event: Event dictionary from logs.
            
        Returns:
            Concatenated text for embedding.
        """
        event_data = event.get("event", {})
        message_type = event_data.get("message_type", "")
        
        if message_type == "ArcImprovementRequest":
            payload = event_data.get("payload", {})
            failure_context = payload.get("failure_context", {})
            
            # Create rich text representation
            parts = [
                f"Failure: {payload.get('failure_category', 'Unknown')}",
                f"Error: {failure_context.get('error', '')}",
                f"Message: {failure_context.get('error_message', '')}",
                f"Context: {json.dumps(failure_context, separators=(',', ':'))}"
            ]
            return " ".join(filter(None, parts))
        
        elif message_type == "ArcLearningReport":
            payload = event_data.get("payload", {})
            
            # Create text for successful/failed execution
            status = "Success" if payload.get("success") else "Failure"
            parts = [
                f"Execution: {status}",
                f"Output: {json.dumps(payload.get('output', {}), separators=(',', ':'))}",
                f"Metrics: {json.dumps(payload.get('metrics', {}), separators=(',', ':'))}"
            ]
            return " ".join(filter(None, parts))
        
        # Fallback for other event types
        return json.dumps(event, separators=(',', ':'))
    
    def index_event(self, event: Dict[str, Any]) -> str:
        """Index a single event in the vector store.
        
        Args:
            event: Event dictionary to index.
            
        Returns:
            Document ID in the vector store.
        """
        # Generate unique ID
        doc_id = f"{event.get('timestamp', '')}_{event.get('event', {}).get('trace_id', '')}"
        
        # Create document text
        doc_text = self._create_document_text(event)
        
        # Generate embedding
        embedding = self._generate_embedding(doc_text)
        
        # Prepare metadata
        metadata = {
            "timestamp": event.get("timestamp", ""),
            "message_type": event.get("event", {}).get("message_type", ""),
            "agent_id": event.get("event", {}).get("agent_id", ""),
            "trace_id": event.get("event", {}).get("trace_id", ""),
        }
        
        # Add specific metadata based on message type
        if metadata["message_type"] == "ArcImprovementRequest":
            payload = event.get("event", {}).get("payload", {})
            metadata["failure_category"] = payload.get("failure_category", "")
            metadata["has_error_message"] = bool(
                payload.get("failure_context", {}).get("error_message")
            )
        elif metadata["message_type"] == "ArcLearningReport":
            payload = event.get("event", {}).get("payload", {})
            metadata["success"] = payload.get("success", False)
        
        # Add to collection
        self.collection.add(
            embeddings=[embedding],
            documents=[doc_text],
            metadatas=[metadata],
            ids=[doc_id]
        )
        
        return doc_id
    
    def search_similar_failures(
        self,
        query: str,
        failure_category: Optional[str] = None,
        limit: int = 5,
        min_similarity: float = 0.7,
    ) -> List[Dict[str, Any]]:
        """Search for similar failures using semantic search.
        
        Args:
            query: Search query (can be error message, context, etc).
            failure_category: Optional filter by failure category.
            limit: Maximum number of results.
            min_similarity: Minimum similarity score (0-1).
            
        Returns:
            List of similar failures with metadata and similarity scores.
        """
        # Generate query embedding
        query_embedding = self._generate_embedding(query)
        
        # Build filter
        where_filter = {"message_type": "ArcImprovementRequest"}
        if failure_category:
            where_filter["failure_category"] = failure_category
        
        # Query collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=limit * 2,  # Get more to filter by similarity
            where=where_filter,
            include=["metadatas", "documents", "distances"]
        )
        
        # Process results
        similar_failures = []
        if results["ids"] and results["ids"][0]:
            for i, doc_id in enumerate(results["ids"][0]):
                # Convert distance to similarity score (1 - distance for cosine)
                similarity = 1 - results["distances"][0][i]
                
                if similarity >= min_similarity:
                    similar_failures.append({
                        "id": doc_id,
                        "similarity": similarity,
                        "metadata": results["metadatas"][0][i],
                        "document": results["documents"][0][i],
                    })
        
        # Sort by similarity and limit
        similar_failures.sort(key=lambda x: x["similarity"], reverse=True)
        return similar_failures[:limit]
    
    def get_failure_clusters(
        self,
        min_cluster_size: int = 3,
        similarity_threshold: float = 0.8,
    ) -> List[Dict[str, Any]]:
        """Identify clusters of similar failures.
        
        This helps discover common failure patterns across the system.
        
        Args:
            min_cluster_size: Minimum failures to form a cluster.
            similarity_threshold: Minimum similarity to be in same cluster.
            
        Returns:
            List of failure clusters with representative examples.
        """
        # Get all failures
        all_failures = self.collection.get(
            where={"message_type": "ArcImprovementRequest"},
            include=["embeddings", "metadatas", "documents"]
        )
        
        if not all_failures["ids"]:
            return []
        
        # Simple clustering using similarity threshold
        clusters = []
        processed = set()
        
        for i, doc_id in enumerate(all_failures["ids"]):
            if doc_id in processed:
                continue
            
            # Find similar failures
            cluster_members = [i]
            cluster_embedding = all_failures["embeddings"][i]
            
            for j, other_id in enumerate(all_failures["ids"]):
                if i != j and other_id not in processed:
                    # Calculate similarity
                    other_embedding = all_failures["embeddings"][j]
                    similarity = self._cosine_similarity(
                        cluster_embedding, other_embedding
                    )
                    
                    if similarity >= similarity_threshold:
                        cluster_members.append(j)
                        processed.add(other_id)
            
            # Create cluster if large enough
            if len(cluster_members) >= min_cluster_size:
                # Extract common keywords from cluster
                cluster_docs = [all_failures["documents"][idx] for idx in cluster_members]
                common_keywords = self._extract_common_keywords(cluster_docs)
                
                clusters.append({
                    "cluster_id": f"cluster_{len(clusters)}",
                    "size": len(cluster_members),
                    "common_keywords": common_keywords[:5],
                    "representative_failure": {
                        "id": all_failures["ids"][cluster_members[0]],
                        "metadata": all_failures["metadatas"][cluster_members[0]],
                        "document": all_failures["documents"][cluster_members[0]],
                    },
                    "member_ids": [all_failures["ids"][idx] for idx in cluster_members],
                })
            
            processed.add(doc_id)
        
        # Sort clusters by size
        clusters.sort(key=lambda x: x["size"], reverse=True)
        return clusters
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        import numpy as np
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    
    def _extract_common_keywords(self, documents: List[str]) -> List[str]:
        """Extract common keywords from a list of documents."""
        from collections import Counter
        
        # Simple keyword extraction
        stop_words = {
            "the", "a", "an", "is", "in", "on", "at", "to", "for", "of", 
            "with", "and", "or", "but", "as", "by", "from", "up", "about",
            "into", "through", "during", "before", "after", "above", "below",
            "between", "under", "again", "further", "then", "once"
        }
        
        word_count = Counter()
        for doc in documents:
            words = doc.lower().split()
            for word in words:
                # Clean and filter
                word = word.strip(".,!?;:\"'()[]{}").strip()
                if word and len(word) > 2 and word not in stop_words:
                    word_count[word] += 1
        
        # Return most common words
        return [word for word, _ in word_count.most_common(10)]
    
    def query_success_patterns(
        self,
        task_description: str,
        limit: int = 5,
    ) -> List[Dict[str, Any]]:
        """Find successful execution patterns similar to a task.
        
        Args:
            task_description: Description of the task.
            limit: Maximum number of results.
            
        Returns:
            List of successful executions with strategies.
        """
        # Generate query embedding
        query_embedding = self._generate_embedding(task_description)
        
        # Query for successful executions
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=limit,
            where={
                "message_type": "ArcLearningReport",
                "success": True
            },
            include=["metadatas", "documents", "distances"]
        )
        
        # Process results
        success_patterns = []
        if results["ids"] and results["ids"][0]:
            for i, doc_id in enumerate(results["ids"][0]):
                similarity = 1 - results["distances"][0][i]
                success_patterns.append({
                    "id": doc_id,
                    "similarity": similarity,
                    "metadata": results["metadatas"][0][i],
                    "document": results["documents"][0][i],
                })
        
        return success_patterns
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the vector store.
        
        Returns:
            Dictionary with collection statistics.
        """
        # Get all documents to count by type
        all_docs = self.collection.get(include=["metadatas"])
        total_count = len(all_docs["ids"])
        
        # Count by message type
        failures = 0
        reports = 0
        successes = 0
        
        for metadata in all_docs.get("metadatas", []):
            msg_type = metadata.get("message_type")
            if msg_type == "ArcImprovementRequest":
                failures += 1
            elif msg_type == "ArcLearningReport":
                reports += 1
                if metadata.get("success", False):
                    successes += 1
        
        return {
            "total_events": total_count,
            "failure_requests": failures,
            "learning_reports": reports,
            "successful_executions": successes,
            "failed_executions": reports - successes if reports > 0 else 0,
            "collection_name": self.collection_name,
            "embedding_model": self.embedding_model_name,
        }