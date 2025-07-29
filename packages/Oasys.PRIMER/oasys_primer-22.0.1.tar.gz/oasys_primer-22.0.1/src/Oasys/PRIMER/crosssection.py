import Oasys.gRPC


# Metaclass for static properties and constants
class CrossSectionType(type):
    _consts = {'PLANE', 'SET'}

    def __getattr__(cls, name):
        if name in CrossSectionType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("CrossSection class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in CrossSectionType._consts:
            raise AttributeError("Cannot set CrossSection class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class CrossSection(Oasys.gRPC.OasysItem, metaclass=CrossSectionType):
    _props = {'bsid', 'colour', 'csid', 'dsid', 'heading', 'hsid', 'id', 'idset', 'include', 'itype', 'label', 'lenl', 'lenm', 'nsid', 'option', 'psid', 'radius', 'ssid', 'tsid', 'xch', 'xct', 'xhev', 'ych', 'yct', 'yhev', 'zch', 'zct', 'zhev'}
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
        if name in CrossSection._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in CrossSection._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("CrossSection instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in CrossSection._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in CrossSection._rprops:
            raise AttributeError("Cannot set read-only CrossSection instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, option, settings):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, option, settings)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new CrossSection object

        Parameters
        ----------
        model : Model
            Model that database cross section will be created in
        option : constant
            Database cross section type. Must be CrossSection.SET or CrossSection.PLANE
        settings : dict
            Options specifying various properties used to create the keyword. If optional values are not specified then their default values will be used

        Returns
        -------
        CrossSection
            CrossSection object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def BlankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the cross sections in the model

        Parameters
        ----------
        model : Model
            Model that all cross sections will be blanked in
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
        Blanks all of the flagged cross sections in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged cross sections will be blanked in
        flag : Flag
            Flag set on the cross sections that you want to blank
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
        Starts an interactive editing panel to create a cross section

        Parameters
        ----------
        model : Model
            Model that the cross section will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        CrossSection
            CrossSection object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def CreateAlongFeatureLine(model, nid1, options):
        """
        Creates a set of cross sections along a feature line and returns them as a list of CrossSection objects. Use Options.edge_angle 
        to control the break angle for the feature line search within this function

        Parameters
        ----------
        model : Model
            Model that the cross_section will be created in
        nid1 : integer
            ID of feature line starting node. The first cross section will be created at this Node's location
        options : dict
            Additional arguments for controlling how the cross sections are created

        Returns
        -------
        list
            List of CrossSection objects (or None if not made). Depending on the geometry of the model and the node provided for nid1, the list may contain less CrossSection objects than requested for the single node method
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "CreateAlongFeatureLine", model, nid1, options)

    def First(model):
        """
        Returns the first cross section in the model

        Parameters
        ----------
        model : Model
            Model to get first cross section in

        Returns
        -------
        CrossSection
            CrossSection object (or None if there are no cross sections in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FirstFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the first free cross section label in the model.
        Also see CrossSection.LastFreeLabel(),
        CrossSection.NextFreeLabel() and
        Model.FirstFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get first free cross section label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            First free in layer in editing panels). If omitted the whole model will be used (Equivalent to
            First free in editing panels)

        Returns
        -------
        int
            CrossSection label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FirstFreeLabel", model, layer)

    def FlagAll(model, flag):
        """
        Flags all of the cross sections in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all cross sections will be flagged in
        flag : Flag
            Flag to set on the cross sections

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of CrossSection objects or properties for all of the cross sections in a model in PRIMER.
        If the optional property argument is not given then a list of CrossSection objects is returned.
        If the property argument is given, that property value for each cross section is returned in the list
        instead of a CrossSection object

        Parameters
        ----------
        model : Model
            Model to get cross sections from
        property : string
            Optional. Name for property to get for all cross sections in the model

        Returns
        -------
        list
            List of CrossSection objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of CrossSection objects for all of the flagged cross sections in a model in PRIMER
        If the optional property argument is not given then a list of CrossSection objects is returned.
        If the property argument is given, then that property value for each cross section is returned in the list
        instead of a CrossSection object

        Parameters
        ----------
        model : Model
            Model to get cross sections from
        flag : Flag
            Flag set on the cross sections that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged cross sections in the model

        Returns
        -------
        list
            List of CrossSection objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the CrossSection object for a cross section ID

        Parameters
        ----------
        model : Model
            Model to find the cross section in
        number : integer
            number of the cross section you want the CrossSection object for

        Returns
        -------
        CrossSection
            CrossSection object (or None if cross section does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last cross section in the model

        Parameters
        ----------
        model : Model
            Model to get last cross section in

        Returns
        -------
        CrossSection
            CrossSection object (or None if there are no cross sections in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def LastFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the last free cross section label in the model.
        Also see CrossSection.FirstFreeLabel(),
        CrossSection.NextFreeLabel() and
        see Model.LastFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get last free cross section label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest free in layer in editing panels). If omitted the whole model will be used

        Returns
        -------
        int
            CrossSection label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "LastFreeLabel", model, layer)

    def NextFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the next free (highest+1) cross section label in the model.
        Also see CrossSection.FirstFreeLabel(),
        CrossSection.LastFreeLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get next free cross section label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest+1 in layer in editing panels). If omitted the whole model will be used (Equivalent to
            Highest+1 in editing panels)

        Returns
        -------
        int
            CrossSection label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NextFreeLabel", model, layer)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a cross section

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only cross sections from that model can be picked.
            If the argument is a Flag then only cross sections that
            are flagged with limit can be selected.
            If omitted, or None, any cross sections from any model can be selected.
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
        CrossSection
            CrossSection object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def RenumberAll(model, start):
        """
        Renumbers all of the cross sections in the model

        Parameters
        ----------
        model : Model
            Model that all cross sections will be renumbered in
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
        Renumbers all of the flagged cross sections in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged cross sections will be renumbered in
        flag : Flag
            Flag set on the cross sections that you want to renumber
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
        Allows the user to select cross sections using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting cross sections
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only cross sections from that model can be selected.
            If the argument is a Flag then only cross sections that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any cross sections can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of cross sections selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged cross sections in the model. The cross sections will be sketched until you either call
        CrossSection.Unsketch(),
        CrossSection.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged cross sections will be sketched in
        flag : Flag
            Flag set on the cross sections that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the cross sections are sketched.
            If omitted redraw is true. If you want to sketch flagged cross sections several times and only
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
        Returns the total number of cross sections in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing cross sections should be counted. If false or omitted
            referenced but undefined cross sections will also be included in the total

        Returns
        -------
        int
            number of cross sections
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnblankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the cross sections in the model

        Parameters
        ----------
        model : Model
            Model that all cross sections will be unblanked in
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
        Unblanks all of the flagged cross sections in the model

        Parameters
        ----------
        model : Model
            Model that the flagged cross sections will be unblanked in
        flag : Flag
            Flag set on the cross sections that you want to unblank
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
        Unsets a defined flag on all of the cross sections in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all cross sections will be unset in
        flag : Flag
            Flag to unset on the cross sections

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all cross sections

        Parameters
        ----------
        model : Model
            Model that all cross sections will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the cross sections are unsketched.
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
        Unsketches all flagged cross sections in the model

        Parameters
        ----------
        model : Model
            Model that all cross sections will be unsketched in
        flag : Flag
            Flag set on the cross sections that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the cross sections are unsketched.
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
        Associates a comment with a cross section

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the cross section

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def Autosize(self, options=Oasys.gRPC.defaultArg):
        """
        Autosizes a _PLANE cross section such that it cuts through all elements in model/psid along that plane

        Parameters
        ----------
        options : dict
            Optional. Object containing additional options

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Autosize", options)

    def Blank(self):
        """
        Blanks the cross section

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank")

    def Blanked(self):
        """
        Checks if the cross section is blanked or not

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
        Clears a flag on the cross section

        Parameters
        ----------
        flag : Flag
            Flag to clear on the cross section

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the cross section. The target include of the copied cross section can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        CrossSection
            CrossSection object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a cross section

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the cross section

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

    def ElemCut(self, shell_label):
        """
        Returns coordinates of the intersections between a shell and a database cross section. Note, ElemCut on the Shell class may be quicker

        Parameters
        ----------
        shell_label : integer
            The label of the shell

        Returns
        -------
        list
            A list containing the x1,y1,z1,x2,y2,z2 coordinates of the cut line, or None if it does not cut. Note this function does not check that the shell is in the cross section definition (part set)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ElemCut", shell_label)

    def ExtractColour(self):
        """
        Extracts the actual colour used for cross section.
        By default in PRIMER many entities such as elements get their colour automatically from the part that they are in.
        PRIMER cycles through 13 default colours based on the label of the entity. In this case the cross section colour
        property will return the value Colour.PART instead of the actual colour.
        This method will return the actual colour which is used for drawing the cross section

        Returns
        -------
        int
            colour value (integer)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ExtractColour")

    def FlagCut(self, flag):
        """
        Flags every element (solid,shell,tshell,beam) cut by the cross section. 
        Note this function does not check that the element is in the cross section definition (part set)

        Parameters
        ----------
        flag : Flag
            Flag bit

        Returns
        -------
        bool
            Boolean
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "FlagCut", flag)

    def Flagged(self, flag):
        """
        Checks if the cross section is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the cross section

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a cross section

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a CrossSection property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the CrossSection.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            cross section property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this cross_section (\*DATABASE_CROSS_SECTION).
        Note that a carriage return is not added.
        See also CrossSection.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the cross_section.
        Note that a carriage return is not added.
        See also CrossSection.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next cross section in the model

        Returns
        -------
        CrossSection
            CrossSection object (or None if there are no more cross sections in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def PartCut(self, part_label, flag=Oasys.gRPC.defaultArg):
        """
        Returns true if cross section is cutting the part, false otherwise. If option flag is active, will flag every element of the part cut by the cross section. 
        Note this function does not check that the part is in the cross section definition (part set)

        Parameters
        ----------
        part_label : integer
            The label of the part
        flag : Flag
            Optional. Optional Flag to flag the element which are cut by the cross section

        Returns
        -------
        bool
            Boolean
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "PartCut", part_label, flag)

    def Previous(self):
        """
        Returns the previous cross section in the model

        Returns
        -------
        CrossSection
            CrossSection object (or None if there are no more cross sections in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def Properties(self):
        """
        Returns an object which describe various cross section properties

        Returns
        -------
        dict
            Dict with properties
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Properties")

    def SetFlag(self, flag):
        """
        Sets a flag on the cross section

        Parameters
        ----------
        flag : Flag
            Flag to set on the cross section

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the cross section. The cross section will be sketched until you either call
        CrossSection.Unsketch(),
        CrossSection.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the cross section is sketched.
            If omitted redraw is true. If you want to sketch several cross sections and only
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
        Unblanks the cross section

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank")

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the cross section

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the cross section is unsketched.
            If omitted redraw is true. If you want to unsketch several cross sections and only
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
        CrossSection
            CrossSection object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this cross section

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

