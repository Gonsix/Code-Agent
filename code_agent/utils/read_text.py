import sys
def load_from_file(path: str) -> str:
    """ ファイルの内容を読み込み、行番号をつける """
    f = open(path, 'r', encoding='utf-8')
    lines = f.read()
    data = ""
    data += f"## file: '{path}'" + "\n\n" 
    for line_num, line in enumerate(lines.split("\n")):
        line = f'{line_num+1:>6}: {line}'
        data += line + "\n"
    f.close()
    return data

def load_from_files(files: list[str] ) -> str:
    """複数のファイルを読み込み、連結する"""
    data = ""
    for file in files:
        file_data = load_from_file(file)
        data += file_data
        data += "\n\n"

    return data

# external API
def get_file_contents(files: list[str])-> str:
    return load_from_files(files)




if __name__ == '__main__':
    files = sys.argv[1:]

    data = load_from_files(files)

    print(data)
