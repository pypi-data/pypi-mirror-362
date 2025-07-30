
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d as mpl
from matplotlib.backend_bases import MouseButton
from matplotlib.backend_tools import Cursors
from matplotlib.widgets import Button


def _interleave(ends):
    a = ends[0]
    b = ends[1]
    return [a[0],b[0]], [a[1],b[1]], [a[2],b[2]]

class define_points:

    def __init__(self, on_complete_cb,
                 xlim =[0,1], ylim =[0,1], zlim=[0,1],
                 xlabel="x", ylabel="y", zlabel="z"):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.xlim=xlim
        self.ylim=ylim
        self.zlim=zlim
        self.xlabel=xlabel
        self.ylabel=ylabel
        self.zlabel=zlabel
        self.points_xyz = []
        self.selectable_point_index = None
        self.selected_point_index = None
        self.mouse_end_pane_idx_on_select = None
        self.init_canvas()
        self.on_complete_cb = on_complete_cb
        self.pointer = mouse_3D(plt, self.ax, self.on_pointer_click, self.on_pointer_move)
        plt.show()

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
        self.ax.figure.canvas.draw_idle()
        self.buttons = buttons(plt, self.fig, self.on_button_press)

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

    def on_button_press(self,action):
        if action == 'clear':
            self.init_canvas()
        elif action == 'save':
            self.on_complete_cb(self.points_xyz)
        elif action == 'exit':
            plt.close()

    def on_pointer_click(self, xyz, ep_idx):
        # If we click whilst moving a point, drop it.
        # Note that its xyz will have been updated during the move to this point
        if(self.selected_point_index is not None):        
            self.selected_point_index = None   
            self.redraw(showframe_xyz = None)
        else:
        # we were just roaming and clicked
            # so if we are over a point and clicked on it, select it
            if(self.selectable_point_index is not None):  
                self.selected_point_index = self.selectable_point_index    
            else:
            # if there's nothing to select,  append the point and immediately select it
                self.points_xyz.append(xyz)         
                self.selected_point_index = len(self.points_xyz) - 1        
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
        else:
        # If we don't have a point selected, see if we could select one
            self.check_for_selectable_point(xy)
            # if we could, show that possibility via cursor and frame lines (or turn these off)
            if (self.selectable_point_index is not None):  
                self.fig.canvas.set_cursor(Cursors.HAND)
                self.redraw(showframe_xyz = xyz)
            else:
                self.redraw(showframe_xyz = None)      
                self.fig.canvas.set_cursor(Cursors.POINTER)  

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


class buttons:
    def __init__(self, plt, fig, buttons_cb):
        self.plt = plt
        self.fig = fig
        self.buttons_cb = buttons_cb
        self.buttons = []

        # Layout settings
        button_height = 0.05
        button_width = 0.2
        spacing = 0.01
        start_y = 0.9

        buttons = [
            ('Clear canvas', 'clear'),
            ('Save', 'save'),
            ('Exit', 'exit'),
            ]

        for i, (label, action) in enumerate(buttons):
            ax = fig.add_axes([0.01, start_y - i*(button_height + spacing), button_width, button_height])
            btn = Button(ax, label)
            btn.on_clicked(lambda event, act=action: self.buttons_cb(act))
            self.buttons.append(btn)


class mouse_3D:

    def __init__(self, plt, ax, on_click_cb, on_move_cb):
        self.plt = plt
        self.ax = ax
        self.on_click_cb = on_click_cb
        self.on_move_cb = on_move_cb
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
            self.on_move_cb(pt,  xy, ep_idx)
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
                self.on_click_cb(pt, ep_idx)
            
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
