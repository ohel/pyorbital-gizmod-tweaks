from GizmoDaemon import *
from GizmoScriptDefault import *
import os
import ReadSymLink


ENABLED = True
VERSION_NEEDED = 3.2
INTERESTED_CLASSES = [GizmoEventClass.Standard]
MP_CONTROL_FILE = os.path.expanduser("~") + "/ramdisk/mpvfifo"
REMOTE_DEVICE = ReadSymLink.readlinkabs("/dev/input/remote")

class USBRemoteMP(GizmoScriptDefault):
	"""
	USB Remote control
	"""
	
	def onEvent(self, Event, Gizmo = None):
		"""
		Called from Base Class' onEvent method.
		See GizmodDispatcher.onEvent documention for an explanation of this function
		"""
		self.returnvalue = False
		if Event.Class == GizmoEventClass.Standard and Event.Type == GizmoEventType.EV_KEY and Gizmo.FileName == REMOTE_DEVICE and os.popen("ps -e | grep mpv | head -n 1").read():
			controlfile = open(MP_CONTROL_FILE, 'w')
		   	if str(Event.Code) == "KEY_PLAYPAUSE" and Event.Value == 1:
				controlfile.write("pause\n")
				self.returnvalue = True
		   	elif str(Event.Code) == "KEY_STOPCD" and Event.Value == 1:
				controlfile.write("frame_step\n")
				self.returnvalue = True
			elif str(Event.Code) == "KEY_TAB":
				if Event.Value == 0 and self.previous_value != 2:
					controlfile.write("seek_chapter +1\n")
				else:
					controlfile.write("seek +2\n")
				self.returnvalue = True
		   	elif str(Event.Code) == "KEY_BACKSPACE":
				if Event.Value == 0 and self.previous_value != 2:
					controlfile.write("seek_chapter -1\n")
				else:
					controlfile.write("seek -2\n")
				self.returnvalue = True
			elif str(Event.Code) == "KEY_PAGEUP" and Event.Value == 1:
				controlfile.write("audio_delay 0.1\n")
				self.returnvalue = True
			elif str(Event.Code) == "KEY_PAGEDOWN" and Event.Value != 0:
				controlfile.write("audio_delay -0.1\n")
				self.returnvalue = True
			elif str(Event.Code) == "KEY_MAIL" and Event.Value == 1:
				controlfile.write("sub_select\n")
				self.returnvalue = True
			elif str(Event.Code) == "KEY_LEFTMETA" and Event.Value == 1:
				controlfile.write("osd_show_progression\n")
				self.returnvalue = True
			elif str(Event.Code) == "KEY_HOMEPAGE" and Event.Value == 1:
				controlfile.write("vo_fullscreen\n")
				self.returnvalue = True
			elif str(Event.Code) == "KEY_MUTE" and Event.Value == 1:
				controlfile.write("switch_audio\n")
				self.returnvalue = True
			elif str(Event.Code) == "KEY_VOLUMEUP" and Event.Value != 0:
				controlfile.write("volume +2\n")
				self.returnvalue = True
			elif str(Event.Code) == "KEY_VOLUMEDOWN" and Event.Value != 0:
				controlfile.write("volume -2\n")
				self.returnvalue = True
			elif str(Event.Code) == "KEY_UP" and Event.Value == 1:
				Gizmod.Keyboards[0].createEvent(GizmoEventType.EV_KEY, GizmoKey.KEY_KP8)
				self.returnvalue = True
			elif str(Event.Code) == "KEY_DOWN" and Event.Value == 1:
				Gizmod.Keyboards[0].createEvent(GizmoEventType.EV_KEY, GizmoKey.KEY_KP2)
				self.returnvalue = True
			elif str(Event.Code) == "KEY_LEFT" and Event.Value == 1:
				Gizmod.Keyboards[0].createEvent(GizmoEventType.EV_KEY, GizmoKey.KEY_KP4)
				self.returnvalue = True
			elif str(Event.Code) == "KEY_RIGHT" and Event.Value == 1:
				Gizmod.Keyboards[0].createEvent(GizmoEventType.EV_KEY, GizmoKey.KEY_KP6)
				self.returnvalue = True
			elif str(Event.Code) == "KEY_ENTER" and Event.Value == 1:
				Gizmod.Keyboards[0].createEvent(GizmoEventType.EV_KEY, GizmoKey.KEY_ENTER)
				self.returnvalue = True
			controlfile.close()
			self.previous_value = Event.Value
	   		return self.returnvalue
	   	else:
			return False
	
	def __init__(self):
		""" 
		Default Constructor
		"""
		self.returnvalue = False
		self.previous_value = 0
		GizmoScriptDefault.__init__(self, ENABLED, VERSION_NEEDED, INTERESTED_CLASSES)

USBRemoteMP()

