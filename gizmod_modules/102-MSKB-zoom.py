from GizmoDaemon import *
from GizmoScriptDefault import *
import subprocess

ENABLED = True
VERSION_NEEDED = 3.2
INTERESTED_CLASSES = [GizmoEventClass.Standard]

class MSKBZoom(GizmoScriptDefault):
	"""
	Enable Microsoft Natural Ergonomic 4000 zoom
	"""
	
	def onEvent(self, Event, Gizmo = None):
		"""
		Called from Base Class' onEvent method.
		See GizmodDispatcher.onEvent documention for an explanation of this function
		"""
		if len(Gizmod.Mice) == 0: return False
		if Event.Class == GizmoEventClass.Standard and Event.Type == GizmoEventType.EV_KEY:
			if Event.RawCode == 418:
				Gizmod.Mice[0].createEventRaw(GizmoEventType.EV_REL, GizmoMouseAxis.WHEEL, Event.Value)
				return True
			elif Event.RawCode == 419:
				Gizmod.Mice[0].createEventRaw(GizmoEventType.EV_REL, GizmoMouseAxis.WHEEL, -Event.Value)
				return True
			else:
				return False
	
	def __init__(self):
		""" 
		Default Constructor
		"""
		
		GizmoScriptDefault.__init__(self, ENABLED, VERSION_NEEDED, INTERESTED_CLASSES)

MSKBZoom()

