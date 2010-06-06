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
import json
import os.path

class SettingsModel():
    
    def __init__(self, caller):
        self._caller = caller
        
        self.source  = "MIXED"
        self.path    = gedit.Plugin.get_data_dir(caller._plugin) + "/"
        
        self._persistenceService = PersistenceService(self)
    
    def load(self):
        self._persistenceService.load()
    
    def save(self):
        self._persistenceService.save()
    
    def set_source(self, value):
        self.source = value
    
    def get_source(self):
        return self.source
    
    def get_words(self, lang):
        path = os.path.expanduser("%slib/global.json" % (self.path))
        f = open(path, "rb")
        d = json.load(f)
        f.close()
        words_list = frozenset(d["statics"].split(' '))
        
        path = os.path.expanduser("%slib/%s.json" % (self.path, lang))
        if not os.path.isfile(path):
            return words_list
        f = open(path, "rb")
        d = json.load(f)
        f.close()
        words_list = words_list.union(d["statics"].split(' '))
        
        return words_list
    
    def get_language_library(self, lang):
        path = os.path.expanduser("%slib/%s.json" % (self.path, lang))
        if not os.path.isfile(path):
            return {}
        f = open(path, "rb")
        d = json.load(f)
        f.close()
        return d
    

class PersistenceService():
    
    def __init__(self, model):
        self._model = model
        
        self.json_path  = os.path.expanduser("%s%s" % (self._model.path, "settings.json"))
        self.settings = None
    
    def load(self):
        f = open(self.json_path, "rb")
        self.settings = json.load(f)
        f.close()
        
        self._model.source = self.settings["source"]
    
    def save(self):
        self.settings["source"] = self._model.source
        
        f = file(self.json_path, "wb")
        json.dump(self.settings, f)
        f.close()
    
