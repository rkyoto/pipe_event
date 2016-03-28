'''
pipe_event2
===========

This module provides a Event class which behaves just like threading.Event
but is based on two pipes created using os.pipe() functions.

Before Python 3.3, monotonic time is not introduced so adjusting system
clock may affect Event.wait() function if specific timeout is set.

Following notes can be found in PEP 0418:

    "If a program uses the system time to schedule events or to implement
    a timeout, it may fail to run events at the right moment or stop the
    timeout too early or too late when the system time is changed manually
    or adjusted automatically by NTP."

This module demonstrates an alternative Event implementation on Unix-like
systems which is not affected by the above issue.

'''

import sys
import os
import fcntl
import select
import threading

def _clear_pipe(fd):
    try:
        while True:
            if not os.read(fd, 1024):
                break
    except OSError:
        pass

class Event:
    def __init__(self):
        _r, _w = os.pipe()  # create the pipe

        # set pipe to non-blocking
        fl = fcntl.fcntl(_r, fcntl.F_GETFL)
        fcntl.fcntl(_r, fcntl.F_SETFL, fl | os.O_NONBLOCK)

        self._r_fd = _r
        self._w_fd = _w
        self._lock = threading.Lock()

    def __del__(self):
        os.close(self._r_fd)
        os.close(self._w_fd)

    def is_set(self):
        return self.wait(0)  # just poll the pipe

    def isSet(self):
        return self.is_set()

    def set(self):
        with self._lock:
            if not self.is_set():
                os.write(self._w_fd, b'\n')

    def clear(self):
        with self._lock:
            _clear_pipe(self._r_fd)

    def wait(self, timeout=None):
        try:
            ret = select.select([self._r_fd], [], [], timeout)[0]
            if ret:
                return True
        except select.error as e:
            sys.stderr.write(str(e) + '\n')
        return False
