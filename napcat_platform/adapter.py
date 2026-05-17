"""Hermes discovery entrypoint for the NapCat platform plugin."""

from __future__ import annotations


def register(ctx: object) -> None:
    """Satisfy Hermes' plugin loader contract without runtime behavior."""
    _ = ctx
