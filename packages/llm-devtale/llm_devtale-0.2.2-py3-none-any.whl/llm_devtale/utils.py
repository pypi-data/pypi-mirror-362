import concurrent.futures
import logging
import os
from typing import Callable, Dict, Iterable, List, TypeVar

import llm
import tiktoken

from .node import NodeType
from .templates import (FILE_TEMPLATE, FOLDER_SHORT_DESCRIPTION_TEMPLATE,
                        ROOT_LEVEL_TEMPLATE, SYSTEM_PROMPT)

# Configure default logger
logger = logging.getLogger("llm_devtale")

# Type variables for generic functions
T = TypeVar("T")
R = TypeVar("R")
prompts: Dict[NodeType, str] = {
    NodeType.FILE: FILE_TEMPLATE,
    NodeType.FOLDER: FOLDER_SHORT_DESCRIPTION_TEMPLATE,
    NodeType.REPOSITORY: ROOT_LEVEL_TEMPLATE,
}


class TokenCounter:
    @staticmethod
    def count_tokens(text: str) -> int:
        return len(tiktoken.get_encoding("cl100k_base").encode(text))


def get_prompt(summary_type: NodeType) -> str:
    prompt: str = prompts.get(summary_type, "")
    if not prompt:
        raise Exception("No template found with {summary_type}")

    return prompt


def generate_summary(
    llm_model: llm.Model,
    data: dict,
    summary_type: NodeType,
    additional_prompt: str = "",
) -> str:
    prompt: str = get_prompt(summary_type).format(
        data=data, additional_prompt=additional_prompt
    )
    return llm_model.prompt(prompt, system=SYSTEM_PROMPT).text()


def get_llm_model(model_name: str) -> llm.Model:
    if not model_name:
        model_name = llm.get_default_model()

    return llm.get_model(model_name)


def parallel_process(
    items: Iterable[T], process_func: Callable[[T], R], max_workers: int = 0
) -> List[R]:
    """
    Process items in parallel using a thread pool.

    Args:
        items: Items to process
        process_func: Function to apply to each item
        max_workers: Maximum number of worker threads

    Returns:
        List of results
    """
    items_list = list(items)
    results = []

    if max_workers < 1:
        max_workers = min(10, (os.cpu_count() or 4))

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for item in items_list:
            futures.append(executor.submit(process_func, item))

        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                logger.error(f"Error in parallel processing: {e}")

    return results


def setup_logging(verbose: bool = False) -> None:
    """
    Set up logging configuration.

    Args:
        verbose: Whether to enable debug logging
        log_file: Path to log file (optional)
    """
    log_level = logging.DEBUG if verbose else logging.INFO

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Clear any existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)

    # Add console handler to root logger
    root_logger.addHandler(console_handler)

    # Suppress verbose logging from libraries unless in debug mode
    if not verbose:
        for lib_logger_name in ["urllib3", "httpx"]:
            logging.getLogger(lib_logger_name).setLevel(logging.WARNING)
