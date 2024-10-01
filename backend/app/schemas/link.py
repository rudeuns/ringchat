from pydantic import BaseModel
from typing import List


class LinkParse(BaseModel):
    urls: List[str]


class LinkCreate(BaseModel):
    url: str
    title: str
    content: str


class LinkStat(BaseModel):
    average_rating: float
    attached_count: int
    favorite_count: int

    class Config:
        from_attributes = True


class LinkResponse(BaseModel):
    id: int
    url: str
    title: str
    content: str
    link_stat: LinkStat

    class Config:
        from_attributes = True


class LinkListResponse(BaseModel):
    links: List[LinkResponse]

    class Config:
        from_attributes = True


class LinkIdListResponse(BaseModel):
    link_ids: List[int]

    class Config:
        from_attributes = True


class LinkSummaryEmbeddingCreate(BaseModel):
    link_id: int
    summary_content: str
    summary_vector: List[float]
