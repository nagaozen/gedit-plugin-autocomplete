gEdit Autocomplete
==================

gEdit Autocomplete suggests word completions based on the text in the active
document. It first attempts to suggest compound words for a given word start,
and only if such words do not exist it resorts to suggesting simple words.

Compond words consist of simple words joined via concatenators. The inbuild
concatenators are targeting c-family, pascal-family, urls and emails:

* `.`
* `:`
* `->`
* `::`
* `://`
* `@`

This version uses `Return` instead of `Tab`, so it plays nice with the snippets 
plugin.

Installation
------------
1. Run the `install` script
2. Open gedit and click `Edit -> Preferences -> Plugins`
3. Check the `Autocomplete-0.9.x` and hit `Close`
4. That's it! Now you can start coding and watch the popup working. Hit `Return`
   to accept the completion.

License
-------

Copyright (C) 2009 [Fabio Zendhi Nagao](http://zend.lojcomm.com.br/),
[Vincent Petithory](http://blog.lunar-dev.net/)

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

There are a lot of completions plugins in the Gnome gEdit Plugins page, and I 
don't know what one was the first but this one is a product by:

- Initial version: Osmo Salomaa <http://users.tkk.fi/~otsaloma/gedit/>
- 0.9.6: Alin Avasilcutei <http://gedit-autocomp.sourceforge.net/>
- 0.9.x: Fabio Nagao <http://zend.lojcomm.com.br/> and Vincent Petithory <http://blog.lunar-dev.net/>


Changes
-------
> @2009-10-17  
> Merged the configurable branch. Renamed the version to 0.9.8
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
