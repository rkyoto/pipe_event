
'''
pipe_event
==========

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
system which is not affected by the above issue.

'''

import os
import fcntl
import select
import threading

class Event:
    def __init__(self):
        r_fd, w_fd = os.pipe()  # create the pipes

        # set read() to non-blocking
        fl = fcntl.fcntl(r_fd, fcntl.F_GETFL)
        fcntl.fcntl(r_fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

        # create file objects
        self.r_pipe = os.fdopen(r_fd, 'rb', 0)
        self.w_pipe = os.fdopen(w_fd, 'wb', 0)

        self.lock = threading.Lock()  # create a lock to guard the pipes

    def __del__(self):
        self.r_pipe.close()
        self.w_pipe.close()

    def is_set(self):
        return self.wait(0)  # just poll the pipe

    def isSet(self):
        return self.is_set()

    def set(self):
        self.lock.acquire()
        if not self.is_set():
            self.w_pipe.write(b'\n')
        self.lock.release()

    def clear(self):
        self.lock.acquire()
        try:
            self.r_pipe.read()
        except:
            pass
        self.lock.release()

    def wait(self, timeout=None):
        ret = select.select([self.r_pipe], [], [], timeout)[0]
        return len(ret) > 0
