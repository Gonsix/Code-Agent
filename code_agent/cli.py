import sys
import os
from typing import List
from pathlib import Path
import typer
from typing_extensions import Annotated

from code_agent.definitions import ROOT_DIR
from code_agent import gen_commit_msg
from code_agent import CodeRefactorAgent, CodeAuditAgent

app = typer.Typer()



@app.command(
    help="Generate a commit message from Git diff between HEAD and index.",
    
    )
def gen_commit(
    repo: Annotated[str, typer.Option("--repo", "-r")] = ".", 
    show_config_path: Annotated[bool, typer.Option(help="Show config path of this agent in your system")] = False ,
):
    if show_config_path is True:
        print(os.path.join(ROOT_DIR, "code_agent/settings/commit_maker_config.toml"))
        sys.exit(0)

    print(f"Creating commit message... repo_path='{repo}'")
    gen_commit_msg(repo=repo)


@app.command(
    help="[Unimplemented feature]: Generate Awesome README for your project in interactive way -> codex gen_readme --help"
)
def gen_readme():
    print("")

@app.command(
    help="[Unimplemented feature]: Suggest comment for source code in specified files -> codex suggest_comment --help"
)
def suggest_comment(
    files: Annotated[List[Path], typer.Argument(help="files to input into agent")]
    ):
    print(f"Received args: files={files}")


@app.command(
    help="Suggest code to help you Refactor source code in specified files -> codex refactor --help"
)
def refactor( 
    files: Annotated[List[Path], typer.Argument(help="files to input into agent")] = None,
    show_config_path: Annotated[bool, typer.Option(help="Show config path of this agent in your system")] = False ,
    ):

    if show_config_path is True:
        print(os.path.join(ROOT_DIR, "code_agent/settings/code_refactorer_config.toml"))
        sys.exit(0)

    if files is None or len(files) == 0 or files == []: 
        print("Code Refactor Agent:  Missing argument 'FILES...'.   ")
        print("See help: codex refactor --help")
        sys.exit(3)
    # Execute the agent
    CodeRefactorAgent(files).run()

@app.command(
    help="Audit code and Suggest improvement to help you fix source code in specified files -> codex audit --help"
)
def audit( 
    files: Annotated[List[Path], typer.Argument(help="files to input into agent")] = None,
    show_config_path: Annotated[bool, typer.Option(help="Show config path of this agent in your system")] = False ,
    ):

    if show_config_path is True:
        print(os.path.join(ROOT_DIR, "code_agent/settings/code_audit_config.toml"))
        sys.exit(0)

    if files is None or len(files) == 0 or files == []: 
        print("Code Refactor Agent:  Missing argument 'FILES...'.   ")
        print("See help: codex refactor --help")
        sys.exit(3)
    # Execute the agent
    CodeAuditAgent(files).run()

@app.command(
    help="[Unimplemented feature]: Describe the source code in files -> codex describe --help"
)
def describe(files: Annotated[List[Path], typer.Argument(help="files to input into agent")]):
    print(f"Received args: files={files}")



def main():
    app()
    
if __name__ == '__main__':
    main()
