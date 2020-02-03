"""
This module is a modification of rainbow-swirl.py by https://hyperion-project.org/
"""
import math
import time
from abc import abstractmethod, ABC
from collections import namedtuple
from functools import wraps
from threading import Thread

from helpers import run_in_thread, EffectSingleTone


class Effect(ABC):
    _states = []

    def __init__(self, hyperion_socket, led_count=84, reverse=False):
        self.hyperion_socket = hyperion_socket
        self.led_count = led_count
        self.reverse = reverse
        self.running = False
        self.brightness = 1.0

        self.led_data = bytearray()

    def stop(self):
        self.running = False

    def clear_all(self):
        self.hyperion_socket.send_data('{"command":"clearall"}\n')

    @abstractmethod
    def fill(self):
        pass

    @abstractmethod
    def run(self):
        pass


def run_once(f):
    func_name = f.__name__

    @wraps(f)
    def inner(self):
        if not func_name in self._states:
            self._states.append(func_name)

            def closure():
                f(self)
                self._states.remove(func_name)

            # t = Thread(target=f, args=(self, ), name=func_name)
            t = Thread(target=closure, name=func_name)
            t.start()


    return inner


class RunningCircle(Effect, EffectSingleTone):
    created = False

    def __init__(self, hyperion_socket, led_count=84, reverse=False):
        if self.created:
            return

        super(RunningCircle, self).__init__(hyperion_socket, led_count, reverse)

        # todo: make threads great again
        self.running = False
        self.paused = False
        self.breathing = False

        Color = namedtuple('Color', ['r', 'g', 'b'])
        self.yellow = Color(245, 155, 1)
        self.green = Color(66, 244, 66)
        self.blue = Color(66, 155, 244)
        self.red = Color(244, 66, 66)
        self.fill()

        self.created = True

    def fill(self):
        colors = [self.yellow, self.green, self.blue, self.red]
        led_block = self.led_count // len(colors)

        # fill the led stip
        for i in range(self.led_count):
            current_color = colors[int(i // led_block)]
            self.led_data += bytearray(current_color)

    @run_once
    def breath(self):
        # breathing effect
        scale = 10
        limit = int(2 * math.pi * scale)
        while self.running:
            for i in range(limit):
                self.brightness = (math.cos(i/scale) + 2) / 3
                time.sleep(0.07)


    @run_once
    def run(self):
        # Calculate the sleep time and rotation increment
        increment = 9
        increment %= self.led_count

        rotation_time = 3
        sleep_time = rotation_time / self.led_count
        while sleep_time < 0.05:
            increment *= 1  # if 0 it'll just pause
            sleep_time *= 3

        # Switch direction if needed
        if self.reverse:
            increment = -increment

        self.running = True
        while self.running:
            # changing brightness
            buf_data = bytearray()
            for data in self.led_data:
                buf_data.append(int(data * self.brightness))

            self.hyperion_socket.send_led_data(buf_data)
            self.led_data = self.led_data[-increment:] + self.led_data[:-increment]
            time.sleep(sleep_time)
