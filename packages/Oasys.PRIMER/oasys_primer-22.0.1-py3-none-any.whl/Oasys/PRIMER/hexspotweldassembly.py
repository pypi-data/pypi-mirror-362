import Oasys.gRPC


# Metaclass for static properties and constants
class HexSpotweldAssemblyType(type):

    def __getattr__(cls, name):

        raise AttributeError("HexSpotweldAssembly class attribute '{}' does not exist".format(name))


class HexSpotweldAssembly(Oasys.gRPC.OasysItem, metaclass=HexSpotweldAssemblyType):
    _props = {'eid1', 'eid10', 'eid11', 'eid12', 'eid13', 'eid14', 'eid15', 'eid16', 'eid2', 'eid3', 'eid4', 'eid5', 'eid6', 'eid7', 'eid8', 'eid9', 'id', 'include', 'opt', 'title'}
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
        if name in HexSpotweldAssembly._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in HexSpotweldAssembly._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("HexSpotweldAssembly instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in HexSpotweldAssembly._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in HexSpotweldAssembly._rprops:
            raise AttributeError("Cannot set read-only HexSpotweldAssembly instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, options):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, options)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new \*DEFINE_HEX_SPOTWELD_ASSEMBLY object

        Parameters
        ----------
        model : Model
            Model that Hex Spotweld Assembly will be created in
        options : dict
            Options for creating the HexSpotweldAssembly

        Returns
        -------
        HexSpotweldAssembly
            HexSpotweldAssembly object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def Create(model, modal=Oasys.gRPC.defaultArg):
        """
        Starts an interactive editing panel to create a DEFINE_HEX_SPOTWELD_ASSEMBLY

        Parameters
        ----------
        model : Model
            Model that the DEFINE_HEX_SPOTWELD_ASSEMBLY will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        HexSpotweldAssembly
            HexSpotweldAssembly object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def First(model):
        """
        Returns the first DEFINE_HEX_SPOTWELD_ASSEMBLY in the model

        Parameters
        ----------
        model : Model
            Model to get first DEFINE_HEX_SPOTWELD_ASSEMBLY in

        Returns
        -------
        HexSpotweldAssembly
            HexSpotweldAssembly object (or None if there are no DEFINE_HEX_SPOTWELD_ASSEMBLYs in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FirstFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the first free DEFINE_HEX_SPOTWELD_ASSEMBLY label in the model.
        Also see HexSpotweldAssembly.LastFreeLabel(),
        HexSpotweldAssembly.NextFreeLabel() and
        Model.FirstFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get first free DEFINE_HEX_SPOTWELD_ASSEMBLY label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            First free in layer in editing panels). If omitted the whole model will be used (Equivalent to
            First free in editing panels)

        Returns
        -------
        int
            HexSpotweldAssembly label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FirstFreeLabel", model, layer)

    def FlagAll(model, flag):
        """
        Flags all of the DEFINE_HEX_SPOTWELD_ASSEMBLYs in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all DEFINE_HEX_SPOTWELD_ASSEMBLYs will be flagged in
        flag : Flag
            Flag to set on the DEFINE_HEX_SPOTWELD_ASSEMBLYs

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of HexSpotweldAssembly objects or properties for all of the DEFINE_HEX_SPOTWELD_ASSEMBLYs in a model in PRIMER.
        If the optional property argument is not given then a list of HexSpotweldAssembly objects is returned.
        If the property argument is given, that property value for each DEFINE_HEX_SPOTWELD_ASSEMBLY is returned in the list
        instead of a HexSpotweldAssembly object

        Parameters
        ----------
        model : Model
            Model to get DEFINE_HEX_SPOTWELD_ASSEMBLYs from
        property : string
            Optional. Name for property to get for all DEFINE_HEX_SPOTWELD_ASSEMBLYs in the model

        Returns
        -------
        list
            List of HexSpotweldAssembly objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of HexSpotweldAssembly objects for all of the flagged DEFINE_HEX_SPOTWELD_ASSEMBLYs in a model in PRIMER
        If the optional property argument is not given then a list of HexSpotweldAssembly objects is returned.
        If the property argument is given, then that property value for each DEFINE_HEX_SPOTWELD_ASSEMBLY is returned in the list
        instead of a HexSpotweldAssembly object

        Parameters
        ----------
        model : Model
            Model to get DEFINE_HEX_SPOTWELD_ASSEMBLYs from
        flag : Flag
            Flag set on the DEFINE_HEX_SPOTWELD_ASSEMBLYs that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged DEFINE_HEX_SPOTWELD_ASSEMBLYs in the model

        Returns
        -------
        list
            List of HexSpotweldAssembly objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the HexSpotweldAssembly object for a DEFINE_HEX_SPOTWELD_ASSEMBLY ID

        Parameters
        ----------
        model : Model
            Model to find the DEFINE_HEX_SPOTWELD_ASSEMBLY in
        number : integer
            number of the DEFINE_HEX_SPOTWELD_ASSEMBLY you want the HexSpotweldAssembly object for

        Returns
        -------
        HexSpotweldAssembly
            HexSpotweldAssembly object (or None if DEFINE_HEX_SPOTWELD_ASSEMBLY does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last DEFINE_HEX_SPOTWELD_ASSEMBLY in the model

        Parameters
        ----------
        model : Model
            Model to get last DEFINE_HEX_SPOTWELD_ASSEMBLY in

        Returns
        -------
        HexSpotweldAssembly
            HexSpotweldAssembly object (or None if there are no DEFINE_HEX_SPOTWELD_ASSEMBLYs in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def LastFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the last free DEFINE_HEX_SPOTWELD_ASSEMBLY label in the model.
        Also see HexSpotweldAssembly.FirstFreeLabel(),
        HexSpotweldAssembly.NextFreeLabel() and
        see Model.LastFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get last free DEFINE_HEX_SPOTWELD_ASSEMBLY label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest free in layer in editing panels). If omitted the whole model will be used

        Returns
        -------
        int
            HexSpotweldAssembly label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "LastFreeLabel", model, layer)

    def NextFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the next free (highest+1) DEFINE_HEX_SPOTWELD_ASSEMBLY label in the model.
        Also see HexSpotweldAssembly.FirstFreeLabel(),
        HexSpotweldAssembly.LastFreeLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get next free DEFINE_HEX_SPOTWELD_ASSEMBLY label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest+1 in layer in editing panels). If omitted the whole model will be used (Equivalent to
            Highest+1 in editing panels)

        Returns
        -------
        int
            HexSpotweldAssembly label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NextFreeLabel", model, layer)

    def RenumberAll(model, start):
        """
        Renumbers all of the DEFINE_HEX_SPOTWELD_ASSEMBLYs in the model

        Parameters
        ----------
        model : Model
            Model that all DEFINE_HEX_SPOTWELD_ASSEMBLYs will be renumbered in
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
        Renumbers all of the flagged DEFINE_HEX_SPOTWELD_ASSEMBLYs in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged DEFINE_HEX_SPOTWELD_ASSEMBLYs will be renumbered in
        flag : Flag
            Flag set on the DEFINE_HEX_SPOTWELD_ASSEMBLYs that you want to renumber
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
        Allows the user to select DEFINE_HEX_SPOTWELD_ASSEMBLYs using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting DEFINE_HEX_SPOTWELD_ASSEMBLYs
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only DEFINE_HEX_SPOTWELD_ASSEMBLYs from that model can be selected.
            If the argument is a Flag then only DEFINE_HEX_SPOTWELD_ASSEMBLYs that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any DEFINE_HEX_SPOTWELD_ASSEMBLYs can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of DEFINE_HEX_SPOTWELD_ASSEMBLYs selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def Total(model, exists=Oasys.gRPC.defaultArg):
        """
        Returns the total number of DEFINE_HEX_SPOTWELD_ASSEMBLYs in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing DEFINE_HEX_SPOTWELD_ASSEMBLYs should be counted. If false or omitted
            referenced but undefined DEFINE_HEX_SPOTWELD_ASSEMBLYs will also be included in the total

        Returns
        -------
        int
            number of DEFINE_HEX_SPOTWELD_ASSEMBLYs
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the DEFINE_HEX_SPOTWELD_ASSEMBLYs in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all DEFINE_HEX_SPOTWELD_ASSEMBLYs will be unset in
        flag : Flag
            Flag to unset on the DEFINE_HEX_SPOTWELD_ASSEMBLYs

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)



# Instance methods
    def AssociateComment(self, comment):
        """
        Associates a comment with a DEFINE_HEX_SPOTWELD_ASSEMBLY

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the DEFINE_HEX_SPOTWELD_ASSEMBLY

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
        Clears a flag on the DEFINE_HEX_SPOTWELD_ASSEMBLY

        Parameters
        ----------
        flag : Flag
            Flag to clear on the DEFINE_HEX_SPOTWELD_ASSEMBLY

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the DEFINE_HEX_SPOTWELD_ASSEMBLY. The target include of the copied DEFINE_HEX_SPOTWELD_ASSEMBLY can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        HexSpotweldAssembly
            HexSpotweldAssembly object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a DEFINE_HEX_SPOTWELD_ASSEMBLY

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the DEFINE_HEX_SPOTWELD_ASSEMBLY

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
        Checks if the DEFINE_HEX_SPOTWELD_ASSEMBLY is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the DEFINE_HEX_SPOTWELD_ASSEMBLY

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a DEFINE_HEX_SPOTWELD_ASSEMBLY

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a HexSpotweldAssembly property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the HexSpotweldAssembly.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            DEFINE_HEX_SPOTWELD_ASSEMBLY property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this HexSpotweldAssembly (\*DEFINE_HEX_SPOTWELD_ASSEMBLY).
        Note that a carriage return is not added.
        See also HexSpotweldAssembly.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the HexSpotweldAssem.
        Note that a carriage return is not added.
        See also HexSpotweldAssembly.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next DEFINE_HEX_SPOTWELD_ASSEMBLY in the model

        Returns
        -------
        HexSpotweldAssembly
            HexSpotweldAssembly object (or None if there are no more DEFINE_HEX_SPOTWELD_ASSEMBLYs in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous DEFINE_HEX_SPOTWELD_ASSEMBLY in the model

        Returns
        -------
        HexSpotweldAssembly
            HexSpotweldAssembly object (or None if there are no more DEFINE_HEX_SPOTWELD_ASSEMBLYs in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on the DEFINE_HEX_SPOTWELD_ASSEMBLY

        Parameters
        ----------
        flag : Flag
            Flag to set on the DEFINE_HEX_SPOTWELD_ASSEMBLY

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
        HexSpotweldAssembly
            HexSpotweldAssembly object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this DEFINE_HEX_SPOTWELD_ASSEMBLY

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

