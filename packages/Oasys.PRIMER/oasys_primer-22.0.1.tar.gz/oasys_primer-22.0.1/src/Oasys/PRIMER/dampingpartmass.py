import Oasys.gRPC


# Metaclass for static properties and constants
class DampingPartMassType(type):
    _consts = {'PART', 'SET'}

    def __getattr__(cls, name):
        if name in DampingPartMassType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("DampingPartMass class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in DampingPartMassType._consts:
            raise AttributeError("Cannot set DampingPartMass class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class DampingPartMass(Oasys.gRPC.OasysItem, metaclass=DampingPartMassType):
    _props = {'flag', 'id', 'include', 'lcid', 'sf', 'srx', 'sry', 'srz', 'stx', 'sty', 'stz', 'type'}
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
        if name in DampingPartMass._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in DampingPartMass._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("DampingPartMass instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in DampingPartMass._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in DampingPartMass._rprops:
            raise AttributeError("Cannot set read-only DampingPartMass instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, type, id, lcid, sf=Oasys.gRPC.defaultArg, flag=Oasys.gRPC.defaultArg, stx=Oasys.gRPC.defaultArg, sty=Oasys.gRPC.defaultArg, stz=Oasys.gRPC.defaultArg, srx=Oasys.gRPC.defaultArg, sry=Oasys.gRPC.defaultArg, srz=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, type, id, lcid, sf, flag, stx, sty, stz, srx, sry, srz)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new DampingPartMass object for \*DAMPING_PART_MASS

        Parameters
        ----------
        model : Model
            Model that damping part mass will be created in
        type : constant
            Damping part mass type. Can be
            DampingPartMass.PART or
            DampingPartMass.SET
        id : integer
            Part/part set id
        lcid : integer
            LC: Damping vs time
        sf : float
            Optional. Scale factor on loadcurve
        flag : integer
            Optional. Flag for scale factors
        stx : float
            Optional. Translational x scale factor
        sty : float
            Optional. Translational y scale factor
        stz : float
            Optional. Translational z scale factor
        srx : float
            Optional. Rotational x scale factor
        sry : float
            Optional. Rotational y scale factor
        srz : float
            Optional. Rotational z scale factor

        Returns
        -------
        DampingPartMass
            DampingPartMass object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def BlankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the damping part masss in the model

        Parameters
        ----------
        model : Model
            Model that all damping part masss will be blanked in
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
        Blanks all of the flagged damping part masss in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged damping part masss will be blanked in
        flag : Flag
            Flag set on the damping part masss that you want to blank
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
        Returns the first damping part mass in the model

        Parameters
        ----------
        model : Model
            Model to get first damping part mass in

        Returns
        -------
        DampingPartMass
            DampingPartMass object (or None if there are no damping part masss in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FlagAll(model, flag):
        """
        Flags all of the damping part masss in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all damping part masss will be flagged in
        flag : Flag
            Flag to set on the damping part masss

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of DampingPartMass objects or properties for all of the damping part masss in a model in PRIMER.
        If the optional property argument is not given then a list of DampingPartMass objects is returned.
        If the property argument is given, that property value for each damping part mass is returned in the list
        instead of a DampingPartMass object

        Parameters
        ----------
        model : Model
            Model to get damping part masss from
        property : string
            Optional. Name for property to get for all damping part masss in the model

        Returns
        -------
        list
            List of DampingPartMass objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of DampingPartMass objects for all of the flagged damping part masss in a model in PRIMER
        If the optional property argument is not given then a list of DampingPartMass objects is returned.
        If the property argument is given, then that property value for each damping part mass is returned in the list
        instead of a DampingPartMass object

        Parameters
        ----------
        model : Model
            Model to get damping part masss from
        flag : Flag
            Flag set on the damping part masss that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged damping part masss in the model

        Returns
        -------
        list
            List of DampingPartMass objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the DampingPartMass object for a damping part mass ID

        Parameters
        ----------
        model : Model
            Model to find the damping part mass in
        number : integer
            number of the damping part mass you want the DampingPartMass object for

        Returns
        -------
        DampingPartMass
            DampingPartMass object (or None if damping part mass does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last damping part mass in the model

        Parameters
        ----------
        model : Model
            Model to get last damping part mass in

        Returns
        -------
        DampingPartMass
            DampingPartMass object (or None if there are no damping part masss in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a damping part mass

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only damping part masss from that model can be picked.
            If the argument is a Flag then only damping part masss that
            are flagged with limit can be selected.
            If omitted, or None, any damping part masss from any model can be selected.
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
        DampingPartMass
            DampingPartMass object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def Select(flag, prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg):
        """
        Allows the user to select damping part masss using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting damping part masss
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only damping part masss from that model can be selected.
            If the argument is a Flag then only damping part masss that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any damping part masss can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of damping part masss selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged damping part masss in the model. The damping part masss will be sketched until you either call
        DampingPartMass.Unsketch(),
        DampingPartMass.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged damping part masss will be sketched in
        flag : Flag
            Flag set on the damping part masss that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the damping part masss are sketched.
            If omitted redraw is true. If you want to sketch flagged damping part masss several times and only
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
        Returns the total number of damping part masss in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing damping part masss should be counted. If false or omitted
            referenced but undefined damping part masss will also be included in the total

        Returns
        -------
        int
            number of damping part masss
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnblankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the damping part masss in the model

        Parameters
        ----------
        model : Model
            Model that all damping part masss will be unblanked in
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
        Unblanks all of the flagged damping part masss in the model

        Parameters
        ----------
        model : Model
            Model that the flagged damping part masss will be unblanked in
        flag : Flag
            Flag set on the damping part masss that you want to unblank
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
        Unsets a defined flag on all of the damping part masss in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all damping part masss will be unset in
        flag : Flag
            Flag to unset on the damping part masss

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all damping part masss

        Parameters
        ----------
        model : Model
            Model that all damping part masss will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the damping part masss are unsketched.
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
        Unsketches all flagged damping part masss in the model

        Parameters
        ----------
        model : Model
            Model that all damping part masss will be unsketched in
        flag : Flag
            Flag set on the damping part masss that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the damping part masss are unsketched.
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
        Associates a comment with a damping part mass

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the damping part mass

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def Blank(self):
        """
        Blanks the damping part mass

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank")

    def Blanked(self):
        """
        Checks if the damping part mass is blanked or not

        Returns
        -------
        bool
            True if blanked, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blanked")

    def ClearFlag(self, flag):
        """
        Clears a flag on the damping part mass

        Parameters
        ----------
        flag : Flag
            Flag to clear on the damping part mass

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the damping part mass. The target include of the copied damping part mass can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        DampingPartMass
            DampingPartMass object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a damping part mass

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the damping part mass

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "DetachComment", comment)

    def Flagged(self, flag):
        """
        Checks if the damping part mass is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the damping part mass

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a damping part mass

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a DampingPartMass property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the DampingPartMass.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            damping part mass property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this damping part mass (\*DAMPING_PART_MASS).
        Note that a carriage return is not added.
        See also DampingPartMass.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the damping part mass.
        Note that a carriage return is not added.
        See also DampingPartMass.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next damping part mass in the model

        Returns
        -------
        DampingPartMass
            DampingPartMass object (or None if there are no more damping part masss in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous damping part mass in the model

        Returns
        -------
        DampingPartMass
            DampingPartMass object (or None if there are no more damping part masss in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on the damping part mass

        Parameters
        ----------
        flag : Flag
            Flag to set on the damping part mass

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the damping part mass. The damping part mass will be sketched until you either call
        DampingPartMass.Unsketch(),
        DampingPartMass.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the damping part mass is sketched.
            If omitted redraw is true. If you want to sketch several damping part masss and only
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
        Unblanks the damping part mass

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank")

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the damping part mass

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the damping part mass is unsketched.
            If omitted redraw is true. If you want to unsketch several damping part masss and only
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
        DampingPartMass
            DampingPartMass object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this damping part mass

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

