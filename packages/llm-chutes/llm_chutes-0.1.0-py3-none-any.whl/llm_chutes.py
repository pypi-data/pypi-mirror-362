import click
import llm
from llm.default_plugins.openai_models import Chat, AsyncChat
from pathlib import Path
from pydantic import Field
from typing import Optional
import json
import time
import httpx


def get_chutes_models():
    """Get models from Chutes AI API with caching"""
    models = fetch_cached_json(
        url="https://llm.chutes.ai/v1/models",
        path=llm.user_dir() / "chutes_models.json",
        cache_timeout=3600,
    )
    
    # Handle different response formats
    if isinstance(models, dict) and "data" in models:
        return models["data"]
    elif isinstance(models, list):
        return models
    else:
        return []


class _mixin:
    class Options(Chat.Options):
        cache: Optional[bool] = Field(
            description="Use auto caching for this model",
            default=None,
        )

    def build_kwargs(self, prompt, stream):
        kwargs = super().build_kwargs(prompt, stream)
        kwargs.pop("cache", None)
        extra_body = {}
        if prompt.options.cache:
            extra_body["chutes"] = {
                "auto_cache": True
            }
        if extra_body:
            kwargs["extra_body"] = extra_body
        return kwargs


class ChutesChat(_mixin, Chat):
    needs_key = "chutes"
    key_env_var = "CHUTES_API_KEY"

    def __str__(self):
        return "chutes: {}".format(self.model_id)


class ChutesAsyncChat(_mixin, AsyncChat):
    needs_key = "chutes"
    key_env_var = "CHUTES_API_KEY"

    def __str__(self):
        return "chutes: {}".format(self.model_id)


@llm.hookimpl
def register_models(register):
    # Only do this if the chutes key is set
    key = llm.get_key("", "chutes", "CHUTES_API_KEY")
    if not key:
        return
    
    for model_definition in get_chutes_models():
        supports_images = get_supports_images(model_definition)
        supports_schema = model_definition.get("supports_schema", False)
        
        kwargs = dict(
            model_id="chutes/{}".format(model_definition["id"]),
            model_name=model_definition["id"],
            vision=supports_images,
            supports_schema=supports_schema,
            api_base="https://llm.chutes.ai/v1",
            headers={"HTTP-Referer": "https://llm.datasette.io/", "X-Title": "LLM"},
        )
        
        # Create model instances
        chat_model = ChutesChat(**kwargs)
        async_chat_model = ChutesAsyncChat(**kwargs)
        
        # Add attachment types for vision models
        if supports_images:
            chat_model.attachment_types = ["image/png", "image/jpeg", "image/gif", "image/webp"]
            async_chat_model.attachment_types = ["image/png", "image/jpeg", "image/gif", "image/webp"]
        
        register(chat_model, async_chat_model)


class DownloadError(Exception):
    pass


def fetch_cached_json(url, path, cache_timeout):
    """Fetch JSON from URL with caching support"""
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
        # Get API key for authenticated requests
        key = llm.get_key("", "chutes", "CHUTES_API_KEY")
        headers = {"HTTP-Referer": "https://llm.datasette.io/", "X-Title": "LLM"}
        if key:
            headers["Authorization"] = f"Bearer {key}"
            
        response = httpx.get(url, headers=headers, follow_redirects=True)
        response.raise_for_status()

        # If successful, write to the file
        with open(path, "w") as file:
            json.dump(response.json(), file)

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


def get_supports_images(model_definition):
    """Check if a model supports image inputs"""
    try:
        # Check if the model supports vision based on the supports_vision field
        if model_definition.get("supports_vision", False):
            return True
        
        # Fallback: check if the model name/ID contains vision-related keywords
        model_id = model_definition.get("id", "").lower()
        vision_keywords = ["vision", "visual", "multimodal", "vlm", "gpt-4o", "claude-3"]
        return any(keyword in model_id for keyword in vision_keywords)
    except Exception:
        return False


def refresh_models():
    """Refresh the cached models from the Chutes AI API"""
    key = llm.get_key("", "chutes", "CHUTES_API_KEY")
    if not key:
        raise click.ClickException("No key found for Chutes AI")
    
    headers = {
        "HTTP-Referer": "https://llm.datasette.io/", 
        "X-Title": "LLM",
        "Authorization": f"Bearer {key}"
    }
    
    # Refresh models cache
    try:
        response = httpx.get("https://llm.chutes.ai/v1/models", headers=headers, follow_redirects=True)
        response.raise_for_status()
        models_data = response.json()
        
        models_path = llm.user_dir() / "chutes_models.json"
        models_path.parent.mkdir(parents=True, exist_ok=True)
        with open(models_path, "w") as file:
            json.dump(models_data, file, indent=2)
        
        # Handle different response formats
        if isinstance(models_data, dict) and "data" in models_data:
            models_count = len(models_data["data"])
        elif isinstance(models_data, list):
            models_count = len(models_data)
        else:
            models_count = 0
            
        click.echo(f"Refreshed {models_count} models cache at {models_path}", err=True)
        
    except httpx.HTTPError as e:
        raise click.ClickException(f"Failed to refresh models cache: {e}")


@llm.hookimpl
def register_commands(cli):
    @cli.group()
    def chutes():
        "Commands relating to the llm-chutes plugin"

    @chutes.command()
    def refresh():
        "Refresh the cached models from the Chutes AI API"
        refresh_models()

    @chutes.command()
    @click.option("json_", "--json", is_flag=True, help="Output as JSON")
    def models(json_):
        "List of Chutes AI models"
        all_models = get_chutes_models()
        if json_:
            click.echo(json.dumps(all_models, indent=2))
        else:
            # Custom format
            for model in all_models:
                bits = []
                bits.append(f"- id: {model['id']}")
                
                # Use root as name if available, otherwise use id
                name = model.get('root', model.get('name', model.get('description', model['id'])))
                bits.append(f"  name: {name}")
                
                # Handle context length from max_model_len
                context_length = model.get('max_model_len', model.get('context_window', model.get('context_length', 'N/A')))
                if isinstance(context_length, int):
                    bits.append(f"  context_length: {context_length:,}")
                else:
                    bits.append(f"  context_length: {context_length}")
                
                # Check for schema support (assume True for now since Chutes doesn't provide this info)
                supports_schema = model.get('supports_schema', True)
                bits.append(f"  supports_schema: {supports_schema}")
                
                # Handle pricing from Chutes AI format
                pricing_dict = {}
                if 'price' in model and isinstance(model['price'], dict):
                    if 'usd' in model['price']:
                        # Chutes AI provides a single USD price, we'll assume it's per 1M tokens
                        usd_price = model['price']['usd']
                        # Convert to per-token price (assuming the price is per 1M tokens)
                        price_per_token = usd_price / 1000000
                        pricing_dict['input'] = str(price_per_token)
                        pricing_dict['output'] = str(price_per_token)
                
                # Fallback to other pricing formats
                if not pricing_dict:
                    if 'input_price' in model:
                        pricing_dict['input'] = model['input_price']
                    if 'output_price' in model:
                        pricing_dict['output'] = model['output_price']
                    elif 'pricing' in model and isinstance(model['pricing'], dict):
                        if 'input' in model['pricing']:
                            pricing_dict['input'] = model['pricing']['input']
                        if 'output' in model['pricing']:
                            pricing_dict['output'] = model['pricing']['output']
                
                pricing = format_pricing(pricing_dict) if pricing_dict else None
                if pricing:
                    bits.append("  pricing: " + pricing)
                    
                click.echo("\n".join(bits) + "\n")


def format_price(key, price_str):
    """Format a price value with appropriate scaling and no trailing zeros."""
    try:
        price = float(price_str)
    except (ValueError, TypeError):
        return None

    if price == 0:
        return None

    # Determine scale based on magnitude
    if price < 0.0001:
        scale = 1000000
        suffix = "/M"
    elif price < 0.001:
        scale = 1000
        suffix = "/K"
    elif price < 1:
        scale = 1000
        suffix = "/K"
    else:
        scale = 1
        suffix = ""

    # Scale the price
    scaled_price = price * scale

    # Format without trailing zeros
    price_str = (
        f"{scaled_price:.10f}".rstrip("0").rstrip(".")
        if "." in f"{scaled_price:.10f}"
        else f"{scaled_price:.0f}"
    )

    return f"{key} ${price_str}{suffix}"


def format_pricing(pricing_dict):
    """Format pricing dictionary into a readable string"""
    formatted_parts = []
    for key, value in pricing_dict.items():
        formatted_price = format_price(key, value)
        if formatted_price:
            formatted_parts.append(formatted_price)
    return ", ".join(formatted_parts)