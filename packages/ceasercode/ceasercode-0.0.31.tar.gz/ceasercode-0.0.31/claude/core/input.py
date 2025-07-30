"""
Claude Code Chat Interface

This module provides the main chat interface for Claude Code with the following features:
- Real-time chat with AI models
- Tool execution with permission system
- Dynamic footer content updates
- Command palette and keyboard shortcuts
- Multiple permission modes (default, auto-accept-edits, bypass-permissions, plan-mode)

Footer Management:
- Left footer: Can be updated dynamically using update_left_footer()
- Right footer: Shows current mode, updated via cycle_mode()
"""

import asyncio
from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, ScrollableContainer
from textual.widgets import Input, Static, Label, ProgressBar, OptionList
from textual import on
from textual.binding import Binding
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown

from claude.tools import tools, tools_dict
from claude.llm import OAI
from claude.core.utils import ORANGE_COLORS, get_contextual_thinking_words, SYSTEM_PROMPT
from claude.core.prompt import PLAN_MODE_PROMPT, DEFAULT_MODE_PROMPT
from claude.core.config import config


class State:
    def __init__(self):
        self.user_interrupt = False


class ChatApp(App):
    """Simple chat interface with message display and input"""
    
    BINDINGS = [
        Binding("shift+tab", "cycle_mode", "Cycle Mode", priority=True),
        Binding("ctrl+c", "clear_input", "Clear Input", priority=True),
        Binding("escape", "interrupt_conversation", "Interrupt Conversation", priority=True),
        Binding("ctrl+d", "clear_input", "Clear Input", priority=True),
        Binding("ctrl+l", "clear_screen", "Clear Screen", priority=True),
        Binding("shift+up", "previous_command", "Previous Command", priority=True),
        Binding("shift+down", "next_command", "Next Command", priority=True),   
    ]
    
    CSS = """
    Screen {
        background: transparent;
    }

    #chat_area {
        height: 1fr;
        padding: 1;
        background: transparent;
        overflow-y: auto;
        scrollbar-size: 0 0;
    }

    #input_area {
        height: auto;
        border: round grey;
        background: transparent;
    }

    #status_bar {
        height: 1;
        background: transparent;
        padding: 0 1;
    }

    #status_indicator {
        color: #E27A53;
        text-style: bold;
    }

    #footer {
        height: 1;
        dock: bottom;
        background: transparent;
    }

    #footer-left {
        text-align: left;
        width: 1fr;
    }

    #footer-right {
        text-align: right;
        width: auto;
    }
    
    .mode-bypass {
        color: #fabd2f;
    }
    
    .mode-plan {
        color: #458588;
    }
    
    .mode-auto-edit {
        color: #915FF0;
    }

    Input {
        background: transparent;
    }

    Static {
        background: transparent;
    }

    .message {
        background: transparent;
        color: grey;
        text-style: italic;
    }
    
    .ai-response {
        background: transparent;
    }
    
    
    .streaming {
        background: transparent;
        color: #E77D22;
    }
    
    .tool-executing {
        background: transparent;
    }
    
    .tool-completed {
        background: transparent;
    }
    
    #permission_area {
        height: auto;
        background: transparent;
        border: round #458588;
        padding: 1;
        margin: 0;
    }
    
    #permission_message {
        color: #a89984;
        text-style: italic;
        padding: 0 0 1 0;
        background: transparent;
    }
    
    #permission_options {
        background: transparent;
        border: none;
        height: auto;
        scrollbar-size: 0 0;
    }
    
    #permission_options:focus {
        border: none;
    }
    
    .option-list--option {
        background: transparent;
        color: #a89984;
        padding: 0 1;
        height: 1;
    }
    
    .option-list--option-highlighted {
        background: transparent;
        color: #fabd2f;
        text-style: bold;
    }
    
    #command_palette {
        height: auto;
        background: transparent;
        border: round #915FF0;
        padding: 1;
        margin: 0;
    }
    
    #command_palette_message {
        color: #a89984;
        text-style: italic;
        padding: 0 0 1 0;
        background: transparent;
    }
    
    #command_options {
        background: transparent;
        border: none;
        height: auto;
        scrollbar-size: 0 0;
    }
    
    #command_options:focus {
        border: none;
    }
    
    """

    def __init__(self,cwd):
        super().__init__()
        self.state = State()
        self.llm = self._initialize_llm()
        self.tool_widgets = {}  # Track tool execution widgets
        self.cwd = cwd
        
        # Generate unique session ID for this chat session
        import uuid
        self.session_id = str(uuid.uuid4())
        
        # Permission system state
        self.pending_tool_call = None
        self.auto_approve_tools = set()  # Tools that user chose "don't ask again" for
        self.waiting_for_permission = False
        
        # Command palette state
        self.waiting_for_command = False
        
        # Command history for up/down arrow navigation
        self.command_history = []
        self.history_index = -1
        
        # Edit confirmation state
        self.pending_edit_result = None
        self.pending_edit_tool_id = None
        self.pending_edit_tool_args = None
        self.waiting_for_edit_confirmation = False
        
        # Agentic loop state for resuming after permissions
        self.pending_agentic_state = None
        
        # Permission modes: 'default', 'auto-accept-edits', 'bypass-permissions', 'plan-mode'
        self.permission_mode = 'default'
        self.modes = ['default', 'auto-accept-edits', 'bypass-permissions', 'plan-mode']
        self.current_mode_index = 0
        
        # Initialize conversation history with system prompt
        self.conversation_history = [
            {"role": "system", "content": self.get_system_prompt()}
        ]
        
        # Tools that don't need permission in default mode
        self.no_permission_tools = {'read_file', 'list_directory', 'web_search', 'fetch_url'}
        
        # Tools that are auto-approved in auto-accept-edits mode
        self.auto_accept_edit_tools = {'write_file', 'edit_file', 'multi_edit_file'}

    def compose(self) -> ComposeResult:
        with ScrollableContainer(id="chat_area"):
            welcome_panel = Panel(
                renderable=Text.from_markup(f"[{ORANGE_COLORS[17]}]✻ [/][bold]Welcome to [/][bold white]Claude Code[/]!\n\n"
                                 f"/help for help, /status for your current setup\n\ncwd: {self.cwd}"),
                border_style=ORANGE_COLORS[17],
                expand=False
            )
            yield Static(welcome_panel, classes="message")
        # Status bar above input
        with Horizontal(id="status_bar"):
            yield Static("", id="status_indicator")
        # Permission area (initially hidden)
        with Vertical(id="permission_area"):
            yield Static("", id="permission_message")
            yield OptionList(
                "1. Yes",
                "2. Yes, and don't ask again this session", 
                "3. No, and tell Claude what to do differently",
                id="permission_options"
            )
        
        # Command palette (initially hidden)
        with Vertical(id="command_palette"):
            yield Static("Command Palette - Select an option:", id="command_palette_message")
            yield OptionList(
                "/host <url> - Set LLM host URL",
                "/provider - Switch LLM provider",
                "/think - Enable thinking mode", 
                "/no-think - Disable thinking mode",
                "/status - Show current configuration",
                "/clear - Clear conversation history",
                id="command_options"
            )
        
        # Input area at bottom
        with Horizontal(id="input_area"):
            yield Label("> ")
            yield Input(placeholder="Type your message here...", compact=True, value="create todo and then task: websearch for latest AI news and then fetch the first URL to summarize")
        # Footer
        with Horizontal(id="footer"):
            yield Static("", id="footer-left")
            yield Static(self.get_mode_display(), id="footer-right")



    def on_ready(self) -> None:
        """Called when the app is ready - focus the input"""
        self.query_one(Input).focus()
        self.theme="gruvbox"
        # Hide permission area initially
        self.query_one("#permission_area").display = False
        # Hide command palette initially
        self.query_one("#command_palette").display = False
        
        # Set initial mode styling (default has no class, so no color)
        footer_right = self.query_one("#footer-right")
        if self.permission_mode == 'auto-accept-edits':
            footer_right.add_class("mode-auto-edit")
        
        # Initialize left footer content
        self.update_left_footer("[grey]  ? for shortcuts[/grey]")

    def on_key(self, event) -> None:
        """Handle key events for command palette"""
        # Only show command palette if we're not waiting for permission and input is focused
        if (event.character == "/" and 
            not self.waiting_for_permission and 
            not self.waiting_for_command and 
            self.query_one(Input).has_focus):
            # Clear input field to prevent "/" from being typed
            self.query_one(Input).clear()
            self.show_command_palette()
            event.prevent_default()
        # Handle escape to hide command palette
        elif event.key == "escape" and self.waiting_for_command:
            self.hide_command_palette()
            event.prevent_default()

    @on(OptionList.OptionSelected, "#permission_options")
    def handle_permission_choice(self, event: OptionList.OptionSelected) -> None:
        """Handle permission choice from OptionList"""
        choice_index = event.option_index
        
        # Check if we're in edit confirmation mode
        if self.waiting_for_edit_confirmation:
            self.handle_edit_confirmation_choice(choice_index)
            return
        
        if choice_index == 0:  # Yes
            self.hide_permission_widget()
            self.call_later(self.execute_pending_tool)
        elif choice_index == 1:  # Yes, and don't ask again
            if self.pending_tool_call:
                tool_name = self.pending_tool_call.function.name
                self.auto_approve_tools.add(tool_name)
            self.hide_permission_widget()
            self.call_later(self.execute_pending_tool)
        elif choice_index == 2:  # No
            self.hide_permission_widget()
            # Add user message asking what to do instead
            self.conversation_history.append({
                "role": "user",
                "content": f"I don't want you to execute the {self.pending_tool_call.function.name} tool. Please suggest an alternative approach or ask me what you should do instead."
            })
            chat_area = self.query_one("#chat_area")
            chat_area.mount(Static(f"\n> I don't want you to execute the {self.pending_tool_call.function.name} tool. Please suggest an alternative.\n", classes="message"))
            self.pending_tool_call = None
            self.call_later(self.start_ai_response, "tool_rejected", self.conversation_history.copy())

    def handle_edit_confirmation_choice(self, choice_index: int):
        """Handle edit confirmation choice"""
        if choice_index == 0:  # Apply edit
            self.call_later(self.apply_pending_edit)
        elif choice_index == 1:  # Discard edit
            self.call_later(self.discard_pending_edit)
        elif choice_index == 2:  # Show full diff
            self.show_full_diff()
            return  # Don't hide permission widget yet
        
        self.hide_permission_widget()

    async def apply_pending_edit(self):
        """Apply the pending edit"""
        try:
            # Apply the edit
            apply_result = await tools_dict['apply_edit']()
            
            # Complete the tool execution with success
            diff_content = self.pending_edit_result.get('diff', '')
            result_text = f"Applied edit - {self.pending_edit_result.get('replacements', 0)} replacement(s)"
            
            self.complete_tool_execution(self.pending_edit_tool_id, self.pending_edit_tool_args, result_text, diff_content)
            
            # Clear pending edit state
            self.clear_edit_confirmation_state()
            
        except Exception as e:
            # Complete with error
            self.complete_tool_execution(self.pending_edit_tool_id, self.pending_edit_tool_args, f"Error applying edit: {str(e)}")
            self.clear_edit_confirmation_state()

    async def discard_pending_edit(self):
        """Discard the pending edit"""
        try:
            # Discard the edit
            discard_result = await tools_dict['discard_edit']()
            
            # Complete the tool execution with discard message
            result_text = f"Edit discarded - {self.pending_edit_result.get('replacements', 0)} replacement(s) not applied"
            self.complete_tool_execution(self.pending_edit_tool_id, self.pending_edit_tool_args, result_text)
            
            # Clear pending edit state
            self.clear_edit_confirmation_state()
            
        except Exception as e:
            # Complete with error
            self.complete_tool_execution(self.pending_edit_tool_id, self.pending_edit_tool_args, f"Error discarding edit: {str(e)}")
            self.clear_edit_confirmation_state()

    def show_full_diff(self):
        """Show the full diff in chat area"""
        from rich.syntax import Syntax
        from rich.panel import Panel
        
        chat_area = self.query_one("#chat_area")
        full_diff = self.pending_edit_result.get('diff', '')
        
        if full_diff.strip():
            # Create syntax highlighted full diff
            diff_syntax = Syntax(full_diff, "diff", theme="monokai", line_numbers=False, word_wrap=True)
            diff_panel = Panel(
                diff_syntax,
                title="Full Diff",
                border_style="cyan",
                expand=False
            )
            diff_widget = Static(diff_panel, classes="message")
            chat_area.mount(diff_widget)
        else:
            chat_area.mount(Static("\nNo diff content available.\n", classes="message"))
        
        # Scroll to end
        self.call_after_refresh(lambda: chat_area.scroll_end(animate=False))

    def clear_edit_confirmation_state(self):
        """Clear edit confirmation state"""
        self.waiting_for_edit_confirmation = False
        self.pending_edit_result = None
        self.pending_edit_tool_id = None
        self.pending_edit_tool_args = None

    @on(OptionList.OptionSelected, "#command_options")
    def handle_command_choice(self, event: OptionList.OptionSelected) -> None:
        """Handle command choice from command palette"""
        choice_index = event.option_index
        self.hide_command_palette()
        
        if choice_index == 0:  # /host <url>
            # For now, show a message that this needs manual input
            chat_area = self.query_one("#chat_area")
            chat_area.mount(Static("\n> Use /host <url> in the input to set host URL\n", classes="message"))
        elif choice_index == 1:  # /provider
            self.show_provider_selection()
        elif choice_index == 2:  # /think
            self.toggle_think_mode(True)
        elif choice_index == 3:  # /no-think  
            self.toggle_think_mode(False)
        elif choice_index == 4:  # /status
            self.show_status()
        elif choice_index == 5:  # /clear
            self.clear_conversation()

    def action_cycle_mode(self) -> None:
        """Action to cycle through modes"""
        self.cycle_mode()

    def action_clear_input(self) -> None:
        """Action to clear the input field"""
        input_widget = self.query_one(Input)
        if input_widget.has_focus:
            input_widget.clear()

    def action_interrupt_conversation(self) -> None:
        """Action to interrupt the conversation"""
        self.state.user_interrupt = True
        status_indicator = self.query_one("#status_indicator")
        chat_area = self.query_one("#chat_area")

        # Clear status indicator immediately
        status_indicator.update("")

        # Clear any pending tool states
        self.pending_tool_call = None
        self.pending_agentic_state = None
        self.tool_widgets.clear()
        
        # Add interrupt message to chat
        chat_area.mount(Static("\n⚠ Conversation interrupted by user\n", classes="message"))
        self.call_after_refresh(lambda: chat_area.scroll_end(animate=False))

    def action_clear_screen(self) -> None:
        """Action to clear the screen but keep conversation history"""
        chat_area = self.query_one("#chat_area")
        
        # Clear all widgets from chat area
        for widget in chat_area.children:
            widget.remove()
        
        # Add welcome message back
        from rich.panel import Panel
        from rich.text import Text
        from claude.core.utils import ORANGE_COLORS
        
        welcome_panel = Panel(
            renderable=Text.from_markup(f"[{ORANGE_COLORS[17]}]✻ [/][bold]Welcome to [/][bold white]Claude Code[/]!\n\n"
                             f"/help for help, /status for your current setup\n\ncwd: {self.cwd}"),
            border_style=ORANGE_COLORS[17],
            expand=False
        )
        chat_area.mount(Static(welcome_panel, classes="message"))
        
        # Scroll to end
        self.call_after_refresh(lambda: chat_area.scroll_end(animate=False))

    def action_previous_command(self) -> None:
        """Action to navigate to previous command in history"""
        input_widget = self.query_one(Input)
        if not input_widget.has_focus or not self.command_history:
            return
        
        if self.history_index == -1:
            # Store current input before navigating history
            self.current_input_backup = input_widget.value
            self.history_index = len(self.command_history) - 1
        elif self.history_index > 0:
            self.history_index -= 1
        
        if 0 <= self.history_index < len(self.command_history):
            input_widget.value = self.command_history[self.history_index]
            input_widget.cursor_position = len(input_widget.value)

    def action_next_command(self) -> None:
        """Action to navigate to next command in history"""
        input_widget = self.query_one(Input)
        if not input_widget.has_focus or not self.command_history or self.history_index == -1:
            return
        
        if self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            input_widget.value = self.command_history[self.history_index]
        else:
            # Restore original input or clear
            input_widget.value = getattr(self, 'current_input_backup', '')
            self.history_index = -1
            self.current_input_backup = ''
        
        input_widget.cursor_position = len(input_widget.value)

    @on(Input.Submitted)
    def handle_message(self, event: Input.Submitted) -> None:
        """Handle when user submits a message"""
        # Don't process input if waiting for permission or command
        if self.waiting_for_permission or self.waiting_for_command:
            return
            
        query = event.value.strip()
        if query:  # Only process non-empty messages
            # Add to command history (avoid duplicates)
            if not self.command_history or self.command_history[-1] != query:
                self.command_history.append(query)
                # Limit history size
                if len(self.command_history) > 100:
                    self.command_history.pop(0)
            
            # Reset history navigation
            self.history_index = -1
            self.current_input_backup = ''
            
            # Handle command shortcuts
            if query.startswith("/host "):
                host_url = query[6:].strip()
                config.set_host(host_url)
                chat_area = self.query_one("#chat_area")
                chat_area.mount(Static(f"\n✓ Host set to: {config.get_host_display()}\n", classes="message"))
                # Reinitialize LLM with new host
                self.llm = self._initialize_llm()
                event.input.clear()
                self.call_after_refresh(lambda: chat_area.scroll_end(animate=False))
                return
            elif query == "/think":
                self.toggle_think_mode(True)
                event.input.clear()
                return
            elif query == "/no-think":
                self.toggle_think_mode(False)
                event.input.clear()
                return
            elif query == "/status":
                self.show_status()
                event.input.clear()
                return
            elif query == "/clear":
                self.clear_conversation()
                event.input.clear()
                return
            elif query == "/provider":
                self.show_provider_selection()
                event.input.clear()
                return
            elif query.startswith("/provider "):
                provider_name = query[10:].strip()
                self.switch_provider(provider_name)
                event.input.clear()
                return
            # Add user message to conversation history
            self.conversation_history.append({
                "role": "user", 
                "content": query
            })
            
            # Add the message to chat area
            chat_area = self.query_one("#chat_area")
            chat_area.mount(Static(f"\n> {query}\n", classes="message"))
            # Clear the input
            event.input.clear()

            chat_area.scroll_end(animate=False)
            self.refresh()
            # Reset interrupt flag for new conversation
            self.state.user_interrupt = False
            self.call_later(self.start_ai_response, query, self.conversation_history.copy())

    def show_permission_widget(self, tool_call):
        """Show permission widget and hide input"""
        self.pending_tool_call = tool_call
        self.waiting_for_permission = True
        
        # Update permission message
        tool_name = tool_call.function.name
        tool_display_name = self.get_tool_display_name(tool_name)
        
        # Handle arguments that might be string or dict
        if tool_call.function.arguments:
            if isinstance(tool_call.function.arguments, str):
                import json
                try:
                    args_dict = json.loads(tool_call.function.arguments)
                    tool_args = list(args_dict.values())[0] if args_dict else ""
                except (json.JSONDecodeError, IndexError):
                    tool_args = tool_call.function.arguments
            elif isinstance(tool_call.function.arguments, dict):
                tool_args = list(tool_call.function.arguments.values())[0] if tool_call.function.arguments else ""
            else:
                tool_args = str(tool_call.function.arguments)
        else:
            tool_args = ""
        
        permission_msg = self.query_one("#permission_message")
        if tool_name == 'bash_execute':
            permission_msg.update(f"Bash command\n{tool_args}\nDo you want to proceed?")
            # Update option list for bash commands
            option_list = self.query_one("#permission_options")
            option_list.clear_options()
            option_list.add_options([
                "1. Yes",
                f"2. Yes, and don't ask again for rm commands in {self.cwd}",
                "3. No, and tell Claude what to do differently (esc)"
            ])
        else:
            permission_msg.update(f"Do you want to make this edit to {tool_display_name}({tool_args})?")
            # Reset to default options for non-bash tools
            option_list = self.query_one("#permission_options")
            option_list.clear_options()
            option_list.add_options([
                "1. Yes",
                "2. Yes, and don't ask again this session",
                "3. No, and tell Claude what to do differently"
            ])
        
        # Show permission area and hide input
        self.query_one("#permission_area").display = True
        self.query_one("#input_area").display = False
        
        # Focus option list and highlight first option
        option_list = self.query_one("#permission_options")
        option_list.focus()
        option_list.highlighted = 0

    def show_edit_confirmation(self, edit_result: dict, tool_id: str, tool_args: str):
        """Show edit confirmation with diff after tool execution"""
        from rich.syntax import Syntax
        from rich.panel import Panel
        
        self.pending_edit_result = edit_result
        self.pending_edit_tool_id = tool_id
        self.pending_edit_tool_args = tool_args
        self.waiting_for_edit_confirmation = True
        
        # Format the diff for display
        diff_content = edit_result.get('diff', '')
        replacements = edit_result.get('replacements', 0)
        file_path = edit_result.get('file_path', '')
        
        # Create the permission message with syntax highlighted diff
        permission_text = f"Edit ready for {file_path} ({replacements} replacement(s))\n\nApply this edit?"
        
        # Show diff in a nice panel in the chat area first
        chat_area = self.query_one("#chat_area")
        if diff_content.strip():
            # Truncate very long diffs for the permission area
            display_diff = diff_content
            if len(diff_content) > 1000:
                diff_lines = diff_content.split('\n')
                if len(diff_lines) > 25:
                    display_diff = '\n'.join(diff_lines[:25]) + f"\n... ({len(diff_lines) - 25} more lines)"
            
            # Create syntax highlighted diff
            diff_syntax = Syntax(display_diff, "diff", theme="monokai", line_numbers=False, word_wrap=True)
            diff_panel = Panel(
                diff_syntax,
                title="Edit Preview",
                border_style="yellow",
                expand=False
            )
            diff_widget = Static(diff_panel, classes="message")
            chat_area.mount(diff_widget)
            
            # Scroll to show the diff
            chat_area.scroll_end(animate=False)
        
        # Update permission message (without the diff content)
        permission_msg = self.query_one("#permission_message")
        permission_msg.update(permission_text)
        
        # Set edit confirmation options
        option_list = self.query_one("#permission_options")
        option_list.clear_options()
        option_list.add_options([
            "1. Apply edit",
            "2. Discard edit", 
            "3. Show full diff"
        ])
        
        # Show permission area and hide input
        self.query_one("#permission_area").display = True
        self.query_one("#input_area").display = False
        
        # Focus option list and highlight first option
        option_list.focus()
        option_list.highlighted = 0

    def hide_permission_widget(self):
        """Hide permission widget and show input"""
        self.waiting_for_permission = False
        self.waiting_for_edit_confirmation = False
        self.query_one("#permission_area").display = False
        self.query_one("#input_area").display = True
        self.query_one(Input).focus()

    def show_command_palette(self):
        """Show command palette and hide input"""
        self.waiting_for_command = True
        
        # Update command options with current state
        command_options = self.query_one("#command_options")
        thinking_status = "enabled" if config.thinking_enabled else "disabled"
        
        command_options.clear_options()
        command_options.add_options([
            f"/host <url> - Set LLM host (current: {config.get_host_display()})",
            f"/provider - Switch provider (current: {config.get_provider_display()})",
            f"/think - Enable thinking (current: {thinking_status})", 
            f"/no-think - Disable thinking (current: {thinking_status})",
            f"/status - Show configuration",
            f"/clear - Clear conversation history"
        ])
        
        # Show command palette and hide input
        self.query_one("#command_palette").display = True
        self.query_one("#input_area").display = False
        
        # Focus command options and highlight first option
        command_options.focus()
        command_options.highlighted = 0

    def hide_command_palette(self):
        """Hide command palette and show input"""
        self.waiting_for_command = False
        self.query_one("#command_palette").display = False
        self.query_one("#input_area").display = True
        self.query_one(Input).focus()

    def _initialize_llm(self):
        """Initialize LLM based on current provider configuration"""
        provider_config = config.get_current_config()
        
        if config.provider == "google":
            api_key = provider_config.get("api_key", "")
            model = provider_config.get("model", "gemini-2.5-flash")
            return OAI(provider="google", api_key=api_key, model=model)
        elif config.provider == "ollama":
            base_url = provider_config.get("host", "http://localhost:11434/v1")
            model = provider_config.get("model", "qwen3:4b")
            return OAI(provider="ollama", base_url=base_url, model=model)
        elif config.provider == "openrouter":
            api_key = provider_config.get("api_key", "")
            model = provider_config.get("model", "google/gemini-2.0-flash-exp:free")
            return OAI(provider="openrouter", api_key=api_key, model=model)
        elif config.provider == "vllm":
            base_url = provider_config.get("base_url", "http://localhost:8000/v1")
            model = provider_config.get("model", None)
            return OAI(provider="vllm", base_url=base_url, model=model)
        else:
            # Default fallback to Google
            api_key = provider_config.get("api_key", "")
            model = provider_config.get("model", "gemini-2.5-flash")
            return OAI(provider="google", api_key=api_key, model=model)

    def show_provider_selection(self):
        """Show provider selection dialog"""
        chat_area = self.query_one("#chat_area")
        
        # Create provider status message
        current_provider = config.provider
        current_config = config.get_current_config()
        
        status_lines = [
            f"\n📡 Current Provider: {config.get_provider_display()}",
            f"Configuration: {current_config}",
            "\nAvailable providers:",
            "  • google - Google Generative AI (Gemini models)",
            "  • ollama - Local Ollama server",
            "  • openrouter - OpenRouter API (multiple models)",
            "  • vllm - Local vLLM server",
            "\nUse: /provider <name> to switch (e.g., /provider google)\n"
        ]
        
        chat_area.mount(Static("\n".join(status_lines), classes="message"))
        self.call_after_refresh(lambda: chat_area.scroll_end(animate=False))

    def switch_provider(self, provider_name: str):
        """Switch to a different LLM provider"""
        chat_area = self.query_one("#chat_area")
        
        try:
            # Set the new provider
            config.set_provider(provider_name)
            
            # Reinitialize LLM with new provider
            self.llm = self._initialize_llm()
            
            current_config = config.get_current_config()
            chat_area.mount(Static(
                f"\n✓ Switched to {config.get_provider_display()} provider\n"
                f"Configuration: {current_config}\n", 
                classes="message"
            ))
            
        except ValueError as e:
            chat_area.mount(Static(f"\n❌ {str(e)}\n", classes="message"))
        except Exception as e:
            chat_area.mount(Static(f"\n❌ Error switching provider: {str(e)}\n", classes="message"))
        
        self.call_after_refresh(lambda: chat_area.scroll_end(animate=False))

    def toggle_think_mode(self, enable_thinking: bool):
        """Toggle thinking mode on/off by updating system prompt"""
        chat_area = self.query_one("#chat_area")
        
        # Update config
        config.thinking_enabled = enable_thinking
        
        # Update conversation history with new system prompt
        self.conversation_history[0] = {
            "role": "system",
            "content": self.get_system_prompt()
        }
        
        # Show feedback message
        if enable_thinking:
            chat_area.mount(Static("\n✓ Thinking mode enabled\n", classes="message"))
        else:
            chat_area.mount(Static("\n✓ Thinking mode disabled\n", classes="message"))
        
        # Scroll to end
        self.call_after_refresh(lambda: chat_area.scroll_end(animate=False))

    def show_status(self):
        """Show current configuration status"""
        chat_area = self.query_one("#chat_area")
        
        thinking_status = "enabled" if hasattr(config, 'thinking_enabled') and config.thinking_enabled else "disabled"
        status_text = f"""
Current Configuration:
- Host: {config.get_host_display()}
- Model: {config.model}
- Context: {config.num_ctx}
- Thinking: {thinking_status}
- Permission Mode: {self.permission_mode}
"""
        chat_area.mount(Static(status_text, classes="message"))
        
        # Scroll to end
        self.call_after_refresh(lambda: chat_area.scroll_end(animate=False))

    def clear_conversation(self):
        """Clear conversation history, chat area, and todos"""
        chat_area = self.query_one("#chat_area")
        
        # Clear all widgets from chat area
        for widget in chat_area.children:
            widget.remove()
        
        # Reset conversation history to just system prompt
        self.conversation_history = [
            {"role": "system", "content": self.get_system_prompt()}
        ]
        
        # Clear todos by calling the clear_todos tool
        try:
            self.call_later(self.clear_todos_async)
        except Exception as e:
            logger.error(f"Failed to clear todos: {e}")
        
        # Generate new session ID for fresh start
        import uuid
        self.session_id = str(uuid.uuid4())
        
        # Add welcome message back
        welcome_panel = Panel(
            renderable=Text.from_markup(f"[{ORANGE_COLORS[17]}]✻ [/][bold]Welcome to [/][bold white]Claude Code[/]!\n\n"
                             f"/help for help, /status for your current setup\n\ncwd: {self.cwd}"),
            border_style=ORANGE_COLORS[17],
            expand=False
        )
        chat_area.mount(Static(welcome_panel, classes="message"))
        
        # Add confirmation message
        chat_area.mount(Static("\n✓ Conversation and todos cleared\n", classes="message"))
        
        # Scroll to end
        self.call_after_refresh(lambda: chat_area.scroll_end(animate=False))

    async def clear_todos_async(self):
        """Async helper to clear todos for current session"""
        try:
            from claude.tools import tools_dict
            if 'todo_write' in tools_dict:
                # Clear by writing empty list - session-based approach
                await tools_dict['todo_write'](todos=[], session_id=self.session_id)
        except Exception as e:
            logger.error(f"Failed to clear todos: {e}")

    def get_tool_display_name(self, tool_name):
        """Get user-friendly display name for tools"""
        tool_names = {
            'read_file': 'Read',
            'write_file': 'Write', 
            'edit_file': 'Edit',
            'multi_edit_file': 'Multi Edit',
            'bash_execute': 'Bash',
            'glob_find_files': 'Glob',
            'grep_search': 'Grep',
            'list_directory': 'LS',
            'fetch_url': 'Web Fetch',
            'web_search': 'Web Search',
            'todo_read': 'Todo Read',
            'todo_write': 'Update Todos',
            'apply_edit': 'Apply Edit',
            'discard_edit': 'Discard Edit'
        }
        return tool_names.get(tool_name, tool_name.replace('_', ' ').title())

    def get_system_prompt(self):
        """Get the appropriate system prompt based on current mode"""
        if self.permission_mode == 'plan-mode':
            base_prompt = PLAN_MODE_PROMPT.format(cwd=self.cwd)
        else:
            base_prompt = DEFAULT_MODE_PROMPT.format(cwd=self.cwd)
        
        # Add /no_think token when thinking is disabled
        if not config.thinking_enabled:
            base_prompt += "/no_think"
        
        return base_prompt

    def get_mode_display(self):
        """Get the display text and style for current mode"""
        if self.permission_mode == 'default':
            return ""
        elif self.permission_mode == 'auto-accept-edits':
            return "⏵⏵ auto-accept edits on   "
        elif self.permission_mode == 'bypass-permissions':
            return "Bypassing Permissions   "
        elif self.permission_mode == 'plan-mode':
            return "⏸ plan mode on   "

    def update_left_footer(self, new_content: str):
        """Update the left footer content dynamically"""
        footer_left = self.query_one("#footer-left")
        footer_left.update(new_content)
        
    def cycle_mode(self):
        """Cycle to the next permission mode"""
        self.current_mode_index = (self.current_mode_index + 1) % len(self.modes)
        old_mode = self.permission_mode
        self.permission_mode = self.modes[self.current_mode_index]
        
        # Update footer
        footer_right = self.query_one("#footer-right")
        footer_right.update(self.get_mode_display())
        
        # Remove all mode classes and add the current one
        footer_right.remove_class("mode-bypass", "mode-plan", "mode-auto-edit")
        if self.permission_mode == 'bypass-permissions':
            footer_right.add_class("mode-bypass")
        elif self.permission_mode == 'plan-mode':
            footer_right.add_class("mode-plan")
        elif self.permission_mode == 'auto-accept-edits':
            footer_right.add_class("mode-auto-edit")
        
        # Update system prompt in conversation history if mode changed
        if old_mode != self.permission_mode:
            self.conversation_history[0] = {
                "role": "system", 
                "content": self.get_system_prompt()
            }

    def needs_permission(self, tool_name):
        """Check if a tool needs permission based on current mode"""
        if self.permission_mode == 'bypass-permissions':
            return False
        elif self.permission_mode == 'plan-mode':
            return True  # Plan mode doesn't use tools, so always ask
        elif self.permission_mode == 'auto-accept-edits':
            # Auto-approve read/list/edit tools, ask for others
            if tool_name in self.no_permission_tools or tool_name in self.auto_accept_edit_tools:
                return False
            return tool_name not in self.auto_approve_tools
        else:  # default mode
            # Only read_file and list_directory don't need permission
            if tool_name in self.no_permission_tools:
                return False
            return tool_name not in self.auto_approve_tools

    async def execute_pending_tool(self):
        """Execute the pending tool after permission is granted"""
        if self.pending_tool_call:
            tool_call = self.pending_tool_call
            tool_display_name = self.get_tool_display_name(tool_call.function.name)
            tool_args = self._extract_tool_args(tool_call.function.arguments, tool_call.function.name)
            tool_id = f"{tool_call.function.name}_{id(tool_call)}"
            
            # Create tool widget with animation
            await self.create_tool_widget(tool_display_name, tool_args, tool_id)
            
            # Execute the actual tool
            result = await self.execute_tool_and_get_result(tool_call, tool_id, tool_args)
            
            # Give time for user to see the tool completion
            await asyncio.sleep(0.1)
            
            # Clear pending tool
            self.pending_tool_call = None
            
            # Check if we need to resume agentic loop
            if self.pending_agentic_state:
                # Add tool result to the pending state messages
                self.pending_agentic_state['messages'].append({
                    'role': 'tool',
                    'content': str(result),
                    'tool_call_id': tool_call.id,
                    'name': tool_call.function.name
                })
                
                # Resume agentic loop
                state = self.pending_agentic_state
                self.pending_agentic_state = None
                await self.agentic_loop(
                    state['query'], 
                    state['messages'], 
                    state['max_iterations'] - state['iteration']
                )
            else:
                # Legacy single tool execution - add to conversation history
                self.conversation_history.append({
                    'role': 'tool',
                    'content': str(result),
                    'tool_call_id': tool_call.id,
                    'name': tool_call.function.name
                })
                
                # Continue with single LLM response
                self.call_later(self.continue_ai_response)

    async def continue_ai_response(self):
        """Continue AI response after tool execution"""
        # Make another LLM call with tool results
        animation_task = asyncio.create_task(self.animate_thinking_status("tool_result", "Processing tool results..."))
        
        loop = asyncio.get_event_loop()
        # Pass no tools in plan mode
        tools_to_use = None if self.permission_mode == 'plan-mode' else tools
        final_response = await loop.run_in_executor(None, lambda: self.llm.run(messages=self.conversation_history, model=config.model, tools=tools_to_use, max_tokens=config.num_ctx))
        
        # Stop thinking animation
        animation_task.cancel()
        try:
            await animation_task
        except asyncio.CancelledError:
            pass
        
        # Display the final response
        if final_response.choices[0].message.content and final_response.choices[0].message.content.strip():
            # Remove thinking content before displaying
            clean_content = self.remove_thinking_content(final_response.choices[0].message.content)
            if clean_content.strip():
                # Use rich Markdown for better rendering
                markdown_content = Markdown("● " + clean_content.strip())
                markdown_widget = Static(markdown_content, classes="ai-response")
                chat_area = self.query_one("#chat_area")
                chat_area.mount(markdown_widget)
                
                # Add assistant response to conversation history
                self.conversation_history.append({
                    "role": "assistant",
                    "content": clean_content.strip()
                })
        
        # Reset status
        status_indicator = self.query_one("#status_indicator")
        status_indicator.update("")
        
        # Ensure scroll to end
        chat_area = self.query_one("#chat_area")
        self.call_after_refresh(lambda: chat_area.scroll_end(animate=False))

    async def start_ai_response(self, query: str, messages: list):
        """Start AI response with proper agentic loop for tool calling"""
        chat_area = self.query_one("#chat_area")
        status_indicator = self.query_one("#status_indicator")
        
        # Start agentic loop
        await self.agentic_loop(query, messages.copy())
        
        # Reset status to empty
        status_indicator.update("")

    async def agentic_loop(self, query: str, messages: list, max_iterations: int = 25):
        """Main agentic loop that continues until no tool calls or max iterations"""
        chat_area = self.query_one("#chat_area")
        iteration = 0
        
        try:
            while iteration < max_iterations and not self.state.user_interrupt:
                iteration += 1
                
                # Check for interrupt before LLM call
                if self.state.user_interrupt:
                    break
                
                # Make LLM call
                animation_task = asyncio.create_task(
                    self.animate_thinking_status(query, "Generating response...")
                )
                
                try:
                    loop = asyncio.get_event_loop()
                    tools_to_use = None if self.permission_mode == 'plan-mode' else tools
                    response = await loop.run_in_executor(
                        None, 
                        lambda: self.llm.run(
                            messages=messages, 
                            model=config.model, 
                            max_tokens=config.num_ctx, 
                            tools=tools_to_use
                        )
                    )
                    
                    # Check interrupt immediately after LLM call
                    if self.state.user_interrupt:
                        break
                        
                except Exception as e:
                    # If interrupted during LLM call, just break
                    if self.state.user_interrupt:
                        break
                    raise e
                finally:
                    # Stop thinking animation
                    animation_task.cancel()
                    try:
                        await animation_task
                    except asyncio.CancelledError:
                        pass
                
                # Add assistant response to conversation
                assistant_msg = {
                    "role": "assistant",
                    "content": response.choices[0].message.content
                }
                if response.choices[0].message.tool_calls:
                    assistant_msg["tool_calls"] = response.choices[0].message.tool_calls
                messages.append(assistant_msg)
                
                # Check for interrupt after LLM response
                if self.state.user_interrupt:
                    break
                
                # Check if there are tool calls
                if response.choices[0].message.tool_calls:
                    # Execute all tool calls
                    tool_results = await self.execute_all_tools(response.choices[0].message.tool_calls)
                    
                    # Check for interrupt after tool execution
                    if self.state.user_interrupt:
                        break
                    
                    # If any tool needs permission and user hasn't granted it yet, stop here
                    if any(result.get('needs_permission') for result in tool_results):
                        # Store state for resuming later
                        self.pending_agentic_state = {
                            'query': query,
                            'messages': messages,
                            'iteration': iteration,
                            'max_iterations': max_iterations
                        }
                        return
                    
                    # Add tool results to conversation
                    for tool_result in tool_results:
                        if 'tool_call_id' in tool_result:
                            messages.append({
                                'role': 'tool',
                                'content': str(tool_result['result']),
                                'tool_call_id': tool_result['tool_call_id'],
                                'name': tool_result['tool_name']
                            })
                    
                    # Continue loop for next iteration
                    continue
                else:
                    # No tool calls - display final response and exit loop
                    if response.choices[0].message.content and response.choices[0].message.content.strip():
                        clean_content = self.remove_thinking_content(response.choices[0].message.content)
                        if clean_content.strip():
                            markdown_content = Markdown("● " + clean_content.strip())
                            markdown_widget = Static(markdown_content, classes="ai-response")
                            chat_area.mount(markdown_widget)
                            
                            # Update conversation history
                            self.conversation_history = messages
                    break
            
            # Max iterations reached
            if iteration >= max_iterations:
                chat_area.mount(Static(f"\n⚠ Max iterations ({max_iterations}) reached. Stopping agent loop.\n", classes="message"))
                
        except Exception as e:
            error_text = f"🤖 **Error in agentic loop**: {str(e)}"
            chat_area.mount(Static(error_text, classes="ai-response"))
        
        # Only update conversation history if not interrupted
        if not self.state.user_interrupt:
            self.conversation_history = messages
        
        self.call_after_refresh(lambda: chat_area.scroll_end(animate=False))

    async def execute_all_tools(self, tool_calls):
        """Execute all tool calls and return results"""
        results = []
        chat_area = self.query_one("#chat_area")
        
        for tc in tool_calls:
            # Check for interrupt before each tool
            if self.state.user_interrupt:
                return results
                
            tool_name = tc.function.name
            
            # Check if tool needs permission
            if self.needs_permission(tool_name):
                # Show permission widget and wait for user decision
                self.show_permission_widget(tc)
                results.append({'needs_permission': True, 'tool_call': tc})
                return results  # Stop here and wait for permission
            
            # Execute tool without permission
            tool_display_name = self.get_tool_display_name(tc.function.name)
            tool_args = self._extract_tool_args(tc.function.arguments, tc.function.name)
            tool_id = f"{tc.function.name}_{id(tc)}"
            
            # Create tool widget and make sure it's visible
            await self.create_tool_widget(tool_display_name, tool_args, tool_id)
            
            # Force immediate UI update and scroll
            chat_area.scroll_end(animate=False)
            self.refresh()
            
            # Small delay to show tool starting
            await asyncio.sleep(0.2)
            
            # Execute tool
            result = await self.execute_tool_and_get_result(tc, tool_id, tool_args)
            
            # Force UI update after tool completion
            chat_area.scroll_end(animate=False)
            self.refresh()
            
            # Give time for user to see completion before next tool
            await asyncio.sleep(0.3)
            
            results.append({
                'result': result,
                'tool_call_id': tc.id,
                'tool_name': tc.function.name,
                'needs_permission': False
            })
        
        return results

    def _extract_tool_args(self, arguments, tool_name=None):
        """Extract tool arguments for display"""
        # Don't show arguments for todo tools - they're too verbose
        if tool_name and tool_name.startswith('todo_'):
            return ""
            
        if arguments:
            if isinstance(arguments, str):
                import json
                try:
                    args_dict = json.loads(arguments)
                    return list(args_dict.values())[0] if args_dict else ""
                except (json.JSONDecodeError, IndexError):
                    return arguments
            elif isinstance(arguments, dict):
                return list(arguments.values())[0] if arguments else ""
            else:
                return str(arguments)
        return ""
    
    async def create_tool_widget(self, tool_name: str, tool_args: str, tool_id: str):
        """Create a widget for tool execution"""
        from rich.text import Text
        chat_area = self.query_one("#chat_area")
        status_indicator = self.query_one("#status_indicator")
        
        # Create rich text with grey dot and bold tool name
        tool_text = Text()
        tool_text.append("● ", style="bright_black")
        tool_text.append(tool_name.title(), style="bold")
        if tool_args:
            tool_text.append(f"({tool_args})", style="default")
        
        tool_widget = Static(tool_text, classes="tool-executing")
        chat_area.mount(tool_widget)
        self.tool_widgets[tool_id] = tool_widget
        
        # Update status bar to show tool progress
        status_indicator.update(f"● Executing {tool_name.title()}...")
        
        # Force scroll to end immediately and refresh
        chat_area.scroll_end(animate=False)
        self.refresh()
        # Also schedule for after refresh as backup
        self.call_after_refresh(lambda: chat_area.scroll_end(animate=False))
    
    async def execute_tool_and_get_result(self, tool_call, tool_id: str, tool_args: str):
        """Execute the actual tool and return the result"""
        try:
            # Check for interrupt before executing
            if self.state.user_interrupt:
                return "Interrupted by user"
                
            tool_name = tool_call.function.name
            
            # Get the tool method from the tools dictionary
            if tool_name in tools_dict:
                tool_method = tools_dict[tool_name]
                
                # Handle arguments that might be string or dict
                if isinstance(tool_call.function.arguments, str):
                    import json
                    try:
                        args_dict = json.loads(tool_call.function.arguments)
                        # Check interrupt before tool execution
                        if self.state.user_interrupt:
                            return "Interrupted by user"
                        result = await tool_method(**args_dict)
                    except json.JSONDecodeError:
                        result = f"Error: Invalid JSON arguments: {tool_call.function.arguments}"
                elif isinstance(tool_call.function.arguments, dict):
                    # Check interrupt before tool execution
                    if self.state.user_interrupt:
                        return "Interrupted by user"
                    result = await tool_method(**tool_call.function.arguments)
                else:
                    # Check interrupt before tool execution
                    if self.state.user_interrupt:
                        return "Interrupted by user"
                    result = await tool_method()
                
                # Generate appropriate result text based on tool and result
                if tool_name == "read_file" and isinstance(result, dict) and 'lines' in result:
                    result_text = f"Read {result['lines']} lines"
                elif tool_name == "list_directory":
                    result_text = f"Listed {len(result)} items"
                elif tool_name == "fetch_url" and isinstance(result, dict):
                    # Special handling for WebFetch results
                    if not result.get('success', True):
                        # Failed fetch - use user-friendly error message
                        error_msg = result.get('user_message', result.get('error', 'Unknown error'))
                        result_text = f"Failed: {error_msg}"
                        self.complete_tool_execution(tool_id, tool_args, result_text)
                        return result
                    else:
                        # Successful fetch
                        success_msg = result.get('user_message', f"Fetched {result.get('size', 0)} characters")
                        result_text = success_msg
                        self.complete_tool_execution(tool_id, tool_args, result_text)
                        return result
                elif tool_name == "web_search" and isinstance(result, str):
                    # Special handling for web_search results (returns JSON string)
                    try:
                        import json
                        search_data = json.loads(result)
                        if isinstance(search_data, dict) and search_data.get('error'):
                            # Failed search - use user-friendly error message
                            error_msg = search_data.get('user_message', search_data.get('message', 'Unknown search error'))
                            result_text = f"Failed: {error_msg}"
                            self.complete_tool_execution(tool_id, tool_args, result_text)
                            return result
                        elif isinstance(search_data, list):
                            # Successful search
                            result_text = f"Found {len(search_data)} search results"
                            self.complete_tool_execution(tool_id, tool_args, result_text)
                            return result
                        else:
                            # Unknown format
                            result_text = "Search completed"
                            self.complete_tool_execution(tool_id, tool_args, result_text)
                            return result
                    except (json.JSONDecodeError, TypeError):
                        # Invalid JSON response
                        result_text = "Search completed (invalid response format)"
                        self.complete_tool_execution(tool_id, tool_args, result_text)
                        return result
                elif tool_name == "edit_file" and isinstance(result, dict) and 'diff' in result:
                    # Check if edit is pending application
                    if result.get('pending_application', False):
                        # Show diff and ask for confirmation
                        diff_content = result['diff']
                        self.show_edit_confirmation(result, tool_id, tool_args)
                        return result  # Don't complete tool execution yet
                    else:
                        # Show the diff for completed edit operations
                        diff_content = result['diff']
                        result_text = f"Edited {result.get('replacements', 0)} occurrence(s)"
                        self.complete_tool_execution(tool_id, tool_args, result_text, diff_content)
                        return result
                elif tool_name == "todo_write" and isinstance(result, dict) and 'todos' in result:
                    # Special handling for todo display - show only checkboxes
                    result_text = ""
                    todo_content = self._format_todos_display(result['todos'])
                    self.complete_tool_execution(tool_id, tool_args, result_text, todo_content)
                    return result
                else:
                    result_text = "done"
                    
                self.complete_tool_execution(tool_id, tool_args, result_text)
                return result
            else:
                result_text = f"Unknown tool: {tool_name}"
                self.complete_tool_execution(tool_id, tool_args, result_text)
                return result_text
                
        except Exception as e:
            error_msg = f"error: {str(e)}"
            self.complete_tool_execution(tool_id, tool_args, error_msg)
            return error_msg
    
    def complete_tool_execution(self, tool_id: str, tool_args, result: str = "", diff_content = None):
        """Mark tool execution as completed with green dot"""
        if tool_id in self.tool_widgets:
            from rich.text import Text
            from rich.syntax import Syntax
            widget = self.tool_widgets[tool_id]
            # Extract tool name from tool_id format: {tool_name}_{id}
            tool_name = '_'.join(tool_id.split('_')[:-1])
            tool_info = self.get_tool_display_name(tool_name)
            status_indicator = self.query_one("#status_indicator")
            chat_area = self.query_one("#chat_area")
            
            # Create rich text with green dot and bold tool name, and result on same widget
            tool_text = Text()
            tool_text.append("● ", style="dim #5cf074")
            tool_text.append(tool_info, style="bold")
            if tool_args:
                tool_text.append(f"({tool_args})", style="default")
            
            # Add result text on next line if available
            if result and result.strip():
                tool_text.append(f"\n  ⎿ {result}\n", style="default")

            widget.update(tool_text)
            widget.remove_class("tool-executing")
            widget.add_class("tool-completed")
            
            # Handle different types of diff_content
            if diff_content:
                if isinstance(diff_content, str) and diff_content.strip():
                    # Regular diff content
                    diff_syntax = Syntax(diff_content, "diff", theme="monokai", line_numbers=False, word_wrap=True)
                    diff_widget = Static(diff_syntax, classes="ai-response")
                    chat_area.mount(diff_widget)
                elif hasattr(diff_content, 'append'):
                    # Rich Text object (for todos)
                    todo_widget = Static(diff_content, classes="ai-response")
                    chat_area.mount(todo_widget)
            
            # Force scroll to end immediately and refresh
            chat_area.scroll_end(animate=False)
            self.refresh()
            # Also schedule for after refresh as backup
            self.call_after_refresh(lambda: chat_area.scroll_end(animate=False))
            
            # Clear status bar
            status_indicator.update("")
            
            # Remove from tracking
            del self.tool_widgets[tool_id]

    def _format_todos_display(self, todos):
        """Format todos with checkboxes and color coding in ID order"""
        from rich.text import Text
        
        formatted_todos = Text()
        
        # Sort todos by ID to maintain order
        sorted_todos = sorted(todos, key=lambda x: x.get('id', '0'))
        
        for todo in sorted_todos:
            status = todo.get('status', 'pending')
            content = todo.get('content', '')
            
            # Get checkbox symbol and color based on status
            if status == 'completed':
                checkbox = "☒"
                color = "#5cf074"  # Green
            elif status == 'in_progress':
                checkbox = "☐"
                color = "#b19cd9"  # Lavender/purple
            else:  # pending
                checkbox = "☐"
                color = "#a89984"  # Grey
            
            # Format the todo line
            formatted_todos.append(f"  {checkbox} ", style=color)
            formatted_todos.append(content, style=color)
            formatted_todos.append("\n")
        
        return formatted_todos
    
    def remove_thinking_content(self, content: str) -> str:
        """Remove <think>...</think> content from the response"""
        # Split by </think> and return the last part, properly stripped
        return content.split('</think>')[-1].strip()

    async def animate_thinking_status(self, query: str, base_message: str):
        """Animate the thinking status with flowers and contextual words"""
        import time
        flower_chars = ["✻", "✺", "✵", "✴", "❋", "❊", "❉", "❈", "❇", "❆", "❅", "❄"]
        flower_index = 0
        
        # Generate contextual thinking words based on user input
        thinking_words = get_contextual_thinking_words(query)
        thinking_word_index = 0
        
        status_indicator = self.query_one("#status_indicator")
        chat_area = self.query_one("#chat_area")
        start_time = time.time()
        
        try:
            while True:
                # Check for interrupt
                if self.state.user_interrupt:
                    break
                    
                elapsed_seconds = int(time.time() - start_time)
                flower_index = (flower_index + 1) % len(flower_chars)
                
                # Change thinking word every 5 flower cycles to slow it down
                if flower_index % 5 == 0:
                    thinking_word_index = (thinking_word_index + 1) % len(thinking_words)
                
                current_thinking_word = thinking_words[thinking_word_index]
                
                status_msg = f"{flower_chars[flower_index]} {current_thinking_word} [grey]({elapsed_seconds}s)[/grey]"
                
                status_indicator.update(status_msg)
                
                # Ensure scroll stays at bottom during long operations every few cycles
                if flower_index % 10 == 0:
                    chat_area.scroll_end(animate=False)
                
                await asyncio.sleep(0.3)
        except asyncio.CancelledError:
            status_indicator.update("")
            raise



def main():
    """Main CLI entry point for ceaser command"""
    import sys
    from pathlib import Path
    
    # Use current working directory by default
    cwd = sys.argv[1] if len(sys.argv) > 1 else str(Path.cwd())
    app = ChatApp(cwd)
    app.run()

if __name__ == "__main__":
    main()
