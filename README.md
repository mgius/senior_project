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

# Controls
Currently all controls are beta only, although I figured I'd document them
anyway.

## Overworld Screen
* Arrow keys move your character.
* 'n' activates the NPC trapped in the box
* 'd' kills your player
* 'u' revives your player
* 'a' activates the worlds worst attack animation

## Battle Screen
Currently no interaction possible.

# To Do List

* Battle decision backend (simple version by Jan 25)
  * Example of both in-game implemented and python implemented
     * This has changed to be JSON on disk or through the in-game editor
     * Maybe write a basic Text UI for it?  (low priority)
  * In-game battle plan editor. (Global Game Jam?)
* Battles
  * Basic battle screen (By Jan 18)
  * Better battle animations (GGJ?)
  * Spells
    * with less shitty animations
* More sprites to choose from
* Need a wrapper around text supporting following features
  * Line wrapping
  * Fetching text + surface from the same object
  * Mostly line wrapping
* Better maps (By Jan 18)
* Better configuration
  * Python config file?
  * may not be worth it
* Rect support functions
  * Clamping/Stretching
  * Center-determining
* BattleCharacter/BattleNPC are largely duplicated code.  Fix that
* Characters need to be able to be dumped to disk, in human readable format
  * Needs to encompass the strategy dumping as well

# Bugs
* Moving and "attacking" at the same kind causes...interesting results
