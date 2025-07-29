from pathlib import Path

from rich.console import Console

from .config import ParserConfig
from .files import FileRepo, FileSelector
from .gitutils import GitRepository
from .node import Node
from .parser import ProjectParser
from .utils import get_llm_model, setup_logging


def main():
    setup_logging(True)
    console = Console()
    repo_path = Path("./")
    config = ParserConfig(
        directory=repo_path,
        dry_run=True,
    )
    git_repo: GitRepository = GitRepository(repo_path)
    effort: dict[str, int] = git_repo.get_git_effort()
    file_repo: FileRepo = FileRepo(repo_path, effort)
    file_selector = FileSelector(
        file_repo,
        ignore_patterns=config.ignore_patterns,
        allowed_extensions=config.allowed_extensions,
    )
    valid_files, token_count = file_selector.get_files_by_token(
        max_token_count=config.max_tokens_per_project,
        max_tokens_per_file=config.max_tokens_per_file,
    )
    model = get_llm_model(model_name=config.model_name)
    project_parser: ProjectParser = ProjectParser(
        parser_config=config, model=model, valid_files=valid_files
    )
    node: Node = project_parser.parse()
    print("File Token count:", token_count)
    console.print(node.to_tree())


if __name__ == "__main__":
    main()
