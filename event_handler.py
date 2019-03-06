from google.assistant.library.event import EventType

from effect import RunningCircle
from subprocess import DEVNULL, STDOUT, check_call


class Action:
    __states = []

    @staticmethod
    def listen():
        # todo: remove from here and make actions with decorator that prevents running threads simultaniously
        RunningCircle(None).stop()
        RunningCircle(None).run()

    @staticmethod
    def answer():
        RunningCircle(None).stop()
        RunningCircle(None).breath()
        RunningCircle(None).run()


    @staticmethod
    def clear():
        RunningCircle(None).stop()
        check_call(['hyperion-remote', '--clearall'], stdout=DEVNULL, stderr=STDOUT)


EVENT_MAP = {
    EventType.ON_CONVERSATION_TURN_STARTED: Action.listen,
    EventType.ON_END_OF_UTTERANCE: Action.answer,
    EventType.ON_RECOGNIZING_SPEECH_FINISHED: lambda: None,  # doing stuff
    EventType.ON_RESPONDING_STARTED: lambda: None,
    EventType.ON_RENDER_RESPONSE: lambda: None,  # actual response do nothing

    'clear': Action.clear
}