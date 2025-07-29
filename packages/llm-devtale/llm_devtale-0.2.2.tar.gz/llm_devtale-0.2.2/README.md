# llm-devtale

`llm-devtale` is a plugin for [Simon Willison's LLM tool](https://github.com/simonw/llm) `llm` command-line tool that automatically generates documentation ("dev tales") for your source code projects. It analyzes your project's files and folders, considering factors like file size, git commit effort, and excluded patterns, to produce a hierarchical, LLM-generated summary of your codebase.

The generated documentation includes:
*   A high-level overview of the entire repository.
*   Summaries for each analyzed folder.
*   Detailed "dev tales" for individual source code files.

To avoid analyzing too much boilerplate or non-important data,  the program expects the folder to be a git repository, so it can order the files by number of commits to focus on the most important files (most commits) within the limits of the tokens configured

Taken inspiration (and some code) from https://github.com/tenxstudio/devtale and https://github.com/irthomasthomas/llm-cartographer

The tool uses threads to speed up the analysis, up to maximum 8 threads, only for file summarization.
## Installation

First, ensure you have `llm` installed:
```bash
uv tool install llm
```

Then, install the `llm-devtale` plugin:
```bash
llm install llm-devtale
```

## Usage

Once installed, the `devtale` command will be available through the `llm` CLI:

```bash
llm devtale [DIRECTORY] [OPTIONS]
```

By default, `DIRECTORY` is the current working directory (`.`).

## Examples

### Generate documentation for the current directory

This will output the generated documentation to your console.
```bash
llm devtale .
```

### Output documentation to a file

Save the generated documentation to `PROJECT_README.md`.
```bash
llm devtale . -o PROJECT_README.md
```

### Use a specific LLM model

Generate documentation using `gpt-4`:
```bash
llm devtale . -m gpt4
```

### Exclude specific files or folders

Exclude all files under `test/` directories and `docs/` folders using gitignore-style patterns:
```bash
llm devtale . -e "**/test/*" -e "docs/"
```

### Filter by file extension

Only include Python (`.py`) and JavaScript (`.js`) files in the analysis (do NOT forget the '\*' before the extension):
```bash
llm devtale . -f *.py -f *.js
```
### Filter by directory

Only include folders src/app and src/utils:
```bash
llm devtale . -k src/app -k src/utils
```

### Limit token usage

Specify the maximum number of tokens to send to the LLM for the entire project and per file:
```bash
llm devtale . --max-tokens 50000 --max-tokens-per-file 5000
```

### Perform a dry run

See which files and folders would be analyzed without actually calling the LLM. This shows the project hierarchy and token counts.
```bash
llm devtale . --dry-run
```

### Add additional instructions to the prompt

Add additional instructions to the end of all LLM prompts.
```bash
llm devtale -p "All summaries should be in uppercase" .
```


## Options

*   `DIRECTORY`: Path to the project directory (default: `.`)
*   `-e, --exclude <PATTERN>`: Patterns to exclude files/folders (gitignore format). Can be used multiple times.
*   `--max-tokens <INT>`: Maximum total tokens to send to the LLM for the entire project.
*   `--max-tokens-per-file <INT>`: Maximum tokens to process per individual file.
*   `-o, --output <PATH>`: Output file path or directory to save the generated documentation.
*   `-m, --model <MODEL_NAME>`: Specify the LLM model to use (e.g., `gpt4`). If not set uses the default model configured in the llm cli tool
*   `-f, --filter-extension <EXTENSION>`: Only include files with these extensions (e.g., `*.py`, `*.md`). Can be used multiple times.
*   `-t, --dry-run`: Show the hierarchy and files that will be analyzed without making LLM calls.
*   `-d, --debug`: Turn on verbose logging.
*   `-k, --filter-folder`: Only parse the specified folder(s)
*   `-p, --prompt`: Additional prompt to be added at the end of the program prompt

## Debug
The program can be executed using an ad-hoc main.py file added for convenience:
```
python -m llm_devtale.main
```
