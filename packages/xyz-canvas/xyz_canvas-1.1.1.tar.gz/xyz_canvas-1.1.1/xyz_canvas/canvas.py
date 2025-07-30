"""
MIT License

Copyright (c) 2025 Alan Robinson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d as mpl
from matplotlib.backend_bases import MouseButton
from matplotlib.backend_tools import Cursors


def _interleave(ends):
    a = ends[0]
    b = ends[1]
    return [a[0],b[0]], [a[1],b[1]], [a[2],b[2]]

class xyz_canvas:

    def __init__(self, *args, xlim =[0,10], ylim =[-20,30], zlim=[-3,5],
                               xlabel="x", ylabel="y", zlabel="z",
                               on_click_cb = None, on_move_cb = None, **kwargs
                 ):
        self.plt = plt
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.xlim=xlim
        self.ylim=ylim
        self.zlim=zlim
        self.xlabel=xlabel
        self.ylabel=ylabel
        self.zlabel=zlabel
        self.on_click_cb = on_click_cb
        self.on_move_cb = on_move_cb
        self.points_xyz = []
        self.selectable_point_index = None
        self.selected_point_index = None
        self.mouse_end_pane_idx_on_select = None
        self.init_canvas()
        self.pointer = mouse_3D(plt, self.ax, self.on_pointer_click, self.on_pointer_move)

    def init_axes(self):
        self.ax.set_xlim(self.xlim)
        self.ax.set_ylim(self.ylim)
        self.ax.set_zlim(self.zlim)
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)
        self.ax.set_zlabel(self.zlabel)

    def init_canvas(self):
        self.points_xyz = []
        self.ax.cla()
        self.init_axes()
        self.selected_point_index = None
        self.ax.figure.canvas.draw_idle()

    def redraw(self, showframe_xyz=None):
        self.ax.cla()
        self.init_axes()
        for p in self.points_xyz:
            x,y,z = p
            self.ax.scatter(x,y,z, color='blue', marker='o', s=50)
        self.ax.figure.canvas.draw_idle()
        if(showframe_xyz):
            xyz = showframe_xyz
            xy_plane_z = self.zlim[0]
            xz_plane_y = self.ylim[1]
            yz_plane_x = self.xlim[0]
            self.ax.plot(*_interleave([xyz,  [xyz[0], xyz[1], xy_plane_z] ]),color='grey', linestyle='--')
            self.ax.plot(*_interleave([xyz,  [xyz[0], xz_plane_y, xyz[2]] ]),color='grey', linestyle='--')
            self.ax.plot(*_interleave([xyz,  [yz_plane_x, xyz[1], xyz[2]] ]),color='grey', linestyle='--')
            x,y,z = xyz[0],xyz[1],xyz[2]
            self.ax.text(x,y,z,f"  ({x:.3f}, {y:.3f}, {z:.3f})", size = 'small')


    def on_pointer_click(self, xyz, ep_idx):
        # If we click whilst moving a point, drop it.
        # Note that its xyz will have been updated during the move to this point
        # This is a 'click away' event so we don't call on_click_cb
        if(self.selected_point_index is not None):        
            self.selected_point_index = None   
            self.redraw(showframe_xyz = None)
        else:
        # we were just roaming and clicked
            # so if we are over a point and clicked on it, select it
            if(self.selectable_point_index is not None):  
                self.selected_point_index = self.selectable_point_index
                if(self.on_click_cb):
                    self.on_click_cb(self, xyz, self.selected_point_index)
            else:
            # if there's nothing to select,  append the point and immediately select it
                self.points_xyz.append(xyz)         
                self.selected_point_index = len(self.points_xyz) - 1
                if(self.on_click_cb):
                    self.on_click_cb(self, xyz, self.selected_point_index)
                self.redraw(showframe_xyz = xyz)
            # whether new or existing, record the ep_idx of the selected point,
            # at the start of its move, for on_pointer_move to use
            self.mouse_end_pane_idx_on_select = ep_idx

    def on_pointer_move(self, xyz, xy, ep_idx):
        # If we have a point selected, 
        if(self.selected_point_index is not None):
            # move the point away from the backplane by keeping one of x,y,z as originally placed
            fix_idx = (self.mouse_end_pane_idx_on_select + 1) % 3
            xyz[fix_idx] = self.points_xyz[self.selected_point_index][fix_idx]           
            self.points_xyz[self.selected_point_index] = xyz
            self.redraw(showframe_xyz = xyz)
            if(self.on_move_cb):
                self.on_move_cb(self, xyz, self.selectable_point_index, self.selected_point_index)
        else:
        # If we don't have a point selected, see if we could select one
            self.check_for_selectable_point(xy)
            # if we could, show that possibility via cursor and frame lines (or turn these off)
            if (self.selectable_point_index is not None):  
                self.fig.canvas.set_cursor(Cursors.HAND)
                self.redraw(showframe_xyz = xyz)
                if(self.on_move_cb):
                    self.on_move_cb(self, xyz, self.selectable_point_index, self.selected_point_index)
            else:
                self.redraw(showframe_xyz = None)      
                self.fig.canvas.set_cursor(Cursors.POINTER)
                if(self.on_move_cb):
                    self.on_move_cb(self, xyz, self.selectable_point_index, self.selected_point_index)


    def check_for_selectable_point(self,xy):
        from mpl_toolkits.mplot3d import proj3d
        width, height = self.fig.canvas.get_width_height()
        pix_tol = 5
        x_tol, y_tol = [pix_tol/width, pix_tol/height]
        for p_ind, p in enumerate(self.points_xyz):
            x,y,_= proj3d.proj_transform(p[0], p[1], p[2], self.ax.get_proj())
            if(abs(x-xy[0])< x_tol and abs(y-xy[1])<y_tol):
                self.selectable_point_index = p_ind
                return
        self.selectable_point_index = None
        return


class mouse_3D:

    def __init__(self, plt, ax, on_click_internal, on_move_internal):
        self.plt = plt
        self.ax = ax
        self.on_click_internal = on_click_internal
        self.on_move_internal = on_move_internal
        self.in_axes_range_prev = False
        self.click_binding_id = None
        self.plt.connect('motion_notify_event', self.on_move)

    def on_move(self, event):
        global in_axes_range_prev
        if event.inaxes:
            if type(getattr(self.ax, 'invM', None)) is None:
                return  # Avoid calling format_coord during redraw/rotation
            s = self.ax.format_coord(event.xdata, event.ydata)
            info = self._get_pane_coords(s)
            if (info == None):
                return
            pt, ep_idx = info[0], info[1]
            xy = [float(event.xdata), float(event.ydata)]
            in_axes_range_now = self._in_axes_range(pt)
            self.on_move_internal(pt,  xy, ep_idx)
            if(not (in_axes_range_now == self.in_axes_range_prev)):
                if in_axes_range_now:
                    self.ax.mouse_init(rotate_btn=0)
                    self.click_binding_id = self.plt.connect('button_press_event', self.on_click)
                else:
                    self.plt.disconnect(self.click_binding_id)
                    self.ax.mouse_init(rotate_btn=1)
                    event.button = None
                self.in_axes_range_prev = in_axes_range_now
     
    def on_click(self, event):
        if event.button is MouseButton.LEFT:
            s = self.ax.format_coord(event.xdata, event.ydata)
            info = self._get_pane_coords(s)
            if (info == None):
                return
            pt, ep_idx = info
            if(self._in_axes_range(pt)):
                self.on_click_internal(pt, ep_idx)
            
    def _get_pane_coords(self, s):
        # gets x,y,z of mouse position from s=ax.format_coord(event.xdata, event.ydata)
        if('elevation' in s):
            return None
        
        s=s.split(",")
        xyz=[0,0,0]
        for idx, valstr in enumerate(s):
            if(' pane' in valstr):
                end_pane_idx = idx
            valstr=valstr.replace(' pane','')
            ordinate = valstr.split("=")[0].strip()
            i = ['x','y','z'].index(ordinate)
            xyz[i]=float(valstr.split("=")[1].replace('−','-'))

        return xyz, end_pane_idx


    def _in_axes_range(self, p):
        # determines if x,y and z are all in the axis ranges
        if p == None:
            return False
        x_in = self.ax.get_xlim()[0] <= p[0] <= self.ax.get_xlim()[1]
        y_in = self.ax.get_ylim()[0] <= p[1] <= self.ax.get_ylim()[1]
        z_in = self.ax.get_zlim()[0] <= p[2] <= self.ax.get_zlim()[1]
        return (x_in and y_in and z_in)



# For backwards compatibility with V1.0.0
class define_points(xyz_canvas):
    import warnings
    def __init__(self, *args, on_complete_cb=None, **kwargs):
        self.warnings.warn(
            "define_points is deprecated and will be removed in a future version. "
            "Please use NewClassName instead.",
            DeprecationWarning,
            stacklevel=2
        )
        if on_complete_cb is not None:
            self.warnings.warn("on_complete_cb is no longer used and will be ignored.", DeprecationWarning)
        super().__init__(*args, **kwargs)
