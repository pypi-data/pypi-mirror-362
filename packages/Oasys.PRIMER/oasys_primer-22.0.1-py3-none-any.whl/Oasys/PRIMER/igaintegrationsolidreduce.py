import Oasys.gRPC


# Metaclass for static properties and constants
class IGAIntegrationSolidReduceType(type):

    def __getattr__(cls, name):

        raise AttributeError("IGAIntegrationSolidReduce class attribute '{}' does not exist".format(name))


class IGAIntegrationSolidReduce(Oasys.gRPC.OasysItem, metaclass=IGAIntegrationSolidReduceType):
    _props = {'include', 'nrdr', 'nrds', 'nrdt', 'patchid'}
    _rprops = {'exists', 'id', 'model'}


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
        if name in IGAIntegrationSolidReduce._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in IGAIntegrationSolidReduce._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("IGAIntegrationSolidReduce instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in IGAIntegrationSolidReduce._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in IGAIntegrationSolidReduce._rprops:
            raise AttributeError("Cannot set read-only IGAIntegrationSolidReduce instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, details):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, details)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new IGAIntegrationSolidReduce object

        Parameters
        ----------
        model : Model
            Model that IGA integration solid reduce will be created in
        details : dict
            Details for creating the IGAIntegrationSolidReduce

        Returns
        -------
        IGAIntegrationSolidReduce
            IGAIntegrationSolidReduce object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def Create(model, modal=Oasys.gRPC.defaultArg):
        """
        Starts an interactive editing panel to create a IGA Integration Solid Reduce

        Parameters
        ----------
        model : Model
            Model that the IGA Integration Solid Reduce will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        IGAIntegrationSolidReduce
            IGAIntegrationSolidReduce object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def First(model):
        """
        Returns the first IGA Integration Solid Reduce in the model

        Parameters
        ----------
        model : Model
            Model to get first IGA Integration Solid Reduce in

        Returns
        -------
        IGAIntegrationSolidReduce
            IGAIntegrationSolidReduce object (or None if there are no IGA Integration Solid Reduces in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FlagAll(model, flag):
        """
        Flags all of the IGA Integration Solid Reduces in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all IGA Integration Solid Reduces will be flagged in
        flag : Flag
            Flag to set on the IGA Integration Solid Reduces

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of IGAIntegrationSolidReduce objects or properties for all of the IGA Integration Solid Reduces in a model in PRIMER.
        If the optional property argument is not given then a list of IGAIntegrationSolidReduce objects is returned.
        If the property argument is given, that property value for each IGA Integration Solid Reduce is returned in the list
        instead of a IGAIntegrationSolidReduce object

        Parameters
        ----------
        model : Model
            Model to get IGA Integration Solid Reduces from
        property : string
            Optional. Name for property to get for all IGA Integration Solid Reduces in the model

        Returns
        -------
        list
            List of IGAIntegrationSolidReduce objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of IGAIntegrationSolidReduce objects for all of the flagged IGA Integration Solid Reduces in a model in PRIMER
        If the optional property argument is not given then a list of IGAIntegrationSolidReduce objects is returned.
        If the property argument is given, then that property value for each IGA Integration Solid Reduce is returned in the list
        instead of a IGAIntegrationSolidReduce object

        Parameters
        ----------
        model : Model
            Model to get IGA Integration Solid Reduces from
        flag : Flag
            Flag set on the IGA Integration Solid Reduces that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged IGA Integration Solid Reduces in the model

        Returns
        -------
        list
            List of IGAIntegrationSolidReduce objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the IGAIntegrationSolidReduce object for a IGA Integration Solid Reduce ID

        Parameters
        ----------
        model : Model
            Model to find the IGA Integration Solid Reduce in
        number : integer
            number of the IGA Integration Solid Reduce you want the IGAIntegrationSolidReduce object for

        Returns
        -------
        IGAIntegrationSolidReduce
            IGAIntegrationSolidReduce object (or None if IGA Integration Solid Reduce does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last IGA Integration Solid Reduce in the model

        Parameters
        ----------
        model : Model
            Model to get last IGA Integration Solid Reduce in

        Returns
        -------
        IGAIntegrationSolidReduce
            IGAIntegrationSolidReduce object (or None if there are no IGA Integration Solid Reduces in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a IGA Integration Solid Reduce

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only IGA Integration Solid Reduces from that model can be picked.
            If the argument is a Flag then only IGA Integration Solid Reduces that
            are flagged with limit can be selected.
            If omitted, or None, any IGA Integration Solid Reduces from any model can be selected.
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
        IGAIntegrationSolidReduce
            IGAIntegrationSolidReduce object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def Select(flag, prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg):
        """
        Allows the user to select IGA Integration Solid Reduces using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting IGA Integration Solid Reduces
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only IGA Integration Solid Reduces from that model can be selected.
            If the argument is a Flag then only IGA Integration Solid Reduces that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any IGA Integration Solid Reduces can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of IGA Integration Solid Reduces selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged IGA Integration Solid Reduces in the model. The IGA Integration Solid Reduces will be sketched until you either call
        IGAIntegrationSolidReduce.Unsketch(),
        IGAIntegrationSolidReduce.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged IGA Integration Solid Reduces will be sketched in
        flag : Flag
            Flag set on the IGA Integration Solid Reduces that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the IGA Integration Solid Reduces are sketched.
            If omitted redraw is true. If you want to sketch flagged IGA Integration Solid Reduces several times and only
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
        Returns the total number of IGA Integration Solid Reduces in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing IGA Integration Solid Reduces should be counted. If false or omitted
            referenced but undefined IGA Integration Solid Reduces will also be included in the total

        Returns
        -------
        int
            number of IGA Integration Solid Reduces
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the IGA Integration Solid Reduces in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all IGA Integration Solid Reduces will be unset in
        flag : Flag
            Flag to unset on the IGA Integration Solid Reduces

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all IGA Integration Solid Reduces

        Parameters
        ----------
        model : Model
            Model that all IGA Integration Solid Reduces will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the IGA Integration Solid Reduces are unsketched.
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
        Unsketches all flagged IGA Integration Solid Reduces in the model

        Parameters
        ----------
        model : Model
            Model that all IGA Integration Solid Reduces will be unsketched in
        flag : Flag
            Flag set on the IGA Integration Solid Reduces that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the IGA Integration Solid Reduces are unsketched.
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
        Associates a comment with a IGA Integration Solid Reduce

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the IGA Integration Solid Reduce

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
        Clears a flag on the IGA Integration Solid Reduce

        Parameters
        ----------
        flag : Flag
            Flag to clear on the IGA Integration Solid Reduce

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the IGA Integration Solid Reduce. The target include of the copied IGA Integration Solid Reduce can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        IGAIntegrationSolidReduce
            IGAIntegrationSolidReduce object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a IGA Integration Solid Reduce

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the IGA Integration Solid Reduce

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
        Checks if the IGA Integration Solid Reduce is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the IGA Integration Solid Reduce

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a IGA Integration Solid Reduce

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a IGAIntegrationSolidReduce property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the IGAIntegrationSolidReduce.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            IGA Integration Solid Reduce property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this IGA integration solid reduce (\*IGA_SOLID).
        Note that a carriage return is not added.
        See also IGAIntegrationSolidReduce.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the IGA integration solid reduce.
        Note that a carriage return is not added.
        See also IGAIntegrationSolidReduce.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next IGA Integration Solid Reduce in the model

        Returns
        -------
        IGAIntegrationSolidReduce
            IGAIntegrationSolidReduce object (or None if there are no more IGA Integration Solid Reduces in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous IGA Integration Solid Reduce in the model

        Returns
        -------
        IGAIntegrationSolidReduce
            IGAIntegrationSolidReduce object (or None if there are no more IGA Integration Solid Reduces in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on the IGA Integration Solid Reduce

        Parameters
        ----------
        flag : Flag
            Flag to set on the IGA Integration Solid Reduce

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the IGA Integration Solid Reduce. The IGA Integration Solid Reduce will be sketched until you either call
        IGAIntegrationSolidReduce.Unsketch(),
        IGAIntegrationSolidReduce.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the IGA Integration Solid Reduce is sketched.
            If omitted redraw is true. If you want to sketch several IGA Integration Solid Reduces and only
            redraw after the last one then use false for redraw and call
            View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Sketch", redraw)

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the IGA Integration Solid Reduce

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the IGA Integration Solid Reduce is unsketched.
            If omitted redraw is true. If you want to unsketch several IGA Integration Solid Reduces and only
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
        IGAIntegrationSolidReduce
            IGAIntegrationSolidReduce object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this IGA Integration Solid Reduce

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

