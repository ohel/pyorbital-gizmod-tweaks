from quodlibet.plugins.events import EventPlugin
import socket

SOCKET_PATH = "/dev/shm/pyorbital"

class LCDStatus(EventPlugin):
    PLUGIN_ID = 'LCD Status'
    PLUGIN_NAME = _('LCD Status Message')
    PLUGIN_DESC = _("Output player status to Matrix Orbital LCD using pyorbital.py.")
    PLUGIN_VERSION = '0.2'

    def enabled(self):

        self.sendsocket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self.sendsocket.connect_ex(SOCKET_PATH)
        self.sendsocket.send("paused\n")

    def disabled(self):
        self.sendsocket.send("quit\n")
        self.sendsocket.close()

    def plugin_on_seek(self, song, msec):
        self.sendsocket.send("seek " + str(msec / 1000 / float(song.get("~#length", 0))) + "\n")

    def plugin_on_song_started(self, song):
        if type(song) == type(None): return
        self.sendsocket.send("artist " + song("artist") + "\n")
        self.sendsocket.send("title " + song("title") + "\n")
        self.sendsocket.send("album " + song("album") + "\n")
        self.sendsocket.send("disc " + str(song.get("discnumber", "")) + "\n")
        self.sendsocket.send("track " + str(song.get("tracknumber", "")) + "\n")

    def plugin_on_song_ended(self, song, stopped):
        self.sendsocket.send("stop\n")
        
    def plugin_on_paused(self):
        self.sendsocket.send("paused\n")

    def plugin_on_unpaused(self):
        self.sendsocket.send("unpaused\n")

