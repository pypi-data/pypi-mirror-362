import Oasys.gRPC


# Metaclass for static properties and constants
class SensorSwitchType(type):
    _consts = {'SWITCH', 'SWITCH_CALC_LOGIC', 'SWITCH_SHELL_TO_VENT'}

    def __getattr__(cls, name):
        if name in SensorSwitchType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("SensorSwitch class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in SensorSwitchType._consts:
            raise AttributeError("Cannot set SensorSwitch class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class SensorSwitch(Oasys.gRPC.OasysItem, metaclass=SensorSwitchType):
    _props = {'abid', 'amax', 'c23', 'filtrid', 'id', 'id_flag', 'include', 'itype', 'label', 'logic', 'nrow', 'option', 'sensid', 'switid', 'timwin', 'title', 'value'}
    _rprops = {'exists', 'model', 'nswit'}


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
        if name in SensorSwitch._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in SensorSwitch._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("SensorSwitch instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in SensorSwitch._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in SensorSwitch._rprops:
            raise AttributeError("Cannot set read-only SensorSwitch instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, option, model, switch_id):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, option, model, switch_id)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new SensorSwitch object

        Parameters
        ----------
        option : constant
            SENSOR_SWITCH suffix. Can be SensorSwitch.SWITCH,
            SensorSwitch.SWITCH_CALC_LOGIC or
            SensorSwitch.SWITCH_SHELL_TO_VENT
        model : Model
            Model that \*SENSOR_SWITCH will be created in
        switch_id : integer
            SensorSwitch id. This is required for the
            SensorSwitch.SWITCH and
            SensorSwitch.SWITCH_CALC_LOGIC options and ignored for
            SensorSwitch.SWITCH_SHELL_TO_VENT

        Returns
        -------
        SensorSwitch
            SensorSwitch object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def Create(model, modal=Oasys.gRPC.defaultArg):
        """
        Starts an interactive editing panel to create a \*SENSOR_SWITCH

        Parameters
        ----------
        model : Model
            Model that the \*SENSOR_SWITCH will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        SensorSwitch
            SensorSwitch object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def First(model):
        """
        Returns the first \*SENSOR_SWITCH in the model

        Parameters
        ----------
        model : Model
            Model to get first \*SENSOR_SWITCH in

        Returns
        -------
        SensorSwitch
            SensorSwitch object (or None if there are no \*SENSOR_SWITCHs in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FirstFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the first free \*SENSOR_SWITCH label in the model.
        Also see SensorSwitch.LastFreeLabel(),
        SensorSwitch.NextFreeLabel() and
        Model.FirstFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get first free \*SENSOR_SWITCH label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            First free in layer in editing panels). If omitted the whole model will be used (Equivalent to
            First free in editing panels)

        Returns
        -------
        int
            SensorSwitch label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FirstFreeLabel", model, layer)

    def FlagAll(model, flag):
        """
        Flags all of the \*SENSOR_SWITCHs in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all \*SENSOR_SWITCHs will be flagged in
        flag : Flag
            Flag to set on the \*SENSOR_SWITCHs

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of SensorSwitch objects or properties for all of the \*SENSOR_SWITCHs in a model in PRIMER.
        If the optional property argument is not given then a list of SensorSwitch objects is returned.
        If the property argument is given, that property value for each \*SENSOR_SWITCH is returned in the list
        instead of a SensorSwitch object

        Parameters
        ----------
        model : Model
            Model to get \*SENSOR_SWITCHs from
        property : string
            Optional. Name for property to get for all \*SENSOR_SWITCHs in the model

        Returns
        -------
        list
            List of SensorSwitch objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of SensorSwitch objects for all of the flagged \*SENSOR_SWITCHs in a model in PRIMER
        If the optional property argument is not given then a list of SensorSwitch objects is returned.
        If the property argument is given, then that property value for each \*SENSOR_SWITCH is returned in the list
        instead of a SensorSwitch object

        Parameters
        ----------
        model : Model
            Model to get \*SENSOR_SWITCHs from
        flag : Flag
            Flag set on the \*SENSOR_SWITCHs that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged \*SENSOR_SWITCHs in the model

        Returns
        -------
        list
            List of SensorSwitch objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the SensorSwitch object for a \*SENSOR_SWITCH ID

        Parameters
        ----------
        model : Model
            Model to find the \*SENSOR_SWITCH in
        number : integer
            number of the \*SENSOR_SWITCH you want the SensorSwitch object for

        Returns
        -------
        SensorSwitch
            SensorSwitch object (or None if \*SENSOR_SWITCH does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last \*SENSOR_SWITCH in the model

        Parameters
        ----------
        model : Model
            Model to get last \*SENSOR_SWITCH in

        Returns
        -------
        SensorSwitch
            SensorSwitch object (or None if there are no \*SENSOR_SWITCHs in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def LastFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the last free \*SENSOR_SWITCH label in the model.
        Also see SensorSwitch.FirstFreeLabel(),
        SensorSwitch.NextFreeLabel() and
        see Model.LastFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get last free \*SENSOR_SWITCH label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest free in layer in editing panels). If omitted the whole model will be used

        Returns
        -------
        int
            SensorSwitch label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "LastFreeLabel", model, layer)

    def NextFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the next free (highest+1) \*SENSOR_SWITCH label in the model.
        Also see SensorSwitch.FirstFreeLabel(),
        SensorSwitch.LastFreeLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get next free \*SENSOR_SWITCH label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest+1 in layer in editing panels). If omitted the whole model will be used (Equivalent to
            Highest+1 in editing panels)

        Returns
        -------
        int
            SensorSwitch label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NextFreeLabel", model, layer)

    def RenumberAll(model, start):
        """
        Renumbers all of the \*SENSOR_SWITCHs in the model

        Parameters
        ----------
        model : Model
            Model that all \*SENSOR_SWITCHs will be renumbered in
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
        Renumbers all of the flagged \*SENSOR_SWITCHs in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged \*SENSOR_SWITCHs will be renumbered in
        flag : Flag
            Flag set on the \*SENSOR_SWITCHs that you want to renumber
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
        Allows the user to select \*SENSOR_SWITCHs using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting \*SENSOR_SWITCHs
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only \*SENSOR_SWITCHs from that model can be selected.
            If the argument is a Flag then only \*SENSOR_SWITCHs that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any \*SENSOR_SWITCHs can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of \*SENSOR_SWITCHs selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def Total(model, exists=Oasys.gRPC.defaultArg):
        """
        Returns the total number of \*SENSOR_SWITCHs in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing \*SENSOR_SWITCHs should be counted. If false or omitted
            referenced but undefined \*SENSOR_SWITCHs will also be included in the total

        Returns
        -------
        int
            number of \*SENSOR_SWITCHs
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the \*SENSOR_SWITCHs in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all \*SENSOR_SWITCHs will be unset in
        flag : Flag
            Flag to unset on the \*SENSOR_SWITCHs

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)



# Instance methods
    def AssociateComment(self, comment):
        """
        Associates a comment with a \*SENSOR_SWITCH

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the \*SENSOR_SWITCH

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
        Clears a flag on the \*SENSOR_SWITCH

        Parameters
        ----------
        flag : Flag
            Flag to clear on the \*SENSOR_SWITCH

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the \*SENSOR_SWITCH. The target include of the copied \*SENSOR_SWITCH can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        SensorSwitch
            SensorSwitch object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a \*SENSOR_SWITCH

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the \*SENSOR_SWITCH

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
        Checks if the \*SENSOR_SWITCH is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the \*SENSOR_SWITCH

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a \*SENSOR_SWITCH

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a SensorSwitch property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the SensorSwitch.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            \*SENSOR_SWITCH property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def GetRow(self, row):
        """
        Returns the data for a row in the SENSOR_SWITCH_SHELL_TO_VENT

        Parameters
        ----------
        row : integer
            The row you want the data for. Note row indices start at 0

        Returns
        -------
        list
            A list of numbers containing the row variables SSID, FTIME and C23V
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetRow", row)

    def GetSwitch(self, row):
        """
        Returns switch ID information for \*SENSOR_SWITCH_CALC-LOGIC

        Parameters
        ----------
        row : integer
            The row you want the data for. Note row indices start at 0

        Returns
        -------
        dict
            Dict containing sensor switch ID information
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetSwitch", row)

    def Keyword(self):
        """
        Returns the keyword for this \*SENSOR_SWITCH.
        Note that a carriage return is not added.
        See also SensorSwitch.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the \*SENSOR_SWITCH.
        Note that a carriage return is not added.
        See also SensorSwitch.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next \*SENSOR_SWITCH in the model

        Returns
        -------
        SensorSwitch
            SensorSwitch object (or None if there are no more \*SENSOR_SWITCHs in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous \*SENSOR_SWITCH in the model

        Returns
        -------
        SensorSwitch
            SensorSwitch object (or None if there are no more \*SENSOR_SWITCHs in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def RemoveRow(self, row):
        """
        Removes the data for a row in \*SENSOR_SWITCH_SHELL_TO_VENT

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

    def RemoveSwitch(self, row):
        """
        Removes sensor switch ID from \*SENSOR_SWITCH_CALC-LOGIC

        Parameters
        ----------
        row : integer
            The sensor switch ID that you want to remove.
            Note that row indices start at 0

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "RemoveSwitch", row)

    def SetFlag(self, flag):
        """
        Sets a flag on the \*SENSOR_SWITCH

        Parameters
        ----------
        flag : Flag
            Flag to set on the \*SENSOR_SWITCH

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def SetRow(self, row, data):
        """
        Sets the data for a row in \*SENSOR_SWITCH_SHELL_TO_VENT

        Parameters
        ----------
        row : integer
            The row you want to set the data for.
            Note that row indices start at 0
        data : List of data
            An list containing the row variables SSID, FTIME and C23V

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetRow", row, data)

    def SetSwitch(self, index, data):
        """
        Specifies a sensor switch ID for a \*SENSOR_SWITCH_CALC-LOGIC

        Parameters
        ----------
        index : integer
            The index of the \*SENSOR_SWITCH_CALC-LOGIC data to set. Note that indices start at 0, not 1.
            0 <= index <= nswit
        data : dict
            Object containing sensor swith ID data

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetSwitch", index, data)

    def ViewParameters(self):
        """
        Object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. This function temporarily
        changes the behaviour so that if a property is a parameter the parameter name is returned instead.
        This can be used with 'method chaining' (see the example below) to make sure a property argument is correct

        Returns
        -------
        SensorSwitch
            SensorSwitch object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this \*SENSOR_SWITCH

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

