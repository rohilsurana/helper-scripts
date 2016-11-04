import glib
import dbus
from dbus.mainloop.glib import DBusGMainLoop
from pushbullet import Pushbullet

access_token = "YOUR ACCESS TOKEN HERE"
pb = Pushbullet(access_token)

argList = {
    "APP_NAME": 0,
    "ID": 1,
    "ICON_NAME": 2,
    "SUMMARY": 3,
    "BODY": 4,
    "ACTIONS": 5,
    "HINTS": 6,
    "TIMEOUT": 7
}


def notifications(bus, message):
    args = message.get_args_list()
    if len(args) > argList["BODY"]:
        # Check if a notification has any content. Only then push it.
        # This is to filter volume change notifications
        if len(args[argList["SUMMARY"]]) > 0 and len(args[argList["BODY"]]) > 0:
            pb.push_note(str(args[argList["SUMMARY"]]), str(args[argList["BODY"]]))


DBusGMainLoop(set_as_default=True)

bus = dbus.SessionBus()
bus.add_match_string_non_blocking("eavesdrop=true, interface='org.freedesktop.Notifications', member='Notify'")
bus.add_message_filter(notifications)

mainloop = glib.MainLoop()
mainloop.run()
