import Oasys.gRPC


# Metaclass for static properties and constants
class RetractorType(type):

    def __getattr__(cls, name):

        raise AttributeError("Retractor class attribute '{}' does not exist".format(name))


class Retractor(Oasys.gRPC.OasysItem, metaclass=RetractorType):
    _props = {'colour', 'dsid', 'flopt', 'include', 'label', 'lcfl', 'lfed', 'llcid', 'nsbi', 'pull', 'sbid', 'sbrid', 'sbrnid', 'sid1', 'sid2', 'sid3', 'sid4', 'tdel', 'transparency', 'ulcid'}
    _rprops = {'exists', 'model', 'shell_seatbelt'}


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
        if name in Retractor._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in Retractor._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("Retractor instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Retractor._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in Retractor._rprops:
            raise AttributeError("Cannot set read-only Retractor instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, sbrid, sbrnid, sbid, llcid, sid1, sid2=Oasys.gRPC.defaultArg, sid3=Oasys.gRPC.defaultArg, sid4=Oasys.gRPC.defaultArg, tdel=Oasys.gRPC.defaultArg, pull=Oasys.gRPC.defaultArg, ulcid=Oasys.gRPC.defaultArg, lfed=Oasys.gRPC.defaultArg, lcfl=Oasys.gRPC.defaultArg, flopt=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, sbrid, sbrnid, sbid, llcid, sid1, sid2, sid3, sid4, tdel, pull, ulcid, lfed, lcfl, flopt)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new Seatbelt Retractor object

        Parameters
        ----------
        model : Model
            Model that retractor will be created in
        sbrid : integer
            Retractor number
        sbrnid : integer
            Node number (or Set Node number if negative)
        sbid : integer
            Seatbelt number.
            (or Set Shell number if sbrnid is negative)
        llcid : integer
            Loadcurve for loading (pull-out vs force)
        sid1 : integer
            Sensor number 1
        sid2 : integer
            Optional. Sensor number 2
        sid3 : integer
            Optional. Sensor number 3
        sid4 : integer
            Optional. Sensor number 4
        tdel : float
            Optional. Time delay after sensor triggers
        pull : float
            Optional. Amount of pull out between time delay ending and retractor locking
        ulcid : integer
            Optional. Loadcurve for unloading (pull-out vs force)
        lfed : float
            Optional. Fed length
        lcfl : integer
            Optional. Loadcurve representing an adaptive multi-level load limiter
        flopt : integer
            Optional. limiting force flage

        Returns
        -------
        Retractor
            Retractor object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def BlankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the retractors in the model

        Parameters
        ----------
        model : Model
            Model that all retractors will be blanked in
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
        Blanks all of the flagged retractors in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged retractors will be blanked in
        flag : Flag
            Flag set on the retractors that you want to blank
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

    def Create(model, modal=Oasys.gRPC.defaultArg):
        """
        Starts an interactive editing panel to create a retractor

        Parameters
        ----------
        model : Model
            Model that the retractor will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        Retractor
            Retractor object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def First(model):
        """
        Returns the first retractor in the model

        Parameters
        ----------
        model : Model
            Model to get first retractor in

        Returns
        -------
        Retractor
            Retractor object (or None if there are no retractors in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FirstFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the first free retractor label in the model.
        Also see Retractor.LastFreeLabel(),
        Retractor.NextFreeLabel() and
        Model.FirstFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get first free retractor label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            First free in layer in editing panels). If omitted the whole model will be used (Equivalent to
            First free in editing panels)

        Returns
        -------
        int
            Retractor label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FirstFreeLabel", model, layer)

    def FlagAll(model, flag):
        """
        Flags all of the retractors in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all retractors will be flagged in
        flag : Flag
            Flag to set on the retractors

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Retractor objects or properties for all of the retractors in a model in PRIMER.
        If the optional property argument is not given then a list of Retractor objects is returned.
        If the property argument is given, that property value for each retractor is returned in the list
        instead of a Retractor object

        Parameters
        ----------
        model : Model
            Model to get retractors from
        property : string
            Optional. Name for property to get for all retractors in the model

        Returns
        -------
        list
            List of Retractor objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Retractor objects for all of the flagged retractors in a model in PRIMER
        If the optional property argument is not given then a list of Retractor objects is returned.
        If the property argument is given, then that property value for each retractor is returned in the list
        instead of a Retractor object

        Parameters
        ----------
        model : Model
            Model to get retractors from
        flag : Flag
            Flag set on the retractors that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged retractors in the model

        Returns
        -------
        list
            List of Retractor objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the Retractor object for a retractor ID

        Parameters
        ----------
        model : Model
            Model to find the retractor in
        number : integer
            number of the retractor you want the Retractor object for

        Returns
        -------
        Retractor
            Retractor object (or None if retractor does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last retractor in the model

        Parameters
        ----------
        model : Model
            Model to get last retractor in

        Returns
        -------
        Retractor
            Retractor object (or None if there are no retractors in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def LastFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the last free retractor label in the model.
        Also see Retractor.FirstFreeLabel(),
        Retractor.NextFreeLabel() and
        see Model.LastFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get last free retractor label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest free in layer in editing panels). If omitted the whole model will be used

        Returns
        -------
        int
            Retractor label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "LastFreeLabel", model, layer)

    def NextFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the next free (highest+1) retractor label in the model.
        Also see Retractor.FirstFreeLabel(),
        Retractor.LastFreeLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get next free retractor label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest+1 in layer in editing panels). If omitted the whole model will be used (Equivalent to
            Highest+1 in editing panels)

        Returns
        -------
        int
            Retractor label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NextFreeLabel", model, layer)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a retractor

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only retractors from that model can be picked.
            If the argument is a Flag then only retractors that
            are flagged with limit can be selected.
            If omitted, or None, any retractors from any model can be selected.
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
        Retractor
            Retractor object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def RenumberAll(model, start):
        """
        Renumbers all of the retractors in the model

        Parameters
        ----------
        model : Model
            Model that all retractors will be renumbered in
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
        Renumbers all of the flagged retractors in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged retractors will be renumbered in
        flag : Flag
            Flag set on the retractors that you want to renumber
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
        Allows the user to select retractors using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting retractors
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only retractors from that model can be selected.
            If the argument is a Flag then only retractors that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any retractors can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of retractors selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged retractors in the model. The retractors will be sketched until you either call
        Retractor.Unsketch(),
        Retractor.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged retractors will be sketched in
        flag : Flag
            Flag set on the retractors that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the retractors are sketched.
            If omitted redraw is true. If you want to sketch flagged retractors several times and only
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
        Returns the total number of retractors in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing retractors should be counted. If false or omitted
            referenced but undefined retractors will also be included in the total

        Returns
        -------
        int
            number of retractors
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnblankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the retractors in the model

        Parameters
        ----------
        model : Model
            Model that all retractors will be unblanked in
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
        Unblanks all of the flagged retractors in the model

        Parameters
        ----------
        model : Model
            Model that the flagged retractors will be unblanked in
        flag : Flag
            Flag set on the retractors that you want to unblank
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
        Unsets a defined flag on all of the retractors in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all retractors will be unset in
        flag : Flag
            Flag to unset on the retractors

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all retractors

        Parameters
        ----------
        model : Model
            Model that all retractors will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the retractors are unsketched.
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
        Unsketches all flagged retractors in the model

        Parameters
        ----------
        model : Model
            Model that all retractors will be unsketched in
        flag : Flag
            Flag set on the retractors that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the retractors are unsketched.
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
        Associates a comment with a retractor

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the retractor

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def Blank(self):
        """
        Blanks the retractor

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank")

    def Blanked(self):
        """
        Checks if the retractor is blanked or not

        Returns
        -------
        bool
            True if blanked, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blanked")

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
        Clears a flag on the retractor

        Parameters
        ----------
        flag : Flag
            Flag to clear on the retractor

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the retractor. The target include of the copied retractor can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        Retractor
            Retractor object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a retractor

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the retractor

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

    def ExtractColour(self):
        """
        Extracts the actual colour used for retractor.
        By default in PRIMER many entities such as elements get their colour automatically from the part that they are in.
        PRIMER cycles through 13 default colours based on the label of the entity. In this case the retractor colour
        property will return the value Colour.PART instead of the actual colour.
        This method will return the actual colour which is used for drawing the retractor

        Returns
        -------
        int
            colour value (integer)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ExtractColour")

    def Flagged(self, flag):
        """
        Checks if the retractor is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the retractor

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a retractor

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a Retractor property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the Retractor.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            retractor property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this retractor (\*ELEMENT_SEATBELT_RETREROMETER)
        Note that a carriage return is not added.
        See also Retractor.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the retractor.
        Note that a carriage return is not added.
        See also Retractor.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next retractor in the model

        Returns
        -------
        Retractor
            Retractor object (or None if there are no more retractors in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous retractor in the model

        Returns
        -------
        Retractor
            Retractor object (or None if there are no more retractors in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on the retractor

        Parameters
        ----------
        flag : Flag
            Flag to set on the retractor

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the retractor. The retractor will be sketched until you either call
        Retractor.Unsketch(),
        Retractor.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the retractor is sketched.
            If omitted redraw is true. If you want to sketch several retractors and only
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
        Unblanks the retractor

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank")

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the retractor

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the retractor is unsketched.
            If omitted redraw is true. If you want to unsketch several retractors and only
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
        Retractor
            Retractor object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this retractor

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

