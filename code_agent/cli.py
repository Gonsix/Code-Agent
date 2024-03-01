import typer
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
def commit(repo: str = "."):
    print(f"Creating commit... repo_path='{repo}'")
    gen_commit_msg(repo=repo)

def main():
    app()
    
if __name__ == '__main__':
    main()
