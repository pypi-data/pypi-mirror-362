import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

# Extensions to consider as text files
DEFAULT_TEXT_EXTENSIONS = [
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".c",
    ".cpp",
    ".h",
    ".hpp",
    ".cs",
    ".go",
    ".rs",
    ".rb",
    ".php",
    ".md",
    ".rst",
    ".txt",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".json",
    ".xml",
    ".sh",
    ".bat",
    ".ps1",
    ".R",
    ".kt",
    ".swift",
    ".m",
    ".mm",
    ".pl",
    ".pm",
    ".sql",
    ".graphql",
    ".lua",
    ".ex",
    ".exs",
    ".erl",
    ".elm",
    ".clj",
    ".scala",
    ".dart",
    ".vue",
    ".svelte",
    ".sol",
    ".pde",
    ".proto",
    ".groovy",
    ".jl",
    ".cf",
    ".tf",
    ".kt",
    ".kts",
]

DISALLOWED_FOLDERS: list[str] = [
    "**/*test*",
    "**/*mock*",
    "**/migrations",
    "**/settings",
    "**/node_modules",
    "**/vendor",
    "**/debug",
    "**/target",
    "**/dist",
    "**/build",
    "**/public",
    "**/generic",
    "**/examples",
    "**/docs",
    "**/themes",
    "**/templates",
    "**/fixtures",
    "**/assets",
    "**/static",
    "**/scripts",
    "**/images",
    "**/styles",
    "**/stylesheets",
    "**/html",
    "**/e2e",
    "**/i18n",
    "**/fonts",
    "**/locales",
    "**/contrib",
    "**/localizations",
    "**/translations",
    "**/cards",
    "**/.git",
    "**/__pycache__",
    "**/venv",
    "**/env",
    "**/.pytest_cache",
    "**/.mypy_cache",
    "**/.ruff_cache",
    "**/.vscode",
    "**/.idea",
    "**/.DS_Store",
]
DISALLOWED_FILES = [
    "*.pyc",
    "*.pyo",
    "*.pyd",
    "*.so",
    "*.dll",
    "*.exe",
    "*.bin",
    "*.obj",
    "*.o",
    "*.a",
    "*.lib",
    "*.dylib",
    "*.ncb",
    "*.sdf",
    "*.suo",
    "*.pdb",
    "*.idb",
    ".env",
    "*.egg-info",
    "*.egg",
    ".tox",
    ".nox",
    ".coverage",
    "*.min.js",
    "*.min.css",
    "*.map",
    "package-lock.json",
    "yarn.lock",
    "*.swp",
    "*.swo",
    ".ipynb_checkpoints",
]

MIN_CODE_LENGTH: int = 500

MAX_TOKENS_PER_PROJECT: int = 200000
MAX_TOKENS_PER_FILE: int = 20000

README_VALID_FILES = ["README.md", "Readme.md", "readme.md"]


@dataclass
class ParserConfig:
    directory: Path = field(default_factory=lambda: Path("."))
    model_name: str = ""

    max_tokens_per_project: int = MAX_TOKENS_PER_PROJECT

    allowed_extensions: List[str] = field(
        default_factory=lambda: DEFAULT_TEXT_EXTENSIONS.copy()
    )
    disallowed_folders: List[str] = field(
        default_factory=lambda: DISALLOWED_FOLDERS.copy()
    )
    disallowed_files: List[str] = field(default_factory=lambda: DISALLOWED_FILES.copy())
    exclude_patterns: List[str] = field(default_factory=list)
    min_code_lenght: int = MIN_CODE_LENGTH
    ignore_patterns: List[str] = field(init=False)  # Will be set in __post_init__

    max_tokens_per_file: int = MAX_TOKENS_PER_FILE
    readme_valid_files: List[str] = field(
        default_factory=lambda: README_VALID_FILES.copy()
    )

    skip_folder_readme: bool = False
    cache_dir: Path = field(
        default_factory=lambda: Path(os.path.expanduser("~/.cache/llm_devtale"))
    )
    dry_run: bool = False
    filter_folders: List[str] = field(default_factory=list)
    prompt: str = ""

    def __post_init__(self):
        """Validate and normalize configuration after initialization."""
        if self.max_tokens_per_project is None:
            self.max_tokens_per_project = MAX_TOKENS_PER_PROJECT
        if self.max_tokens_per_file is None:
            self.max_tokens_per_file = MAX_TOKENS_PER_FILE

        if not self.allowed_extensions:
            self.allowed_extensions = DEFAULT_TEXT_EXTENSIONS.copy()

        self.ignore_patterns = (
            self.disallowed_files + self.disallowed_folders + self.exclude_patterns
        )
        # Convert string paths to Path objects
        if isinstance(self.directory, str):
            self.directory = Path(self.directory).resolve()
        if isinstance(self.cache_dir, str):
            self.cache_dir = Path(self.cache_dir)
        # Create cache directory if it doesn't exist
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        # Normalize filter_extensions
        if self.allowed_extensions:
            # Ensure all extensions start with a dot
            self.allowed_extensions = [
                ext if ext.startswith(".") else f".{ext}"
                for ext in self.allowed_extensions
            ]
