from datetime import datetime
from functools import wraps

from google.assistant.library.event import EventType

from effect import RunningCircle


class Action:
    @staticmethod
    def listen():
        RunningCircle(None).run()

    @staticmethod
    def answer():
        RunningCircle(None).run()
        RunningCircle(None).breath()

    @staticmethod
    def clear():
        RunningCircle(None).stop()
        RunningCircle(None).clear_all()

    @staticmethod
    def crash():
        raise Exception('crash')

EVENT_MAP = {
    EventType.ON_CONVERSATION_TURN_STARTED: Action.listen,
    EventType.ON_END_OF_UTTERANCE: Action.answer,
    EventType.ON_RECOGNIZING_SPEECH_FINISHED: lambda: None,  # doing stuff
    EventType.ON_RESPONDING_STARTED: lambda: None,
    EventType.ON_RENDER_RESPONSE: lambda: None,  # actual response do nothing
    EventType.ON_ASSISTANT_ERROR: Action.crash,

    'clear': Action.clear
}
