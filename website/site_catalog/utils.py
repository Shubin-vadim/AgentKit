"""Stateless text helpers for the website generator."""

import re

SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z])")
FRONTMATTER_FENCE = "---"
BLOCK_SCALARS = {">", ">-", ">+", "|", "|-", "|+"}
DISPLAY_NAMES = {
    "openspec": "OpenSpec",
    "speckit": "Spec Kit",
    "langgraph": "LangGraph",
    "vllm": "vLLM",
    "sglang": "SGLang",
    "llm-infra": "LLM infrastructure",
    "patterns": "Design patterns",
}


def first_sentence(text: str) -> str:
    """Cut a description down to its first sentence.

    :param text: A skill description, possibly several sentences long.
    :return: The first sentence, or the whole text when it has only one.
    """
    return SENTENCE_END.split(text.strip(), maxsplit=1)[0]


def display_name(folder: str) -> str:
    """Turn a folder name into a heading.

    :param folder: A folder name such as ``reverse-engineering``.
    :return: A known product name, or the folder in sentence case.
    """
    return DISPLAY_NAMES.get(folder, folder.replace("-", " ").capitalize())


def table_cell(text: str) -> str:
    """Make text safe inside a Markdown table cell.

    :param text: Any single-line or multi-line text.
    :return: One line with pipes escaped.
    """
    return " ".join(text.split()).replace("|", "\\|")


def frontmatter(text: str) -> dict[str, str]:
    """Read the top-level scalar keys of a Markdown file's YAML frontmatter.

    Handles ``key: value`` and folded or literal block scalars (``key: >-``);
    nested mappings and lists are skipped.

    :param text: The file contents.
    :return: Key to value; empty when the file has no frontmatter.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != FRONTMATTER_FENCE:
        return {}
    values: dict[str, str] = {}
    block_key: str | None = None
    for line in lines[1:]:
        if line.strip() == FRONTMATTER_FENCE:
            break
        if block_key and (line.startswith((" ", "\t")) or not line.strip()):
            values[block_key] = f"{values[block_key]} {line.strip()}".strip()
            continue
        block_key = None
        if line.startswith((" ", "\t")) or ":" not in line:
            continue
        key, _, value = line.partition(":")
        value = value.strip()
        if value in BLOCK_SCALARS:
            block_key, values[key.strip()] = key.strip(), ""
        else:
            values[key.strip()] = value.strip("\"'")
    return values
