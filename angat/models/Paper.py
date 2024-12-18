from typing import Iterable, List, Optional
from django.db import models
import uuid
from pgvector.django import VectorField, HnswIndex
from langchain_community.embeddings import HuggingFaceEmbeddings

class Embedding_Function:
    embedding_func = HuggingFaceEmbeddings(
            model_name='sentence-transformers/all-MiniLM-L6-v2'
        )
    
    @classmethod
    def embed(cls, input: List[str]) -> List[List[float]]:
        return cls.embedding_func.embed_documents(input)

# Create your models here.
class Paper(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=1000, blank=False)
    authors = models.CharField(max_length=1000, blank=False)
    abstract = models.TextField(blank=False)
    link = models.URLField(max_length=100, null=True, blank=True)
    abstract_embeddings = VectorField(dimensions=384, null=False, blank=False, )

    class Meta:
        indexes = [
            HnswIndex(
                name="all_MiniLM_L6_v2_vector_index",
                fields=["abstract_embeddings"],
                m=16,
                ef_construction=64,
                opclasses=["vector_cosine_ops"],
            )
        ]

    def __str__(self) -> str:
        return f"""
            Title: {self.title}
            Authors: {self.authors}
        """

    def save(self, *args, **kwargs) -> None:
        self.abstract_embeddings = self.create_embeddings()
        super().save(*args, **kwargs)

    def create_embeddings(self) -> List[float]:
        return Embedding_Function.embed([self.abstract])[0]    
