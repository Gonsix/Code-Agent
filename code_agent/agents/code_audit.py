import sys, os
from typing import List
from pathlib import Path
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser, RetryOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from rich.console import Console, Group
from rich.syntax import Syntax
from rich.theme import Theme
from rich.panel import Panel
from rich.text import Text

from code_agent.output_schemas import AuditReport, displayAuditReport
from code_agent.config import settings, load_config
from code_agent.definitions import ROOT_DIR
from code_agent.utils import get_file_contents

class CodeAuditAgent(object):
    def __init__(self, files: List[Path]) -> None:
        self.target_files = files

    def run(self):

        settings = load_config(os.path.join(ROOT_DIR, "code_agent/settings/code_audit_config.toml"))

        # Loading source code from multiple files.
        code_chunks = get_file_contents([str(path) for path in self.target_files])

        # TODO: settingファイルからOPENAI_API_KEYを読み込み
        llm = ChatOpenAI(model="gpt-4-1106-preview", temperature=0.0)

        prompt = ChatPromptTemplate.from_messages(messages=[
            ("system", settings.templates.SYSTEM_TEMPLATE),
            ("user", settings.templates.USER_TEMPLATE)
        ])

        pydantic_parser = PydanticOutputParser(pydantic_object=AuditReport)
        # This second parser calls out to another LLM to fix any errors when the first parser fails.
        parser = OutputFixingParser.from_llm(llm=ChatOpenAI(model="gpt-4-1106-preview", temperature=0.0), parser=pydantic_parser)

        chain = prompt | llm | parser

        # CodingStandardReview型のオブジェクトで受け取る
        # TODO: ユーザーが設定ファイルのテンプレートに変数を新しく追加したときに、このプログラムを触らなくてよくする
        result: AuditReport = chain.invoke({
            "language": settings.variables.language, 
            "extra_instruction": settings.variables.extra_instruction,
            "format_instruction": parser.get_format_instructions(),
            "code_chunks": code_chunks
        
        })
        displayAuditReport(result)
