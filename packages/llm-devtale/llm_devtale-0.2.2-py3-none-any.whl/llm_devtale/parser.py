import logging
import os
from pathlib import Path
from typing import List, Optional

import llm

from .config import ParserConfig
from .node import Node, NodeType
from .utils import generate_summary, parallel_process

logger = logging.getLogger("llm_devtale")


class Parser:
    def __init__(
        self,
        parser_config: ParserConfig,
        model: llm.Model,
        item_path: str = "./",
        folder_full_name: str = "",
        valid_files: list = [],
    ):
        self.parser_config: ParserConfig = parser_config
        self.model = model
        self.root_path: str = str(parser_config.directory)
        self.item_path: str = item_path
        self.folder_full_name: str = folder_full_name
        self.valid_files = valid_files

    def _should_ignore(self, path, root_path) -> bool:
        path = Path(path)

        if os.path.isabs(path):
            item_relative_path: str = str(Path(path).relative_to(root_path))
        else:
            item_relative_path: str = str(path)

        # If hot_files is not empty, only include the files that are in the hot_files list
        if self.valid_files and item_relative_path not in self.valid_files:
            return True

        return False


class ProjectParser(Parser):
    def get_readme(self) -> str:
        original_readme_content: str = ""
        for readme in self.parser_config.readme_valid_files:
            readme_path = os.path.join(self.root_path, readme)
            if os.path.exists(readme_path):
                with open(readme_path, "r") as file:
                    original_readme_content = " ".join(file.readlines())
                    break

        return original_readme_content

    def parse(
        self,
    ) -> Node:
        """It creates a dev tale for each file in the repository, and it
        generates a README for the whole repository.
        """

        repository_name: str = os.path.basename(os.path.abspath(self.root_path))
        project_node = Node(
            name=repository_name,
            description="",
            node_type=NodeType.REPOSITORY,
        )
        # Get the project tree before modify it along with the complete list of files
        # that the repository has.
        file_paths = list(
            map(lambda x: os.path.join(self.root_path, x), self.valid_files)
        )

        # Extract the folder paths from files list. This allows to avoid processing
        # folders that should be ignored, and to use the process_folder logic.
        folders = list(set([os.path.dirname(file_path) for file_path in file_paths]))

        if self.parser_config.filter_folders:
            folders = [
                os.path.normpath(os.path.join(self.root_path, f))
                for f in self.parser_config.filter_folders
            ]

        # sort to always have the root folder at the beggining of the list.
        folders: List[str] = sorted(folders, key=lambda path: path.count("/"))

        # Get the folder's README section of each folder while it create a dev tale
        # for each file.
        for folder_path in folders:
            folder_full_name: str = ""
            try:
                # Fix folder path to avoid issues with file system.
                if not folder_path.endswith("/"):
                    folder_path += "/"

                folder_full_name = os.path.relpath(folder_path, self.root_path)

                # folder's summary
                folder_parser = FolderParser(
                    parser_config=self.parser_config,
                    model=self.model,
                    item_path=folder_path,
                    folder_full_name=folder_full_name,
                    valid_files=self.valid_files,
                )

                folder_tale = folder_parser.parse()
            except Exception:
                logger.exception(f"failed parsing folder {folder_path}")
                folder_tale = None

            # Create a dictionary with the folder's info that serves as context for
            # generating the main repository summary
            if folder_tale:
                project_node.add_children(folder_tale)

        project_summary = ""
        if (
            project_node.children
            and not self.parser_config.skip_folder_readme
            and not self.parser_config.dry_run
        ):
            original_readme = self.get_readme()
            project_data: dict = {
                "project_name": repository_name,
                "project_content": project_node.to_dict(),
                "project_readme": original_readme,
            }
            project_summary = generate_summary(
                self.model,
                project_data,
                summary_type=NodeType.REPOSITORY,
                additional_prompt=self.parser_config.prompt,
            )
            project_node.description = project_summary

        return project_node


class FolderParser(Parser):
    def parse(self) -> Node:
        """It creates a dev tale for each file in the directory without exploring
        subdirectories, and it generates a summary section for the folder.
        """
        folder_path: str = self.item_path
        node_dir = Node(
            name=self.folder_full_name, description="", node_type=NodeType.FOLDER
        )

        file_paths = [
            os.path.join(folder_path, fn)
            for fn in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, fn))
            and not self._should_ignore(os.path.join(folder_path, fn), self.root_path)
        ]

        def make_parser(path: str) -> Optional[Node]:
            try:
                return FileParser(
                    parser_config=self.parser_config,
                    model=self.model,
                    item_path=path,
                    valid_files=self.valid_files,
                ).parse()
            except Exception:
                logger.exception(f"failed parsing {path}")
                return None

        file_tales = parallel_process(file_paths, make_parser, max_workers=8)
        for tale in filter(None, file_tales):
            node_dir.add_children(tale)

        if (
            node_dir.children
            and not self.parser_config.skip_folder_readme
            and not self.parser_config.dry_run
        ):
            # Generate a folder one-line description using the folder's readme as context.
            folder_data: dict = {
                "folder_name": self.folder_full_name,
                "folder_content": node_dir.to_dict(),
            }

            folder_summary = generate_summary(
                self.model,
                folder_data,
                summary_type=NodeType.FOLDER,
                additional_prompt=self.parser_config.prompt,
            )
            node_dir.description = folder_summary

        return node_dir


class FileParser(Parser):
    def parse(self) -> Optional[Node | None]:
        file_path: str = self.item_path
        file_name: str = os.path.basename(file_path)

        with open(file_path, "r") as file:
            code: str = file.read()

        # # Return empty devtale if the input file is empty.
        if not code or len(code) < self.parser_config.min_code_lenght:
            return None

        file_node = Node(name=file_name, description="", node_type=NodeType.FILE)
        file_data: dict[str, str] = {
            "file_name": file_name,
            "file_content": code,
        }
        if not self.parser_config.dry_run:
            file_summary = generate_summary(
                self.model,
                file_data,
                summary_type=NodeType.FILE,
                additional_prompt=self.parser_config.prompt,
            )
            file_node.description = file_summary

        return file_node
