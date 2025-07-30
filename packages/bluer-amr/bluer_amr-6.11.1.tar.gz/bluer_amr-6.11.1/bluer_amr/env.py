from bluer_options.env import load_config, load_env, get_env

load_config(__name__)


BLUER_AMR_CONFIG = get_env("BLUER_AMR_CONFIG")
