from typing import List
from langchain_core.pydantic_v1 import BaseModel, Field


# OutputのSchemaを定義
class FeatureChange(BaseModel):
    title: str = Field(description="A feature added, removed, or changed")
    description: str = Field(description="more detailed and informative description about the feature change.")
    relevant_files: List[str] = Field(description="a list of relevant files related to what you are describing.")
class CommitMessage(BaseModel):
    title: str = Field(description="What is the main purpose of this commit?(72 characters)")
    changes: List[FeatureChange] = Field(max_items=6, description="a list of feature changes in this commit")

