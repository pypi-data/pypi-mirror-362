import llm
from llm.default_plugins.openai_models import Chat
from llm.utils import remove_dict_none_values
from pathlib import Path
import json
import time
import httpx

def get_moonshot_models():
    return fetch_cached_json(
        url="https://api.moonshot.ai/v1/models",
        path=llm.user_dir() / "moonshot_models.json",
        cache_timeout=3600,
    ).get("data", [])

class MoonshotChat(Chat):
    needs_key = "moonshot"
    key_env_var = "MOONSHOT_KEY"

    def __str__(self):
        return f"Moonshot: {self.model_id}"

    def execute(self, prompt, stream, response, conversation=None, key=None):
        client = self.get_client(key=key)
        messages = self.build_messages(prompt, conversation)
        kwargs = remove_dict_none_values(prompt.options.dict())

        if stream:
            completion_stream = client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                stream=True,
                **kwargs,
            )
            for chunk in completion_stream:
                content = chunk.choices[0].delta.content
                if content is not None:
                    yield content
        else:
            completion = client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                stream=True,
                **kwargs,
            )
            response.response_json = completion.model_dump()
            if completion.usage:
                self.set_usage(response, completion.usage.model_dump())
            content = completion.choices[0].message.content
            yield content

@llm.hookimpl
def register_models(register):
    key = llm.get_key("", "moonshot", "MOONSHOT_KEY")
    if not key:
        return

    models = get_moonshot_models()
    for model_def in models:
        register(
            MoonshotChat(
                model_id=f"moonshot/{model_def['id']}",
                model_name=model_def["id"],
                api_base="https://api.moonshot.ai/v1/",
            )
        )

def fetch_cached_json(url, path, cache_timeout):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.is_file() and (time.time() - path.stat().st_mtime) < cache_timeout:
        with open(path, "r") as f:
            return json.load(f)

    key = llm.get_key("", "moonshot", "MOONSHOT_KEY")
    if not key:
        return {"data": []}

    headers = {"Authorization": f"Bearer {key}"}

    try:
        response = httpx.get(url, headers=headers, follow_redirects=True)
        response.raise_for_status()
        data = response.json()
        with open(path, "w") as f:
            json.dump(data, f)
        return data
    except httpx.HTTPError:
        if path.is_file():
            with open(path, "r") as f:
                return json.load(f)
        raise
