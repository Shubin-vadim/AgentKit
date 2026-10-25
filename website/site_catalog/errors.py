"""Errors raised while building the website catalog."""

from agent_kit import AppError


class CatalogError(AppError):
    """The kit or its README lacks something the website is built from."""
