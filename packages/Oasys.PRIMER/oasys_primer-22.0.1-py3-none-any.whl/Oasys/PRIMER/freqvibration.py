import Oasys.gRPC


# Metaclass for static properties and constants
class FreqVibrationType(type):
    _consts = {'FATIGUE', 'VIBRATION'}

    def __getattr__(cls, name):
        if name in FreqVibrationType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("FreqVibration class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in FreqVibrationType._consts:
            raise AttributeError("Cannot set FreqVibration class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class FreqVibration(Oasys.gRPC.OasysItem, metaclass=FreqVibrationType):
    _props = {'dampf', 'dmpmas', 'dmpstf', 'dmptyp', 'fnmax', 'fnmin', 'icoarse', 'include', 'inftg', 'ipanelu', 'ipanelv', 'lcdam', 'lctyp', 'ldflag', 'ldtyp', 'mdmax', 'mdmin', 'method', 'mftg', 'napsd', 'ncpsd', 'nftg', 'option', 'pref', 'restrm', 'restrt', 'strsf', 'strtyp', 'tcoarse', 'temper', 'texpos', 'umlt', 'unit', 'vaflag', 'vapsd', 'varms'}
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
        if name in FreqVibration._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in FreqVibration._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("FreqVibration instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in FreqVibration._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in FreqVibration._rprops:
            raise AttributeError("Cannot set read-only FreqVibration instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, option):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, option)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new FreqVibration object

        Parameters
        ----------
        model : Model
            Model that \*FREQUENCY_DOMAIN_RANDOM_VIBRATION will be created in
        option : constant
            Specify the type of \*FREQUENCY_DOMAIN_RANDOM_VIBRATION. Can be
            FreqVibration.VIBRATION,
            FreqVibration.FATIGUE

        Returns
        -------
        FreqVibration
            FreqVibration object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def Create(model, modal=Oasys.gRPC.defaultArg):
        """
        Starts an interactive editing panel to create a \*FREQUENCY_DOMAIN_RANDOM_VIBRATION

        Parameters
        ----------
        model : Model
            Model that the \*FREQUENCY_DOMAIN_RANDOM_VIBRATION will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        FreqVibration
            FreqVibration object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def First(model):
        """
        Returns the first \*FREQUENCY_DOMAIN_RANDOM_VIBRATION in the model

        Parameters
        ----------
        model : Model
            Model to get first \*FREQUENCY_DOMAIN_RANDOM_VIBRATION in

        Returns
        -------
        FreqVibration
            FreqVibration object (or None if there are no \*FREQUENCY_DOMAIN_RANDOM_VIBRATIONs in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FlagAll(model, flag):
        """
        Flags all of the \*FREQUENCY_DOMAIN_RANDOM_VIBRATIONs in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all \*FREQUENCY_DOMAIN_RANDOM_VIBRATIONs will be flagged in
        flag : Flag
            Flag to set on the \*FREQUENCY_DOMAIN_RANDOM_VIBRATIONs

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of FreqVibration objects or properties for all of the \*FREQUENCY_DOMAIN_RANDOM_VIBRATIONs in a model in PRIMER.
        If the optional property argument is not given then a list of FreqVibration objects is returned.
        If the property argument is given, that property value for each \*FREQUENCY_DOMAIN_RANDOM_VIBRATION is returned in the list
        instead of a FreqVibration object

        Parameters
        ----------
        model : Model
            Model to get \*FREQUENCY_DOMAIN_RANDOM_VIBRATIONs from
        property : string
            Optional. Name for property to get for all \*FREQUENCY_DOMAIN_RANDOM_VIBRATIONs in the model

        Returns
        -------
        list
            List of FreqVibration objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetAutoPsdLoadData(index):
        """
        Returns the Auto PSD load data for a specific Auto PSD Load definition as a list. For each Auto PSD load definition there will be 8 values. 
        There are napsd Auto PSD load definitions.

        Parameters
        ----------
        index : integer
            Index you want the Auto PSD load data for. Note that indices start at 0

        Returns
        -------
        list
            A list containing the Auto PSD load data (values: sid[integer], stype[integer], dof[integer], ldpsd[integer], ldvel[integer], ldflw[integer], ldspn[integer], cid[integer]). The list length will be 8
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetAutoPsdLoadData", index)

    def GetCrossPsdLoadData(index):
        """
        Returns the Cross PSD load data for a specific Cross PSD Load definition as a list. For each Cross PSD load definition there will be 5 values. 
        There are ncpsd Cross PSD load definitions.

        Parameters
        ----------
        index : integer
            Index you want the Cross PSD load data for. Note that indices start at 0

        Returns
        -------
        list
            A list containing the Cross PSD load data (values: load_i[integer], load_j[integer], lctyp2[integer], ldpsd1[integer], ldpsd2[integer]). The list length will be 5
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetCrossPsdLoadData", index)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of FreqVibration objects for all of the flagged \*FREQUENCY_DOMAIN_RANDOM_VIBRATIONs in a model in PRIMER
        If the optional property argument is not given then a list of FreqVibration objects is returned.
        If the property argument is given, then that property value for each \*FREQUENCY_DOMAIN_RANDOM_VIBRATION is returned in the list
        instead of a FreqVibration object

        Parameters
        ----------
        model : Model
            Model to get \*FREQUENCY_DOMAIN_RANDOM_VIBRATIONs from
        flag : Flag
            Flag set on the \*FREQUENCY_DOMAIN_RANDOM_VIBRATIONs that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged \*FREQUENCY_DOMAIN_RANDOM_VIBRATIONs in the model

        Returns
        -------
        list
            List of FreqVibration objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the FreqVibration object for a \*FREQUENCY_DOMAIN_RANDOM_VIBRATION ID

        Parameters
        ----------
        model : Model
            Model to find the \*FREQUENCY_DOMAIN_RANDOM_VIBRATION in
        number : integer
            number of the \*FREQUENCY_DOMAIN_RANDOM_VIBRATION you want the FreqVibration object for

        Returns
        -------
        FreqVibration
            FreqVibration object (or None if \*FREQUENCY_DOMAIN_RANDOM_VIBRATION does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def GetInftgData(index):
        """
        Returns the path and filename of a binary database for fatigue information from a specific initial damage card. There are 
        inftg filenames. This method is only applicable when option is
        FreqVibration.FATIGUE.

        Parameters
        ----------
        index : integer
            Index of an initial damage card that you want the filename from. Note that indices start at 0

        Returns
        -------
        str
            Return value from an initial damage card (values: filename[string])
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetInftgData", index)

    def GetSNCurveData(index):
        """
        Returns the data of a specific zone for fatigue analysis as a list. For each zone there will be 8
        values. There are nftg zone definitions for fatigue analysis. This method is only applicable when option is
        FreqVibration.FATIGUE.

        Parameters
        ----------
        index : integer
            Index you want the zone data for. Note that indices start at 0

        Returns
        -------
        int
            An list containing the zone data (values: pid[integer], lcid[integer], ptype[integer], ltype[integer], a[float], b[float], sthres[float], snlimt[integer]). The list length will be 8.
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetSNCurveData", index)

    def Last(model):
        """
        Returns the last \*FREQUENCY_DOMAIN_RANDOM_VIBRATION in the model

        Parameters
        ----------
        model : Model
            Model to get last \*FREQUENCY_DOMAIN_RANDOM_VIBRATION in

        Returns
        -------
        FreqVibration
            FreqVibration object (or None if there are no \*FREQUENCY_DOMAIN_RANDOM_VIBRATIONs in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def Select(flag, prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg):
        """
        Allows the user to select \*FREQUENCY_DOMAIN_RANDOM_VIBRATIONs using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting \*FREQUENCY_DOMAIN_RANDOM_VIBRATIONs
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only \*FREQUENCY_DOMAIN_RANDOM_VIBRATIONs from that model can be selected.
            If the argument is a Flag then only \*FREQUENCY_DOMAIN_RANDOM_VIBRATIONs that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any \*FREQUENCY_DOMAIN_RANDOM_VIBRATIONs can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of \*FREQUENCY_DOMAIN_RANDOM_VIBRATIONs selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SetAutoPsdLoadData(index, data):
        """
        Set the data for a specific Auto PSD load card. For each Auto PSD load card there will be 8 values. 
        There are napsd Auto PSD load cards.

        Parameters
        ----------
        index : integer
            Index you want to set Auto PSD load data for. Note that indices start at 0
        data : List of data
            An list containing the Auto PSD load data (values: sid[integer], stype[integer], dof[integer], ldpsd[integer], ldvel[integer], ldflw[integer],
            ldspn[integer], cid[integer]). The list length should be 8

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "SetAutoPsdLoadData", index, data)

    def SetCrossPsdLoadData(index, data):
        """
        Set the data for a specific Cross PSD load card. For each Cross PSD load card there will be 5 values. 
        There are ncpsd Cross PSD load cards.

        Parameters
        ----------
        index : integer
            Index you want to set Cross PSD load data for. Note that indices start at 0
        data : List of data
            An list containing the Cross PSD load data (values: load_i[integer], load_j[integer], lctyp2[integer], ldpsd1[integer], ldpsd2[integer]). 
            The list length should be 5

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "SetCrossPsdLoadData", index, data)

    def SetInftgData(index, filename):
        """
        Set the filename data for an existing binary database for fatigue infromation for a specific initial damage card. There are 
        inftg filenames. This method is only applicable when option is
        FreqVibration.FATIGUE.

        Parameters
        ----------
        index : integer
            Index of an initial damage card that you want the filename for. Note that indices start at 0
        filename : string
            Path and name of existing binary database fro fatigue information

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "SetInftgData", index, filename)

    def SetSNCurveData(index, data):
        """
        Set the data for a specific zone for fatigue analysis. For each zone there will be 8 values. 
        There are nftg zone definitions for fatigue analysis. This method is only applicable when option is
        FreqVibration.FATIGUE

        Parameters
        ----------
        index : integer
            Index you want to set the fatigue analysis zone data for. Note that indices start at 0
        data : List of data
            An list containing the zone data (values: pid[integer], lcid[integer], ptype[integer], ltype[integer],
            a[float], b[float], sthres[float], snlimt[integer]). The list length will be 8

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "SetSNCurveData", index, data)

    def Total(model, exists=Oasys.gRPC.defaultArg):
        """
        Returns the total number of \*FREQUENCY_DOMAIN_RANDOM_VIBRATIONs in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing \*FREQUENCY_DOMAIN_RANDOM_VIBRATIONs should be counted. If false or omitted
            referenced but undefined \*FREQUENCY_DOMAIN_RANDOM_VIBRATIONs will also be included in the total

        Returns
        -------
        int
            number of \*FREQUENCY_DOMAIN_RANDOM_VIBRATIONs
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the \*FREQUENCY_DOMAIN_RANDOM_VIBRATIONs in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all \*FREQUENCY_DOMAIN_RANDOM_VIBRATIONs will be unset in
        flag : Flag
            Flag to unset on the \*FREQUENCY_DOMAIN_RANDOM_VIBRATIONs

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)



# Instance methods
    def AddAutoPsdLoadData(self):
        """
        Allows user to add a new Auto PSD load card in \*FREQUENCY_DOMAIN_RANDOM_VIBRATION.
        The new card has uninitialised fields and should be updated by 
        FreqVibration.SetAutoPsdLoadData().

        Returns
        -------
        integer
            Index of the new auto PSD load
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AddAutoPsdLoadData")

    def AddCrossPsdLoadData(self):
        """
        Allows user to add a new Cross PSD load card in \*FREQUENCY_DOMAIN_RANDOM_VIBRATION.
        The new card has uninitialised fields and should be updated by 
        FreqVibration.SetCrossPsdLoadData().

        Returns
        -------
        integer
            Index of the new cross PSD load
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AddCrossPsdLoadData")

    def AddInftgData(self):
        """
        Allows user to add new Initial Damage cards in \*FREQUENCY_DOMAIN_RANDOM_VIBRATION. This method is only applicable when option is
        FreqVibration.FATIGUE.
        The new cards have uninitialised fields and should be updated by 
        FreqVibration.SetInftgData().

        Returns
        -------
        integer
            Index of the new initial damage card
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AddInftgData")

    def AddSNCurveData(self):
        """
        Allows user to add new S-N curve cards in \*FREQUENCY_DOMAIN_RANDOM_VIBRATION. This method is only applicable when option is
        FreqVibration.FATIGUE.
        The new cards have uninitialised fields and should be updated by 
        FreqVibration.SetSNCurveData().

        Returns
        -------
        integer
            Index of the new S-N curve card
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AddSNCurveData")

    def AssociateComment(self, comment):
        """
        Associates a comment with a \*FREQUENCY_DOMAIN_RANDOM_VIBRATION

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the \*FREQUENCY_DOMAIN_RANDOM_VIBRATION

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
        Clears a flag on the \*FREQUENCY_DOMAIN_RANDOM_VIBRATION

        Parameters
        ----------
        flag : Flag
            Flag to clear on the \*FREQUENCY_DOMAIN_RANDOM_VIBRATION

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the \*FREQUENCY_DOMAIN_RANDOM_VIBRATION. The target include of the copied \*FREQUENCY_DOMAIN_RANDOM_VIBRATION can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        FreqVibration
            FreqVibration object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a \*FREQUENCY_DOMAIN_RANDOM_VIBRATION

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the \*FREQUENCY_DOMAIN_RANDOM_VIBRATION

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
        Checks if the \*FREQUENCY_DOMAIN_RANDOM_VIBRATION is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the \*FREQUENCY_DOMAIN_RANDOM_VIBRATION

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a \*FREQUENCY_DOMAIN_RANDOM_VIBRATION

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a FreqVibration property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the FreqVibration.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            \*FREQUENCY_DOMAIN_RANDOM_VIBRATION property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this \*FREQUENCY_DOMAIN_RANDOM_VIBRATION.
        Note that a carriage return is not added.
        See also FreqVibration.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the \*FREQUENCY_DOMAIN_RANDOM_VIBRATION.
        Note that a carriage return is not added.
        See also FreqVibration.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next \*FREQUENCY_DOMAIN_RANDOM_VIBRATION in the model

        Returns
        -------
        FreqVibration
            FreqVibration object (or None if there are no more \*FREQUENCY_DOMAIN_RANDOM_VIBRATIONs in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous \*FREQUENCY_DOMAIN_RANDOM_VIBRATION in the model

        Returns
        -------
        FreqVibration
            FreqVibration object (or None if there are no more \*FREQUENCY_DOMAIN_RANDOM_VIBRATIONs in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def RemoveAutoPsdLoadData(self, index):
        """
        Allows user to remove a specified Auto PSD load card in \*FREQUENCY_DOMAIN_RANDOM_VIBRATION.

        Parameters
        ----------
        index : integer
            Index of the auto PSD load card you want to remove. Note that indices start at 0

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "RemoveAutoPsdLoadData", index)

    def RemoveCrossPsdLoadData(self, index):
        """
        Allows user to remove a specified Cross PSD load card in \*FREQUENCY_DOMAIN_RANDOM_VIBRATION.

        Parameters
        ----------
        index : integer
            Index of the cross PSD load card you want to remove. Note that indices start at 0

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "RemoveCrossPsdLoadData", index)

    def RemoveInftgData(self, index):
        """
        Allows user to remove a specified Initial Damage card in \*FREQUENCY_DOMAIN_RANDOM_VIBRATION.
        This method is only applicable when option is FreqVibration.FATIGUE.

        Parameters
        ----------
        index : integer
            Index of the Initrial Damage card you want to remove. Note that indices start at 0

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "RemoveInftgData", index)

    def RemoveSNCurveData(self, index):
        """
        Allows user to remove a specified S-N curve card in \*FREQUENCY_DOMAIN_RANDOM_VIBRATION.
        This method is only applicable when option is FreqVibration.FATIGUE.

        Parameters
        ----------
        index : integer
            Index of the S-N curve card you want to remove. Note that indices start at 0

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "RemoveSNCurveData", index)

    def SetFlag(self, flag):
        """
        Sets a flag on the \*FREQUENCY_DOMAIN_RANDOM_VIBRATION

        Parameters
        ----------
        flag : Flag
            Flag to set on the \*FREQUENCY_DOMAIN_RANDOM_VIBRATION

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
        FreqVibration
            FreqVibration object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this \*FREQUENCY_DOMAIN_RANDOM_VIBRATION

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

