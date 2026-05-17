"""Tests for the minimal Hermes plugin discovery skeleton."""

from __future__ import annotations

import importlib
from collections.abc import Callable
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]


class RecordingContext:
    """Context double that records accidental registration calls."""

    def __init__(self) -> None:
        """Initialize an empty call log."""
        self.calls: list[str] = []

    def __getattr__(self, name: str) -> Callable[..., None]:
        """Return a recorder for any registration-like method."""

        def record(*_args: object, **_kwargs: object) -> None:
            self.calls.append(name)

        return record


def _load_package_entrypoint() -> ModuleType:
    return importlib.import_module("napcat_platform")


def _manifest_value(field: str) -> str:
    prefix = f"{field}:"
    for line in (ROOT / "plugin.yaml").read_text(encoding="utf-8").splitlines():
        if line.startswith(prefix):
            return line.removeprefix(prefix).strip()
    raise AssertionError(f"Missing plugin.yaml field: {field}")


def test_plugin_manifest_is_minimal_platform_manifest() -> None:
    """Manifest exposes the minimal platform plugin identity."""
    assert _manifest_value("name") == "hermes-platform-napcat"
    assert _manifest_value("kind") == "platform"
    assert _manifest_value("version") == "0.1.0"


def test_register_is_discovery_only() -> None:
    """Register can be called by Hermes without adding runtime behavior."""
    module = _load_package_entrypoint()
    ctx = RecordingContext()

    module.register(ctx)

    assert ctx.calls == []
