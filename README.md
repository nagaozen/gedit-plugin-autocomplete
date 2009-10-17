GEdit Autocomplete
==================

This plugin provides a popup with the possible completions available in the 
opened documents. This version is the very same of Alin Avasilcutei 0.9.6 and 
the only difference is that instead of using Tab to complete, it's now using 
Enter. This change is useful to make the plugin play nice with the snippets 
plugin - a super useful built-in plugin that no one could live without.

Installation
------------
1. Run the `install` script
2. Open gedit and click `Edit -> Preferences -> Plugins`
3. Check the `Autocomplete-0.9.7` and hit `Close`
4. That's it! Now you can start coding and watch the popup working. Hit `Return`
   to accept the completion.

License
-------

Copyright (C) 2009 [Fabio Zendhi Nagao](http://zend.lojcomm.com.br/), [Vincent Petithory](http://blog.lunar-dev.net/)

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; either version 2 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA

Credits
-------

There are a lot of completions plugins in the Gnome GEdit Plugins page, and I 
don't know what one was the first but this one is a product by:

- Initial version: Osmo Salomaa <http://users.tkk.fi/~otsaloma/gedit/>
- 0.9.6: Alin Avasilcutei <http://gedit-autocomp.sourceforge.net/>
- 0.9.6-Return: Fabio Nagao <http://zend.lojcomm.com.br/>
- 0.9.7: Vincent Petithory <http://blog.lunar-dev.net/> (from 0.9.6-Return)


Changes
-------
> @2009-10-17  
> Merged the configurable branch.Renamed the version to 0.9.8
> 
>   * The completion behavior can be one of the following :
>      * global : each window shares their words, so any word in any window is eligible for completion anywhere
>      * local : each window only knows its own words, so only those are eligible for completion in the window.
>   * A global list of predefined words is available in any window.
>   * A configuration dialog is available to tweak the above settings.

> @2009-10-03  
> Added an plugin icon.Renamed the version to 0.9.7

> @2009-10-04  
> bugfix: Completion was active only on the last opened window. Previous 
> opened windows lost the completion feature.

> @2009-05-15  
> I did a brief read in the plugin, changed tabs into four spaces, fixed some
> typos and made the required changes to make Return run as the trigger
> instead of Tab.
