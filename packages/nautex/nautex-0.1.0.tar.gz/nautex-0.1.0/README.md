# pre-release todo list

- [ ] test publishing
- [ ] refine publishing
- [ ] check how UV work
- 
- [ ] create makefile
- [ ] test on linux: CLI + Cursor
- [ ] test on mac
- [ ] test on windows

- [ ] manage rules population 
- [ ] manage rule mcp config population

- [ ] cleanup UI
  - [ ] refine status page
  - [ ] refine status message to MCP tool
  - [ ] update actual link for requesting api keys 
   - [ ] make sure auth will work toward project line
   - [ ] rename project: Your First Project
   - [ ] from implementation plan list add link for manual on GH of how to create good plan
    - [ ] step by step screenshots
    - [ ] recommendations and tricks


- [ ] refine readme
 - [ ] now it works graphics
 - [ ] platform screenshots --> separate readme files
 - [ ] Put MIT license
 - [ ] quick start manual
 - [ ] contribution guide
 - [ ] claude code / gemini / codex / windsurf reference
- [ ] create account from scratch workflow
- 


# Nautex CLI

Command-line interface for integrating AI coding agents with the Nautex.ai platform.

## Overview

Nautex CLI provides a bridge between AI-powered IDEs (like Cursor and Windsurf) and the Nautex.ai task and requirements management platform through the Model Context Protocol (MCP).

## Features

- **Interactive Setup**: TUI-based configuration for easy onboarding
- **MCP Integration**: FastMCP server for seamless AI agent communication
- **Task Management**: Retrieve, update, and manage tasks from Nautex.ai
- **Cross-Platform**: Works on macOS, Linux, and Windows

## Installation

```bash
pip install nautex-cli
```

## Quick Start

1. **Setup**: Configure your connection to Nautex.ai
   ```bash
   nautex setup
   ```

2. **Check Status**: View your current configuration
   ```bash
   nautex status
   ```

3. **Run as MCP Server**: For AI agent integration
   ```bash
   nautex mcp
   ```

## Requirements

- Python 3.10+
- Nautex.ai API token

## Development

Install in development mode:

```bash
make install-dev
```

Run linters and formatters:

```bash
make lint
make format
```

## License

MIT License - see LICENSE file for details.

## Contributing

This is an open-source project. Contributions are welcome!

## Support

For issues and questions, please visit our [GitHub repository](https://github.com/nautex-ai/nautex-cli). 
