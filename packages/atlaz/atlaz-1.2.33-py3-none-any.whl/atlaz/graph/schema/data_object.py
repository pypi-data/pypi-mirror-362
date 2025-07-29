from typing import List, Optional
from pydantic import BaseModel, Field

class Entity(BaseModel):

    ID: int = Field(..., description="Unique identifier of the entity.")
    Name: str = Field(..., description="Human-readable name of the entity.")
    Definition: Optional[str] = Field(None, description="Definition or description of the entity.")

class RelationshipEntity(BaseModel):

    ID: int = Field(..., description="Unique identifier of the relationship entity.")
    Name: str = Field(..., description="Human-readable name of the relationship entity.")
    Definition: Optional[str] = Field(None, description="Definition or description of the relationship entity.")
    SourceNodeTypeID: int = Field(..., description="ID of the abstract type the source entity can have.")
    TargetNodeTypeID: int = Field(..., description="ID of the abstract type the target entity can have.")
    Transitive: bool = Field(..., description="True if the relationship is transitive (A->B and B->C imply A->C).")
    Bidirectional: bool = Field(..., description="True if the relationship is bidirectional (A->B implies B->A).")

class Relationship(BaseModel):

    ID: int = Field(..., description="Unique identifier for this specific relationship instance.")
    SourceNodeID: int = Field(..., description="ID of the source node in the relationship.")
    TargetNodeID: int = Field(..., description="ID of the target node in the relationship.")
    EntityID: int = Field(..., description="Which RelationshipEntity is used (e.g., 'Is A Type Of').")
    Motivation: Optional[str] = Field(None, description="Reason or motivation for why this relationship holds.")

class GraphObject(BaseModel):

    Entities: List[Entity] = Field(
        ..., description="List of domain Entities in the graph."
    )
    RelationshipEntities: List[RelationshipEntity] = Field(
        ..., description="List of special RelationshipEntities (like 'Is A Type Of')."
    )
    Relationships: List[Relationship] = Field(
        ..., description="List of actual relationships linking source and target nodes."
    )