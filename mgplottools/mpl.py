"""
Support routines for matplotlib plotting.

The module also contains a standard palette of colors (`colors` module
dictionary) and line styles (`ls` module dictionary).

For the colors, it is recommended to set up the color cycle by hand in your
matplotlibrc file. Alternatively, you can call

    >>> mgplottools.mpl.set_color_cycle()

in order to enforce the use of the module color palette at runtime.

For the linestyles (which are encoded as "dashes"), you may use a cyclic
iterator while plotting:

    >>> ls_cycle = mgplottools.mpl.new_ls_cycle()
    >>> ax.plot(linspace(0, 10, 100), linspace(0, 10, 100),
    >>>         dashes=next(ls_cycle))

You must create a new cycle object each time your want to restart the cycle
(e.g. for a new panel)
"""
from itertools import cycle
import matplotlib
import matplotlib.figure
import numpy as np
from matplotlib.ticker import AutoMinorLocator, FormatStrFormatter

cm2inch = 0.39370079


# colors


colors = {
"white"        : (255, 255, 255), #ffffff
"black"        : (0, 0, 0),       #000000
"blue"         : (55, 126, 184),  #377eb8
"orange"       : (255, 127, 0),   #ff7f00
"red"          : (228, 26, 28),   #e41a1c
"green"        : (77, 175, 74),   #4daf4a
"purple"       : (152, 78, 163),  #984ea3
"brown"        : (166, 86, 40),   #a65628
"pink"         : (247, 129, 191), #f781bf
"yellow"       : (210, 210, 21),  #d2d215
"lightred"     : (251, 154, 153), #fb9a99
"lightblue"    : (166, 206, 227), #a6cee3
"lightorange"  : (253, 191, 111), #fdbf6f
"lightgreen"   : (178, 223, 138), #b2df8a
"lightpurple"  : (202, 178, 214), #cab2d6
"grey"         : (153, 153, 153), #999999
}


def get_color(name, alpha=0.0, format='web'):
    """
    Return color for the given color name, depending on `format`.

    If format is 'rgb', return (r,g,b) tuple ( values in [0,1) )

    If format is 'rgba', return (r,g,b,a) tuple ( values in [0,1) ), where a is
    the given alpha value

    If format is 'web', return rgb hex string (with '#' prefix)
    """
    r, g, b = colors[name.lower()]
    if format == 'web':
        return "#%02x%02x%02x" % (r, g, b)
    if format == 'rgb':
        return (r, g, b)
    elif format == 'rgba':
        return (r, g, b, alpha)


def set_color_cycle(color_cycle=None):
    """
    Set the automatic matplotlib color cycle to the given array of color names.

    `color_cycle` must be an array of color names that appear in the module
    `color` dictionary. It defaults to

    ["blue", "orange", "red", "green", "purple", "brown", "pink", "yellow",
     "lightred", "lightblue", "lightorange", "lightgreen", "lightpurple"]

    """
    if color_cycle is None:
        color_cycle = ["blue", "orange", "red", "green", "purple",
        "brown", "pink", "yellow", "lightred", "lightblue", "lightorange",
        "lightgreen", "lightpurple"]
    matplotlib.rc('axes',
                  color_cycle=[get_color(cname) for cname in color_cycle])


# line styles


ls = {
    "solid"            : (None, None),
    "dashed"           : (4,1.5),
    "long-dashed"      : (8,1),
    "double-dashed"    : (3,1,3,2.5),
    "dash-dotted"      : (5,1,1,1),
    "dot-dot-dashed"   : (1,1,1,1,7,1),
    "dash-dash-dotted" : (4,1,4,1,1,1),
    "dotted"           : (1,1),
    "double-dotted"    : (1,1,1,3),
}


def new_ls_cycle(ls_cycle=None):
    """
    Return a cyclic iterator of linestyles (dashes)

    ls_cycle must be an array of line style names that appear in the module
    `ls` dictionary. It defaults to

    ["solid", "dashed", "long-dashed", "dash-dotted", "dash-dash-dotted",
     "dot-dot-dashed",  "double-dashed", "dotted", "double-dotted"]

    Use as:

    >>> ls_cycle = mgplottools.mpl.new_ls_cycle()
    >>> ax.plot(linspace(0, 10, 100), linspace(0, 10, 100),
    >>>         dashes=next(ls_cycle))
    """
    if ls_cycle is None:
        ls_cycle = ["solid", "dashed", "long-dashed", "dash-dotted",
                    "dash-dash-dotted", "dot-dot-dashed",  "double-dashed",
                    "dotted", "double-dotted"]
    return cycle([ls[l] for l in ls_cycle])


# utilities


def new_figure(fig_width, fig_height, size_in_cm=True, style=None,
    no_backend=False, quiet=False, **kwargs):
    """
    Return a new matplotlib figure of the specified size (in cm by default)

    Information about the matplotlib backend, settings and the figure will be
    printed on STDOUT, unless `quiet=True` is given.

    The remaining kwargs are passed to the Figure init routine

    Arguments
    ---------

    fig_width: float
        total width of figure canvas, in cm (or inches if `size_in_cm=False`

    fig_height: float
        total height of figure canvas, in cm (or inches if `size_in_cm=False`

    size_in_cm: boolean, optional
        give as False to indicate that `fig_width` and `fig_height` are in
        inches instead of cm

    style: string or array of strings, optional
        A style file to overwrite or ammend the matplotlibrc file. For
        matplotlib version >=1.4, the style sheet feature will be used, see
        <http://matplotlib.org/users/style_sheets.html>
        In older versions of matplotlib, `style` must a filename or URL string;
        the contents of the file will be merged with the matplotlibrc settings

    no_backend: boolean, optional
        If given as True, skip the use of the pyplot entirely, creating the
        figure in a purely object-oriented way.

    quiet: boolean, optional

    Notes
    -----

    You may use the figure as follows, assuming the pyplot is used
    (`no_backend=False`)

    >>> import matplotlib
    >>> matplotlib.use('PDF') # backend ('PDF' for pdf, 'Agg' for png)
    >>> fig = mgplottools.mpl.new_figure(10, 4)
    >>> pos = [0.05, 0.05, 0.9, 0.9] # left, bottom offset, width, height
    >>> ax = fig.add_axes(pos)
    >>> ax.plot(linspace(0, 10, 100), linspace(0, 10, 100))
    >>> fig.savefig('out.pdf', format='pdf')

    Alternatively, for a GUI backend, instead of `fig.savefig()`, you can
    display all created figures using `fig.show()` -- it is set up as an alias
    to matplotlib.pyplot.show().

    If you want to do any interactive plotting in ipython (i.e. manipulating
    the plot after its creation), make sure to load the %matplotlib or %pylab
    magic functions. Also, you must use pyplot

    >>> import matplotlib.pyplot as plt

    Do not use `plt.ion()`, which does not work in ipython.
    Simply create a figure, then call `plt.show()` and `plt.draw()`

    If not using a backend (`no_backend=True`, bypassing the pyplot state
    machine), you must create the canvas manually. Consider using the
    `show_fig`, `write_pdf`, `write_eps`, and `write_png` routines
    """
    if (no_backend):
        from matplotlib.figure import Figure as figure
        backend = "N/A"
        using_pyplot = False
    else:
        using_pyplot = True
        from matplotlib.pyplot import figure
        backend = matplotlib.get_backend().lower()

    if not quiet:
        print "Using backend: ", backend
        print "Using maplotlibrc: ", matplotlib.matplotlib_fname()
    if style is not None:
        try:
            import matplotlib.style as mpl_style
            mpl_style.use(style)
            if not quiet:
                print "Using style: ", style
        except ImportError:
            if not quiet:
                print "The style package was added to matplotlib in version " \
                "1.4. It is not available in your release.\n"
                print "Using fall-back implementation"
            try:
                from matplotlib import rc_params_from_file
                rc = rc_params_from_file(style, use_default_template=False)
                matplotlib.rcParams.update(rc)
            except:
                print "Style '%s' not found" % style
        except ValueError as e:
            print "Error loading style %s: %s" % (style, e)

    if size_in_cm:
        if not quiet:
            print "Figure height: ", fig_height, " cm"
            print "Figure width : ", fig_width, " cm"
        fig = figure(figsize=(fig_width*cm2inch, fig_height*cm2inch),
                      **kwargs)
    else:
        if not quiet:
            print "Figure height: ", fig_height / cm2inch, " cm"
            print "Figure width : ", fig_width / cm2inch , " cm"
        fig = figure(figsize=(fig_width, fig_height), **kwargs)
    if using_pyplot:
        # replace fig.show() with matplotlib.pyplot.show()
        from matplotlib.pyplot import show
        fig.show = show
    return fig


def set_axis(ax, which_axis, start, stop, step, range=None, minor=0,
             format=None, label=None, labelpad=None, ticklabels=None):
    """
    Format the x or y axis of the given axes object

    Parameters
    ----------

    ax: instance of matplotlib.axes.Axes
        Axes instance in which to set the x or y axis
    which_axis: str
        Either 'x', or 'y'
    start: float
        value for first tick on the axis (and start of axis, unless range is
        given
    stop: float
        value for last tick on the axis (and stop of axis, unless range is
        given)
    step: float
        step between major ticks
    range: tuple
        The minimum and maximum value of the axis. If not given, [start, stop]
    minor:
        Number of subdivisions of the interval between major ticks; e.g.,
        minor=2 will place a single minor tick midway between major ticks.
    format: str
        Format string to use for tick labels. Will be chosen automatically if
        not given
    label: str
        Axis-label
    labelpad: float
        spacing in points between the label and the axis
    ticklabels: array of strings, boolean
        If given, labels for the major tick marks. Alternatively, if given as a
        boolean value "False", suppress labels
    """
    if which_axis == 'x':
        axis = ax.xaxis
    elif which_axis == 'y':
        axis = ax.yaxis
    else:
        raise ValueError('which_axis must be either "x", or "y"')
    axis.set_ticks(np.arange(float(start),
                   float(stop) + float(step)/2.0,
                   float(step)))
    if format is not None:
        majorFormatter = FormatStrFormatter(format)
        axis.set_major_formatter(majorFormatter)
    if minor > 0:
        minorLocator = AutoMinorLocator(minor)
        axis.set_minor_locator(minorLocator)
    if range is None:
        range = [start, stop]
    if which_axis == 'x':
        ax.set_xlim(range)
        if label is not None:
            ax.set_xlabel(label, labelpad=labelpad)
        if ticklabels is not None:
            try:
                ax.set_xticklabels([str(v) for v in ticklabels])
            except TypeError:
                if not ticklabels:
                    ax.set_xticklabels([])
    elif which_axis == 'y':
        ax.set_ylim(range)
        if label is not None:
            ax.set_ylabel(label, labelpad=labelpad)
        if ticklabels is not None:
            try:
                ax.set_yticklabels([str(v) for v in ticklabels])
            except TypeError:
                if not ticklabels:
                    ax.set_yticklabels([])


def show_fig(fig):
    """
    Display the given figure in a custom Qt4 window. This is independent from
    the pyplot framework and thus works for figures that were created with
    `no_backend=True`.

    However, after calling this routine, an existing pyplot backend will be
    permanently changed and may be dysfunctional.

    Also, interactively showing the figure can change its size, so you you want
    to generate a PDF of PNG file after showing the figure, make sure the
    figure size is correct.
    """
    from PyQt4.QtCore import Qt
    from PyQt4.QtGui import QMainWindow, QWidget, QVBoxLayout, QApplication
    # TODO: make interactive
    # http://stackoverflow.com/questions/22729206/matplotlib-show-figure-again

    class AppForm(QMainWindow):
        def __init__(self, fig):
            parent = None
            QMainWindow.__init__(self, parent)
            self.create_main_frame(fig)
            self.on_draw()

        def create_main_frame(self, fig):
            from matplotlib.backends.backend_qt4agg import (
                        FigureCanvasQTAgg as FigureCanvas,
                        NavigationToolbar2QT as NavigationToolbar)
            self.main_frame = QWidget()
            self.fig = fig
            self.canvas = FigureCanvas(self.fig)
            self.canvas.setParent(self.main_frame)
            self.canvas.setFocusPolicy(Qt.StrongFocus)
            self.canvas.setFocus()

            self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

            self.canvas.mpl_connect('key_press_event', self.on_key_press)

            vbox = QVBoxLayout()
            vbox.addWidget(self.canvas)  # the matplotlib canvas
            vbox.addWidget(self.mpl_toolbar)
            self.main_frame.setLayout(vbox)
            self.setCentralWidget(self.main_frame)

        def on_draw(self):
            self.canvas.draw()

        def on_key_press(self, event):
            from matplotlib.backend_bases import key_press_handler
            print('you pressed', event.key)
            # implement the default mpl key press events described at
            # http://matplotlib.org/users/navigation_toolbar.html
            key_press_handler(event, self.canvas, self.mpl_toolbar)

    app = QApplication([])
    form = AppForm(fig)
    form.show()
    app.exec_()


def write_pdf(fig, outfile, dpi=72):
    """
    Write a pdf of the given figure, indendent of the pyplot backend.
    However, if the figure was created from pyplot, an existing pyplot backend
    will be permanently changed and may be dysfunctional.
    """
    from matplotlib.backends.backend_pdf \
    import FigureCanvasPdf as FigureCanvas
    canvas = FigureCanvas(fig)
    canvas.print_figure(outfile, dpi=dpi)


def write_png(fig, outfile, dpi=72):
    """
    Write a png of the given figure, indendent of the pyplot backend.
    However, if the figure was created from pyplot, an existing pyplot backend
    will be permanently changed and may be dysfunctional.
    """
    from matplotlib.backends.backend_agg \
    import FigureCanvasAgg as FigureCanvas
    canvas = FigureCanvas(fig)
    canvas.print_figure(outfile, dpi=dpi)


def write_eps(fig, outfile, dpi=72):
    """
    Write a eps of the given figure, indendent of the pyplot backend.
    However, if the figure was created from pyplot, an existing pyplot backend
    will be permanently changed and may be dysfunctional.
    """
    from matplotlib.backends.backend_ps \
    import FigureCanvasPS as FigureCanvas
    canvas = FigureCanvas(fig)
    canvas.print_figure(outfile, dpi=dpi)
