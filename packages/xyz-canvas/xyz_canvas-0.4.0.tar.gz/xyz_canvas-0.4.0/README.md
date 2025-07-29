# xyz_canvas
## Interactive canvas for editing 3D geometry, using only matplotlib.pyplot

This is a demo of xyz_canvas (pre-release, V0.4.0), a Python library intended to support adding, editing, and connecting 3D wire-frame objects using only Matplotlib. 

The idea is that this will be called by code that needs the  user to define / edit these objects in 3D space.

The capability being demonstrated is **being able to create and edit in 3D space using only Matplotlib**. This is somewhat distinct from the demo program itself, which works as described below. The features of the demo that support this capability are:
1. Using ax.format_coord(event.xdata, event.ydata) to create a '3D Mouse' class 'mouse_3D'
2. Using the 3D mouse to position lines with end points pinned to the 'backplanes' of the 3D view
3. Using a 3D frame visualisation, and temporarily fixing *one* coordinate's value, to provide a UI to move end points into general 3D space (away from backplanes)
4. Using the backplane-pinned 3D coordinates of the 3D mouse at the time of line end selection to decide which coordinate to fix during the 3D move

### Demo progam
The demo program demo.py is minimal, as is the object creation capability of the canvas.py 'engine', but these limitations don't detract from the core idea stated above.

Currently, objects consist only of lines, which may be disconnected. An object consists of one or more lines. Pressing 'save' fires the callback with the set of added lines as an argument. To add a line, click two points within the axis space. The view may be rotated at any time by clicking and dragging just oustide the axis space.

# Known issues
As of now, there are no known issues with the capability being demonstrated; it is possible to use only the mouse (and only the main button) to create and move line ends in 3D. However, see below.

# Next Steps
I intend to make the demonstration capabilty more useful, e.g. I will add a 'delete most recent' button alongside the 'clear' (all) button, so that this could be used as-is within other software. Also note that I need to work out if it's possible to disentangle the core capability from the supporting demonstration code, as the latter isn't fully contained in demo.py and infact exists within canvas.py.

One way to do this might be to combine steps 2 and 3 above, and rewriting the library so that its sole function is to get a true 3D point from the user.


## Installation
Install with pip:
```
pip install xyz_canvas
```

## Demo Screenshot

![Capture](https://github.com/user-attachments/assets/03082efb-99ed-424e-9171-418b5173cc13)

