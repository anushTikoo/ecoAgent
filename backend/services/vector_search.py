# services/vector_search.py
from database import get_conn
from typing import List, Dict, Any

async def semantic_search(
    session_id: str,
    current_sector: str,
    query_embedding: List[float],
    limit: int = 5
) -> List[Dict[str, Any]]:
    """
    Returns top-N most similar vector_memory rows using cosine similarity.
    Excludes the current sector.
    """
    connection = await get_conn()
    rows = await connection.fetch("""
        SELECT content, sector
        FROM vector_memory
        WHERE session_id = $1
          AND sector != $2
        ORDER BY embedding <=> $3
        LIMIT $4
    """, session_id, current_sector, query_embedding, limit)

    return [
        {
            "content": r["content"],
            "sector": r["sector"]
        }
        for r in rows
    ]