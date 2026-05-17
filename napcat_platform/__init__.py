"""Discovery-only Hermes plugin entrypoint for NapCat."""

from __future__ import annotations

from .adapter import register as register

PLUGIN_NAME = "hermes-platform-napcat"
PLUGIN_VERSION = "0.1.0"

__all__ = ["main", "register"]


def main() -> None:
    """Print a small CLI hint for local smoke tests."""
    print(f"{PLUGIN_NAME} {PLUGIN_VERSION}: discovery-only plugin skeleton")
