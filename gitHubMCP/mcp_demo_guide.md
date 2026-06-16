# GitHub MCP Demo Guide

This guide explains how to use the `gitHubMCP` demo folder and how to explore GitHub MCP features in this workspace.

## Goals

- Show repository and branch inspection
- Demonstrate file creation and update workflows
- Explain issue and PR interaction patterns
- Document how to use GitHub MCP tools from Copilot Chat

## Recommended demo flow

1. Open `README.md` and `demo.py`.
2. Open `demo_notebook.ipynb` and read the markdown cells.
3. Run `python ui.py` and open `http://127.0.0.1:8500/` to interact with the demo UI.
4. Use the UI to:
   - list repositories for a GitHub owner
   - show last commit details for a repository
   - list open issues for a repository
   - inspect local demo files and GitHub environment context
5. Use GitHub Copilot Chat to ask for:
   - a summary of the current repo state
   - a list of files in this folder
   - a sample branch listing
   - a proposal for a new demo artifact
5. Use MCP tools to create or update files in the repo.

## Sample MCP tool examples

### List branches

Ask Copilot Chat to invoke the MCP branch listing tool for the current repository:

- `mcp_github_mcp_se_list_branches`

### Create or update a file

Use the MCP file creation/update tool to add a new demo artifact remotely:

- `mcp_github_mcp_se_create_or_update_file`

### Inspect an issue

Use the issue read tool to fetch issue metadata or comments:

- `mcp_github_mcp_se_issue_read`

### Secret scanning and code search

Use GitHub MCP scanning tools for security and code discovery:

- `mcp_github_mcp_se_run_secret_scanning`

## Practical demo tasks

- Task 1: add a new code sample or notebook section describing MCP operations
- Task 2: create a demo branch named `mcp-demo` and document the change
- Task 3: write a sample issue describing how to extend the demo

## Notes

- This folder is intentionally self-contained so the demo artifacts are easy to inspect.
- The actual GitHub MCP interactions happen through the assistant tool calls, not through the local script.
- If you want to use real GitHub API access from `demo.py`, set `GITHUB_TOKEN` and `GITHUB_REPOSITORY` in your environment.
