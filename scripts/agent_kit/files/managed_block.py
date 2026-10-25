"""A region of a user-owned file that agent-kit owns and rewrites."""

import re

from pydantic import BaseModel, ConfigDict


class ManagedBlock(BaseModel):
    """Two marker lines that delimit the part of a file agent-kit may rewrite."""

    model_config = ConfigDict(frozen=True)

    begin: str
    end: str

    def _find(self, text: str) -> re.Match[str] | None:
        pattern = re.escape(self.begin) + r"\n?(.*?)" + re.escape(self.end)
        return re.search(pattern, text, re.S)

    def inner(self, text: str) -> str:
        """Return what is between the markers.

        :param text: The whole file.
        :return: The block contents, or ``""`` when the file has no block.
        """
        match = self._find(text)
        return match.group(1) if match else ""

    def outside(self, text: str) -> str:
        """Return the file without the block.

        :param text: The whole file.
        :return: Everything the user owns.
        """
        match = self._find(text)
        return text if not match else text[: match.start()] + text[match.end() :]

    def put(self, text: str, body: str) -> str:
        """Replace the block, or append it when the file has none yet.

        :param text: The whole file (may be empty).
        :param body: The new block contents, without markers.
        :return: The updated file.
        """
        block = f"{self.begin}\n{body}\n{self.end}"
        match = self._find(text)
        if match:
            return text[: match.start()] + block + text[match.end() :]
        separator = "\n\n" if text.strip() else ""
        return text.rstrip() + separator + block + "\n"
