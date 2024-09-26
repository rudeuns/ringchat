from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from typing import List
from app.db.models import Link, LinkSummaryEmbedding, LinkStat
from app.schemas import LinkCreate, LinkSummaryEmbeddingCreate


async def get_links_by_query(
    db: AsyncSession,
    query_vector: List[float],
    top_k: int = 10,
    threshold: float = 0.75,
) -> List[Link]:
    try:
        result = await db.execute(
            select(
                LinkSummaryEmbedding,
                (
                    1
                    - LinkSummaryEmbedding.summary_vector.cosine_distance(
                        query_vector
                    )
                ).label("similarity"),
            )
            .filter(
                (
                    1
                    - LinkSummaryEmbedding.summary_vector.cosine_distance(
                        query_vector
                    )
                )
                > threshold
            )
            .limit(top_k)
        )

        link_ids = []
        for row in result.fetchall():
            link_ids.append(row[0].link_id)
            print("similarity:", row[1])

        # link_ids = [row[0].link_id for row in result.fetchall()]
        if link_ids:
            link_result = await db.execute(
                select(Link)
                .join(LinkStat, Link.id == LinkStat.link_id)
                .options(selectinload(Link.link_stat))
                .filter(Link.id.in_(link_ids))
                .order_by(LinkStat.average_rating.desc())
            )

            links = link_result.scalars().all()
        else:
            links = []

        return links

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail="DB error occurred while reading link and performing similarity search.",
            headers={"X-Error": "DB_READ_ERROR"},
        ) from e


async def create_link(db: AsyncSession, link_data: LinkCreate) -> Link:
    try:
        new_link = Link(**link_data.model_dump())
        db.add(new_link)
        await db.flush()

        new_link_stat = LinkStat(link_id=new_link.id)
        db.add(new_link_stat)

        await db.commit()
        await db.refresh(new_link)

        return new_link

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="DB error occurred while writing link.",
            headers={"X-Error": "DB_WRITE_ERROR"},
        ) from e


async def get_existing_links_by_url(
    db: AsyncSession, urls: List[str]
) -> List[Link]:
    try:
        result = await db.execute(select(Link).filter(Link.url.in_(urls)))

        existing_links = result.scalars().all()
        return existing_links

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail="DB error occurred while reading link.",
            headers={"X-Error": "DB_READ_ERROR"},
        ) from e


async def get_link_by_id(db: AsyncSession, link_id: int) -> Link:
    try:
        result = await db.execute(select(Link).filter(Link.id == link_id))

        link = result.scalars().first()
        return link

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail="DB error occurred while reading link.",
            headers={"X-Error": "DB_READ_ERROR"},
        ) from e


async def create_link_summary_embedding(
    db: AsyncSession, summary_embedding_data: LinkSummaryEmbeddingCreate
) -> LinkSummaryEmbedding:
    try:
        new_summary_embedding = LinkSummaryEmbedding(
            **summary_embedding_data.model_dump()
        )
        db.add(new_summary_embedding)

        await db.commit()
        await db.refresh(new_summary_embedding)

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="DB error occurred while writing link_summary_embedding.",
            headers={"X-Error": "DB_WRITE_ERROR"},
        ) from e
