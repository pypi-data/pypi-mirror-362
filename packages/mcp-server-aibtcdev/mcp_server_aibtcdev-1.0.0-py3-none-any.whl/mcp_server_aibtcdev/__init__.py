"""
aibtcdev MCP Server

A Model Context Protocol server for interacting with the aibtcdev-backend API,
including trading, DAO management, agent account management, and AI evaluation.
"""

__version__ = "1.0.0"

from .server import main

__all__ = ["main"]
