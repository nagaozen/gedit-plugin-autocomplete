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

import gedit

from plugin import AutoComplete
from config import ConfigurationDialog

class AutoCompletePlugin(gedit.Plugin):
    
    def __init__(self):
        gedit.Plugin.__init__(self)
        self._instances = {}
    
    def activate(self, window):
        self._instances[window] = AutoComplete(self, window)
    
    def deactivate(self, window):
        self._instances[window].deactivate()
        del self._instances[window]
    
    def update_ui(self, window):
        self._instances[window].update_ui()
    
    def is_configurable(self):
        return True
    
    def create_configure_dialog(self):
        dialog = ConfigurationDialog(self)
        return dialog
    
