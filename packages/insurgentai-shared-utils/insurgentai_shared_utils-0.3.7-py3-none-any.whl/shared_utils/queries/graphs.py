from typing import Optional
from uuid import UUID
from sqlmodel import Session, select
from shared_utils.sql_models import ChunkGraph

def insert_graph(session: Session, graph: ChunkGraph) -> None:
    """
    Inserts a new graph into the database.

    Args:
        session (Session): The session to use for the insert operation.
        graph (Graph): The graph object to insert.

    Returns:
        None
    """
    session.add(graph)
    session.commit()

def get_graph(session: Session, graph_id: UUID) -> Optional[ChunkGraph]:
    """
    Retrieves a graph by its ID.

    Args:
        session (Session): The session to use for the query.
        graph_id (UUID): The ID of the graph to retrieve.

    Returns:
        Optional[Graph]: The graph data if found, otherwise None.
    """
    statement = select(ChunkGraph).where(ChunkGraph.graph_id == graph_id)
    result = session.exec(statement).first()
    return result if result else None

def get_graph_for_chunk(session: Session, chunk_id: UUID) -> Optional[ChunkGraph]:
    """
    Retrieves the graph associated with a specific chunk.

    Args:
        session (Session): The session to use for the query.
        chunk_id (UUID): The ID of the chunk.

    Returns:
        Optional[Graph]: The graph data if found, otherwise None.
    """
    statement = select(ChunkGraph).where(ChunkGraph.chunk_id == chunk_id)
    result = session.exec(statement).first()
    return result if result else None

def get_graphs_for_chunks(session: Session, chunk_ids: List[UUID]) -> List[ChunkGraph]:
    """
    Retrieves the graphs associated with specific chunks.

    Args:
        session (Session): The session to use for the query.
        chunk_ids (List[UUID]): The IDs of the chunks.

    Returns:
        List[Graph]: The list of graph data if found, otherwise an empty list.
    """
    statement = select(ChunkGraph).where(ChunkGraph.chunk_id.in_(chunk_ids))
    results = session.exec(statement).all()
    return results if results else []