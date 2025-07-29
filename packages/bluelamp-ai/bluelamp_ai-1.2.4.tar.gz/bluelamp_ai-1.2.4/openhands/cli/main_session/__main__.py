"""Main entry point for main_session module."""

import asyncio
from openhands.cli.main_session.main import main_with_loop

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main_with_loop(loop))
    finally:
        loop.close()