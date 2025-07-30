import os
import sys
import subprocess
import asyncio
import time
from typing import Optional, List

from textual.app import App, ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Input, Label, Static, Select, Button, TextArea
from textual.reactive import reactive
from textual import on, work
from textual.binding import Binding
from textual.worker import Worker
from textual.screen import Screen

from tAI.LLM.LLM_Integration import llm
from tAI.Utils.config_manager import config_manager
from tAI.Utils.api_key_manager import update_api_key


class SettingsScreen(Screen):
    """The settings screen."""

    def __init__(self, model_dict: dict, default_model_key: str, prompt: str, fullscreen: bool, openrouter_all: bool) -> None:
        super().__init__()
        self.model_dict = model_dict
        self.default_model_key = default_model_key
        self.prompt = prompt
        self.fullscreen = fullscreen
        self.openrouter_all = openrouter_all
        self.settings_tab = "default_model"

    def compose(self) -> ComposeResult:
        yield Container(
            Container(
                Button("← Back", id="back_btn"),
                Static("Settings", id="settings_title"),
                id="settings_header"
            ),
            Horizontal(
                Container(
                    Button("Default Model", id="nav_default_model", classes="nav-button active"),
                    Button("API Key Setup", id="nav_api_key", classes="nav-button"),
                    Button("Prompt Config", id="nav_prompt", classes="nav-button"),
                    Button("Others", id="nav_others", classes="nav-button"),
                    id="settings_nav"
                ),
                Container(
                    Container(
                        Static("Default Model", id="default_model_title"),
                        Select(
                            options=[(name, name) for name in self.model_dict.keys()],
                            value=self.default_model_key,
                            id="settings_model_select"
                        ),
                        Button("Save", id="save_default_model"),
                        id="default_model_panel"
                    ),
                    Container(
                        Static("API Key Setup", id="api_key_title"),
                        Select(
                            options=[
                                ("Google", "google"),
                                ("OpenAI", "openai"),
                                ("Anthropic", "anthropic"),
                                ("OpenRouter", "openrouter")
                            ],
                            value="google",
                            id="api_provider_select"
                        ),
                        Input(
                            placeholder="Enter your API key here...",
                            password=True,
                            id="api_key_input"
                        ),
                        Button("Save", id="save_api_key"),
                        id="api_key_panel",
                        classes="hidden"
                    ),
                    Container(
                        Static("Prompt Config", id="prompt_title"),
                        TextArea(self.prompt, id="prompt_textarea"),
                        Button("Save", id="save_prompt"),
                        id="prompt_panel",
                        classes="hidden"
                    ),
                    Container(
                        # Static("", id="others_title"),
                        Static("Full screen mode:", id="fullscreen_title"),
                        Select(
                            options=[("Yes", True), ("No", False)],
                            value=self.fullscreen,
                            id="fullscreen_select"
                        ),
                        Static("Set openrouter for all models:", id="openrouter_title"),
                        Static("(If set to 'Yes' then need to provide paid API key for openrouter, Default free openrouter API key won't work anymore)", id="openrouter_title_note"),
                        Select(
                            options=[("Yes", True), ("No", False)],
                            value=self.openrouter_all,
                            id="openrouter_select"
                        ),

                        Button("Save", id="save_others"),
                        id="others_panel",
                        classes="hidden"
                    ),
                    id="settings_content"
                ),
                id="settings_body"
            ),
            id="settings_container"
        )
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back_btn":
            self.app.pop_screen()
        elif event.button.id == "nav_default_model":
            self.settings_tab = "default_model"
            self.switch_tab()
        elif event.button.id == "nav_api_key":
            self.settings_tab = "api_key"
            self.switch_tab()
        elif event.button.id == "nav_prompt":
            self.settings_tab = "prompt"
            self.switch_tab()
        elif event.button.id == "nav_others":
            self.settings_tab = "others"
            self.switch_tab()
        elif event.button.id == "save_default_model":
            self.save_default_model()
        elif event.button.id == "save_api_key":
            self.save_api_key()
        elif event.button.id == "save_prompt":
            self.save_prompt()
        elif event.button.id == "save_others":
            self.save_other_settings()
            
    def switch_tab(self):
        for btn in self.query("#settings_nav Button"):
            btn.remove_class("active")
        
        for panel_id in ["#default_model_panel", "#api_key_panel", "#prompt_panel", "#others_panel"]:
            self.query_one(panel_id).add_class("hidden")
        
        if self.settings_tab == "default_model":
            self.query_one("#nav_default_model").add_class("active")
            self.query_one("#default_model_panel").remove_class("hidden")
        elif self.settings_tab == "api_key":
            self.query_one("#nav_api_key").add_class("active")
            self.query_one("#api_key_panel").remove_class("hidden")
        elif self.settings_tab == "prompt":
            self.query_one("#nav_prompt").add_class("active")
            self.query_one("#prompt_panel").remove_class("hidden")
        elif self.settings_tab == "others":
            self.query_one("#nav_others").add_class("active")
            self.query_one("#others_panel").remove_class("hidden")

    def save_default_model(self):
        select_widget = self.query_one("#settings_model_select", Select)
        selected_model_name = str(select_widget.value)
        model_id = self.model_dict[selected_model_name]
        
        config_manager.set_default_model(model_id)
        
        main_app = self.app
        main_app.default_model_value = model_id
        main_app.model = model_id
        main_app.query_one("#model_select", Select).value = selected_model_name
        main_app.status_text = f"✅ Default model saved: {selected_model_name}"

    def save_api_key(self):
        provider = str(self.query_one("#api_provider_select", Select).value)
        api_key_input = self.query_one("#api_key_input", Input)
        api_key = api_key_input.value.strip()
        
        if not api_key:
            self.app.status_text = "❌ Please enter an API key"
            return
        
        update_api_key(provider, api_key)
        api_key_input.value = ""
        self.app.status_text = f"✅ {provider.capitalize()} API key saved successfully (Please restart the app to apply the changes)"

    def save_prompt(self):
        prompt_text = self.query_one("#prompt_textarea", TextArea).text
        config_manager.set_prompt(prompt_text)
        self.app.prompt = prompt_text
        self.app.setup_llm()
        self.app.status_text = f"✅ Prompt configuration saved"

    def save_other_settings(self):
        fullscreen = self.query_one("#fullscreen_select", Select).value
        openrouter_all = self.query_one("#openrouter_select", Select).value
        config_manager.set_set_full_screen(fullscreen)
        config_manager.set_set_openrouter_for_all(openrouter_all)

        self.app.fullscreen = fullscreen
        self.app.openrouter_all = openrouter_all 
        
    
        self.app.status_text = "✅ Settings saved (Please restart the app to apply the changes)"


class TAI(App):
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    CSS_PATH = os.path.join(APP_ROOT, "style.tcss")

    BINDINGS = [
        Binding("escape", "quit", "Exit", priority=True),
        Binding("ctrl+c", "quit", "Cancel", priority=True),
        Binding("ctrl+e", "toggle_mode", "Toggle Execute/Paste Mode", priority=True),
        Binding("ctrl+s", "show_settings", "Settings", priority=True),
    ]

    status_text = reactive("Initializing...")
    current_command = reactive("")
    command_output = reactive("")
    show_response = reactive(False)
    show_output = reactive(False)
    execute_mode = reactive(False)
    pending_paste_command = None

    def __init__(self, models: dict, default_model: str, prompt: str, fullscreen: bool, openrouter_all: bool,):
        super().__init__()
        self.model_dict = models
        self.default_model_value = default_model
        self.model = self.default_model_value
        self.prompt = prompt
        self.fullscreen = fullscreen
        self.openrouter_all = openrouter_all
        self.default_model_key = [k for k, v in self.model_dict.items() if v == self.default_model_value][0]

    def compose(self) -> ComposeResult:
        yield Container(
            Container(
                Static("🤖 AI Command Helper", id="title"),
                Button("🛠️ Settings", id="settings_btn", classes="settings-button"),
                id="header"
            ),
            Select(
                options=[(name, name) for name in self.model_dict.keys()],
                value=self.default_model_key,
                id="model_select"
            ),
            Input(
                placeholder="e.g., 'list all files larger than 100MB'",
                id="input"
            ),
            Static(self.status_text, id="status"),
            Static("", id="response", classes="hidden"),
            Static("", id="output", classes="hidden"),
            id="main_container"
        )
        
    def action_show_settings(self) -> None:
        self.push_screen(SettingsScreen(
            self.model_dict, 
            self.default_model_key, 
            self.prompt,
            self.fullscreen,
            self.openrouter_all,
        ))

    @on(Button.Pressed, "#settings_btn")
    def handle_settings_button(self) -> None:
        self.action_show_settings()

    def on_mount(self) -> None:
        self.query_one("#input", Input).focus()
        self.setup_llm()

    def setup_llm(self):
        try:
            self.llm = llm(prompt=self.prompt, openrouter_all=self.openrouter_all)
            mode = "EXECUTE" if self.execute_mode else "PASTE"
            self.status_text = f"Ready! Mode: {mode} (Ctrl+E to toggle) | Type your command request..."
        except Exception as e:
            self.status_text = f"Error initializing LLM: {str(e)}"

    def watch_status_text(self, status: str) -> None:
        try:
            self.query_one("#status", Static).update(status)
        except:
            pass

    def watch_current_command(self, command: str) -> None:
        try:
            response_widget = self.query_one("#response", Static)
            if command:
                response_widget.update(f"Generated: {command}")
                response_widget.remove_class("hidden")
                self.show_response = True
            else:
                response_widget.add_class("hidden")
                self.show_response = False
        except:
            pass

    def watch_command_output(self, output: str) -> None:
        try:
            output_widget = self.query_one("#output", Static)
            if output:
                output_widget.update(f"Output:\n{output}")
                output_widget.remove_class("hidden")
                self.show_output = True
            else:
                output_widget.add_class("hidden")
                self.show_output = False
        except:
            pass

    def watch_execute_mode(self, mode: bool) -> None:
        if self.llm:
            mode_text = "EXECUTE" if mode else "PASTE"
            self.status_text = f"Ready! Mode: {mode_text} (Ctrl+E to toggle) | Type your command request..."

    def action_toggle_mode(self) -> None:
        self.execute_mode = not self.execute_mode
        self.command_output = ""
        
    @on(Select.Changed, "#model_select")
    def handle_llm_change(self, event: Select.Changed) -> None:
        self.model = self.model_dict[str(event.value)]

    @on(Input.Submitted)
    def handle_submission(self, event: Input.Submitted) -> None:
        query = event.value.strip()
        if not query:
            return
        if not self.llm:
            self.status_text = "❌ LLM not initialized"
            return
        
        self.current_command = ""
        self.command_output = ""
        self.status_text = "🔄 Generating command..."
        self.generate_command(self.model,query)

    @work(exclusive=True)
    async def generate_command(self, model: str, query: str) -> None:
        try:
            command = await asyncio.to_thread(
                self.llm.generate_command,
                model,
                query
            )
            
            if self.execute_mode:
                self.status_text = "✅ Command generated! Executing..."
                await self.execute_command(command)
            else:
                self.status_text = "✅ Command generated! Exiting and pasting to terminal..."
                self.pending_paste_command = command
                await asyncio.sleep(1)
                self.exit(result=command)
            
        except Exception as e:
            self.status_text = f"❌ Error: {str(e)}"

    @work(thread=True)
    def execute_command(self, command: str) -> None:
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            output = ""
            if result.stdout:
                output += result.stdout
            if result.stderr:
                output += f"\nErrors:\n{result.stderr}"
            
            if not output.strip():
                output = f"Command executed successfully (exit code: {result.returncode})"
            
            self.call_from_thread(self._update_after_execution, output, result.returncode)
            
        except subprocess.TimeoutExpired:
            self.call_from_thread(self._update_after_execution, "Command timed out after 30 seconds", 1)
        except Exception as e:
            self.call_from_thread(self._update_after_execution, f"Error executing command: {str(e)}", 1)

    def _update_after_execution(self, output: str, exit_code: int) -> None:
        self.command_output = output
        if exit_code == 0:
            self.status_text = "✅ Command executed successfully! Press Esc to exit or continue..."
        else:
            self.status_text = f"⚠️ Command failed (exit code: {exit_code}). Press Esc to exit or continue..."

    def action_quit(self) -> None:
        self.exit()