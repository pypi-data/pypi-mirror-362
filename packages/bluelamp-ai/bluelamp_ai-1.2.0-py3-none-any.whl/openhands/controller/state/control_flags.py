from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar(
    'T', int, float
)  # Type for the value (int for iterations, float for budget)


@dataclass
class ControlFlag(Generic[T]):
    """Base class for control flags that manage limits and state transitions."""

    limit_increase_amount: T  # Kept for compatibility, not used for limits
    current_value: T  # Used for monitoring and analytics
    max_value: T  # Kept for compatibility, not used for limits
    headless_mode: bool = False  # Kept for compatibility

    # Note: reached_limit() and increase_limit() methods removed as limits are now disabled

    def step(self):
        """Determine the next state based on the current state and mode.

        Returns:
            ControlFlagState: The next state.
        """
        raise NotImplementedError


@dataclass
class IterationControlFlag(ControlFlag[int]):
    """Control flag for managing iteration limits."""

    # Note: reached_limit() and increase_limit() methods removed as limits are disabled

    def step(self):
        """Increment iteration count for monitoring purposes.
        
        No limits are enforced - the agent can run indefinitely.
        Loop detection is handled by StuckDetector which provides more
        sophisticated pattern-based detection instead of simple count limits.
        """
        self.current_value += 1


@dataclass
class BudgetControlFlag(ControlFlag[float]):
    """Control flag for managing budget limits."""

    # Note: reached_limit() and increase_limit() methods removed as limits are disabled

    def step(self):
        """Update budget state for monitoring purposes.

        No limits are enforced - the agent can run with unlimited budget.
        Budget tracking is maintained for monitoring and analytics only.
        """
        # Budget is updated externally, no action needed here
        pass
