import Oasys.gRPC


# Metaclass for static properties and constants
class LinearType(type):
    _consts = {'GLOBAL', 'LOCAL'}

    def __getattr__(cls, name):
        if name in LinearType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("Linear class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in LinearType._consts:
            raise AttributeError("Cannot set Linear class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class Linear(Oasys.gRPC.OasysItem, metaclass=LinearType):
    _props = {'format', 'include', 'lcid'}
    _rprops = {'exists', 'model', 'total'}


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
        if name in Linear._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in Linear._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("Linear instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Linear._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in Linear._rprops:
            raise AttributeError("Cannot set read-only Linear instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, format, lcid, nid, dof, coeff, cid=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, format, lcid, nid, dof, coeff, cid)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new Linear object

        Parameters
        ----------
        model : Model
            Model that Linear will be created in
        format : constant
            Specify the type of constrained linear. Can be
            Linear.GLOBAL or
            Linear.LOCAL)
        lcid : integer
            Linear label
        nid : integer
            Node id
        dof : integer
            Degrees-of-Freedom
        coeff : float
            Non-zero coefficient
        cid : integer
            Optional. Coordinate System ID if format is Linear.LOCAL. The default value is 0

        Returns
        -------
        Linear
            Linear object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def BlankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the constrained linears in the model

        Parameters
        ----------
        model : Model
            Model that all constrained linears will be blanked in
        redraw : boolean
            Optional. If model should be redrawn or not.
            If omitted redraw is false. If you want to do several (un)blanks and only
            redraw after the last one then use false for all redraws apart from the last one.
            Alternatively you can redraw using View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "BlankAll", model, redraw)

    def BlankFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the flagged constrained linears in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged constrained linears will be blanked in
        flag : Flag
            Flag set on the constrained linears that you want to blank
        redraw : boolean
            Optional. If model should be redrawn or not.
            If omitted redraw is false. If you want to do several (un)blanks and only
            redraw after the last one then use false for all redraws apart from the last one.
            Alternatively you can redraw using View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "BlankFlagged", model, flag, redraw)

    def Create(model, modal=Oasys.gRPC.defaultArg):
        """
        Starts an interactive editing panel to create a constrained linear

        Parameters
        ----------
        model : Model
            Model that the constrained linear will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        Linear
            Linear object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def First(model):
        """
        Returns the first constrained linear in the model

        Parameters
        ----------
        model : Model
            Model to get first constrained linear in

        Returns
        -------
        Linear
            Linear object (or None if there are no constrained linears in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FirstFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the first free constrained linear label in the model.
        Also see Linear.LastFreeLabel(),
        Linear.NextFreeLabel() and
        Model.FirstFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get first free constrained linear label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            First free in layer in editing panels). If omitted the whole model will be used (Equivalent to
            First free in editing panels)

        Returns
        -------
        int
            Linear label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FirstFreeLabel", model, layer)

    def FlagAll(model, flag):
        """
        Flags all of the constrained linears in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all constrained linears will be flagged in
        flag : Flag
            Flag to set on the constrained linears

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Linear objects or properties for all of the constrained linears in a model in PRIMER.
        If the optional property argument is not given then a list of Linear objects is returned.
        If the property argument is given, that property value for each constrained linear is returned in the list
        instead of a Linear object

        Parameters
        ----------
        model : Model
            Model to get constrained linears from
        property : string
            Optional. Name for property to get for all constrained linears in the model

        Returns
        -------
        list
            List of Linear objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Linear objects for all of the flagged constrained linears in a model in PRIMER
        If the optional property argument is not given then a list of Linear objects is returned.
        If the property argument is given, then that property value for each constrained linear is returned in the list
        instead of a Linear object

        Parameters
        ----------
        model : Model
            Model to get constrained linears from
        flag : Flag
            Flag set on the constrained linears that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged constrained linears in the model

        Returns
        -------
        list
            List of Linear objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the Linear object for a constrained linear ID

        Parameters
        ----------
        model : Model
            Model to find the constrained linear in
        number : integer
            number of the constrained linear you want the Linear object for

        Returns
        -------
        Linear
            Linear object (or None if constrained linear does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last constrained linear in the model

        Parameters
        ----------
        model : Model
            Model to get last constrained linear in

        Returns
        -------
        Linear
            Linear object (or None if there are no constrained linears in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def LastFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the last free constrained linear label in the model.
        Also see Linear.FirstFreeLabel(),
        Linear.NextFreeLabel() and
        see Model.LastFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get last free constrained linear label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest free in layer in editing panels). If omitted the whole model will be used

        Returns
        -------
        int
            Linear label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "LastFreeLabel", model, layer)

    def NextFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the next free (highest+1) constrained linear label in the model.
        Also see Linear.FirstFreeLabel(),
        Linear.LastFreeLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get next free constrained linear label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest+1 in layer in editing panels). If omitted the whole model will be used (Equivalent to
            Highest+1 in editing panels)

        Returns
        -------
        int
            Linear label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NextFreeLabel", model, layer)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a constrained linear

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only constrained linears from that model can be picked.
            If the argument is a Flag then only constrained linears that
            are flagged with limit can be selected.
            If omitted, or None, any constrained linears from any model can be selected.
            from any model
        modal : boolean
            Optional. If picking is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the pick will be modal
        button_text : string
            Optional. By default the window with the prompt will have a button labelled 'Cancel'
            which if pressed will cancel the pick and return None. If you want to change the
            text on the button use this argument. If omitted 'Cancel' will be used

        Returns
        -------
        Linear
            Linear object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def RenumberAll(model, start):
        """
        Renumbers all of the constrained linears in the model

        Parameters
        ----------
        model : Model
            Model that all constrained linears will be renumbered in
        start : integer
            Start point for renumbering

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "RenumberAll", model, start)

    def RenumberFlagged(model, flag, start):
        """
        Renumbers all of the flagged constrained linears in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged constrained linears will be renumbered in
        flag : Flag
            Flag set on the constrained linears that you want to renumber
        start : integer
            Start point for renumbering

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "RenumberFlagged", model, flag, start)

    def Select(flag, prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg):
        """
        Allows the user to select constrained linears using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting constrained linears
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only constrained linears from that model can be selected.
            If the argument is a Flag then only constrained linears that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any constrained linears can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of constrained linears selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged constrained linears in the model. The constrained linears will be sketched until you either call
        Linear.Unsketch(),
        Linear.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged constrained linears will be sketched in
        flag : Flag
            Flag set on the constrained linears that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the constrained linears are sketched.
            If omitted redraw is true. If you want to sketch flagged constrained linears several times and only
            redraw after the last one then use false for redraw and call
            View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "SketchFlagged", model, flag, redraw)

    def Total(model, exists=Oasys.gRPC.defaultArg):
        """
        Returns the total number of constrained linears in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing constrained linears should be counted. If false or omitted
            referenced but undefined constrained linears will also be included in the total

        Returns
        -------
        int
            number of constrained linears
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnblankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the constrained linears in the model

        Parameters
        ----------
        model : Model
            Model that all constrained linears will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not.
            If omitted redraw is false. If you want to do several (un)blanks and only
            redraw after the last one then use false for all redraws apart from the last one.
            Alternatively you can redraw using View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnblankAll", model, redraw)

    def UnblankFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the flagged constrained linears in the model

        Parameters
        ----------
        model : Model
            Model that the flagged constrained linears will be unblanked in
        flag : Flag
            Flag set on the constrained linears that you want to unblank
        redraw : boolean
            Optional. If model should be redrawn or not.
            If omitted redraw is false. If you want to do several (un)blanks and only
            redraw after the last one then use false for all redraws apart from the last one.
            Alternatively you can redraw using View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnblankFlagged", model, flag, redraw)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the constrained linears in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all constrained linears will be unset in
        flag : Flag
            Flag to unset on the constrained linears

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all constrained linears

        Parameters
        ----------
        model : Model
            Model that all constrained linears will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the constrained linears are unsketched.
            If omitted redraw is true. If you want to unsketch several things and only
            redraw after the last one then use false for redraw and call
            View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnsketchAll", model, redraw)

    def UnsketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all flagged constrained linears in the model

        Parameters
        ----------
        model : Model
            Model that all constrained linears will be unsketched in
        flag : Flag
            Flag set on the constrained linears that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the constrained linears are unsketched.
            If omitted redraw is true. If you want to unsketch several things and only
            redraw after the last one then use false for redraw and call
            View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnsketchFlagged", model, flag, redraw)



# Instance methods
    def AddRowData(self, nid, dof, coeff, cid=Oasys.gRPC.defaultArg):
        """
        Used to add additional independent card 2 to the keyword. Adds this data to the end of the selected \*CONSTRAINED_LINEAR

        Parameters
        ----------
        nid : integer
            Node id
        dof : integer
            Degrees-of-Freedom
        coeff : float
            Non-zero coefficient
        cid : integer
            Optional. Coordinate System ID if format is Linear.LOCAL. The default value is 0

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AddRowData", nid, dof, coeff, cid)

    def AssociateComment(self, comment):
        """
        Associates a comment with a constrained linear

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the constrained linear

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def Blank(self):
        """
        Blanks the constrained linear

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank")

    def Blanked(self):
        """
        Checks if the constrained linear is blanked or not

        Returns
        -------
        bool
            True if blanked, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blanked")

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
        Clears a flag on the constrained linear

        Parameters
        ----------
        flag : Flag
            Flag to clear on the constrained linear

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the constrained linear. The target include of the copied constrained linear can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        Linear
            Linear object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a constrained linear

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the constrained linear

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "DetachComment", comment)

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
        Checks if the constrained linear is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the constrained linear

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a constrained linear

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a Linear property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the Linear.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            constrained linear property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def GetRowData(self, row_index):
        """
        Returns independent card 2 for the selected row of the \*CONSTRAINED_LINEAR

        Parameters
        ----------
        row_index : Integer
            The row index of the data to return. Note that indices start at 0, not 1.
            0 <= row_index < Linear.total

        Returns
        -------
        list
            List containing data
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetRowData", row_index)

    def Keyword(self):
        """
        Returns the keyword for this Linear (\*constrained_linear).
        Note that a carriage return is not added.
        See also Linear.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the Linear.
        Note that a carriage return is not added.
        See also Linear.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next constrained linear in the model

        Returns
        -------
        Linear
            Linear object (or None if there are no more constrained linears in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous constrained linear in the model

        Returns
        -------
        Linear
            Linear object (or None if there are no more constrained linears in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def RemoveRowData(self, row_index):
        """
        Removes an independent card 2 for the selected row on the \*CONSTRAINED_LINEAR

        Parameters
        ----------
        row_index : Integer
            The row index of the data to return. Note that indices start at 0, not 1.
            0 <= row_index < Linear.total

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "RemoveRowData", row_index)

    def SetFlag(self, flag):
        """
        Sets a flag on the constrained linear

        Parameters
        ----------
        flag : Flag
            Flag to set on the constrained linear

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def SetRowData(self, row_index, nid, dof, coeff, cid=Oasys.gRPC.defaultArg):
        """
        Used to reset values in already existing card 2 in the selected row of \*CONSTRAINED_LINEAR

        Parameters
        ----------
        row_index : Integer
            The row index of the data to return. Note that indices start at 0, not 1.
            0 <= row_index < Linear.total
        nid : integer
            Node id
        dof : integer
            Degrees-of-Freedom
        coeff : float
            Non-zero coefficient
        cid : integer
            Optional. Coordinate System ID if format is Linear.LOCAL. The default value is 0

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetRowData", row_index, nid, dof, coeff, cid)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the constrained linear. The constrained linear will be sketched until you either call
        Linear.Unsketch(),
        Linear.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the constrained linear is sketched.
            If omitted redraw is true. If you want to sketch several constrained linears and only
            redraw after the last one then use false for redraw and call
            View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Sketch", redraw)

    def Unblank(self):
        """
        Unblanks the constrained linear

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank")

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the constrained linear

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the constrained linear is unsketched.
            If omitted redraw is true. If you want to unsketch several constrained linears and only
            redraw after the last one then use false for redraw and call
            View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unsketch", redraw)

    def ViewParameters(self):
        """
        Object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. This function temporarily
        changes the behaviour so that if a property is a parameter the parameter name is returned instead.
        This can be used with 'method chaining' (see the example below) to make sure a property argument is correct

        Returns
        -------
        Linear
            Linear object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this constrained linear

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

