from app.db.database import create_db_session
import app.db.crud as crud
from app.schemas import LinkSummaryEmbeddingCreate
from app.utils.langchain import summarize_content
from app.utils.embedding import generate_embedding


async def summarize_and_embed_link(link_id: int):
    try:
        db = await create_db_session()

        link = await crud.get_link_by_id(db=db, link_id=link_id)

        if link:
            summary = summarize_content(link.content)
            embedding_vector = generate_embedding(
                text=summary, model_type="openai"
            )

            await crud.create_link_summary_embedding(
                db=db,
                summary_embedding_data=LinkSummaryEmbeddingCreate(
                    link_id=link_id,
                    summary_content=summary,
                    summary_vector=embedding_vector,
                ),
            )

    except Exception as e:
        raise Exception(
            f"Unexpected error occurred in Celery task: {str(e)}"
        ) from e

    finally:
        await db.close()
