import Oasys.gRPC


# Metaclass for static properties and constants
class ContactGuidedCableType(type):
    _consts = {'PART', 'SET_PART'}

    def __getattr__(cls, name):
        if name in ContactGuidedCableType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("ContactGuidedCable class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in ContactGuidedCableType._consts:
            raise AttributeError("Cannot set ContactGuidedCable class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class ContactGuidedCable(Oasys.gRPC.OasysItem, metaclass=ContactGuidedCableType):
    _props = {'cid', 'endtol', 'fric', 'heading', 'id', 'include', 'nsid', 'pid', 'ptype', 'soft', 'ssfac'}
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
        if name in ContactGuidedCable._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in ContactGuidedCable._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("ContactGuidedCable instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in ContactGuidedCable._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in ContactGuidedCable._rprops:
            raise AttributeError("Cannot set read-only ContactGuidedCable instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, ptype, nsid, pid, soft=Oasys.gRPC.defaultArg, ssfac=Oasys.gRPC.defaultArg, fric=Oasys.gRPC.defaultArg, cid=Oasys.gRPC.defaultArg, heading=Oasys.gRPC.defaultArg, endtol=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, ptype, nsid, pid, soft, ssfac, fric, cid, heading, endtol)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new ContactGuidedCable object

        Parameters
        ----------
        model : Model
            Model that ContactGuidedCable will be created in
        ptype : constant
            Specify the type of ContactGuidedCable (Can be
            ContactGuidedCable.PART or
            ContactGuidedCable.SET_PART
        nsid : integer
            Node Set ID that guides the 1D elements
        pid : integer
            Part ID or Part Set ID
        soft : integer
            Optional. Flag for soft constraint option. Set to 1 for soft constraint
        ssfac : float
            Optional. Stiffness scale factor for penalty stiffness value. The default value is unity. This applies to SOFT set to 0 and 1
        fric : float
            Optional. Contact friction
        cid : integer
            Optional. ContactGuidedCable number (Same as label)
        heading : string
            Optional. ContactGuidedCable heading (Same as title)
        endtol : float
            Optional. Tolerance, in length units

        Returns
        -------
        ContactGuidedCable
            ContactGuidedCable object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def BlankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the contact guided_cables in the model

        Parameters
        ----------
        model : Model
            Model that all contact guided_cables will be blanked in
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
        Blanks all of the flagged contact guided_cables in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged contact guided_cables will be blanked in
        flag : Flag
            Flag set on the contact guided_cables that you want to blank
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
        Returns the first contact guided_cable in the model

        Parameters
        ----------
        model : Model
            Model to get first contact guided_cable in

        Returns
        -------
        ContactGuidedCable
            ContactGuidedCable object (or None if there are no contact guided_cables in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FirstFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the first free contact guided_cable label in the model.
        Also see ContactGuidedCable.LastFreeLabel(),
        ContactGuidedCable.NextFreeLabel() and
        Model.FirstFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get first free contact guided_cable label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            First free in layer in editing panels). If omitted the whole model will be used (Equivalent to
            First free in editing panels)

        Returns
        -------
        int
            ContactGuidedCable label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FirstFreeLabel", model, layer)

    def FlagAll(model, flag):
        """
        Flags all of the contact guided_cables in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all contact guided_cables will be flagged in
        flag : Flag
            Flag to set on the contact guided_cables

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of ContactGuidedCable objects or properties for all of the contact guided_cables in a model in PRIMER.
        If the optional property argument is not given then a list of ContactGuidedCable objects is returned.
        If the property argument is given, that property value for each contact guided_cable is returned in the list
        instead of a ContactGuidedCable object

        Parameters
        ----------
        model : Model
            Model to get contact guided_cables from
        property : string
            Optional. Name for property to get for all contact guided_cables in the model

        Returns
        -------
        list
            List of ContactGuidedCable objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of ContactGuidedCable objects for all of the flagged contact guided_cables in a model in PRIMER
        If the optional property argument is not given then a list of ContactGuidedCable objects is returned.
        If the property argument is given, then that property value for each contact guided_cable is returned in the list
        instead of a ContactGuidedCable object

        Parameters
        ----------
        model : Model
            Model to get contact guided_cables from
        flag : Flag
            Flag set on the contact guided_cables that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged contact guided_cables in the model

        Returns
        -------
        list
            List of ContactGuidedCable objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the ContactGuidedCable object for a contact guided_cable ID

        Parameters
        ----------
        model : Model
            Model to find the contact guided_cable in
        number : integer
            number of the contact guided_cable you want the ContactGuidedCable object for

        Returns
        -------
        ContactGuidedCable
            ContactGuidedCable object (or None if contact guided_cable does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last contact guided_cable in the model

        Parameters
        ----------
        model : Model
            Model to get last contact guided_cable in

        Returns
        -------
        ContactGuidedCable
            ContactGuidedCable object (or None if there are no contact guided_cables in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def LastFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the last free contact guided_cable label in the model.
        Also see ContactGuidedCable.FirstFreeLabel(),
        ContactGuidedCable.NextFreeLabel() and
        see Model.LastFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get last free contact guided_cable label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest free in layer in editing panels). If omitted the whole model will be used

        Returns
        -------
        int
            ContactGuidedCable label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "LastFreeLabel", model, layer)

    def NextFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the next free (highest+1) contact guided_cable label in the model.
        Also see ContactGuidedCable.FirstFreeLabel(),
        ContactGuidedCable.LastFreeLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get next free contact guided_cable label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest+1 in layer in editing panels). If omitted the whole model will be used (Equivalent to
            Highest+1 in editing panels)

        Returns
        -------
        int
            ContactGuidedCable label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NextFreeLabel", model, layer)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a contact guided_cable

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only contact guided_cables from that model can be picked.
            If the argument is a Flag then only contact guided_cables that
            are flagged with limit can be selected.
            If omitted, or None, any contact guided_cables from any model can be selected.
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
        ContactGuidedCable
            ContactGuidedCable object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def RenumberAll(model, start):
        """
        Renumbers all of the contact guided_cables in the model

        Parameters
        ----------
        model : Model
            Model that all contact guided_cables will be renumbered in
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
        Renumbers all of the flagged contact guided_cables in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged contact guided_cables will be renumbered in
        flag : Flag
            Flag set on the contact guided_cables that you want to renumber
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
        Allows the user to select contact guided_cables using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting contact guided_cables
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only contact guided_cables from that model can be selected.
            If the argument is a Flag then only contact guided_cables that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any contact guided_cables can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of contact guided_cables selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged contact guided_cables in the model. The contact guided_cables will be sketched until you either call
        ContactGuidedCable.Unsketch(),
        ContactGuidedCable.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged contact guided_cables will be sketched in
        flag : Flag
            Flag set on the contact guided_cables that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the contact guided_cables are sketched.
            If omitted redraw is true. If you want to sketch flagged contact guided_cables several times and only
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
        Returns the total number of contact guided_cables in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing contact guided_cables should be counted. If false or omitted
            referenced but undefined contact guided_cables will also be included in the total

        Returns
        -------
        int
            number of contact guided_cables
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnblankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the contact guided_cables in the model

        Parameters
        ----------
        model : Model
            Model that all contact guided_cables will be unblanked in
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
        Unblanks all of the flagged contact guided_cables in the model

        Parameters
        ----------
        model : Model
            Model that the flagged contact guided_cables will be unblanked in
        flag : Flag
            Flag set on the contact guided_cables that you want to unblank
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
        Unsets a defined flag on all of the contact guided_cables in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all contact guided_cables will be unset in
        flag : Flag
            Flag to unset on the contact guided_cables

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all contact guided_cables

        Parameters
        ----------
        model : Model
            Model that all contact guided_cables will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the contact guided_cables are unsketched.
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
        Unsketches all flagged contact guided_cables in the model

        Parameters
        ----------
        model : Model
            Model that all contact guided_cables will be unsketched in
        flag : Flag
            Flag set on the contact guided_cables that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the contact guided_cables are unsketched.
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
        Associates a comment with a contact guided_cable

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the contact guided_cable

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def Blank(self):
        """
        Blanks the contact guided_cable

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank")

    def Blanked(self):
        """
        Checks if the contact guided_cable is blanked or not

        Returns
        -------
        bool
            True if blanked, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blanked")

    def ClearFlag(self, flag):
        """
        Clears a flag on the contact guided_cable

        Parameters
        ----------
        flag : Flag
            Flag to clear on the contact guided_cable

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the contact guided_cable. The target include of the copied contact guided_cable can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        ContactGuidedCable
            ContactGuidedCable object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a contact guided_cable

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the contact guided_cable

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "DetachComment", comment)

    def Flagged(self, flag):
        """
        Checks if the contact guided_cable is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the contact guided_cable

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a contact guided_cable

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a ContactGuidedCable property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the ContactGuidedCable.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            contact guided_cable property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this ContactGuidedCable (\*contact_guided_cable).
        Note that a carriage return is not added.
        See also ContactGuidedCable.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the ContactGuidedCable.
        Note that a carriage return is not added.
        See also ContactGuidedCable.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next contact guided_cable in the model

        Returns
        -------
        ContactGuidedCable
            ContactGuidedCable object (or None if there are no more contact guided_cables in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous contact guided_cable in the model

        Returns
        -------
        ContactGuidedCable
            ContactGuidedCable object (or None if there are no more contact guided_cables in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on the contact guided_cable

        Parameters
        ----------
        flag : Flag
            Flag to set on the contact guided_cable

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the contact guided_cable. The contact guided_cable will be sketched until you either call
        ContactGuidedCable.Unsketch(),
        ContactGuidedCable.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the contact guided_cable is sketched.
            If omitted redraw is true. If you want to sketch several contact guided_cables and only
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
        Unblanks the contact guided_cable

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank")

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the contact guided_cable

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the contact guided_cable is unsketched.
            If omitted redraw is true. If you want to unsketch several contact guided_cables and only
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
        ContactGuidedCable
            ContactGuidedCable object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this contact guided_cable

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

