"""Plugin system for MCP Gateway.

This package provides a flexible plugin system for extending MCP Gateway functionality.
"""

from mcp_gateway.plugins.base import (
    Plugin,
    PluginContext,
    GuardrailPlugin,
    TracingPlugin,
)
from mcp_gateway.plugins.manager import PluginManager, register_plugin

__all__ = [
    "Plugin",
    "PluginContext",
    "GuardrailPlugin",
    "TracingPlugin",
    "PluginManager",
    "register_plugin",
]
