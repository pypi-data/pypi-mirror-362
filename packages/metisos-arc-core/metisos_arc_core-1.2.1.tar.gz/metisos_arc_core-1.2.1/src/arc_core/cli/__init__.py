"""
ARC Core Command Line Interface

This module provides the CLI interface for the ARC Core package.
"""
from .arc import cli

# For backward compatibility with entry points
def main():
    """Main entry point for the ARC CLI."""
    cli()
