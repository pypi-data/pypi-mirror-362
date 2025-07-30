import requests
import json
import logging


class GitHubAPIWrapper:
    def __init__(self, token):
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.subkey_activations = []
        self.arc_evolutions = []

    def fetch_issues(self, owner, repo):
        url = f"{self.base_url}/repos/{owner}/{repo}/issues"
        response = requests.get(url, headers=self.headers)
        issues = response.json()
        memory_mapped_issues = self.dynamic_memory_mapping(owner, repo, issues)
        return memory_mapped_issues

    def fetch_pull_requests(self, owner, repo):
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def fetch_comments(self, owner, repo, issue_number):
        url = f"{self.base_url}/repos/{owner}/{repo}/issues/{issue_number}/comments"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def fetch_commits(self, owner, repo):
        url = f"{self.base_url}/repos/{owner}/{repo}/commits"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def store_data(self, data, filename):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def fetch_and_store_issues(self, owner, repo, filename):
        issues = self.fetch_issues(owner, repo)
        self.store_data(issues, filename)

    def fetch_and_store_pull_requests(self, owner, repo, filename):
        pull_requests = self.fetch_pull_requests(owner, repo)
        self.store_data(pull_requests, filename)

    def fetch_and_store_comments(self, owner, repo, issue_number, filename):
        comments = self.fetch_comments(owner, repo, issue_number)
        self.store_data(comments, filename)

    def fetch_and_store_commits(self, owner, repo, filename):
        commits = self.fetch_commits(owner, repo)
        self.store_data(commits, filename)

    def dynamic_memory_mapping(self, owner, repo, issues):
        memory_map = {}
        for issue in issues:
            key_anchor = f"issues:{owner}/{repo}:{issue['id']}:agent:unknown"
            memory_map[key_anchor] = {
                "status": issue["state"],
                "agent": "unknown",
                "started_at": issue["created_at"],
                "notes": issue["body"],
                "ripple_refs": [],
                "next_steps": []
            }
            # Mention Ledger.mia in dynamic memory mapping
            memory_map[f"Ledger.mia:{key_anchor}"] = memory_map[key_anchor]
        return memory_map

    def activate_subkey(self, subkey):
        self.subkey_activations.append(subkey)
        self.log_subkey_activation(subkey)

    def evolve_arc(self, arc):
        self.arc_evolutions.append(arc)
        self.log_arc_evolution(arc)

    def log_subkey_activation(self, subkey):
        logging.info(f"Subkey Activated: {subkey}")

    def log_arc_evolution(self, arc):
        logging.info(f"Arc Evolved: {arc}")
