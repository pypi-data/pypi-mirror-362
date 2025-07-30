"""
This module handles updating API keys in the .env file.
"""
from dotenv import set_key
import os
from tAI.Utils.security import encrypt_data

# Determine the absolute path to the .env file based on the script's location.
# This ensures we always use the .env file bundled with the application.
APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOTENV_PATH = os.path.join(APP_ROOT, ".env")

def update_api_key(provider: str, api_key: str) -> None:
    """
    Updates the API key for a given provider in the bundled .env file.

    Args:
        provider (str): The name of the provider (e.g., 'google', 'openai').
        api_key (str): The API key to set.
    """
    key_mapping = {
        "google": "GEMINI_API_KEY",
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "openrouter": "OPENROUTER_API_KEY",
    }
    
    variable_name = key_mapping.get(provider)
    if variable_name:
        encrypted_key = encrypt_data(api_key)
        # Check if the .env file exists before trying to write to it.
        # The build script ensures it's created.
        if os.path.exists(DOTENV_PATH):
            set_key(DOTENV_PATH, variable_name, encrypted_key)
            print(f"✅ Successfully updated {provider.capitalize()} API key.")
        else:
            print(f"❌ Error: .env file not found at {DOTENV_PATH}. Please reinstall the package.")
    else:
        print(f"❌ Invalid provider specified: {provider}") 