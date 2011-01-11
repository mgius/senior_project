# Dependencies

## Python
I developed using Python 2.6.  Other versions may or may not work.

## PyGame
This project depends on PyGame 1.9.1.  As of 2010-12-27, Debian does
not contain a new enough version of PyGame (although Ubuntu does).
You will need to install a new version of PyGame to run this program.

If you have easy_install installed, installing the latest pygame is as
simple as running

    easy_install -U pygame --user

You may need to add yourself to appropriate groups in order to run
this command as a mortal user and add pygame system-wide.

## SDL
PyGame has a dependency on SDL, although some libraries are optional.
At the moment, I'm taking advantage of SDL-image for GIF import 
purposes. I am not aware of any SDL version requirements.  As long as 
PyGame installs, this game should work.

# To Do List

* Battle decision backend
  * Example of both in-game implemented and python implemented
  * In-game battle plan editor.
* Battles
  * Better battle animations
  * Spells
    * with less shitty animations
* More sprites to choose from
* In-game text overlay (status, menu, etc)
* Better maps
* Better configuration
  * Python config file?
* "map file format"
  * XML? JSON? Something else?
