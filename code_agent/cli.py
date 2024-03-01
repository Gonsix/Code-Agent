from typing import List
import sys

from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

from commit_agent.git_utils import get_diff_head_index, git_commit


# OutputのSchemaを定義
class FeatureChange(BaseModel):
    title: str = Field(description="A feature added, removed, or changed")
    description: str = Field(description="more detailed and informative description about the feature change.")
    relevant_files: List[str] = Field(description="a list of relevant files related to what you are describing.")
class CommitMessage(BaseModel):
    title: str = Field(description="What is the main purpose of this commit?(72 characters)")
    changes: List[FeatureChange] = Field(max_items=6, description="a list of feature changes in this commit")



COMMIT_MAKER_TEMPLATE_SYSTEM = """You are Git Commit-Maker, a language model designed to generate a clear Commit message.
Your task is to create a commit message from given commit diff(changes), have not actually been committed but already indexed.

Follow these guidelines
- Focus on the new code (lines starting with '+')
- The generated title and description should prioritize the most significant changes.
- You are going to answer in well-designed Markdown 


Example Commit Diff:
======
## file: 'src/file1.py'

@@ -12,5 +12,5 @@ def func1():
code line 1 that remained unchanged in the commit
code line 2 that remained unchanged in the commit
-code line that was removed in the commit
+code line added in the commit
code line 3 that remained unchanged in the commit

@@ ... @@ def func2():
...


## file: 'src/file2.py'
...
======

About output format:
{format_instruction}

"""

COMMIT_MAKER_TEMPLATE_USER = """The Commit Diff: 
=====
{patch}
=====
"""



def main():

    patch = get_diff_head_index()

    llm = ChatOpenAI(model="gpt-4-1106-preview", temperature=0.0)

    prompt = ChatPromptTemplate.from_messages(messages=[
        ("system", COMMIT_MAKER_TEMPLATE_SYSTEM),
        ("user", COMMIT_MAKER_TEMPLATE_USER)
    ])

    parser = PydanticOutputParser(pydantic_object=CommitMessage)

    chain = prompt | llm | parser

    result: CommitMessage = chain.invoke({
        "format_instruction": parser.get_format_instructions(),
        "patch": patch
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
    
    # commit_message += "\n"

    print("# >>>>> commit message >>>>>\n")
    print(commit_message)
    print("# <<<<< commit message <<<<<")


    answer = input('Do you want to commit using this message?(y/n) > ')

    match answer:
        case "y":
            git_commit(repo_path="./", commit_message=commit_message)
            print("✅ Successfully committed.")
        case "n":
            print("Okay, finishing program.")
            sys.exit(0)
        case _:
            raise ValueError("Not a point")

if __name__ == '__main__':
    main()
