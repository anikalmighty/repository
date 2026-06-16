# GitHub MCP Demo

This folder contains a small demo and guide for understanding GitHub MCP capabilities inside the GitHub Copilot Chat environment.

## Purpose

- Show how to structure a GitHub MCP demo in a repository
- Explain key MCP feature categories
- Provide a local helper script and a walkthrough guide
- Document how to use Copilot Chat tools to inspect and modify repositories

## Contents

- `README.md` - overview of the demo and how to use it
- `demo.py` - local helper script that describes the demo and inspects the workspace
- `mcp_demo_guide.md` - step-by-step walkthrough for using GitHub MCP features
- `demo_notebook.ipynb` - notebook with a lightweight local demo and commentary
- `ui.py` - local browser-based UI for interacting with demo helper functions

## How to use this demo

1. Open this folder in VS Code.
2. Review `mcp_demo_guide.md` for the recommended GitHub MCP flow.
3. Use GitHub Copilot Chat in this workspace to explore the demo and execute MCP tool operations.
4. Run `demo.py` locally to verify the demo artifact layout and workspace context.
5. Run `python ui.py` and open `http://127.0.0.1:8500/` to interact with the UI.

## UI capabilities

The browser UI now supports:

- listing the local demo files
- showing GitHub environment context
- listing repositories for a GitHub owner
- listing open issues for a repository
- showing the latest commit details for a repository
- saving a manifest file

## What GitHub MCP can do

GitHub MCP provides structured tools for repository interactions, such as:

- repository file read/write
- branch listing and branch operations
- issue and pull request inspection
- commit and release metadata access
- secret scanning and search
- authenticated operations via GitHub tooling

## Notes

This demo is written for a workspace-powered GitHub Copilot Chat session. The actual remote GitHub operations are exercised through MCP tool calls, not through the local `demo.py` script.
