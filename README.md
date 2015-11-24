pipe_event
==========

This module provides a Event class which behaves just like threading.Event
but is based on two pipes created using os.pipe() functions.

Before Python 3.3, monotonic time is not introduced so adjusting system
clock may affect Event.wait() function if specific timeout is set.

Following notes can be found in PEP 0418:

    If a program uses the system time to schedule events or to implement
    a timeout, it may fail to run events at the right moment or stop the
    timeout too early or too late when the system time is changed manually
    or adjusted automatically by NTP.

This module demonstrates an alternative Event implementation on Unix-like
system which is not affected by the above issue.

License
-------

Copyright 2015 Jason Liao <liao0928@msn.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
