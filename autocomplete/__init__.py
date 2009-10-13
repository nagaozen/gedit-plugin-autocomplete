"""
 __init__.py
 This file is part of "Gedit Autocomplete"
 Copyright (C) 2009 - Vincent Petithory, Fabio Zendhi Nagao
 
 "Gedit Autocomplete" is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.
 
 "Gedit Autocomplete" is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public License
 along with "Gedit Autocomplete"; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, 
 Boston, MA  02110-1301  USA
"""

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
		engine = AutoCompleteEngine(str(self.windows_count), self.config, {}, [])
		engine.activate(window)
		self.eng_map[window] = engine
	
	def activate_with_global_scope(self,window):
		# Create autocomplete engine in global scope mode
		engine = AutoCompleteEngine(str(self.windows_count), self.config, self.words, self.dictionary_words)
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
		
	
