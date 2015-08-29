# pyorbital-gizmod-tweaks
USB LCD display controller + music player plugin + Gizmo Daemon tweaks all-in-one spaghetti.

## Gizmo Daemon tweaks

[Gizmod Daemon](http://gizmod.sourceforge.net/) is a utility to control stuff based on input events. It hasn't been maintained for a while and basically I've just hacked stuff to it for modern system software and my hardware. I use it to modify input from two USB keyboards (so that one acts as a remote) and to add more functionality to mice. For example many modern mice show up as a mouse and a keyboard to the computer. If one wanted to fully map the mouse buttons, one would be also overwriting keyboard shortcuts. With Gizmo Daemon one can make a distinction between a real keyboard and mouse buttons.

## PyOrbital LCD display controller

PyOrbital is a dirty script to control a Matrix Orbital LK202 USB LCD display. I mainly use it with [Quod Libet](https://quodlibet.readthedocs.org/en/latest/) music player, for which I made a plugin and a hack for smooth usage. I uploaded this in case someone needs a hint on how to control a USB LCD display, there's also an udev rule to initialize one.

Basically the whole thing operates as follows. A generic USB keyboard (Sunwave el-cheapo remote) talks to Linux input system, which Gizmod interrupts. A Gizmod module or Quod Libet talks to PyOrbital, which in turn talks to the LCD display. The result is a working remote control with visual feedback. There's a [video](https://www.youtube.com/watch?v=OUsN4T12dc8) of everything working together.

