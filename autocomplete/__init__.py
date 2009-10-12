import gedit

from completion import AutoCompleteEngine
from config import ConfigModel
from config import ConfigurationDialog

class AutoCompletePlugin(gedit.Plugin):
	
	def __init__(self):
		gedit.Plugin.__init__(self)
		# load the plugin settings
		self.windows_count = 0
		self.eng_map = {}
		self.words = {}
		self.dictionary_words = []
		self.filepath = '~/.gnome2/gedit/autocomplete_settings.xml'
		
		self.base_text = "bonjour magalie"
		self.config = ConfigModel(self.filepath)
		self.config.load()
		
	def activate(self, window):
		self.windows_count += 1
		if self.config.get_scope() == "global":
			self.activate_with_global_scope(window)
		else:
			self.activate_with_local_scope(window)
	
	def activate_with_local_scope(self,window):
		# Create autocomplete engine in local scope mode
		engine = AutoCompleteEngine(str(self.windows_count), {}, [], self.base_text)
		engine.activate(window)
		self.eng_map[window] = engine
	
	def activate_with_global_scope(self,window):
		# Create autocomplete engine in global scope mode
		engine = AutoCompleteEngine(str(self.windows_count), self.words, self.dictionary_words, self.base_text)
		engine.activate(window)
		self.eng_map[window] = engine
	
	def deactivate(self, window):
		self.windows_count -= 1
		engine = self.eng_map[window]
		engine.deactivate(window)
		self.eng_map[window] = None
	
	def is_configurable(self):
		return True

	def create_configure_dialog(self):
		dialog = ConfigurationDialog(self.config,self.config_changed_callback)
		return dialog
	
	def config_changed_callback(self):
		ws = []
		for w in self.eng_map:
			self.deactivate(w)
			ws.append(w)

		self.eng_map = None
		self.words = None
		self.dictionary_words = None

		self.windows_count = 0
		self.eng_map = {}
		self.words = {}
		self.dictionary_words = []
		for window2 in ws:
			self.activate(window2)
		
	
