import os
from pathlib import Path
from typing import List, Tuple


from .utils import TokenCounter


class FileRepo:
    def __init__(self, repo_path: Path, git_effort: dict):
        self.repo_path: Path = repo_path
        self.effort: dict = git_effort


class FileSelector:
    def __init__(
        self,
        file_repo: FileRepo,
        ignore_patterns: list[str] = [],
        allowed_extensions: list[str] = [],
    ) -> None:
        self.ignore_patterns: List[str] = ignore_patterns
        self.allowed_extensions: List[str] = allowed_extensions
        self.file_repo = file_repo

    def valid_extension(self, file: str) -> bool:
        if os.path.splitext(file)[1] in self.allowed_extensions:
            return True

        return False

    def valid_file(self, file: str) -> bool:
        path = Path(file)

        if not self.valid_extension(file):
            return False

        for pattern in self.ignore_patterns:
            if path.match(pattern) or any(p.match(pattern) for p in path.parents):
                return False
        return True

    def count_tokens(self, file_path) -> int:
        if not os.path.isabs(file_path):
            file_path = os.path.join(self.file_repo.repo_path, file_path)

        try:
            with open(file_path, "r") as f:
                content: str = f.read()
                token_count = TokenCounter.count_tokens(content)
        except Exception:
            token_count = 0

        return token_count

    def get_files_by_token(
        self, max_token_count: int, max_tokens_per_file: int = 20000
    ) -> Tuple[list, int]:
        """
        Returns the files that fir into the max_toke_count, focusing first in the files with most commits,
        assuming that more commits means more importance
        """
        git_effort: dict[str, int] = self.file_repo.effort

        valid_files = filter(self.valid_file, git_effort.keys())

        total_token_count: int = 0
        hot_files: List[str] = []

        for valid_file in valid_files:
            file_token_count = self.count_tokens(valid_file)
            if file_token_count == 0:
                continue
            if file_token_count > max_tokens_per_file:
                continue

            if file_token_count + total_token_count > max_token_count:
                break

            total_token_count += file_token_count
            hot_files.append(valid_file)

        return hot_files, total_token_count
