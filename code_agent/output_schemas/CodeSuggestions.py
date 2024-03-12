from typing import List
from langchain_core.pydantic_v1 import BaseModel, Field


class FileCodeSuggestion(BaseModel):
    relevant_file: str = Field(description="a relevant file you want to subject")
    relevant_code: str = Field(description="a relevant code block that the user is going to improve, including original comments")
    relevant_line_start: int = Field(description="the line number that the relevant code block start")
    suggestion_description: str = Field(description="a concise and actionable description for your improvement suggestion")
    improved_code: str = Field(description="an improved code block, should be valid code, based on what you propose.")
# TODO: max_items も設定ファイルで設定できるようにする
class CodeSuggestions(BaseModel):
    suggestions: List[FileCodeSuggestion] = Field(description="a list of code suggestions, sorted in order of its importance.")
