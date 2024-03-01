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
def commit(repo: Annotated[str, typer.Option("--repo", "-r")] = "."): #repo: str = "."
    print(f"Creating commit message... repo_path='{repo}'")
    gen_commit_msg()

def main():
    app()
    
if __name__ == '__main__':
    main()
