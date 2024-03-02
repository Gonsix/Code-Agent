from typing import List
from pathlib import Path
import typer
from typing_extensions import Annotated

from code_agent import gen_commit_msg

app = typer.Typer()

@app.command()
def say_hello():
    print("hello")

@app.command()
def say_goodbye():
    print("goodbyte")

@app.command(
    help="Generate a commit message from Git diff between HEAD and index.",
    
    )
def gen_commit(repo: Annotated[str, typer.Option("--repo", "-r")] = "."): #repo: str = "."
    print(f"Creating commit message... repo_path='{repo}'")
    gen_commit_msg()


@app.command(
    help="[Unimplemented feature]: Generate Awesome README for your project in interactive way -> codex gen_readme --help"
)
def gen_readme():
    print("")

@app.command(
    help="[Unimplemented feature]: Suggest comment for source code in specified files -> codex suggest_comment --help"
)
def suggest_comment(files: Annotated[List[Path], typer.Argument(help="files to input into agent")]):
    print(f"Received args: files={files}")

@app.command(
    help="[Unimplemented feature]: Refactor and Suggest code for source code in specified files -> codex suggest_code --help"
)
def suggest_code(files: Annotated[List[Path], typer.Argument(help="files to input into agent")]):
    print()



@app.command(
    help="[Unimplemented feature]: Describe the source code in files -> codex describe --help"
)
def describe(files: Annotated[List[Path], typer.Argument(help="files to input into agent")]):
    print(f"Received args: files={files}")



def main():
    app()
    
if __name__ == '__main__':
    main()
