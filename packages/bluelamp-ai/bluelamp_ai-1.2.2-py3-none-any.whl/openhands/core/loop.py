import asyncio

from openhands.controller import AgentController
from openhands.core.error_handler import handle_malformed_action_error
from openhands.core.exceptions import LLMMalformedActionError
from openhands.core.logger import openhands_logger as logger
from openhands.core.schema import AgentState
from openhands.memory.memory import Memory
from openhands.runtime.base import Runtime


async def run_agent_until_done(
    controller: AgentController,
    runtime: Runtime,
    memory: Memory,
    end_states: list[AgentState],
) -> None:
    """run_agent_until_done takes a controller and a runtime, and will run
    the agent until it reaches a terminal state.
    Note that runtime must be connected before being passed in here.
    """

    def status_callback(msg_type: str, msg_id: str, msg: str) -> None:
        if msg_type == 'error':
            # Check if this is a recoverable error (like path restriction)
            is_recoverable = False
            if 'LLMMalformedActionError' in msg and 'Invalid path' in msg:
                # This is a path restriction error - recoverable
                is_recoverable = True
                logger.warning(f'Recoverable path error: {msg}')
            elif msg_id == 'STATUS$ERROR_RUNTIME_DISCONNECTED':
                # Runtime disconnection is critical
                logger.error(f'Critical runtime error: {msg}')
            else:
                # Check if it's a known recoverable error pattern
                recoverable_patterns = [
                    'You can only work with files in',
                    'Invalid path',
                    'Path access restricted'
                ]
                is_recoverable = any(pattern in msg for pattern in recoverable_patterns)
                
                if is_recoverable:
                    logger.warning(f'Recoverable error: {msg}')
                else:
                    logger.error(f'Critical error: {msg}')
            
            if controller and not is_recoverable:
                # Only set ERROR state for critical errors
                controller.state.last_error = msg
                asyncio.create_task(controller.set_agent_state_to(AgentState.ERROR))
            elif controller and is_recoverable:
                # For recoverable errors, just log and continue
                controller.state.last_error = ''
        else:
            logger.info(msg)

    if hasattr(runtime, 'status_callback') and runtime.status_callback:
        raise ValueError(
            'Runtime status_callback was set, but run_agent_until_done will override it',
        )
    if hasattr(controller, 'status_callback') and controller.status_callback:
        raise ValueError(
            'Controller status_callback was set, but run_agent_until_done will override it',
        )

    runtime.status_callback = status_callback
    controller.status_callback = status_callback
    memory.status_callback = status_callback

    while controller.state.agent_state not in end_states:
        await asyncio.sleep(1)
