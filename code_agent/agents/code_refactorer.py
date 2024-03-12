import sys
from typing import List
from pathlib import Path
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain_openai import ChatOpenAI, OpenAI
from rich.console import Console, Group
from rich.syntax import Syntax
from rich.theme import Theme
from rich.panel import Panel
from rich.text import Text

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
        # TODO: OutputParserExceptionのハンドリング
        result: CodeSuggestions = chain.invoke({
            "language": settings['code_refactorer'].language, 
            "format_instruction": parser.get_format_instructions(),
            "code_chunks": code_chunks
        
        })

        # show result
        def align(code_snippet: str, width: int) -> str:
            """
            引数で受け取った文字列型のコードスニペットを全ての行でwidthの数だけ空白でインデントした文字列を返す関数
            """
            lines = code_snippet.splitlines()
            indented_lines = [ " "*width + f"{line}\n" for line in lines]
            return "".join(indented_lines)
        
        # # richライブラリを使った出力
        theme = "monokai"
        console = Console()


        rich_objects = []  # 空のリストとして初期化

        for suggestion in result.suggestions:
            lexer = Syntax.guess_lexer(path=suggestion.relevant_file)
            
            # スタイルをTextオブジェクトの引数として直接指定
            rich_objects.append(Text(f"{suggestion.suggestion_description}", style="bold yellow"))
            rich_objects.append(Text("   in ", end=""))
            rich_objects.append(Text(f"{suggestion.relevant_file}", style="green"))

            # From
            rich_objects.append(Text("From:", style="bold"))
            syntax = Syntax(suggestion.relevant_code, lexer, theme=theme, line_numbers=True, start_line=suggestion.relevant_line_start)
            rich_objects.append(syntax)
            
            improved_code = align(suggestion.improved_code, len(str(suggestion.relevant_line_start))+3)
            # Into
            rich_objects.append(Text("Into:", style="bold"))
            syntax = Syntax(improved_code, lexer, theme=theme, line_numbers=False)
            rich_objects.append(syntax)

            rich_objects.append(Text("\n"))

        console.print(Panel(Group(*rich_objects), title="🧐 Code Suggestions:", border_style="white"))
