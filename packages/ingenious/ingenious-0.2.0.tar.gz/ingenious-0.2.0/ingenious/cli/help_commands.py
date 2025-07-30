"""
Help and status CLI commands for Insight Ingenious.

This module provides backward compatibility while delegating to the new command architecture.
"""

from __future__ import annotations

from typing import Optional

import typer
from rich.console import Console
from typing_extensions import Annotated

from ingenious.cli.commands.help import (
    HelpCommand,
    StatusCommand,
    ValidateCommand,
    VersionCommand,
)


def register_commands(app: typer.Typer, console: Console) -> None:
    """Register help and status commands with the typer app."""

    @app.command(name="help", help="Show detailed help and getting started guide")
    def help_command(
        topic: Annotated[
            Optional[str],
            typer.Argument(help="Specific topic: setup, workflows, config, deployment"),
        ] = None,
    ):
        """
        📚 Show comprehensive help for getting started with Insight Ingenious.

        Topics available:
        • setup - Initial project setup steps
        • workflows - Understanding and configuring workflows
        • config - Configuration file details
        • deployment - Deployment options and best practices
        """
        cmd = HelpCommand(console)
        cmd.run(topic=topic)

    @app.command(name="status", help="Check system status and configuration")
    def status():
        """
        🔍 Check the status of your Insight Ingenious configuration.

        Validates:
        • Configuration files existence and validity
        • Environment variables
        • Required dependencies
        • Available workflows
        """
        cmd = StatusCommand(console)
        cmd.run()

    @app.command(name="version", help="Show version information")
    def version():
        """
        📦 Display version information for Insight Ingenious.
        """
        cmd = VersionCommand(console)
        cmd.run()

    @app.command(name="validate", help="Validate system configuration and requirements")
    def validate():
        """
        ✅ Comprehensive validation of your Insight Ingenious setup.

        Performs deep validation of:
        • Configuration file syntax and required fields
        • Profile file syntax and credentials
        • Azure OpenAI connectivity
        • Workflow requirements
        • Dependencies

        This command helps identify issues before starting the server.
        """
        cmd = ValidateCommand(console)
        cmd.run()
