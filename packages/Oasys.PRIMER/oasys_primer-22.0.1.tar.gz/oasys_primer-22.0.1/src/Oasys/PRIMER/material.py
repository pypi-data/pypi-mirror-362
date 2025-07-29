import Oasys.gRPC


# Metaclass for static properties and constants
class MaterialType(type):

    def __getattr__(cls, name):

        raise AttributeError("Material class attribute '{}' does not exist".format(name))


class Material(Oasys.gRPC.OasysItem, metaclass=MaterialType):
    _props = {'addDamageGissmo', 'addErosion', 'colour', 'include', 'label', 'mid', 'properties', 'title', 'transparency', 'type', 'typeNumber'}
    _rprops = {'addKeywords', 'cols', 'exists', 'model', 'optionalCards', 'rows'}


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
        if name in Material._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in Material._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("Material instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Material._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in Material._rprops:
            raise AttributeError("Cannot set read-only Material instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, mid, type):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, mid, type)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new Material object

        Parameters
        ----------
        model : Model
            Model that material will be created in
        mid : integer or string
            Material number or character label
        type : string
            Material type. Either give the Ansys LS-DYNA material name or
            3 digit number

        Returns
        -------
        Material
            Material object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def BlankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the materials in the model

        Parameters
        ----------
        model : Model
            Model that all materials will be blanked in
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
        Blanks all of the flagged materials in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged materials will be blanked in
        flag : Flag
            Flag set on the materials that you want to blank
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
        Starts an interactive editing panel to create a material

        Parameters
        ----------
        model : Model
            Model that the material will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        Material
            Material object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def First(model):
        """
        Returns the first material in the model

        Parameters
        ----------
        model : Model
            Model to get first material in

        Returns
        -------
        Material
            Material object (or None if there are no materials in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FirstFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the first free material label in the model.
        Also see Material.LastFreeLabel(),
        Material.NextFreeLabel() and
        Model.FirstFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get first free material label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            First free in layer in editing panels). If omitted the whole model will be used (Equivalent to
            First free in editing panels)

        Returns
        -------
        int
            Material label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FirstFreeLabel", model, layer)

    def FlagAll(model, flag):
        """
        Flags all of the materials in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all materials will be flagged in
        flag : Flag
            Flag to set on the materials

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Material objects or properties for all of the materials in a model in PRIMER.
        If the optional property argument is not given then a list of Material objects is returned.
        If the property argument is given, that property value for each material is returned in the list
        instead of a Material object

        Parameters
        ----------
        model : Model
            Model to get materials from
        property : string
            Optional. Name for property to get for all materials in the model

        Returns
        -------
        list
            List of Material objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Material objects for all of the flagged materials in a model in PRIMER
        If the optional property argument is not given then a list of Material objects is returned.
        If the property argument is given, then that property value for each material is returned in the list
        instead of a Material object

        Parameters
        ----------
        model : Model
            Model to get materials from
        flag : Flag
            Flag set on the materials that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged materials in the model

        Returns
        -------
        list
            List of Material objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the Material object for a material ID

        Parameters
        ----------
        model : Model
            Model to find the material in
        number : integer
            number of the material you want the Material object for

        Returns
        -------
        Material
            Material object (or None if material does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last material in the model

        Parameters
        ----------
        model : Model
            Model to get last material in

        Returns
        -------
        Material
            Material object (or None if there are no materials in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def LastFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the last free material label in the model.
        Also see Material.FirstFreeLabel(),
        Material.NextFreeLabel() and
        see Model.LastFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get last free material label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest free in layer in editing panels). If omitted the whole model will be used

        Returns
        -------
        int
            Material label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "LastFreeLabel", model, layer)

    def NextFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the next free (highest+1) material label in the model.
        Also see Material.FirstFreeLabel(),
        Material.LastFreeLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get next free material label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest+1 in layer in editing panels). If omitted the whole model will be used (Equivalent to
            Highest+1 in editing panels)

        Returns
        -------
        int
            Material label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NextFreeLabel", model, layer)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a material

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only materials from that model can be picked.
            If the argument is a Flag then only materials that
            are flagged with limit can be selected.
            If omitted, or None, any materials from any model can be selected.
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
        Material
            Material object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def RenumberAll(model, start):
        """
        Renumbers all of the materials in the model

        Parameters
        ----------
        model : Model
            Model that all materials will be renumbered in
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
        Renumbers all of the flagged materials in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged materials will be renumbered in
        flag : Flag
            Flag set on the materials that you want to renumber
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
        Allows the user to select materials using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting materials
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only materials from that model can be selected.
            If the argument is a Flag then only materials that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any materials can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of materials selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged materials in the model. The materials will be sketched until you either call
        Material.Unsketch(),
        Material.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged materials will be sketched in
        flag : Flag
            Flag set on the materials that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the materials are sketched.
            If omitted redraw is true. If you want to sketch flagged materials several times and only
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
        Returns the total number of materials in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing materials should be counted. If false or omitted
            referenced but undefined materials will also be included in the total

        Returns
        -------
        int
            number of materials
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnblankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the materials in the model

        Parameters
        ----------
        model : Model
            Model that all materials will be unblanked in
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
        Unblanks all of the flagged materials in the model

        Parameters
        ----------
        model : Model
            Model that the flagged materials will be unblanked in
        flag : Flag
            Flag set on the materials that you want to unblank
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
        Unsets a defined flag on all of the materials in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all materials will be unset in
        flag : Flag
            Flag to unset on the materials

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all materials

        Parameters
        ----------
        model : Model
            Model that all materials will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the materials are unsketched.
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
        Unsketches all flagged materials in the model

        Parameters
        ----------
        model : Model
            Model that all materials will be unsketched in
        flag : Flag
            Flag set on the materials that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the materials are unsketched.
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
    def AddOptionalCards(self):
        """
        Adds any optional cards for the material.
        Some materials have extra optional cards in the input.
        If they are there Ansys LS-DYNA will read them but they are not required input. For example a material could have
        three required cards and one extra optional card. If PRIMER reads this material from a keyword file and it only has
        the three required cards then the properties in the material will only be defined for those cards. i.e. there
        will not be any properties in the material for the extra optional line.
        If you edit the material interactively in PRIMER then the extra optional card will be shown so you can add
        values if required. When writing the material to a keyword file the extra optional card will be omitted if
        none of the fields are used.
        If you want to add one of the properties for the extra optional card in JavaScript this method will
        ensure that the extra card is defined and the properties added to the material as zero values. You can then use
        Material.SetPropertyByIndex(), 
        Material.SetPropertyByName() or
        Material.SetPropertyByRowCol() as normal to set the properties.
        Also see the optionalCards property

        Returns
        -------
        None
            no return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AddOptionalCards")

    def AssociateComment(self, comment):
        """
        Associates a comment with a material

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the material

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def Blank(self):
        """
        Blanks the material

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank")

    def Blanked(self):
        """
        Checks if the material is blanked or not

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
        Clears a flag on the material

        Parameters
        ----------
        flag : Flag
            Flag to clear on the material

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the material. The target include of the copied material can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        Material
            Material object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def Density(self):
        """
        Get the density material

        Returns
        -------
        float
            float
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Density")

    def DetachComment(self, comment):
        """
        Detaches a comment from a material

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the material

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
        Extracts the actual colour used for material.
        By default in PRIMER many entities such as elements get their colour automatically from the part that they are in.
        PRIMER cycles through 13 default colours based on the label of the entity. In this case the material colour
        property will return the value Colour.PART instead of the actual colour.
        This method will return the actual colour which is used for drawing the material

        Returns
        -------
        int
            colour value (integer)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ExtractColour")

    def Flagged(self, flag):
        """
        Checks if the material is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the material

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetAddDamageGissmoData(self):
        """
        Returns the \*MAT_ADD_DAMAGE_GISSMO data of material

        Returns
        -------
        dict
            Dict with properties
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetAddDamageGissmoData")

    def GetAddErosionData(self):
        """
        Returns the \*MAT_ADD_EROSION data of material. Note that this method does not support pre-R11 properties

        Returns
        -------
        dict
            Dict with properties
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetAddErosionData")

    def GetComments(self):
        """
        Extracts the comments associated to a material

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a Material property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the Material.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            material property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def GetPropertyByIndex(self, index):
        """
        Returns the value of property at index index for this
        Material object or None if no property exists

        Parameters
        ----------
        index : integer
            The index of the property value to retrieve.
            (the number of properties can be found from properties)
            Note that indices start at 0. There is no link between indices and rows/columns so adjacent
            fields on a line for a material may not have adjacent indices

        Returns
        -------
        int
            Property value (float/integer)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetPropertyByIndex", index)

    def GetPropertyByName(self, acronym):
        """
        Returns the value of property string acronym for this
        Material object or None if no property exists

        Parameters
        ----------
        acronym : string
            The acronym of the property value to retrieve

        Returns
        -------
        int
            Property value (float/integer)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetPropertyByName", acronym)

    def GetPropertyByRowCol(self, row, col):
        """
        Returns the value of the property for row and col for this
        Material object or None if no property exists.
        Note that rows and columns start at 0

        Parameters
        ----------
        row : integer
            The row of the property value to retrieve
        col : integer
            The column of the property value to retrieve

        Returns
        -------
        int
            Property value (float/integer)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetPropertyByRowCol", row, col)

    def GetPropertyNameForIndex(self, index):
        """
        Returns the name of the property at index index for this
        Material object or None if there is no property

        Parameters
        ----------
        index : integer
            The index of the property name to retrieve.
            (the number of properties can be found from properties)
            Note that indices start at 0. There is no link between indices and rows/columns so adjacent
            fields on a line for a material may not have adjacent indices

        Returns
        -------
        str
            Property name (string)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetPropertyNameForIndex", index)

    def GetPropertyNameForRowCol(self, row, col):
        """
        Returns the name of the property at row and col for this
        Material object or None if there is no property.
        Note that rows and columns start at 0

        Parameters
        ----------
        row : integer
            The row of the property name to retrieve
        col : integer
            The column of the property name to retrieve

        Returns
        -------
        str
            Property name (string)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetPropertyNameForRowCol", row, col)

    def Keyword(self, index=Oasys.gRPC.defaultArg):
        """
        Returns the keyword for this material (e.g. \*MAT_RIGID, \*MAT_ELASTIC etc).
        Note that a carriage return is not added.
        See also Material.KeywordCards()

        Parameters
        ----------
        index : integer
            Optional. If this argument is not given then the material keyword is returned as normal.
            However if the material also has \*MAT_ADD_xxxx cards defined for it (e.g. \*MAT_ADD_EROSION) then the index can be
            used to return the title for the \*MAT_ADD card instead. The index value starts from zero. The number of \*MAT_ADD cards
            can be found from the addKeywords property

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword", index)

    def KeywordCards(self, index=Oasys.gRPC.defaultArg):
        """
        Returns the keyword cards for the material.
        Note that a carriage return is not added.
        See also Material.Keyword()

        Parameters
        ----------
        index : integer
            Optional. If this argument is not given then the material keyword cards are returned as normal.
            However if the material also has \*MAT_ADD_xxxx cards defined for it (e.g. \*MAT_ADD_EROSION) then the index can be
            used to return the cards for the \*MAT_ADD card instead. The index value starts from zero. The number of \*MAT_ADD cards
            can be found from the addKeywords property

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards", index)

    def Next(self):
        """
        Returns the next material in the model

        Returns
        -------
        Material
            Material object (or None if there are no more materials in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def PoissonsRatio(self):
        """
        Get Poissons ratio for the material

        Returns
        -------
        float
            float
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "PoissonsRatio")

    def Previous(self):
        """
        Returns the previous material in the model

        Returns
        -------
        Material
            Material object (or None if there are no more materials in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetAddDamageGissmoData(self, data):
        """
        Sets the \*MAT_ADD_DAMAGE_GISSMO data of material

        Parameters
        ----------
        data : dict
            Data returned from Material.GetAddDamageGissmoData

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetAddDamageGissmoData", data)

    def SetAddErosionData(self, data):
        """
        Sets the \*MAT_ADD_EROSION data of material. Note that this method does not support pre-R11 properties

        Parameters
        ----------
        data : dict
            Data returned from Material.GetAddErosionData

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetAddErosionData", data)

    def SetFlag(self, flag):
        """
        Sets a flag on the material

        Parameters
        ----------
        flag : Flag
            Flag to set on the material

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def SetPropertyByIndex(self, index, value):
        """
        Sets the value of property at index index for this Material object

        Parameters
        ----------
        index : integer
            The index of the property value to set.
            (the number of properties can be found from properties)
            Note that indices start at 0. There is no link between indices and rows/columns so adjacent
            fields on a line for a material may not have adjacent indices
        value : integer/float for numeric properties, string for character properties
            The value of the property to set

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetPropertyByIndex", index, value)

    def SetPropertyByName(self, acronym, value):
        """
        Sets the value of property string acronym for this Material object

        Parameters
        ----------
        acronym : string
            The acronym of the property value to set
        value : integer/float for numeric properties, string for character properties
            The value of the property to set

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetPropertyByName", acronym, value)

    def SetPropertyByRowCol(self, row, col, value):
        """
        Sets the value of the property for row and col for this
        Material object.Note that rows and columns start at 0

        Parameters
        ----------
        row : integer
            The row of the property value to set
        col : integer
            The column of the property value to set
        value : integer/float for numeric properties, string for character properties
            The value of the property to set

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetPropertyByRowCol", row, col, value)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the material. The material will be sketched until you either call
        Material.Unsketch(),
        Material.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the material is sketched.
            If omitted redraw is true. If you want to sketch several materials and only
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
        Unblanks the material

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank")

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the material

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the material is unsketched.
            If omitted redraw is true. If you want to unsketch several materials and only
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
        Material
            Material object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this material

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

    def YieldStress(self):
        """
        Get Yield stress for the material

        Returns
        -------
        float
            float
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "YieldStress")

    def YoungsModulus(self):
        """
        Get Youngs modulus for the material

        Returns
        -------
        float
            float
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "YoungsModulus")

