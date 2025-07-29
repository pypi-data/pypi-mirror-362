import os
import httpx
import llm
from llm.default_plugins.openai_models import Chat
from pydantic import Field
from typing import Optional
import json
import click
import time
from pathlib import Path

# Try to import AsyncChat, but make it optional for older LLM versions
try:
    from llm.default_plugins.openai_models import AsyncChat
    HAS_ASYNC_CHAT = True
except ImportError:
    AsyncChat = None
    HAS_ASYNC_CHAT = False


class _mixin:
    class Options(Chat.Options):
        pass

    def build_kwargs(self, prompt, stream):
        kwargs = super().build_kwargs(prompt, stream)
        return kwargs


class LiteLLMChat(_mixin, Chat):
    needs_key = "litellm"
    key_env_var = "LITELLM_KEY"

    def __init__(self, model_id, model_name, api_base, **kwargs):
        self._model_name = model_name
        super().__init__(model_id, api_base=api_base, **kwargs)
        # Set model_name after parent initialization
        self._model_name = model_name

    @property
    def model_name(self):
        return self._model_name

    @model_name.setter
    def model_name(self, value):
        self._model_name = value

    def __str__(self):
        return self.model_id


# Only define async chat class if AsyncChat is available
if HAS_ASYNC_CHAT:
    class LiteLLMAsyncChat(_mixin, AsyncChat):
        needs_key = "litellm"
        key_env_var = "LITELLM_KEY"

        def __init__(self, model_id, model_name, api_base, **kwargs):
            self._model_name = model_name
            super().__init__(model_id, api_base=api_base, **kwargs)
            # Set model_name after parent initialization
            self._model_name = model_name

        @property
        def model_name(self):
            return self._model_name

        @model_name.setter
        def model_name(self, value):
            self._model_name = value

        def __str__(self):
            return self.model_id
else:
    LiteLLMAsyncChat = None


def get_litellm_url():
    """Get LiteLLM URL from environment variable."""
    litellm_url = os.getenv("LITELLM_URL")
    if not litellm_url:
        raise ValueError(
            "LITELLM_URL environment variable is required. "
            "Please set it to your LiteLLM server URL (e.g., http://localhost:4000)"
        )
    
    # Ensure URL ends with /v1 for OpenAI-compatible API
    if not litellm_url.endswith('/v1'):
        if litellm_url.endswith('/'):
            litellm_url = litellm_url + 'v1'
        else:
            litellm_url = litellm_url + '/v1'
    
    return litellm_url


class DownloadError(Exception):
    pass


def fetch_cached_json(url, path, cache_timeout, headers=None):
    """Fetch JSON data with caching support."""
    path = Path(path)

    # Create directories if not exist
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.is_file():
        # Get the file's modification time
        mod_time = path.stat().st_mtime
        # Check if it's more than the cache_timeout old
        if time.time() - mod_time < cache_timeout:
            # If not, load the file
            with open(path, "r") as file:
                return json.load(file)

    # Try to download the data
    try:
        response = httpx.get(url, headers=headers or {}, follow_redirects=True, timeout=10.0)
        response.raise_for_status()  # This will raise an HTTPError if the request fails

        # If successful, write to the file
        with open(path, "w") as file:
            json.dump(response.json(), file, indent=2)

        return response.json()
    except httpx.HTTPError:
        # If there's an existing file, load it
        if path.is_file():
            with open(path, "r") as file:
                return json.load(file)
        else:
            # If not, raise an error
            raise DownloadError(
                f"Failed to download data and no cache is available at {path}"
            )


def get_litellm_models():
    """Fetch available models from LiteLLM server with caching."""
    try:
        litellm_url = get_litellm_url()
        
        # Get API key if available
        key = llm.get_key("", "litellm", "LITELLM_KEY")
        headers = {}
        if key:
            headers["Authorization"] = f"Bearer {key}"
        
        # Use caching with 1-hour timeout
        models_data = fetch_cached_json(
            url=f"{litellm_url}/models",
            path=llm.user_dir() / "litellm_models.json",
            cache_timeout=3600,
            headers=headers
        )
        
        if "data" in models_data:
            return models_data["data"]
        else:
            return models_data
    except Exception as e:
        # If we can't fetch models, return some common defaults
        print(f"Warning: Could not fetch models from LiteLLM server: {e}")
        return [
            {"id": "gpt-3.5-turbo", "object": "model"},
            {"id": "gpt-4", "object": "model"},
            {"id": "claude-3-sonnet", "object": "model"},
            {"id": "claude-3-haiku", "object": "model"},
        ]


@llm.hookimpl
def register_models(register):
    # Check if LITELLM_URL is set
    try:
        litellm_url = get_litellm_url()
    except ValueError:
        # If LITELLM_URL is not set, don't register any models
        return
    
    # Get available models from LiteLLM server
    models = get_litellm_models()
    
    for model in models:
        model_id = model.get("id", "unknown")
        model_name = model_id
        
        kwargs = dict(
            model_id=f"litellm/{model_id}",
            model_name=model_name,
            api_base=litellm_url,
        )
        
        # Create model instances
        chat_model = LiteLLMChat(**kwargs)
        
        if HAS_ASYNC_CHAT:
            async_chat_model = LiteLLMAsyncChat(**kwargs)
            register(chat_model, async_chat_model)
        else:
            register(chat_model)


def refresh_models():
    """Refresh the cached models from the LiteLLM server"""
    try:
        litellm_url = get_litellm_url()
    except ValueError as e:
        raise click.ClickException(str(e))
    
    # Get API key if available
    key = llm.get_key("", "litellm", "LITELLM_KEY")
    headers = {}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    
    # Refresh models cache
    try:
        response = httpx.get(f"{litellm_url}/models", headers=headers, follow_redirects=True, timeout=10.0)
        response.raise_for_status()
        models_data = response.json()
        
        models_path = llm.user_dir() / "litellm_models.json"
        models_path.parent.mkdir(parents=True, exist_ok=True)
        with open(models_path, "w") as file:
            json.dump(models_data, file, indent=2)
        
        if "data" in models_data:
            models_count = len(models_data["data"])
        else:
            models_count = len(models_data) if isinstance(models_data, list) else 1
        
        click.echo(f"Refreshed {models_count} models cache at {models_path}", err=True)
        
    except httpx.HTTPError as e:
        raise click.ClickException(f"Failed to refresh models cache: {e}")


@llm.hookimpl
def register_commands(cli):
    @cli.group()
    def litellm():
        "Commands relating to the llm-lite plugin"

    @litellm.command()
    def refresh():
        "Refresh the cached models from the LiteLLM server"
        refresh_models()

    @litellm.command()
    @click.option("json_", "--json", is_flag=True, help="Output as JSON")
    def models(json_):
        "List available LiteLLM models"
        try:
            all_models = get_litellm_models()
            if json_:
                click.echo(json.dumps(all_models, indent=2))
            else:
                # Custom format
                for model in all_models:
                    model_id = model.get("id", "unknown")
                    click.echo(f"- id: {model_id}")
                    if "object" in model:
                        click.echo(f"  type: {model['object']}")
                    if "owned_by" in model:
                        click.echo(f"  owned_by: {model['owned_by']}")
                    click.echo()
        except Exception as e:
            click.echo(f"Error fetching models: {e}", err=True)

    @litellm.command()
    def status():
        "Check LiteLLM server status"
        try:
            litellm_url = get_litellm_url()
            
            # Get API key if available
            key = llm.get_key("", "litellm", "LITELLM_KEY")
            headers = {}
            if key:
                headers["Authorization"] = f"Bearer {key}"
            
            # Try to hit the health endpoint
            health_url = litellm_url.replace('/v1', '/health')
            response = httpx.get(health_url, headers=headers, timeout=5.0)
            
            if response.status_code == 200:
                click.echo(f"✅ LiteLLM server is running at {litellm_url}")
                try:
                    health_data = response.json()
                    if isinstance(health_data, dict):
                        for key, value in health_data.items():
                            click.echo(f"   {key}: {value}")
                except:
                    click.echo(f"   Status: {response.status_code}")
            else:
                click.echo(f"⚠️  LiteLLM server responded with status {response.status_code}")
                
        except ValueError as e:
            click.echo(f"❌ Configuration error: {e}", err=True)
        except Exception as e:
            click.echo(f"❌ Cannot connect to LiteLLM server: {e}", err=True)