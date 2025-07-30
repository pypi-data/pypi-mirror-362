from abc import abstractmethod
from collections.abc import Iterable

from openhands.events.event import Event, EventSource
from openhands.events.event_filter import EventFilter


class EventStoreABC:
    """A stored list of events backing a conversation."""

    sid: str
    user_id: str | None

    @abstractmethod
    def search_events(
        self,
        start_id: int = 0,
        end_id: int | None = None,
        reverse: bool = False,
        filter: EventFilter | None = None,
        limit: int | None = None,
    ) -> Iterable[Event]:
        """Retrieve events from the event stream, optionally excluding events using a filter.

        Args:
            start_id: The ID of the first event to retrieve. Defaults to 0.
            end_id: The ID of the last event to retrieve. Defaults to the last event in the stream.
            reverse: Whether to retrieve events in reverse order. Defaults to False.
            filter: An optional event filter

        Yields:
            Events from the stream that match the criteria.
        """

    @abstractmethod
    def get_event(self, id: int) -> Event:
        """Retrieve a single event from the event stream. Raise a FileNotFoundError if there was no such event."""

    @abstractmethod
    def get_latest_event(self) -> Event:
        """Get the latest event from the event stream."""

    @abstractmethod
    def get_latest_event_id(self) -> int:
        """Get the id of the latest event from the event stream."""
