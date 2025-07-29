import Oasys.gRPC


# Metaclass for static properties and constants
class StrainBeamType(type):

    def __getattr__(cls, name):

        raise AttributeError("StrainBeam class attribute '{}' does not exist".format(name))


class StrainBeam(Oasys.gRPC.OasysItem, metaclass=StrainBeamType):
    _props = {'eid', 'include', 'rdisp', 'rrot', 'sdisp', 'srot', 'tdisp', 'trot'}
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
        if name in StrainBeam._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in StrainBeam._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("StrainBeam instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in StrainBeam._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in StrainBeam._rprops:
            raise AttributeError("Cannot set read-only StrainBeam instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, details):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, details)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new StrainBeam object

        Parameters
        ----------
        model : Model
            Model that strain_beam will be created in
        details : dict
            Details for creating the StrainBeam

        Returns
        -------
        StrainBeam
            StrainBeam object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def First(model):
        """
        Returns the first initial strain beam in the model

        Parameters
        ----------
        model : Model
            Model to get first initial strain beam in

        Returns
        -------
        StrainBeam
            StrainBeam object (or None if there are no initial strain beams in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FlagAll(model, flag):
        """
        Flags all of the initial strain beams in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all initial strain beams will be flagged in
        flag : Flag
            Flag to set on the initial strain beams

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of StrainBeam objects or properties for all of the initial strain beams in a model in PRIMER.
        If the optional property argument is not given then a list of StrainBeam objects is returned.
        If the property argument is given, that property value for each initial strain beam is returned in the list
        instead of a StrainBeam object

        Parameters
        ----------
        model : Model
            Model to get initial strain beams from
        property : string
            Optional. Name for property to get for all initial strain beams in the model

        Returns
        -------
        list
            List of StrainBeam objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of StrainBeam objects for all of the flagged initial strain beams in a model in PRIMER
        If the optional property argument is not given then a list of StrainBeam objects is returned.
        If the property argument is given, then that property value for each initial strain beam is returned in the list
        instead of a StrainBeam object

        Parameters
        ----------
        model : Model
            Model to get initial strain beams from
        flag : Flag
            Flag set on the initial strain beams that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged initial strain beams in the model

        Returns
        -------
        list
            List of StrainBeam objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the StrainBeam object for a initial strain beam ID

        Parameters
        ----------
        model : Model
            Model to find the initial strain beam in
        number : integer
            number of the initial strain beam you want the StrainBeam object for

        Returns
        -------
        StrainBeam
            StrainBeam object (or None if initial strain beam does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last initial strain beam in the model

        Parameters
        ----------
        model : Model
            Model to get last initial strain beam in

        Returns
        -------
        StrainBeam
            StrainBeam object (or None if there are no initial strain beams in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a initial strain beam

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only initial strain beams from that model can be picked.
            If the argument is a Flag then only initial strain beams that
            are flagged with limit can be selected.
            If omitted, or None, any initial strain beams from any model can be selected.
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
        StrainBeam
            StrainBeam object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def Select(flag, prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg):
        """
        Allows the user to select initial strain beams using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting initial strain beams
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only initial strain beams from that model can be selected.
            If the argument is a Flag then only initial strain beams that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any initial strain beams can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of initial strain beams selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged initial strain beams in the model. The initial strain beams will be sketched until you either call
        StrainBeam.Unsketch(),
        StrainBeam.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged initial strain beams will be sketched in
        flag : Flag
            Flag set on the initial strain beams that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the initial strain beams are sketched.
            If omitted redraw is true. If you want to sketch flagged initial strain beams several times and only
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
        Returns the total number of initial strain beams in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing initial strain beams should be counted. If false or omitted
            referenced but undefined initial strain beams will also be included in the total

        Returns
        -------
        int
            number of initial strain beams
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the initial strain beams in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all initial strain beams will be unset in
        flag : Flag
            Flag to unset on the initial strain beams

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all initial strain beams

        Parameters
        ----------
        model : Model
            Model that all initial strain beams will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the initial strain beams are unsketched.
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
        Unsketches all flagged initial strain beams in the model

        Parameters
        ----------
        model : Model
            Model that all initial strain beams will be unsketched in
        flag : Flag
            Flag set on the initial strain beams that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the initial strain beams are unsketched.
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
        Associates a comment with a initial strain beam

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the initial strain beam

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def ClearFlag(self, flag):
        """
        Clears a flag on the initial strain beam

        Parameters
        ----------
        flag : Flag
            Flag to clear on the initial strain beam

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the initial strain beam. The target include of the copied initial strain beam can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        StrainBeam
            StrainBeam object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a initial strain beam

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the initial strain beam

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "DetachComment", comment)

    def Flagged(self, flag):
        """
        Checks if the initial strain beam is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the initial strain beam

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a initial strain beam

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a StrainBeam property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the StrainBeam.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            initial strain beam property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this initial strain beam (\*INITIAL_STRAIN_SHELL).
        Note that a carriage return is not added.
        See also StrainBeam.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the initial strain beam.
        Note that a carriage return is not added.
        See also StrainBeam.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next initial strain beam in the model

        Returns
        -------
        StrainBeam
            StrainBeam object (or None if there are no more initial strain beams in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous initial strain beam in the model

        Returns
        -------
        StrainBeam
            StrainBeam object (or None if there are no more initial strain beams in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on the initial strain beam

        Parameters
        ----------
        flag : Flag
            Flag to set on the initial strain beam

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the initial strain beam. The initial strain beam will be sketched until you either call
        StrainBeam.Unsketch(),
        StrainBeam.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the initial strain beam is sketched.
            If omitted redraw is true. If you want to sketch several initial strain beams and only
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
        Unsketches the initial strain beam

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the initial strain beam is unsketched.
            If omitted redraw is true. If you want to unsketch several initial strain beams and only
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
        StrainBeam
            StrainBeam object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this initial strain beam

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

