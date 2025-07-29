import Oasys.gRPC


# Metaclass for static properties and constants
class GeometrySurfaceType(type):

    def __getattr__(cls, name):

        raise AttributeError("GeometrySurface class attribute '{}' does not exist".format(name))


class GeometrySurface(Oasys.gRPC.OasysItem, metaclass=GeometrySurfaceType):
    _props = {'include'}
    _rprops = {'exists', 'id', 'label', 'model'}


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
        if name in GeometrySurface._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in GeometrySurface._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("GeometrySurface instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in GeometrySurface._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in GeometrySurface._rprops:
            raise AttributeError("Cannot set read-only GeometrySurface instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Static methods
    def BlankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the surfaces in the model

        Parameters
        ----------
        model : Model
            Model that all surfaces will be blanked in
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
        Blanks all of the flagged surfaces in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged surfaces will be blanked in
        flag : Flag
            Flag set on the surfaces that you want to blank
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

    def First(model):
        """
        Returns the first surface in the model

        Parameters
        ----------
        model : Model
            Model to get first surface in

        Returns
        -------
        GeometrySurface
            GeometrySurface object (or None if there are no surfaces in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FirstFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the first free surface label in the model.
        Also see GeometrySurface.LastFreeLabel(),
        GeometrySurface.NextFreeLabel() and
        Model.FirstFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get first free surface label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            First free in layer in editing panels). If omitted the whole model will be used (Equivalent to
            First free in editing panels)

        Returns
        -------
        int
            GeometrySurface label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FirstFreeLabel", model, layer)

    def FlagAll(model, flag):
        """
        Flags all of the surfaces in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all surfaces will be flagged in
        flag : Flag
            Flag to set on the surfaces

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of GeometrySurface objects or properties for all of the surfaces in a model in PRIMER.
        If the optional property argument is not given then a list of GeometrySurface objects is returned.
        If the property argument is given, that property value for each surface is returned in the list
        instead of a GeometrySurface object

        Parameters
        ----------
        model : Model
            Model to get surfaces from
        property : string
            Optional. Name for property to get for all surfaces in the model

        Returns
        -------
        list
            List of GeometrySurface objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of GeometrySurface objects for all of the flagged surfaces in a model in PRIMER
        If the optional property argument is not given then a list of GeometrySurface objects is returned.
        If the property argument is given, then that property value for each surface is returned in the list
        instead of a GeometrySurface object

        Parameters
        ----------
        model : Model
            Model to get surfaces from
        flag : Flag
            Flag set on the surfaces that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged surfaces in the model

        Returns
        -------
        list
            List of GeometrySurface objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the GeometrySurface object for a surface ID

        Parameters
        ----------
        model : Model
            Model to find the surface in
        number : integer
            number of the surface you want the GeometrySurface object for

        Returns
        -------
        GeometrySurface
            GeometrySurface object (or None if surface does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last surface in the model

        Parameters
        ----------
        model : Model
            Model to get last surface in

        Returns
        -------
        GeometrySurface
            GeometrySurface object (or None if there are no surfaces in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def LastFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the last free surface label in the model.
        Also see GeometrySurface.FirstFreeLabel(),
        GeometrySurface.NextFreeLabel() and
        see Model.LastFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get last free surface label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest free in layer in editing panels). If omitted the whole model will be used

        Returns
        -------
        int
            GeometrySurface label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "LastFreeLabel", model, layer)

    def NextFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the next free (highest+1) surface label in the model.
        Also see GeometrySurface.FirstFreeLabel(),
        GeometrySurface.LastFreeLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get next free surface label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest+1 in layer in editing panels). If omitted the whole model will be used (Equivalent to
            Highest+1 in editing panels)

        Returns
        -------
        int
            GeometrySurface label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NextFreeLabel", model, layer)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a surface

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only surfaces from that model can be picked.
            If the argument is a Flag then only surfaces that
            are flagged with limit can be selected.
            If omitted, or None, any surfaces from any model can be selected.
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
        GeometrySurface
            GeometrySurface object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def RenumberAll(model, start):
        """
        Renumbers all of the surfaces in the model

        Parameters
        ----------
        model : Model
            Model that all surfaces will be renumbered in
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
        Renumbers all of the flagged surfaces in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged surfaces will be renumbered in
        flag : Flag
            Flag set on the surfaces that you want to renumber
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
        Allows the user to select surfaces using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting surfaces
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only surfaces from that model can be selected.
            If the argument is a Flag then only surfaces that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any surfaces can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of surfaces selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged surfaces in the model. The surfaces will be sketched until you either call
        GeometrySurface.Unsketch(),
        GeometrySurface.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged surfaces will be sketched in
        flag : Flag
            Flag set on the surfaces that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the surfaces are sketched.
            If omitted redraw is true. If you want to sketch flagged surfaces several times and only
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
        Returns the total number of surfaces in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing surfaces should be counted. If false or omitted
            referenced but undefined surfaces will also be included in the total

        Returns
        -------
        int
            number of surfaces
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnblankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the surfaces in the model

        Parameters
        ----------
        model : Model
            Model that all surfaces will be unblanked in
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
        Unblanks all of the flagged surfaces in the model

        Parameters
        ----------
        model : Model
            Model that the flagged surfaces will be unblanked in
        flag : Flag
            Flag set on the surfaces that you want to unblank
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
        Unsets a defined flag on all of the surfaces in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all surfaces will be unset in
        flag : Flag
            Flag to unset on the surfaces

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all surfaces

        Parameters
        ----------
        model : Model
            Model that all surfaces will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the surfaces are unsketched.
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
        Unsketches all flagged surfaces in the model

        Parameters
        ----------
        model : Model
            Model that all surfaces will be unsketched in
        flag : Flag
            Flag set on the surfaces that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the surfaces are unsketched.
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
        Associates a comment with a surface

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the surface

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def Blank(self):
        """
        Blanks the surface

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank")

    def Blanked(self):
        """
        Checks if the surface is blanked or not

        Returns
        -------
        bool
            True if blanked, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blanked")

    def CalculateNormal(self, u, y):
        """
        Calculate the normal vector for a parametric point on a surface

        Parameters
        ----------
        u : real
            u parametric coordinate
        y : real
            v parametric coordinate

        Returns
        -------
        list
            List containing x, y and z values
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "CalculateNormal", u, y)

    def CalculatePoint(self, u, v):
        """
        Calculate the X, Y and Z coordinates for a parametric point on a surface

        Parameters
        ----------
        u : real
            u parametric coordinate
        v : real
            v parametric coordinate

        Returns
        -------
        list
            List containing x, y and z values
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "CalculatePoint", u, v)

    def ClearFlag(self, flag):
        """
        Clears a flag on the surface

        Parameters
        ----------
        flag : Flag
            Flag to clear on the surface

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the surface. The target include of the copied surface can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        GeometrySurface
            GeometrySurface object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a surface

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the surface

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "DetachComment", comment)

    def Flagged(self, flag):
        """
        Checks if the surface is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the surface

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a surface

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetEdgeIndices(self):
        """
        Return a list of all the edge indices for a surface (in pairs)

        Returns
        -------
        list
            List of indices
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetEdgeIndices")

    def GetParameter(self, prop):
        """
        Checks if a GeometrySurface property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the GeometrySurface.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            surface property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def GetTriaIndices(self):
        """
        Return a list of all the tria indices for a surface (in triplets)

        Returns
        -------
        list
            List of indices
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetTriaIndices")

    def GetVertices(self):
        """
        Return a list of all the vertex coordinates for a surface (in triplets)

        Returns
        -------
        list
            List of indices
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetVertices")

    def Next(self):
        """
        Returns the next surface in the model

        Returns
        -------
        GeometrySurface
            GeometrySurface object (or None if there are no more surfaces in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous surface in the model

        Returns
        -------
        GeometrySurface
            GeometrySurface object (or None if there are no more surfaces in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def ProjectPoint(self, x, y, z):
        """
        Project a point onto the surface

        Parameters
        ----------
        x : real
            X coordinate of point to project
        y : real
            Y coordinate of point to project
        z : real
            Z coordinate of point to project

        Returns
        -------
        list
            List containing u and v values
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ProjectPoint", x, y, z)

    def SetFlag(self, flag):
        """
        Sets a flag on the surface

        Parameters
        ----------
        flag : Flag
            Flag to set on the surface

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the surface. The surface will be sketched until you either call
        GeometrySurface.Unsketch(),
        GeometrySurface.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the surface is sketched.
            If omitted redraw is true. If you want to sketch several surfaces and only
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
        Unblanks the surface

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank")

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the surface

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the surface is unsketched.
            If omitted redraw is true. If you want to unsketch several surfaces and only
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
        GeometrySurface
            GeometrySurface object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this surface

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

