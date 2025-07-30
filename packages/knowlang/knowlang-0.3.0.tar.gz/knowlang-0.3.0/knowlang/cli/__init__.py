"""CLI entry points for KnowLang."""

import asyncio
import importlib.metadata
from typing import Optional, Sequence
from knowlang.cli.argparser import parse_args
from knowlang.utils import FancyLogger


def load_plugins():
    eps = importlib.metadata.entry_points().select(group="knowlang.plugins")

    for ep in eps:
        try:
            # Loading the plugin causes its module-level code to run
            ep.load()
        except Exception as e:
            LOG.error(f"Error loading plugin {ep.name}: {e}")


LOG = FancyLogger(__name__)


async def main(args: Optional[Sequence[str]] = None) -> int:
    """Main CLI entry point.

    Args:
        args: Command line arguments. If None, sys.argv[1:] is used.

    Returns:
        Exit code (0 for success, non-zero for error)
    """
    parsed_args = parse_args()

    # Setup logging
    if parsed_args.verbose:
        LOG.setLevel("DEBUG")

    try:
        # Execute command
        await parsed_args.command_func(parsed_args)
        return 0
    except Exception as e:
        import traceback

        LOG.error(traceback.format_exc())
        LOG.error(f"Error: {str(e)}")
        return 1


def cli_main() -> None:
    """Entry point for CLI scripts."""
    # setup_logger()
    load_plugins()
    exit_code = asyncio.run(main())
    exit(exit_code)
