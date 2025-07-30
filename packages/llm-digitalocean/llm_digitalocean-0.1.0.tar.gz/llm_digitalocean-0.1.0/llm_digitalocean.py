import click
import llm
from llm.default_plugins.openai_models import Chat, AsyncChat
from pathlib import Path
from pydantic import Field
from typing import Optional
import json
import time
import httpx


def get_digitalocean_models():
    """Get DigitalOcean models with caching support"""
    models = fetch_cached_json(
        url="https://inference.do-ai.run/v1/models",
        path=llm.user_dir() / "digitalocean_models.json",
        cache_timeout=3600,  # 1 hour cache
        headers=get_headers(),
    )["data"]
    
    # Process models to add additional metadata
    for model in models:
        model["supports_schema"] = False  # DigitalOcean doesn't support structured outputs yet
        model["supports_vision"] = get_supports_images(model)
    
    return models


def get_headers():
    """Get headers for DigitalOcean API requests"""
    key = llm.get_key("", "digitalocean", "DIGITAL_OCEAN")
    if not key:
        raise click.ClickException("No key found for DigitalOcean. Set DIGITAL_OCEAN environment variable or use 'llm keys set digitalocean'")
    
    return {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://llm.datasette.io/",
        "X-Title": "LLM"
    }


class _mixin:
    class Options(Chat.Options):
        pass

    def build_kwargs(self, prompt, stream):
        kwargs = super().build_kwargs(prompt, stream)
        return kwargs


class DigitalOceanChat(_mixin, Chat):
    needs_key = "digitalocean"
    key_env_var = "DIGITAL_OCEAN"

    def __str__(self):
        return "DigitalOcean: {}".format(self.model_id)


class DigitalOceanAsyncChat(_mixin, AsyncChat):
    needs_key = "digitalocean"
    key_env_var = "DIGITAL_OCEAN"

    def __str__(self):
        return "DigitalOcean: {}".format(self.model_id)


@llm.hookimpl
def register_models(register):
    # Only do this if the DigitalOcean key is set
    key = llm.get_key("", "digitalocean", "DIGITAL_OCEAN")
    if not key:
        return
    
    for model_definition in get_digitalocean_models():
        supports_images = get_supports_images(model_definition)
        kwargs = dict(
            model_id="digitalocean/{}".format(model_definition["id"]),
            model_name=model_definition["id"],
            vision=supports_images,
            supports_schema=model_definition.get("supports_schema", False),
            api_base="https://inference.do-ai.run/v1",
            headers=get_headers(),
        )
        
        # Create model instances
        chat_model = DigitalOceanChat(**kwargs)
        async_chat_model = DigitalOceanAsyncChat(**kwargs)
        
        # Add attachment types for vision models
        if supports_images:
            chat_model.attachment_types = ["image/png", "image/jpeg", "image/gif", "image/webp"]
            async_chat_model.attachment_types = ["image/png", "image/jpeg", "image/gif", "image/webp"]
        
        register(chat_model, async_chat_model)


class DownloadError(Exception):
    pass


def fetch_cached_json(url, path, cache_timeout, headers=None):
    """Fetch JSON data with caching support"""
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
        response = httpx.get(url, headers=headers or {}, follow_redirects=True, timeout=30.0)
        response.raise_for_status()  # This will raise an HTTPError if the request fails

        # If successful, write to the file
        with open(path, "w") as file:
            json.dump(response.json(), file, indent=2)

        return response.json()
    except httpx.HTTPError as e:
        # If there's an existing file, load it
        if path.is_file():
            with open(path, "r") as file:
                return json.load(file)
        else:
            # If not, raise an error
            raise DownloadError(
                f"Failed to download data from {url} and no cache is available at {path}: {e}"
            )


def get_supports_images(model_definition):
    """Check if a model supports vision/images"""
    try:
        # Check if the model supports vision based on explicit field
        if model_definition.get("supports_vision", False):
            return True
        
        # Fallback: check if the model name/ID contains vision-related keywords
        model_id = model_definition.get("id", "").lower()
        vision_keywords = ["vision", "visual", "multimodal", "vlm", "gpt-4o", "claude-3"]
        return any(keyword in model_id for keyword in vision_keywords)
    except Exception:
        return False


def refresh_models():
    """Refresh the cached models from the DigitalOcean API"""
    key = llm.get_key("", "digitalocean", "DIGITAL_OCEAN")
    if not key:
        raise click.ClickException("No key found for DigitalOcean. Set DIGITAL_OCEAN environment variable or use 'llm keys set digitalocean'")
    
    headers = get_headers()
    
    # Refresh models cache
    try:
        response = httpx.get("https://inference.do-ai.run/v1/models", headers=headers, follow_redirects=True, timeout=30.0)
        response.raise_for_status()
        models_data = response.json()
        
        models_path = llm.user_dir() / "digitalocean_models.json"
        models_path.parent.mkdir(parents=True, exist_ok=True)
        with open(models_path, "w") as file:
            json.dump(models_data, file, indent=2)
        
        models_count = len(models_data.get("data", []))
        click.echo(f"Refreshed {models_count} DigitalOcean models cache at {models_path}", err=True)
        
    except httpx.HTTPError as e:
        raise click.ClickException(f"Failed to refresh models cache: {e}")


@llm.hookimpl
def register_commands(cli):
    @cli.group()
    def digitalocean():
        "Commands relating to the llm-digitalocean plugin"

    @digitalocean.command()
    def refresh():
        "Refresh the cached models from the DigitalOcean API"
        refresh_models()

    @digitalocean.command()
    @click.option("json_", "--json", is_flag=True, help="Output as JSON")
    def models(json_):
        "List of DigitalOcean models"
        all_models = get_digitalocean_models()
        if json_:
            click.echo(json.dumps(all_models, indent=2))
        else:
            # Custom format
            for model in all_models:
                bits = []
                bits.append(f"- id: {model['id']}")
                # Use object type or id as name
                name = model.get('object', model['id'])
                bits.append(f"  name: {name}")
                
                # Add creation date if available
                if 'created' in model:
                    created_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(model['created']))
                    bits.append(f"  created: {created_time}")
                
                # Add owner information
                if 'owned_by' in model:
                    bits.append(f"  owned_by: {model['owned_by']}")
                
                bits.append(f"  supports_schema: {model.get('supports_schema', False)}")
                bits.append(f"  supports_vision: {model.get('supports_vision', False)}")
                
                click.echo("\n".join(bits) + "\n")

    @digitalocean.command()
    def cache_info():
        "Show cache information"
        cache_file = llm.user_dir() / "digitalocean_models.json"
        if cache_file.exists():
            cache_stat = cache_file.stat()
            cache_age = time.time() - cache_stat.st_mtime
            click.echo(f"Cache file: {cache_file}")
            click.echo(f"Cache age: {cache_age:.0f} seconds ({cache_age/3600:.1f} hours)")
            
            try:
                with open(cache_file, 'r') as f:
                    cached_data = json.load(f)
                    models_count = len(cached_data.get('data', []))
                    click.echo(f"Cached models: {models_count}")
            except (json.JSONDecodeError, KeyError):
                click.echo("Cache file is corrupted")
        else:
            click.echo("No cache file found")