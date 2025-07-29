# Nautex

Nautex is a command-line tool and MCP (Multi-Agent Collaboration Protocol) server that integrates the Nautex AI platform with development environments. It acts as a Product and Project manager for coding agents, facilitating AI-assisted software development.

## Installation

```bash
uvx nautex setup
```

## Requirements

- Python 3.10 or higher
- Dependencies: pydantic, aiohttp, textual, fastmcp, python-dotenv, aiofiles

## Features

- **Interactive Setup**: Configure your Nautex integration with a text-based user interface
- **Integration Status**: View the status of your Nautex integration
- **MCP Server**: Run an MCP server for IDE integration, enabling AI agents to:
  - Get project and plan information
  - Retrieve the next development scope
  - Update task statuses and add notes
  - Access project documents and dependencies

## Usage

### Initial Setup

```bash
nautex setup
```

This launches an interactive TUI to configure your Nautex integration.

### Check Status

```bash
nautex status
```

View the current integration status with a TUI, or use `--noui` flag for console output:

```bash
nautex status --noui
```

### Start MCP Server

```bash
nautex mcp
```

Starts the MCP server for IDE integration, allowing AI agents to interact with the Nautex platform.

### Testing MCP Functionality

```bash
nautex mcp test next_scope
```

Tests the next_scope functionality of the MCP server.

## License

MIT
