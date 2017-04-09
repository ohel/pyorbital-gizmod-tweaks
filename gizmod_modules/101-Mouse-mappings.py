from GizmoDaemon import *
from GizmoScriptDefault import *
import ReadSymLink

ENABLED = True
VERSION_NEEDED = 3.2
INTERESTED_CLASSES = [GizmoEventClass.Standard]
MOUSE_DEVICE = ReadSymLink.readlinkabs("/dev/input/evdev-mouse")

class MouseMappings(GizmoScriptDefault):
    """
    Enable keyboard mappings for mouse thumb buttons and tilt wheel
    """

    def onEvent(self, Event, Gizmo = None):
        """
        Called from Base Class' onEvent method.
        See GizmodDispatcher.onEvent documention for an explanation of this function
        """
        if Event.Class != GizmoEventClass.Standard or Gizmo.FileName != MOUSE_DEVICE:
            return False

        if Event.Type == GizmoEventType.EV_KEY:
            if str(Event.Code) == "BTN_SIDE":
                if Event.Value == 1:
                    Gizmod.Keyboards[0].createEventRaw(GizmoEventType.EV_KEY, GizmoKey.KEY_ENTER, 1)
                elif Event.Value == 0:
                    Gizmod.Keyboards[0].createEventRaw(GizmoEventType.EV_KEY, GizmoKey.KEY_ENTER, 0)
            elif str(Event.Code) == "BTN_EXTRA":
                if Event.Value == 1:
                    Gizmod.Keyboards[0].createEventRaw(GizmoEventType.EV_KEY, GizmoKey.KEY_LEFTCTRL, 1)
                elif Event.Value == 0:
                    Gizmod.Keyboards[0].createEventRaw(GizmoEventType.EV_KEY, GizmoKey.KEY_LEFTCTRL, 0)
            elif str(Event.Code) == "BTN_MIDDLE":
                if Event.Value == 1:
                    Gizmod.Keyboards[0].createEventRaw(GizmoEventType.EV_KEY, GizmoKey.KEY_ESC, 1)
                elif Event.Value == 0:
                    Gizmod.Keyboards[0].createEventRaw(GizmoEventType.EV_KEY, GizmoKey.KEY_ESC, 0)
        elif Event.Type == GizmoEventType.EV_REL and Event.RawCode == 6:
            if Event.Value == 1:
                Gizmod.Keyboards[0].createEvent(GizmoEventType.EV_KEY, GizmoKey.KEY_LEFT)
            elif Event.Value == -1:
                Gizmod.Keyboards[0].createEvent(GizmoEventType.EV_KEY, GizmoKey.KEY_RIGHT)

        return True

    def __init__(self):
        """
        Default Constructor
        """

        GizmoScriptDefault.__init__(self, ENABLED, VERSION_NEEDED, INTERESTED_CLASSES)

MouseMappings()
