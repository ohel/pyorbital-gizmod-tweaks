from GizmoDaemon import *
from GizmoScriptDefault import *
import subprocess
import ReadSymLink

ENABLED = True
VERSION_NEEDED = 3.2
INTERESTED_CLASSES = [GizmoEventClass.Standard]
RAPOO_DEVICE = ReadSymLink.readlinkabs("/dev/input/evdev-rapoo-keyboard")

class RAPOOScrolling(GizmoScriptDefault):
	"""
	Disable RAPOO P7800 zoom and scroll instead
	"""
	
	def onEvent(self, Event, Gizmo = None):
		"""
		Called from Base Class' onEvent method.
		See GizmodDispatcher.onEvent documention for an explanation of this function
		"""
		if len(Gizmod.Mice) == 0: return False
		if Event.Class == GizmoEventClass.Standard and Event.Type == GizmoEventType.EV_KEY and Gizmo.FileName == RAPOO_DEVICE:
			if str(Event.Code) == "KEY_KPPLUS" and Event.Value > 0:
				Gizmod.Mice[0].createEventRaw(GizmoEventType.EV_REL, GizmoMouseAxis.WHEEL, pow(Event.Value, 4)) # power to scroll faster
				return True
			elif str(Event.Code) == "KEY_KPMINUS" and Event.Value > 0:
				Gizmod.Mice[0].createEventRaw(GizmoEventType.EV_REL, GizmoMouseAxis.WHEEL, -pow(Event.Value, 4))
				return True
			else:
				return False
	
	def __init__(self):
		""" 
		Default Constructor
		"""
		
		GizmoScriptDefault.__init__(self, ENABLED, VERSION_NEEDED, INTERESTED_CLASSES)

RAPOOScrolling()

