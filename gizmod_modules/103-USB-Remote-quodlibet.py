from GizmoDaemon import *
from GizmoScriptDefault import *
import subprocess
import os
import time
import socket
import ReadSymLink

ENABLED = True
VERSION_NEEDED = 3.2
INTERESTED_CLASSES = [GizmoEventClass.Standard]
QL_CONTROL_FILE = os.path.expanduser("~") + "/.quodlibet/control"
QL_BIN = "/opt/programs/quodlibet/quodlibet.py"
REMOTE_DEVICE = ReadSymLink.readlinkabs("/dev/input/remote")
SOCKET_PATH = "/dev/shm/pyorbital"

class USBRemoteQL(GizmoScriptDefault):
    """
    USB Remote control
    """
    
    def onEvent(self, Event, Gizmo = None):
        """
        Called from Base Class' onEvent method.
        See GizmodDispatcher.onEvent documention for an explanation of this function
        """
        if Event.Class == GizmoEventClass.Standard and Event.Type == GizmoEventType.EV_KEY and Gizmo.FileName == REMOTE_DEVICE and os.path.exists(QL_CONTROL_FILE):

            controlfile = open(QL_CONTROL_FILE, 'w')
            self.returnvalue = False
            if not self.connected:
                self.connected = not self.sendsocket.connect_ex(SOCKET_PATH)

            if str(Event.Code) == "KEY_HOMEPAGE" and Event.Value == 1:
                subprocess.Popen([os.path.expanduser("~") + "/.scripts/screensaver.sh", "standby"])
                #controlfile.write("toggle-window\n")
                #if self.connected:
                #    self.sendsocket.send("visible\n")
                self.returnvalue = True
            elif str(Event.Code) == "KEY_LEFTMETA" and Event.Value == 1:
                controlfile.write("random album\n")
                if self.connected:
                    self.sendsocket.send("ralbum\n")
                self.returnvalue = True
            elif str(Event.Code) == "KEY_TAB":
                if Event.Value == 0 and self.previous_value != 2:
                    controlfile.write("next\n")
                else:
                    controlfile.write("seek +0:" + str(Event.Value) + "\n")
                self.returnvalue = True
            elif str(Event.Code) == "KEY_BACKSPACE":
                if Event.Value == 0 and self.previous_value != 2:
                    controlfile.write("seek 0:0\n")
                    controlfile.write("previous\n")
                else:
                    controlfile.write("seek -0:" + str(Event.Value) + "\n")
                self.returnvalue = True
            elif str(Event.Code) == "KEY_STOPCD" and Event.Value == 1:
                controlfile.write("pause\n")
                controlfile.write("seek 0:0\n")
                if self.connected:
                    self.sendsocket.send("stop\n")
                self.returnvalue = True
            elif str(Event.Code) == "KEY_PLAYPAUSE" and Event.Value == 1:
                controlfile.write("play-pause\n")
                self.returnvalue = True
            elif str(Event.Code) == "KEY_RIGHT" and Event.Value == 1:
                Gizmod.Keyboards[0].createEvent(GizmoEventType.EV_KEY, GizmoKey.KEY_TAB)
                self.returnvalue = True
            elif str(Event.Code) == "KEY_LEFT" and Event.Value == 1:
                Gizmod.Keyboards[0].createEvent(GizmoEventType.EV_KEY, GizmoKey.KEY_TAB, [GizmoKey.KEY_LEFTSHIFT])
                self.returnvalue = True
            elif str(Event.Code) == "KEY_UP" and Event.Value != 0:
                Gizmod.Keyboards[0].createEvent(GizmoEventType.EV_KEY, GizmoKey.KEY_UP)
                self.returnvalue = True
            elif str(Event.Code) == "KEY_DOWN" and Event.Value != 0:
                Gizmod.Keyboards[0].createEvent(GizmoEventType.EV_KEY, GizmoKey.KEY_DOWN)
                self.returnvalue = True
            elif str(Event.Code) == "KEY_ENTER" and Event.Value == 1:
                Gizmod.Keyboards[0].createEvent(GizmoEventType.EV_KEY, GizmoKey.KEY_ENTER)
                self.returnvalue = True
            elif str(Event.Code) == "KEY_MAIL" and Event.Value == 1:
                controlfile.write("focus\n")
                controlfile.close()
                time.sleep(0.2)
                controlfile = open(QL_CONTROL_FILE, 'w')
                Gizmod.Keyboards[0].createEvent(GizmoEventType.EV_KEY, GizmoKey.KEY_J, [GizmoKey.KEY_LEFTCTRL])
                if self.connected:
                    self.sendsocket.send("jumpto\n")
                self.returnvalue = True
            elif str(Event.Code) == "KEY_PAGEUP" and Event.Value == 1:
                controlfile.write("order toggle\n")
#                if self.connected:
#                    self.sendsocket.send("order\n")
                self.returnvalue = True
            elif str(Event.Code) == "KEY_PAGEDOWN" and Event.Value == 1:
                controlfile.write("unfilter\n")
                if self.connected:
                    self.sendsocket.send("clearf\n")
                self.returnvalue = True
            elif str(Event.Code) == "KEY_MUTE" and Event.Value == 1:
                controlfile.write("volume 5\n")
#                if self.connected:
#                    self.sendsocket.send("volume 0.05\n")
                self.returnvalue = True
            elif str(Event.Code) == "KEY_VOLUMEUP":
                controlfile.write("volume +" + str(Event.Value) + "\n")
#                if self.connected:
#                    self.sendsocket.send("volume +" + str(Event.Value) + "\n")
#                    ql_status = str.split(os.popen(QL_BIN + " --status").read())
#                    if ql_status:
#                        self.sendsocket.send("volume " + ql_status[2] + "\n")
                self.returnvalue = True
            elif str(Event.Code) == "KEY_VOLUMEDOWN":
                controlfile.write("volume -" + str(Event.Value) + "\n")
#                if self.connected:
#                    self.sendsocket.send("volume -" + str(Event.Value) + "\n")
#                    ql_status = str.split(os.popen(QL_BIN + " --status").read())
#                    if ql_status:
#                        self.sendsocket.send("volume " + ql_status[2] + "\n")
                self.returnvalue = True
            controlfile.close()
            self.previous_value = Event.Value
            return self.returnvalue
        elif Event.Class == GizmoEventClass.Standard and Event.Type == GizmoEventType.EV_KEY and Gizmo.FileName == REMOTE_DEVICE and str(Event.Code) == "KEY_HOMEPAGE" and not(os.popen("ps -e | grep mplayer").read()) and Event.Value == 1:
            if not os.popen("ps -e | grep pyorbital.py").read():
                subprocess.Popen(["/opt/programs/misc/pyorbital.py", "2>&1", "&"])
            subprocess.Popen([QL_BIN, "2>&1", "&"])
            return True
        else:
            return False
    
    def __init__(self):
        """ 
        Default Constructor
        """
        self.returnvalue = False
        self.previous_value = 0
        self.sendsocket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self.connected = not self.sendsocket.connect_ex(SOCKET_PATH)
        GizmoScriptDefault.__init__(self, ENABLED, VERSION_NEEDED, INTERESTED_CLASSES)

USBRemoteQL()

