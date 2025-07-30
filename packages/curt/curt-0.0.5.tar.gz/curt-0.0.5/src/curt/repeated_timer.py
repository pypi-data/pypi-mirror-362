#
#  Created by IntelliJ IDEA.
#  User: jahazielaa
#  Date: 07/12/2022
#  Time: 01:16 p.m.
"""Repeated timer

This file allows the user to create threads.

This file requires the following imports: 'time', 'threading'.

This file contains the following classes:
    * RepeatedTimer - class for thread creation
"""

import threading
import time


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.next_call = time.time()
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self.next_call += self.interval
            self._timer = threading.Timer(self.next_call - time.time(), self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False
