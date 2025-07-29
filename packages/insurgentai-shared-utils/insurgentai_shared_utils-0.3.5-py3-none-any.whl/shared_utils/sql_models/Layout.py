from uuid import UUID
from sqlmodel import SQLModel, Field
from sqlalchemy.dialects.postgresql import JSONB

class Layout(SQLModel, table=True):
    """Represents a layout for a graph, storing the positions of nodes in a 2D space."""
    __tablename__ = "layouts"
    layout_name: str = Field(primary_key=True, index=True, description="The unique name for the layout.")
    graph_name: str = Field(primary_key=True, description="The Apache AGE graph name this layout belongs to.")
    positions: dict[int, tuple[float, float]] = Field(sa_type=JSONB)