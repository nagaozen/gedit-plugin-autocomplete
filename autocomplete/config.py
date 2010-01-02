# gEdit AutoComplete
# Copyright (C) 2009 Fabio Zendhi Nagao, Vincent Petithory
# Copyright (C) 2006 Alin Avasilcutei, Osmo Salomaa
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pygtk
pygtk.require('2.0')
import gtk

from settings import SettingsModel

class ConfigurationDialog(gtk.Dialog):
    
    def __init__(self, caller):
        self._model = SettingsModel(self)
        self._model.load()
        
        self.current_source = ""
        
        gtk.Dialog.__init__(self, "AutoComplete settings", None, gtk.DIALOG_DESTROY_WITH_PARENT)
        self.set_resizable(False)
        
        # Definitions
        source_label = gtk.Label("<b>Completion source:</b>")
        source_label.set_use_markup(True)
        source_label.set_justify(gtk.JUSTIFY_LEFT)
        
        self.mixed_radio = gtk.RadioButton(None, "Mixed")
        self.all_documents_radio = gtk.RadioButton(self.mixed_radio, "All documents")
        self.library_radio = gtk.RadioButton(self.mixed_radio, "Library")
        
        if self._model.get_source() == "ALL_DOCUMENTS":
            self.all_documents_radio.set_active(True)
        if self._model.get_source() == "LIBRARY":
            self.library_radio.set_active(True)
        
        self.mixed_radio.connect("toggled", self.source_change, "MIXED")
        self.all_documents_radio.connect("toggled", self.source_change, "ALL_DOCUMENTS")
        self.library_radio.connect("toggled", self.source_change, "LIBRARY")
        
        # Positioning
        option_a_box = gtk.HBox()
        option_b_box = gtk.HBox()
        option_c_box = gtk.HBox()
        
        option_a_box.pack_start(self.mixed_radio, False, False, 0)
        option_b_box.pack_start(self.all_documents_radio, False, False, 0)
        option_c_box.pack_start(self.library_radio, False, False, 0)
        
        self.vbox.pack_start(source_label, True, True, 10)
        self.vbox.pack_start(option_a_box, True, True, 0)
        self.vbox.pack_start(option_b_box, True, True, 0)
        self.vbox.pack_start(option_c_box, True, True, 0)
        
        # Buttons
        close_button = self.add_button(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)
        close_button.grab_default()
        close_button.connect_object("clicked", gtk.Widget.destroy, self)
        
        help_button = self.add_button(gtk.STOCK_HELP, gtk.RESPONSE_HELP)
        help_button.connect_object("clicked", self.show_help_dialog, None)
        
        # Display
        self.vbox.show_all()
        self.show()
    
    def source_change(self, widget, data=None):
        if widget.get_active():
            self._model.set_source(data)
        self._model.save()
    
    def show_help_dialog(self, gobject):
        dialog = gtk.Dialog("AutoComplete help")
        
        close_button = dialog.add_button(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)
        close_button.grab_default()
        close_button.connect_object("clicked", gtk.Widget.destroy, dialog)
        
        hbox = gtk.HBox(False, 0)
        hbox.set_border_width(40)
        
        label = gtk.Label("Help still isn't available yet...")
        
        hbox.pack_start(label, True, True, 0)
        
        dialog.vbox.pack_start(hbox, True, True, 0)
        dialog.show_all()
    
