from os.path import join
from dynaconf import Dynaconf
from code_agent.definitions import ROOT_DIR

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=[join(ROOT_DIR, f) for f in [
        'code_agent/settings/commit_maker_config.toml',
        'code_agent/settings/code_refactorer_config.toml',

    ]]
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.

def load_config(config_path: str)-> Dynaconf:
    """
    This function returns Dynaconf settings from config_path    
    """
    settings = Dynaconf(
        envvar_prefix="DYNACONF",
        settings_files=[
            config_path
        ]
    )
    return settings
