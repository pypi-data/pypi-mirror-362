import Oasys.gRPC


# Metaclass for static properties and constants
class SolidType(type):
    _consts = {'EDGE_1', 'EDGE_10', 'EDGE_11', 'EDGE_12', 'EDGE_2', 'EDGE_3', 'EDGE_4', 'EDGE_5', 'EDGE_6', 'EDGE_7', 'EDGE_8', 'EDGE_9', 'FACE_1', 'FACE_2', 'FACE_3', 'FACE_4', 'FACE_5', 'FACE_6'}

    def __getattr__(cls, name):
        if name in SolidType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("Solid class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in SolidType._consts:
            raise AttributeError("Cannot set Solid class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class Solid(Oasys.gRPC.OasysItem, metaclass=SolidType):
    _props = {'a1', 'a2', 'a3', 'colour', 'd1', 'd2', 'd3', 'dof', 'edges', 'eid', 'faces', 'h20', 'h27', 'h64', 'h8toh20', 'h8toh27', 'h8toh64', 'include', 'label', 'n1', 'n10', 'n11', 'n12', 'n13', 'n14', 'n15', 'n16', 'n17', 'n18', 'n19', 'n2', 'n20', 'n21', 'n22', 'n23', 'n24', 'n25', 'n26', 'n27', 'n28', 'n29', 'n3', 'n30', 'n31', 'n32', 'n33', 'n34', 'n35', 'n36', 'n37', 'n38', 'n39', 'n4', 'n40', 'n41', 'n42', 'n43', 'n44', 'n45', 'n46', 'n47', 'n48', 'n49', 'n5', 'n50', 'n51', 'n52', 'n53', 'n54', 'n55', 'n56', 'n57', 'n58', 'n59', 'n6', 'n60', 'n61', 'n62', 'n63', 'n64', 'n7', 'n8', 'n9', 'ns1', 'ns2', 'ns3', 'ns4', 'ns5', 'ns6', 'ns7', 'ns8', 'ortho', 'p21', 'p40', 'pid', 't15', 't20', 'tet4totet10', 'transparency'}
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
        if name in Solid._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in Solid._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("Solid instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Solid._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in Solid._rprops:
            raise AttributeError("Cannot set read-only Solid instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, options):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, options)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new Solid object. If you are creating a 4 noded solid either only give 4 nodes or give 8 nodes
        but make nodes 4 to 8 the same number. If you are creating a 6 noded solid either only give 6 nodes or give 8 nodes
        but make nodes 5 and 6 the same number and nodes 7 and 8 the same number

        Parameters
        ----------
        model : Model
            Model that solid will be created in
        options : dict
            Options for creating the solid

        Returns
        -------
        Solid
            Solid object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def BlankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the solids in the model

        Parameters
        ----------
        model : Model
            Model that all solids will be blanked in
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
        Blanks all of the flagged solids in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged solids will be blanked in
        flag : Flag
            Flag set on the solids that you want to blank
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

    def CoordsToIsoparametric(model, x, y, z, n1, n2, n3, n4):
        """
        Calculates the isoparametric coordinates for a point on 3 or 4 noded segment

        Parameters
        ----------
        model : Model
            Model designated model
        x : float
            X coordinate of point
        y : float
            Y coordinate of point
        z : float
            Z coordinate of point
        n1 : integer
            node 1 of segment
        n2 : integer
            node 2 of segment
        n3 : integer
            node 3 of segment
        n4 : integer
            node 4 of segment

        Returns
        -------
        list
            List containing s and t isoparametric coordinates and the distance the point is from the segment If it is not possible to calculate the isoparametric coordinates None is returned
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "CoordsToIsoparametric", model, x, y, z, n1, n2, n3, n4)

    def Create(model, modal=Oasys.gRPC.defaultArg):
        """
        Starts an interactive editing panel to create a solid

        Parameters
        ----------
        model : Model
            Model that the solid will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        Solid
            Solid object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def FindSolidInBox(model, xmin, xmax, ymin, ymax, zmin, zmax, flag=Oasys.gRPC.defaultArg, excl=Oasys.gRPC.defaultArg, vis_only=Oasys.gRPC.defaultArg):
        """
        Returns a list of Solid objects for the solids within a box.
        Please note this function provides a list of all solids that could potentially
        be in the box (using computationally cheap bounding box comparison) it is not
        a rigorous test of whether the solid is actually in the box.
        This may include solids that are ostensibly outside box. The user should apply their own test.
        (this function is intended to provide an upper bound of elems to test)
        Setting the "excl" flag will require that the solid is fully contained
        but this may not capture all the solids you want to process

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
            Optional. Optional flag to restrict solids considered, if 0 all solids considered
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
            List of Solid objects
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FindSolidInBox", model, xmin, xmax, ymin, ymax, zmin, zmax, flag, excl, vis_only)

    def First(model):
        """
        Returns the first solid in the model

        Parameters
        ----------
        model : Model
            Model to get first solid in

        Returns
        -------
        Solid
            Solid object (or None if there are no solids in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FirstFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the first free solid label in the model.
        Also see Solid.LastFreeLabel(),
        Solid.NextFreeLabel() and
        Model.FirstFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get first free solid label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            First free in layer in editing panels). If omitted the whole model will be used (Equivalent to
            First free in editing panels)

        Returns
        -------
        int
            Solid label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FirstFreeLabel", model, layer)

    def FlagAll(model, flag):
        """
        Flags all of the solids in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all solids will be flagged in
        flag : Flag
            Flag to set on the solids

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Solid objects or properties for all of the solids in a model in PRIMER.
        If the optional property argument is not given then a list of Solid objects is returned.
        If the property argument is given, that property value for each solid is returned in the list
        instead of a Solid object

        Parameters
        ----------
        model : Model
            Model to get solids from
        property : string
            Optional. Name for property to get for all solids in the model

        Returns
        -------
        list
            List of Solid objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Solid objects for all of the flagged solids in a model in PRIMER
        If the optional property argument is not given then a list of Solid objects is returned.
        If the property argument is given, then that property value for each solid is returned in the list
        instead of a Solid object

        Parameters
        ----------
        model : Model
            Model to get solids from
        flag : Flag
            Flag set on the solids that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged solids in the model

        Returns
        -------
        list
            List of Solid objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the Solid object for a solid ID

        Parameters
        ----------
        model : Model
            Model to find the solid in
        number : integer
            number of the solid you want the Solid object for

        Returns
        -------
        Solid
            Solid object (or None if solid does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last solid in the model

        Parameters
        ----------
        model : Model
            Model to get last solid in

        Returns
        -------
        Solid
            Solid object (or None if there are no solids in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def LastFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the last free solid label in the model.
        Also see Solid.FirstFreeLabel(),
        Solid.NextFreeLabel() and
        see Model.LastFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get last free solid label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest free in layer in editing panels). If omitted the whole model will be used

        Returns
        -------
        int
            Solid label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "LastFreeLabel", model, layer)

    def NextFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the next free (highest+1) solid label in the model.
        Also see Solid.FirstFreeLabel(),
        Solid.LastFreeLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get next free solid label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest+1 in layer in editing panels). If omitted the whole model will be used (Equivalent to
            Highest+1 in editing panels)

        Returns
        -------
        int
            Solid label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NextFreeLabel", model, layer)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a solid

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only solids from that model can be picked.
            If the argument is a Flag then only solids that
            are flagged with limit can be selected.
            If omitted, or None, any solids from any model can be selected.
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
        Solid
            Solid object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def RenumberAll(model, start):
        """
        Renumbers all of the solids in the model

        Parameters
        ----------
        model : Model
            Model that all solids will be renumbered in
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
        Renumbers all of the flagged solids in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged solids will be renumbered in
        flag : Flag
            Flag set on the solids that you want to renumber
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
        Allows the user to select solids using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting solids
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only solids from that model can be selected.
            If the argument is a Flag then only solids that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any solids can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of solids selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged solids in the model. The solids will be sketched until you either call
        Solid.Unsketch(),
        Solid.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged solids will be sketched in
        flag : Flag
            Flag set on the solids that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the solids are sketched.
            If omitted redraw is true. If you want to sketch flagged solids several times and only
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
        Returns the total number of solids in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing solids should be counted. If false or omitted
            referenced but undefined solids will also be included in the total

        Returns
        -------
        int
            number of solids
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnblankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the solids in the model

        Parameters
        ----------
        model : Model
            Model that all solids will be unblanked in
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
        Unblanks all of the flagged solids in the model

        Parameters
        ----------
        model : Model
            Model that the flagged solids will be unblanked in
        flag : Flag
            Flag set on the solids that you want to unblank
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
        Unsets a defined flag on all of the solids in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all solids will be unset in
        flag : Flag
            Flag to unset on the solids

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all solids

        Parameters
        ----------
        model : Model
            Model that all solids will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the solids are unsketched.
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
        Unsketches all flagged solids in the model

        Parameters
        ----------
        model : Model
            Model that all solids will be unsketched in
        flag : Flag
            Flag set on the solids that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the solids are unsketched.
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
        Calculates the aspect ratio for the solid

        Returns
        -------
        float
            float
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AspectRatio")

    def AssociateComment(self, comment):
        """
        Associates a comment with a solid

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the solid

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def Blank(self):
        """
        Blanks the solid

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank")

    def Blanked(self):
        """
        Checks if the solid is blanked or not

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
        Clears a flag on the solid

        Parameters
        ----------
        flag : Flag
            Flag to clear on the solid

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the solid. The target include of the copied solid can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        Solid
            Solid object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a solid

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the solid

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
        Returns coordinates of the intersections between a solid and a database cross section

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
        Extracts the actual colour used for solid.
        By default in PRIMER many entities such as elements get their colour automatically from the part that they are in.
        PRIMER cycles through 13 default colours based on the label of the entity. In this case the solid colour
        property will return the value Colour.PART instead of the actual colour.
        This method will return the actual colour which is used for drawing the solid

        Returns
        -------
        int
            colour value (integer)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ExtractColour")

    def Flagged(self, flag):
        """
        Checks if the solid is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the solid

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a solid

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a Solid property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the Solid.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            solid property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Jacobian(self):
        """
        Calculates the jacobian for the solid

        Returns
        -------
        float
            float
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Jacobian")

    def Keyword(self):
        """
        Returns the keyword for this solid (\*SOLID, \*SOLID_SCALAR or \*SOLID_SCALAR_VALUE).
        Note that a carriage return is not added.
        See also Solid.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the solid.
        Note that a carriage return is not added.
        See also Solid.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next solid in the model

        Returns
        -------
        Solid
            Solid object (or None if there are no more solids in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous solid in the model

        Returns
        -------
        Solid
            Solid object (or None if there are no more solids in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on the solid

        Parameters
        ----------
        flag : Flag
            Flag to set on the solid

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the solid. The solid will be sketched until you either call
        Solid.Unsketch(),
        Solid.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the solid is sketched.
            If omitted redraw is true. If you want to sketch several solids and only
            redraw after the last one then use false for redraw and call
            View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Sketch", redraw)

    def TetCollapse(self):
        """
        Calculates the tetrahedral collapse for the solid

        Returns
        -------
        float
            float
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "TetCollapse")

    def TiedNodeCheck(self, contact_label, flag, option1, option2):
        """
        Checks if nodes of solid are tied by contact or directly attached (non-zero option1)

        Parameters
        ----------
        contact_label : integer
            The label of the tied contact. If zero the tied contact is found for the solid by reverse lookup
        flag : Flag
            flag bit
        option1 : integer
            Directly tied node (logical OR) 0:NONE 1:NRB/C_EXNO 2:BEAM 4:SHELL 8:SOLID 16:TSHELL
        option2 : integer
            0:No action 1:report error if directly attached node (acc. option1) also captured by contact

        Returns
        -------
        str
            string
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "TiedNodeCheck", contact_label, flag, option1, option2)

    def Timestep(self):
        """
        Calculates the timestep for the solid

        Returns
        -------
        float
            float
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Timestep")

    def Unblank(self):
        """
        Unblanks the solid

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank")

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the solid

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the solid is unsketched.
            If omitted redraw is true. If you want to unsketch several solids and only
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
        Solid
            Solid object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Volume(self):
        """
        Calculates the volume for the solid

        Returns
        -------
        float
            float
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Volume")

    def Warpage(self):
        """
        Calculates the warpage for the solid

        Returns
        -------
        float
            float
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Warpage")

    def Xrefs(self):
        """
        Returns the cross references for this solid

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

