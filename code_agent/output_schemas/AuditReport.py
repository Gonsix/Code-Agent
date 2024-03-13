from enum import Enum
from typing import List
from langchain_core.pydantic_v1 import BaseModel, Field

from rich.console import Console
from rich.syntax import Syntax


class CodeSuggestion(BaseModel):
    relevant_file: str = Field(description="a relevant file you want to subject")
    relevant_code: str = Field(description="a relevant code block that the user is going to improve, including original comments and empty lines")
    relevant_line_start: int = Field(description="the line number that the relevant code block start")
    improved_code: str = Field(description="an improved code block, should be valid code, based on what you propose.")
    description: str = Field(description="an informative and actionable description of your proposal, How user should modify code?")

class BugType(str, Enum):
    memory_bug = "Memory Bug"
    logic_bug = "Logic Bug"
    syntax_bug = "Syntax Bug"
    exception_handling_bug = "Improper exception handling Bug"
    race_condition_bug = "Race Condition Bug"
    io_bug = "I/O Bug"
    resource_leak_bug = "Resource leak Bug"
    other = "Other Bug"

class Bug(BaseModel):
    title: str = Field(description="a short concise title of the bug that you found.")
    type: BugType = Field(description="Type of the bug")
    suggestion: CodeSuggestion

class AuditReport(BaseModel):
    bugs: List[Bug]
    summary: str = Field(description="comprehensive and informative summary of bugs you found in the code chunks")


def displayAuditReport(report: AuditReport)->None:

    console = Console()

    def align(code_snippet: str, width: int) -> str:
        """
        引数で受け取った文字列型のコードスニペットを全ての行でwidthの数だけ空白でインデントした文字列を返す
        """
        lines = code_snippet.splitlines()
        indented_lines = [ " "*width + f"{line}\n" for line in lines]
        return "".join(indented_lines)
    
    for item in report.bugs:
        console.print(f"[bold magenta]Title:[/] {item.title}", justify="left")
        console.print(f"[bold magenta]Type:[/] {item.type.value}", justify="left")
        

        lexer = Syntax.guess_lexer(path=item.suggestion.relevant_file)
        console.print(f"[bold magenta]Suggestion:[/] {item.suggestion.description}", justify="left")
        console.print(f"  in [green][/] {item.suggestion.relevant_file}", justify="left")
        console.print("[bold magenta]From:[/]", justify="left")
        syntax = Syntax(item.suggestion.relevant_code, lexer=lexer, theme="monokai", line_numbers=True, start_line=item.suggestion.relevant_line_start)
        console.print(syntax)
        console.print("[bold magenta]Into:[/]", justify="left")
        improved_code = align(item.suggestion.improved_code, len(str(item.suggestion.relevant_line_start))+3)
        syntax_improved = Syntax(improved_code, lexer=lexer, theme="monokai", line_numbers=False)
        console.print(syntax_improved)

        console.print("")  

    console.print(f"[bold green]Summary[/]")
    console.print(f"[yellow]{report.summary}[/]")

