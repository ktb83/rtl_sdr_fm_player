"""Custom widgets module for rtl_sdr_fm_player"""
import time

import tkinter as tk

class Marquee(tk.Canvas):  # pylint: disable=too-many-ancestors
    """A scrolling text marquee using tkinter canvas widget"""
    def __init__(self, parent, text, font=None, the_args=None):
        if the_args is None:
            the_args = {'margin': 2, 'borderwidth': 0, 'fps': 30,
                        'width': 265, 'height': 22, 'highlightthickness': 0,
                        'relief': 'flat', 'font': None, 'fgd': None, 'bgd': None,
                        'highlightcolor': None,
                        'highlightbackground': None}
        tk.Canvas.__init__(self, parent, borderwidth=the_args['borderwidth'],
                           relief=the_args['relief'], bg=the_args['bgd'],
                           width=the_args['width'], height=the_args['height'],
                           highlightthickness=the_args['highlightthickness'],
                           highlightcolor=the_args['highlightcolor'],
                           highlightbackground=the_args['highlightbackground'])
        self.fps = the_args['fps']
        self.font = font
        self.fgd = the_args['fgd']
        self.text = self.create_text(0, -1000, fill=self.fgd, font=self.font,
                                     text=text, anchor="w", tags=("text",))
        self.animate()

    def update_text(self, new_text):
        """Update marquee text"""
        self.delete(self.text)
        self.text = self.create_text(0, -1000, fill=self.fgd, font=self.font,
                                     text=new_text, anchor="w", tags=("text",))

    def animate(self):
        """Scroll the marquee text"""
        (x_0, y_0, x_1, _y_1) = self.bbox("text")
        if x_1 < 0 or y_0 < 0:
            x_0 = self.winfo_width()
            y_0 = int(self.winfo_height() / 2)
            self.coords("text", x_0, y_0)
        else:
            self.move("text", -1, 0)
        self.after_id = self.after(int(1000/self.fps), self.animate)


class PresetButton(tk.Radiobutton):  # pylint: disable=too-many-ancestors
    """A custom radio button using tkinter Radiobutton widget"""
    def __init__(self, parent, args=None):
        if args is None:
            args = {'w': 5, 'bw': 0, 'sc': 'black', 'fg': 'white', 'bg': 'gray11',
                    'afg': 'white', 'abg': 'gray11', 'hlc': 'gray11', 'hlbg': 'gray11',
                    'txt': '', 'val': '', 'name': '', 'var': None, 'sp_cmd': None, 'lp_cmd': None}
        tk.Radiobutton.__init__(
            self, parent, width=args['w'], borderwidth=args['bw'],
            selectcolor=args['sc'], fg=args['fg'], bg=args['bg'],
            activeforeground=args['afg'], activebackground=args['abg'],
            highlightcolor=args['hlc'], highlightbackground=args['hlbg'],
            name=args['name'], text=args['txt'], value=args['val'], variable=args['var'])
        self.short_press_cmd = args.get('sp_cmd', None)
        self.long_press_cmd = args.get('lp_cmd', None)
        self.press_time = 0
        self.release_time = 0
        self.after_id = None
        self.parent = parent
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

    def _on_press(self, event):
        del event  # unused
        self.press_time = time.time()
        print('press time: ' + str(self.press_time))

    def _on_release(self, event):
        del event  # unused
        self.release_time = time.time()
        print('release time: ' + str(self.release_time))
        if self.release_time - self.press_time > 2:
            if self.long_press_cmd is not None:
                self.long_press_cmd()
        else:
            if self.short_press_cmd is not None:
                self.short_press_cmd()

    def set_short_press_cmd(self, cmd):
        """Set short press command"""
        self.short_press_cmd = cmd

    def set_long_press_cmd(self, cmd):
        """Set long press command"""
        self.long_press_cmd = cmd


class RoundedButton(tk.Canvas):  # pylint: disable=too-many-ancestors
    """A custom rounded-corner button using tkinter canvas widget"""
    def __init__(self, parent, args=None):
        if args is None:
            args = {'width': 64, 'height': 64, 'cornerradius': 8,
                    'padding': 0, 'color': 'black', 'bg': 'gray11', 'image': None,
                    'press_command': None, 'release_command': None,
                    'repeatdelay': None, 'repeatinterval': None}
        tk.Canvas.__init__(self, parent, borderwidth=0, selectborderwidth=0,
                           insertwidth=0, relief="flat", highlightthickness=0,
                           bg=args['bg'])
        self.press_command = args.get('press_command', None)
        self.release_command = args.get('release_command', None)
        self.repeatdelay = args.get('repeatdelay', None)
        self.repeatinterval = args.get('repeatinterval', None)
        self.after_id = None
        self.parent = parent
        self.canvas_back = None
        if args['cornerradius'] > 0.5 * args['width']:
            print("Error: cornerradius is greater than width.")
            return None
        if args['cornerradius'] > 0.5 * args['height']:
            print("Error: cornerradius is greater than height.")
            return None
        rad = 2 * args['cornerradius']
        def shape():
            self.create_polygon(
                (args['padding'],
                 args['height']-args['cornerradius']-args['padding']-1,
                 args['padding'],
                 args['cornerradius']+args['padding'],
                 args['padding']+args['cornerradius'],
                 args['padding'],
                 args['width']-args['padding']-args['cornerradius']-1,
                 args['padding'],
                 args['width']-args['padding']-1,
                 args['cornerradius']+args['padding'],
                 args['width']-args['padding']-1,
                 args['height']-args['cornerradius']-args['padding']-1,
                 args['width']-args['padding']-args['cornerradius']-1,
                 args['height']-args['padding']-1,
                 args['padding']+args['cornerradius'],
                 args['height']-args['padding']-1),
                fill=args['color'], outline=args['color'], width=0)
            self.create_arc(
                (args['padding'], args['padding']+rad,
                 args['padding']+rad, args['padding']),
                start=90, extent=90,
                fill=args['color'], outline=args['color'], width=0)
            self.create_arc(
                (args['width']-args['padding']-rad-1, args['padding'],
                 args['width']-args['padding']-1, args['padding']+rad),
                start=0, extent=90,
                fill=args['color'], outline=args['color'], width=0)
            self.create_arc(
                (args['width']-args['padding']-1, args['height']-rad-args['padding']-1,
                 args['width']-args['padding']-rad-1, args['height']-args['padding']-1),
                start=270, extent=90,
                fill=args['color'], outline=args['color'], width=0)
            self.create_arc(
                (args['padding'], args['height']-args['padding']-rad-1,
                 args['padding']+rad, args['height']-args['padding']-1),
                start=180, extent=90,
                fill=args['color'], outline=args['color'], width=0)

        shape()
        (x_0, y_0, x_1, y_1) = self.bbox("all")
        width = (x_1-x_0-3)
        height = (y_1-y_0-3)
        self.configure(width=width, height=height)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        if args.get('image', None) is not None:
            bg_pos_x = (width / 2)
            bg_pos_y = (height / 2)
            self.canvas_back = self.create_image(bg_pos_x, bg_pos_y,
                                                 image=args['image'])
        return None

    def _on_press(self, event):
        del event  # unused
        self.configure(relief="sunken")
        if self.press_command is not None:
            self.press_command()
            if self.repeatdelay is not None:
                self.after_id = self.after(self.repeatdelay, self._on_repeat)

    def _on_repeat(self):
        self.configure(relief="sunken")
        if self.press_command is not None:
            self.press_command()
            if self.repeatinterval is not None:
                self.after_id = self.after(self.repeatinterval, self._on_repeat)

    def _on_release(self, event):
        del event  # unused
        self.configure(relief="raised")
        if self.after_id is not None:
            self.after_cancel(self.after_id)
        if self.release_command is not None:
            self.release_command()

    def update_image(self, image=None):
        """Change the button image"""
        if image is not None:
            self.itemconfig(self.canvas_back, image=image)

    def update_release_command(self, release_command=None):
        """Change the release command"""
        if release_command is not None:
            self.release_command = release_command
