import argparse
from tAI.App.app import TAI
from tAI.KeyAutomation import Automate
from tAI.Utils.api_key_manager import update_api_key
from tAI.Utils.config_manager import config_manager

def tAI():
    parser = argparse.ArgumentParser(description="🤖 AI Command Helper", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--google", type=str, help="Set the Google Gemini API key")
    parser.add_argument("--openai", type=str, help="Set the OpenAI API key")
    parser.add_argument("--anthropic", type=str, help="Set the Anthropic API key")
    parser.add_argument("--openrouter", type=str, help="Set the OpenRouter API key")
    parser.add_argument("--default-model", type=str, help="Set the default model for the application")
    parser.add_argument("--models", action="store_true", help="List all available models")
    parser.add_argument("--fullscreen", type=str.lower, choices=['true', 'false'], help="Set the fullscreen mode (true or false)")
    args = parser.parse_args()

    models = config_manager.get_models()

    if args.models:
        print("Available models:")
        for name, identifier in models.items():
            print(f"- {name}: {identifier}")
        return

    if args.default_model:
        if args.default_model in models.values():
            config_manager.set_default_model(args.default_model)
            print(f"✅ Default model set to: {args.default_model}")
        else:
            print(f"❌ Error: Model '{args.default_model}' not found.")
            print("Please use the --models flag to see the list of available models.")
        return

    if args.fullscreen is not None:
        fullscreen_value = args.fullscreen == 'true'
        config_manager.set_set_full_screen(fullscreen_value)
        print(f"✅ Fullscreen mode set to: {fullscreen_value}")
        return
        
    api_keys_to_update = {
        "google": args.google,
        "openai": args.openai,
        "anthropic": args.anthropic,
        "openrouter": args.openrouter,
    }

    updated = False
    for provider, key in api_keys_to_update.items():
        if key:
            update_api_key(provider, key)
            updated = True

    if updated:
        return

    automate = Automate()
    
    # Get all configs
    default_model = config_manager.get_default_model()
    prompt = config_manager.get_prompt()
    fullscreen = config_manager.get_set_full_screen()
    openrouter_all = config_manager.get_set_openrouter_for_all()

    app = TAI(
        models=models,
        default_model=default_model,
        prompt=prompt,
        fullscreen=fullscreen,
        openrouter_all=openrouter_all,
    )
    result = app.run(inline=not fullscreen)
    if result is not None:
        automate.paste_command_to_terminal(result)

if __name__ == "__main__":
    tAI()