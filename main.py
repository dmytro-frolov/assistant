#!/usr/bin/env python

import sys
import logging
import json
from subprocess import DEVNULL, STDOUT, check_call

import google.oauth2.credentials
from google.assistant.library import Assistant

from effect import RunningCircle
from event_handler import EVENT_MAP, Action
from json_client import HyperionConnection


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger(__name__)

"""
TODO: rewrite event loops using a new google service
google library is depricated.
measure cpu load on this and on the new one.
"""

def event_loop(assistant):

    for assistant_event in assistant.start():
        print('event:', assistant_event)
        print('event args: {}\n'.format(assistant_event.args))
        
        callback = EVENT_MAP.get(assistant_event.type, EVENT_MAP['clear'])
        callback()


if __name__ == '__main__':
    file = "/home/osmc/.config/google-oauthlib-tool/credentials.json"
    with open(file, 'r') as f:
        credentials = google.oauth2.credentials.Credentials(token=None,
                                                            **json.load(f))

    with HyperionConnection('localhost', 19444) as hyperion_socket:
        RunningCircle(hyperion_socket)

        with Assistant(credentials, 'osmc-c6683') as assistant:
            print(assistant)
            event_loop(assistant)
