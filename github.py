import requests
from typing import Dict, List, Optional
from mcp.server.fastmcp import FastMCP
BASE_URL = "https://api.github.com"

mcp = FastMCP("github")

class GitHub:
    def __init__(self, token: str):
        """Initialize GitHub API client with personal access token."""
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Helper function to make API requests with rate limiting."""
        url = f"{BASE_URL}/{endpoint}"
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    @mcp.tool()
    def get_user_info(self, username: str) -> Dict:
        """
        Fetch user information.
        Endpoint: GET /users/:username
        Returns: User details (name, email, bio, etc.)
        """
        return self._make_request(f"users/{username}")

    @mcp.tool()
    def get_user_repos(self, username: str, per_page: int = 30, page: int = 1) -> List[Dict]:
        """
        Fetch a user's public repositories.
        Endpoint: GET /users/:username/repos
        Returns: List of repositories
        """
        params = {"per_page": per_page, "page": page}
        return self._make_request(f"users/{username}/repos", params=params)

    @mcp.tool()
    def get_repo_issues(self, owner: str, repo: str, state: str = "open", per_page: int = 30, page: int = 1) -> List[Dict]:
        """
        Fetch issues for a repository.
        Endpoint: GET /repos/:owner/:repo/issues
        Args:
            state: 'open', 'closed', or 'all'
        Returns: List of issues
        """
        params = {"state": state, "per_page": per_page, "page": page}
        return self._make_request(f"repos/{owner}/{repo}/issues", params=params)

    @mcp.tool()
    def get_repo_commits(self, owner: str, repo: str, per_page: int = 30, page: int = 1) -> List[Dict]:
        """
        Fetch commits for a repository.
        Endpoint: GET /repos/:owner/:repo/commits
        Returns: List of commits
        """
        params = {"per_page": per_page, "page": page}
        return self._make_request(f"repos/{owner}/{repo}/commits", params=params)

    @mcp.tool()
    def get_repo_pull_requests(self, owner: str, repo: str, state: str = "closed", per_page: int = 30, page: int = 1) -> List[Dict]:
        """
        Fetch pull requests for a repository.
        Endpoint: GET /repos/:owner/:repo/pulls
        Args:
            state: 'open', 'closed', or 'all'
        Returns: List of pull requests
        """
        params = {"state": state, "per_page": per_page, "page": page}
        return self._make_request(f"repos/{owner}/{repo}/pulls", params=params)
    
known_actions = {
    "get_user_info": GitHub.get_user_info,
    "get_user_repos": GitHub.get_user_repos,
    "get_repo_issues": GitHub.get_repo_issues,
    "get_repo_commits": GitHub.get_repo_commits,
    "get_repo_pull_requests": GitHub.get_repo_pull_requests,
}

mcp.run(transport="stdio")