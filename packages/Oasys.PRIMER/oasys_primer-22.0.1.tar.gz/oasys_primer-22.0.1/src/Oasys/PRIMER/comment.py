import Oasys.gRPC


# Metaclass for static properties and constants
class CommentType(type):
    _consts = {'MULTIPLE', 'SINGLE'}

    def __getattr__(cls, name):
        if name in CommentType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("Comment class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in CommentType._consts:
            raise AttributeError("Cannot set Comment class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class Comment(Oasys.gRPC.OasysItem, metaclass=CommentType):
    _props = {'anchor_mode', 'header', 'include', 'nlines', 'noecho'}
    _rprops = {'exists', 'model'}


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

# If one of the properties we define then get it
        if name in Comment._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in Comment._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("Comment instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Comment._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in Comment._rprops:
            raise AttributeError("Cannot set read-only Comment instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, header=Oasys.gRPC.defaultArg, mode=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, header, mode)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new Comment object

        Parameters
        ----------
        model : Model
            Model that comment will be created in
        header : string
            Optional. Comment number
        mode : constant
            Optional. Anchor: single or multiple

        Returns
        -------
        Comment
            Comment object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def Create(model, modal=Oasys.gRPC.defaultArg):
        """
        Starts an interactive editing panel to create a comment

        Parameters
        ----------
        model : Model
            Model that the comment will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        Comment
            Comment object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def First(model):
        """
        Returns the first comment in the model

        Parameters
        ----------
        model : Model
            Model to get first comment in

        Returns
        -------
        Comment
            Comment object (or None if there are no comments in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FlagAll(model, flag):
        """
        Flags all of the comments in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all comments will be flagged in
        flag : Flag
            Flag to set on the comments

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Comment objects or properties for all of the comments in a model in PRIMER.
        If the optional property argument is not given then a list of Comment objects is returned.
        If the property argument is given, that property value for each comment is returned in the list
        instead of a Comment object

        Parameters
        ----------
        model : Model
            Model to get comments from
        property : string
            Optional. Name for property to get for all comments in the model

        Returns
        -------
        list
            List of Comment objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Comment objects for all of the flagged comments in a model in PRIMER
        If the optional property argument is not given then a list of Comment objects is returned.
        If the property argument is given, then that property value for each comment is returned in the list
        instead of a Comment object

        Parameters
        ----------
        model : Model
            Model to get comments from
        flag : Flag
            Flag set on the comments that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged comments in the model

        Returns
        -------
        list
            List of Comment objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the Comment object for a comment ID

        Parameters
        ----------
        model : Model
            Model to find the comment in
        number : integer
            number of the comment you want the Comment object for

        Returns
        -------
        Comment
            Comment object (or None if comment does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last comment in the model

        Parameters
        ----------
        model : Model
            Model to get last comment in

        Returns
        -------
        Comment
            Comment object (or None if there are no comments in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def Select(flag, prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg):
        """
        Allows the user to select comments using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting comments
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only comments from that model can be selected.
            If the argument is a Flag then only comments that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any comments can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of comments selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def Total(model, exists=Oasys.gRPC.defaultArg):
        """
        Returns the total number of comments in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing comments should be counted. If false or omitted
            referenced but undefined comments will also be included in the total

        Returns
        -------
        int
            number of comments
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the comments in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all comments will be unset in
        flag : Flag
            Flag to unset on the comments

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)



# Instance methods
    def AddLine(self, line_content, line_number=Oasys.gRPC.defaultArg):
        """
        Adds a line, or a list of lines, to a comment object

        Parameters
        ----------
        line_content : String or list of strings
            String that will be added to a line
        line_number : Integer
            Optional. 0: First line, 1: Second line, etc.
            If list of lines has been passed in the first argument, the first line of the list will be inserted in the line number specified in second argument, the second line of the list will be inserted in the following line number, etc.
            If that line already exists, that line and rest of them below will be shifted down.
            If greater than number of existing lines, blank lines will be added.
            If lower than 0, not valid argument.
            If no argument, the line(s) will be appended at the end.

        Returns
        -------
        None
            no return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AddLine", line_content, line_number)

    def Browse(self, modal=Oasys.gRPC.defaultArg):
        """
        Starts an edit panel in Browse mode

        Parameters
        ----------
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        None
            no return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Browse", modal)

    def ClearFlag(self, flag):
        """
        Clears a flag on the comment

        Parameters
        ----------
        flag : Flag
            Flag to clear on the comment

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the comment. The target include of the copied comment can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        Comment
            Comment object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DeleteLine(self, line_number):
        """
        Deletes a line of a comment

        Parameters
        ----------
        line_number : Integer
            Line number to delete (starting at 0). The following lines will be shifted up

        Returns
        -------
        None
            no return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "DeleteLine", line_number)

    def Edit(self, modal=Oasys.gRPC.defaultArg):
        """
        Starts an interactive editing panel

        Parameters
        ----------
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        None
            no return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Edit", modal)

    def Flagged(self, flag):
        """
        Checks if the comment is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the comment

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetLine(self, line=Oasys.gRPC.defaultArg):
        """
        Extracts the lines (the strings) from a comment object

        Parameters
        ----------
        line : integer
            Optional. Line number to be extracted. Default value: 0 (first line)

        Returns
        -------
        str
            String (or None if no lines in the comment and not argument passed)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetLine", line)

    def GetParameter(self, prop):
        """
        Checks if a Comment property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the Comment.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            comment property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this comment (\*COMMENT) and the header of the comment if there is one.
        Note that a carriage return is not added.
        See also Comment.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the comment.
        Note that a carriage return is not added.
        See also Comment.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def ModifyLine(self, line_number, new_line_content):
        """
        Modifies the content of a line in a comment

        Parameters
        ----------
        line_number : Integer
            Line number to modify (starting at 0)
        new_line_content : String
            String that replaces the existing one in a line

        Returns
        -------
        None
            no return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ModifyLine", line_number, new_line_content)

    def Next(self):
        """
        Returns the next comment in the model

        Returns
        -------
        Comment
            Comment object (or None if there are no more comments in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous comment in the model

        Returns
        -------
        Comment
            Comment object (or None if there are no more comments in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on the comment

        Parameters
        ----------
        flag : Flag
            Flag to set on the comment

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def ViewParameters(self):
        """
        Object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. This function temporarily
        changes the behaviour so that if a property is a parameter the parameter name is returned instead.
        This can be used with 'method chaining' (see the example below) to make sure a property argument is correct

        Returns
        -------
        Comment
            Comment object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this comment

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

