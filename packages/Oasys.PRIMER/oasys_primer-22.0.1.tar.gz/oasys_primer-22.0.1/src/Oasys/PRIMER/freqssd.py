import Oasys.gRPC


# Metaclass for static properties and constants
class FreqSSDType(type):
    _consts = {'DIRECT', 'DIRECT_FD', 'ERP', 'FATIGUE', 'FRF', 'SUBCASE'}

    def __getattr__(cls, name):
        if name in FreqSSDType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("FreqSSD class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in FreqSSDType._consts:
            raise AttributeError("Cannot set FreqSSD class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class FreqSSD(Oasys.gRPC.OasysItem, metaclass=FreqSSDType):
    _props = {'c', 'dampf', 'dmpflg', 'dmpmas', 'dmpstf', 'erpref', 'erprlf', 'fnmax', 'fnmin', 'include', 'istress', 'lcdam', 'lcflag', 'lcftg', 'lctyp', 'mdmax', 'mdmin', 'memory', 'nerp', 'notyp', 'nout', 'nova', 'option', 'radeff', 'relatv', 'restdp', 'restmd', 'ro', 'strtyp'}
    _rprops = {'exists', 'label', 'model'}


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
        if name in FreqSSD._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in FreqSSD._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("FreqSSD instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in FreqSSD._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in FreqSSD._rprops:
            raise AttributeError("Cannot set read-only FreqSSD instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, option):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, option)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new FreqSSD object

        Parameters
        ----------
        model : Model
            Model that \*FREQUENCY_DOMAIN_SSD will be created in
        option : constant
            Specify the type of \*FREQUENCY_DOMAIN_SSD. Can be
            FreqSSD.DIRECT,
            FreqSSD.DIRECT_FD,
            FreqSSD.FATIGUE,
            FreqSSD.FRF,
            FreqSSD.ERP or
            FreqSSD.SUBCASE

        Returns
        -------
        FreqSSD
            FreqSSD object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def Create(model, modal=Oasys.gRPC.defaultArg):
        """
        Starts an interactive editing panel to create a \*FREQUENCY_DOMAIN_SSD

        Parameters
        ----------
        model : Model
            Model that the \*FREQUENCY_DOMAIN_SSD will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        FreqSSD
            FreqSSD object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def First(model):
        """
        Returns the first \*FREQUENCY_DOMAIN_SSD in the model

        Parameters
        ----------
        model : Model
            Model to get first \*FREQUENCY_DOMAIN_SSD in

        Returns
        -------
        FreqSSD
            FreqSSD object (or None if there are no \*FREQUENCY_DOMAIN_SSDs in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FlagAll(model, flag):
        """
        Flags all of the \*FREQUENCY_DOMAIN_SSDs in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all \*FREQUENCY_DOMAIN_SSDs will be flagged in
        flag : Flag
            Flag to set on the \*FREQUENCY_DOMAIN_SSDs

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of FreqSSD objects or properties for all of the \*FREQUENCY_DOMAIN_SSDs in a model in PRIMER.
        If the optional property argument is not given then a list of FreqSSD objects is returned.
        If the property argument is given, that property value for each \*FREQUENCY_DOMAIN_SSD is returned in the list
        instead of a FreqSSD object

        Parameters
        ----------
        model : Model
            Model to get \*FREQUENCY_DOMAIN_SSDs from
        property : string
            Optional. Name for property to get for all \*FREQUENCY_DOMAIN_SSDs in the model

        Returns
        -------
        list
            List of FreqSSD objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of FreqSSD objects for all of the flagged \*FREQUENCY_DOMAIN_SSDs in a model in PRIMER
        If the optional property argument is not given then a list of FreqSSD objects is returned.
        If the property argument is given, then that property value for each \*FREQUENCY_DOMAIN_SSD is returned in the list
        instead of a FreqSSD object

        Parameters
        ----------
        model : Model
            Model to get \*FREQUENCY_DOMAIN_SSDs from
        flag : Flag
            Flag set on the \*FREQUENCY_DOMAIN_SSDs that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged \*FREQUENCY_DOMAIN_SSDs in the model

        Returns
        -------
        list
            List of FreqSSD objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the FreqSSD object for a \*FREQUENCY_DOMAIN_SSD ID

        Parameters
        ----------
        model : Model
            Model to find the \*FREQUENCY_DOMAIN_SSD in
        number : integer
            number of the \*FREQUENCY_DOMAIN_SSD you want the FreqSSD object for

        Returns
        -------
        FreqSSD
            FreqSSD object (or None if \*FREQUENCY_DOMAIN_SSD does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last \*FREQUENCY_DOMAIN_SSD in the model

        Parameters
        ----------
        model : Model
            Model to get last \*FREQUENCY_DOMAIN_SSD in

        Returns
        -------
        FreqSSD
            FreqSSD object (or None if there are no \*FREQUENCY_DOMAIN_SSDs in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def Select(flag, prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg):
        """
        Allows the user to select \*FREQUENCY_DOMAIN_SSDs using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting \*FREQUENCY_DOMAIN_SSDs
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only \*FREQUENCY_DOMAIN_SSDs from that model can be selected.
            If the argument is a Flag then only \*FREQUENCY_DOMAIN_SSDs that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any \*FREQUENCY_DOMAIN_SSDs can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of \*FREQUENCY_DOMAIN_SSDs selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def Total(model, exists=Oasys.gRPC.defaultArg):
        """
        Returns the total number of \*FREQUENCY_DOMAIN_SSDs in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing \*FREQUENCY_DOMAIN_SSDs should be counted. If false or omitted
            referenced but undefined \*FREQUENCY_DOMAIN_SSDs will also be included in the total

        Returns
        -------
        int
            number of \*FREQUENCY_DOMAIN_SSDs
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the \*FREQUENCY_DOMAIN_SSDs in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all \*FREQUENCY_DOMAIN_SSDs will be unset in
        flag : Flag
            Flag to unset on the \*FREQUENCY_DOMAIN_SSDs

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)



# Instance methods
    def AddLoadData(self):
        """
        Allows user to add a new load card in \*FREQUENCY_DOMAIN_SSD. This method is only applicable when option is
        not FreqSSD.SUBCASE.
        The new card has uninitialised fields and should be updated by 
        FreqSSD.SetLoadData().

        Returns
        -------
        integer
            Index of the new load
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AddLoadData")

    def AddSubcaseData(self):
        """
        Allows user to add new subcase cards in \*FREQUENCY_DOMAIN_SSD. This method is only applicable when option is
        FreqSSD.SUBCASE.
        The new cards have uninitialised fields and should be updated by 
        FreqSSD.SetSubcaseData().

        Returns
        -------
        integer
            Index of the new subcase
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AddSubcaseData")

    def AssociateComment(self, comment):
        """
        Associates a comment with a \*FREQUENCY_DOMAIN_SSD

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the \*FREQUENCY_DOMAIN_SSD

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
        Clears a flag on the \*FREQUENCY_DOMAIN_SSD

        Parameters
        ----------
        flag : Flag
            Flag to clear on the \*FREQUENCY_DOMAIN_SSD

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the \*FREQUENCY_DOMAIN_SSD. The target include of the copied \*FREQUENCY_DOMAIN_SSD can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        FreqSSD
            FreqSSD object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a \*FREQUENCY_DOMAIN_SSD

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the \*FREQUENCY_DOMAIN_SSD

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
        Checks if the \*FREQUENCY_DOMAIN_SSD is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the \*FREQUENCY_DOMAIN_SSD

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a \*FREQUENCY_DOMAIN_SSD

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetErpData(self, index):
        """
        Returns the ERP data for a specific ERP part as a list. For each ERP part there will be 2 values. 
        There are nerp ERP parts. This method is only applicable when option is
        FreqSSD.ERP.

        Parameters
        ----------
        index : integer
            Index you want the ERP data for. Note that indices start at 0

        Returns
        -------
        list
            A list containing the ERP data (values: pid[integer], ptyp[integer]). The list length will be 2
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetErpData", index)

    def GetLoadData(self, index):
        """
        Returns the data for a specific excitation load as a list. For each load there will be 8
        values. There can be as many loads as needed. This method is only applicable when option is
        not FreqSSD.SUBCASE.

        Parameters
        ----------
        index : integer
            Index you want the load data for. Note that indices start at 0

        Returns
        -------
        int
            An list containing the load data (values: nid[integer], ntyp[integer], dof[integer], vad[integer], lc1[integer], lc2[integer], sf[real], vid[integer]). The list length will be 8.
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetLoadData", index)

    def GetParameter(self, prop):
        """
        Checks if a FreqSSD property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the FreqSSD.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            \*FREQUENCY_DOMAIN_SSD property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def GetSubcaseData(self, index):
        """
        Returns the data for a specific subcase as a list. For each subcase there will be 3 +
        8 x nload values. There can be as many subcases as needed. This method is only applicable when option is
        FreqSSD.SUBCASE.

        Parameters
        ----------
        index : integer
            Index you want the subcase data for. Note that indices start at 0

        Returns
        -------
        int
            An list containing the subcase data (values: caseid[string], title[string], nload[integer], nid[integer], ntyp[integer], dof[integer], vad[integer], lc1[integer], lc2[integer], sf[real], vid[integer], ...)  Where values nid to vid are repeated nload times in the list. The list length will be 3 + 8 x nload.
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetSubcaseData", index)

    def Keyword(self):
        """
        Returns the keyword for this \*FREQUENCY_DOMAIN_SSD.
        Note that a carriage return is not added.
        See also FreqSSD.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the \*FREQUENCY_DOMAIN_SSD.
        Note that a carriage return is not added.
        See also FreqSSD.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next \*FREQUENCY_DOMAIN_SSD in the model

        Returns
        -------
        FreqSSD
            FreqSSD object (or None if there are no more \*FREQUENCY_DOMAIN_SSDs in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous \*FREQUENCY_DOMAIN_SSD in the model

        Returns
        -------
        FreqSSD
            FreqSSD object (or None if there are no more \*FREQUENCY_DOMAIN_SSDs in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def RemoveLoadData(self, index):
        """
        Allows user to remove a specified load card in \*FREQUENCY_DOMAIN_SSD.
        This method is only applicable when option is not
        FreqSSD.SUBCASE.

        Parameters
        ----------
        index : integer
            Index of the load card you want to remove. Note that indices start at 0

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "RemoveLoadData", index)

    def RemoveSubcaseData(self, index):
        """
        Allows user to remove cards for a specified subcase in \*FREQUENCY_DOMAIN_SSD.
        This method is only applicable when option is FreqSSD.SUBCASE.

        Parameters
        ----------
        index : integer
            Index of the subcase you want to remove cards for. Note that indices start at 0

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "RemoveSubcaseData", index)

    def SetErpData(self, index, data):
        """
        Set the data for a specific ERP part. For each ERP part there will be 2 values. 
        There are nerp ERP parts. This method is only applicable when option is
        FreqSSD.ERP.

        Parameters
        ----------
        index : integer
            Index you want to set ERP data for. Note that indices start at 0
        data : List of data
            An list containing the ERP data (values: pid[integer], ptyp[integer]). The list length should be 2

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetErpData", index, data)

    def SetFlag(self, flag):
        """
        Sets a flag on the \*FREQUENCY_DOMAIN_SSD

        Parameters
        ----------
        flag : Flag
            Flag to set on the \*FREQUENCY_DOMAIN_SSD

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def SetLoadData(self, index, data):
        """
        Set the data for a specific excitation load. For each load there will be 8 values. 
        There can be as many loads as needed. This method is only applicable when option is
        not FreqSSD.SUBCASE.

        Parameters
        ----------
        index : integer
            Index you want to set load data for. Note that indices start at 0
        data : List of data
            An list containing the load data (values: nid[integer], ntyp[integer], dof[integer], vad[integer],
            lc1[integer], lc2[integer], sf[real], vid[integer]). The list length should be 8.

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetLoadData", index, data)

    def SetSubcaseData(self, index, caseid, title, nload, data):
        """
        Set the data for a specific subcase. For each subcase, data will have 8 x nload values.
        There can be as many subcases as needed. This method is only applicable when option is
        FreqSSD.SUBCASE.

        Parameters
        ----------
        index : integer
            Index you want to set subcase data for. Note that indices start at 0
        caseid : string
            Identification string to be used as the case ID (must include at least one letter)
        title : string
            A description of the current loading case (can be blank)
        nload : integer
            Number of loads for this loading case
        data : List of data
            An list containing the subcase load data (values: nid[integer],
            ntyp[integer], dof[integer], vad[integer], lc1[integer], lc2[integer], sf[real], vid[integer], ...) 
            Where values nid to vid are repeated nload times in the list. The list length should be 8 x nload.

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetSubcaseData", index, caseid, title, nload, data)

    def ViewParameters(self):
        """
        Object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. This function temporarily
        changes the behaviour so that if a property is a parameter the parameter name is returned instead.
        This can be used with 'method chaining' (see the example below) to make sure a property argument is correct

        Returns
        -------
        FreqSSD
            FreqSSD object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this \*FREQUENCY_DOMAIN_SSD

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

