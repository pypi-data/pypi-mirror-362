import json
import logging
import os

from typing import Any, Dict, List

import faiss
import numpy as np

from ..models import Document, VectorChunk
from ..settings import SUPPORTAL_SETTINGS

logger = logging.getLogger("django_supportal")


class VectorService:
    def __init__(self):
        self.vector_db_path = SUPPORTAL_SETTINGS["VECTOR_DB_PATH"]
        self.top_k = SUPPORTAL_SETTINGS["TOP_K_RESULTS"]
        self.dimension = 1536  # openai embedding dimension
        self.index = None
        self.metadata = {}
        self._ensure_vector_db_directory()

    def _ensure_vector_db_directory(self):
        """create vector db directory if it doesn't exist"""
        os.makedirs(self.vector_db_path, exist_ok=True)

    def create_index(self, business_id: int):
        """create or load faiss index for business"""
        index_path = os.path.join(self.vector_db_path, f"business_{business_id}.index")
        metadata_path = os.path.join(
            self.vector_db_path, f"business_{business_id}_metadata.json"
        )

        if os.path.exists(index_path) and os.path.exists(metadata_path):
            self.index = faiss.read_index(index_path)
            with open(metadata_path, "r") as f:
                self.metadata = json.load(f)
        else:
            self.index = faiss.IndexFlatL2(self.dimension)
            self.metadata = {}

    def add_document_chunks(
        self, document: Document, chunks_data: List[Dict[str, Any]]
    ):
        """add document chunks to vector index"""
        try:
            embeddings = []
            chunk_metadata = []

            for chunk_data in chunks_data:
                embedding = np.array(chunk_data["embedding"], dtype=np.float32)
                embeddings.append(embedding)

                # store metadata
                metadata = {
                    "document_id": document.id,
                    "chunk_index": chunk_data["chunk_index"],
                    "content": chunk_data["content"],
                    "document_title": document.title,
                }
                chunk_metadata.append(metadata)

            if embeddings:
                embeddings_array = np.array(embeddings)

                # add to faiss index
                start_idx = self.index.ntotal
                self.index.add(embeddings_array)

                # store metadata
                for i, metadata in enumerate(chunk_metadata):
                    self.metadata[start_idx + i] = metadata

                # save index and metadata
                self._save_index(document.business.id)

                logger.info(
                    f"added {len(embeddings)} chunks to vector index for document {document.id}"
                )

        except Exception as e:
            logger.error(f"error adding document chunks to vector index: {str(e)}")

    def search_similar_chunks(
        self, business_id: int, query_embedding: List[float], top_k: int = None
    ) -> List[Dict[str, Any]]:
        """search for similar chunks in vector index"""
        try:
            self.create_index(business_id)

            if self.index.ntotal == 0:
                return []

            top_k = top_k or self.top_k
            query_vector = np.array([query_embedding], dtype=np.float32)

            distances, indices = self.index.search(
                query_vector, min(top_k, self.index.ntotal)
            )

            results = []
            for distance, idx in zip(distances[0], indices[0]):
                if idx in self.metadata:
                    result = self.metadata[idx].copy()
                    result["similarity_score"] = float(distance)
                    results.append(result)

            return results

        except Exception as e:
            logger.error(f"error searching similar chunks: {str(e)}")
            return []

    def _save_index(self, business_id: int):
        """save faiss index and metadata to disk"""
        index_path = os.path.join(self.vector_db_path, f"business_{business_id}.index")
        metadata_path = os.path.join(
            self.vector_db_path, f"business_{business_id}_metadata.json"
        )

        faiss.write_index(self.index, index_path)
        with open(metadata_path, "w") as f:
            json.dump(self.metadata, f)

    def delete_document_chunks(self, business_id: int, document_id: int):
        """remove document chunks from vector index"""
        try:
            self.create_index(business_id)

            # find indices to remove
            indices_to_remove = []
            for idx, metadata in self.metadata.items():
                if metadata["document_id"] == document_id:
                    indices_to_remove.append(idx)

            # remove from metadata
            for idx in indices_to_remove:
                del self.metadata[idx]

            # rebuild index without removed chunks
            if indices_to_remove:
                self._rebuild_index(business_id)

            logger.info(
                f"removed {len(indices_to_remove)} chunks from vector index for document {document_id}"
            )

        except Exception as e:
            logger.error(f"error removing document chunks from vector index: {str(e)}")

    def _rebuild_index(self, business_id: int):
        """rebuild faiss index after removing chunks"""
        # this is a simplified rebuild - in production you might want a more efficient approach
        chunks = VectorChunk.objects.filter(document__business_id=business_id)

        self.index = faiss.IndexFlatL2(self.dimension)
        self.metadata = {}

        embeddings = []
        for i, chunk in enumerate(chunks):
            embedding = np.array(chunk.embedding, dtype=np.float32)
            embeddings.append(embedding)

            self.metadata[i] = {
                "document_id": chunk.document.id,
                "chunk_index": chunk.chunk_index,
                "content": chunk.content,
                "document_title": chunk.document.title,
            }

        if embeddings:
            embeddings_array = np.array(embeddings)
            self.index.add(embeddings_array)

        self._save_index(business_id)

    def get_context_from_chunks(self, chunks: List[Dict[str, Any]]) -> str:
        """combine chunks into context for ai"""
        context_parts = []
        for chunk in chunks:
            context_parts.append(f"from {chunk['document_title']}:\n{chunk['content']}")

        return "\n\n".join(context_parts)
