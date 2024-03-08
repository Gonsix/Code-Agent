import sys
from typing import List
from pathlib import Path
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain_openai import ChatOpenAI, OpenAI
from rich.console import Console
from rich.markdown import Markdown
from rich.syntax import Syntax

from code_agent.output_schemas import CodeSuggestions
from code_agent.config import settings
from code_agent.utils import get_file_contents

class CodeRefactorAgent(object):
    def __init__(self, files: List[Path]) -> None:
        self.target_files = files

    def run(self):

        code_chunks = get_file_contents([str(path) for path in self.target_files])


        # TODO: settingファイルからOPENAI_API_KEYを読み込み
        llm = ChatOpenAI(model="gpt-4-1106-preview", temperature=0.0)

        prompt = ChatPromptTemplate.from_messages(messages=[
            ("system", settings['code_refactorer'].SYSTEM_TEMPLATE),
            ("user", settings['code_refactorer'].USER_TEMPLATE)
        ])

        parser = PydanticOutputParser(pydantic_object=CodeSuggestions)

        chain = prompt | llm | parser

        result: CodeSuggestions = chain.invoke({
            "language": settings['code_refactorer'].language, 
            "format_instruction": parser.get_format_instructions(),
            "code_chunks": code_chunks
        
        })

        # show result

        # richライブラリを使った出力
        theme = "monokai"
        line_numbers = True
        console = Console()

        console.print("[bold magenta]🧐 Code Suggestions:[/bold magenta]")
        # FIXME: highlightされるコードの行が一行ズレている。Pythonコードではズレが発生しなかった。Rustではズレている

        for suggestion in result.suggestions:
            # ファイルに固有なのでlexer を毎回作成する
            lexer = Syntax.guess_lexer(path=suggestion.relevant_file)
            
            console.print(f"[bold yellow]- {suggestion.suggestion_description}[/bold yellow]")
            console.print(f"   in [green]{suggestion.relevant_file}[/green]")
            console.print("\n[bold]From:[/bold]")
            syntax = Syntax(suggestion.relevant_code, lexer, theme=theme, line_numbers=line_numbers, start_line=suggestion.relevant_line_start)
            console.print(syntax)
            console.print("[bold]Into:[/bold]")
            syntax = Syntax(suggestion.improved_code, lexer, theme=theme, line_numbers=line_numbers, start_line=suggestion.relevant_line_start)
            console.print(syntax)
            console.print("\n")


