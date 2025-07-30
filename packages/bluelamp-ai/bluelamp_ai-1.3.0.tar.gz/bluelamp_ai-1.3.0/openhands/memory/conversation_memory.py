from __future__ import annotations
from typing import Generator

from litellm import ModelResponse

from openhands.core.config.agent_config import AgentConfig
from openhands.core.logger import openhands_logger as logger
from openhands.core.message import ImageContent, Message, TextContent
from openhands.core.schema import ActionType
from openhands.events.action import (
    Action,
    AgentDelegateAction,
    AgentFinishAction,
    AgentThinkAction,

    CmdRunAction,
    FileEditAction,
    FileReadAction,
    MessageAction,
)
from openhands.events.action.mcp import MCPAction
from openhands.events.action.message import SystemMessageAction
from openhands.events.event import Event
from openhands.events.observation import (
    AgentCondensationObservation,
    AgentDelegateObservation,
    AgentThinkObservation,
    BrowserOutputObservation,
    CmdOutputObservation,
    FileEditObservation,
    FileReadObservation,
    UserRejectObservation,
)
from openhands.events.observation.error import ErrorObservation
from openhands.events.observation.mcp import MCPObservation
from openhands.events.observation.observation import Observation
from openhands.events.serialization.event import truncate_content
from openhands.utils.prompt import (
    ConversationInstructions,
    PromptManager,
    RepositoryInfo,
    RuntimeInfo,
)


class ConversationMemory:
    """Processes event history into a coherent conversation for the agent."""

    def __init__(self, config: AgentConfig, prompt_manager: PromptManager):
        self.agent_config = config
        self.prompt_manager = prompt_manager
        logger.info(f"[ConversationMemory] Initialized with prompt_manager: {type(prompt_manager).__name__}")

    @staticmethod
    def _is_valid_image_url(url: str | None) -> bool:
        """Check if an image URL is valid and non-empty.

        Args:
            url: The image URL to validate

        Returns:
            True if the URL is valid, False otherwise
        """
        return bool(url and url.strip())

    def process_events(
        self,
        condensed_history: list[Event],
        initial_user_action: MessageAction,
        max_message_chars: int | None = None,
        vision_is_active: bool = False,
    ) -> list[Message]:
        """Process state history into a list of messages for the LLM.

        Ensures that tool call actions are processed correctly in function calling mode.

        Args:
            condensed_history: The condensed history of events to convert
            max_message_chars: The maximum number of characters in the content of an event included
                in the prompt to the LLM. Larger observations are truncated.
            vision_is_active: Whether vision is active in the LLM. If True, image URLs will be included.
            initial_user_action: The initial user message action, if available. Used to ensure the conversation starts correctly.
        """
        events = condensed_history

        # Ensure the event list starts with SystemMessageAction, then MessageAction(source='user')
        self._ensure_system_message(events)
        self._ensure_initial_user_message(events, initial_user_action)

        # log visual browsing status
        logger.debug(f'Visual browsing: {self.agent_config.enable_som_visual_browsing}')

        # Initialize empty messages list
        messages = []

        # Process regular events
        pending_tool_call_action_messages: dict[str, Message] = {}
        tool_call_id_to_message: dict[str, Message] = {}

        for i, event in enumerate(events):
            # create a regular message from an event
            if isinstance(event, Action):
                messages_to_add = self._process_action(
                    action=event,
                    pending_tool_call_action_messages=pending_tool_call_action_messages,
                    vision_is_active=vision_is_active,
                )
            elif isinstance(event, Observation):
                messages_to_add = self._process_observation(
                    obs=event,
                    tool_call_id_to_message=tool_call_id_to_message,
                    max_message_chars=max_message_chars,
                    vision_is_active=vision_is_active,
                    enable_som_visual_browsing=self.agent_config.enable_som_visual_browsing,
                    current_index=i,
                    events=events,
                )
            else:
                raise ValueError(f'Unknown event type: {type(event)}')

            # Check pending tool call action messages and see if they are complete
            _response_ids_to_remove = []
            for (
                response_id,
                pending_message,
            ) in pending_tool_call_action_messages.items():
                assert pending_message.tool_calls is not None, (
                    'Tool calls should NOT be None when function calling is enabled & the message is considered pending tool call. '
                    f'Pending message: {pending_message}'
                )
                if all(
                    tool_call.id in tool_call_id_to_message
                    for tool_call in pending_message.tool_calls
                ):
                    # If complete:
                    # -- 1. Add the message that **initiated** the tool calls
                    messages_to_add.append(pending_message)
                    # -- 2. Add the tool calls **results***
                    for tool_call in pending_message.tool_calls:
                        messages_to_add.append(tool_call_id_to_message[tool_call.id])
                        tool_call_id_to_message.pop(tool_call.id)
                    _response_ids_to_remove.append(response_id)
            # Cleanup the processed pending tool messages
            for response_id in _response_ids_to_remove:
                pending_tool_call_action_messages.pop(response_id)

            messages += messages_to_add

        # Apply final filtering so that the messages in context don't have unmatched tool calls
        # and tool responses, for example
        messages = list(ConversationMemory._filter_unmatched_tool_calls(messages))

        # Apply final formatting
        messages = self._apply_user_message_formatting(messages)

        return messages

    def _apply_user_message_formatting(self, messages: list[Message]) -> list[Message]:
        """Applies formatting rules, such as adding newlines between consecutive user messages."""
        formatted_messages = []
        prev_role = None
        for msg in messages:
            # Add double newline between consecutive user messages
            if msg.role == 'user' and prev_role == 'user' and len(msg.content) > 0:
                # Find the first TextContent in the message to add newlines
                for content_item in msg.content:
                    if isinstance(content_item, TextContent):
                        # Prepend two newlines to ensure visual separation
                        content_item.text = '\n\n' + content_item.text
                        break
            formatted_messages.append(msg)
            prev_role = msg.role  # Update prev_role after processing each message
        return formatted_messages

    def _process_action(
        self,
        action: Action,
        pending_tool_call_action_messages: dict[str, Message],
        vision_is_active: bool = False,
    ) -> list[Message]:
        """Converts an action into a message format that can be sent to the LLM.

        This method handles different types of actions and formats them appropriately:
        1. For tool-based actions (AgentDelegate, CmdRun, FileEdit) and agent-sourced AgentFinish:
            - In function calling mode: Stores the LLM's response in pending_tool_call_action_messages
            - In non-function calling mode: Creates a message with the action string
        2. For MessageActions: Creates a message with the text content and optional image content

        Args:
            action: The action to convert. Can be one of:
                - CmdRunAction: For executing bash commands
                - FileEditAction: For editing files
                - FileReadAction: For reading files using openhands-aci commands

                - AgentFinishAction: For ending the interaction
                - MessageAction: For sending messages
                - MCPAction: For interacting with the MCP server
            pending_tool_call_action_messages: Dictionary mapping response IDs to their corresponding messages.
                Used in function calling mode to track tool calls that are waiting for their results.

            vision_is_active: Whether vision is active in the LLM. If True, image URLs will be included

        Returns:
            list[Message]: A list containing the formatted message(s) for the action.
                May be empty if the action is handled as a tool call in function calling mode.

        Note:
            In function calling mode, tool-based actions are stored in pending_tool_call_action_messages
            rather than being returned immediately. They will be processed later when all corresponding
            tool call results are available.
        """
        # create a regular message from an event
        if isinstance(
            action,
            (
                AgentDelegateAction,
                AgentThinkAction,
                FileEditAction,
                FileReadAction,

                MCPAction,
            ),
        ) or (isinstance(action, CmdRunAction) and action.source == 'agent'):
            tool_metadata = action.tool_call_metadata
            assert tool_metadata is not None, (
                'Tool call metadata should NOT be None when function calling is enabled. Action: '
                + str(action)
            )

            llm_response: ModelResponse = tool_metadata.model_response
            assistant_msg = getattr(llm_response.choices[0], 'message')

            # Add the LLM message (assistant) that initiated the tool calls
            # (overwrites any previous message with the same response_id)
            logger.debug(
                f'Tool calls type: {type(assistant_msg.tool_calls)}, value: {assistant_msg.tool_calls}'
            )
            pending_tool_call_action_messages[llm_response.id] = Message(
                role=getattr(assistant_msg, 'role', 'assistant'),
                # tool call content SHOULD BE a string
                content=[TextContent(text=assistant_msg.content)]
                if assistant_msg.content and assistant_msg.content.strip()
                else [],
                tool_calls=assistant_msg.tool_calls,
            )
            return []
        elif isinstance(action, AgentFinishAction):
            role = 'user' if action.source == 'user' else 'assistant'

            # when agent finishes, it has tool_metadata
            # which has already been executed, and it doesn't have a response
            # when the user finishes (/exit), we don't have tool_metadata
            tool_metadata = action.tool_call_metadata
            if tool_metadata is not None:
                # take the response message from the tool call
                assistant_msg = getattr(
                    tool_metadata.model_response.choices[0], 'message'
                )
                content = assistant_msg.content or ''

                # save content if any, to thought
                if action.thought:
                    if action.thought != content:
                        action.thought += '\n' + content
                else:
                    action.thought = content

                # remove the tool call metadata
                action.tool_call_metadata = None
            if role not in ('user', 'system', 'assistant', 'tool'):
                raise ValueError(f'Invalid role: {role}')
            return [
                Message(
                    role=role,  # type: ignore[arg-type]
                    content=[TextContent(text=action.thought)],
                )
            ]
        elif isinstance(action, MessageAction):
            role = 'user' if action.source == 'user' else 'assistant'
            content = [TextContent(text=action.content or '')]
            if vision_is_active and action.image_urls:
                content.append(ImageContent(image_urls=action.image_urls))
            if role not in ('user', 'system', 'assistant', 'tool'):
                raise ValueError(f'Invalid role: {role}')
            return [
                Message(
                    role=role,  # type: ignore[arg-type]
                    content=content,
                )
            ]
        elif isinstance(action, CmdRunAction) and action.source == 'user':
            content = [
                TextContent(text=f'User executed the command:\n{action.command}')
            ]
            return [
                Message(
                    role='user',  # Always user for CmdRunAction
                    content=content,
                )
            ]
        elif isinstance(action, SystemMessageAction):
            # Convert SystemMessageAction to a system message
            return [
                Message(
                    role='system',
                    content=[TextContent(text=action.content)],
                    # Include tools if function calling is enabled
                    tool_calls=None,
                )
            ]
        return []

    def _process_observation(
        self,
        obs: Observation,
        tool_call_id_to_message: dict[str, Message],
        max_message_chars: int | None = None,
        vision_is_active: bool = False,
        enable_som_visual_browsing: bool = False,
        current_index: int = 0,
        events: list[Event] | None = None,
    ) -> list[Message]:
        """Converts an observation into a message format that can be sent to the LLM.

        This method handles different types of observations and formats them appropriately:
        - CmdOutputObservation: Formats command execution results with exit codes
        - FileEditObservation: Formats file editing results
        - FileReadObservation: Formats file reading results from openhands-aci
        - AgentDelegateObservation: Formats results from delegated agent tasks
        - ErrorObservation: Formats error messages from failed actions
        - UserRejectObservation: Formats user rejection messages

        In function calling mode, observations with tool_call_metadata are stored in
        tool_call_id_to_message for later processing instead of being returned immediately.

        Args:
            obs: The observation to convert
            tool_call_id_to_message: Dictionary mapping tool call IDs to their corresponding messages (used in function calling mode)
            max_message_chars: The maximum number of characters in the content of an observation included in the prompt to the LLM
            vision_is_active: Whether vision is active in the LLM. If True, image URLs will be included
            enable_som_visual_browsing: Whether to enable visual browsing for the SOM model
            current_index: The index of the current event in the events list (for deduplication)
            events: The list of all events (for deduplication)

        Returns:
            list[Message]: A list containing the formatted message(s) for the observation.
                May be empty if the observation is handled as a tool response in function calling mode.

        Raises:
            ValueError: If the observation type is unknown
        """
        message: Message

        if isinstance(obs, CmdOutputObservation):
            # if it doesn't have tool call metadata, it was triggered by a user action
            if obs.tool_call_metadata is None:
                text = truncate_content(
                    f'\nObserved result of command executed by user:\n{obs.to_agent_observation()}',
                    max_message_chars,
                )
            else:
                text = truncate_content(obs.to_agent_observation(), max_message_chars)
            message = Message(role='user', content=[TextContent(text=text)])
        elif isinstance(obs, MCPObservation):
            # logger.warning(f'MCPObservation: {obs}')
            text = truncate_content(obs.content, max_message_chars)
            message = Message(role='user', content=[TextContent(text=text)])

        elif isinstance(obs, FileEditObservation):
            text = truncate_content(str(obs), max_message_chars)
            message = Message(role='user', content=[TextContent(text=text)])
        elif isinstance(obs, FileReadObservation):
            message = Message(
                role='user', content=[TextContent(text=obs.content)]
            )  # Content is already truncated by openhands-aci
        elif isinstance(obs, BrowserOutputObservation):
            text = obs.content
            if (
                obs.trigger_by_action == ActionType.BROWSE_INTERACTIVE
                and enable_som_visual_browsing
                and vision_is_active
            ):
                text += 'Image: Current webpage screenshot (Note that only visible portion of webpage is present in the screenshot. You may need to scroll to view the remaining portion of the web-page.)\n'

                # Determine which image to use and validate it
                image_url = None
                if obs.set_of_marks is not None and len(obs.set_of_marks) > 0:
                    image_url = obs.set_of_marks
                    image_type = 'set of marks'
                elif obs.screenshot is not None and len(obs.screenshot) > 0:
                    image_url = obs.screenshot
                    image_type = 'screenshot'

                # Create message content with text
                content = [TextContent(text=text)]

                # Only add ImageContent if we have a valid image URL
                if self._is_valid_image_url(image_url):
                    content.append(ImageContent(image_urls=[image_url]))  # type: ignore
                    logger.debug(f'Vision enabled for browsing, showing {image_type}')
                else:
                    if image_url:
                        logger.warning(
                            f'Invalid image URL format for {image_type}: {image_url[:50]}...'
                        )
                        # Add text indicating the image was filtered
                        content[
                            0
                        ].text += f'\n\nNote: The {image_type} for this webpage was invalid or empty and has been filtered. The agent should use alternative methods to access visual information about the webpage.'
                    else:
                        logger.debug(
                            'Vision enabled for browsing, but no valid image available'
                        )
                        # Add text indicating no image was available
                        content[
                            0
                        ].text += '\n\nNote: No visual information (screenshot or set of marks) is available for this webpage. The agent should rely on the text content above.'

                message = Message(role='user', content=content)  # type: ignore
            else:
                message = Message(
                    role='user',
                    content=[TextContent(text=text)],
                )
                logger.debug('Vision disabled for browsing, showing text')
        elif isinstance(obs, AgentDelegateObservation):
            text = truncate_content(
                obs.outputs.get('content', obs.content),
                max_message_chars,
            )
            message = Message(role='user', content=[TextContent(text=text)])
        elif isinstance(obs, AgentThinkObservation):
            text = truncate_content(obs.content, max_message_chars)
            message = Message(role='user', content=[TextContent(text=text)])
        elif isinstance(obs, ErrorObservation):
            text = truncate_content(obs.content, max_message_chars)
            text += '\n[Error occurred in processing last action]'
            message = Message(role='user', content=[TextContent(text=text)])
        elif isinstance(obs, UserRejectObservation):
            text = 'OBSERVATION:\n' + truncate_content(obs.content, max_message_chars)
            text += '\n[Last action has been rejected by the user]'
            message = Message(role='user', content=[TextContent(text=text)])
        elif isinstance(obs, AgentCondensationObservation):
            text = truncate_content(obs.content, max_message_chars)
            message = Message(role='user', content=[TextContent(text=text)])
        else:
            # If an observation message is not returned, it will cause an error
            # when the LLM tries to return the next message
            raise ValueError(f'Unknown observation type: {type(obs)}')

        # Update the message as tool response properly
        if (tool_call_metadata := getattr(obs, 'tool_call_metadata', None)) is not None:
            tool_call_id_to_message[tool_call_metadata.tool_call_id] = Message(
                role='tool',
                content=message.content,
                tool_call_id=tool_call_metadata.tool_call_id,
                name=tool_call_metadata.function_name,
            )
            # No need to return the observation message
            # because it will be added by get_action_message when all the corresponding
            # tool calls in the SAME request are processed
            return []

        return [message]

    def apply_prompt_caching(self, messages: list[Message]) -> None:
        """Applies caching breakpoints to the messages.

        For new Anthropic API, we only need to mark the last user or tool message as cacheable.
        """
        if len(messages) > 0 and messages[0].role == 'system':
            messages[0].content[-1].cache_prompt = True
        # NOTE: this is only needed for anthropic
        for message in reversed(messages):
            if message.role in ('user', 'tool'):
                message.content[
                    -1
                ].cache_prompt = True  # Last item inside the message content
                break


    @staticmethod
    def _filter_unmatched_tool_calls(
        messages: list[Message],
    ) -> Generator[Message, None, None]:
        """Filter out tool calls that don't have matching tool responses and vice versa.

        This ensures that every tool_call_id in a tool message has a corresponding tool_calls[].id
        in an assistant message, and vice versa. The original list is unmodified, when tool_calls is
        updated the message is copied.

        This does not remove items with id set to None.
        """
        tool_call_ids = {
            tool_call.id
            for message in messages
            if message.tool_calls
            for tool_call in message.tool_calls
            if message.role == 'assistant' and tool_call.id
        }
        tool_response_ids = {
            message.tool_call_id
            for message in messages
            if message.role == 'tool' and message.tool_call_id
        }

        for message in messages:
            # Remove tool messages with no matching assistant tool call
            if message.role == 'tool' and message.tool_call_id:
                if message.tool_call_id in tool_call_ids:
                    yield message

            # Remove assistant tool calls with no matching tool response
            elif message.role == 'assistant' and message.tool_calls:
                all_tool_calls_match = all(
                    tool_call.id in tool_response_ids
                    for tool_call in message.tool_calls
                )
                if all_tool_calls_match:
                    yield message
                else:
                    matched_tool_calls = [
                        tool_call
                        for tool_call in message.tool_calls
                        if tool_call.id in tool_response_ids
                    ]

                    if matched_tool_calls:
                        # Keep an updated message if there are tools calls left
                        yield message.model_copy(
                            update={'tool_calls': matched_tool_calls}
                        )
            else:
                # Any other case is kept
                yield message

    def _ensure_system_message(self, events: list[Event]) -> None:
        """Checks if a SystemMessageAction exists and adds one if not (for legacy compatibility)."""
        # Check if there's a SystemMessageAction in the events
        has_system_message = any(
            isinstance(event, SystemMessageAction) for event in events
        )

        # Legacy behavior: If no SystemMessageAction is found, add one
        if not has_system_message:
            logger.debug(
                '[ConversationMemory] No SystemMessageAction found in events. '
                'Adding one for backward compatibility. '
            )
            # Debug logging
            logger.info(f"[ConversationMemory] Prompt manager type: {type(self.prompt_manager).__name__}")
            if hasattr(self.prompt_manager, 'system_prompt_filename'):
                logger.info(f"[ConversationMemory] System prompt filename: {self.prompt_manager.system_prompt_filename}")
            
            system_prompt = self.prompt_manager.get_system_message()
            if system_prompt:
                system_message = SystemMessageAction(content=system_prompt)
                # Insert the system message directly at the beginning of the events list
                events.insert(0, system_message)
                logger.info(
                    '[ConversationMemory] Added SystemMessageAction for backward compatibility'
                )
                # Log a preview of the system prompt
                preview = system_prompt[:200] if len(system_prompt) > 200 else system_prompt
                logger.info(f"[ConversationMemory] System prompt preview: {preview}...")

    def _ensure_initial_user_message(
        self, events: list[Event], initial_user_action: MessageAction
    ) -> None:
        """Checks if the second event is a user MessageAction and inserts the provided one if needed."""
        if (
            not events
        ):  # Should have system message from previous step, but safety check
            logger.error('Cannot ensure initial user message: event list is empty.')
            # Or raise? Let's log for now, _ensure_system_message should handle this.
            return

        # We expect events[0] to be SystemMessageAction after _ensure_system_message
        if len(events) == 1:
            # Only system message exists
            logger.info(
                'Initial user message action was missing. Inserting the initial user message.'
            )
            events.insert(1, initial_user_action)
        elif not isinstance(events[1], MessageAction) or events[1].source != 'user':
            # The second event exists but is not the correct initial user message action.
            # We will insert the correct one provided.
            logger.info(
                'Second event was not the initial user message action. Inserting correct one at index 1.'
            )

            # Insert the user message event at index 1. This will be the second message as LLM APIs expect
            # but something was wrong with the history, so log all we can.
            events.insert(1, initial_user_action)

        # Else: events[1] is already a user MessageAction.
        # Check if it matches the one provided (if any discrepancy, log warning but proceed).
        elif events[1] != initial_user_action:
            logger.debug(
                'The user MessageAction at index 1 does not match the provided initial_user_action. '
                'Proceeding with the one found in condensed history.'
            )
