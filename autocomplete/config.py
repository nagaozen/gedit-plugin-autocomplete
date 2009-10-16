"""
 config.py
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

import pygtk
pygtk.require('2.0')
import gtk
import os.path
from xml.parsers import expat

class ConfigModel():
	
	def __init__(self, filepath):
		# init default values
		self.scope = "global"
		self.base_words = ""
		self.filepath = filepath
		self.sv = ConfigService(self, filepath)
		
	def load(self):
		self.sv.load()
		
	def save(self):
		self.sv.save()
		
	def get_scope(self):
		return self.scope
	
	def set_scope(self,value):
		self.scope = value
		
	def get_base_words(self):
		return self.base_words
		
	def set_base_words(self,value):
		self.base_words = value

class ConfigService():
	def __init__(self, config, filepath):
		self.file = os.path.expanduser(str(filepath))
		self.config = config
		self.current_tag = None
	
	def load(self):
		
		dirname = os.path.dirname(self.file)
		if not os.path.isdir(dirname):
			os.makedirs(dirname)
		if not os.path.isfile(self.file):
			self.save(config,filepath)
		
		self.current_tag = None
		
		parser = expat.ParserCreate('UTF-8')
		parser.buffer_text = True
		parser.StartElementHandler = self.__start_element
		parser.EndElementHandler = self.__end_element
		parser.CharacterDataHandler = self.__character_data

		parser.ParseFile(open(self.file, 'rb'))
		
	def save(self):
		fp = file(self.file, "wb")
		fp.write('<?xml version="1.0" encoding="UTF-8"?>\n')
		scope_dump = '    <scope>%s</scope>\n' % self._escape(self.config.get_scope())
		base_words_dump = '    <words>%s</words>\n' % self._escape(self.config.get_base_words())
		settings = '<autocomplete>\n%s</autocomplete>\n' % (scope_dump+base_words_dump);
		fp.write(settings)
		fp.close()
		
	def _escape(self, xml):
		return xml.replace('&', '&amp;') \
					 .replace('<', '&lt;')  \
					 .replace('>', '&gt;')  \
					 .replace('"', '&quot;')
	
	def __start_element(self, tag, attrs):
		if tag == 'scope':
			self.current_tag = 'scope'
		elif tag == 'words':
			self.current_tag = 'words'
	def __end_element(self, tag):
		self.current_tag = None
	def __character_data(self, data):
		if self.current_tag == 'scope':
			self.config.set_scope(data)
		elif self.current_tag == 'words':
			self.config.set_base_words(data)
	
class ConfigurationDialog(gtk.Dialog):
	def __init__(self,config,callback):
		gtk.Dialog.__init__(self,"Autocomplete settings",None,gtk.DIALOG_DESTROY_WITH_PARENT)
		self.set_resizable(False)
		self.config = config
		self.callback = callback
		
		close_button = self.add_button(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)
		close_button.grab_default()
		help_button = self.add_button(gtk.STOCK_HELP, gtk.RESPONSE_HELP)
		
		help_button.connect_object("clicked", self.show_help_dialog,None)
		close_button.connect_object("clicked", gtk.Widget.destroy,self)
		
		scope_box = gtk.VBox(False, 0)
		scope_box.set_border_width(25)
		
		box_scope_label = gtk.HBox(False,10)
		scope_label = gtk.Label("<b>Scope</b>")
		scope_label.set_use_markup(True)
		scope_label.set_justify(gtk.JUSTIFY_LEFT)
		box_scope_label.pack_start(scope_label, False, False, 0)
		
		box_gsb = gtk.HBox(False,0)
		global_scope_button = gtk.RadioButton(None, "global")
		global_scope_label_indent = gtk.Label("    ")
		global_scope_label_indent.set_justify(gtk.JUSTIFY_LEFT)
		
		box_lsb = gtk.HBox(False,0)
		local_scope_button = gtk.RadioButton(global_scope_button, "local for each window")
		local_scope_label_indent = gtk.Label("    ")
		local_scope_label_indent.set_justify(gtk.JUSTIFY_LEFT)
		
		box_gsb.pack_start(global_scope_label_indent,False,False,0)
		box_gsb.pack_start(global_scope_button,False,False,0)
		
		box_lsb.pack_start(local_scope_label_indent,False,False,0)
		box_lsb.pack_start(local_scope_button,False,False,0)
		
		if self.config.get_scope() == "global":
			global_scope_button.set_active(True)
		else:
			local_scope_button.set_active(True)
		
		# NOTE : if connecting to local_scope_button too, even with clicked, 
		# 		 the callback function is called twice.
		#		 So we just connect that button
		global_scope_button.connect_object("toggled", self.configuration_change,None)
		
		self.global_scope_button = global_scope_button;
		self.local_scope_button = local_scope_button;
		
		
		scope_box.pack_start(box_scope_label)
		scope_box.pack_start(box_gsb)
		scope_box.pack_start(box_lsb)
		
		
		"""
			Word completion entries
		"""
		
		words_box = gtk.VBox(False, 0)
		words_box.set_border_width(25)
		
		box_words_label = gtk.HBox(False,10)
		words_label = gtk.Label("<b>Completion words</b>")
		words_label.set_use_markup(True)
		words_label.set_justify(gtk.JUSTIFY_LEFT)
		box_words_label.pack_start(words_label, False, False, 0)
		
		words_label_description = gtk.Label("    <i>Enter words you want to have in the completion list by default : </i>")
		words_label_description.set_use_markup(True)
		words_label_description.set_justify(gtk.JUSTIFY_LEFT)
		words_text_view = gtk.TextView()
		words_text_view.set_editable(True)
		words_text_view.set_wrap_mode(gtk.WRAP_WORD)
		words_text_view.set_border_width(0)
		words_text_view.set_size_request(-1, 150)
		words_text_view.set_left_margin(3)
		words_text_view.set_right_margin(3)
		
		words_buffer = gtk.TextBuffer()
		
		words_buffer.set_text(self.config.get_base_words())
		words_text_view.set_buffer(words_buffer)
		words_buffer.connect_object("changed", self.configuration_change,None)
		
		self.words_buffer = words_buffer
		
		words_box.pack_start(box_words_label, False, False, 10)
		words_box.pack_start(words_label_description, False, False, 0)
		sw = gtk.ScrolledWindow()
		sw.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
		sw.set_shadow_type(gtk.SHADOW_IN)
		sw.add(words_text_view)
		words_box.add(sw)
		
		self.vbox.pack_start(scope_box, True, True, 0)
		self.vbox.pack_start(words_box)
		self.show()
		self.vbox.show_all()
	
	def get_config(self):
		return self.config
	
	def configuration_change(self,widget,data=None):
		if self.global_scope_button.get_active():
			self.config.set_scope("global")
		else:
			self.config.set_scope("local")
		
		self.config.set_base_words(self.words_buffer.get_text(self.words_buffer.get_start_iter(),self.words_buffer.get_end_iter(),True))
		self.config.save()
		self.callback()
	
	def show_help_dialog(self,widget,data=None):
		help_dialog = gtk.Dialog("Autocomplete plugin help")
		close_button = help_dialog.add_button(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)
		close_button.grab_default()
		close_button.connect_object("clicked", gtk.Widget.destroy, help_dialog)
		
		inner_box = gtk.HBox(False, 0)
		inner_box.set_border_width(40)
		help_label = gtk.Label("Help is coming soon...")
		
		inner_box.pack_start(help_label, True, True, 0)
		help_dialog.vbox.pack_start(inner_box, True, True, 0)
		help_dialog.show_all()
