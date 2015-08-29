from GizmoDaemon import *
from GizmoScriptDefault import *
import os
import ReadSymLink


ENABLED = True
VERSION_NEEDED = 3.2
INTERESTED_CLASSES = [GizmoEventClass.Standard]
REMOTE_DEVICE = ReadSymLink.readlinkabs("/dev/input/remote")

class USBRemoteS(GizmoScriptDefault):
    """
    USB Remote control
    """
    
    def onEvent(self, Event, Gizmo = None):
        """
        Called from Base Class' onEvent method.
        See GizmodDispatcher.onEvent documention for an explanation of this function
        """
        if Event.Class == GizmoEventClass.Standard and Gizmo.FileName == REMOTE_DEVICE:
            if Event.Type == GizmoEventType.EV_KEY:
                if str(Event.Code) == "KEY_ESC":
                    if Event.Value == 0:
                        self.esc_counter = 0
                    else:
                        self.esc_counter = self.esc_counter + 1
                    if self.esc_counter > 30:
                        subprocess.Popen(["sudo", "shutdown" ,"-hP", "now"])
                elif str(Event.Code) == "KEY_NEXTSONG" and Event.Value == 1:
                    subprocess.Popen(["/usr/bin/terminal", "--hide-borders", "--geometry", "50x10", "-x", os.path.expanduser("~") + "/.scripts/toggle_digital_source.sh", "autoclose"])
                elif str(Event.Code) == "KEY_PREVIOUSSONG" and Event.Value == 1:
                    subprocess.Popen([os.path.expanduser("~") + "/.scripts/screensaver.sh", "standby"])
                elif str(Event.Code) == "BTN_LEFT" and Event.Value == 1:
                    # ok key
                    pass
                elif str(Event.Code) == "BTN_RIGHT" and Event.Value == 1:
                    # menu key
                    subprocess.Popen("/opt/programs/gizmod/customgizmo/menulauncher")
                self.previous_value = Event.Value
                return True
#           elif Event.Type == GizmoEventType.EV_REL:
        else:
            return False
    
    def __init__(self):
        """ 
        Default Constructor
        """
        self.previous_value = 0
        self.esc_counter = 0
        GizmoScriptDefault.__init__(self, ENABLED, VERSION_NEEDED, INTERESTED_CLASSES)

USBRemoteS()

