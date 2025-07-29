import Oasys.gRPC


# Metaclass for static properties and constants
class MorphFlowType(type):

    def __getattr__(cls, name):

        raise AttributeError("MorphFlow class attribute '{}' does not exist".format(name))


class MorphFlow(Oasys.gRPC.OasysItem, metaclass=MorphFlowType):
    _props = {'include', 'max', 'min', 'name', 'step', 'type'}
    _rprops = {'exists', 'model', 'npoints', 'nvals'}


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
        if name in MorphFlow._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in MorphFlow._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("MorphFlow instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in MorphFlow._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in MorphFlow._rprops:
            raise AttributeError("Cannot set read-only MorphFlow instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, name):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, name)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new MorphFlow object

        Parameters
        ----------
        model : Model
            Model that morph flow will be created in
        name : string
            MorphFlow name

        Returns
        -------
        MorphFlow
            MorphFlow object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def BlankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the flows in the model

        Parameters
        ----------
        model : Model
            Model that all flows will be blanked in
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
        Blanks all of the flagged flows in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged flows will be blanked in
        flag : Flag
            Flag set on the flows that you want to blank
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
        Starts an interactive editing panel to create a flow

        Parameters
        ----------
        model : Model
            Model that the flow will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        MorphFlow
            MorphFlow object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def First(model):
        """
        Returns the first flow in the model

        Parameters
        ----------
        model : Model
            Model to get first flow in

        Returns
        -------
        MorphFlow
            MorphFlow object (or None if there are no flows in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FlagAll(model, flag):
        """
        Flags all of the flows in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all flows will be flagged in
        flag : Flag
            Flag to set on the flows

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of MorphFlow objects or properties for all of the flows in a model in PRIMER.
        If the optional property argument is not given then a list of MorphFlow objects is returned.
        If the property argument is given, that property value for each flow is returned in the list
        instead of a MorphFlow object

        Parameters
        ----------
        model : Model
            Model to get flows from
        property : string
            Optional. Name for property to get for all flows in the model

        Returns
        -------
        list
            List of MorphFlow objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of MorphFlow objects for all of the flagged flows in a model in PRIMER
        If the optional property argument is not given then a list of MorphFlow objects is returned.
        If the property argument is given, then that property value for each flow is returned in the list
        instead of a MorphFlow object

        Parameters
        ----------
        model : Model
            Model to get flows from
        flag : Flag
            Flag set on the flows that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged flows in the model

        Returns
        -------
        list
            List of MorphFlow objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the MorphFlow object for a flow ID

        Parameters
        ----------
        model : Model
            Model to find the flow in
        number : integer
            number of the flow you want the MorphFlow object for

        Returns
        -------
        MorphFlow
            MorphFlow object (or None if flow does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def GetFromName(model, morph_flow_name):
        """
        Returns the stored MorphFlow object for a morph flow name.
        WARNING: This assumes that there is at most one morph flow with a given name.
        Otherwise this function only returns the first occurrence

        Parameters
        ----------
        model : Model
            Model to find the morph flow in
        morph_flow_name : string
            name of the morph flow you want the MorphFlow object for

        Returns
        -------
        MorphFlow
            MorphFlow object (or None if morph flow does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromName", model, morph_flow_name)

    def Last(model):
        """
        Returns the last flow in the model

        Parameters
        ----------
        model : Model
            Model to get last flow in

        Returns
        -------
        MorphFlow
            MorphFlow object (or None if there are no flows in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a flow

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only flows from that model can be picked.
            If the argument is a Flag then only flows that
            are flagged with limit can be selected.
            If omitted, or None, any flows from any model can be selected.
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
        MorphFlow
            MorphFlow object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def Select(flag, prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg):
        """
        Allows the user to select flows using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting flows
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only flows from that model can be selected.
            If the argument is a Flag then only flows that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any flows can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of flows selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged flows in the model. The flows will be sketched until you either call
        MorphFlow.Unsketch(),
        MorphFlow.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged flows will be sketched in
        flag : Flag
            Flag set on the flows that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the flows are sketched.
            If omitted redraw is true. If you want to sketch flagged flows several times and only
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
        Returns the total number of flows in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing flows should be counted. If false or omitted
            referenced but undefined flows will also be included in the total

        Returns
        -------
        int
            number of flows
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnblankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the flows in the model

        Parameters
        ----------
        model : Model
            Model that all flows will be unblanked in
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
        Unblanks all of the flagged flows in the model

        Parameters
        ----------
        model : Model
            Model that the flagged flows will be unblanked in
        flag : Flag
            Flag set on the flows that you want to unblank
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
        Unsets a defined flag on all of the flows in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all flows will be unset in
        flag : Flag
            Flag to unset on the flows

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all flows

        Parameters
        ----------
        model : Model
            Model that all flows will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the flows are unsketched.
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
        Unsketches all flagged flows in the model

        Parameters
        ----------
        model : Model
            Model that all flows will be unsketched in
        flag : Flag
            Flag set on the flows that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the flows are unsketched.
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
        Associates a comment with a flow

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the flow

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def Blank(self):
        """
        Blanks the flow

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank")

    def Blanked(self):
        """
        Checks if the flow is blanked or not

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
        Clears a flag on the flow

        Parameters
        ----------
        flag : Flag
            Flag to clear on the flow

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the flow. The target include of the copied flow can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        MorphFlow
            MorphFlow object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a flow

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the flow

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
        Checks if the flow is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the flow

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a flow

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a MorphFlow property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the MorphFlow.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            flow property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def GetRow(self, row):
        """
        Returns the data for a row in the morph flow

        Parameters
        ----------
        row : integer
            The row you want the data for. Note row indices start at 0

        Returns
        -------
        list
            A list of numbers containing the morph point ID at index 0 and the vector components at indices 1, 2, 3
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetRow", row)

    def GetValue(self, index):
        """
        Get the value at given index on the morph flow with type "DISCRETE"

        Parameters
        ----------
        index : integer
            The index where you are extracting the value.
            Note row indices start at 0

        Returns
        -------
        float
            float
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetValue", index)

    def Keyword(self):
        """
        Returns the keyword for this morph flow (\*MORPH_FLOW).
        Note that a carriage return is not added.
        See also MorphFlow.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the morph flow.
        Note that a carriage return is not added.
        See also MorphFlow.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next flow in the model

        Returns
        -------
        MorphFlow
            MorphFlow object (or None if there are no more flows in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous flow in the model

        Returns
        -------
        MorphFlow
            MorphFlow object (or None if there are no more flows in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def RemoveRow(self, row):
        """
        Removes the data (a morph point ID and its three
        vector components) for a row in \*MORPH_FLOW

        Parameters
        ----------
        row : integer
            The row you want to remove the data for.
            Note that row indices start at 0

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "RemoveRow", row)

    def RemoveValue(self, index):
        """
        Removes the value at given index in \*MORPH_FLOW with type "DISCRETE"

        Parameters
        ----------
        index : integer
            The index where you are removing the value.
            Note that indices start at 0

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "RemoveValue", index)

    def SetFlag(self, flag):
        """
        Sets a flag on the flow

        Parameters
        ----------
        flag : Flag
            Flag to set on the flow

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def SetRow(self, row, data):
        """
        Sets the data for a row in \*MORPH_FLOW

        Parameters
        ----------
        row : integer
            The row you want to set the data for.
            Note that row indices start at 0
        data : List of data
            The data you want to set the row to. It should be of length 4
            having the morph point ID at index 0, and the vector components at
            indices 1, 2, 3

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetRow", row, data)

    def SetValue(self, index, value):
        """
        Sets the value at given index in a \*MORPH_FLOW with type "DISCRETE"

        Parameters
        ----------
        index : integer
            The row you want to set the data for.
            Note that row indices start at 0
        value : real
            The new value to insert into the list

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetValue", index, value)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the flow. The flow will be sketched until you either call
        MorphFlow.Unsketch(),
        MorphFlow.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the flow is sketched.
            If omitted redraw is true. If you want to sketch several flows and only
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
        Unblanks the flow

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank")

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the flow

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the flow is unsketched.
            If omitted redraw is true. If you want to unsketch several flows and only
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
        MorphFlow
            MorphFlow object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this flow

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

