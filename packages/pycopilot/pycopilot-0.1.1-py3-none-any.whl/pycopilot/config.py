import platformdirs

DEVICE_CODE_LOGIN_URL = "https://github.com/login/device/code"
DEVICE_CODE_TOKEN_CHECK_URL = "https://github.com/login/oauth/access_token"
GH_AUTH_TOKEN_URL = "https://api.github.com/user"
GH_COPILOT_INTERNAL_AUTH_URL = "https://api.github.com/copilot_internal/v2/token"
GITHUB_COPILOT_CHAT_COMPLETIONS_URL = "https://api.githubcopilot.com/chat/completions"

CLIENT_ID = "Iv1.b507a08c87ecfe98"
CONFIG_DIR = platformdirs.user_data_path("com.kdheepak.pycopilot")
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
RUNTIME_DIR = platformdirs.user_runtime_path("com.kdheepak.pycopilot")
RUNTIME_DIR.mkdir(parents=True, exist_ok=True)

BASE_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "editor-version": "Neovim/0.9.2",
    "editor-plugin-version": "copilot.lua/1.11.4",
    "User-Agent": "GithubCopilot/1.133.0",
}

COPILOT_CHAT_HEADERS = {
    "copilot-integration-id": "vscode-chat",
    "openai-organization": "github-copilot",
    "openai-intent": "conversation-panel",
    "editor-version": "vscode/1.85.1",
    "editor-plugin-version": "copilot-chat/0.12.2023120701",
    "accept": "*/*",
}
