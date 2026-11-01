"""
AI-related models for HintAI V2.
Includes document embeddings and knowledge graph concepts.
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from backend_v2.app.core.database import Base
from pgvector.sqlalchemy import Vector
import numpy as np


class DocumentEmbedding(Base):
    """
    Document embeddings for RAG (Retrieval-Augmented Generation).
    """
    __tablename__ = "document_embeddings"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, nullable=False)  # Can reference exam_documents or learning_resources
    document_type = Column(String(20), nullable=False)  # exam, solution, resource, etc.
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    
    # Content
    content_text = Column(Text, nullable=False)  # Extracted text from the document
    
    # Embedding vector (1536 dimensions for Pixtral)
    embedding = Column(Vector(1536), nullable=False)
    
    # Metadata
    metadata = Column(JSON, default={})  # Additional metadata (e.g., page number, section)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="document_embeddings")
    
    def __repr__(self):
        return f"<DocumentEmbedding(id={self.id}, document_type={self.document_type})>"


class Concept(Base):
    """
    Concept in the knowledge graph.
    """
    __tablename__ = "concepts"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Concept metadata
    name = Column(String(255), nullable=False)
    description = Column(Text)
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    chapter_id = Column(Integer, ForeignKey("chapters.id"))
    
    # Knowledge graph
    difficulty_level = Column(Integer, default=3)  # 1-5
    importance = Column(Integer, default=5)  # 1-10
    
    # Status
    is_verified = Column(Boolean, default=False)
    verified_by = Column(Integer, ForeignKey("users.id"))
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    subject = relationship("Subject", back_populates="concepts")
    chapter = relationship("Chapter", back_populates="concepts")
    verified_by_user = relationship("User", foreign_keys=[verified_by])
    
    # Knowledge graph relationships
    related_from = relationship(
        "Concept",
        secondary="concept_relations",
        primaryjoin="Concept.id == concept_relations.c.from_concept_id",
        secondaryjoin="Concept.id == concept_relations.c.to_concept_id",
        back_populates="related_to"
    )
    related_to = relationship(
        "Concept",
        secondary="concept_relations",
        primaryjoin="Concept.id == concept_relations.c.to_concept_id",
        secondaryjoin="Concept.id == concept_relations.c.from_concept_id",
        back_populates="related_from"
    )
    
    def __repr__(self):
        return f"<Concept(id={self.id}, name={self.name})>"


# Many-to-many relationship between concepts
concept_relations = Table(
    "concept_relations",
    Base.metadata,
    Column("from_concept_id", Integer, ForeignKey("concepts.id", ondelete="CASCADE"), primary_key=True),
    Column("to_concept_id", Integer, ForeignKey("concepts.id", ondelete="CASCADE"), primary_key=True),
    Column("relation_type", String(50), nullable=False),  # requires, related_to, part_of, etc.
    Column("weight", Integer, default=1),  # Strength of the relationship (0-100)
    Column("created_at", DateTime, server_default=func.now()),
)
