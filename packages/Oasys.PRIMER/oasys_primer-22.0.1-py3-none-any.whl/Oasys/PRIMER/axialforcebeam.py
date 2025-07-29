import Oasys.gRPC


# Metaclass for static properties and constants
class AxialForceBeamType(type):

    def __getattr__(cls, name):

        raise AttributeError("AxialForceBeam class attribute '{}' does not exist".format(name))


class AxialForceBeam(Oasys.gRPC.OasysItem, metaclass=AxialForceBeamType):
    _props = {'bsid', 'include', 'kbend', 'lcid', 'scale'}
    _rprops = {'exists', 'id', 'model'}


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
        if name in AxialForceBeam._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in AxialForceBeam._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("AxialForceBeam instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in AxialForceBeam._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in AxialForceBeam._rprops:
            raise AttributeError("Cannot set read-only AxialForceBeam instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, bsid, lcid, scale=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, bsid, lcid, scale)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new AxialForceBeam object

        Parameters
        ----------
        model : Model
            Model that axial force beam will be created in
        bsid : integer
            BeamSet ID
        lcid : integer
            Loadcurve ID defining preload versus time
        scale : float
            Optional. Scale factor on curve

        Returns
        -------
        AxialForceBeam
            AxialForceBeam object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def First(model):
        """
        Returns the first axial force beam in the model

        Parameters
        ----------
        model : Model
            Model to get first axial force beam in

        Returns
        -------
        AxialForceBeam
            AxialForceBeam object (or None if there are no axial force beams in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FlagAll(model, flag):
        """
        Flags all of the axial force beams in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all axial force beams will be flagged in
        flag : Flag
            Flag to set on the axial force beams

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of AxialForceBeam objects or properties for all of the axial force beams in a model in PRIMER.
        If the optional property argument is not given then a list of AxialForceBeam objects is returned.
        If the property argument is given, that property value for each axial force beam is returned in the list
        instead of a AxialForceBeam object

        Parameters
        ----------
        model : Model
            Model to get axial force beams from
        property : string
            Optional. Name for property to get for all axial force beams in the model

        Returns
        -------
        list
            List of AxialForceBeam objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of AxialForceBeam objects for all of the flagged axial force beams in a model in PRIMER
        If the optional property argument is not given then a list of AxialForceBeam objects is returned.
        If the property argument is given, then that property value for each axial force beam is returned in the list
        instead of a AxialForceBeam object

        Parameters
        ----------
        model : Model
            Model to get axial force beams from
        flag : Flag
            Flag set on the axial force beams that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged axial force beams in the model

        Returns
        -------
        list
            List of AxialForceBeam objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the AxialForceBeam object for a axial force beam ID

        Parameters
        ----------
        model : Model
            Model to find the axial force beam in
        number : integer
            number of the axial force beam you want the AxialForceBeam object for

        Returns
        -------
        AxialForceBeam
            AxialForceBeam object (or None if axial force beam does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last axial force beam in the model

        Parameters
        ----------
        model : Model
            Model to get last axial force beam in

        Returns
        -------
        AxialForceBeam
            AxialForceBeam object (or None if there are no axial force beams in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def Select(flag, prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg):
        """
        Allows the user to select axial force beams using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting axial force beams
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only axial force beams from that model can be selected.
            If the argument is a Flag then only axial force beams that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any axial force beams can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of axial force beams selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged axial force beams in the model. The axial force beams will be sketched until you either call
        AxialForceBeam.Unsketch(),
        AxialForceBeam.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged axial force beams will be sketched in
        flag : Flag
            Flag set on the axial force beams that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the axial force beams are sketched.
            If omitted redraw is true. If you want to sketch flagged axial force beams several times and only
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
        Returns the total number of axial force beams in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing axial force beams should be counted. If false or omitted
            referenced but undefined axial force beams will also be included in the total

        Returns
        -------
        int
            number of axial force beams
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the axial force beams in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all axial force beams will be unset in
        flag : Flag
            Flag to unset on the axial force beams

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all axial force beams

        Parameters
        ----------
        model : Model
            Model that all axial force beams will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the axial force beams are unsketched.
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
        Unsketches all flagged axial force beams in the model

        Parameters
        ----------
        model : Model
            Model that all axial force beams will be unsketched in
        flag : Flag
            Flag set on the axial force beams that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the axial force beams are unsketched.
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
        Associates a comment with a axial force beam

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the axial force beam

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def ClearFlag(self, flag):
        """
        Clears a flag on the axial force beam

        Parameters
        ----------
        flag : Flag
            Flag to clear on the axial force beam

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the axial force beam. The target include of the copied axial force beam can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        AxialForceBeam
            AxialForceBeam object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a axial force beam

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the axial force beam

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "DetachComment", comment)

    def Flagged(self, flag):
        """
        Checks if the axial force beam is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the axial force beam

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a axial force beam

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a AxialForceBeam property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the AxialForceBeam.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            axial force beam property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this axial force beam (\*INITIAL_AXIAL_FORCE_BEAM).
        Note that a carriage return is not added.
        See also AxialForceBeam.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the axial force beam.
        Note that a carriage return is not added.
        See also AxialForceBeam.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next axial force beam in the model

        Returns
        -------
        AxialForceBeam
            AxialForceBeam object (or None if there are no more axial force beams in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous axial force beam in the model

        Returns
        -------
        AxialForceBeam
            AxialForceBeam object (or None if there are no more axial force beams in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on the axial force beam

        Parameters
        ----------
        flag : Flag
            Flag to set on the axial force beam

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the axial force beam. The axial force beam will be sketched until you either call
        AxialForceBeam.Unsketch(),
        AxialForceBeam.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the axial force beam is sketched.
            If omitted redraw is true. If you want to sketch several axial force beams and only
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
        Unsketches the axial force beam

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the axial force beam is unsketched.
            If omitted redraw is true. If you want to unsketch several axial force beams and only
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
        AxialForceBeam
            AxialForceBeam object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this axial force beam

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

