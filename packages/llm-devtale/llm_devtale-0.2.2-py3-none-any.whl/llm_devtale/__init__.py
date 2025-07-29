import logging
import traceback
from pathlib import Path

import click
import llm
from rich.console import Console

from .config import ParserConfig
from .files import FileRepo, FileSelector
from .gitutils import GitRepository
from .node import Node
from .parser import ProjectParser
from .utils import get_llm_model, setup_logging

logger = logging.getLogger("llm_devtale")
console = Console()


@llm.hookimpl
def register_commands(cli):
    @cli.command(name="devtale", help="Create documentation from source files")
    @click.argument(
        "directory",
        type=click.Path(exists=True, file_okay=False, dir_okay=True),
        default=".",
    )
    @click.option(
        "--exclude", "-e", multiple=True, help="Patterns to exclude (gitignore format)"
    )
    @click.option(
        "--max-tokens", type=int, help="Maximum number of tokens to send to the LLM"
    )
    @click.option(
        "--max-tokens-per-file",
        type=int,
        help="Max tokens per file",
    )
    @click.option(
        "--output", "-o", type=click.Path(), help="Output file path or directory"
    )
    @click.option("--model", "-m", help="LLM model to use")
    @click.option(
        "--filter-extension",
        "-f",
        multiple=True,
        help="Only include files with these extensions",
    )
    @click.option(
        "--filter-folder",
        "-k",
        multiple=True,
        help="Only include files with these folders",
    )
    @click.option(
        "--dry-run",
        "-t",
        is_flag=True,
        help="Show hierarchy and files that will be analyzed without using the LLM",
    )
    @click.option(
        "--debug",
        "-d",
        is_flag=True,
        help="Turns on debug logging",
    )
    @click.option(
        "-p",
        "--prompt",
        type=str,
        help="Additional prompt to be included at the end in the summarization instructions",
    )
    def devtale(
        directory,
        exclude,
        max_tokens,
        max_tokens_per_file,
        output,
        model,
        filter_extension,
        filter_folder,
        dry_run,
        debug,
        prompt,
    ):
        try:
            setup_logging(verbose=debug)
            exclude_patterns = list(exclude)
            allowed_extensions = list(filter_extension)

            config = ParserConfig(
                directory=directory,
                model_name=model,
                max_tokens_per_file=max_tokens_per_file,
                max_tokens_per_project=max_tokens,
                exclude_patterns=exclude_patterns,
                allowed_extensions=allowed_extensions,
                dry_run=dry_run,
                filter_folders=filter_folder,
                prompt=prompt,
            )
            git_repo: GitRepository = GitRepository(directory)
            effort: dict[str, int] = git_repo.get_git_effort()
            file_repo: FileRepo = FileRepo(directory, effort)

            file_selector = FileSelector(
                file_repo,
                ignore_patterns=config.ignore_patterns,
                allowed_extensions=config.allowed_extensions,
            )

            valid_files, token_count = file_selector.get_files_by_token(
                max_token_count=config.max_tokens_per_project,
                max_tokens_per_file=config.max_tokens_per_file,
            )
            logger.debug(f"Files to be analyzed: {valid_files}")
            model = get_llm_model(model_name=config.model_name)
            project_parser: ProjectParser = ProjectParser(
                parser_config=config, model=model, valid_files=valid_files
            )
            node: Node = project_parser.parse()

            click.echo(f"Total file Token count: {token_count}")

            if output:
                result = node.to_string()
                output_file = Path(output)

                with open(output_file, "w") as f:
                    f.write(result)
            else:
                console.print(node.to_tree())
        except Exception as e:
            click.secho(f"Error ({e.__class__.__name__}): {e!r}", fg="red")
            click.secho(traceback.format_exc(), fg="bright_black")
            raise click.Abort()
