"""Main entry point for openhands2 with CodeActAgent."""

import asyncio
import logging
import os
import sys

from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import clear

import openhands.agenthub
import openhands.cli.suppress_warnings  # noqa: F401
from openhands.cli.commands import (
    check_folder_security_agreement,
    handle_commands,
)
from openhands.cli.settings import modify_llm_settings_basic
from openhands.cli.tui import (
    UsageMetrics,
    display_agent_running_message,
    display_banner,
    display_event,
    display_initial_user_prompt,
    display_initialization_animation,
    display_runtime_initialization_message,
    display_welcome_message,
    process_agent_pause,
    read_confirmation_input,
    read_prompt_input,
)
from openhands.cli.utils import (
    update_usage_metrics,
)
from openhands.controller import AgentController
from openhands.controller.agent import Agent
from openhands.core.config import (
    OpenHandsConfig,
    parse_arguments,
    setup_config_from_args,
)
from openhands.core.config.utils import get_workspace_mount_path
from openhands.core.config.condenser_config import NoOpCondenserConfig
from openhands.core.config.mcp_config import OpenHandsMCPConfigImpl
from openhands.core.logger import openhands_logger as logger
from openhands.core.loop import run_agent_until_done
from openhands.core.schema import AgentState
from openhands.core.setup import (
    create_agent,
    create_controller,
    create_memory,
    create_runtime,
    generate_sid,
    initialize_repository_for_runtime,
)
from openhands.events import EventSource, EventStreamSubscriber
from openhands.events.action import (
    ChangeAgentStateAction,
    MessageAction,
)
from openhands.events.event import Event
from openhands.events.observation import (
    AgentStateChangedObservation,
)
from openhands.io import read_task
from openhands.mcp import add_mcp_tools_to_agent
from openhands.memory.condenser.impl.llm_summarizing_condenser import (
    LLMSummarizingCondenserConfig,
)
from openhands.runtime.base import Runtime
from openhands.storage.settings.file_settings_store import FileSettingsStore

# Import Portal authentication
from openhands.cli.auth import PortalAuthenticator, get_authenticator

# Import the main session runner from the original main.py
from openhands.cli.main import cleanup_session, run_session, run_setup_flow


async def main_with_loop(loop: asyncio.AbstractEventLoop) -> None:
    """Runs the CodeActAgent in CLI mode."""
    args = parse_arguments()

    logger.setLevel(logging.WARNING)

    # Load config from toml and override with command line arguments
    config: OpenHandsConfig = setup_config_from_args(args)
    
    # Force CodeActAgent
    config.default_agent = 'CodeActAgent'

    # Load settings from Settings Store
    settings_store = await FileSettingsStore.get_instance(config=config, user_id=None)
    settings = await settings_store.load()

    # Portal authentication check
    auth = get_authenticator()
    api_key = auth.load_api_key()
    
    # Track if we've shown the banner during setup
    banner_shown = False

    # Check Portal authentication first
    if not api_key:
        clear()
        print_formatted_text(
            HTML('<ansiblue>🔐 BlueLamp CLI Authentication Required</ansiblue>\n')
        )
        print_formatted_text(
            HTML('<grey>Please log in with your Portal account to continue.</grey>\n')
        )
        
        try:
            success = await auth.prompt_for_login()
            if not success:
                print_formatted_text(
                    HTML('<ansired>❌ Authentication failed. Exiting...</ansired>')
                )
                return
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            print_formatted_text(
                HTML(f'<ansired>❌ Authentication error: {e}</ansired>')
            )
            return
            
        banner_shown = True

    # Verify API key is valid
    else:
        try:
            result = await auth.verify_api_key(auto_reauth=True)
            if not result.get("success"):
                print_formatted_text(
                    HTML('<ansired>❌ Invalid authentication token. Please login again.</ansired>')
                )
                return
            logger.info(f"Authenticated as: {auth.user_info.get('name') if auth.user_info else 'Unknown'}")  # type: ignore
        except Exception as e:
            logger.error(f"Token verification error: {e}")
            print_formatted_text(
                HTML('<ansired>❌ Authentication verification failed. Please login again.</ansired>')
            )
            # Clear invalid auth
            auth.clear_auth()
            return

    # If settings don't exist, automatically enter the setup flow
    if not settings:
        # Clear the terminal before showing the banner (if not already shown)
        if not banner_shown:
            clear()

        await run_setup_flow(config, settings_store)
        banner_shown = True

        settings = await settings_store.load()

    # Use settings from settings store if available and override with command line arguments
    if settings:
        # Force CodeActAgent regardless of settings
        config.default_agent = 'CodeActAgent'
        
        if not args.llm_config and settings.llm_model and settings.llm_api_key:
            llm_config = config.get_llm_config()
            llm_config.model = settings.llm_model
            llm_config.api_key = settings.llm_api_key
            llm_config.base_url = settings.llm_base_url
            config.set_llm_config(llm_config)
        config.security.confirmation_mode = (
            settings.confirmation_mode if settings.confirmation_mode else False
        )

        if settings.enable_default_condenser:
            llm_config = config.get_llm_config()
            agent_config = config.get_agent_config(config.default_agent)
            agent_config.condenser = LLMSummarizingCondenserConfig(
                llm_config=llm_config,
                type='llm',
            )
            config.set_agent_config(agent_config)
            config.enable_default_condenser = True
        else:
            agent_config = config.get_agent_config(config.default_agent)
            agent_config.condenser = NoOpCondenserConfig(type='noop')
            config.set_agent_config(agent_config)
            config.enable_default_condenser = False

    # Determine if CLI defaults should be overridden
    val_override = args.override_cli_mode
    should_override_cli_defaults = (
        val_override is True
        or (isinstance(val_override, str) and val_override.lower() in ('true', '1'))
        or (isinstance(val_override, int) and val_override == 1)
    )

    if not should_override_cli_defaults:
        config.runtime = 'cli'
        # Set default workspace mount if not configured
        workspace_mount_path = get_workspace_mount_path(config)
        if not workspace_mount_path:
            # Set default workspace mount to current directory
            current_dir = os.getcwd()
            config.sandbox.volumes = f"{current_dir}:/workspace:rw"
        else:
            current_dir = workspace_mount_path
        config.security.confirmation_mode = True

    # Get current working directory from workspace mount
    workspace_dir = get_workspace_mount_path(config)
    if workspace_dir:
        current_dir = workspace_dir
    else:
        current_dir = os.getcwd()

    if not current_dir:
        raise ValueError('Workspace directory not specified')

    if not check_folder_security_agreement(config, current_dir):
        # User rejected, exit application
        return

    # Read task from file, CLI args, or stdin
    task_str = read_task(args, config.cli_multiline_input)

    # Show CodeActAgent welcome message
    if not banner_shown:
        clear()
        display_banner(session_id='delegation')
        
    print_formatted_text(
        HTML('<ansigreen>🎯 CodeActAgent - Task Execution &amp; Coordination</ansigreen>\n')
    )
    print_formatted_text(
        HTML('<grey>This agent will analyze your requirements and execute tasks efficiently.</grey>\n')
    )

    # Run the first session
    new_session_requested = await run_session(
        loop,
        config,
        settings_store,
        current_dir,
        task_str,
        session_name=args.name,
        skip_banner=True,  # We already showed our custom banner
    )

    # If a new session was requested, run it
    while new_session_requested:
        new_session_requested = await run_session(
            loop, config, settings_store, current_dir, None,
        )


def main():
    """Entry point for openhands2 command."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main_with_loop(loop))
    except KeyboardInterrupt:
        print('Received keyboard interrupt, shutting down...')
    except ConnectionRefusedError as e:
        print(f'Connection refused: {e}')
        sys.exit(1)
    except Exception as e:
        print(f'An error occurred: {e}')
        sys.exit(1)
    finally:
        try:
            # Cancel all running tasks
            pending = asyncio.all_tasks(loop)
            for task in pending:
                task.cancel()
            
            # Wait for all tasks to complete cancellation
            if pending:
                loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
        except Exception:
            pass
        finally:
            loop.close()


if __name__ == '__main__':
    main()