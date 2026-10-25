"""A reporter that remembers what it was told, for assertions."""


class RecordingReporter:
    """Keeps every reported line so tests can assert on them."""

    def __init__(self) -> None:
        self.actions: list[tuple[str, str, str]] = []
        self.infos: list[str] = []
        self.warnings: list[str] = []
        self.errors: list[str] = []

    def action(self, action: str, path: str, note: str = "") -> None:
        """Record a file change.

        :param action: The verb.
        :param path: The relative path.
        :param note: Optional detail.
        """
        self.actions.append((action, path, note))

    def info(self, message: str) -> None:
        """Record a plain line.

        :param message: The text.
        """
        self.infos.append(message)

    def warn(self, message: str) -> None:
        """Record a warning.

        :param message: The text.
        """
        self.warnings.append(message)

    def error(self, message: str) -> None:
        """Record an error.

        :param message: The text.
        """
        self.errors.append(message)

    def verbs(self) -> list[str]:
        """List the recorded action verbs.

        :return: Verbs in order.
        """
        return [verb for verb, _, _ in self.actions]
