import asyncio
from pathlib import Path

from prompt_toolkit import print_formatted_text
from prompt_toolkit.shortcuts import clear, print_container
from prompt_toolkit.widgets import Frame, TextArea

from openhands.cli.settings import (
    display_settings,
    modify_llm_settings_advanced,
    modify_llm_settings_basic,
)
from openhands.cli.tui import (
    COLOR_GREY,
    UsageMetrics,
    cli_confirm,
    display_help,
    display_shutdown_message,
    display_status,
)
from openhands.cli.utils import (
    add_local_config_trusted_dir,
    get_local_config_trusted_dirs,
    read_file,
    write_to_file,
)
from openhands.core.config import (
    OpenHandsConfig,
)
from openhands.core.schema import AgentState
from openhands.events import EventSource
from openhands.events.action import (
    ChangeAgentStateAction,
    MessageAction,
)
from openhands.events.stream import EventStream
from openhands.storage.settings.file_settings_store import FileSettingsStore


async def handle_commands(
    command: str,
    event_stream: EventStream,
    usage_metrics: UsageMetrics,
    sid: str,
    config: OpenHandsConfig,
    current_dir: str,
    settings_store: FileSettingsStore,
) -> tuple[bool, bool]:
    close_repl = False
    new_session_requested = False

    if command == '/exit':
        close_repl = handle_exit_command(
            event_stream,
            usage_metrics,
            sid,
        )
    elif command == '/help':
        handle_help_command(config.default_agent)
    elif command == '/init':
        close_repl = await handle_init_command(
            config, event_stream, current_dir,
        )
    elif command == '/status':
        handle_status_command(usage_metrics, sid)
    elif command == '/new':
        close_repl, new_session_requested = handle_new_command(
            event_stream, usage_metrics, sid,
        )
    elif command == '/settings':
        await handle_settings_command(config, settings_store)
    elif command == '/resume':
        close_repl, new_session_requested = await handle_resume_command(event_stream)
    # /switchコマンドは削除（CodeActAgent2ではマイクロエージェントが自動発動）
    else:
        close_repl = True
        action = MessageAction(content=command)
        event_stream.add_event(action, EventSource.USER)

    return close_repl, new_session_requested


def handle_exit_command(
    event_stream: EventStream, usage_metrics: UsageMetrics, sid: str,
) -> bool:
    close_repl = False

    confirm_exit = (
        cli_confirm('\nセッションを終了しますか？', ['はい終了します', 'いいえ続けます']) == 0
    )

    if confirm_exit:
        event_stream.add_event(
            ChangeAgentStateAction(AgentState.STOPPED),
            EventSource.ENVIRONMENT,
        )
        display_shutdown_message(usage_metrics, sid)
        close_repl = True

    return close_repl


def handle_help_command(agent_type: str | None = None) -> None:
    display_help(agent_type)


async def handle_init_command(
    config: OpenHandsConfig, event_stream: EventStream, current_dir: str,
) -> bool:
    # Microagent functionality has been removed
    print_formatted_text(
        '\n/initコマンドは削除されました。\n',
    )
    return False


def handle_status_command(usage_metrics: UsageMetrics, sid: str) -> None:
    display_status(usage_metrics, sid)


def handle_new_command(
    event_stream: EventStream, usage_metrics: UsageMetrics, sid: str,
) -> tuple[bool, bool]:
    close_repl = False
    new_session_requested = False

    new_session_requested = (
        cli_confirm(
            '\n現在のセッションが終了し、会話履歴が失われます。\n\n続行しますか？',
            ['はい、続行', 'いいえ、やめる'],
        )
        == 0
    )

    if new_session_requested:
        close_repl = True
        new_session_requested = True
        event_stream.add_event(
            ChangeAgentStateAction(AgentState.STOPPED),
            EventSource.ENVIRONMENT,
        )
        display_shutdown_message(usage_metrics, sid)

    return close_repl, new_session_requested


async def handle_settings_command(
    config: OpenHandsConfig,
    settings_store: FileSettingsStore,
) -> None:
    display_settings(config)
    modify_settings = cli_confirm(
        '\nWhich settings would you like to modify?',
        [
            'Basic',
            'Advanced',
            'Go back',
        ],
    )

    if modify_settings == 0:
        await modify_llm_settings_basic(config, settings_store)
    elif modify_settings == 1:
        await modify_llm_settings_advanced(config, settings_store)


# FIXME: Currently there's an issue with the actual 'resume' behavior.
# Setting the agent state to RUNNING will currently freeze the agent without continuing with the rest of the task.
# This is a workaround to handle the resume command for the time being. Replace user message with the state change event once the issue is fixed.
async def handle_resume_command(
    event_stream: EventStream,
) -> tuple[bool, bool]:
    close_repl = True
    new_session_requested = False

    event_stream.add_event(
        MessageAction(content='continue'),
        EventSource.USER,
    )

    # event_stream.add_event(
    #     ChangeAgentStateAction(AgentState.RUNNING),
    #     EventSource.ENVIRONMENT,
    # )

    return close_repl, new_session_requested




def check_folder_security_agreement(config: OpenHandsConfig, current_dir: str) -> bool:
    # Directories trusted by user for the CLI to use as workspace
    # Config from ~/.openhands/config.toml overrides the app config

    app_config_trusted_dirs = config.sandbox.trusted_dirs
    local_config_trusted_dirs = get_local_config_trusted_dirs()

    trusted_dirs = local_config_trusted_dirs
    if not local_config_trusted_dirs:
        trusted_dirs = app_config_trusted_dirs

    is_trusted = current_dir in trusted_dirs

    if not is_trusted:
        security_frame = Frame(
            TextArea(
                text=(
                    f' Do you trust the files in this folder?\n\n'
                    f'   {current_dir}\n\n'
                    ' OpenHands may read and execute files in this folder with your permission.'
                ),
                style=COLOR_GREY(),
                read_only=True,
                wrap_lines=True,
            ),
            style=f'fg:{COLOR_GREY()}',
        )

        clear()
        print_container(security_frame)
        print_formatted_text('')

        confirm = (
            cli_confirm('続行しますか？', ['はい、続行', 'いいえ、終了']) == 0
        )

        if confirm:
            add_local_config_trusted_dir(current_dir)

        return confirm

    return True
