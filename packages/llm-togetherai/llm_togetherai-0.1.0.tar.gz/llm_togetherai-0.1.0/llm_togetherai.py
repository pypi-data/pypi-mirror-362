import click
import llm
from llm.default_plugins.openai_models import Chat, AsyncChat
from pathlib import Path
from pydantic import Field
from typing import Optional
import json
import time
import httpx


def get_together_models():
    """Fetch Together AI models from cache or API"""
    models = fetch_cached_json(
        url="https://api.together.xyz/v1/models",
        path=llm.user_dir() / "together_models.json",
        cache_timeout=3600,
    )
    
    # Together AI returns a list directly, not wrapped in a "data" field
    if isinstance(models, list):
        return models
    else:
        # Fallback in case the API structure changes
        return models.get("data", models)


class _mixin:
    """Mixin class for Together AI specific options and functionality"""
    
    class Options(Chat.Options):
        # Together AI specific options can be added here
        pass

    def build_kwargs(self, prompt, stream):
        """Build kwargs for the API request"""
        kwargs = super().build_kwargs(prompt, stream)
        return kwargs


class TogetherChat(_mixin, Chat):
    """Together AI Chat model implementation"""
    needs_key = "together"
    key_env_var = "TOGETHER_API_KEY"

    def __str__(self):
        return "together: {}".format(self.model_id)


class TogetherAsyncChat(_mixin, AsyncChat):
    """Together AI Async Chat model implementation"""
    needs_key = "together"
    key_env_var = "TOGETHER_API_KEY"

    def __str__(self):
        return "together: {}".format(self.model_id)


@llm.hookimpl
def register_models(register):
    """Register Together AI models with LLM"""
    # Only register models if the Together AI key is set
    key = llm.get_key("", "together", "TOGETHER_API_KEY")
    if not key:
        return
    
    for model_definition in get_together_models():
        supports_images = get_supports_images(model_definition)
        
        kwargs = dict(
            model_id="together/{}".format(model_definition["id"]),
            model_name=model_definition["id"],
            vision=supports_images,
            api_base="https://api.together.xyz/v1",
            headers={
                "HTTP-Referer": "https://llm.datasette.io/", 
                "X-Title": "LLM"
            },
        )
        
        # Create model instances
        chat_model = TogetherChat(**kwargs)
        async_chat_model = TogetherAsyncChat(**kwargs)
        
        # Add attachment types for vision models
        if supports_images:
            chat_model.attachment_types = ["image/png", "image/jpeg", "image/gif", "image/webp"]
            async_chat_model.attachment_types = ["image/png", "image/jpeg", "image/gif", "image/webp"]
        
        register(chat_model, async_chat_model)


class DownloadError(Exception):
    """Exception raised when model data cannot be downloaded or cached"""
    pass


def fetch_cached_json(url, path, cache_timeout):
    """
    Fetch JSON data from URL with caching mechanism
    
    Args:
        url: The URL to fetch data from
        path: Local cache file path
        cache_timeout: Cache timeout in seconds
    
    Returns:
        JSON data from cache or API
    """
    path = Path(path)

    # Create directories if they don't exist
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
        # Get the Together AI API key for authentication
        key = llm.get_key("", "together", "TOGETHER_API_KEY")
        headers = {
            "Authorization": f"Bearer {key}",
            "HTTP-Referer": "https://llm.datasette.io/", 
            "X-Title": "LLM"
        }
        
        response = httpx.get(url, headers=headers, follow_redirects=True)
        response.raise_for_status()

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


def get_supports_images(model_definition):
    """
    Determine if a model supports image inputs based on its definition
    
    Args:
        model_definition: Model definition from Together AI API
    
    Returns:
        bool: True if model supports images, False otherwise
    """
    try:
        # Check model type - Together AI uses "type" field
        model_type = model_definition.get("type", "").lower()
        if "vision" in model_type or "multimodal" in model_type:
            return True
        
        # Check model ID for vision-related keywords
        model_id = model_definition.get("id", "").lower()
        vision_keywords = ["vision", "visual", "multimodal", "vlm", "llava"]
        return any(keyword in model_id for keyword in vision_keywords)
    except Exception:
        return False


def refresh_models():
    """Refresh the cached models from the Together AI API"""
    key = llm.get_key("", "together", "TOGETHER_API_KEY")
    if not key:
        raise click.ClickException("No key found for Together AI")
    
    headers = {
        "Authorization": f"Bearer {key}",
        "HTTP-Referer": "https://llm.datasette.io/", 
        "X-Title": "LLM"
    }
    
    # Refresh models cache
    try:
        response = httpx.get("https://api.together.xyz/v1/models", headers=headers, follow_redirects=True)
        response.raise_for_status()
        models_data = response.json()
        
        models_path = llm.user_dir() / "together_models.json"
        models_path.parent.mkdir(parents=True, exist_ok=True)
        with open(models_path, "w") as file:
            json.dump(models_data, file, indent=2)
        
        # Together AI returns a list directly
        models_count = len(models_data) if isinstance(models_data, list) else len(models_data.get("data", []))
        click.echo(f"Refreshed {models_count} models cache at {models_path}", err=True)
        
    except httpx.HTTPError as e:
        raise click.ClickException(f"Failed to refresh models cache: {e}")


@llm.hookimpl
def register_commands(cli):
    """Register CLI commands for the Together AI plugin"""
    
    @cli.group()
    def together():
        "Commands relating to the llm-togetherai plugin"

    @together.command()
    def refresh():
        "Refresh the cached models from the Together AI API"
        refresh_models()

    @together.command()
    @click.option("json_", "--json", is_flag=True, help="Output as JSON")
    def models(json_):
        "List of Together AI models"
        all_models = get_together_models()
        if json_:
            click.echo(json.dumps(all_models, indent=2))
        else:
            # Custom format
            for model in all_models:
                bits = []
                bits.append(f"- id: {model['id']}")
                
                # Use display_name if available, otherwise use id
                name = model.get('display_name', model['id'])
                bits.append(f"  name: {name}")
                
                # Context length
                context_length = model.get('context_length', 'N/A')
                if isinstance(context_length, int) and context_length > 0:
                    bits.append(f"  context_length: {context_length:,}")
                else:
                    bits.append(f"  context_length: {context_length}")
                
                # Model type
                model_type = model.get('type', 'N/A')
                bits.append(f"  type: {model_type}")
                
                # Organization
                organization = model.get('organization', 'N/A')
                bits.append(f"  organization: {organization}")
                
                # Pricing information
                pricing_dict = model.get('pricing', {})
                if pricing_dict:
                    pricing = format_pricing(pricing_dict)
                    if pricing:
                        bits.append("  pricing: " + pricing)
                
                click.echo("\n".join(bits) + "\n")


def format_price(key, price_value):
    """Format a price value with appropriate scaling and no trailing zeros."""
    if price_value == 0:
        return None

    # Convert to float if it's not already
    price = float(price_value)

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
    
    # Together AI pricing structure
    for key, value in pricing_dict.items():
        if key in ["input", "output"] and value > 0:
            formatted_price = format_price(key, value)
            if formatted_price:
                formatted_parts.append(formatted_price)
    
    return ", ".join(formatted_parts)