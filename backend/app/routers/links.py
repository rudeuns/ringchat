from typing import List

from fastapi import APIRouter
from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.tables import Links
from app.models.tables import Vectors
from app.utils.vector_operations import cosine_similarity
from app.utils.vector_operations import embeddings

router = APIRouter()


class Link(BaseModel):
    url: str
    avgScore: float
    sumUsedNum: int
    sumBookmark: int


@router.get("/links", response_model=List[Link])
async def search_links(query: str, db: Session = Depends(get_db)):
    query_vector = embeddings.embed_query(query)
    vectors = db.query(Vectors).all()

    threshold = 0.3
    similarities = []

    for vector in vectors:
        similarity = cosine_similarity(query_vector, vector.summary_vector)
        if similarity > threshold:
            similarities.append((vector.link_id, similarity))

    top_similarities = sorted(similarities, key=lambda x: x[1], reverse=True)[
        :10
    ]

    top_link_ids = [item[0] for item in top_similarities]
    top_links = db.query(Links).filter(Links.link_id.in_(top_link_ids)).all()

    response = [
        Link(
            url=link.url,
            avgScore=link.avg_score,
            sumUsedNum=link.sum_used_num,
            sumBookmark=link.sum_bookmark,
        )
        for link in top_links
    ]

    return response
