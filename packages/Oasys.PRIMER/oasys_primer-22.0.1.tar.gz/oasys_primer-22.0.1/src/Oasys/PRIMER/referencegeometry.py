import Oasys.gRPC


# Metaclass for static properties and constants
class ReferenceGeometryType(type):

    def __getattr__(cls, name):

        raise AttributeError("ReferenceGeometry class attribute '{}' does not exist".format(name))


class ReferenceGeometry(Oasys.gRPC.OasysItem, metaclass=ReferenceGeometryType):
    _props = {'aid', 'birth', 'birth_time', 'id', 'include', 'iout', 'label', 'nido', 'rdt', 'sx', 'sy', 'sz'}
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
        if name in ReferenceGeometry._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in ReferenceGeometry._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("ReferenceGeometry instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in ReferenceGeometry._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in ReferenceGeometry._rprops:
            raise AttributeError("Cannot set read-only ReferenceGeometry instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, aid=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, aid)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new ReferenceGeometry object

        Parameters
        ----------
        model : Model
            Model that ReferenceGeometry will be created in
        aid : integer
            Optional. ReferenceGeometry number to set _ID suffix

        Returns
        -------
        ReferenceGeometry
            ReferenceGeometry object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def Create(model, modal=Oasys.gRPC.defaultArg):
        """
        Starts an interactive editing panel to create a airbag reference geometry

        Parameters
        ----------
        model : Model
            Model that the airbag reference geometry will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        ReferenceGeometry
            ReferenceGeometry object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def First(model):
        """
        Returns the first airbag reference geometry in the model

        Parameters
        ----------
        model : Model
            Model to get first airbag reference geometry in

        Returns
        -------
        ReferenceGeometry
            ReferenceGeometry object (or None if there are no airbag reference geometrys in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FirstFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the first free airbag reference geometry label in the model.
        Also see ReferenceGeometry.LastFreeLabel(),
        ReferenceGeometry.NextFreeLabel() and
        Model.FirstFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get first free airbag reference geometry label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            First free in layer in editing panels). If omitted the whole model will be used (Equivalent to
            First free in editing panels)

        Returns
        -------
        int
            ReferenceGeometry label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FirstFreeLabel", model, layer)

    def FlagAll(model, flag):
        """
        Flags all of the airbag reference geometrys in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all airbag reference geometrys will be flagged in
        flag : Flag
            Flag to set on the airbag reference geometrys

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of ReferenceGeometry objects or properties for all of the airbag reference geometrys in a model in PRIMER.
        If the optional property argument is not given then a list of ReferenceGeometry objects is returned.
        If the property argument is given, that property value for each airbag reference geometry is returned in the list
        instead of a ReferenceGeometry object

        Parameters
        ----------
        model : Model
            Model to get airbag reference geometrys from
        property : string
            Optional. Name for property to get for all airbag reference geometrys in the model

        Returns
        -------
        list
            List of ReferenceGeometry objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of ReferenceGeometry objects for all of the flagged airbag reference geometrys in a model in PRIMER
        If the optional property argument is not given then a list of ReferenceGeometry objects is returned.
        If the property argument is given, then that property value for each airbag reference geometry is returned in the list
        instead of a ReferenceGeometry object

        Parameters
        ----------
        model : Model
            Model to get airbag reference geometrys from
        flag : Flag
            Flag set on the airbag reference geometrys that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged airbag reference geometrys in the model

        Returns
        -------
        list
            List of ReferenceGeometry objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the ReferenceGeometry object for a airbag reference geometry ID

        Parameters
        ----------
        model : Model
            Model to find the airbag reference geometry in
        number : integer
            number of the airbag reference geometry you want the ReferenceGeometry object for

        Returns
        -------
        ReferenceGeometry
            ReferenceGeometry object (or None if airbag reference geometry does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last airbag reference geometry in the model

        Parameters
        ----------
        model : Model
            Model to get last airbag reference geometry in

        Returns
        -------
        ReferenceGeometry
            ReferenceGeometry object (or None if there are no airbag reference geometrys in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def LastFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the last free airbag reference geometry label in the model.
        Also see ReferenceGeometry.FirstFreeLabel(),
        ReferenceGeometry.NextFreeLabel() and
        see Model.LastFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get last free airbag reference geometry label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest free in layer in editing panels). If omitted the whole model will be used

        Returns
        -------
        int
            ReferenceGeometry label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "LastFreeLabel", model, layer)

    def NextFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the next free (highest+1) airbag reference geometry label in the model.
        Also see ReferenceGeometry.FirstFreeLabel(),
        ReferenceGeometry.LastFreeLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get next free airbag reference geometry label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest+1 in layer in editing panels). If omitted the whole model will be used (Equivalent to
            Highest+1 in editing panels)

        Returns
        -------
        int
            ReferenceGeometry label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NextFreeLabel", model, layer)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a airbag reference geometry

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only airbag reference geometrys from that model can be picked.
            If the argument is a Flag then only airbag reference geometrys that
            are flagged with limit can be selected.
            If omitted, or None, any airbag reference geometrys from any model can be selected.
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
        ReferenceGeometry
            ReferenceGeometry object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def RenumberAll(model, start):
        """
        Renumbers all of the airbag reference geometrys in the model

        Parameters
        ----------
        model : Model
            Model that all airbag reference geometrys will be renumbered in
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
        Renumbers all of the flagged airbag reference geometrys in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged airbag reference geometrys will be renumbered in
        flag : Flag
            Flag set on the airbag reference geometrys that you want to renumber
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
        Allows the user to select airbag reference geometrys using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting airbag reference geometrys
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only airbag reference geometrys from that model can be selected.
            If the argument is a Flag then only airbag reference geometrys that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any airbag reference geometrys can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of airbag reference geometrys selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged airbag reference geometrys in the model. The airbag reference geometrys will be sketched until you either call
        ReferenceGeometry.Unsketch(),
        ReferenceGeometry.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged airbag reference geometrys will be sketched in
        flag : Flag
            Flag set on the airbag reference geometrys that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the airbag reference geometrys are sketched.
            If omitted redraw is true. If you want to sketch flagged airbag reference geometrys several times and only
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
        Returns the total number of airbag reference geometrys in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing airbag reference geometrys should be counted. If false or omitted
            referenced but undefined airbag reference geometrys will also be included in the total

        Returns
        -------
        int
            number of airbag reference geometrys
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the airbag reference geometrys in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all airbag reference geometrys will be unset in
        flag : Flag
            Flag to unset on the airbag reference geometrys

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all airbag reference geometrys

        Parameters
        ----------
        model : Model
            Model that all airbag reference geometrys will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the airbag reference geometrys are unsketched.
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
        Unsketches all flagged airbag reference geometrys in the model

        Parameters
        ----------
        model : Model
            Model that all airbag reference geometrys will be unsketched in
        flag : Flag
            Flag set on the airbag reference geometrys that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the airbag reference geometrys are unsketched.
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
        Associates a comment with a airbag reference geometry

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the airbag reference geometry

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

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
        Clears a flag on the airbag reference geometry

        Parameters
        ----------
        flag : Flag
            Flag to clear on the airbag reference geometry

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the airbag reference geometry. The target include of the copied airbag reference geometry can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        ReferenceGeometry
            ReferenceGeometry object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a airbag reference geometry

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the airbag reference geometry

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
        Checks if the airbag reference geometry is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the airbag reference geometry

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a airbag reference geometry

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetNode(self, nid):
        """
        Returns the reference geometry coordinates for the node

        Parameters
        ----------
        nid : integer
            Node ID

        Returns
        -------
        list
            A list containing the three reference coordinates (or None if the node is not on the reference geometry)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetNode", nid)

    def GetParameter(self, prop):
        """
        Checks if a ReferenceGeometry property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the ReferenceGeometry.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            airbag reference geometry property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this reference_geometry (\*AIRBAG_REFERENCE_GEOMETRY).
        Note that a carriage return is not added.
        See also ReferenceGeometry.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the reference_geometry.
        Note that a carriage return is not added.
        See also ReferenceGeometry.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next airbag reference geometry in the model

        Returns
        -------
        ReferenceGeometry
            ReferenceGeometry object (or None if there are no more airbag reference geometrys in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous airbag reference geometry in the model

        Returns
        -------
        ReferenceGeometry
            ReferenceGeometry object (or None if there are no more airbag reference geometrys in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def RemoveNode(self, nid):
        """
        Removes a node from the reference geometry if it is on it

        Parameters
        ----------
        nid : integer
            Node ID

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "RemoveNode", nid)

    def SetFlag(self, flag):
        """
        Sets a flag on the airbag reference geometry

        Parameters
        ----------
        flag : Flag
            Flag to set on the airbag reference geometry

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def SetNode(self, nid, x, y, z):
        """
        Adds a node to the reference geometry if not already there,
        otherwise just changes the coordinates

        Parameters
        ----------
        nid : integer
            Node ID
        x : real
            X reference coordinate
        y : real
            Y reference coordinate
        z : real
            Z reference coordinate

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetNode", nid, x, y, z)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the airbag reference geometry. The airbag reference geometry will be sketched until you either call
        ReferenceGeometry.Unsketch(),
        ReferenceGeometry.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the airbag reference geometry is sketched.
            If omitted redraw is true. If you want to sketch several airbag reference geometrys and only
            redraw after the last one then use false for redraw and call
            View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Sketch", redraw)

    def Spool(self):
        """
        Spools a reference geometry, entry by entry. See also ReferenceGeometry.StartSpool

        Returns
        -------
        list
            A list containing the node ID and the three coordinates. Returns 0 if no more items
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Spool")

    def StartSpool(self):
        """
        Starts a reference geometry spooling operation. See also ReferenceGeometry.Spool

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "StartSpool")

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the airbag reference geometry

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the airbag reference geometry is unsketched.
            If omitted redraw is true. If you want to unsketch several airbag reference geometrys and only
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
        ReferenceGeometry
            ReferenceGeometry object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this airbag reference geometry

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

