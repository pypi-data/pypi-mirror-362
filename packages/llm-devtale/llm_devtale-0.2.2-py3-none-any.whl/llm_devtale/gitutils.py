from git import Repo

from pathlib import Path


class GitRepository:
    def __init__(self, repo_path: Path):
        self.repo_path: Path = repo_path
        self.repo: Repo = Repo(self.repo_path)

    def get_commit_count(self) -> int:
        return int(self.repo.git.rev_list("--count", "HEAD"))

    def get_git_effort(self) -> dict[str, int]:
        result: str = self.repo.git.effort()

        res: dict[str, int] = {}

        for line in result.split("\n"):
            words = line.split()

            if len(words) < 3:
                continue
            if words[1] == "commits":
                continue
            if words[0] == "":
                continue

            file: str = words[0].split("..")[0]
            try:
                commits = int(words[1])
            except Exception:
                commits = 1

            res[file] = commits

        return dict(sorted(res.items(), key=lambda item: item[1], reverse=True))
