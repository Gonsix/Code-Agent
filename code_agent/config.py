from os.path import abspath, dirname, join
from dynaconf import Dynaconf

current_dir = dirname(abspath(__file__))
# 末尾の "/code_agent"を削除. これで設定ファイルへの正しいパスになる
def remove_trailing_path(original_path: str, trailing_path: str = "/code_agent") -> str:
    if original_path.endswith(trailing_path):
        # 末尾のパターンを削除
        return original_path[:-len(trailing_path)]
    else:
        # 末尾のパターンが見つからなければ、元の文字列をそのまま返す
        return original_path

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=[join(remove_trailing_path(current_dir), f) for f in [
        'code_agent/settings/commit_maker_config.toml',
    ]]
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
