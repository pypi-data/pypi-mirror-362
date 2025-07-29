# CLI TUI input and output functions
# Handles all input and output to the console
# CLI Settings are handled separately in cli_settings.py

import asyncio
import sys
import threading
import time
from collections.abc import Generator
from typing import Callable

from prompt_toolkit import PromptSession, print_formatted_text
from prompt_toolkit.application import Application
from prompt_toolkit.completion import CompleteEvent, Completer, Completion
from prompt_toolkit.document import Document
from prompt_toolkit.formatted_text import HTML, FormattedText, StyleAndTextTuples
from prompt_toolkit.input import create_input
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.key_processor import KeyPressEvent
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.lexers import Lexer
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.shortcuts import print_container
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import Frame, TextArea

from openhands import __version__
from openhands.cli.branding import COLORS, STYLE_DICT, MESSAGES, COMMAND_DESCRIPTIONS, get_message
from openhands.core.config import OpenHandsConfig
from openhands.core.exceptions import UserCancelledError
from openhands.core.schema import AgentState
from openhands.events import EventSource, EventStream
from openhands.events.action import (
    Action,
    ActionConfirmationStatus,
    ChangeAgentStateAction,
    CmdRunAction,
    MessageAction,
)
from openhands.events.event import Event
from openhands.events.observation import (
    AgentStateChangedObservation,
    CmdOutputObservation,
    ErrorObservation,
    FileEditObservation,
    FileReadObservation,
)
from openhands.llm.metrics import Metrics


print_lock = threading.Lock()


# Branding utility functions
def get_default_style():
    """現在のブランドに応じたスタイルを返す"""
    from .branding import get_style_dict
    return Style.from_dict(get_style_dict())

def get_color_grey():
    """Get grey color from current branding."""
    from .branding import get_current_colors
    return get_current_colors()['grey']

def get_color_gold():
    """Get primary color from current branding."""
    from .branding import get_current_colors
    return get_current_colors()['primary']

def get_commands():
    """Get command descriptions from current branding."""
    from .branding import get_current_command_descriptions
    return get_current_command_descriptions()

# 後方互換性のための定数（動的評価）
DEFAULT_STYLE = get_default_style
COLOR_GREY = get_color_grey
COLOR_GOLD = get_color_gold
COMMANDS = get_commands


class UsageMetrics:
    def __init__(self) -> None:
        self.metrics: Metrics = Metrics()
        self.session_init_time: float = time.time()


class CustomDiffLexer(Lexer):
    """Custom lexer for the specific diff format."""

    def lex_document(self, document: Document) -> Callable[[int], StyleAndTextTuples]:
        lines = document.lines

        def get_line(lineno: int) -> StyleAndTextTuples:
            line = lines[lineno]
            if line.startswith('+'):
                return [('ansigreen', line)]
            if line.startswith('-'):
                return [('ansired', line)]
            if line.startswith('[') or line.startswith('('):
                # Style for metadata lines like [Existing file...] or (content...)
                return [('bold', line)]
            # Default style for other lines
            return [('', line)]

        return get_line


# CLI initialization and startup display functions
def display_runtime_initialization_message(runtime: str) -> None:
    print_formatted_text('')
    if runtime == 'local':
        print_formatted_text(HTML('<grey>⚙️ Starting local runtime...</grey>'))
    print_formatted_text('')


def display_initialization_animation(text: str, is_loaded: asyncio.Event) -> None:
    ANIMATION_FRAMES = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']

    i = 0
    while not is_loaded.is_set():
        sys.stdout.write('\n')
        sys.stdout.write(
            f'\033[s\033[J\033[38;2;255;215;0m[{ANIMATION_FRAMES[i % len(ANIMATION_FRAMES)]}] {text}\033[0m\033[u\033[1A',
        )
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1

    sys.stdout.write('\r' + ' ' * (len(text) + 10) + '\r')
    sys.stdout.flush()


def display_banner(session_id: str) -> None:
    import os
    import getpass
    from .branding import get_current_banner, get_current_brand_name
    
    # 動的バナー表示
    banner = get_current_banner()
    print_formatted_text(
        HTML(banner),
        style=get_default_style(),
    )

    # セッション情報を表示
    current_dir = os.getcwd()
    current_user = getpass.getuser()
    
    print_formatted_text(HTML(f'<grey>セッションディレクトリ：</grey><yellow>{current_dir}</yellow>'))
    print_formatted_text(HTML(f'<grey>ログインユーザー：</grey><cyan>{current_user}</cyan>'))
    print_formatted_text(HTML(f'<grey>モード：</grey><green>新規プロジェクト</green>'))
    print_formatted_text('')


def display_welcome_message(message: str = '') -> None:
    # ウェルカムメッセージを表示しない（コメントアウト）
    pass


def display_initial_user_prompt(prompt: str) -> None:
    print_formatted_text(
        FormattedText(
            [
                ('', '\n'),
                (COLORS()['primary'], '> '),
                ('', prompt),
            ],
        ),
    )


# Prompt output display functions
def display_event(event: Event, config: OpenHandsConfig) -> None:
    with print_lock:
        if isinstance(event, Action):
            if hasattr(event, 'thought'):
                display_message(event.thought)
            if hasattr(event, 'final_thought'):
                display_message(event.final_thought)
        if isinstance(event, MessageAction):
            if event.source == EventSource.AGENT:
                display_message(event.content)

        if isinstance(event, CmdRunAction):
            # Only display the command if it's not already confirmed
            # Commands are always shown when AWAITING_CONFIRMATION, so we don't need to show them again when CONFIRMED
            if event.confirmation_state != ActionConfirmationStatus.CONFIRMED:
                display_command(event)

            if event.confirmation_state == ActionConfirmationStatus.CONFIRMED:
                pass  # Already displayed
        elif isinstance(event, CmdOutputObservation):
            display_command_output(event.content)
        elif isinstance(event, FileEditObservation):
            display_file_edit(event)
        elif isinstance(event, FileReadObservation):
            display_file_read(event)
        elif isinstance(event, AgentStateChangedObservation):
            display_agent_state_change_message(event.agent_state)
        elif isinstance(event, ErrorObservation):
            display_error(event.content)


def display_message(message: str) -> None:
    message = message.strip()

    if message:
        print_formatted_text(f'\n{message}')


def display_error(error: str) -> None:
    error = error.strip()

    if error:
        container = Frame(
            TextArea(
                text=error,
                read_only=True,
                style='ansired',
                wrap_lines=True,
            ),
            title='エラー',
            style='ansired',
        )
        print_formatted_text('')
        print_container(container)


def display_command(event: CmdRunAction) -> None:
    container = Frame(
        TextArea(
            text=f'$ {event.command}',
            read_only=True,
            style=COLOR_GREY(),
            wrap_lines=True,
        ),
        title='コマンド',
        style='ansiblue',
    )
    print_formatted_text('')
    print_container(container)


def display_command_output(output: str) -> None:
    lines = output.split('\n')
    formatted_lines = []
    for line in lines:
        if line.startswith('[Python Interpreter') or line.startswith('openhands@'):
            # TODO: clean this up once we clean up terminal output
            continue
        formatted_lines.append(line)
        formatted_lines.append('\n')

    # Remove the last newline if it exists
    if formatted_lines:
        formatted_lines.pop()

    container = Frame(
        TextArea(
            text=''.join(formatted_lines),
            read_only=True,
            style=COLOR_GREY(),
            wrap_lines=True,
        ),
        title='コマンド出力',
        style=f'fg:{COLOR_GREY()}',
    )
    print_formatted_text('')
    print_container(container)


def display_file_edit(event: FileEditObservation) -> None:
    container = Frame(
        TextArea(
            text=event.visualize_diff(n_context_lines=4),
            read_only=True,
            wrap_lines=True,
            lexer=CustomDiffLexer(),
        ),
        title='ファイル編集',
        style=f'fg:{COLOR_GREY()}',
    )
    print_formatted_text('')
    print_container(container)


def display_file_read(event: FileReadObservation) -> None:
    content = event.content.replace('\t', ' ')
    container = Frame(
        TextArea(
            text=content,
            read_only=True,
            style=COLOR_GREY(),
            wrap_lines=True,
        ),
        title='ファイル読み込み',
        style=f'fg:{COLOR_GREY()}',
    )
    print_formatted_text('')
    print_container(container)




# Interactive command output display functions
def display_help(agent_type: str | None = None) -> None:
    # Version header and introduction
    print_formatted_text(
        HTML(
            f'\n<grey>OpenHands CLI v{__version__}</grey>\n'
            '<gold>OpenHands CLI lets you interact with the OpenHands agent from the command line.</gold>\n',
        ),
    )

    # Usage examples
    print_formatted_text('Things that you can try:')
    print_formatted_text(
        HTML(
            '• Ask questions about the codebase <grey>> How does main.py work?</grey>\n'
            '• Edit files or add new features <grey>> Add a new function to ...</grey>\n'
            '• Find and fix issues <grey>> Fix the type error in ...</grey>\n',
        ),
    )

    # Tips section
    print_formatted_text(
        'Some tips to get the most out of OpenHands:\n'
        '• Be as specific as possible about the desired outcome or the problem to be solved.\n'
        '• Provide context, including relevant file paths and line numbers if available.\n'
        '• Break large tasks into smaller, manageable prompts.\n'
        '• Include relevant error messages or logs.\n'
        '• Specify the programming language or framework, if not obvious.\n',
    )

    # Commands section
    print_formatted_text(HTML('Interactive commands:'))
    commands_html = ''
    
    # 基本コマンドを表示
    for command, description in COMMANDS().items():  # type: ignore
        commands_html += f'<gold><b>{command}</b></gold> - <grey>{description}</grey>\n'
    
    # CodeActAgent2専用情報を追加
    if agent_type == 'CodeActAgent2':
        commands_html += '\n<ansigreen>CodeActAgent2 マイクロエージェント:</ansigreen>\n'
        commands_html += '<gold><b>debug, error</b></gold> - <grey>デバッグ探偵が自動発動</grey>\n'
        commands_html += '<gold><b>feature, extension</b></gold> - <grey>機能拡張プランナーが自動発動</grey>\n'
        commands_html += '<gold><b>refactor, cleanup</b></gold> - <grey>リファクタリングマネージャーが自動発動</grey>\n'
    
    print_formatted_text(HTML(commands_html))

    # Footer
    print_formatted_text(
        HTML(
            '<grey>詳細はこちら: https://docs.all-hands.dev/usage/getting-started</grey>',
        ),
    )


def display_usage_metrics(usage_metrics: UsageMetrics) -> None:
    cost_str = f'${usage_metrics.metrics.accumulated_cost:.6f}'
    input_tokens_str = (
        f'{usage_metrics.metrics.accumulated_token_usage.prompt_tokens:,}'
    )
    cache_read_str = (
        f'{usage_metrics.metrics.accumulated_token_usage.cache_read_tokens:,}'
    )
    cache_write_str = (
        f'{usage_metrics.metrics.accumulated_token_usage.cache_write_tokens:,}'
    )
    output_tokens_str = (
        f'{usage_metrics.metrics.accumulated_token_usage.completion_tokens:,}'
    )
    total_tokens_str = f'{usage_metrics.metrics.accumulated_token_usage.prompt_tokens + usage_metrics.metrics.accumulated_token_usage.completion_tokens:,}'

    labels_and_values = [
        ('   総コスト (USD):', cost_str),
        ('', ''),
        ('   入力トークン数:', input_tokens_str),
        ('      キャッシュヒット:', cache_read_str),
        ('      キャッシュ書き込み:', cache_write_str),
        ('   出力トークン数:', output_tokens_str),
        ('', ''),
        ('   総トークン数:', total_tokens_str),
    ]

    # Calculate max widths for alignment
    max_label_width = max(len(label) for label, _ in labels_and_values)
    max_value_width = max(len(value) for _, value in labels_and_values)

    # Construct the summary text with aligned columns
    summary_lines = [
        f'{label:<{max_label_width}} {value:<{max_value_width}}'
        for label, value in labels_and_values
    ]
    summary_text = '\n'.join(summary_lines)

    container = Frame(
        TextArea(
            text=summary_text,
            read_only=True,
            style=COLOR_GREY(),
            wrap_lines=True,
        ),
        title='使用量統計',
        style=f'fg:{COLOR_GREY()}',
    )

    print_container(container)


def get_session_duration(session_init_time: float) -> str:
    current_time = time.time()
    session_duration = current_time - session_init_time
    hours, remainder = divmod(session_duration, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f'{int(hours)}h {int(minutes)}m {int(seconds)}s'


def display_shutdown_message(usage_metrics: UsageMetrics, session_id: str) -> None:
    duration_str = get_session_duration(usage_metrics.session_init_time)

    print_formatted_text(HTML('<grey>Closing current conversation...</grey>'))
    print_formatted_text('')
    display_usage_metrics(usage_metrics)
    print_formatted_text('')
    print_formatted_text(HTML(f'<grey>Conversation duration: {duration_str}</grey>'))
    print_formatted_text('')
    print_formatted_text(HTML(f'<grey>Closed conversation {session_id}</grey>'))
    print_formatted_text('')


def display_status(usage_metrics: UsageMetrics, session_id: str) -> None:
    duration_str = get_session_duration(usage_metrics.session_init_time)

    print_formatted_text('')
    print_formatted_text(HTML(f'<grey>Conversation ID: {session_id}</grey>'))
    print_formatted_text(HTML(f'<grey>Uptime:          {duration_str}</grey>'))
    print_formatted_text('')
    display_usage_metrics(usage_metrics)


def display_agent_running_message() -> None:
    print_formatted_text('')
    print_formatted_text(
        HTML(f'<blue>{get_message("agent_running")}</blue> <grey>(Ctrl-Pで一時停止)</grey>'),
        style=get_default_style(),
    )


def display_agent_state_change_message(agent_state: str) -> None:
    if agent_state == AgentState.PAUSED:
        print_formatted_text('')
        print_formatted_text(
            HTML(
                f'<blue>{get_message("agent_paused")}</blue> <grey>(/resumeで続行)</grey>',
            ),
            style=get_default_style(),
        )
    elif agent_state == AgentState.FINISHED:
        print_formatted_text('')
        print_formatted_text(HTML(f'<blue>{get_message("agent_finished")}</blue>'), style=get_default_style())
    elif agent_state == AgentState.AWAITING_USER_INPUT:
        print_formatted_text('')
        print_formatted_text(HTML(f'<blue>{get_message("agent_waiting")}</blue>'), style=get_default_style())


# Common input functions
class CommandCompleter(Completer):
    """Custom completer for commands."""

    def __init__(self, agent_state: str, agent_type: str | None = None) -> None:
        super().__init__()
        self.agent_state = agent_state
        self.agent_type = agent_type

    def get_completions(
        self, document: Document, complete_event: CompleteEvent,
    ) -> Generator[Completion, None, None]:
        # コマンド補完機能を無効化
        # ファイルパス入力時のエラーを防ぐため、補完候補を返さない
        return
        yield  # unreachable code to satisfy generator type


def create_prompt_session() -> PromptSession[str]:
    return PromptSession(style=get_default_style())


async def read_prompt_input(agent_state: str, multiline: bool = False, agent_type: str | None = None) -> str:
    try:
        prompt_session = create_prompt_session()
        prompt_session.completer = (
            CommandCompleter(agent_state, agent_type) if not multiline else None
        )

        if multiline:
            kb = KeyBindings()

            @kb.add('c-d')
            def _(event: KeyPressEvent) -> None:
                event.current_buffer.validate_and_handle()

            with patch_stdout():
                print_formatted_text('')
                message = await prompt_session.prompt_async(
                    HTML(
                        '<gold>Enter your message and press Ctrl-D to finish:</gold>\n',
                    ),
                    multiline=True,
                    key_bindings=kb,
                )
        else:
            with patch_stdout():
                print_formatted_text('')
                message = await prompt_session.prompt_async(
                    HTML('<gold>> </gold>'),
                )
        return message if message is not None else ''
    except (KeyboardInterrupt, EOFError):
        return '/exit'


async def read_confirmation_input() -> str:
    try:
        prompt_session = create_prompt_session()

        with patch_stdout():
            print_formatted_text('')
            confirmation: str = await prompt_session.prompt_async(
                HTML('<gold>実行を進めていいですか？ h(はい)/i(いいえ)/t(つねに許可) > </gold>'),
            )

            confirmation = '' if confirmation is None else confirmation.strip().lower()

            if confirmation in ['h', 'はい']:
                return 'yes'
            if confirmation in ['i', 'いいえ']:
                return 'no'
            if confirmation in ['t', 'つねに', 'つねに許可']:
                return 'always'
            return 'no'
    except (KeyboardInterrupt, EOFError):
        return 'no'


async def process_agent_pause(done: asyncio.Event, event_stream: EventStream) -> None:
    input = create_input()

    def keys_ready() -> None:
        for key_press in input.read_keys():
            if (
                key_press.key == Keys.ControlP
                or key_press.key == Keys.ControlC
                or key_press.key == Keys.ControlD
            ):
                print_formatted_text('')
                print_formatted_text(HTML('<gold>エージェントの動作をキャンセルしています...</gold>'))
                event_stream.add_event(
                    ChangeAgentStateAction(AgentState.PAUSED),
                    EventSource.USER,
                )
                done.set()

    with input.raw_mode():
        with input.attach(keys_ready):
            await done.wait()


def cli_confirm(
    question: str = 'Are you sure?', choices: list[str] | None = None,
) -> int:
    """Display a confirmation prompt with the given question and choices.

    Returns the index of the selected choice.
    """
    if choices is None:
        choices = ['Yes', 'No']
    selected = [0]  # Using list to allow modification in closure

    def get_choice_text() -> list:
        return [
            ('class:question', f'{question}\n\n'),
        ] + [
            (
                'class:selected' if i == selected[0] else 'class:unselected',
                f'{"> " if i == selected[0] else "  "}{choice}\n',
            )
            for i, choice in enumerate(choices)
        ]

    kb = KeyBindings()

    @kb.add('up')
    def _(event: KeyPressEvent) -> None:
        selected[0] = (selected[0] - 1) % len(choices)

    @kb.add('down')
    def _(event: KeyPressEvent) -> None:
        selected[0] = (selected[0] + 1) % len(choices)

    @kb.add('enter')
    def _(event: KeyPressEvent) -> None:
        event.app.exit(result=selected[0])

    style = Style.from_dict({'selected': COLOR_GOLD(), 'unselected': ''})

    layout = Layout(
        HSplit(
            [
                Window(
                    FormattedTextControl(get_choice_text),
                    always_hide_cursor=True,
                ),
            ],
        ),
    )

    app: Application[int] = Application(
        layout=layout,
        key_bindings=kb,
        style=style,
        mouse_support=True,
        full_screen=False,
    )

    return app.run(in_thread=True)


def kb_cancel() -> KeyBindings:
    """Custom key bindings to handle ESC as a user cancellation."""
    bindings = KeyBindings()

    @bindings.add('escape')
    def _(event: KeyPressEvent) -> None:
        event.app.exit(exception=UserCancelledError, style='class:aborting')

    return bindings

