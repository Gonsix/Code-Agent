import sys

from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from code_agent.utils.git import get_diff_head_index, git_commit

from code_agent.config import settings
from code_agent.output_schemas import CommitMessage


def gen_commit_msg(repo:str = "."):

    patch = get_diff_head_index()
    if patch is None:
        print("codex commit Error: Nothing to commit.")
        sys.exit(2)

    llm = ChatOpenAI(model="gpt-4-1106-preview", temperature=0.0)

    prompt = ChatPromptTemplate.from_messages(messages=[
        ("system", settings.SYSTEM_TEMPLATE),
        ("user", settings.USER_TEMPLATE)
    ])


    parser = PydanticOutputParser(pydantic_object=CommitMessage) # 

    chain = prompt | llm | parser

    result: CommitMessage = chain.invoke({
        "format_instruction": parser.get_format_instructions(),
        "patch": patch,
        "language": settings.language
    })



    ## Make a complete commit message
    commit_message = ""
    commit_message += "🌟 " + result.title + "\n"
    commit_message += "\n"
    
    commit_message += f"Changes({len(result.changes)}):" + "\n"
    for change in result.changes:
        commit_message += f" 🚩 {change.title}" + "   @ "
        commit_message += ", ".join(change.relevant_files) + "\n"
        commit_message += f"     {change.description}" + "\n"
    

    print("# >>>>> commit message >>>>>\n")
    print(commit_message)
    print("# <<<<< commit message <<<<<")


    answer = input('Do you want to commit using this message?(y/n) > ')

    match answer:
        case "y":
            git_commit(repo_path=repo, commit_message=commit_message)
            print("✅ Successfully committed.")
        case "n":
            print("Okay, finishing program.")
            sys.exit(0)
        case _:
            raise ValueError("Not a point")

if __name__ == '__main__':
    gen_commit_msg(".")
