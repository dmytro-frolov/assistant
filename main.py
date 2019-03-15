#!/usr/bin/env python

import json
from subprocess import DEVNULL, STDOUT, check_call
from time import sleep

import google.oauth2.credentials
from google.assistant.library import Assistant

from effect import RunningCircle
from event_handler import EVENT_MAP, Action
from json_client import HyperionConnection


def clear_color():
    # effect.stop()
    check_call(['hyperion-remote', '--clearall'], stdout=DEVNULL, stderr=STDOUT)


def event_loop(assistant):
    for assistant_event in assistant.start():
        callback = EVENT_MAP.get(assistant_event.type, EVENT_MAP['clear'])
        callback()

        print('event:', assistant_event)
        print('event args: {}\n'.format(assistant_event.args))


if __name__ == '__main__':
    file = "/home/osmc/.config/google-oauthlib-tool/credentials.json"
    with open(file, 'r') as f:
        credentials = google.oauth2.credentials.Credentials(token=None,
                                                            **json.load(f))

    with HyperionConnection('localhost', 19444) as hyperion_socket:
        RunningCircle(hyperion_socket)

        # Action.answer()
        # sleep(2)
        # Action.clear()
        # pass
        with Assistant(credentials, 'osmc-c6683') as assistant:
            event_loop(assistant)
