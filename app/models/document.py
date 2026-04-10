from pydantic import BaseModel


class Document(BaseModel):
    id: str
    index_text: str
    metadata: dict


class SearchResult(BaseModel):
    id: str
    score: float
    name: str
    price: str
    thumbnail_url: str
    specification: str
    dosage_form: str
    country_of_manufacture: str
