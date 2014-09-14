"""
Input/Output routines
"""
import numpy as np


def writetotxt(fname, *args, **kwargs):
    """
    Inverse function to numpy.genfromtxt and similar to `numpy.savetxt`,
    but allowing to write *multiple* numpy arrays as columns to a text file.
    Also, handle headers/footers more intelligently.

    The first argument is the filename or handler to which to write, followed
    by an arbitrary number of numpy arrays, to be written as columns in the
    file (real arrays will produce once column, complex arrays two). The
    remaining keyword arguments are passed directly to `numpy.savetxt` (with
    fixes to the header/footer lines, as described below)

    Parameters
    ----------
    fname : filename or file handle
        If the filename ends in ``.gz``, the file is automatically saved in
        compressed gzip format.  `loadtxt` understands gzipped files
        transparently.
    *args: ndarray
        Numpy arrays to write to fname. All arrays must have the same length
    fmt : str or sequence of strs, optional
        A single format (%10.5f), a sequence of formats, or a
        multi-format string, e.g. 'Iteration %d -- %10.5f', in which
        case `delimiter` is ignored. For a complex array in `*args`, a format
        for the real and imaginary parts must be given.
        Defaults to '%.18e'
    delimiter : str, optional
        Character separating columns. Defaults to ''
    header : str or sequence of strs, optional
        String that will be written at the beginning of the file. If sequence
        of strings, multiple lines will be written.
    footer : str or sequence of strs, optional
        String that will be written at the end of the file. If sequence of
        strings, multiple lines will be written
    comments : str, optional
        String that will be prepended to the each line of the ``header`` and
        ``footer`` strings, to mark them as comments. Defaults to '# '


    Notes
    -----

    The `header` and `footer` lines are handled more intelligently than by the
    `numpy.savetxt` routine.  First, header and footer may be an array of lines
    instead of just a (multiline) string.  Second, each line in the header may
    or may not already include the `comments` prefix. If a line does not
    include the `comments` prefix yet, but starts with a sufficient number of
    spaces, the `comments` prefix will not be prepended to the line in output,
    but will overwrite the beginning of the line, so as not to change the line
    length. E.g. giving `header="   time [ns]"` will result in a header line of
    `#  time [ns]` in the output, not `#    time [ns]`.

    Further explanation of the `fmt` parameter
    (``%[flag]width[.precision]specifier``):

    flags:
        ``-`` : left justify

        ``+`` : Forces to precede result with + or -.

        ``0`` : Left pad the number with zeros instead of space (see width).

    width:
        Minimum number of characters to be printed. The value is not truncated
        if it has more characters.

    precision:
        - For integer specifiers (eg. ``d,i``), the minimum number of
          digits.
        - For ``e, E`` and ``f`` specifiers, the number of digits to print
          after the decimal point.
        - For ``g`` and ``G``, the maximum number of significant digits.

    specifiers (partial list):
        ``c`` : character

        ``d`` or ``i`` : signed decimal integer

        ``e`` or ``E`` : scientific notation with ``e`` or ``E``.

        ``f`` : decimal floating point

        ``g,G`` : use the shorter of ``e,E`` or ``f``

    For more details, see `numpy.savetxt`

    """

    fmt       = kwargs.get('fmt', '%.18e')
    delimiter = kwargs.get('delimiter', '')
    header    = kwargs.get('header', '')
    footer    = kwargs.get('footer', '')
    comments  = kwargs.get('comments', "# ")
    l_comments = len(comments)

    # open file
    own_fh = False
    if isinstance(fname, str):
        own_fh = True
        if fname.endswith('.gz'):
            import gzip
            fh = gzip.open(fname, 'wb')
        else:
            fh = open(fname, 'w')
    elif hasattr(fname, 'write'):
        fh = fname
    else:
        raise ValueError('fname must be a string or file handle')

    try:

        # write header
        if isinstance(header, (list, tuple)):
            header = "\n".join(header)
        if len(header) > 0:
            for line in header.split("\n"):
                if not line.startswith(comments):
                    if line.startswith(" "*l_comments):
                        line = comments + line[l_comments:]
                    else:
                        line = comments + line
                print >> fh, line

        # check input data and prepare row format
        n_cols = 0
        n_rows = 0
        row_fmt = ""
        completed_row_fmt = False
        if type(fmt) in (list, tuple):
            row_fmt = delimiter.join(fmt)
            completed_row_fmt = True
        elif isinstance(fmt, str):
            if fmt.count('%') > 1:
                row_fmt = fmt
                completed_row_fmt = True
        for a in args:
            if n_rows == 0:
                n_rows = len(a)
            else:
                if n_rows != len(a):
                    raise ValueError("All arrays must be of same length")
            if np.iscomplexobj(a):
                n_cols += 2
                if not completed_row_fmt:
                    row_fmt += "%s%s%s%s" % (fmt, delimiter, fmt, delimiter)
            else:
                n_cols += 1
                if not completed_row_fmt:
                    row_fmt += "%s%s" % (fmt, delimiter)
        if row_fmt.count('%') != n_cols:
            raise ValueError('fmt has wrong number of %% formats:  %s'
                             % row_fmt)
        if not completed_row_fmt:
            if len(delimiter) > 0:
                row_fmt = row_fmt[:-len(delimiter)]
            completed_row_fmt = True

        # write out data
        for i_row in xrange(n_rows):
            row_data = []
            for a in args:
                if np.iscomplexobj(a):
                    row_data.append(a[i_row].real)
                    row_data.append(a[i_row].imag)
                else:
                    row_data.append(a[i_row])
            print >> fh, row_fmt % tuple(row_data)

        # write footer
        if (isinstance(footer, (list, tuple))):
            footer = "\n".join(footer)
        if len(footer) > 0:
            for line in footer.split("\n"):
                if not line.startswith(comments):
                    if line.startswith(" "*l_comments):
                        line = comments + line[l_comments:]
                    else:
                        line = comments + line
                print >> fh, line

    finally:
        if own_fh:
            fh.close()
