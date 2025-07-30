# Claude

> A powerful terminal-based chat application with integrated LLM capabilities and extensible tool support.

![img.png](img.png)

## Overview

Claude is a modern TUI (Terminal User Interface) chat application that provides seamless interaction with Large Language Models through Ollama. Built with Python and Textual, it offers a rich, responsive interface for AI-powered conversations with built-in tool integration for enhanced functionality.

## Key Features

- **Rich Terminal Interface**: Modern, responsive TUI built with Textual framework
- **LLM Integration**: Native support for Ollama with multiple model compatibility
- **Extensible Tools**: Built-in file operations and web utilities
- **Async Architecture**: Non-blocking operations for smooth user experience
- **Modular Design**: Clean, maintainable codebase with clear separation of concerns

## Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd claude

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

## Prerequisites

- **Python**: 3.8 or higher
- **Ollama**: Local installation required
- **Dependencies**: textual, ollama, pydantic

## Architecture

```
claude/
├── core/           # Core application components
│   └── components/ # UI components and layouts
├── llm/           # Language model integrations
└── tools/         # Utility and tool implementations
```

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## License

This project is open source and available under the MIT License.