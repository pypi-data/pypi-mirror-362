"""
MkDocs Kuma Uptime Badge Plugin.

A plugin that converts shorthand placeholders to full Uptime Kuma badge links.
"""

import importlib.metadata

from mkdocs_kuma_uptime_badge.plugin import UptimeBadgePlugin

try:
    __version__ = importlib.metadata.version("mkdocs-kuma-uptime-badge")
except importlib.metadata.PackageNotFoundError:
    # Package is not installed
    __version__ = "0.0.0"

__all__ = ["UptimeBadgePlugin"]
