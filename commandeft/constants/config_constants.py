REQUIRED_KEYS: list[str] = ["model", "temperature", "max_tokens", "accept_command_behavior"]

TEMPERATURE = "temperature"
MAX_TOKENS = "max_tokens"
MODEL = "model"
API_KEY = "api_key"
ACCEPT_COMMAND_BEHAVIOR = "accept_command_behavior"
GPT_3_5_TURBO = "gpt-3.5-turbo"
GPT4 = "gpt4"


MODELS_LIST: list[str] = [GPT_3_5_TURBO, GPT4]
MODELS_MAX_TOKENS: dict[str, int] = {GPT_3_5_TURBO: 4096, GPT4: 2048}
COMMAND_BEHAVIOURS: list[str] = ["run", "copy"]


