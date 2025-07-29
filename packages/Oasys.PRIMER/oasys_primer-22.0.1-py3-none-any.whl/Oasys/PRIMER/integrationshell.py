import Oasys.gRPC


# Metaclass for static properties and constants
class IntegrationShellType(type):

    def __getattr__(cls, name):

        raise AttributeError("IntegrationShell class attribute '{}' does not exist".format(name))


class IntegrationShell(Oasys.gRPC.OasysItem, metaclass=IntegrationShellType):
    _props = {'esop', 'failopt', 'include', 'irid', 'nip', 'pid', 's', 'wf'}
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
        if name in IntegrationShell._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in IntegrationShell._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("IntegrationShell instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in IntegrationShell._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in IntegrationShell._rprops:
            raise AttributeError("Cannot set read-only IntegrationShell instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, irid, nip, esop=Oasys.gRPC.defaultArg, failopt=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, irid, nip, esop, failopt)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new IntegrationShell object

        Parameters
        ----------
        model : Model
            Model that ints will be created in
        irid : integer
            Integration_Beam ID
        nip : integer
            Number of integration points
        esop : integer
            Optional. Equal spacing of integration points option. If omitted esop will be 0
        failopt : integer
            Optional. Treatment of failure when mixing different constitutive types. If omitted failopt will be 0

        Returns
        -------
        IntegrationShell
            IntegrationShell object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def Create(model, modal=Oasys.gRPC.defaultArg):
        """
        Starts an interactive editing panel to create a integration shell

        Parameters
        ----------
        model : Model
            Model that the integration shell will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        IntegrationShell
            IntegrationShell object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def First(model):
        """
        Returns the first integration shell in the model

        Parameters
        ----------
        model : Model
            Model to get first integration shell in

        Returns
        -------
        IntegrationShell
            IntegrationShell object (or None if there are no integration shells in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FirstFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the first free integration shell label in the model.
        Also see IntegrationShell.LastFreeLabel(),
        IntegrationShell.NextFreeLabel() and
        Model.FirstFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get first free integration shell label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            First free in layer in editing panels). If omitted the whole model will be used (Equivalent to
            First free in editing panels)

        Returns
        -------
        int
            IntegrationShell label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FirstFreeLabel", model, layer)

    def FlagAll(model, flag):
        """
        Flags all of the integration shells in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all integration shells will be flagged in
        flag : Flag
            Flag to set on the integration shells

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of IntegrationShell objects or properties for all of the integration shells in a model in PRIMER.
        If the optional property argument is not given then a list of IntegrationShell objects is returned.
        If the property argument is given, that property value for each integration shell is returned in the list
        instead of a IntegrationShell object

        Parameters
        ----------
        model : Model
            Model to get integration shells from
        property : string
            Optional. Name for property to get for all integration shells in the model

        Returns
        -------
        list
            List of IntegrationShell objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of IntegrationShell objects for all of the flagged integration shells in a model in PRIMER
        If the optional property argument is not given then a list of IntegrationShell objects is returned.
        If the property argument is given, then that property value for each integration shell is returned in the list
        instead of a IntegrationShell object

        Parameters
        ----------
        model : Model
            Model to get integration shells from
        flag : Flag
            Flag set on the integration shells that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged integration shells in the model

        Returns
        -------
        list
            List of IntegrationShell objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the IntegrationShell object for a integration shell ID

        Parameters
        ----------
        model : Model
            Model to find the integration shell in
        number : integer
            number of the integration shell you want the IntegrationShell object for

        Returns
        -------
        IntegrationShell
            IntegrationShell object (or None if integration shell does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last integration shell in the model

        Parameters
        ----------
        model : Model
            Model to get last integration shell in

        Returns
        -------
        IntegrationShell
            IntegrationShell object (or None if there are no integration shells in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def LastFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the last free integration shell label in the model.
        Also see IntegrationShell.FirstFreeLabel(),
        IntegrationShell.NextFreeLabel() and
        see Model.LastFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get last free integration shell label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest free in layer in editing panels). If omitted the whole model will be used

        Returns
        -------
        int
            IntegrationShell label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "LastFreeLabel", model, layer)

    def NextFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the next free (highest+1) integration shell label in the model.
        Also see IntegrationShell.FirstFreeLabel(),
        IntegrationShell.LastFreeLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get next free integration shell label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest+1 in layer in editing panels). If omitted the whole model will be used (Equivalent to
            Highest+1 in editing panels)

        Returns
        -------
        int
            IntegrationShell label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NextFreeLabel", model, layer)

    def RenumberAll(model, start):
        """
        Renumbers all of the integration shells in the model

        Parameters
        ----------
        model : Model
            Model that all integration shells will be renumbered in
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
        Renumbers all of the flagged integration shells in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged integration shells will be renumbered in
        flag : Flag
            Flag set on the integration shells that you want to renumber
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
        Allows the user to select integration shells using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting integration shells
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only integration shells from that model can be selected.
            If the argument is a Flag then only integration shells that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any integration shells can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of integration shells selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def Total(model, exists=Oasys.gRPC.defaultArg):
        """
        Returns the total number of integration shells in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing integration shells should be counted. If false or omitted
            referenced but undefined integration shells will also be included in the total

        Returns
        -------
        int
            number of integration shells
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the integration shells in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all integration shells will be unset in
        flag : Flag
            Flag to unset on the integration shells

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)



# Instance methods
    def AssociateComment(self, comment):
        """
        Associates a comment with a integration shell

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the integration shell

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
        Clears a flag on the integration shell

        Parameters
        ----------
        flag : Flag
            Flag to clear on the integration shell

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the integration shell. The target include of the copied integration shell can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        IntegrationShell
            IntegrationShell object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a integration shell

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the integration shell

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
        Checks if the integration shell is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the integration shell

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a integration shell

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetIntegrationPoint(self, index):
        """
        Returns the data for an integration point in \*INTEGRATION_SHELL.Note data is only available when NIP>0 and ESOP=0

        Parameters
        ----------
        index : integer
            Index you want the integration point data for. Note that indices start at 0

        Returns
        -------
        list
            A list containing the integration point data
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetIntegrationPoint", index)

    def GetParameter(self, prop):
        """
        Checks if a IntegrationShell property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the IntegrationShell.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            integration shell property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this ints (\*INTEGRATION_SHELL).
        Note that a carriage return is not added.
        See also IntegrationShell.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the ints.
        Note that a carriage return is not added.
        See also IntegrationShell.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next integration shell in the model

        Returns
        -------
        IntegrationShell
            IntegrationShell object (or None if there are no more integration shells in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous integration shell in the model

        Returns
        -------
        IntegrationShell
            IntegrationShell object (or None if there are no more integration shells in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on the integration shell

        Parameters
        ----------
        flag : Flag
            Flag to set on the integration shell

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def SetIntegrationPoint(self, index, s, wf, pid=Oasys.gRPC.defaultArg):
        """
        Sets the integration point data for an \*INTEGRATION_SHELL

        Parameters
        ----------
        index : integer
            Index you want to set the integration point data for. Note that indices start at 0
        s : float
            Coordinate of integration point in range -1 to 1
        wf : float
            Weighting factor, thickness associated with the integration point divided by actual shell thickness
        pid : integer
            Optional. Optional part ID if different from the PID specified on the element card

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetIntegrationPoint", index, s, wf, pid)

    def ViewParameters(self):
        """
        Object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. This function temporarily
        changes the behaviour so that if a property is a parameter the parameter name is returned instead.
        This can be used with 'method chaining' (see the example below) to make sure a property argument is correct

        Returns
        -------
        IntegrationShell
            IntegrationShell object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this integration shell

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

