import Oasys.gRPC


# Metaclass for static properties and constants
class StrainSolidType(type):
    _consts = {'SET', 'SOLID'}

    def __getattr__(cls, name):
        if name in StrainSolidType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("StrainSolid class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in StrainSolidType._consts:
            raise AttributeError("Cannot set StrainSolid class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class StrainSolid(Oasys.gRPC.OasysItem, metaclass=StrainSolidType):
    _props = {'eid', 'epsxx', 'epsxy', 'epsyy', 'epsyz', 'epszx', 'epszz', 'include', 'type'}
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
        if name in StrainSolid._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in StrainSolid._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("StrainSolid instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in StrainSolid._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in StrainSolid._rprops:
            raise AttributeError("Cannot set read-only StrainSolid instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, type, eid, epsxx, epsyy, epszz, epsxy, epsyz, epszx):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, type, eid, epsxx, epsyy, epszz, epsxy, epsyz, epszx)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new StrainSolid object

        Parameters
        ----------
        model : Model
            Model that strain_solid will be created in
        type : constant
            Specify the type of initial strain solid (Can be
            StrainSolid.SOLID or
            StrainSolid.SET)
        eid : integer
            Solid Element ID or solid set ID
        epsxx : real
            The xxth strain component in the global cartesian system
        epsyy : real
            The yyth strain component in the global cartesian system
        epszz : real
            The zzth strain component in the global cartesian system
        epsxy : real
            The xyth strain component in the global cartesian system
        epsyz : real
            The yzth strain component in the global cartesian system
        epszx : real
            The zxth strain component in the global cartesian system

        Returns
        -------
        StrainSolid
            StrainSolid object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def First(model):
        """
        Returns the first initial strain solid in the model

        Parameters
        ----------
        model : Model
            Model to get first initial strain solid in

        Returns
        -------
        StrainSolid
            StrainSolid object (or None if there are no initial strain solids in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FlagAll(model, flag):
        """
        Flags all of the initial strain solids in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all initial strain solids will be flagged in
        flag : Flag
            Flag to set on the initial strain solids

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of StrainSolid objects or properties for all of the initial strain solids in a model in PRIMER.
        If the optional property argument is not given then a list of StrainSolid objects is returned.
        If the property argument is given, that property value for each initial strain solid is returned in the list
        instead of a StrainSolid object

        Parameters
        ----------
        model : Model
            Model to get initial strain solids from
        property : string
            Optional. Name for property to get for all initial strain solids in the model

        Returns
        -------
        list
            List of StrainSolid objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of StrainSolid objects for all of the flagged initial strain solids in a model in PRIMER
        If the optional property argument is not given then a list of StrainSolid objects is returned.
        If the property argument is given, then that property value for each initial strain solid is returned in the list
        instead of a StrainSolid object

        Parameters
        ----------
        model : Model
            Model to get initial strain solids from
        flag : Flag
            Flag set on the initial strain solids that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged initial strain solids in the model

        Returns
        -------
        list
            List of StrainSolid objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the StrainSolid object for a initial strain solid ID

        Parameters
        ----------
        model : Model
            Model to find the initial strain solid in
        number : integer
            number of the initial strain solid you want the StrainSolid object for

        Returns
        -------
        StrainSolid
            StrainSolid object (or None if initial strain solid does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last initial strain solid in the model

        Parameters
        ----------
        model : Model
            Model to get last initial strain solid in

        Returns
        -------
        StrainSolid
            StrainSolid object (or None if there are no initial strain solids in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a initial strain solid

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only initial strain solids from that model can be picked.
            If the argument is a Flag then only initial strain solids that
            are flagged with limit can be selected.
            If omitted, or None, any initial strain solids from any model can be selected.
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
        StrainSolid
            StrainSolid object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def Select(flag, prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg):
        """
        Allows the user to select initial strain solids using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting initial strain solids
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only initial strain solids from that model can be selected.
            If the argument is a Flag then only initial strain solids that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any initial strain solids can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of initial strain solids selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged initial strain solids in the model. The initial strain solids will be sketched until you either call
        StrainSolid.Unsketch(),
        StrainSolid.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged initial strain solids will be sketched in
        flag : Flag
            Flag set on the initial strain solids that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the initial strain solids are sketched.
            If omitted redraw is true. If you want to sketch flagged initial strain solids several times and only
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
        Returns the total number of initial strain solids in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing initial strain solids should be counted. If false or omitted
            referenced but undefined initial strain solids will also be included in the total

        Returns
        -------
        int
            number of initial strain solids
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the initial strain solids in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all initial strain solids will be unset in
        flag : Flag
            Flag to unset on the initial strain solids

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all initial strain solids

        Parameters
        ----------
        model : Model
            Model that all initial strain solids will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the initial strain solids are unsketched.
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
        Unsketches all flagged initial strain solids in the model

        Parameters
        ----------
        model : Model
            Model that all initial strain solids will be unsketched in
        flag : Flag
            Flag set on the initial strain solids that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the initial strain solids are unsketched.
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
        Associates a comment with a initial strain solid

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the initial strain solid

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def ClearFlag(self, flag):
        """
        Clears a flag on the initial strain solid

        Parameters
        ----------
        flag : Flag
            Flag to clear on the initial strain solid

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the initial strain solid. The target include of the copied initial strain solid can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        StrainSolid
            StrainSolid object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a initial strain solid

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the initial strain solid

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "DetachComment", comment)

    def Flagged(self, flag):
        """
        Checks if the initial strain solid is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the initial strain solid

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a initial strain solid

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a StrainSolid property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the StrainSolid.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            initial strain solid property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this initial strain solid (\*INITIAL_STRESS_SOLID).
        Note that a carriage return is not added.
        See also StrainSolid.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the initial strain solid.
        Note that a carriage return is not added.
        See also StrainSolid.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next initial strain solid in the model

        Returns
        -------
        StrainSolid
            StrainSolid object (or None if there are no more initial strain solids in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous initial strain solid in the model

        Returns
        -------
        StrainSolid
            StrainSolid object (or None if there are no more initial strain solids in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on the initial strain solid

        Parameters
        ----------
        flag : Flag
            Flag to set on the initial strain solid

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the initial strain solid. The initial strain solid will be sketched until you either call
        StrainSolid.Unsketch(),
        StrainSolid.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the initial strain solid is sketched.
            If omitted redraw is true. If you want to sketch several initial strain solids and only
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
        Unsketches the initial strain solid

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the initial strain solid is unsketched.
            If omitted redraw is true. If you want to unsketch several initial strain solids and only
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
        StrainSolid
            StrainSolid object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this initial strain solid

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

