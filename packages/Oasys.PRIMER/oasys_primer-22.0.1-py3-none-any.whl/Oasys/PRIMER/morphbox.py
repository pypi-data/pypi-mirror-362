import Oasys.gRPC


# Metaclass for static properties and constants
class MorphBoxType(type):

    def __getattr__(cls, name):

        raise AttributeError("MorphBox class attribute '{}' does not exist".format(name))


class MorphBox(Oasys.gRPC.OasysItem, metaclass=MorphBoxType):
    _props = {'include', 'label'}
    _rprops = {'exists', 'model', 'nx', 'ny', 'nz', 'setid'}


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
        if name in MorphBox._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in MorphBox._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("MorphBox instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in MorphBox._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in MorphBox._rprops:
            raise AttributeError("Cannot set read-only MorphBox instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, label, flag, options=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, label, flag, options)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new MorphBox object around flagged items

        Parameters
        ----------
        model : Model
            Model that morph box will be created in
        label : integer
            MorphBox number
        flag : Flag
            Flag set on the entities (for example nodes, elements and/or parts) that you want to create the box around
        options : dict
            Optional. Options to create the box

        Returns
        -------
        MorphBox
            MorphBox object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def BlankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the boxs in the model

        Parameters
        ----------
        model : Model
            Model that all boxs will be blanked in
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
        Blanks all of the flagged boxs in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged boxs will be blanked in
        flag : Flag
            Flag set on the boxs that you want to blank
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
        Returns the first box in the model

        Parameters
        ----------
        model : Model
            Model to get first box in

        Returns
        -------
        MorphBox
            MorphBox object (or None if there are no boxs in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FirstFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the first free box label in the model.
        Also see MorphBox.LastFreeLabel(),
        MorphBox.NextFreeLabel() and
        Model.FirstFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get first free box label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            First free in layer in editing panels). If omitted the whole model will be used (Equivalent to
            First free in editing panels)

        Returns
        -------
        int
            MorphBox label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FirstFreeLabel", model, layer)

    def FlagAll(model, flag):
        """
        Flags all of the boxs in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all boxs will be flagged in
        flag : Flag
            Flag to set on the boxs

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def FlagAllMorphedConnections(model, flag):
        """
        Flags all connections, in a given model, that have been morphed since their last remake. This 
        includes connections that have been morphed by a morph box that has since been deleted

        Parameters
        ----------
        model : Model
            Model containing desired connections
        flag : integer
            Flag to mark morphed connections

        Returns
        -------
        bool
            True if successful, False if not
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAllMorphedConnections", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of MorphBox objects or properties for all of the boxs in a model in PRIMER.
        If the optional property argument is not given then a list of MorphBox objects is returned.
        If the property argument is given, that property value for each box is returned in the list
        instead of a MorphBox object

        Parameters
        ----------
        model : Model
            Model to get boxs from
        property : string
            Optional. Name for property to get for all boxs in the model

        Returns
        -------
        list
            List of MorphBox objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of MorphBox objects for all of the flagged boxs in a model in PRIMER
        If the optional property argument is not given then a list of MorphBox objects is returned.
        If the property argument is given, then that property value for each box is returned in the list
        instead of a MorphBox object

        Parameters
        ----------
        model : Model
            Model to get boxs from
        flag : Flag
            Flag set on the boxs that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged boxs in the model

        Returns
        -------
        list
            List of MorphBox objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the MorphBox object for a box ID

        Parameters
        ----------
        model : Model
            Model to find the box in
        number : integer
            number of the box you want the MorphBox object for

        Returns
        -------
        MorphBox
            MorphBox object (or None if box does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last box in the model

        Parameters
        ----------
        model : Model
            Model to get last box in

        Returns
        -------
        MorphBox
            MorphBox object (or None if there are no boxs in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def LastFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the last free box label in the model.
        Also see MorphBox.FirstFreeLabel(),
        MorphBox.NextFreeLabel() and
        see Model.LastFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get last free box label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest free in layer in editing panels). If omitted the whole model will be used

        Returns
        -------
        int
            MorphBox label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "LastFreeLabel", model, layer)

    def NextFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the next free (highest+1) box label in the model.
        Also see MorphBox.FirstFreeLabel(),
        MorphBox.LastFreeLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get next free box label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest+1 in layer in editing panels). If omitted the whole model will be used (Equivalent to
            Highest+1 in editing panels)

        Returns
        -------
        int
            MorphBox label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NextFreeLabel", model, layer)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a box

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only boxs from that model can be picked.
            If the argument is a Flag then only boxs that
            are flagged with limit can be selected.
            If omitted, or None, any boxs from any model can be selected.
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
        MorphBox
            MorphBox object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def RenumberAll(model, start):
        """
        Renumbers all of the boxs in the model

        Parameters
        ----------
        model : Model
            Model that all boxs will be renumbered in
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
        Renumbers all of the flagged boxs in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged boxs will be renumbered in
        flag : Flag
            Flag set on the boxs that you want to renumber
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
        Allows the user to select boxs using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting boxs
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only boxs from that model can be selected.
            If the argument is a Flag then only boxs that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any boxs can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of boxs selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SetMorphConnections(status):
        """
        Turns Morph Connections on/off

        Parameters
        ----------
        status : boolean
            true turns Morph Connections on.
            false turns Morph Connections off

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "SetMorphConnections", status)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged boxs in the model. The boxs will be sketched until you either call
        MorphBox.Unsketch(),
        MorphBox.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged boxs will be sketched in
        flag : Flag
            Flag set on the boxs that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the boxs are sketched.
            If omitted redraw is true. If you want to sketch flagged boxs several times and only
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
        Returns the total number of boxs in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing boxs should be counted. If false or omitted
            referenced but undefined boxs will also be included in the total

        Returns
        -------
        int
            number of boxs
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnblankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the boxs in the model

        Parameters
        ----------
        model : Model
            Model that all boxs will be unblanked in
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
        Unblanks all of the flagged boxs in the model

        Parameters
        ----------
        model : Model
            Model that the flagged boxs will be unblanked in
        flag : Flag
            Flag set on the boxs that you want to unblank
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
        Unsets a defined flag on all of the boxs in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all boxs will be unset in
        flag : Flag
            Flag to unset on the boxs

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all boxs

        Parameters
        ----------
        model : Model
            Model that all boxs will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the boxs are unsketched.
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
        Unsketches all flagged boxs in the model

        Parameters
        ----------
        model : Model
            Model that all boxs will be unsketched in
        flag : Flag
            Flag set on the boxs that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the boxs are unsketched.
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
    def ApplyMorphing(self, redraw=Oasys.gRPC.defaultArg):
        """
        Recalculates the X, Y and Z coordinates of all nodes linked to the
        morph box by the \*SET_NODE_COLUMN. This should be called when coordinates of
        morph points have changed and you wish to apply the morphing. If several morph
        point positions on the same box change, then it is more speed-efficient to call
        this function only once for the box

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not.
            If omitted redraw is false. If you want to apply the morphing to several boxes and only
            redraw after the last one then use false for all redraws apart from the last one.
            Alternatively you can redraw using Model.UpdateGraphics()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ApplyMorphing", redraw)

    def AssociateComment(self, comment):
        """
        Associates a comment with a box

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the box

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def Blank(self):
        """
        Blanks the box

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank")

    def Blanked(self):
        """
        Checks if the box is blanked or not

        Returns
        -------
        bool
            True if blanked, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blanked")

    def ClearFlag(self, flag):
        """
        Clears a flag on the box

        Parameters
        ----------
        flag : Flag
            Flag to clear on the box

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the box. The target include of the copied box can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        MorphBox
            MorphBox object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a box

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the box

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "DetachComment", comment)

    def FlagMorphedConnections(self, flag):
        """
        Flags all connections that have been morphed, by a givine morph box, since their last remake. 
        A connection could be morphed by one morph box and not another, therefore calling this function on two boxes 
        that share a connection may produce different results depending on which box the function is called for. 
        E.g. morb1 and morb2 share conx1, morb1 gets morphed whereas morb2 remains unchanged. Calling this function 
        for morb1 will flag conx1, however calling the function for morb2 won't flag conx1

        Parameters
        ----------
        flag : integer
            Flag to mark morphed connections

        Returns
        -------
        bool
            True if successful, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "FlagMorphedConnections", flag)

    def Flagged(self, flag):
        """
        Checks if the box is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the box

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a box

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a MorphBox property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the MorphBox.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            box property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def GetPoint(self, xindex, yindex, zindex):
        """
        Returns the morph point ID on the morph box at indices in X, Y and Z
        directions

        Parameters
        ----------
        xindex : integer
            Index of the point in X direction. Note that indices start at 0,
            so it should be 0 for the points with the smallest parameteric X coordinate
            and box.nx-1 for the points with the highest X
        yindex : integer
            Index of the point in Y direction. Note that indices start at 0,
            so it should be 0 for the points with the smallest parameteric Y coordinate
            and box.ny-1 for the points with the highest Y
        zindex : integer
            Index of the point in Z direction. Note that indices start at 0,
            so it should be 0 for the points with the smallest parameteric Z coordinate
            and box.nz-1 for the points with the highest Z

        Returns
        -------
        MorphPoint
            A MorphPoint object for the point on the box at given indices
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetPoint", xindex, yindex, zindex)

    def Keyword(self):
        """
        Returns the keyword for this morph box (\*MORPH_BOX or \*MORPH_BOX_HIGH_ORDER).
        Note that a carriage return is not added.
        See also MorphBox.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the morph box.
        Note that a carriage return is not added.
        See also MorphBox.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next box in the model

        Returns
        -------
        MorphBox
            MorphBox object (or None if there are no more boxs in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous box in the model

        Returns
        -------
        MorphBox
            MorphBox object (or None if there are no more boxs in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def Reset(self, redraw=Oasys.gRPC.defaultArg):
        """
        Resets the morph box to its initial position and updates the coordinates of all its nodes

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not.
            If omitted redraw is false. If you want to reset several boxes and only
            redraw after the last one then use false for all redraws apart from the last one.
            Alternatively you can redraw using Model.UpdateGraphics()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Reset", redraw)

    def SetFlag(self, flag):
        """
        Sets a flag on the box

        Parameters
        ----------
        flag : Flag
            Flag to set on the box

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def SetPointID(self, xindex, yindex, zindex, id):
        """
        Replaces the morph point ID on the list, whose size depends on the
        orders in X, Y and Z directions, with the given new ID

        Parameters
        ----------
        xindex : integer
            Index of the point in X direction. Note that indices start at 0,
            so it should be 0 for the points with the smallest parameteric X coordinate
            and box.nx-1 for the points with the highest X
        yindex : integer
            Index of the point in Y direction. Note that indices start at 0,
            so it should be 0 for the points with the smallest parameteric Y coordinate
            and box.ny-1 for the points with the highest Y
        zindex : integer
            Index of the point in Z direction. Note that indices start at 0,
            so it should be 0 for the points with the smallest parameteric Z coordinate
            and box.nz-1 for the points with the highest Z
        id : integer
            New MorphPoint id

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetPointID", xindex, yindex, zindex, id)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the box. The box will be sketched until you either call
        MorphBox.Unsketch(),
        MorphBox.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the box is sketched.
            If omitted redraw is true. If you want to sketch several boxs and only
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
        Unblanks the box

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank")

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the box

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the box is unsketched.
            If omitted redraw is true. If you want to unsketch several boxs and only
            redraw after the last one then use false for redraw and call
            View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unsketch", redraw)

    def UpdateParametricCoordinates(self):
        """
        Recalculates parametric X, Y, Z coordinates for each node in the \*SET_NODE_COLUMN
        associated with the morph box. This needs to be called whenever morph points on the
        box or their coordinates have been changed manually and you wish to keep all nodes
        at their intrinsic global X, Y, Z coordinates.
        Provided Morph Connections is on (see MorphBox.SetMorphConnections()),
        this will also force PRIMER to recalculate the parametric coordinates for any connections 
        in the morph box next time one of its morph points is moved

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "UpdateParametricCoordinates")

    def ViewParameters(self):
        """
        Object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. This function temporarily
        changes the behaviour so that if a property is a parameter the parameter name is returned instead.
        This can be used with 'method chaining' (see the example below) to make sure a property argument is correct

        Returns
        -------
        MorphBox
            MorphBox object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this box

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

