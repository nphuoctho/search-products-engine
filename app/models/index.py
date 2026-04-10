from pydantic import BaseModel


class IndexResponse(BaseModel):
    indexed_docs: int
    snapshot: str
