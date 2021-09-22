# This file is adapted from
# https://github.com/maximecb/gym-minigrid/blob/master/gym_minigrid/window.py


import sys

# Only ask users to install matplotlib if they actually need it
try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    print(
        "To display the environment in a window, please install matplotlib, eg:"
    )
    print("pip3 install --user matplotlib")
    sys.exit(-1)


class Window:
    """
    Window to draw a gridworld instance using Matplotlib
    """

    def __init__(self, title):
        self.fig = None

        self.imshow_obj = None

        # Create the figure and axes
        self.fig, self.ax = plt.subplots()

        # Show the env name in the window title
        self.fig.canvas.set_window_title(title)

        # Turn off x/y axis numbering/ticks
        self.ax.xaxis.set_ticks_position("none")
        self.ax.yaxis.set_ticks_position("none")
        _ = self.ax.set_xticklabels([])
        _ = self.ax.set_yticklabels([])

        # Flag indicating the window was closed
        self.closed = False
        self.title = ""

        def close_handler(evt):
            self.closed = True

        self.fig.canvas.mpl_connect("close_event", close_handler)

        # Remove all keymaps
        for key in plt.rcParams.keys():
            if "keymap" in key:
                plt.rcParams[key].clear()

    def show_obs(self, img, msg=""):
        """
        Show an rbg tiles of the observation and in-game message
        """

        # Show the first image of the environment
        if self.imshow_obj is None:
            self.imshow_obj = self.ax.imshow(img, interpolation="bilinear")

        self.imshow_obj.set_data(img)
        self.fig.canvas.draw()

        if msg != self.title:
            self.title = msg
            plt.title(msg, loc="left")

        # Let matplotlib process UI events
        # This is needed for interactive mode to work properly
        plt.pause(0.001)

    def set_caption(self, text):
        """
        Set/update the caption text below the image
        """

        plt.xlabel(text)

    def reg_key_handler(self, key_handler):
        """
        Register a keyboard event handler
        """

        # Keyboard handler
        self.fig.canvas.mpl_connect("key_press_event", key_handler)

    def show(self, block=True):
        """
        Show the window, and start an event loop
        """

        # If not blocking, trigger interactive mode
        if not block:
            plt.ion()

        # Show the plot
        # In non-interative mode, this enters the matplotlib event loop
        # In interactive mode, this call does not block
        plt.show()

    def close(self):
        """
        Close the window
        """

        plt.close()
        self.closed = True
