import sys
from git import Repo, Diff

def get_diff_head_index(repo_path = '.')-> str:
    repo = Repo(repo_path)
    try:
        head = repo.head.commit
    except ValueError:
        print("codex commit Error: There is no commit to compare with. Please commit something first!")
        print("  (Hint) The gmm compares the index to the head commit.")
        sys.exit(2)
    except Exception as e:
        print(e)
        sys.exit(-1)

    # default   : compare against the Index
    # None      : compare against the working tree
    diff = head.diff(create_patch=True)
    patch_all = ""
    for d in diff:
        d: Diff = d
        patch = f"""## file: '{d.a_path if d.a_path else d.b_path}'

{d.diff.decode('utf-8')}


"""
        patch_all += patch

    return patch_all if patch_all != "" else None


# TODO: sinceからuntilまでのコミットのコミットメッセージを、LLMに渡すために取得する
def get_diff(since: str = None, until: str = None, repo_path='.')-> str:
    repo = Repo(repo_path)
    since_commit = repo.commit(since)
    until_commit = repo.commit(until)
    
    diff = since_commit.diff(until_commit, create_patch=True)
    patch_all = ""
    for d in diff:
        d: Diff = d
        patch = f"""## file: '{d.a_path if d.a_path else d.b_path}'

{d.diff.decode('utf-8')}


"""
        patch_all += patch
    return patch_all
    
# Python cannot overloads
def get_diff_one(commit_str: str, repo_path='.')->str:
    repo = Repo(repo_path)

    commit = repo.commit(commit_str)
    parent = commit.parents[0]

    diff = parent.diff(commit, create_patch=True)
    patch_all = ""
    for d in diff:
        d: Diff = d
        patch = f"""## file: '{d.a_path if d.a_path else d.b_path}'

{d.diff.decode('utf-8')}


"""
        patch_all += patch
    return patch_all



def git_commit(repo_path: str='./', commit_message: str=""):
    repo = Repo(repo_path)
    repo.index.commit(commit_message)


if __name__ == '__main__':
    # print('hello')
    ## Comment out if you want to see the result of get_diff_head_index
    # patch = get_diff_head_index(repo_path='../')

    # patch = get_diff(sys.argv[1], sys.argv[2], repo_path='../')
    # print(patch)

    # patch = get_diff(sys.argv[1], repo_path='../')
    patch = get_diff_head_index(repo_path=sys.argv[1])
    print(patch)
