import Oasys.gRPC


# Metaclass for static properties and constants
class ContactType(type):
    _consts = {'BEAM_OFFSET', 'CONSTR_OFFSET', 'CROSSED_EDGES', 'MPP_METHOD', 'MPP_MODE', 'NO_OFFSET', 'PENETRATIONS', 'SHELL_AUTO', 'SHELL_THICK', 'SHELL_THIN', 'SIMPLE_OFFSET', 'SMP_METHOD', 'SMP_MODE'}

    def __getattr__(cls, name):
        if name in ContactType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("Contact class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in ContactType._consts:
            raise AttributeError("Cannot set Contact class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class Contact(Oasys.gRPC.OasysItem, metaclass=ContactType):
    _props = {'a', 'algo', 'alpha', 'b', 'bc_flg', 'beta', 'bsort', 'bt', 'bucket', 'c', 'check_mode', 'chksegs', 'cid', 'cid_rcf', 'cideta', 'cidmu', 'close', 'cn', 'cn_1', 'colour', 'contact_penchk_dup_shells', 'cparm8', 'cparm8smp', 'ct2cn', 'ct2cn_1', 'd', 'd_comp', 'dbdth', 'dbinr', 'dbpid', 'dc', 'depth', 'dfscl', 'dnlscl', 'dprfac', 'dt', 'dtpchk', 'dtstif', 'edgek', 'eloff', 'ending', 'epm', 'epscale', 'eraten', 'erates', 'erosop', 'fcm', 'fd', 'flangl', 'fnlscl', 'formula', 'frad', 'frcfrq', 'fricsf', 'fs', 'fsf', 'fstol', 'ftorq', 'ftosa', 'grpable', 'h0', 'hclose', 'heading', 'i2d3d', 'iadj', 'icor', 'id', 'igap', 'ignore', 'ignroff', 'include', 'inititer', 'ipback', 'isym', 'isym_1', 'k', 'kpf', 'label', 'lcbucket', 'lceps', 'lceps2', 'lcfdt', 'lcfst', 'lch', 'lcid', 'lcid1', 'lcid2', 'lcidab', 'lcidnf', 'lcidrf', 'lmax', 'lmin', 'maxpar', 'mes', 'mortar', 'mpp', 'mtcj', 'nen', 'nfls', 'nhv', 'nmhis', 'nmtwh', 'ns2track', 'nstwh', 'ntprm', 'numint', 'offset', 'offset_1', 'offset_flag', 'option', 'option_1', 'param', 'parmax', 'penchk', 'penmax', 'pensf', 'pstiff', 'q2tri', 'region', 'saboxid', 'sapr', 'sast', 'sbboxid', 'sbopt', 'sbpr', 'sbst', 'sfls', 'sfnbr', 'sfsa', 'sfsat', 'sfsb', 'sfsbt', 'sharec', 'shledg', 'shloff', 'shlthk', 'sldstf', 'sldthk', 'snlog', 'sofscl', 'soft', 'srmodel', 'srnde', 'ssftyp', 'surfa', 'surfatyp', 'surfb', 'surfbtyp', 'swtpr', 'tblcid', 'tcso', 'temp', 'tetfac', 'tfail', 'thermal', 'thkoff', 'thkopt', 'tiedid', 'time', 'tscale', 'tsvx', 'tsvy', 'tsvz', 'type', 'up1', 'up10', 'up11', 'up12', 'up13', 'up14', 'up15', 'up16', 'up2', 'up3', 'up4', 'up5', 'up6', 'up7', 'up8', 'up9', 'us', 'vc', 'vdc', 'vsf'}
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
        if name in Contact._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in Contact._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("Contact instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Contact._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in Contact._rprops:
            raise AttributeError("Cannot set read-only Contact instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, type, id=Oasys.gRPC.defaultArg, heading=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, type, id, heading)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new Contact object

        Parameters
        ----------
        model : Model
            Model that Contact will be created in
        type : string
            Type of contact
        id : integer
            Optional. Contact number
        heading : string
            Optional. Title for the Contact

        Returns
        -------
        Contact
            Contact object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def BlankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the contacts in the model

        Parameters
        ----------
        model : Model
            Model that all contacts will be blanked in
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
        Blanks all of the flagged contacts in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged contacts will be blanked in
        flag : Flag
            Flag set on the contacts that you want to blank
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
        Starts an interactive editing panel to create a contact

        Parameters
        ----------
        model : Model
            Model that the contact will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        Contact
            Contact object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def First(model):
        """
        Returns the first contact in the model

        Parameters
        ----------
        model : Model
            Model to get first contact in

        Returns
        -------
        Contact
            Contact object (or None if there are no contacts in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FirstFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the first free contact label in the model.
        Also see Contact.LastFreeLabel(),
        Contact.NextFreeLabel() and
        Model.FirstFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get first free contact label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            First free in layer in editing panels). If omitted the whole model will be used (Equivalent to
            First free in editing panels)

        Returns
        -------
        int
            Contact label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FirstFreeLabel", model, layer)

    def FlagAll(model, flag):
        """
        Flags all of the contacts in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all contacts will be flagged in
        flag : Flag
            Flag to set on the contacts

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Contact objects or properties for all of the contacts in a model in PRIMER.
        If the optional property argument is not given then a list of Contact objects is returned.
        If the property argument is given, that property value for each contact is returned in the list
        instead of a Contact object

        Parameters
        ----------
        model : Model
            Model to get contacts from
        property : string
            Optional. Name for property to get for all contacts in the model

        Returns
        -------
        list
            List of Contact objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Contact objects for all of the flagged contacts in a model in PRIMER
        If the optional property argument is not given then a list of Contact objects is returned.
        If the property argument is given, then that property value for each contact is returned in the list
        instead of a Contact object

        Parameters
        ----------
        model : Model
            Model to get contacts from
        flag : Flag
            Flag set on the contacts that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged contacts in the model

        Returns
        -------
        list
            List of Contact objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the Contact object for a contact ID

        Parameters
        ----------
        model : Model
            Model to find the contact in
        number : integer
            number of the contact you want the Contact object for

        Returns
        -------
        Contact
            Contact object (or None if contact does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last contact in the model

        Parameters
        ----------
        model : Model
            Model to get last contact in

        Returns
        -------
        Contact
            Contact object (or None if there are no contacts in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def LastFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the last free contact label in the model.
        Also see Contact.FirstFreeLabel(),
        Contact.NextFreeLabel() and
        see Model.LastFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get last free contact label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest free in layer in editing panels). If omitted the whole model will be used

        Returns
        -------
        int
            Contact label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "LastFreeLabel", model, layer)

    def NextFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the next free (highest+1) contact label in the model.
        Also see Contact.FirstFreeLabel(),
        Contact.LastFreeLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get next free contact label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest+1 in layer in editing panels). If omitted the whole model will be used (Equivalent to
            Highest+1 in editing panels)

        Returns
        -------
        int
            Contact label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NextFreeLabel", model, layer)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a contact

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only contacts from that model can be picked.
            If the argument is a Flag then only contacts that
            are flagged with limit can be selected.
            If omitted, or None, any contacts from any model can be selected.
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
        Contact
            Contact object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def RenumberAll(model, start):
        """
        Renumbers all of the contacts in the model

        Parameters
        ----------
        model : Model
            Model that all contacts will be renumbered in
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
        Renumbers all of the flagged contacts in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged contacts will be renumbered in
        flag : Flag
            Flag set on the contacts that you want to renumber
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
        Allows the user to select contacts using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting contacts
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only contacts from that model can be selected.
            If the argument is a Flag then only contacts that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any contacts can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of contacts selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged contacts in the model. The contacts will be sketched until you either call
        Contact.Unsketch(),
        Contact.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged contacts will be sketched in
        flag : Flag
            Flag set on the contacts that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the contacts are sketched.
            If omitted redraw is true. If you want to sketch flagged contacts several times and only
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
        Returns the total number of contacts in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing contacts should be counted. If false or omitted
            referenced but undefined contacts will also be included in the total

        Returns
        -------
        int
            number of contacts
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnblankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the contacts in the model

        Parameters
        ----------
        model : Model
            Model that all contacts will be unblanked in
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
        Unblanks all of the flagged contacts in the model

        Parameters
        ----------
        model : Model
            Model that the flagged contacts will be unblanked in
        flag : Flag
            Flag set on the contacts that you want to unblank
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
        Unsets a defined flag on all of the contacts in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all contacts will be unset in
        flag : Flag
            Flag to unset on the contacts

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all contacts

        Parameters
        ----------
        model : Model
            Model that all contacts will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the contacts are unsketched.
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
        Unsketches all flagged contacts in the model

        Parameters
        ----------
        model : Model
            Model that all contacts will be unsketched in
        flag : Flag
            Flag set on the contacts that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the contacts are unsketched.
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
        Associates a comment with a contact

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the contact

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def Blank(self):
        """
        Blanks the contact

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank")

    def Blanked(self):
        """
        Checks if the contact is blanked or not

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
        Clears a flag on the contact

        Parameters
        ----------
        flag : Flag
            Flag to clear on the contact

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Constrained(self, connection=Oasys.gRPC.defaultArg):
        """
        see if tied/spotweld contact uses constrained formulation

        Parameters
        ----------
        connection : boolean
            Optional. if true will only consider contacts used for PRIMER connections. The default is false

        Returns
        -------
        bool
            logical
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Constrained", connection)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the contact. The target include of the copied contact can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        Contact
            Contact object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a contact

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the contact

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
        Extracts the actual colour used for contact.
        By default in PRIMER many entities such as elements get their colour automatically from the part that they are in.
        PRIMER cycles through 13 default colours based on the label of the entity. In this case the contact colour
        property will return the value Colour.PART instead of the actual colour.
        This method will return the actual colour which is used for drawing the contact

        Returns
        -------
        int
            colour value (integer)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ExtractColour")

    def Flagged(self, flag):
        """
        Checks if the contact is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the contact

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a contact

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a Contact property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the Contact.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            contact property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Interactions(self, type=Oasys.gRPC.defaultArg):
        """
        Returns a list of objects describing the interactions which can either be penetrations
        (tracked nodes that are tied to or penetrate elements in the contact) or crossed edges (contact segments that cross)

        Parameters
        ----------
        type : constant
            Optional. What type of interactions to return. Can be bitwise code of Contact.PENETRATIONS
            to return penetrations and Contact.CROSSED_EDGES to return crossed edges.
            If omitted penetrations will be returned

        Returns
        -------
        list
            List of dicts with properties
        """
        return Oasys.PRIMER._connection.instanceMethodStream(self.__class__.__name__, self._handle, "Interactions", type)

    def Keyword(self):
        """
        Returns the keyword for this Contact (\*BOUNDARY_PRESCRIBED_MOTION_xxxx).
        Note that a carriage return is not added.
        See also Contact.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the Contact.
        Note that a carriage return is not added.
        See also Contact.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next contact in the model

        Returns
        -------
        Contact
            Contact object (or None if there are no more contacts in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def PenCheck(self, flag, eflag):
        """
        Flags nodes that penetrate (or tie) in contact

        Parameters
        ----------
        flag : Flag
            Flag to be set on penetrating (or tied) node
        eflag : integer
            Optional flag for elements. If supplied, node will be flagged only
            if it penetrates (or ties to) an element that is flagged. Node and element
            flag may be the same

        Returns
        -------
        int
            zero if contact successfully checked
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "PenCheck", flag, eflag)

    def PenCheckEdit(self, modal=Oasys.gRPC.defaultArg, check_mode=Oasys.gRPC.defaultArg, mpp_threshold=Oasys.gRPC.defaultArg, report_crossed_3d_elems=Oasys.gRPC.defaultArg, contact_penchk_dup_shells=Oasys.gRPC.defaultArg):
        """
        launches the interactive edit panel for penetration check on the con

        Parameters
        ----------
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal
        check_mode : constant
            Optional. Check mode. Can be Model.MPP_MODE or
            Model.SMP_MODE.
            Default is set to the oa pref contact_check_mode
        mpp_threshold : real
            Optional. Can set the MPP threshold, by default this is set to the oa pref contact_mpp_penetration_threshold
        report_crossed_3d_elems : boolean
            Optional. Can set the value of reporting crossed elements to TRUE or FALSE, by default this is set to the oa pref report_crossed_3d_elems
        contact_penchk_dup_shells : constant
            Optional. Duplicate shell treatment Can be Model.SHELL_AUTO,
            Model.SHELL_THICK or
            Model.SHELL_THIN.
            Default is set to the oa pref contact_penchk_dup_shells

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "PenCheckEdit", modal, check_mode, mpp_threshold, report_crossed_3d_elems, contact_penchk_dup_shells)

    def Previous(self):
        """
        Returns the previous contact in the model

        Returns
        -------
        Contact
            Contact object (or None if there are no more contacts in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on the contact

        Parameters
        ----------
        flag : Flag
            Flag to set on the contact

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the contact. The contact will be sketched until you either call
        Contact.Unsketch(),
        Contact.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the contact is sketched.
            If omitted redraw is true. If you want to sketch several contacts and only
            redraw after the last one then use false for redraw and call
            View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Sketch", redraw)

    def StatusCheck(self):
        """
        Checks sliding contact for crossed edges and penetrations

        Returns
        -------
        list
            A list containing count of crossed edges, count of penetrations (note if a node penetrates more than one segment, it is only reported once here)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "StatusCheck")

    def Unblank(self):
        """
        Unblanks the contact

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank")

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the contact

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the contact is unsketched.
            If omitted redraw is true. If you want to unsketch several contacts and only
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
        Contact
            Contact object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this contact

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

