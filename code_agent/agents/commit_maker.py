import sys
import os

from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from code_agent.utils.git import get_diff_head_index, git_commit

from code_agent.config import settings
from code_agent.output_schemas import CommitMessage


def gen_commit_msg(repo:str = "."):

    patch = get_diff_head_index(repo_path=repo)
    if patch is None:
        print("codex commit Error: Nothing to commit.")
        os._exit(2)


    llm = ChatOpenAI(model="gpt-4-1106-preview", temperature=0.0)
    # 設定ファイルからシステムテンプレートとユーザーテンプレートを読み出してプロンプトを定義
    prompt = ChatPromptTemplate.from_messages(messages=[
        ("system", settings.SYSTEM_TEMPLATE),
        ("user", settings.USER_TEMPLATE)
    ])
    # CommitMessageオブジェクトを渡してパーサーを作成
    parser = PydanticOutputParser(pydantic_object=CommitMessage) # 

    # チェインの定義
    chain = prompt | llm | parser

    # 実際にここでOpenAI API が呼ばれる
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

    try:
        answer = input('Do you want to commit using this message?(y/n) > ').strip().lower()

        if answer == 'y':
            git_commit(repo_path=repo, commit_message=commit_message)
            print("✅ Successfully committed.")
        elif answer == 'n':
            print("Okay, finishing program.")
            os._exit(0)
        else:
            raise ValueError("Invalid input")
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by the user.")
        sys.exit(1)

if __name__ == '__main__':
    gen_commit_msg(".")
