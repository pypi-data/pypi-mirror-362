import Oasys.gRPC


# Metaclass for static properties and constants
class SensorDefineType(type):
    _consts = {'DEFINE_CALC_MATH', 'DEFINE_ELEMENT', 'DEFINE_ELEMENT_SET', 'DEFINE_FORCE', 'DEFINE_FUNCTION', 'DEFINE_MISC', 'DEFINE_NODE', 'DEFINE_NODE_SET'}

    def __getattr__(cls, name):
        if name in SensorDefineType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("SensorDefine class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in SensorDefineType._consts:
            raise AttributeError("Cannot set SensorDefine class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class SensorDefine(Oasys.gRPC.OasysItem, metaclass=SensorDefineType):
    _props = {'calc', 'comp', 'crd', 'ctype', 'elemid', 'etype', 'ftype', 'func', 'func_sens1', 'func_sens10', 'func_sens11', 'func_sens12', 'func_sens13', 'func_sens14', 'func_sens15', 'func_sens16', 'func_sens2', 'func_sens3', 'func_sens4', 'func_sens5', 'func_sens6', 'func_sens7', 'func_sens8', 'func_sens9', 'i0', 'i1', 'i2', 'i3', 'i4', 'i5', 'include', 'label', 'layer', 'mtype', 'node1', 'node2', 'option', 'pwr', 'sens1', 'sens2', 'sens3', 'sens4', 'sens5', 'sens6', 'sensid', 'setopt', 'sf', 'typeid', 'vid'}
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
        if name in SensorDefine._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in SensorDefine._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("SensorDefine instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in SensorDefine._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in SensorDefine._rprops:
            raise AttributeError("Cannot set read-only SensorDefine instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, option, model, define_id, type_or_entity_1, entity_2):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, option, model, define_id, type_or_entity_1, entity_2)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new SensorDefine object

        Parameters
        ----------
        option : constant
            SENSOR_DEFINE suffix. Can be SensorDefine.DEFINE_CALC_MATH,
            SensorDefine.DEFINE_ELEMENT,
            SensorDefine.DEFINE_ELEMENT_SET,
            SensorDefine.DEFINE_FORCE,
            SensorDefine.DEFINE_MISC,
            SensorDefine.DEFINE_NODE,
            SensorDefine.DEFINE_NODE_SET or
            SensorDefine.DEFINE_FUNCTION
        model : Model
            Model that \*SENSOR_DEFINE will be created in
        define_id : integer
            SensorDefine id
        type_or_entity_1 : string/label
            For SensorDefine.DEFINE_NODE, SensorDefine.DEFINE_NODE_SET option it is Node ID or NODE set ID respectively,
            For SensorDefine.DEFINE_FUNCTION option it is DEFINE_FUNCTION ID,
            For SensorDefine.DEFINE_CALC_MATH option it is Calc string, 
            For SensorDefine.DEFINE_ELEMENT and SensorDefine.DEFINE_ELEMENT_SET option it is Etype string, 
            For SensorDefine.DEFINE_FORCE option it is Ftype string, 
            For SensorDefine.DEFINE_MISC option it is Mtype string
        entity_2 : label
            Applicable only for SensorDefine.DEFINE_NODE, 
            SensorDefine.DEFINE_NODE_SET, 
            SensorDefine.DEFINE_CALC_MATH, 
            SensorDefine.DEFINE_ELEMENT, 
            SensorDefine.DEFINE_ELEMENT_SET or 
            SensorDefine.DEFINE_FORCE.
            It is NODE or NODE set ID for SensorDefine.DEFINE_NODE or SensorDefine.DEFINE_NODE_SET respectively,
            Sensor Define ID for SensorDefine.DEFINE_CALC_MATH,
            Element ID or Element set ID for SensorDefine.DEFINE_ELEMENT or SensorDefine.DEFINE_ELEMENT_SET respectively or
            Type ID for SensorDefine.DEFINE_FORCE

        Returns
        -------
        SensorDefine
            SensorDefine object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def Create(model, modal=Oasys.gRPC.defaultArg):
        """
        Starts an interactive editing panel to create a \*SENSOR_DEFINE

        Parameters
        ----------
        model : Model
            Model that the \*SENSOR_DEFINE will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        SensorDefine
            SensorDefine object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def First(model):
        """
        Returns the first \*SENSOR_DEFINE in the model

        Parameters
        ----------
        model : Model
            Model to get first \*SENSOR_DEFINE in

        Returns
        -------
        SensorDefine
            SensorDefine object (or None if there are no \*SENSOR_DEFINEs in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FirstFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the first free \*SENSOR_DEFINE label in the model.
        Also see SensorDefine.LastFreeLabel(),
        SensorDefine.NextFreeLabel() and
        Model.FirstFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get first free \*SENSOR_DEFINE label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            First free in layer in editing panels). If omitted the whole model will be used (Equivalent to
            First free in editing panels)

        Returns
        -------
        int
            SensorDefine label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FirstFreeLabel", model, layer)

    def FlagAll(model, flag):
        """
        Flags all of the \*SENSOR_DEFINEs in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all \*SENSOR_DEFINEs will be flagged in
        flag : Flag
            Flag to set on the \*SENSOR_DEFINEs

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of SensorDefine objects or properties for all of the \*SENSOR_DEFINEs in a model in PRIMER.
        If the optional property argument is not given then a list of SensorDefine objects is returned.
        If the property argument is given, that property value for each \*SENSOR_DEFINE is returned in the list
        instead of a SensorDefine object

        Parameters
        ----------
        model : Model
            Model to get \*SENSOR_DEFINEs from
        property : string
            Optional. Name for property to get for all \*SENSOR_DEFINEs in the model

        Returns
        -------
        list
            List of SensorDefine objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of SensorDefine objects for all of the flagged \*SENSOR_DEFINEs in a model in PRIMER
        If the optional property argument is not given then a list of SensorDefine objects is returned.
        If the property argument is given, then that property value for each \*SENSOR_DEFINE is returned in the list
        instead of a SensorDefine object

        Parameters
        ----------
        model : Model
            Model to get \*SENSOR_DEFINEs from
        flag : Flag
            Flag set on the \*SENSOR_DEFINEs that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged \*SENSOR_DEFINEs in the model

        Returns
        -------
        list
            List of SensorDefine objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the SensorDefine object for a \*SENSOR_DEFINE ID

        Parameters
        ----------
        model : Model
            Model to find the \*SENSOR_DEFINE in
        number : integer
            number of the \*SENSOR_DEFINE you want the SensorDefine object for

        Returns
        -------
        SensorDefine
            SensorDefine object (or None if \*SENSOR_DEFINE does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last \*SENSOR_DEFINE in the model

        Parameters
        ----------
        model : Model
            Model to get last \*SENSOR_DEFINE in

        Returns
        -------
        SensorDefine
            SensorDefine object (or None if there are no \*SENSOR_DEFINEs in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def LastFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the last free \*SENSOR_DEFINE label in the model.
        Also see SensorDefine.FirstFreeLabel(),
        SensorDefine.NextFreeLabel() and
        see Model.LastFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get last free \*SENSOR_DEFINE label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest free in layer in editing panels). If omitted the whole model will be used

        Returns
        -------
        int
            SensorDefine label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "LastFreeLabel", model, layer)

    def NextFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the next free (highest+1) \*SENSOR_DEFINE label in the model.
        Also see SensorDefine.FirstFreeLabel(),
        SensorDefine.LastFreeLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get next free \*SENSOR_DEFINE label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest+1 in layer in editing panels). If omitted the whole model will be used (Equivalent to
            Highest+1 in editing panels)

        Returns
        -------
        int
            SensorDefine label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NextFreeLabel", model, layer)

    def RenumberAll(model, start):
        """
        Renumbers all of the \*SENSOR_DEFINEs in the model

        Parameters
        ----------
        model : Model
            Model that all \*SENSOR_DEFINEs will be renumbered in
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
        Renumbers all of the flagged \*SENSOR_DEFINEs in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged \*SENSOR_DEFINEs will be renumbered in
        flag : Flag
            Flag set on the \*SENSOR_DEFINEs that you want to renumber
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
        Allows the user to select \*SENSOR_DEFINEs using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting \*SENSOR_DEFINEs
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only \*SENSOR_DEFINEs from that model can be selected.
            If the argument is a Flag then only \*SENSOR_DEFINEs that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any \*SENSOR_DEFINEs can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of \*SENSOR_DEFINEs selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def Total(model, exists=Oasys.gRPC.defaultArg):
        """
        Returns the total number of \*SENSOR_DEFINEs in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing \*SENSOR_DEFINEs should be counted. If false or omitted
            referenced but undefined \*SENSOR_DEFINEs will also be included in the total

        Returns
        -------
        int
            number of \*SENSOR_DEFINEs
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the \*SENSOR_DEFINEs in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all \*SENSOR_DEFINEs will be unset in
        flag : Flag
            Flag to unset on the \*SENSOR_DEFINEs

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)



# Instance methods
    def AssociateComment(self, comment):
        """
        Associates a comment with a \*SENSOR_DEFINE

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the \*SENSOR_DEFINE

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
        Clears a flag on the \*SENSOR_DEFINE

        Parameters
        ----------
        flag : Flag
            Flag to clear on the \*SENSOR_DEFINE

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the \*SENSOR_DEFINE. The target include of the copied \*SENSOR_DEFINE can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        SensorDefine
            SensorDefine object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a \*SENSOR_DEFINE

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the \*SENSOR_DEFINE

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
        Checks if the \*SENSOR_DEFINE is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the \*SENSOR_DEFINE

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a \*SENSOR_DEFINE

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a SensorDefine property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the SensorDefine.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            \*SENSOR_DEFINE property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this \*SENSOR_DEFINE.
        Note that a carriage return is not added.
        See also SensorDefine.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the \*SENSOR_DEFINE.
        Note that a carriage return is not added.
        See also SensorDefine.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next \*SENSOR_DEFINE in the model

        Returns
        -------
        SensorDefine
            SensorDefine object (or None if there are no more \*SENSOR_DEFINEs in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous \*SENSOR_DEFINE in the model

        Returns
        -------
        SensorDefine
            SensorDefine object (or None if there are no more \*SENSOR_DEFINEs in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on the \*SENSOR_DEFINE

        Parameters
        ----------
        flag : Flag
            Flag to set on the \*SENSOR_DEFINE

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
        SensorDefine
            SensorDefine object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this \*SENSOR_DEFINE

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

