import Oasys.gRPC


# Metaclass for static properties and constants
class CoordinateSystemType(type):
    _consts = {'NODES', 'SYSTEM', 'VECTOR'}

    def __getattr__(cls, name):
        if name in CoordinateSystemType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("CoordinateSystem class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in CoordinateSystemType._consts:
            raise AttributeError("Cannot set CoordinateSystem class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class CoordinateSystem(Oasys.gRPC.OasysItem, metaclass=CoordinateSystemType):
    _props = {'cid', 'cidl', 'dir', 'flag', 'heading', 'include', 'label', 'lx', 'ly', 'lz', 'n1', 'n2', 'n3', 'nid', 'option', 'ox', 'oy', 'oz', 'px', 'py', 'pz', 'vx', 'vy', 'vz', 'xx', 'xy', 'xz'}
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
        if name in CoordinateSystem._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in CoordinateSystem._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("CoordinateSystem instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in CoordinateSystem._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in CoordinateSystem._rprops:
            raise AttributeError("Cannot set read-only CoordinateSystem instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, details):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, details)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new CoordinateSystem object for \*DEFINE_COORDINATE_NODES

        Parameters
        ----------
        model : Model
            Model that csys will be created in
        details : dict
            Details for creating the CoordinateSystem

        Returns
        -------
        CoordinateSystem
            CoordinateSystem object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def BlankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the coordinate systems in the model

        Parameters
        ----------
        model : Model
            Model that all coordinate systems will be blanked in
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
        Blanks all of the flagged coordinate systems in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged coordinate systems will be blanked in
        flag : Flag
            Flag set on the coordinate systems that you want to blank
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
        Starts an interactive editing panel to create a coordinate system

        Parameters
        ----------
        model : Model
            Model that the coordinate system will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        CoordinateSystem
            CoordinateSystem object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def First(model):
        """
        Returns the first coordinate system in the model

        Parameters
        ----------
        model : Model
            Model to get first coordinate system in

        Returns
        -------
        CoordinateSystem
            CoordinateSystem object (or None if there are no coordinate systems in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FirstFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the first free coordinate system label in the model.
        Also see CoordinateSystem.LastFreeLabel(),
        CoordinateSystem.NextFreeLabel() and
        Model.FirstFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get first free coordinate system label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            First free in layer in editing panels). If omitted the whole model will be used (Equivalent to
            First free in editing panels)

        Returns
        -------
        int
            CoordinateSystem label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FirstFreeLabel", model, layer)

    def FlagAll(model, flag):
        """
        Flags all of the coordinate systems in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all coordinate systems will be flagged in
        flag : Flag
            Flag to set on the coordinate systems

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of CoordinateSystem objects or properties for all of the coordinate systems in a model in PRIMER.
        If the optional property argument is not given then a list of CoordinateSystem objects is returned.
        If the property argument is given, that property value for each coordinate system is returned in the list
        instead of a CoordinateSystem object

        Parameters
        ----------
        model : Model
            Model to get coordinate systems from
        property : string
            Optional. Name for property to get for all coordinate systems in the model

        Returns
        -------
        list
            List of CoordinateSystem objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of CoordinateSystem objects for all of the flagged coordinate systems in a model in PRIMER
        If the optional property argument is not given then a list of CoordinateSystem objects is returned.
        If the property argument is given, then that property value for each coordinate system is returned in the list
        instead of a CoordinateSystem object

        Parameters
        ----------
        model : Model
            Model to get coordinate systems from
        flag : Flag
            Flag set on the coordinate systems that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged coordinate systems in the model

        Returns
        -------
        list
            List of CoordinateSystem objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the CoordinateSystem object for a coordinate system ID

        Parameters
        ----------
        model : Model
            Model to find the coordinate system in
        number : integer
            number of the coordinate system you want the CoordinateSystem object for

        Returns
        -------
        CoordinateSystem
            CoordinateSystem object (or None if coordinate system does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last coordinate system in the model

        Parameters
        ----------
        model : Model
            Model to get last coordinate system in

        Returns
        -------
        CoordinateSystem
            CoordinateSystem object (or None if there are no coordinate systems in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def LastFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the last free coordinate system label in the model.
        Also see CoordinateSystem.FirstFreeLabel(),
        CoordinateSystem.NextFreeLabel() and
        see Model.LastFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get last free coordinate system label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest free in layer in editing panels). If omitted the whole model will be used

        Returns
        -------
        int
            CoordinateSystem label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "LastFreeLabel", model, layer)

    def NextFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the next free (highest+1) coordinate system label in the model.
        Also see CoordinateSystem.FirstFreeLabel(),
        CoordinateSystem.LastFreeLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get next free coordinate system label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest+1 in layer in editing panels). If omitted the whole model will be used (Equivalent to
            Highest+1 in editing panels)

        Returns
        -------
        int
            CoordinateSystem label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NextFreeLabel", model, layer)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a coordinate system

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only coordinate systems from that model can be picked.
            If the argument is a Flag then only coordinate systems that
            are flagged with limit can be selected.
            If omitted, or None, any coordinate systems from any model can be selected.
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
        CoordinateSystem
            CoordinateSystem object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def RenumberAll(model, start):
        """
        Renumbers all of the coordinate systems in the model

        Parameters
        ----------
        model : Model
            Model that all coordinate systems will be renumbered in
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
        Renumbers all of the flagged coordinate systems in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged coordinate systems will be renumbered in
        flag : Flag
            Flag set on the coordinate systems that you want to renumber
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
        Allows the user to select coordinate systems using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting coordinate systems
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only coordinate systems from that model can be selected.
            If the argument is a Flag then only coordinate systems that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any coordinate systems can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        float
            Number of coordinate systems selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged coordinate systems in the model. The coordinate systems will be sketched until you either call
        CoordinateSystem.Unsketch(),
        CoordinateSystem.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged coordinate systems will be sketched in
        flag : Flag
            Flag set on the coordinate systems that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the coordinate systems are sketched.
            If omitted redraw is true. If you want to sketch flagged coordinate systems several times and only
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
        Returns the total number of coordinate systems in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing coordinate systems should be counted. If false or omitted
            referenced but undefined coordinate systems will also be included in the total

        Returns
        -------
        float
            number of coordinate systems
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnblankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the coordinate systems in the model

        Parameters
        ----------
        model : Model
            Model that all coordinate systems will be unblanked in
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
        Unblanks all of the flagged coordinate systems in the model

        Parameters
        ----------
        model : Model
            Model that the flagged coordinate systems will be unblanked in
        flag : Flag
            Flag set on the coordinate systems that you want to unblank
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
        Unsets a defined flag on all of the coordinate systems in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all coordinate systems will be unset in
        flag : Flag
            Flag to unset on the coordinate systems

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all coordinate systems

        Parameters
        ----------
        model : Model
            Model that all coordinate systems will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the coordinate systems are unsketched.
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
        Unsketches all flagged coordinate systems in the model

        Parameters
        ----------
        model : Model
            Model that all coordinate systems will be unsketched in
        flag : Flag
            Flag set on the coordinate systems that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the coordinate systems are unsketched.
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
        Associates a comment with a coordinate system

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the coordinate system

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def Blank(self):
        """
        Blanks the coordinate system

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank")

    def Blanked(self):
        """
        Checks if the coordinate system is blanked or not

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
        Clears a flag on the coordinate system

        Parameters
        ----------
        flag : Flag
            Flag to clear on the coordinate system

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the coordinate system. The target include of the copied coordinate system can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        CoordinateSystem
            CoordinateSystem object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a coordinate system

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the coordinate system

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
        Checks if the coordinate system is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the coordinate system

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a coordinate system

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a CoordinateSystem property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the CoordinateSystem.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            coordinate system property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this csys (\*DEFINE_COORDINATE).
        Note that a carriage return is not added.
        See also CoordinateSystem.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the csys.
        Note that a carriage return is not added.
        See also CoordinateSystem.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next coordinate system in the model

        Returns
        -------
        CoordinateSystem
            CoordinateSystem object (or None if there are no more coordinate systems in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous coordinate system in the model

        Returns
        -------
        CoordinateSystem
            CoordinateSystem object (or None if there are no more coordinate systems in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on the coordinate system

        Parameters
        ----------
        flag : Flag
            Flag to set on the coordinate system

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the coordinate system. The coordinate system will be sketched until you either call
        CoordinateSystem.Unsketch(),
        CoordinateSystem.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the coordinate system is sketched.
            If omitted redraw is true. If you want to sketch several coordinate systems and only
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
        Unblanks the coordinate system

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank")

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the coordinate system

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the coordinate system is unsketched.
            If omitted redraw is true. If you want to unsketch several coordinate systems and only
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
        CoordinateSystem
            CoordinateSystem object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this coordinate system

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

