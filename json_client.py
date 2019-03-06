"""
This module is used to send the led data to hyperion's json server

Created on 27.11.2014

@author: Fabian Hertwig
"""

import socket


class HyperionConnection:
    def __init__(self, host, port, timeout=10):
        self.host = host
        self.port = port
        self.timeout = timeout

        self.s = None

    def __enter__(self):
        self.s = socket.socket()
        self.s.settimeout(self.timeout)
        try:
            self.s.connect((self.host, self.port))

        except Exception as e:
            print("Error on connection to ", self.host, ":", self.port, "\nMessage: ", e.args)

        else:
            return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self.s.send(bytearray('{"command":"clearall"}\n', encoding='utf8'))
            self.s.close()

        except Exception as e:
            print("Could not close socket connection\nMessage: ", e.args)

    def send_led_data(self, led_data):
        """
        Send the led data in a message format the hyperion json server understands
        :param led_data: bytearray of the led data (r,g,b) * hyperion.ledcount
        """
        # create a message to send
        message = '{"color":['
        # add all the color values to the message
        for i in range(len(led_data)):
            message += repr(led_data[i])
            # separate the color values with ",", but do not add a "," at the end
            if not i == len(led_data) - 1:
                message += ','
        # complete message
        message += '],"command":"color","priority":100}\n'

        try:
            self.s.send(bytearray(message, encoding='utf8'))

        except Exception as e:
            print("Error while sending the led data\nMessage: ", e.args)
            raise
