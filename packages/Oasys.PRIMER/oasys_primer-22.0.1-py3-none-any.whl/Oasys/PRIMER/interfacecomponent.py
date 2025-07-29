import Oasys.gRPC


# Metaclass for static properties and constants
class InterfaceComponentType(type):
    _consts = {'NODE', 'SEGMENT'}

    def __getattr__(cls, name):
        if name in InterfaceComponentType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("InterfaceComponent class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in InterfaceComponentType._consts:
            raise AttributeError("Cannot set InterfaceComponent class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class InterfaceComponent(Oasys.gRPC.OasysItem, metaclass=InterfaceComponentType):
    _props = {'cid', 'include', 'nid', 'nsid', 'option', 'ssid', 'title'}
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
        if name in InterfaceComponent._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in InterfaceComponent._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("InterfaceComponent instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in InterfaceComponent._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in InterfaceComponent._rprops:
            raise AttributeError("Cannot set read-only InterfaceComponent instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, type, snid_ssid, cid, nid, label=Oasys.gRPC.defaultArg, title=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, type, snid_ssid, cid, nid, label, title)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new InterfaceComponent object

        Parameters
        ----------
        model : Model
            Model that InterfaceComponent will be created in
        type : constant
            InterfaceComponent type. Can be
            InterfaceComponent.NODE,
            InterfaceComponent.SEGMENT,
        snid_ssid : integer
            Set node or set segment ID
        cid : integer
            Coordinate system ID
        nid : integer
            Node ID
        label : integer
            Optional. InterfaceComponent number
        title : string
            Optional. Title for this interface

        Returns
        -------
        InterfaceComponent
            InterfaceComponent object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def Create(model, modal=Oasys.gRPC.defaultArg):
        """
        Starts an interactive editing panel to create a interface component

        Parameters
        ----------
        model : Model
            Model that the interface component will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        InterfaceComponent
            InterfaceComponent object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def First(model):
        """
        Returns the first interface component in the model

        Parameters
        ----------
        model : Model
            Model to get first interface component in

        Returns
        -------
        InterfaceComponent
            InterfaceComponent object (or None if there are no interface components in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FirstFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the first free interface component label in the model.
        Also see InterfaceComponent.LastFreeLabel(),
        InterfaceComponent.NextFreeLabel() and
        Model.FirstFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get first free interface component label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            First free in layer in editing panels). If omitted the whole model will be used (Equivalent to
            First free in editing panels)

        Returns
        -------
        int
            InterfaceComponent label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FirstFreeLabel", model, layer)

    def FlagAll(model, flag):
        """
        Flags all of the interface components in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all interface components will be flagged in
        flag : Flag
            Flag to set on the interface components

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of InterfaceComponent objects or properties for all of the interface components in a model in PRIMER.
        If the optional property argument is not given then a list of InterfaceComponent objects is returned.
        If the property argument is given, that property value for each interface component is returned in the list
        instead of a InterfaceComponent object

        Parameters
        ----------
        model : Model
            Model to get interface components from
        property : string
            Optional. Name for property to get for all interface components in the model

        Returns
        -------
        list
            List of InterfaceComponent objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of InterfaceComponent objects for all of the flagged interface components in a model in PRIMER
        If the optional property argument is not given then a list of InterfaceComponent objects is returned.
        If the property argument is given, then that property value for each interface component is returned in the list
        instead of a InterfaceComponent object

        Parameters
        ----------
        model : Model
            Model to get interface components from
        flag : Flag
            Flag set on the interface components that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged interface components in the model

        Returns
        -------
        list
            List of InterfaceComponent objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the InterfaceComponent object for a interface component ID

        Parameters
        ----------
        model : Model
            Model to find the interface component in
        number : integer
            number of the interface component you want the InterfaceComponent object for

        Returns
        -------
        InterfaceComponent
            InterfaceComponent object (or None if interface component does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last interface component in the model

        Parameters
        ----------
        model : Model
            Model to get last interface component in

        Returns
        -------
        InterfaceComponent
            InterfaceComponent object (or None if there are no interface components in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def LastFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the last free interface component label in the model.
        Also see InterfaceComponent.FirstFreeLabel(),
        InterfaceComponent.NextFreeLabel() and
        see Model.LastFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get last free interface component label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest free in layer in editing panels). If omitted the whole model will be used

        Returns
        -------
        int
            InterfaceComponent label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "LastFreeLabel", model, layer)

    def NextFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the next free (highest+1) interface component label in the model.
        Also see InterfaceComponent.FirstFreeLabel(),
        InterfaceComponent.LastFreeLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get next free interface component label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest+1 in layer in editing panels). If omitted the whole model will be used (Equivalent to
            Highest+1 in editing panels)

        Returns
        -------
        int
            InterfaceComponent label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NextFreeLabel", model, layer)

    def RenumberAll(model, start):
        """
        Renumbers all of the interface components in the model

        Parameters
        ----------
        model : Model
            Model that all interface components will be renumbered in
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
        Renumbers all of the flagged interface components in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged interface components will be renumbered in
        flag : Flag
            Flag set on the interface components that you want to renumber
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
        Allows the user to select interface components using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting interface components
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only interface components from that model can be selected.
            If the argument is a Flag then only interface components that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any interface components can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of interface components selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def Total(model, exists=Oasys.gRPC.defaultArg):
        """
        Returns the total number of interface components in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing interface components should be counted. If false or omitted
            referenced but undefined interface components will also be included in the total

        Returns
        -------
        int
            number of interface components
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the interface components in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all interface components will be unset in
        flag : Flag
            Flag to unset on the interface components

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)



# Instance methods
    def AssociateComment(self, comment):
        """
        Associates a comment with a interface component

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the interface component

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
        Clears a flag on the interface component

        Parameters
        ----------
        flag : Flag
            Flag to clear on the interface component

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the interface component. The target include of the copied interface component can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        InterfaceComponent
            InterfaceComponent object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a interface component

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the interface component

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
        Checks if the interface component is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the interface component

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a interface component

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a InterfaceComponent property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the InterfaceComponent.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            interface component property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this InterfaceComponent (\*INTERFACE_COMPONENT).
        Note that a carriage return is not added.
        See also InterfaceComponent.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the InterfaceComponent.
        Note that a carriage return is not added.
        See also InterfaceComponent.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next interface component in the model

        Returns
        -------
        InterfaceComponent
            InterfaceComponent object (or None if there are no more interface components in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous interface component in the model

        Returns
        -------
        InterfaceComponent
            InterfaceComponent object (or None if there are no more interface components in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on the interface component

        Parameters
        ----------
        flag : Flag
            Flag to set on the interface component

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
        InterfaceComponent
            InterfaceComponent object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this interface component

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

