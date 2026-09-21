from agent.models.events import EventType


class EventProcessor:
    """Classifies text into application event types."""

    def classify_text(self, text: str) -> EventType:
        """
        Classify a completed text buffer.
        
        """

        if not text:
            return EventType.UNKNOWN

        if len(text) == 1 and text.isalpha():
            return EventType.LETTER

        if len(text) > 1 and text.isalpha():
            return EventType.WORD

        if len(text) == 1:
            return EventType.CHARACTER

        return EventType.UNKNOWN