import requests
from pydantic import BaseModel
from pydantic.dataclasses import dataclass
import dataclasses
import json
import enum
from collections import deque
import uuid
import time

from .auth import Authentication, BASE_HEADERS
from .config import COPILOT_CHAT_HEADERS, GITHUB_COPILOT_CHAT_COMPLETIONS_URL


class Role(str, enum.Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Message(BaseModel):
    content: str
    role: Role


@dataclass
class Copilot:
    chat_history: list[Message] = dataclasses.field(default_factory=lambda: [])
    responses: list[dict] = dataclasses.field(default_factory=lambda: [])
    system_prompt: str = ""

    def __post_init__(self):
        self._auth = Authentication()
        self.authenticate()
        self.vscode_sid = self.generate_vscode_session_id()
        self.device_id = uuid.uuid4().hex[0:6]
        self._models = {}

    @staticmethod
    def generate_vscode_session_id() -> str:
        """Generate a VSCode session ID by combining a UUID4 with current timestamp in milliseconds."""
        return f"{uuid.uuid4()}{int(time.time() * 1000)}"

    def authenticate(self):
        self.auth = self._auth.try_auth()
        self.token = self.auth.token

    @property
    def models(self):
        if self._models:
            # return cached models without having to make a request again
            return self._models

        response = requests.get(
            "https://api.githubcopilot.com/models",
            headers=BASE_HEADERS
            | COPILOT_CHAT_HEADERS
            | {
                "Authorization": f"Bearer {self.auth.copilot_auth.token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )
        response.raise_for_status()

        models_data = response.json()
        data = [
            model
            for model in models_data["data"]
            if model.get("capabilities", {}).get("type") == "chat"
        ]
        self._models = data
        return self._models

    def _generate_messages(self) -> list[dict]:
        return [
            Message(
                role=Role.SYSTEM, content="The output must always be in raw Markdown."
            ).model_dump(mode="json"),
            Message(role=Role.SYSTEM, content=self.system_prompt).model_dump(
                mode="json"
            ),
        ] + [m.model_dump(mode="json") for m in self.chat_history]

    def reset(self):
        self.chat_history = []
        self.responses = []

    def feed(self, prompt: str):
        self.chat_history.append(Message(role=Role.USER, content=prompt))

    def ask(
        self,
        prompt,
        model="gpt-4-o-preview",
        n=1,
        temperature=0.1,
        top_p=1,
        intent=True,
    ) -> Message:
        deque(self.generate_ask(prompt, model, n, temperature, top_p, intent), maxlen=0)
        return self.chat_history[-1]

    def generate_ask(
        self,
        prompt,
        model="gpt-4o",
        n=1,
        temperature=0.1,
        top_p=1,
        top_k=10,
        n_predict=-1,
        min_p=0.5,
        intent=True,
        cache_prompt=True,
    ):
        self.chat_history.append(Message(role=Role.USER, content=prompt))

        response = requests.post(
            GITHUB_COPILOT_CHAT_COMPLETIONS_URL,
            headers=BASE_HEADERS
            | COPILOT_CHAT_HEADERS
            | {
                "vscode-sessionid": self.vscode_sid,
                "machineid": self.device_id,
                "Authorization": f"Bearer {self.auth.copilot_auth.token}",
            },
            json={
                "messages": self._generate_messages(),
                "model": model,
                "n": n,
                "temperature": temperature,
                "top_p": top_p,
                "intent": intent,
                "cache_prompt": cache_prompt,
                "top_k": top_k,
                "n_predict": n_predict,
                "min_p": min_p,
                "stream": True,
            },
            stream=True,
        )

        full_response = ""
        for line in response.iter_lines():
            line = line.replace(b"data: ", b"")
            if line.startswith(b"[DONE]"):
                break
            elif line == b"":
                continue
            try:
                line = json.loads(line)
                if "choices" not in line:
                    print("Error:", line)
                    raise Exception(f"No choices on {line}")
                if len(line["choices"]) == 0:
                    continue
                if "delta" in line["choices"][0]:
                    content = line["choices"][0]["delta"]["content"]
                else:
                    # model doesn't support streaming
                    content = line["choices"][0]["message"]["content"]
                if content is None:
                    continue
                full_response += content
                yield content
            except json.decoder.JSONDecodeError:
                print("Error:", line)
                continue

        self.chat_history.append(Message(role=Role.ASSISTANT, content=full_response))
        return self.chat_history[-1]


if __name__ == "__main__":
    print("Starting Copilot...")

    from pycopilot.copilot import Copilot

    copilot = Copilot()
    print(copilot.ask("Print out a flask hello world program", model="o1").content)
