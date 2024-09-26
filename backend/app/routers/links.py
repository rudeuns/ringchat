from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db, create_db_session
from app.schemas import (
    LinkParse,
    LinkCreate,
    LinkListResponse,
    LinkIdListResponse,
)
import app.db.crud as crud
from app.utils.embedding import generate_embedding
from app.utils.parser import parse_single_url
from app.tasks.link_task import summarize_and_embed_link
import asyncio

router = APIRouter(tags=["links"])


@router.get("/links", response_model=LinkListResponse)
async def get_links(
    query: str = Query(),
    db: AsyncSession = Depends(get_db),
):
    try:
        query_vector = generate_embedding(text=query, model_type="openai")

        links = await crud.get_links_by_query(db=db, query_vector=query_vector)

        return LinkListResponse(links=links)

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Unexpected error occurred while fetching links.",
            headers={"X-Error": "SERVER_ERROR"},
        ) from e


@router.post("/links", response_model=LinkIdListResponse)
async def create_links(
    link_data: LinkParse,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    try:
        urls = [url for url in link_data.urls if url.strip()]

        existing_links = await crud.get_existing_links_by_url(db=db, urls=urls)
        existing_urls = [link.url for link in existing_links]
        existing_link_ids = [link.id for link in existing_links]

        new_link_ids = []
        new_urls = [url for url in urls if url not in existing_urls]
        if new_urls:
            new_links = await asyncio.gather(
                *(parse_and_create_link(url=url) for url in new_urls)
            )
            new_link_ids = [link.id for link in new_links]

            for link_id in new_link_ids:
                background_tasks.add_task(summarize_and_embed_link, link_id)

        return LinkIdListResponse(link_ids=existing_link_ids + new_link_ids)

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Unexpected error occurred while parsing and creating link.",
            headers={"X-Error": "SERVER_ERROR"},
        ) from e


async def parse_and_create_link(url: str):
    documents = parse_single_url(url)

    if not documents or len(documents) == 0:
        raise HTTPException(
            status_code=404,
            detail=f"No content could be extracted from the URL: {url}",
            headers={"X-Error": "PARSING_ERROR"},
        )

    document = documents[0]
    title = document.metadata.get("title", "No Title")
    content = document.page_content

    db = await create_db_session()

    new_link = await crud.create_link(
        db=db, link_data=LinkCreate(url=url, title=title, content=content)
    )

    await db.close()

    return new_link
