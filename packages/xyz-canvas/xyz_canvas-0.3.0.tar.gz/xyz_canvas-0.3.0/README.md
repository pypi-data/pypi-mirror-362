# xyz_canvas
Interactive canvas for editing 3D geometry, using only matplotlib.pyplot

This is a demo of xyz_canvas (pre-release, V0.3.0), a Python library intended to add, edit, and connect 3D wire-frame objects using only Matplotlib. 

The idea is that this will be called by code that needs the  user to define / edit these objects in 3D space.

Currently, objects consist only of lines, which may be disconnected. An object consists of one or more lines.

Pressing 'save' fires the callback with the set of added lines as an argument.

To add a line, click two points within the axis space. The view may be rotated at any time by clicking and dragging just oustide the axis space.

# Known issues
Currently, when you *add* a line, both ends are pinned to the 'closest' backplane (shaded & gridded areas). You may add a line from one backplane to another.

I'm experimenting with ways to overcome this without making the UI clunky. The current version here achieves this by allowing line ends to be picked up (click on them) and dragged away from their plane. However, once 'dropped', if they are dropped away from all three backplanes, they can't be selected again.

More trivially, I need to add a 'delete most recent' button alongside the 'clear' (all) button.


## Installation
Install with pip:
```
pip install xyz_canvas
```

## Demo Screenshot

![Capture](https://github.com/user-attachments/assets/aea93646-d451-4597-84dc-5f81d00c52bf)
