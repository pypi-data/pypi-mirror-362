import Oasys.gRPC


# Metaclass for static properties and constants
class InterfaceLinkingEdgeType(type):

    def __getattr__(cls, name):

        raise AttributeError("InterfaceLinkingEdge class attribute '{}' does not exist".format(name))


class InterfaceLinkingEdge(Oasys.gRPC.OasysItem, metaclass=InterfaceLinkingEdgeType):
    _props = {'ifid', 'include', 'nsid'}
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
        if name in InterfaceLinkingEdge._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in InterfaceLinkingEdge._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("InterfaceLinkingEdge instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in InterfaceLinkingEdge._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in InterfaceLinkingEdge._rprops:
            raise AttributeError("Cannot set read-only InterfaceLinkingEdge instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, nsid, ifid):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, nsid, ifid)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new InterfaceLinkingEdge object

        Parameters
        ----------
        model : Model
            Model that Interface Linking Edge will be created in
        nsid : integer
            Node set ID
        ifid : integer
            Interface ID

        Returns
        -------
        InterfaceLinkingEdge
            InterfaceLinkingEdge object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def First(model):
        """
        Returns the first Interface Linking Edge in the model

        Parameters
        ----------
        model : Model
            Model to get first Interface Linking Edge in

        Returns
        -------
        InterfaceLinkingEdge
            InterfaceLinkingEdge object (or None if there are no Interface Linking Edges in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FlagAll(model, flag):
        """
        Flags all of the Interface Linking Edges in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all Interface Linking Edges will be flagged in
        flag : Flag
            Flag to set on the Interface Linking Edges

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of InterfaceLinkingEdge objects or properties for all of the Interface Linking Edges in a model in PRIMER.
        If the optional property argument is not given then a list of InterfaceLinkingEdge objects is returned.
        If the property argument is given, that property value for each Interface Linking Edge is returned in the list
        instead of a InterfaceLinkingEdge object

        Parameters
        ----------
        model : Model
            Model to get Interface Linking Edges from
        property : string
            Optional. Name for property to get for all Interface Linking Edges in the model

        Returns
        -------
        list
            List of InterfaceLinkingEdge objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of InterfaceLinkingEdge objects for all of the flagged Interface Linking Edges in a model in PRIMER
        If the optional property argument is not given then a list of InterfaceLinkingEdge objects is returned.
        If the property argument is given, then that property value for each Interface Linking Edge is returned in the list
        instead of a InterfaceLinkingEdge object

        Parameters
        ----------
        model : Model
            Model to get Interface Linking Edges from
        flag : Flag
            Flag set on the Interface Linking Edges that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged Interface Linking Edges in the model

        Returns
        -------
        list
            List of InterfaceLinkingEdge objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the InterfaceLinkingEdge object for a Interface Linking Edge ID

        Parameters
        ----------
        model : Model
            Model to find the Interface Linking Edge in
        number : integer
            number of the Interface Linking Edge you want the InterfaceLinkingEdge object for

        Returns
        -------
        InterfaceLinkingEdge
            InterfaceLinkingEdge object (or None if Interface Linking Edge does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last Interface Linking Edge in the model

        Parameters
        ----------
        model : Model
            Model to get last Interface Linking Edge in

        Returns
        -------
        InterfaceLinkingEdge
            InterfaceLinkingEdge object (or None if there are no Interface Linking Edges in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def Select(flag, prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg):
        """
        Allows the user to select Interface Linking Edges using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting Interface Linking Edges
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only Interface Linking Edges from that model can be selected.
            If the argument is a Flag then only Interface Linking Edges that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any Interface Linking Edges can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of Interface Linking Edges selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def Total(model, exists=Oasys.gRPC.defaultArg):
        """
        Returns the total number of Interface Linking Edges in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing Interface Linking Edges should be counted. If false or omitted
            referenced but undefined Interface Linking Edges will also be included in the total

        Returns
        -------
        int
            number of Interface Linking Edges
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the Interface Linking Edges in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all Interface Linking Edges will be unset in
        flag : Flag
            Flag to unset on the Interface Linking Edges

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)



# Instance methods
    def AssociateComment(self, comment):
        """
        Associates a comment with a Interface Linking Edge

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the Interface Linking Edge

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def ClearFlag(self, flag):
        """
        Clears a flag on the Interface Linking Edge

        Parameters
        ----------
        flag : Flag
            Flag to clear on the Interface Linking Edge

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the Interface Linking Edge. The target include of the copied Interface Linking Edge can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        InterfaceLinkingEdge
            InterfaceLinkingEdge object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a Interface Linking Edge

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the Interface Linking Edge

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "DetachComment", comment)

    def Flagged(self, flag):
        """
        Checks if the Interface Linking Edge is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the Interface Linking Edge

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a Interface Linking Edge

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a InterfaceLinkingEdge property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the InterfaceLinkingEdge.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            Interface Linking Edge property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this Interface Linking Edge (\*INTERFACE_LINKING_EDGE).
        Note that a carriage return is not added.
        See also InterfaceLinkingEdge.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the Interface Linking Edge.
        Note that a carriage return is not added.
        See also InterfaceLinkingEdge.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next Interface Linking Edge in the model

        Returns
        -------
        InterfaceLinkingEdge
            InterfaceLinkingEdge object (or None if there are no more Interface Linking Edges in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous Interface Linking Edge in the model

        Returns
        -------
        InterfaceLinkingEdge
            InterfaceLinkingEdge object (or None if there are no more Interface Linking Edges in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on the Interface Linking Edge

        Parameters
        ----------
        flag : Flag
            Flag to set on the Interface Linking Edge

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
        InterfaceLinkingEdge
            InterfaceLinkingEdge object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this Interface Linking Edge

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

