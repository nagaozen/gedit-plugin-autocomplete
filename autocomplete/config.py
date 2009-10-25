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

import gedit
import pygtk
pygtk.require('2.0')
import gtk
import gtksourceview2
import os.path
from xml.parsers import expat

class ConfigModel():
	
	def __init__(self, filepath):
		# init default values
		self.scope = "global"
		self.lang_words = {}
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
		
	def get_words(self):
		# TODO make a copy
		return self.lang_words
		
	def set_words(self,value):
		self.lang_words = value
		
	def get_lang_words(self,lang):
		try:
			words = self.lang_words[lang]
			return words
		except:
			return ''
		
	
	def set_lang_words(self,lang,value):
		self.lang_words[lang] = value

class ConfigService():
	def __init__(self, config, filepath):
		self.file = os.path.expanduser(str(filepath))
		self.config = config
		self.current_tag = None
		self.current_lang = None
		self.langs = None
	
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
		lang_words_list_dump = ''
		lang_words_map = self.config.get_words()
		for lang in lang_words_map:
			lang_words_list_dump += '        <lang name="%s">%s</lang>\n' % (self._escape(lang) , self._escape(lang_words_map[lang]))
		words_dump = '    <langs>\n%s    </langs>\n' % lang_words_list_dump
		settings = '<autocomplete>\n%s</autocomplete>\n' % (scope_dump+words_dump);
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
		elif tag == 'langs':
			self.current_tag = 'langs'
			self.langs = {}
		elif tag == 'lang':
			self.current_tag = 'lang'
			self.current_lang = attrs['name']
		
	
	def __end_element(self, tag):
		self.current_tag = None
		if tag == 'langs':
			self.config.set_words(self.langs)
		
	
	def __character_data(self, data):
		if self.current_tag == 'scope':
			self.config.set_scope(data)
		elif self.current_tag == 'langs':
			pass
		elif self.current_tag == 'lang':
			self.langs[self.current_lang] = data
		
	
	
class ConfigurationDialog(gtk.Dialog):
	def __init__(self,config,callback):
		gtk.Dialog.__init__(self,"Autocomplete settings",None,gtk.DIALOG_DESTROY_WITH_PARENT)
		self.set_resizable(False)
		self.config = config
		self.callback = callback
		
		validate_button = self.add_button(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)
		validate_button.grab_default()
		#cancel_button = self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
		help_button = self.add_button(gtk.STOCK_HELP, gtk.RESPONSE_HELP)
		
		validate_button.connect_object("clicked", self.on_validate,None)
		#cancel_button.connect_object("clicked", gtk.Widget.destroy, self)
		help_button.connect_object("clicked", self.show_help_dialog,None)
		
		scope_box = gtk.VBox(False, 0)
		scope_box.set_border_width(15)
		
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
		#-- disabled. save is done on closing
		#global_scope_button.connect_object("toggled", self.configuration_change,None)
		
		self.global_scope_button = global_scope_button;
		self.local_scope_button = local_scope_button;
		
		
		scope_box.pack_start(box_scope_label)
		scope_box.pack_start(box_gsb)
		scope_box.pack_start(box_lsb)
		
		
		"""
			Word completion entries
		"""
		
		words_box = gtk.VBox(False, 0)
		words_box.set_border_width(15)
		
		box_words_label = gtk.HBox(False,10)
		words_label = gtk.Label("<b>Completion words</b>")
		words_label.set_use_markup(True)
		words_label.set_justify(gtk.JUSTIFY_LEFT)
		box_words_label.pack_start(words_label, False, False, 0)
		
		words_label_description = gtk.Label("    <i>Enter words you want to have in the completion list by default : </i>")
		words_label_description.set_use_markup(True)
		words_label_description.set_justify(gtk.JUSTIFY_LEFT)
		
		words_box.pack_start(box_words_label, False, False, 0)
		words_box.pack_start(words_label_description, False, False, 10)
		
		""" Languages discovery """
		
		manager = gtksourceview2.LanguageManager()
		#manager.set_search_path(dirs + self.manager.get_search_path())
		langs = gedit.language_manager_list_languages_sorted(manager, True)
		# Stores lang name / words
		langs_model = gtk.ListStore(str,object)
		for lang in langs:
			document = gedit.Document()
			# NOTE : room for optimization here. Set language when requesting to show the View instead of now
			document.set_language(lang)
			document.set_text(self.config.get_lang_words(lang.get_name()))
			lang_text_view = gedit.View(document)
			langs_model.append([lang.get_name(), lang_text_view])
		
		global_document = gedit.Document()
		global_document.set_text(self.config.get_lang_words('Global'))
		global_lang_text_view = gedit.View(global_document)
		langs_model.prepend(['Global', global_lang_text_view])
		box_langs = gtk.HBox(False,0)
		box_langs.set_size_request(150,200)
		lang_list = gtk.TreeView(langs_model)
		cell = gtk.CellRendererText()
		lang_column = gtk.TreeViewColumn('Language', cell)
		lang_column.set_attributes(cell, text=0)
		lang_list.append_column(lang_column)
		
		langs_selection = lang_list.get_selection()
		langs_selection.connect('changed', self.lang_list_selection_change)
		# Select the first element, 'Global'.
		iter = langs_model.get_iter_first()
		langs_selection.select_iter(iter)
		
		sw_lang_views = gtk.ScrolledWindow()
		sw_lang_views.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
		sw_lang_views.set_shadow_type(gtk.SHADOW_IN)
		
		# Add list
		sw_langs = gtk.ScrolledWindow()
		sw_langs.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
		sw_langs.set_shadow_type(gtk.SHADOW_IN)
		sw_langs.add(lang_list)
		
		# pack everything
		box_langs.pack_start(sw_langs, True, True, 0)
		box_langs.pack_start(sw_lang_views, True, True, 0)
		words_box.pack_start(box_langs, True, True, 0)	
		
		self.vbox.pack_start(scope_box, True, True, 0)
		self.vbox.pack_start(words_box)
		self.show()
		self.vbox.show_all()
		
		self.langs_model = langs_model
		self.sw_lang_views = sw_lang_views
		self.sw_lang_views.add(global_lang_text_view)
	
	def lang_list_selection_change(self, treeselection):
		# retrieve gedit.view in treeview model
		selected_item = treeselection.get_selected()
		view = selected_item[0].get_value(selected_item[1],1)
		self.sw_lang_views.remove(self.sw_lang_views.get_child())
		self.sw_lang_views.add(view)
	
	def get_config(self):
		return self.config
	
	def on_validate(self,widget,data=None):
		self.commit()
		gtk.Widget.destroy(self)
	
	def commit(self):
		if self.global_scope_button.get_active():
			self.config.set_scope("global")
		else:
			self.config.set_scope("local")
		
		lang_words = {}
		for lang_item in self.langs_model:
			document = lang_item[1].get_buffer()
			""" may need to pass False instead of True (actually, include hidden chars) """
			lang_words[lang_item[0]] = document.get_text(document.get_start_iter(),document.get_end_iter(), True) 
			
		self.config.set_words(lang_words)
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
