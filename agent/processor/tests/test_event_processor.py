from agent.models.events import EventType
from agent.processor.event_processor import EventProcessor


def test_single_letter():
    processor = EventProcessor()

    assert processor.classify_text("a") == EventType.LETTER


def test_word():
    processor = EventProcessor()

    assert processor.classify_text("ola") == EventType.WORD


def test_another_word():
    processor = EventProcessor()

    assert processor.classify_text("python") == EventType.WORD


def test_number():
    processor = EventProcessor()

    assert processor.classify_text("7") == EventType.CHARACTER


def test_symbol():
    processor = EventProcessor()

    assert processor.classify_text("@") == EventType.CHARACTER


def test_empty_text():
    processor = EventProcessor()

    assert processor.classify_text("") == EventType.UNKNOWN