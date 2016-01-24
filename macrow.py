#!/usr/bin/python
#

import sys
import os
import time
from Xlib import X, XK, display, protocol
from Xlib.ext import record
from gi.repository import Notify

local_dpy = display.Display()
recording_display = display.Display()
# keycode of macro keys - checked with xev
list_macro_keys = [191, 192, 193, 194, 195]
recorded_macro_keykode = [[], [], [], [], []]
macro_id = 0
counter = 0


state = 1
# state 1 = get macro identifer, define if play macro or record macro
# state 2 = play macro
# state 3 = record macro -- wait for an macro id.
# state 4 = record macro -- wait for keys + macro id.
# def macro_identifier():
# the first pressed combo is the macro identifier
# print 'macro identifiers'


def show_notification(str):
    Notify.init("MacroW")
    Hello = Notify.Notification.new("MacroW:", str, "dialog-information",)
    Hello.show()


def send_key(event_):
    window = local_dpy.get_input_focus()._data["focus"]
    if event_.type == X.KeyPress:
        event_to_send = protocol.event.KeyPress(
            time=int(time.time()),
            root=local_dpy.screen().root,
            window=window,
            same_screen=0, child=X.NONE,
            root_x=0, root_y=0, event_x=0, event_y=0,
            state=event_.state,
            detail=event_.detail
        )
        window.send_event(event_to_send, propagate=True)
    if event_.type == X.KeyRelease:
        event_to_send = protocol.event.KeyRelease(
            time=int(time.time()),
            root=local_dpy.screen().root,
            window=window,
            same_screen=0, child=X.NONE,
            root_x=0, root_y=0, event_x=0, event_y=0,
            state=event_.state,
            detail=event_.detail
        )
        window.send_event(event_to_send, propagate=True)
    local_dpy.flush()
    time.sleep(0.01)


def play_macro():
    global macro_id, state, recorded_macro_keykode
    # print 'playing macro', macro_id

    for event_ in recorded_macro_keykode[macro_id - 191]:
        send_key(event_)
    macro_id = 0
    state = 1


def callback(reply):
    global state, list_macro_keys, macro_id
    global recorded_macro_keykode

    if reply.client_swapped or (reply.category != record.FromServer):
        return
    if not len(reply.data) or ord(reply.data[0]) < 2:  # not an event
        return

    while len(reply.data):
        event, reply.data = protocol.rq.EventField(None).parse_binary_value(
            reply.data, recording_display.display, None, None)
        keysym = local_dpy.keycode_to_keysym(event.detail, 0)
        if event.type == X.KeyPress and keysym == XK.XK_Escape:  # ESC KEY

            if state > 2:
                # print 'Canceling Macro Recording'
                show_notification('Canceling Macro Recording')
                if macro_id > 0:
                    recorded_macro_keykode[macro_id - 191] = []
                    macro_id = 0
                    state = 1
                return
        # State 1
        if event.type == X.KeyRelease and state == 1:
            if event.detail in list_macro_keys:  # if one of the macro key is called run
                state = 2
                macro_id = event.detail
            if event.detail == 75:  # if f9 is pressed record macroe
                state = 3
                # print 'Macro recording , waiting for macro identifier'
                show_notification(
                    'Macro recording , waiting for macro identifier')
                return
        # State 2
        if state == 2:
            play_macro()
            return
        # State 3
        if event.type == X.KeyRelease and state == 3:
            local_dpy.flush()
            if event.detail in list_macro_keys:  # if one of the macro key is called run
                macro_id = event.detail
                state = 4
                recorded_macro_keykode[macro_id - 191] = []
                # print 'GOT MACRO, waiting for keystrokes.'
                show_notification('Waiting for keystrokes')
                return
        # State 4
        if state == 4:
            if event.detail in list_macro_keys:  # if one of the macro key is called run
                if event.type == X.KeyRelease:
                    # print 'Macro Recorded'
                    show_notification('Macro recorded')
                    time.sleep(0.1)
                    macro_id = 0
                    state = 1
                    return
            elif event.type in [X.KeyPress, X.KeyRelease]:
                recorded_macro_keykode[macro_id - 191].append(event)


def main():
    # Check if the extension is present
    if not recording_display.has_extension("RECORD"):
        print "RECORD extension not found"
        sys.exit(1)

    show_notification("MacroW is running")
    # Create a recording context; we only want key and mouse events (not
    # preocessed)
    context = recording_display.record_create_context(
        0,
        [record.AllClients],
        [{'core_requests': (0, 0),
          'core_replies': (0, 0),
          'ext_requests': (0, 0, 0, 0),
          'ext_replies': (0, 0, 0, 0),
          'delivered_events': (0, 0),
          'device_events': (X.KeyPress, X.MotionNotify),
          'errors': (0, 0),
          'client_started': False,
          'client_died': False,
          }])

    recording_display.record_enable_context(context, callback)
    recording_display.record_free_context(context)


if __name__ == "__main__":
    main()
