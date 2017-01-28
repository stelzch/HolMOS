"""
A curses-based interface for the server
(Sorry for spaghetti code)
"""
import urwid
import netifaces

palette = [
	('bg', '', '', '', '#ffa', '#228'),
	('window', '', '', '', '#fff', '#888'),
	('widget', '', '', '', '#000', '#fff'),
	('highlight', '', '', '', '#fff', '#000')

]


class SettingsView ():
	def __init__(self):
		self.header = urwid.Text("""  _____           ____
 / ___/__ ___ _  / __/__ _____  _____ ____
/ /__/ _ `/  ' \_\ \/ -_) __/ |/ / -_) __/
\___/\_,_/_/_/_/___/\__/_/  |___/\__/_/
""")
		self.editResX = urwid.AttrMap(urwid.IntEdit(default=1280), 'widget')
		self.editResY = urwid.AttrMap(urwid.IntEdit(default=720), 'widget')
		self.labelRes = urwid.Text('Resolution')
		self.editFramerate = urwid.AttrMap(urwid.IntEdit(default=24), 'widget')
		self.labelFramerate = urwid.Text('Framerate')
		self.editQuality = urwid.AttrMap(urwid.IntEdit(default=20), 'widget')
		self.labelQuality = urwid.Text('Video Quality')
		self.settingsContent = [
			self.header,
			urwid.Columns([self.labelRes, urwid.Columns([self.editResX,  urwid.Text('x', wrap='space', align='center'), self.editResY])]),
			urwid.Columns([self.labelFramerate, self.editFramerate]),
			urwid.Columns([self.labelQuality, self.editQuality]),
			urwid.Divider(),
			urwid.Text('Network Interfaces')
		]
		for interface in netifaces.interfaces():
			btn = urwid.Button(interface)
			urwid.connect_signal(btn, 'click', self.handle_interface_selected, interface)
			self.settingsContent.append(urwid.AttrMap(btn, None, focus_map='highlight'))
		self.rootWidget = urwid.LineBox(
					urwid.Filler(
						urwid.Pile(self.settingsContent)
						),'Settings')

	def handle_interface_selected(self, button, choice):
		swap_view('error', 'Hello World')

	def get_root(self):
		return self.rootWidget

class ErrorView():
	def __init__(self, errorMsg):
		self.error = urwid.Text(errorMsg)
		self.rootWidget = urwid.LineBox(urwid.Filler(self.error), 'Error!')
	def get_root(self):
		return self.rootWidget

	def set_msg(self, errorMsg):
		self.error = urwid.Text(errorMsg)

def handle_input(key):
	if key in ('q', 'Q'):
		raise urwid.ExitMainLoop()


settings = SettingsView()
error = ErrorView('test')
frame = urwid.Frame(settings.get_root())
def swap_view(dest, msg=None):
	print("called")
	if dest == 'settings':
		frame = urwid.Frame(settings.get_root())
		#frame.draw()
	elif dest == 'error':
		if msg:
			error.set_msg(msg)
		frame = urwid.Frame(error.get_root())
		#frame.draw()

window = urwid.AttrMap(frame, 'window')
placeholder = urwid.AttrMap(
				urwid.Overlay(window, urwid.SolidFill(),
					align='center', width=('relative', 87),
					valign='middle', height=('relative', 87),
					min_width=20, min_height = 9
				), 'bg')


loop = urwid.MainLoop(placeholder, palette, unhandled_input=handle_input)
loop.screen.set_terminal_properties(colors=256)
loop.run()