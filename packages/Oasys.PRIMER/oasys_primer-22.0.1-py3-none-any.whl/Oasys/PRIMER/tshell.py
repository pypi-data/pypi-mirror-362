import Oasys.gRPC


# Metaclass for static properties and constants
class TshellType(type):

    def __getattr__(cls, name):

        raise AttributeError("Tshell class attribute '{}' does not exist".format(name))


class Tshell(Oasys.gRPC.OasysItem, metaclass=TshellType):
    _props = {'beta', 'beta_angle', 'colour', 'composite', 'eid', 'include', 'label', 'n1', 'n2', 'n3', 'n4', 'n5', 'n6', 'n7', 'n8', 'nip', 'pid', 'transparency'}
    _rprops = {'exists', 'model', 'nodes'}


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
        if name in Tshell._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in Tshell._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("Tshell instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Tshell._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in Tshell._rprops:
            raise AttributeError("Cannot set read-only Tshell instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, eid, pid, n1, n2, n3, n4, n5, n6, n7=Oasys.gRPC.defaultArg, n8=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, eid, pid, n1, n2, n3, n4, n5, n6, n7, n8)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new Tshell object. Use either 6 or 8 nodes when
        creating a new thick shell

        Parameters
        ----------
        model : Model
            Model that thick shell will be created in
        eid : integer
            Tshell number
        pid : integer
            Part number
        n1 : integer
            Node number 1
        n2 : integer
            Node number 2
        n3 : integer
            Node number 3
        n4 : integer
            Node number 4
        n5 : integer
            Node number 5
        n6 : integer
            Node number 6
        n7 : integer
            Optional. Node number 7
        n8 : integer
            Optional. Node number 8

        Returns
        -------
        Tshell
            Tshell object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def BlankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the thick shells in the model

        Parameters
        ----------
        model : Model
            Model that all thick shells will be blanked in
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
        Blanks all of the flagged thick shells in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged thick shells will be blanked in
        flag : Flag
            Flag set on the thick shells that you want to blank
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
        Starts an interactive editing panel to create a thick shell

        Parameters
        ----------
        model : Model
            Model that the thick shell will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        Tshell
            Tshell object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def FindTshellInBox(model, xmin, xmax, ymin, ymax, zmin, zmax, flag=Oasys.gRPC.defaultArg, excl=Oasys.gRPC.defaultArg, vis_only=Oasys.gRPC.defaultArg):
        """
        Returns a list of Tshell objects for the thick shells within a box.
        Please note this function provides a list of all thick shells that could potentially
        be in the box (using computationally cheap bounding box comparison) it is not
        a rigorous test of whether the thick shellis actually in the box.
        This may include tshells that are ostensibly outside box. The user should apply their own test.
        (this function is intended to provide an upper bound of elems to test)
        Setting the "excl" flag will require that the tshell is fully contained.
        but this may not capture all the tshells you want to process

        Parameters
        ----------
        model : Model
            Model designated model
        xmin : real
            Minimum bound in global x
        xmax : real
            Maximum bound in global x
        ymin : real
            Minimum bound in global y
        ymax : real
            Maximum bound in global y
        zmin : real
            Minimum bound in global z
        zmax : real
            Maximum bound in global z
        flag : integer
            Optional. Optional flag to restrict thick shells considered, if 0 all tshells considered
        excl : integer
            Optional. Optional flag ( 0) Apply inclusive selection
            ( 1) Apply exclusive selection
            inclusive selection means elements intersect box
            exclusive selection means elements contained in box
        vis_only : integer
            Optional. Optional flag to consider visible elements only (1), if (0) all elements considered

        Returns
        -------
        list
            List of Tshell objects
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FindTshellInBox", model, xmin, xmax, ymin, ymax, zmin, zmax, flag, excl, vis_only)

    def First(model):
        """
        Returns the first thick shell in the model

        Parameters
        ----------
        model : Model
            Model to get first thick shell in

        Returns
        -------
        Tshell
            Tshell object (or None if there are no thick shells in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FirstFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the first free thick shell label in the model.
        Also see Tshell.LastFreeLabel(),
        Tshell.NextFreeLabel() and
        Model.FirstFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get first free thick shell label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            First free in layer in editing panels). If omitted the whole model will be used (Equivalent to
            First free in editing panels)

        Returns
        -------
        int
            Tshell label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FirstFreeLabel", model, layer)

    def FlagAll(model, flag):
        """
        Flags all of the thick shells in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all thick shells will be flagged in
        flag : Flag
            Flag to set on the thick shells

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Tshell objects or properties for all of the thick shells in a model in PRIMER.
        If the optional property argument is not given then a list of Tshell objects is returned.
        If the property argument is given, that property value for each thick shell is returned in the list
        instead of a Tshell object

        Parameters
        ----------
        model : Model
            Model to get thick shells from
        property : string
            Optional. Name for property to get for all thick shells in the model

        Returns
        -------
        list
            List of Tshell objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Tshell objects for all of the flagged thick shells in a model in PRIMER
        If the optional property argument is not given then a list of Tshell objects is returned.
        If the property argument is given, then that property value for each thick shell is returned in the list
        instead of a Tshell object

        Parameters
        ----------
        model : Model
            Model to get thick shells from
        flag : Flag
            Flag set on the thick shells that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged thick shells in the model

        Returns
        -------
        list
            List of Tshell objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the Tshell object for a thick shell ID

        Parameters
        ----------
        model : Model
            Model to find the thick shell in
        number : integer
            number of the thick shell you want the Tshell object for

        Returns
        -------
        Tshell
            Tshell object (or None if thick shell does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last thick shell in the model

        Parameters
        ----------
        model : Model
            Model to get last thick shell in

        Returns
        -------
        Tshell
            Tshell object (or None if there are no thick shells in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def LastFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the last free thick shell label in the model.
        Also see Tshell.FirstFreeLabel(),
        Tshell.NextFreeLabel() and
        see Model.LastFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get last free thick shell label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest free in layer in editing panels). If omitted the whole model will be used

        Returns
        -------
        int
            Tshell label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "LastFreeLabel", model, layer)

    def NextFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the next free (highest+1) thick shell label in the model.
        Also see Tshell.FirstFreeLabel(),
        Tshell.LastFreeLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get next free thick shell label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest+1 in layer in editing panels). If omitted the whole model will be used (Equivalent to
            Highest+1 in editing panels)

        Returns
        -------
        int
            Tshell label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NextFreeLabel", model, layer)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a thick shell

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only thick shells from that model can be picked.
            If the argument is a Flag then only thick shells that
            are flagged with limit can be selected.
            If omitted, or None, any thick shells from any model can be selected.
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
        Tshell
            Tshell object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def RenumberAll(model, start):
        """
        Renumbers all of the thick shells in the model

        Parameters
        ----------
        model : Model
            Model that all thick shells will be renumbered in
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
        Renumbers all of the flagged thick shells in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged thick shells will be renumbered in
        flag : Flag
            Flag set on the thick shells that you want to renumber
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
        Allows the user to select thick shells using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting thick shells
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only thick shells from that model can be selected.
            If the argument is a Flag then only thick shells that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any thick shells can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of thick shells selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged thick shells in the model. The thick shells will be sketched until you either call
        Tshell.Unsketch(),
        Tshell.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged thick shells will be sketched in
        flag : Flag
            Flag set on the thick shells that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the thick shells are sketched.
            If omitted redraw is true. If you want to sketch flagged thick shells several times and only
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
        Returns the total number of thick shells in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing thick shells should be counted. If false or omitted
            referenced but undefined thick shells will also be included in the total

        Returns
        -------
        int
            number of thick shells
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnblankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the thick shells in the model

        Parameters
        ----------
        model : Model
            Model that all thick shells will be unblanked in
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
        Unblanks all of the flagged thick shells in the model

        Parameters
        ----------
        model : Model
            Model that the flagged thick shells will be unblanked in
        flag : Flag
            Flag set on the thick shells that you want to unblank
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
        Unsets a defined flag on all of the thick shells in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all thick shells will be unset in
        flag : Flag
            Flag to unset on the thick shells

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all thick shells

        Parameters
        ----------
        model : Model
            Model that all thick shells will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the thick shells are unsketched.
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
        Unsketches all flagged thick shells in the model

        Parameters
        ----------
        model : Model
            Model that all thick shells will be unsketched in
        flag : Flag
            Flag set on the thick shells that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the thick shells are unsketched.
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
    def AspectRatio(self):
        """
        Calculates the aspect ratio for the thick shell

        Returns
        -------
        float
            float
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AspectRatio")

    def AssociateComment(self, comment):
        """
        Associates a comment with a thick shell

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the thick shell

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def Blank(self):
        """
        Blanks the thick shell

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank")

    def Blanked(self):
        """
        Checks if the thick shell is blanked or not

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
        Clears a flag on the thick shell

        Parameters
        ----------
        flag : Flag
            Flag to clear on the thick shell

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the thick shell. The target include of the copied thick shell can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        Tshell
            Tshell object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a thick shell

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the thick shell

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

    def ElemCut(self, database_cross_section_label):
        """
        Returns coordinates of the intersections between a thick shell and a database cross section

        Parameters
        ----------
        database_cross_section_label : integer
            The label of the database cross section

        Returns
        -------
        dict
            Dict with properties
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ElemCut", database_cross_section_label)

    def ExtractColour(self):
        """
        Extracts the actual colour used for thick shell.
        By default in PRIMER many entities such as elements get their colour automatically from the part that they are in.
        PRIMER cycles through 13 default colours based on the label of the entity. In this case the thick shell colour
        property will return the value Colour.PART instead of the actual colour.
        This method will return the actual colour which is used for drawing the thick shell

        Returns
        -------
        int
            colour value (integer)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ExtractColour")

    def Flagged(self, flag):
        """
        Checks if the thick shell is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the thick shell

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a thick shell

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetCompositeData(self, ipt):
        """
        Returns the composite data for an integration point in \*ELEMENT_TSHELL_COMPOSITE

        Parameters
        ----------
        ipt : integer
            The integration point you want the data for. Note that integration points start at 0, not 1

        Returns
        -------
        list
            A list of numbers containing the material id, thickness and beta angle
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetCompositeData", ipt)

    def GetNodeIDs(self):
        """
        Returns the labels of the nodes on the thick shell as a list.
        See also Tshell.GetNodes()

        Returns
        -------
        int
            List of node labels (integers)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetNodeIDs")

    def GetNodes(self):
        """
        Returns the nodes on the thick shell as a list of Node objects.
        See also Tshell.GetNodeIDs()

        Returns
        -------
        list
            List of Node objects
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetNodes")

    def GetParameter(self, prop):
        """
        Checks if a Tshell property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the Tshell.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            thick shell property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Jacobian(self):
        """
        Calculates the jacobian for the thick shell

        Returns
        -------
        float
            float
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Jacobian")

    def Keyword(self):
        """
        Returns the keyword for this thick shell (\*ELEMENT_TSHELL or \*ELEMENT_TSHELL_COMPOSITE).
        Note that a carriage return is not added.
        See also Tshell.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the thick shell.
        Note that a carriage return is not added.
        See also Tshell.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next thick shell in the model

        Returns
        -------
        Tshell
            Tshell object (or None if there are no more thick shells in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous thick shell in the model

        Returns
        -------
        Tshell
            Tshell object (or None if there are no more thick shells in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def RemoveCompositeData(self, ipt):
        """
        Removes the composite data for an integration point in \*ELEMENT_TSHELL_COMPOSITE

        Parameters
        ----------
        ipt : integer
            The integration point you want to remove.
            Note that integration points start at 0, not 1

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "RemoveCompositeData", ipt)

    def SetCompositeData(self, ipt, mid, thick, beta):
        """
        Sets the composite data for an integration point in \*ELEMENT_TSHELL_COMPOSITE

        Parameters
        ----------
        ipt : integer
            The integration point you want to set the data for.
            Note that integration points start at 0, not 1
        mid : integer
            Material ID for the integration point
        thick : real
            Thickness of the integration point
        beta : real
            Material angle of the integration point

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetCompositeData", ipt, mid, thick, beta)

    def SetFlag(self, flag):
        """
        Sets a flag on the thick shell

        Parameters
        ----------
        flag : Flag
            Flag to set on the thick shell

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the thick shell. The thick shell will be sketched until you either call
        Tshell.Unsketch(),
        Tshell.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the thick shell is sketched.
            If omitted redraw is true. If you want to sketch several thick shells and only
            redraw after the last one then use false for redraw and call
            View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Sketch", redraw)

    def Timestep(self):
        """
        Calculates the timestep for the thick shell

        Returns
        -------
        float
            float
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Timestep")

    def Unblank(self):
        """
        Unblanks the thick shell

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank")

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the thick shell

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the thick shell is unsketched.
            If omitted redraw is true. If you want to unsketch several thick shells and only
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
        Tshell
            Tshell object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Warpage(self):
        """
        Calculates the warpage for the thick shell

        Returns
        -------
        float
            float
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Warpage")

    def Xrefs(self):
        """
        Returns the cross references for this thick shell

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

