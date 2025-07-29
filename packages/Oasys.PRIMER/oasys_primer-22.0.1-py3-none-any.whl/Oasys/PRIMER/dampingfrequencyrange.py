import Oasys.gRPC


# Metaclass for static properties and constants
class DampingFrequencyRangeType(type):
    _consts = {'DEFORM', 'NO_OPT'}

    def __getattr__(cls, name):
        if name in DampingFrequencyRangeType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("DampingFrequencyRange class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in DampingFrequencyRangeType._consts:
            raise AttributeError("Cannot set DampingFrequencyRange class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class DampingFrequencyRange(Oasys.gRPC.OasysItem, metaclass=DampingFrequencyRangeType):
    _props = {'cdamp', 'cdampv', 'fhigh', 'flow', 'icard2', 'iflg', 'include', 'ipwp', 'option', 'pidref', 'psid'}
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
        if name in DampingFrequencyRange._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in DampingFrequencyRange._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("DampingFrequencyRange instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in DampingFrequencyRange._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in DampingFrequencyRange._rprops:
            raise AttributeError("Cannot set read-only DampingFrequencyRange instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, option=Oasys.gRPC.defaultArg, cdamp=Oasys.gRPC.defaultArg, flow=Oasys.gRPC.defaultArg, fhigh=Oasys.gRPC.defaultArg, psid=Oasys.gRPC.defaultArg, pidref=Oasys.gRPC.defaultArg, iflg=Oasys.gRPC.defaultArg, icard2=Oasys.gRPC.defaultArg, cdampv=Oasys.gRPC.defaultArg, ipwp=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, option, cdamp, flow, fhigh, psid, pidref, iflg, icard2, cdampv, ipwp)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new DampingFrequencyRange object for \*DAMPING_FREQUENCY_RANGE

        Parameters
        ----------
        model : Model
            Model that damping frequency range will be created in
        option : constant
            Optional. Damping frequency range type. Can be
            DampingFrequencyRange.NO_OPT or
            DampingFrequencyRange.DEFORM
        cdamp : float
            Optional. Fraction of critical damping
        flow : float
            Optional. Lowest frequency in range of interest
        fhigh : float
            Optional. Highest frequency in range of interest
        psid : integer
            Optional. Set Part set ID
        pidref : integer
            Optional. Part ID
        iflg : integer
            Optional. Method used for internal calculation of damping constants
        icard2 : integer
            Optional. Flag for reading the additional card
        cdampv : float
            Optional. Fraction of critical damping applied to pressure/volume response of solid elements
        ipwp : integer
            Optional. Flag to determine whether damping is applied to excess pore pressure

        Returns
        -------
        DampingFrequencyRange
            DampingFrequencyRange object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def BlankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the damping frequency ranges in the model

        Parameters
        ----------
        model : Model
            Model that all damping frequency ranges will be blanked in
        redraw : boolean
            Optional. If model should be redrawn or not.
            If omitted redraw is false. If you want to do several (un)blanks and only
            redraw after the last one then use false for all redraws apart from the last one.
            Alternatively you can redraw using View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "BlankAll", model, redraw)

    def BlankFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the flagged damping frequency ranges in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged damping frequency ranges will be blanked in
        flag : Flag
            Flag set on the damping frequency ranges that you want to blank
        redraw : boolean
            Optional. If model should be redrawn or not.
            If omitted redraw is false. If you want to do several (un)blanks and only
            redraw after the last one then use false for all redraws apart from the last one.
            Alternatively you can redraw using View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "BlankFlagged", model, flag, redraw)

    def First(model):
        """
        Returns the first damping frequency range in the model

        Parameters
        ----------
        model : Model
            Model to get first damping frequency range in

        Returns
        -------
        DampingFrequencyRange
            DampingFrequencyRange object (or None if there are no damping frequency ranges in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FlagAll(model, flag):
        """
        Flags all of the damping frequency ranges in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all damping frequency ranges will be flagged in
        flag : Flag
            Flag to set on the damping frequency ranges

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of DampingFrequencyRange objects or properties for all of the damping frequency ranges in a model in PRIMER.
        If the optional property argument is not given then a list of DampingFrequencyRange objects is returned.
        If the property argument is given, that property value for each damping frequency range is returned in the list
        instead of a DampingFrequencyRange object

        Parameters
        ----------
        model : Model
            Model to get damping frequency ranges from
        property : string
            Optional. Name for property to get for all damping frequency ranges in the model

        Returns
        -------
        list
            List of DampingFrequencyRange objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of DampingFrequencyRange objects for all of the flagged damping frequency ranges in a model in PRIMER
        If the optional property argument is not given then a list of DampingFrequencyRange objects is returned.
        If the property argument is given, then that property value for each damping frequency range is returned in the list
        instead of a DampingFrequencyRange object

        Parameters
        ----------
        model : Model
            Model to get damping frequency ranges from
        flag : Flag
            Flag set on the damping frequency ranges that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged damping frequency ranges in the model

        Returns
        -------
        list
            List of DampingFrequencyRange objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the DampingFrequencyRange object for a damping frequency range ID

        Parameters
        ----------
        model : Model
            Model to find the damping frequency range in
        number : integer
            number of the damping frequency range you want the DampingFrequencyRange object for

        Returns
        -------
        DampingFrequencyRange
            DampingFrequencyRange object (or None if damping frequency range does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last damping frequency range in the model

        Parameters
        ----------
        model : Model
            Model to get last damping frequency range in

        Returns
        -------
        DampingFrequencyRange
            DampingFrequencyRange object (or None if there are no damping frequency ranges in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a damping frequency range

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only damping frequency ranges from that model can be picked.
            If the argument is a Flag then only damping frequency ranges that
            are flagged with limit can be selected.
            If omitted, or None, any damping frequency ranges from any model can be selected.
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
        DampingFrequencyRange
            DampingFrequencyRange object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def Select(flag, prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg):
        """
        Allows the user to select damping frequency ranges using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting damping frequency ranges
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only damping frequency ranges from that model can be selected.
            If the argument is a Flag then only damping frequency ranges that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any damping frequency ranges can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of damping frequency ranges selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged damping frequency ranges in the model. The damping frequency ranges will be sketched until you either call
        DampingFrequencyRange.Unsketch(),
        DampingFrequencyRange.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged damping frequency ranges will be sketched in
        flag : Flag
            Flag set on the damping frequency ranges that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the damping frequency ranges are sketched.
            If omitted redraw is true. If you want to sketch flagged damping frequency ranges several times and only
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
        Returns the total number of damping frequency ranges in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing damping frequency ranges should be counted. If false or omitted
            referenced but undefined damping frequency ranges will also be included in the total

        Returns
        -------
        int
            number of damping frequency ranges
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnblankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the damping frequency ranges in the model

        Parameters
        ----------
        model : Model
            Model that all damping frequency ranges will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not.
            If omitted redraw is false. If you want to do several (un)blanks and only
            redraw after the last one then use false for all redraws apart from the last one.
            Alternatively you can redraw using View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnblankAll", model, redraw)

    def UnblankFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the flagged damping frequency ranges in the model

        Parameters
        ----------
        model : Model
            Model that the flagged damping frequency ranges will be unblanked in
        flag : Flag
            Flag set on the damping frequency ranges that you want to unblank
        redraw : boolean
            Optional. If model should be redrawn or not.
            If omitted redraw is false. If you want to do several (un)blanks and only
            redraw after the last one then use false for all redraws apart from the last one.
            Alternatively you can redraw using View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnblankFlagged", model, flag, redraw)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the damping frequency ranges in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all damping frequency ranges will be unset in
        flag : Flag
            Flag to unset on the damping frequency ranges

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all damping frequency ranges

        Parameters
        ----------
        model : Model
            Model that all damping frequency ranges will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the damping frequency ranges are unsketched.
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
        Unsketches all flagged damping frequency ranges in the model

        Parameters
        ----------
        model : Model
            Model that all damping frequency ranges will be unsketched in
        flag : Flag
            Flag set on the damping frequency ranges that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the damping frequency ranges are unsketched.
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
        Associates a comment with a damping frequency range

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the damping frequency range

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def Blank(self):
        """
        Blanks the damping frequency range

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank")

    def Blanked(self):
        """
        Checks if the damping frequency range is blanked or not

        Returns
        -------
        bool
            True if blanked, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blanked")

    def ClearFlag(self, flag):
        """
        Clears a flag on the damping frequency range

        Parameters
        ----------
        flag : Flag
            Flag to clear on the damping frequency range

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the damping frequency range. The target include of the copied damping frequency range can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        DampingFrequencyRange
            DampingFrequencyRange object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a damping frequency range

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the damping frequency range

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "DetachComment", comment)

    def Flagged(self, flag):
        """
        Checks if the damping frequency range is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the damping frequency range

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a damping frequency range

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a DampingFrequencyRange property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the DampingFrequencyRange.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            damping frequency range property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this damping frequency range (\*DAMPING_FREQUENCY_RANGE).
        Note that a carriage return is not added.
        See also DampingFrequencyRange.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the damping frequency range.
        Note that a carriage return is not added.
        See also DampingFrequencyRange.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next damping frequency range in the model

        Returns
        -------
        DampingFrequencyRange
            DampingFrequencyRange object (or None if there are no more damping frequency ranges in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous damping frequency range in the model

        Returns
        -------
        DampingFrequencyRange
            DampingFrequencyRange object (or None if there are no more damping frequency ranges in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on the damping frequency range

        Parameters
        ----------
        flag : Flag
            Flag to set on the damping frequency range

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the damping frequency range. The damping frequency range will be sketched until you either call
        DampingFrequencyRange.Unsketch(),
        DampingFrequencyRange.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the damping frequency range is sketched.
            If omitted redraw is true. If you want to sketch several damping frequency ranges and only
            redraw after the last one then use false for redraw and call
            View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Sketch", redraw)

    def Unblank(self):
        """
        Unblanks the damping frequency range

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank")

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the damping frequency range

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the damping frequency range is unsketched.
            If omitted redraw is true. If you want to unsketch several damping frequency ranges and only
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
        DampingFrequencyRange
            DampingFrequencyRange object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this damping frequency range

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

