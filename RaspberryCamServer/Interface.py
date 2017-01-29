"""
A curses-based interface for the server
(Sorry for spaghetti code)
"""
import urwid
import sys
import netifaces
from RaspberryCamServer.Server import Server

palette = [
	('bg', '', '', '', '#ffa', '#228'),
	('window', '', '', '', '#fff', '#888'),
	('widget', '', '', '', '#000', '#258'),
	('highlight', '', '', '', '#000', '#258'),
	('log', '', '', '', '#fff', '#258'),
	('info', '', '', '', '#4f4', '#258'),
	('error', '', '', '', '#f44', '#258'),
	('warning', '', '', '', '#ff4', '#258')
]


class SettingsView ():
	def __init__(self):
		self.header = urwid.Text('''  _____           ____
 / ___/__ ___ _  / __/__ _____  _____ ____
/ /__/ _ `/  ' \_\ \/ -_) __/ |/ / -_) __/
\___/\_,_/_/_/_/___/\__/_/  |___/\__/_/

Press i to show more information
Press h to show help
''')
		self.editResX = urwid.AttrMap(urwid.IntEdit(default=1280), 'widget')
		self.editResY = urwid.AttrMap(urwid.IntEdit(default=720), 'widget')
		self.labelRes = urwid.Text('Resolution')
		self.editFramerate = urwid.AttrMap(urwid.IntEdit(default=24), 'widget')
		self.labelFramerate = urwid.Text('Framerate')
		self.editQuality = urwid.AttrMap(urwid.IntEdit(default=20), 'widget')
		self.labelQuality = urwid.Text('Video Quality')
		self.editBitrate = urwid.AttrMap(urwid.IntEdit(default=25000), 'widget')
		self.labelBitrate = urwid.Text('Bitrate')
		self.settingsContent = [
			self.header,
			urwid.Columns([self.labelRes, urwid.Columns([self.editResX,  urwid.Text('x', wrap='space', align='center'), self.editResY])]),
			urwid.Columns([self.labelFramerate, self.editFramerate]),
			urwid.Columns([self.labelQuality, self.editQuality]),
			urwid.Columns([self.labelBitrate, self.editBitrate]),
			urwid.Divider(),
			urwid.Text('Network Interfaces')
		]
		for interface in netifaces.interfaces():
			btn = urwid.Button(interface)
			urwid.connect_signal(btn, 'click', self.handle_interface_selected, interface)
			self.settingsContent.append(urwid.AttrMap(btn, None, focus_map='highlight'))
		self.rootWidget = urwid.LineBox(
					urwid.Filler(
						urwid.Pile(self.settingsContent), 'top'
						), 'Settings')

	def handle_interface_selected(self, button, choice):
		swap_view('error', 'Hello World')

	def get_root(self):
		return self.rootWidget

class InfoView():
	def __init__(self, msg, title=''):
		self.error = urwid.Text(msg)
		self.rootWidget = urwid.LineBox(urwid.Filler(self.error, 'top'), title)
	def get_root(self):
		return self.rootWidget

	def set_msg(self, msg):
		self.error = urwid.Text(msg)

class LogView():
	def __init__(self):
		self.curLog = list()
		self.status = urwid.Text('')
		self.logger = urwid.Text('', wrap='any')
		self.container = urwid.Filler(urwid.Pile([
			self.status,
			urwid.Divider(),
			urwid.AttrMap(self.logger, 'widget')
			]), 'top')
		self.rootWidget = urwid.LineBox(self.container,
			'Log')

		self.server = Server(self.log)
	def get_root(self):
		return self.rootWidget

	def log(self, ttype, msg):
		self.curLog.insert(0, ('widget', msg))
		self.curLog.insert(0, (ttype, '['+ttype.upper()+'] '))
		self.logger.set_text(self.curLog)

	def stop(self):
		self.server.stop()

def handle_input(key):
	if key in ('q', 'Q'):
		raise urwid.ExitMainLoop()
	if key in ('i', 'I'):
		swap_view('info')
	if key in ('s', 'S'):
		swap_view('settings')
	if key in ('h', 'H'):
		swap_view('help')
	if key in ('l', 'L'):
		swap_view('log')

loop = urwid.MainLoop(None, palette, unhandled_input=handle_input)

settings = SettingsView()
info = InfoView('''Written by Christoph Stelz for the HolMOS-Project.
Version 0.0.1 Alpha

Published under MIT License.

Press s to go back to the settings

''', 'Information')
helpV = InfoView('''Quality determines the output quality or the h264 codec.
10 means lossless, 40 means lossy. 20-25 is highly recommended.

Bitrate is the bitrate in Kbps at which video will be encoded. Maximum is 25000 (25 Mbps).

Press s to go back to settings.
''', 'Help')

error = InfoView('error')
log = LogView()
frame = urwid.Frame(settings.get_root())

def swap_view(dest, msg=None):
	if dest == 'settings':
		frame = urwid.Frame(settings.get_root())
		window = urwid.AttrMap(frame, 'window')
		placeholder = urwid.AttrMap(
				urwid.Overlay(window, urwid.SolidFill(),
					align='center', width=('relative', 87),
					valign='middle', height=('relative', 87),
					min_width=20, min_height = 9
				), 'bg')
		loop.widget = placeholder
	elif dest == 'error':
		if msg:
			error.set_msg(msg)
		frame = urwid.Frame(error.get_root())
		window = urwid.AttrMap(frame, 'window')
		placeholder = urwid.AttrMap(
				urwid.Overlay(window, urwid.SolidFill(),
					align='center', width=('relative', 87),
					valign='middle', height=('relative', 87),
					min_width=20, min_height = 9
				), 'bg')
		loop.widget = placeholder
	elif dest == 'info':
		frame = urwid.Frame(info.get_root())
		window = urwid.AttrMap(frame, 'window')
		placeholder = urwid.AttrMap(
				urwid.Overlay(window, urwid.SolidFill(),
					align='center', width=('relative', 87),
					valign='middle', height=('relative', 87),
					min_width=20, min_height = 9
				), 'bg')
		loop.widget = placeholder
	elif dest == 'help':
		frame = urwid.Frame(helpV.get_root())
		window = urwid.AttrMap(frame, 'window')
		placeholder = urwid.AttrMap(
				urwid.Overlay(window, urwid.SolidFill(),
					align='center', width=('relative', 87),
					valign='middle', height=('relative', 87),
					min_width=20, min_height = 9
				), 'bg')
		loop.widget = placeholder
	elif dest == 'log':
		frame = urwid.Frame(log.get_root())
		window = urwid.AttrMap(frame, 'window')
		placeholder = urwid.AttrMap(
				urwid.Overlay(window, urwid.SolidFill(),
					align='center', width=('relative', 87),
					valign='middle', height=('relative', 87),
					min_width=20, min_height = 9
				), 'bg')
		loop.widget = placeholder


swap_view('settings')



loop.screen.set_terminal_properties(colors=256)
loop.run()
print("hi")
log.stop() # Server gets terminated with log
sys.exit(0)