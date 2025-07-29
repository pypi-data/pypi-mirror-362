import Oasys.gRPC


# Metaclass for static properties and constants
class WindowType(type):
    _consts = {'CANCEL', 'NO', 'NONMODAL', 'OK', 'YES'}

    def __getattr__(cls, name):
        if name in WindowType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("Window class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in WindowType._consts:
            raise AttributeError("Cannot set Window class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class Window(Oasys.gRPC.OasysItem, metaclass=WindowType):


    def __del__(self):
        if not Oasys.PRIMER._connection:
            return

        if self._handle is None:
            return

        Oasys.PRIMER._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
# If constructor for an item fails in program, then _handle will not be set and when
# __del__ is called to return the object we will call this to get the (undefined) value
        if name == "_handle":
            return None

        raise AttributeError("Window instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# Set the property locally
        self.__dict__[name] = value


# Static methods
    def Error(title, error, buttons=Oasys.gRPC.defaultArg):
        """
        Show an error message in a window

        Parameters
        ----------
        title : string
            Title for window
        error : string
            Error message to show in window.
            The maximum number of lines that can be shown is controlled by the
            Options.max_window_lines option
        buttons : constant
            Optional. The buttons to use. Can be bitwise OR of Window.OK,
            Window.CANCEL,
            Window.YES or
            Window.NO. If this is omitted an OK button will be used.
            By default the window will be modal. If Window.NONMODAL
            is also given the window will be non-modal instead

        Returns
        -------
        int
            Button pressed
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Error", title, error, buttons)

    def GetDirectory(initial=Oasys.gRPC.defaultArg):
        """
        Map the directory selector box native to your machine, allowing you to choose a directory.
        On Unix this will be a Motif selector. Windows will use the standard windows directory selector

        Parameters
        ----------
        initial : string
            Optional. Initial directory to start from

        Returns
        -------
        str
            directory (string), (or None if cancel pressed)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetDirectory", initial)

    def GetFile(extension=Oasys.gRPC.defaultArg, save=Oasys.gRPC.defaultArg, initial=Oasys.gRPC.defaultArg):
        """
        Map a file selector box allowing you to choose a file.
        See also Window.GetFiles() and
        Window.GetFilename()

        Parameters
        ----------
        extension : string
            Optional. Extension to filter by
        save : boolean
            Optional. If true the file selector is to be used for saving a file. If false (default) the file selector is for opening
            a file.
            Due to native operating system file selector differences, on linux new filenames can only be given when saving a file.
            On windows it is possible to give new filenames when opening or saving a file
        initial : string
            Optional. Initial directory to start from

        Returns
        -------
        str
            filename (string), (or None if cancel pressed)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFile", extension, save, initial)

    def GetFilename(title, message, extension=Oasys.gRPC.defaultArg, initial=Oasys.gRPC.defaultArg, save=Oasys.gRPC.defaultArg):
        """
        Map a window allowing you to input a filename (or select it using a file selector). OK and Cancel buttons are shown.
        See also Window.GetFile()

        Parameters
        ----------
        title : string
            Title for window
        message : string
            Message to show in window
        extension : string
            Optional. Extension to filter by
        initial : string
            Optional. Initial value
        save : boolean
            Optional. If true the file selector is to be used for saving a file. If false (default) the file selector is for opening
            a file.
            Due to native operating system file selector differences, on linux new filenames can only be given when saving a file.
            On windows it is possible to give new filenames when opening or saving a file

        Returns
        -------
        str
            filename (string), (or None if cancel pressed)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFilename", title, message, extension, initial, save)

    def GetFiles(extension=Oasys.gRPC.defaultArg):
        """
        Map a file selector box allowing you to choose multiple files.
        See also Window.GetFile() and
        Window.GetFilename()

        Parameters
        ----------
        extension : string
            Optional. Extension to filter by

        Returns
        -------
        str
            List of filenames (strings), or None if cancel pressed
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFiles", extension)

    def GetInteger(title, message, initial=Oasys.gRPC.defaultArg):
        """
        Map a window allowing you to input an integer. OK and Cancel buttons are shown

        Parameters
        ----------
        title : string
            Title for window
        message : string
            Message to show in window
        initial : integer
            Optional. Initial value

        Returns
        -------
        int
            value input (integer), or None if cancel pressed
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetInteger", title, message, initial)

    def GetNumber(title, message, initial=Oasys.gRPC.defaultArg):
        """
        Map a window allowing you to input a number. OK and Cancel buttons are shown

        Parameters
        ----------
        title : string
            Title for window
        message : string
            Message to show in window
        initial : float
            Optional. Initial value

        Returns
        -------
        float
            value input (float), or None if cancel pressed
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetNumber", title, message, initial)

    def GetPassword(title, message):
        """
        Map a window allowing you to input a password. OK and Cancel buttons are shown.
        This is identical to Window.GetString except the
        string is hidden and no initial value can be given

        Parameters
        ----------
        title : string
            Title for window
        message : string
            Message to show in window

        Returns
        -------
        str
            value input (string), or None if cancel pressed
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetPassword", title, message)

    def GetString(title, message, initial=Oasys.gRPC.defaultArg):
        """
        Map a window allowing you to input a string. OK and Cancel buttons are shown

        Parameters
        ----------
        title : string
            Title for window
        message : string
            Message to show in window
        initial : string
            Optional. Initial value

        Returns
        -------
        str
            value input (string), or None if cancel pressed
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetString", title, message, initial)

    def Information(title, info, buttons=Oasys.gRPC.defaultArg):
        """
        Show information in a window

        Parameters
        ----------
        title : string
            Title for window
        info : string
            Information to show in window.
            The maximum number of lines that can be shown is controlled by the
            Options.max_window_lines option
        buttons : constant
            Optional. The buttons to use. Can be bitwise OR of Window.OK,
            Window.CANCEL,
            Window.YES or
            Window.NO. If this is omitted an OK button will be used.
            By default the window will be modal. If Window.NONMODAL
            is also given the window will be non-modal instead

        Returns
        -------
        int
            Button pressed
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Information", title, info, buttons)

    def Message(title, message, buttons=Oasys.gRPC.defaultArg):
        """
        Show a message in a window

        Parameters
        ----------
        title : string
            Title for window
        message : string
            Message to show in window.
            The maximum number of lines that can be shown is controlled by the
            Options.max_window_lines option
        buttons : constant
            Optional. The buttons to use. Can be bitwise OR of Window.OK,
            Window.CANCEL,
            Window.YES or
            Window.NO. If this is omitted an OK button will be used
            By default the window will be modal. If Window.NONMODAL
            is also given the window will be non-modal instead

        Returns
        -------
        int
            Button pressed
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Message", title, message, buttons)

    def Question(title, question, buttons=Oasys.gRPC.defaultArg):
        """
        Show a question in a window

        Parameters
        ----------
        title : string
            Title for window
        question : string
            Question to show in window.
            The maximum number of lines that can be shown is controlled by the
            Options.max_window_lines option
        buttons : constant
            Optional. The buttons to use. Can be bitwise OR of Window.OK,
            Window.CANCEL,
            Window.YES or
            Window.NO. If this is omitted Yes and No button will be used.
            By default the window will be modal. If Window.NONMODAL
            is also given the window will be non-modal instead

        Returns
        -------
        int
            Button pressed
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Question", title, question, buttons)

    def Warning(title, warning, buttons=Oasys.gRPC.defaultArg):
        """
        Show a warning message in a window

        Parameters
        ----------
        title : string
            Title for window
        warning : string
            Warning message to show in window.
            The maximum number of lines that can be shown is controlled by the
            Options.max_window_lines option
        buttons : constant
            Optional. The buttons to use. Can be bitwise OR of Window.OK,
            Window.CANCEL,
            Window.YES or
            Window.NO. If this is omitted an OK button will be used.
            By default the window will be modal. If Window.NONMODAL
            is also given the window will be non-modal instead

        Returns
        -------
        int
            Button pressed
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Warning", title, warning, buttons)

