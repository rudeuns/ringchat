from datetime import datetime
from datetime import timedelta

from langchain.embeddings import HuggingFaceEmbeddings
import numpy as np
from sqlalchemy import not_
from sqlalchemy.orm import Session as Session_

from app.database import Session
from app.models.tables import Links
from app.models.tables import Vectors

now_utc = datetime.now()
kst_offset = timedelta(hours=9)
now_kst = now_utc + kst_offset

# HuggingFace 임베딩 모델 초기화
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def get_links_not_in_vectors(session):
    subquery = session.query(Vectors.link_id).subquery()
    links = (
        session.query(Links.link_id, Links.link_document)
        .filter(not_(Links.link_id.in_(subquery)))
        .all()
    )
    return links


def create_and_save_embedding(
    session: Session_, link_id: int, document: str, time
):
    # summary = document_summary(document)
    total_vector = embeddings.embed_query(document)
    total_vector = np.array(total_vector).tolist()

    summary_vector = embeddings.embed_query(document)
    summary_vector = np.array(summary_vector).tolist()

    vector = Vectors(
        summary_vector=summary_vector,
        total_vector=total_vector,
        link_id=link_id,
        created_time=time,
    )
    session.add(vector)
    session.commit()


def batch_insert_vector():
    with Session() as session:
        for link in get_links_not_in_vectors(session):
            try:
                # 문서를 임베딩하고 Vectors 테이블에 저장
                create_and_save_embedding(
                    session, link.link_id, link.link_document, now_kst
                )
                print(f"Vector created and saved for link_id: {link.link_id}")
            except Exception as e:
                print(f"Failed to process link_id {link.link_id}: {e}")


def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
