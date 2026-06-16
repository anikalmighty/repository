"""GitHub MCP demo helper."""

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent


def describe_mcp_capabilities() -> list[str]:
    """Return a list of GitHub MCP capability categories."""
    return [
        "Repository read/write",
        "Branch listing and branch metadata",
        "Issue and pull request inspection",
        "Commit and release metadata",
        "Code search and secret scanning",
        "File creation and updates",
    ]


def list_demo_files() -> list[str]:
    """Return the list of demo files inside this folder."""
    return [str(path.name) for path in ROOT.iterdir() if path.is_file()]


def get_github_context() -> dict[str, str | None]:
    """Return environment context for GitHub if available."""
    return {
        "GITHUB_TOKEN": os.environ.get("GITHUB_TOKEN"),
        "GITHUB_REPOSITORY": os.environ.get("GITHUB_REPOSITORY"),
        "GITHUB_ACTOR": os.environ.get("GITHUB_ACTOR"),
    }


def github_headers() -> dict[str, str]:
    """Build GitHub API headers using optional token authentication."""
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "GitHub-MCP-Demo",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def github_api_get(path: str, query: dict[str, str] | None = None) -> object:
    """Perform a GitHub API GET request and return the parsed JSON response."""
    query_string = ""
    if query:
        query_string = "?" + urllib.parse.urlencode(query)
    url = f"https://api.github.com{path}{query_string}"
    req = urllib.request.Request(url, headers=github_headers())
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as exc:
        payload = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API GET failed: {exc.code} {exc.reason} - {payload}")


def list_github_repos(owner: str) -> list[dict[str, object]]:
    """List public GitHub repositories for a user or org."""
    return github_api_get(f"/users/{urllib.parse.quote(owner)}/repos", {"per_page": "100", "sort": "updated"})  # type: ignore[assignment]


def get_last_commit(owner: str, repo: str) -> dict[str, object]:
    """Return the most recent commit details for a repository."""
    commits = github_api_get(
        f"/repos/{urllib.parse.quote(owner)}/{urllib.parse.quote(repo)}/commits",
        {"per_page": "1"},
    )
    return commits[0] if isinstance(commits, list) and commits else {}


def get_commits(owner: str, repo: str, per_page: int = 100) -> list[dict[str, object]]:
    """Return all commits for a repository by following pagination."""
    commits: list[dict[str, object]] = []
    page = 1
    while True:
        page_commits = github_api_get(
            f"/repos/{urllib.parse.quote(owner)}/{urllib.parse.quote(repo)}/commits",
            {"per_page": str(per_page), "page": str(page)},
        )
        if not isinstance(page_commits, list) or not page_commits:
            break
        commits.extend(page_commits)
        if len(page_commits) < per_page:
            break
        page += 1
    return commits


def list_repo_issues(owner: str, repo: str, state: str = "open") -> list[dict[str, object]]:
    """List repository issues, optionally filtering by state."""
    return github_api_get(
        f"/repos/{urllib.parse.quote(owner)}/{urllib.parse.quote(repo)}/issues",
        {"state": state, "per_page": "50"},
    )  # type: ignore[assignment]


def generate_demo_manifest() -> dict[str, object]:
    """Return a simple manifest for the demo artifacts."""
    return {
        "folder": str(ROOT),
        "files": list_demo_files(),
        "mcp_capabilities": describe_mcp_capabilities(),
    }


def save_manifest(output_name: str = "demo_manifest.json") -> Path:
    """Write the demo manifest as JSON into the demo folder."""
    output_path = ROOT / output_name
    with open(output_path, "w", encoding="utf-8") as handle:
        json.dump(generate_demo_manifest(), handle, indent=2)
    return output_path


if __name__ == "__main__":
    print("GitHub MCP Demo helper")
    print("========================")
    print("Demo folder:", ROOT)
    print("Repository root:", REPO_ROOT)
    print()
    print("Demo files:")
    for filename in list_demo_files():
        print(" -", filename)
    print()
    print("GitHub context:")
    for key, value in get_github_context().items():
        print(f" - {key}: {value if value is not None else '<not set>'}")
    manifest_path = save_manifest()
    print()
    print("Wrote demo manifest:", manifest_path)
