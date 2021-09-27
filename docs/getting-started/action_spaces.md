# Action Spaces

## Overview

MiniHack has a large, structured and context-sensitive action space. We give practitioners an easy way to restrict the action space in order to promote targeted skill discovery.
For example, [navigation tasks](../envs/navigation/index) mostly require movement commands, and occasionally, kicking doors, searching or eating. [Skill acquisition tasks](../envs/skill/index), on the other hand, require interactions with objects, e.g. managing the inventory, casting spells, zapping wands, reading scrolls, eating comestibles, quaffing potions, etc. In these tasks 75 actions are used.

The actual game of NetHack uses ASCII inputs, i.e., individual keyboard presses including modifiers like
Ctrl and Meta. NLE pre-defines 98 actions, 16 of which are compass directions and 82 of which
are command actions. T

## Specifying the Action Space

The actions used in MiniHack are defined [here](https://github.com/facebookresearch/nle/blob/master/nle/nethack/actions.py). The following example shows how to set the action space of the environment to movements towards 8 compass directions with `open`, `kick`, and `search` actions.
```python
from nle import nethack
MOVE_ACTIONS = tuple(nethack.CompassDirection)
NAVIGATE_ACTIONS = MOVE_ACTIONS + (
    nethack.Command.OPEN,
    nethack.Command.KICK,
    nethack.Command.SEARCH,
)
env = gym.make(
    "MiniHack-Corridor-R3-v0",
    actions=NAVIGATE_ACTIONS,
)
```

Note that using different observation keys can make environments significantly easier or harder.

## Possible Actions

| Name       |Value|Key| Description                                     |
|------------|---|---|---------------------------------------------------|
|EXTCMD|35 |#  |perform an extended command                        |
|EXTLIST|191|M-?|list all extended commands                         |
|ADJUST|225|M-a|adjust inventory letters                           |
|ANNOTATE|193|M-A|name current level                                 |
|APPLY|97 |a  |apply (use) a tool (pick-axe, key, lamp...)        |
|ATTRIBUTES|24 |C-x|show your attributes                               |
|AUTOPICKUP|64 |@  |toggle the pickup option on/off                    |
|CALL|67 |C  |call (name) something                              |
|CAST|90 |Z  |zap (cast) a spell                                 |
|CHAT|227|M-c|talk to someone                                    |
|CLOSE|99 |c  |close a door                                       |
|CONDUCT|195|M-C|list voluntary challenges you have maintained      |
|DIP|228|M-d|dip an object into something                       |
|DOWN|62 |>  |go down (e.g., a staircase)                        |
|DROP|100|d  |drop an item                                       |
|DROPTYPE|68 |D  |drop specific item types                           |
|EAT|101|e  |eat something                                      |
|ESC|27 |C-[|escape from the current query/action               |
|ENGRAVE|69 |E  |engrave writing on the floor                       |
|ENHANCE|229|M-e|advance or check weapon and spell skills           |
|FIRE|102|f  |fire ammunition from quiver                        |
|FIGHT|70 |F  |Prefix: force fight even if you don't see a monster|
|FORCE|230|M-f|force a lock                                       |
|GLANCE|59 |;  |show what type of thing a map symbol corresponds to|
|HELP|63 |?  |give a help message                                |
|HISTORY|86 |V  |show long version and game history                 |
|INVENTORY|105|i  |show your inventory                                |
|INVENTTYPE|73 |I  |inventory specific item types                      |
|INVOKE|233|M-i|invoke an object's special powers                  |
|JUMP|234|M-j|jump to another location                           |
|KICK|4  |C-d|kick something                                     |
|KNOWN|92 |\  |show what object types have been discovered        |
|KNOWNCLASS|96 |`  |show discovered types for one class of objects     |
|LOOK|58 |:  |look at what is here                               |
|LOOT|236|M-l|loot a box on the floor                            |
|MONSTER|237|M-m|use monster's special ability                      |
|MORE|13 |C-m|read the next message                              |
|MOVE|109|m  |Prefix: move without picking up objects/fighting   |
|MOVEFAR|77 |M  |Prefix: run without picking up objects/fighting    |
|OFFER|239|M-o|offer a sacrifice to the gods                      |
|OPEN|111|o  |open a door                                        |
|OPTIONS|79 |O  |show option settings, possibly change them         |
|OVERVIEW|15 |C-o|show a summary of the explored dungeon             |
|PAY|112|p  |pay your shopping bill                             |
|PICKUP|44 |,  |pick up things at the current location             |
|PRAY|240|M-p|pray to the gods for help                          |
|PREVMSG|16 |C-p|view recent game messages                          |
|PUTON|80 |P  |put on an accessory (ring, amulet, etc)            |
|QUAFF|113|q  |quaff (drink) something                            |
|QUIT|241|M-q|exit without saving current game                   |
|QUIVER|81 |Q  |select ammunition for quiver                       |
|READ|114|r  |read a scroll or spellbook                         |
|REDRAW|18 |C-r|redraw screen                                      |
|REMOVE|82 |R  |remove an accessory (ring, amulet, etc)            |
|RIDE|210|M-R|mount or dismount a saddled steed                  |
|RUB|242|M-r|rub a lamp or a stone                              |
|RUSH|103|g  |Prefix: rush until something interesting is seen   |
|SAVE|83 |S  |save the game and exit                             |
|SEARCH|115|s  |search for traps and secret doors                  |
|SEEALL|42 |*  |show all equipment in use                          |
|SEETRAP|94 |^  |show the type of adjacent trap                     |
|SIT|243|M-s|sit down                                           |
|SWAP|120|x  |swap wielded and secondary weapons                 |
|TAKEOFF|84 |T  |take off one piece of armor                        |
|TAKEOFFALL|65 |A  |remove all armor                                   |
|TELEPORT|20 |C-t|teleport around the level                          |
|THROW|116|t  |throw something                                    |
|TIP|212|M-T|empty a container                                  |
|TRAVEL|95 |_  |travel to a specific location on the map           |
|TURN|244|M-t|turn undead away                                   |
|TWOWEAPON|88 |X  |toggle two-weapon combat                           |
|UNTRAP|245|M-u|untrap something                                   |
|UP|60 |<  |go up (e.g., a staircase)                          |
|VERSION|246|M-v|list compile time options                          |
|VERSIONSHORT|118|v  |show version                                       |
|WAIT / SELF|46 |.  |rest one move while doing nothing / apply to self  |
|WEAR|87 |W  |wear a piece of armor                              |
|WHATDOES|38 |&  |tell what a command does                           |
|WHATIS|47 |/  |show what type of thing a symbol corresponds to    |
|WIELD|119|w  |wield (put in use) a weapon                        |
|WIPE|247|M-w|wipe off your face                                 |
|ZAP|112|z  |zap a wand                                         |

The descriptions are mostly taken from the cmd.c file in the NetHack source code.
For a detailed description of these actions, as well as other NetHack commands, we refer the reader to the [NetHack guide book](http://www.nethack.org/download/3.6.5/nethack-365-Guidebook.pdf).