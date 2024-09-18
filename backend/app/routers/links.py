from typing import List

from fastapi import APIRouter
from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.tables import Links
from app.models.tables import Vectors

router = APIRouter()


class Link(BaseModel):
    url: str
    link_title: str
    avgScore: float
    sumUsedNum: int
    sumBookmark: int


@router.get("/links", response_model=List[Link])
async def search_links(query: str, db: Session = Depends(get_db)):
    # query_vector = get_query_vector(query)

    vectors = db.query(Vectors).all()

    threshold = 0.5
    similarities = []

    for vector in vectors:
        similarities.append((vector.link_id, threshold))

    # for vector in vectors:
    #     summary_vector = np.array(vector.summary_vector)
    #     similarity = cosine_similarity(query_vector, summary_vector)
    #     if similarity > threshold:
    # similarities.append((vector.link_id, similarity))

    top_similarities = sorted(similarities, key=lambda x: x[1], reverse=True)[
        :10
    ]

    top_link_ids = [item[0] for item in top_similarities]
    top_links = db.query(Links).filter(Links.link_id.in_(top_link_ids)).all()

    response = [
        Link(
            url=link.url,
            link_title=link.link_title,
            avgScore=link.avg_score,
            sumUsedNum=link.sum_used_num,
            sumBookmark=link.sum_bookmark,
        )
        for link in top_links
    ]

    return response
