"""The rule model shared by every client adapter."""

from pydantic import BaseModel, ConfigDict

CODE_FENCE = "```"
HEADING_MARK = "#"


class Rule(BaseModel):
    """A parsed ``.mdc`` rule: original text, body, and optional file scope."""

    model_config = ConfigDict(frozen=True)

    name: str
    source: str
    body: str
    globs: tuple[str, ...] = ()
    always: bool = False

    @property
    def scope(self) -> tuple[str, ...]:
        """Give the files this rule is limited to.

        :return: File globs; empty when the rule always applies.
        """
        return () if self.always else self.globs

    def scope_note(self) -> str:
        """Describe the scope in plain text, for clients that cannot scope rules.

        :return: A Markdown line ending in a blank line, or ``""`` when unscoped.
        """
        if not self.scope:
            return ""
        patterns = ", ".join(f"`{glob}`" for glob in self.scope)
        return f"_Applies when working on files matching: {patterns}._\n\n"

    def demoted_body(self) -> str:
        """Push every heading one level down, leaving fenced code untouched.

        :return: The body, ready to embed under another heading.
        """
        lines: list[str] = []
        fenced = False
        for line in self.body.splitlines():
            if line.lstrip().startswith(CODE_FENCE):
                fenced = not fenced
            demote = not fenced and line.startswith(HEADING_MARK)
            lines.append(HEADING_MARK + line if demote else line)
        return "\n".join(lines)
