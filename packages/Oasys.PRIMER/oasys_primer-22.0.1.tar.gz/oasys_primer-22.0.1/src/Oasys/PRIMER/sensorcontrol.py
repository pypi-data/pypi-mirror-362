import Oasys.gRPC


# Metaclass for static properties and constants
class SensorControlType(type):

    def __getattr__(cls, name):

        raise AttributeError("SensorControl class attribute '{}' does not exist".format(name))


class SensorControl(Oasys.gRPC.OasysItem, metaclass=SensorControlType):
    _props = {'cntlid', 'defcv', 'estyp', 'include', 'initstt', 'label', 'nrep', 'swit1', 'swit2', 'swit3', 'swit4', 'swit5', 'swit6', 'swit7', 'timeoff', 'timeoff/idiscl', 'type', 'typeid'}
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
        if name in SensorControl._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in SensorControl._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("SensorControl instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in SensorControl._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in SensorControl._rprops:
            raise AttributeError("Cannot set read-only SensorControl instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, sensor_control_id, type, type_id=Oasys.gRPC.defaultArg, estyp=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, sensor_control_id, type, type_id, estyp)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new SensorControl object

        Parameters
        ----------
        model : Model
            Model that \*SENSOR_CONTROL will be created in
        sensor_control_id : integer
            SensorControl id
        type : string
            Entity type to be controlled. Can be "AIRBAG", "BAGVENTPOP", "BELTPRET", "BELTRETRA",
            "BELTSLIP", "CONTACT", "CONTACT2D", "DEF2RIG", "CURVE", "DISC-ELE", "DISC-ELES",
            "ELESET", "FUNCTION", "JOINT", "JOINTSTIFF", "M PRESSURE", "RWALL", "SPC",
            "SPOTWELD"
        type_id : integer
            Optional. ID of entity to be controlled if type is not FUNCTION or input value for FUNCTION
        estyp : string
            Optional. Element Set Type to be controlled. Can be "BEAM", "DISC", "SHELL", "SOLID", "TSHELL". Required only if Type argument is "ELESET"

        Returns
        -------
        SensorControl
            SensorControl object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def Create(model, modal=Oasys.gRPC.defaultArg):
        """
        Starts an interactive editing panel to create a \*SENSOR_CONTROL

        Parameters
        ----------
        model : Model
            Model that the \*SENSOR_CONTROL will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        SensorControl
            SensorControl object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def First(model):
        """
        Returns the first \*SENSOR_CONTROL in the model

        Parameters
        ----------
        model : Model
            Model to get first \*SENSOR_CONTROL in

        Returns
        -------
        SensorControl
            SensorControl object (or None if there are no \*SENSOR_CONTROLs in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FirstFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the first free \*SENSOR_CONTROL label in the model.
        Also see SensorControl.LastFreeLabel(),
        SensorControl.NextFreeLabel() and
        Model.FirstFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get first free \*SENSOR_CONTROL label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            First free in layer in editing panels). If omitted the whole model will be used (Equivalent to
            First free in editing panels)

        Returns
        -------
        int
            SensorControl label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FirstFreeLabel", model, layer)

    def FlagAll(model, flag):
        """
        Flags all of the \*SENSOR_CONTROLs in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all \*SENSOR_CONTROLs will be flagged in
        flag : Flag
            Flag to set on the \*SENSOR_CONTROLs

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of SensorControl objects or properties for all of the \*SENSOR_CONTROLs in a model in PRIMER.
        If the optional property argument is not given then a list of SensorControl objects is returned.
        If the property argument is given, that property value for each \*SENSOR_CONTROL is returned in the list
        instead of a SensorControl object

        Parameters
        ----------
        model : Model
            Model to get \*SENSOR_CONTROLs from
        property : string
            Optional. Name for property to get for all \*SENSOR_CONTROLs in the model

        Returns
        -------
        list
            List of SensorControl objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of SensorControl objects for all of the flagged \*SENSOR_CONTROLs in a model in PRIMER
        If the optional property argument is not given then a list of SensorControl objects is returned.
        If the property argument is given, then that property value for each \*SENSOR_CONTROL is returned in the list
        instead of a SensorControl object

        Parameters
        ----------
        model : Model
            Model to get \*SENSOR_CONTROLs from
        flag : Flag
            Flag set on the \*SENSOR_CONTROLs that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged \*SENSOR_CONTROLs in the model

        Returns
        -------
        list
            List of SensorControl objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the SensorControl object for a \*SENSOR_CONTROL ID

        Parameters
        ----------
        model : Model
            Model to find the \*SENSOR_CONTROL in
        number : integer
            number of the \*SENSOR_CONTROL you want the SensorControl object for

        Returns
        -------
        SensorControl
            SensorControl object (or None if \*SENSOR_CONTROL does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last \*SENSOR_CONTROL in the model

        Parameters
        ----------
        model : Model
            Model to get last \*SENSOR_CONTROL in

        Returns
        -------
        SensorControl
            SensorControl object (or None if there are no \*SENSOR_CONTROLs in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def LastFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the last free \*SENSOR_CONTROL label in the model.
        Also see SensorControl.FirstFreeLabel(),
        SensorControl.NextFreeLabel() and
        see Model.LastFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get last free \*SENSOR_CONTROL label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest free in layer in editing panels). If omitted the whole model will be used

        Returns
        -------
        int
            SensorControl label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "LastFreeLabel", model, layer)

    def NextFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the next free (highest+1) \*SENSOR_CONTROL label in the model.
        Also see SensorControl.FirstFreeLabel(),
        SensorControl.LastFreeLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get next free \*SENSOR_CONTROL label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest+1 in layer in editing panels). If omitted the whole model will be used (Equivalent to
            Highest+1 in editing panels)

        Returns
        -------
        int
            SensorControl label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NextFreeLabel", model, layer)

    def RenumberAll(model, start):
        """
        Renumbers all of the \*SENSOR_CONTROLs in the model

        Parameters
        ----------
        model : Model
            Model that all \*SENSOR_CONTROLs will be renumbered in
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
        Renumbers all of the flagged \*SENSOR_CONTROLs in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged \*SENSOR_CONTROLs will be renumbered in
        flag : Flag
            Flag set on the \*SENSOR_CONTROLs that you want to renumber
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
        Allows the user to select \*SENSOR_CONTROLs using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting \*SENSOR_CONTROLs
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only \*SENSOR_CONTROLs from that model can be selected.
            If the argument is a Flag then only \*SENSOR_CONTROLs that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any \*SENSOR_CONTROLs can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of \*SENSOR_CONTROLs selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged \*SENSOR_CONTROLs in the model. The \*SENSOR_CONTROLs will be sketched until you either call
        SensorControl.Unsketch(),
        SensorControl.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged \*SENSOR_CONTROLs will be sketched in
        flag : Flag
            Flag set on the \*SENSOR_CONTROLs that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the \*SENSOR_CONTROLs are sketched.
            If omitted redraw is true. If you want to sketch flagged \*SENSOR_CONTROLs several times and only
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
        Returns the total number of \*SENSOR_CONTROLs in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing \*SENSOR_CONTROLs should be counted. If false or omitted
            referenced but undefined \*SENSOR_CONTROLs will also be included in the total

        Returns
        -------
        int
            number of \*SENSOR_CONTROLs
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the \*SENSOR_CONTROLs in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all \*SENSOR_CONTROLs will be unset in
        flag : Flag
            Flag to unset on the \*SENSOR_CONTROLs

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all \*SENSOR_CONTROLs

        Parameters
        ----------
        model : Model
            Model that all \*SENSOR_CONTROLs will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the \*SENSOR_CONTROLs are unsketched.
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
        Unsketches all flagged \*SENSOR_CONTROLs in the model

        Parameters
        ----------
        model : Model
            Model that all \*SENSOR_CONTROLs will be unsketched in
        flag : Flag
            Flag set on the \*SENSOR_CONTROLs that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the \*SENSOR_CONTROLs are unsketched.
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
        Associates a comment with a \*SENSOR_CONTROL

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the \*SENSOR_CONTROL

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
        Clears a flag on the \*SENSOR_CONTROL

        Parameters
        ----------
        flag : Flag
            Flag to clear on the \*SENSOR_CONTROL

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the \*SENSOR_CONTROL. The target include of the copied \*SENSOR_CONTROL can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        SensorControl
            SensorControl object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a \*SENSOR_CONTROL

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the \*SENSOR_CONTROL

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
        Checks if the \*SENSOR_CONTROL is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the \*SENSOR_CONTROL

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a \*SENSOR_CONTROL

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a SensorControl property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the SensorControl.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            \*SENSOR_CONTROL property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this \*SENSOR_CONTROL.
        Note that a carriage return is not added.
        See also SensorControl.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the \*SENSOR_CONTROL.
        Note that a carriage return is not added.
        See also SensorControl.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next \*SENSOR_CONTROL in the model

        Returns
        -------
        SensorControl
            SensorControl object (or None if there are no more \*SENSOR_CONTROLs in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous \*SENSOR_CONTROL in the model

        Returns
        -------
        SensorControl
            SensorControl object (or None if there are no more \*SENSOR_CONTROLs in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on the \*SENSOR_CONTROL

        Parameters
        ----------
        flag : Flag
            Flag to set on the \*SENSOR_CONTROL

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the \*SENSOR_CONTROL. The \*SENSOR_CONTROL will be sketched until you either call
        SensorControl.Unsketch(),
        SensorControl.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the \*SENSOR_CONTROL is sketched.
            If omitted redraw is true. If you want to sketch several \*SENSOR_CONTROLs and only
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
        Unsketches the \*SENSOR_CONTROL

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the \*SENSOR_CONTROL is unsketched.
            If omitted redraw is true. If you want to unsketch several \*SENSOR_CONTROLs and only
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
        SensorControl
            SensorControl object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this \*SENSOR_CONTROL

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

