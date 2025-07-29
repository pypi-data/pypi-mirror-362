import Oasys.gRPC


# Metaclass for static properties and constants
class PrescribedFinalGeometryType(type):

    def __getattr__(cls, name):

        raise AttributeError("PrescribedFinalGeometry class attribute '{}' does not exist".format(name))


class PrescribedFinalGeometry(Oasys.gRPC.OasysItem, metaclass=PrescribedFinalGeometryType):
    _props = {'bpfgid', 'deathd', 'id', 'include', 'label', 'lcidf'}
    _rprops = {'exists', 'lines', 'model'}


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
        if name in PrescribedFinalGeometry._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in PrescribedFinalGeometry._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("PrescribedFinalGeometry instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in PrescribedFinalGeometry._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in PrescribedFinalGeometry._rprops:
            raise AttributeError("Cannot set read-only PrescribedFinalGeometry instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, bpfgid):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, bpfgid)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new PrescribedFinalGeometry object

        Parameters
        ----------
        model : Model
            Model that PrescribedFinalGeometry will be created in
        bpfgid : PrescribedFinalGeometry
            PrescribedFinalGeometry number

        Returns
        -------
        PrescribedFinalGeometry
            PrescribedFinalGeometry object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def BlankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the boundary prescribed final geometrys in the model

        Parameters
        ----------
        model : Model
            Model that all boundary prescribed final geometrys will be blanked in
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
        Blanks all of the flagged boundary prescribed final geometrys in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged boundary prescribed final geometrys will be blanked in
        flag : Flag
            Flag set on the boundary prescribed final geometrys that you want to blank
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
        Starts an interactive editing panel to create a boundary prescribed final geometry

        Parameters
        ----------
        model : Model
            Model that the boundary prescribed final geometry will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        PrescribedFinalGeometry
            PrescribedFinalGeometry object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def First(model):
        """
        Returns the first boundary prescribed final geometry in the model

        Parameters
        ----------
        model : Model
            Model to get first boundary prescribed final geometry in

        Returns
        -------
        PrescribedFinalGeometry
            PrescribedFinalGeometry object (or None if there are no boundary prescribed final geometrys in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FirstFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the first free boundary prescribed final geometry label in the model.
        Also see PrescribedFinalGeometry.LastFreeLabel(),
        PrescribedFinalGeometry.NextFreeLabel() and
        Model.FirstFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get first free boundary prescribed final geometry label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            First free in layer in editing panels). If omitted the whole model will be used (Equivalent to
            First free in editing panels)

        Returns
        -------
        int
            PrescribedFinalGeometry label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FirstFreeLabel", model, layer)

    def FlagAll(model, flag):
        """
        Flags all of the boundary prescribed final geometrys in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all boundary prescribed final geometrys will be flagged in
        flag : Flag
            Flag to set on the boundary prescribed final geometrys

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of PrescribedFinalGeometry objects or properties for all of the boundary prescribed final geometrys in a model in PRIMER.
        If the optional property argument is not given then a list of PrescribedFinalGeometry objects is returned.
        If the property argument is given, that property value for each boundary prescribed final geometry is returned in the list
        instead of a PrescribedFinalGeometry object

        Parameters
        ----------
        model : Model
            Model to get boundary prescribed final geometrys from
        property : string
            Optional. Name for property to get for all boundary prescribed final geometrys in the model

        Returns
        -------
        list
            List of PrescribedFinalGeometry objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of PrescribedFinalGeometry objects for all of the flagged boundary prescribed final geometrys in a model in PRIMER
        If the optional property argument is not given then a list of PrescribedFinalGeometry objects is returned.
        If the property argument is given, then that property value for each boundary prescribed final geometry is returned in the list
        instead of a PrescribedFinalGeometry object

        Parameters
        ----------
        model : Model
            Model to get boundary prescribed final geometrys from
        flag : Flag
            Flag set on the boundary prescribed final geometrys that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged boundary prescribed final geometrys in the model

        Returns
        -------
        list
            List of PrescribedFinalGeometry objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the PrescribedFinalGeometry object for a boundary prescribed final geometry ID

        Parameters
        ----------
        model : Model
            Model to find the boundary prescribed final geometry in
        number : integer
            number of the boundary prescribed final geometry you want the PrescribedFinalGeometry object for

        Returns
        -------
        PrescribedFinalGeometry
            PrescribedFinalGeometry object (or None if boundary prescribed final geometry does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last boundary prescribed final geometry in the model

        Parameters
        ----------
        model : Model
            Model to get last boundary prescribed final geometry in

        Returns
        -------
        PrescribedFinalGeometry
            PrescribedFinalGeometry object (or None if there are no boundary prescribed final geometrys in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def LastFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the last free boundary prescribed final geometry label in the model.
        Also see PrescribedFinalGeometry.FirstFreeLabel(),
        PrescribedFinalGeometry.NextFreeLabel() and
        see Model.LastFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get last free boundary prescribed final geometry label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest free in layer in editing panels). If omitted the whole model will be used

        Returns
        -------
        int
            PrescribedFinalGeometry label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "LastFreeLabel", model, layer)

    def NextFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the next free (highest+1) boundary prescribed final geometry label in the model.
        Also see PrescribedFinalGeometry.FirstFreeLabel(),
        PrescribedFinalGeometry.LastFreeLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get next free boundary prescribed final geometry label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest+1 in layer in editing panels). If omitted the whole model will be used (Equivalent to
            Highest+1 in editing panels)

        Returns
        -------
        int
            PrescribedFinalGeometry label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NextFreeLabel", model, layer)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a boundary prescribed final geometry

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only boundary prescribed final geometrys from that model can be picked.
            If the argument is a Flag then only boundary prescribed final geometrys that
            are flagged with limit can be selected.
            If omitted, or None, any boundary prescribed final geometrys from any model can be selected.
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
        PrescribedFinalGeometry
            PrescribedFinalGeometry object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def RenumberAll(model, start):
        """
        Renumbers all of the boundary prescribed final geometrys in the model

        Parameters
        ----------
        model : Model
            Model that all boundary prescribed final geometrys will be renumbered in
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
        Renumbers all of the flagged boundary prescribed final geometrys in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged boundary prescribed final geometrys will be renumbered in
        flag : Flag
            Flag set on the boundary prescribed final geometrys that you want to renumber
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
        Allows the user to select boundary prescribed final geometrys using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting boundary prescribed final geometrys
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only boundary prescribed final geometrys from that model can be selected.
            If the argument is a Flag then only boundary prescribed final geometrys that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any boundary prescribed final geometrys can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of boundary prescribed final geometrys selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged boundary prescribed final geometrys in the model. The boundary prescribed final geometrys will be sketched until you either call
        PrescribedFinalGeometry.Unsketch(),
        PrescribedFinalGeometry.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged boundary prescribed final geometrys will be sketched in
        flag : Flag
            Flag set on the boundary prescribed final geometrys that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the boundary prescribed final geometrys are sketched.
            If omitted redraw is true. If you want to sketch flagged boundary prescribed final geometrys several times and only
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
        Returns the total number of boundary prescribed final geometrys in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing boundary prescribed final geometrys should be counted. If false or omitted
            referenced but undefined boundary prescribed final geometrys will also be included in the total

        Returns
        -------
        int
            number of boundary prescribed final geometrys
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnblankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the boundary prescribed final geometrys in the model

        Parameters
        ----------
        model : Model
            Model that all boundary prescribed final geometrys will be unblanked in
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
        Unblanks all of the flagged boundary prescribed final geometrys in the model

        Parameters
        ----------
        model : Model
            Model that the flagged boundary prescribed final geometrys will be unblanked in
        flag : Flag
            Flag set on the boundary prescribed final geometrys that you want to unblank
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
        Unsets a defined flag on all of the boundary prescribed final geometrys in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all boundary prescribed final geometrys will be unset in
        flag : Flag
            Flag to unset on the boundary prescribed final geometrys

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all boundary prescribed final geometrys

        Parameters
        ----------
        model : Model
            Model that all boundary prescribed final geometrys will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the boundary prescribed final geometrys are unsketched.
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
        Unsketches all flagged boundary prescribed final geometrys in the model

        Parameters
        ----------
        model : Model
            Model that all boundary prescribed final geometrys will be unsketched in
        flag : Flag
            Flag set on the boundary prescribed final geometrys that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the boundary prescribed final geometrys are unsketched.
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
    def AssociateComment(self, comment):
        """
        Associates a comment with a boundary prescribed final geometry

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the boundary prescribed final geometry

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def Blank(self):
        """
        Blanks the boundary prescribed final geometry

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank")

    def Blanked(self):
        """
        Checks if the boundary prescribed final geometry is blanked or not

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
        Clears a flag on the boundary prescribed final geometry

        Parameters
        ----------
        flag : Flag
            Flag to clear on the boundary prescribed final geometry

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the boundary prescribed final geometry. The target include of the copied boundary prescribed final geometry can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        PrescribedFinalGeometry
            PrescribedFinalGeometry object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a boundary prescribed final geometry

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the boundary prescribed final geometry

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
        Checks if the boundary prescribed final geometry is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the boundary prescribed final geometry

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a boundary prescribed final geometry

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetData(self, index):
        """
        Returns data for open-ended cards for a given row number in \*BOUNDARY_PRESCRIBED_FINAL_GEOMETRY

        Parameters
        ----------
        index : integer
            Index of open-ended card you want the data for. Note that indices start at 0, not 1.
            0 <= index < lines

        Returns
        -------
        list
            A list containing data (NID, X, Y, Z, LCID, DEATH)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetData", index)

    def GetParameter(self, prop):
        """
        Checks if a PrescribedFinalGeometry property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the PrescribedFinalGeometry.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            boundary prescribed final geometry property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this PrescribedFinalGeometry (\*BOUNDARY_PRESCRIBED_FINAL_GEOMETRY).
        Note that a carriage return is not added.
        See also PrescribedFinalGeometry.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the PrescribedFinalGeometry.
        Note that a carriage return is not added.
        See also PrescribedFinalGeometry.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next boundary prescribed final geometry in the model

        Returns
        -------
        PrescribedFinalGeometry
            PrescribedFinalGeometry object (or None if there are no more boundary prescribed final geometrys in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous boundary prescribed final geometry in the model

        Returns
        -------
        PrescribedFinalGeometry
            PrescribedFinalGeometry object (or None if there are no more boundary prescribed final geometrys in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def RemoveData(self, index):
        """
        Removes a line of data for a \*BOUNDARY_PRESCRIBED_FINAL_GEOMETRY

        Parameters
        ----------
        index : Integer
            The index of the \*BOUNDARY_PRESCRIBED_FINAL_GEOMETRY data to remove. Note that indices start at 0, not 1.
            0 <= index < lines

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "RemoveData", index)

    def SetData(self, index, nid, x, y, z, lcid=Oasys.gRPC.defaultArg, death=Oasys.gRPC.defaultArg):
        """
        Sets a line of data for a \*BOUNDARY_PRESCRIBED_FINAL_GEOMETRY

        Parameters
        ----------
        index : Integer
            The index of the \*BOUNDARY_PRESCRIBED_FINAL_GEOMETRY data to set. Note that indices start at 0, not 1.
            0 <= index <= lines
        nid : integer
            Node or negative node set number
        x : float
            X coordinates of final geometry
        y : float
            Y coordinates of final geometry
        z : float
            Z coordinates of final geometry
        lcid : integer
            Optional. Loadcurve number
        death : float
            Optional. Death time

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetData", index, nid, x, y, z, lcid, death)

    def SetFlag(self, flag):
        """
        Sets a flag on the boundary prescribed final geometry

        Parameters
        ----------
        flag : Flag
            Flag to set on the boundary prescribed final geometry

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the boundary prescribed final geometry. The boundary prescribed final geometry will be sketched until you either call
        PrescribedFinalGeometry.Unsketch(),
        PrescribedFinalGeometry.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the boundary prescribed final geometry is sketched.
            If omitted redraw is true. If you want to sketch several boundary prescribed final geometrys and only
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
        Unblanks the boundary prescribed final geometry

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank")

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the boundary prescribed final geometry

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the boundary prescribed final geometry is unsketched.
            If omitted redraw is true. If you want to unsketch several boundary prescribed final geometrys and only
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
        PrescribedFinalGeometry
            PrescribedFinalGeometry object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this boundary prescribed final geometry

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

