<div align="center">

# LoopLM

🤖 A powerful tool for seamlessly integrating LLMs in your development workflow

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Documentation](https://img.shields.io/badge/docs-mkdocs-blue)](https://chaitanya.one/looplm)

</div>

---

> [!NOTE]
> LoopLM is in active development. While fully functional, expect frequent updates and improvements.

LoopLM is a highly customisable command line tool that seamlessly integrates various Language Models into your development workflow. It offers a unified, secure, and efficient way to interact with state-of-the-art AI models directly from your terminal.

## Features

- 🚀 **Support for multiple LLM providers**: Works with OpenAI, Anthropic, Google Gemini, Azure OpenAI, AWS Bedrock, and other providers through [LiteLLM](https://litellm.vercel.app/docs/providers) integration. You can easily switch between different providers and models
- 📂 **File Integration**: Include files directly in your prompts using @file directives, supporting code files, logs, configurations, and even PDFs and documents
- 🔒 **Secure Configuration**: All API keys and credentials are stored securely using encryption
- 💻 **Simple CLI**: Intuitive command-line interface for quick access to AI capabilities
- 💬 **Interactive Chat Mode**: Engage in persistent, interactive conversations with your preferred LLM using looplm chat
- 🎨 **Modern TUI**: Full-page Terminal User Interface with real-time streaming, session management, and intuitive controls
- 🔍 **Rich Output**: Beautiful terminal output with markdown support
- 🔍 **Smart Context**: Maintain conversation context and system prompts for consistent interactions

## Quick Start

1. Install LoopLM ([pipx](https://github.com/pypa/pipx) is recommended):
```bash
pipx install looplm
```

2. Configure your first provider:
```bash
looplm --configure
```

3. Start using the CLI with direct file support:
```bash
# Review code with file directive
looplm "Review this code: @file(src/main.py)"

# Compare implementations
looplm "Compare these files: @file(v1.py) vs @file(v2.py)"

# Analyze logs
looplm "Check this log: @file(/var/log/app.log)"
```

4. Start an interactive chat session:
```bash
# Traditional Rich console interface
looplm chat

# New full-page Textual interface (recommended)
looplm chat --ui textual
```

## 🔧 Coding Agent

LoopLM includes a powerful coding agent with specialized tools for software development:

```bash
# Quick setup - run this once to set up the coding agent
./setup_coding_agent.sh

# Then use the coding agent
coding "Analyze the structure of this Python project"
coding "Help me refactor this function to be more efficient"
coding "Find all TODO comments in the codebase"
```

The coding agent provides:
- 📁 **File Operations**: Read, write, copy, and manage files
- 🔍 **Code Analysis**: Find functions, classes, and analyze project structure
- 🔎 **Search Tools**: Grep-like search with regex support
- 📝 **Smart Editing**: Search and replace with safety checks
- 🔀 **Git Integration**: Status, diff, and commit history
- 🖥️ **Shell Access**: Execute commands for testing and building

See [CODING_AGENT.md](CODING_AGENT.md) for detailed setup and usage instructions.

## Why LoopLM?

LoopLM is designed for developers who:
- Want quick access to LLMs without leaving the terminal
- Work with multiple LLM providers and need a unified interface
- Want to integrate LLM assistance into their development workflow
- Need a coding agent that can understand and modify codebases

## Requirements

- Python 3.10 or higher
- API keys for the providers you want to use

## 📖 Documentation

For comprehensive documentation, visit [our documentation site](https://chaitanya.one/looplm).
