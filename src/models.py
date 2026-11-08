
from pydantic import BaseModel, Field


class Characteristic(BaseModel):
    name: str
    value: str


class ProductCard(BaseModel):
    seo_title: str

    seo_description: str

    characteristics: list[Characteristic]

    search_queries: list[str] = Field(
        min_length=3,
        max_length=5
    )

    commercial_block: str

    missing_information: list[str]

    warnings: list[str]

    needs_more_data: bool
