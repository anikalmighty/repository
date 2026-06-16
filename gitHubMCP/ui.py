"""Simple local UI for the GitHub MCP demo."""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import json

from demo import (
    describe_mcp_capabilities,
    get_github_context,
    list_demo_files,
    list_github_repos,
    get_commits,
    list_repo_issues,
    save_manifest,
)

HOST = "127.0.0.1"
PORT = 8500


def format_html(title: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>{title}</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; line-height: 1.6; }}
    h1 {{ color: #0b4f6c; }}
    pre {{ background: #f4f4f4; padding: 12px; border-radius: 8px; overflow-x: auto; }}
    .button {{ display: inline-block; margin: 8px 4px; padding: 10px 16px; background: #1f77b4; color: white; text-decoration: none; border-radius: 6px; }}
    .button:hover {{ background: #155a8a; }}
  </style>
</head>
<body>
  <h1>{title}</h1>
  {body}
</body>
</html>"""


class DemoUIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        action = query.get("action", [""])[0]

        if parsed.path in {"/", "/index.html"}:
            self._send_html(self.render_home())
            return

        if parsed.path == "/run":
            self._send_html(self.render_action(action))
            return

        if parsed.path == "/repos":
            owner = query.get("owner", ["anikalmighty"])[0]
            repos = list_github_repos(owner)
            repo_names = [repo.get("name", "") for repo in repos if isinstance(repo, dict)]
            self._send_json({"repos": repo_names})
            return

        self.send_error(404, "Not Found")

    def render_home(self) -> str:
        body = (
            "<p>Use the controls below to run demo actions and inspect the local MCP demo.</p>"
            "<form action=\"/run\" method=\"get\">"
            "<div style=\"margin-bottom:16px;\">"
            "<label style=\"margin-right:16px;\">GitHub owner: <input name=\"owner\" id=\"ownerInput\" value=\"anikalmighty\" style=\"width:220px;\"/></label>"
            "<label>Repository: <select name=\"repo\" id=\"repoSelect\" style=\"width:240px;\"></select></label>"
            "<button class=\"button\" type=\"button\" onclick=\"loadRepos()\">Refresh repos</button>"
            "</div>"
            "<div>"
            "<button class=\"button\" type=\"submit\" name=\"action\" value=\"list_files\">List Demo Files</button>"
            "<button class=\"button\" type=\"submit\" name=\"action\" value=\"describe_capabilities\">Show Capabilities</button>"
            "<button class=\"button\" type=\"submit\" name=\"action\" value=\"github_context\">Show GitHub Context</button>"
            "<button class=\"button\" type=\"submit\" name=\"action\" value=\"list_repos\">List Repositories</button>"
            "<button class=\"button\" type=\"submit\" name=\"action\" value=\"list_issues\">List Open Issues</button>"
            "<button class=\"button\" type=\"submit\" name=\"action\" value=\"list_commits\">Show All Commits</button>"
            "<button class=\"button\" type=\"submit\" name=\"action\" value=\"save_manifest\">Save Manifest</button>"
            "</div>"
            "</form>"
            "<p>Open this page in a browser to interact with the demo.</p>"
            "<script>\n"
            "async function loadRepos() {\n"
            "  const owner = document.getElementById('ownerInput').value || 'anikalmighty';\n"
            "  const response = await fetch('/repos?owner=' + encodeURIComponent(owner));\n"
            "  const data = await response.json();\n"
            "  const select = document.getElementById('repoSelect');\n"
            "  select.innerHTML = '';\n"
            "  if (!data.repos || data.repos.length === 0) {\n"
            "    const option = document.createElement('option');\n"
            "    option.text = 'No repos found';\n"
            "    option.value = '';\n"
            "    select.add(option);\n"
            "    return;\n"
            "  }\n"
            "  data.repos.forEach(function(repo) {\n"
            "    const option = document.createElement('option');\n"
            "    option.value = repo;\n"
            "    option.text = repo;\n"
            "    select.add(option);\n"
            "  });\n"
            "}\n"
            "window.addEventListener('load', loadRepos);\n"
            "</script>"
        )
        return format_html("GitHub MCP Demo UI", body)

    def render_action(self, action: str) -> str:
        try:
            if action == "list_files":
                items = list_demo_files()
                body = "<h2>Demo Files</h2><pre>" + "\n".join(items) + "</pre>"
            elif action == "describe_capabilities":
                items = describe_mcp_capabilities()
                body = "<h2>MCP Demo Capabilities</h2><pre>" + "\n".join(items) + "</pre>"
            elif action == "github_context":
                context = get_github_context()
                body = "<h2>GitHub Context</h2><pre>" + "\n".join(f"{k}: {v}" for k, v in context.items()) + "</pre>"
            elif action == "list_repos":
                owner = self._query_owner()
                repos = list_github_repos(owner)
                body = f"<h2>Repositories for {owner}</h2><pre>"
                body += "\n".join(
                    f"{repo['full_name']} - {repo.get('description', '') or '<no description>'}"
                    for repo in repos
                )
                body += "</pre>"
            elif action == "list_issues":
                owner = self._query_owner()
                repo = self._query_repo()
                issues = list_repo_issues(owner, repo)
                if issues:
                    body = f"<h2>Open Issues for {owner}/{repo}</h2><pre>"
                    body += "\n".join(
                        f"#{issue['number']}: {issue['title']} (state={issue['state']})"
                        for issue in issues
                    )
                    body += "</pre>"
                else:
                    body = f"<h2>Open Issues for {owner}/{repo}</h2><p>No open issues found.</p>"
            elif action == "list_commits":
                owner = self._query_owner()
                repo = self._query_repo()
                commits = get_commits(owner, repo)
                if commits:
                    body = f"<h2>Commits for {owner}/{repo}</h2><pre>"
                    body += "\n".join(
                        f"{commit.get('sha', '')[:7]} - {commit.get('commit', {}).get('author', {}).get('name', '<unknown>')} - {commit.get('commit', {}).get('author', {}).get('date', '<unknown>')} - {commit.get('commit', {}).get('message', '').splitlines()[0]}"
                        for commit in commits
                    )
                    body += "</pre>"
                else:
                    body = f"<h2>Commits for {owner}/{repo}</h2><p>No commits found.</p>"
            elif action == "save_manifest":
                path = save_manifest()
                body = f"<h2>Manifest Saved</h2><p>Wrote manifest to <strong>{path}</strong>.</p>"
            else:
                body = "<p>Unknown action. Return to the <a href=\"/\">home page</a>.</p>"
        except Exception as exc:
            body = f"<h2>Error</h2><pre>{exc}</pre>"

        body += '<p><a class="button" href="/">Back to home</a></p>'
        return format_html("GitHub MCP Demo UI", body)

    def _query_owner(self) -> str:
        return self._get_query_value("owner") or "anikalmighty"

    def _query_repo(self) -> str:
        return self._get_query_value("repo") or "repository"

    def _get_query_value(self, name: str) -> str | None:
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        value = query.get(name, [None])[0]
        return value

    def _send_html(self, html: str) -> None:
        encoded = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def _send_json(self, data: object) -> None:
        encoded = json.dumps(data).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, format: str, *args) -> None:
        return


def main() -> None:
    server_address = (HOST, PORT)
    print(f"Starting GitHub MCP Demo UI at http://{HOST}:{PORT}/")
    print("Press Ctrl+C to stop.")
    with HTTPServer(server_address, DemoUIHandler) as httpd:
        httpd.serve_forever()


if __name__ == "__main__":
    main()
