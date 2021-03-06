import re
from os import path

class Cmd():

	def __init__(self, cmd, file, dir, console, env = None, timeout = None, parser = None, keybind = False):
		self.cmd     = cmd
		self.file    = file
		self.dir     = dir
		self.console = console
		if type(env) == dict:
			self.env = env
		else:
			self.env = None
		self.timeout = timeout
		self.parser  = parser
		self.keybind = keybind

	@staticmethod
	def parse(file, listener):
		rootdir  = listener.root.dir
		cmd      = listener.get('CMD')
		console  = listener.get('CONSOLE') or listener.root.get('CONSOLE')
		env      = listener.get('ENV') or listener.root.get('ENV')
		timeout  = listener.get('TIMEOUT') or listener.root.get('TIMEOUT') or None
		dirname  = path.dirname(file)
		name     = path.basename(file)
		basename = path.splitext(name)[0]

		variables = listener.root.get('VAR')
		if variables:
			cmd = re.sub(r'\$(\w+)', lambda m: variables.get(m.group(1), m.group(0)), cmd)
		cmd = re.sub(r'\$FILEDIR\b', lambda m: dirname, cmd)
		cmd = re.sub(r'\$DIR\b', lambda m: dirname, cmd)
		cmd = re.sub(r'\$FILENAME\b', lambda m: name, cmd)
		cmd = re.sub(r'\$NAME\b', lambda m: name, cmd)
		cmd = re.sub(r'\$BASENAME\b', lambda m: basename, cmd)
		cmd = re.sub(r'\$FILE\b', lambda m: file, cmd)
		cmd = re.sub(r'\$ROOT\b', lambda m: rootdir, cmd)

		return Cmd( cmd, file, rootdir, console, env, timeout)
