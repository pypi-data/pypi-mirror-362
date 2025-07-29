import Oasys.gRPC


# Metaclass for static properties and constants
class ShellType(type):
    _consts = {'EDGE_1', 'EDGE_2', 'EDGE_3', 'EDGE_4'}

    def __getattr__(cls, name):
        if name in ShellType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("Shell class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in ShellType._consts:
            raise AttributeError("Cannot set Shell class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class Shell(Oasys.gRPC.OasysItem, metaclass=ShellType):
    _props = {'beta', 'colour', 'composite', 'composite_long', 'dof', 'edges', 'eid', 'include', 'label', 'mcid', 'n1', 'n2', 'n3', 'n4', 'n5', 'n6', 'n7', 'n8', 'nip', 'ns1', 'ns2', 'ns3', 'ns4', 'offset', 'pid', 'shl4_to_shl8', 'thic1', 'thic2', 'thic3', 'thic4', 'thic5', 'thic6', 'thic7', 'thic8', 'thickness', 'transparency'}
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
        if name in Shell._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in Shell._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("Shell instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Shell._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in Shell._rprops:
            raise AttributeError("Cannot set read-only Shell instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, eid, pid, n1, n2, n3, n4=Oasys.gRPC.defaultArg, n5=Oasys.gRPC.defaultArg, n6=Oasys.gRPC.defaultArg, n7=Oasys.gRPC.defaultArg, n8=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, eid, pid, n1, n2, n3, n4, n5, n6, n7, n8)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new Shell object. Use either 3, 4, 6 or 8 nodes when
        creating a new shell. If you are creating a 3 noded shell either only give 3 nodes or give 4 nodes
        but make nodes 3 and 4 the same number. Similarly, 6 noded shells can be created with 6 node arguments
        or with 8 nodes but nodes 3 and 4 the same number and nodes 7 and 8 the same number

        Parameters
        ----------
        model : Model
            Model that shell will be created in
        eid : integer
            Shell number
        pid : integer
            Part number
        n1 : integer
            Node number 1
        n2 : integer
            Node number 2
        n3 : integer
            Node number 3
        n4 : integer
            Optional. Node number 4
        n5 : integer
            Optional. Node number 5
        n6 : integer
            Optional. Node number 6
        n7 : integer
            Optional. Node number 7
        n8 : integer
            Optional. Node number 8

        Returns
        -------
        Shell
            Shell object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def BlankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the shells in the model

        Parameters
        ----------
        model : Model
            Model that all shells will be blanked in
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
        Blanks all of the flagged shells in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged shells will be blanked in
        flag : Flag
            Flag set on the shells that you want to blank
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
        Starts an interactive editing panel to create a shell

        Parameters
        ----------
        model : Model
            Model that the shell will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        Shell
            Shell object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def FillHolesOnFlagged(model, flag, remeshhole, pid=Oasys.gRPC.defaultArg, max_hole_size=Oasys.gRPC.defaultArg, mesh_element_size=Oasys.gRPC.defaultArg, planarsurface=Oasys.gRPC.defaultArg):
        """
        Fills multiple holes using flagged shells

        Parameters
        ----------
        model : Model
            Model that all shells are in
        flag : Flag
            flag bit
        remeshhole : boolean
            TRUE if elements around the hole should be remeshed
        pid : integer
            Optional. Needs to be specified if RemeshHole is FALSE. Specifies the Part id where the mesh is filled
        max_hole_size : float
            Optional. Maximum size of the hole which is to be filled. If omitted a default size of 20.0 will be set
        mesh_element_size : float
            Optional. Element size of the mesh which fills the hole. If omitted a default size of 10.0 will be set
        planarsurface : boolean
            Optional. Needs to be specified if RemeshHole is TRUE. TRUE if we need to Use planar surface

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FillHolesOnFlagged", model, flag, remeshhole, pid, max_hole_size, mesh_element_size, planarsurface)

    def FindShellInBox(model, xmin, xmax, ymin, ymax, zmin, zmax, flag=Oasys.gRPC.defaultArg, excl=Oasys.gRPC.defaultArg, vis_only=Oasys.gRPC.defaultArg):
        """
        Returns a list of Shell objects for the shells within a box.
        Please note in (default) inclusive mode this function provides a list of all shells that could potentially
        be in the box (using computationally cheap bounding box comparison - local box vs main box). 
        NOTE - it is not a rigorous test of whether the shell is actually in the box.
        An extension of "spot_thickness" is applied to each local shell box. By default this is 10mm.
        You can use "Options.connection_max_thickness = x" to reduce this value.
        This may return shells that are ostensibly outside box. The user should apply their own test on each shell returned.
        The purpose of this function is to reduce the number of shells you need to test.
        Setting the exclusive option will only return shells that are fully contained in the main box
        This may not capture all the shells you want to process so must be used with care

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
            Optional. Optional flag to restrict shells considered, if 0 all shells considered
        excl : integer
            Optional. Optional flag ( 0) Apply inclusive selection with local box extension = "spot_thickness" (default 10)
            (-1) Apply inclusive selection with local box extension = 0.5\*shell thickness
            ( 1) Apply exclusive selection 
            inclusive selection means elements intersect box
            exclusive selection means elements contained in box
        vis_only : integer
            Optional. Optional flag to consider visible shells only (1), if (0) all shells considered

        Returns
        -------
        list
            List of Shell objects
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FindShellInBox", model, xmin, xmax, ymin, ymax, zmin, zmax, flag, excl, vis_only)

    def First(model):
        """
        Returns the first shell in the model

        Parameters
        ----------
        model : Model
            Model to get first shell in

        Returns
        -------
        Shell
            Shell object (or None if there are no shells in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FirstFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the first free shell label in the model.
        Also see Shell.LastFreeLabel(),
        Shell.NextFreeLabel() and
        Model.FirstFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get first free shell label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            First free in layer in editing panels). If omitted the whole model will be used (Equivalent to
            First free in editing panels)

        Returns
        -------
        int
            Shell label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FirstFreeLabel", model, layer)

    def FlagAll(model, flag):
        """
        Flags all of the shells in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all shells will be flagged in
        flag : Flag
            Flag to set on the shells

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Shell objects or properties for all of the shells in a model in PRIMER.
        If the optional property argument is not given then a list of Shell objects is returned.
        If the property argument is given, that property value for each shell is returned in the list
        instead of a Shell object

        Parameters
        ----------
        model : Model
            Model to get shells from
        property : string
            Optional. Name for property to get for all shells in the model

        Returns
        -------
        list
            List of Shell objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Shell objects for all of the flagged shells in a model in PRIMER
        If the optional property argument is not given then a list of Shell objects is returned.
        If the property argument is given, then that property value for each shell is returned in the list
        instead of a Shell object

        Parameters
        ----------
        model : Model
            Model to get shells from
        flag : Flag
            Flag set on the shells that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged shells in the model

        Returns
        -------
        list
            List of Shell objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the Shell object for a shell ID

        Parameters
        ----------
        model : Model
            Model to find the shell in
        number : integer
            number of the shell you want the Shell object for

        Returns
        -------
        Shell
            Shell object (or None if shell does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last shell in the model

        Parameters
        ----------
        model : Model
            Model to get last shell in

        Returns
        -------
        Shell
            Shell object (or None if there are no shells in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def LastFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the last free shell label in the model.
        Also see Shell.FirstFreeLabel(),
        Shell.NextFreeLabel() and
        see Model.LastFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get last free shell label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest free in layer in editing panels). If omitted the whole model will be used

        Returns
        -------
        int
            Shell label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "LastFreeLabel", model, layer)

    def MakeConsistentNormalsFlagged(model, flag, shell_label=Oasys.gRPC.defaultArg):
        """
        Make all the flagged SHELL normals consistent with a selected one, the Seed Element

        Parameters
        ----------
        model : Model
            Model that all shells are in
        flag : Flag
            flag bit
        shell_label : integer
            Optional. The label of the seed shell. If omitted, or None, the first flagged shell is used as the seed shell

        Returns
        -------
        list
            List containing the labels of shells which have had normals reversed
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "MakeConsistentNormalsFlagged", model, flag, shell_label)

    def NextFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the next free (highest+1) shell label in the model.
        Also see Shell.FirstFreeLabel(),
        Shell.LastFreeLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get next free shell label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest+1 in layer in editing panels). If omitted the whole model will be used (Equivalent to
            Highest+1 in editing panels)

        Returns
        -------
        int
            Shell label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NextFreeLabel", model, layer)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a shell

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only shells from that model can be picked.
            If the argument is a Flag then only shells that
            are flagged with limit can be selected.
            If omitted, or None, any shells from any model can be selected.
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
        Shell
            Shell object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def PickIsoparametric(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a point on a shell. The isoparametric coordinates of the point picked on the
        shell are returned as well as the shell picked. These coordinates are suitable for using in the function
        Shell.IsoparametricToCoords().
        See also Shell.Pick()

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only shells from that model can be picked.
            If the argument is a Flag then only shells that
            are flagged with limit can be selected.
            If omitted, or None, any shells from any model can be selected.
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
        list
            List containing Shell object and isoparametric coordinates (or None if not picked or the point is not on a shell)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "PickIsoparametric", prompt, limit, modal, button_text)

    def RenumberAll(model, start):
        """
        Renumbers all of the shells in the model

        Parameters
        ----------
        model : Model
            Model that all shells will be renumbered in
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
        Renumbers all of the flagged shells in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged shells will be renumbered in
        flag : Flag
            Flag set on the shells that you want to renumber
        start : integer
            Start point for renumbering

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "RenumberFlagged", model, flag, start)

    def ReverseNormalsFlagged(model, flag):
        """
        Reverse all the flagged shell normals

        Parameters
        ----------
        model : Model
            Model that all shells are in
        flag : Flag
            flag bit

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "ReverseNormalsFlagged", model, flag)

    def Select(flag, prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg):
        """
        Allows the user to select shells using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting shells
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only shells from that model can be selected.
            If the argument is a Flag then only shells that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any shells can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of shells selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged shells in the model. The shells will be sketched until you either call
        Shell.Unsketch(),
        Shell.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged shells will be sketched in
        flag : Flag
            Flag set on the shells that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the shells are sketched.
            If omitted redraw is true. If you want to sketch flagged shells several times and only
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
        Returns the total number of shells in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing shells should be counted. If false or omitted
            referenced but undefined shells will also be included in the total

        Returns
        -------
        int
            number of shells
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnblankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the shells in the model

        Parameters
        ----------
        model : Model
            Model that all shells will be unblanked in
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
        Unblanks all of the flagged shells in the model

        Parameters
        ----------
        model : Model
            Model that the flagged shells will be unblanked in
        flag : Flag
            Flag set on the shells that you want to unblank
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
        Unsets a defined flag on all of the shells in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all shells will be unset in
        flag : Flag
            Flag to unset on the shells

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all shells

        Parameters
        ----------
        model : Model
            Model that all shells will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the shells are unsketched.
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
        Unsketches all flagged shells in the model

        Parameters
        ----------
        model : Model
            Model that all shells will be unsketched in
        flag : Flag
            Flag set on the shells that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the shells are unsketched.
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
    def Angles(self):
        """
        Calculates the minimum and maximum internal angles (in degrees) for the shell

        Returns
        -------
        int
            List of numbers containing min and max angles
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Angles")

    def Area(self):
        """
        Calculates the area for the shell

        Returns
        -------
        float
            float
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Area")

    def AspectRatio(self):
        """
        Calculates the aspect ratio for the shell

        Returns
        -------
        float
            float
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AspectRatio")

    def AssociateComment(self, comment):
        """
        Associates a comment with a shell

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the shell

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def Blank(self):
        """
        Blanks the shell

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank")

    def Blanked(self):
        """
        Checks if the shell is blanked or not

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
        Clears a flag on the shell

        Parameters
        ----------
        flag : Flag
            Flag to clear on the shell

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def CoordsToIsoparametric(self, x, y, z):
        """
        Calculates the isoparametric coordinates for a point on the shell

        Parameters
        ----------
        x : float
            X coordinate of point
        y : float
            Y coordinate of point
        z : float
            Z coordinate of point

        Returns
        -------
        list
            List containing s and t isoparametric coordinates and the distance the point is from the shell (positive in direction of shell normal). If it is not possible to calculate the isoparametric coordinates None is returned
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "CoordsToIsoparametric", x, y, z)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the shell. The target include of the copied shell can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        Shell
            Shell object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a shell

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the shell

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
        Returns coordinates of the intersections between a shell and a database cross section

        Parameters
        ----------
        database_cross_section_label : integer
            The label of the database cross section

        Returns
        -------
        list
            A list containing the x1,y1,z1,x2,y2,z2 coordinates of the cut line, or None if it does not cut. Note this function does not check that the shell is in the cross section definition (part set)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ElemCut", database_cross_section_label)

    def ExtractColour(self):
        """
        Extracts the actual colour used for shell.
        By default in PRIMER many entities such as elements get their colour automatically from the part that they are in.
        PRIMER cycles through 13 default colours based on the label of the entity. In this case the shell colour
        property will return the value Colour.PART instead of the actual colour.
        This method will return the actual colour which is used for drawing the shell

        Returns
        -------
        int
            colour value (integer)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ExtractColour")

    def FillAttachedHole(self, pid, size):
        """
        Fills in (meshes) a hole attached to the shell

        Parameters
        ----------
        pid : integer
            The Part number that the new shells will be created in
        size : float
            The size for created elements

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "FillAttachedHole", pid, size)

    def Flagged(self, flag):
        """
        Checks if the shell is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the shell

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetAttachedShells(self, tolerance=Oasys.gRPC.defaultArg, recursive=Oasys.gRPC.defaultArg):
        """
        Returns the shells that are attached to the shell. Note that 'attached' means that the
        shells must share 2 nodes

        Parameters
        ----------
        tolerance : float
            Optional. This tolerance can be used to limit the selection to shells whose
            normal vector is within this tolerance (in degrees) of the original shell. If omitted the tolerance is
            180 degrees
        recursive : boolean
            Optional. If recursive is false then only the shells actually attached to the shell will be
            returned (this could also be done by using the Xrefs class but this method
            is provided for convenience.
            If recursive is true then PRIMER will keep finding attached shells until no more can be found.
            If omitted recursive will be false

        Returns
        -------
        list
            List of Shell objects (or None if there are no attached shells)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetAttachedShells", tolerance, recursive)

    def GetComments(self):
        """
        Extracts the comments associated to a shell

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetCompositeData(self, ipt):
        """
        Returns the composite data for an integration point in \*ELEMENT_SHELL_COMPOSITE

        Parameters
        ----------
        ipt : integer
            The integration point you want the data for. Note that integration points start at 0, not 1

        Returns
        -------
        list
            A list containing the material ID, thickness and beta angle values. If the _COMPOSITE_LONG option is set, then the list returned will also contain the ply ID
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetCompositeData", ipt)

    def GetNodeIDs(self):
        """
        Returns the labels of the nodes on the shell as a list.
        See also Shell.GetNodes()

        Returns
        -------
        int
            List of node labels (integers)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetNodeIDs")

    def GetNodes(self):
        """
        Returns the nodes on the shell as a list of Node objects.
        See also Shell.GetNodeIDs()

        Returns
        -------
        list
            List of Node objects
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetNodes")

    def GetParameter(self, prop):
        """
        Checks if a Shell property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the Shell.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            shell property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def GetShellReferenceGeometry(self):
        """
        Returns the airbag shell reference geometry of the shell

        Returns
        -------
        int
            The shell reference geometry ID of the shell (or 0 if it hasn't got any)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetShellReferenceGeometry")

    def IsoparametricToCoords(self, s, t):
        """
        Calculates the coordinates for a point on the shell from the isoparametric coords

        Parameters
        ----------
        s : float
            First isoparametric coordinate
        t : float
            Second isoparametric coordinate

        Returns
        -------
        int
            List of numbers containing x, y and z or None if not possible to calculate
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "IsoparametricToCoords", s, t)

    def Jacobian(self):
        """
        Calculates the jacobian for the shell

        Returns
        -------
        float
            float
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Jacobian")

    def Keyword(self):
        """
        Returns the keyword for this shell (\*SHELL, \*SHELL_SCALAR or \*SHELL_SCALAR_VALUE).
        Note that a carriage return is not added.
        See also Shell.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the shell.
        Note that a carriage return is not added.
        See also Shell.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Length(self):
        """
        Calculates the minimum length for the shell

        Returns
        -------
        float
            float
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Length")

    def Next(self):
        """
        Returns the next shell in the model

        Returns
        -------
        Shell
            Shell object (or None if there are no more shells in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def NormalVector(self):
        """
        Calculates the unit normal vector for the shell

        Returns
        -------
        int
            List of numbers containing x, y and z components of unit normal vector or None if the vector cannot be calculated (for example if the shell has zero area)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "NormalVector")

    def Previous(self):
        """
        Returns the previous shell in the model

        Returns
        -------
        Shell
            Shell object (or None if there are no more shells in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def RemoveCompositeData(self, ipt):
        """
        Removes the composite data for an integration point in \*ELEMENT_SHELL_COMPOSITE

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

    def ReverseNormal(self, redraw=Oasys.gRPC.defaultArg):
        """
        Reverse shell normal

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not.
            If omitted redraw is false. If you want to reverse several shell normals and only
            redraw after the last one then use false for all redraws apart from the last one

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ReverseNormal", redraw)

    def SetCompositeData(self, ipt, mid, thick, beta, plyid=Oasys.gRPC.defaultArg):
        """
        Sets the composite data for an integration point in \*ELEMENT_SHELL_COMPOSITE

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
        plyid : integer
            Optional. Ply ID for the integration point. This should be used if the _COMPOSITE_LONG option is set for the shell

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetCompositeData", ipt, mid, thick, beta, plyid)

    def SetFlag(self, flag):
        """
        Sets a flag on the shell

        Parameters
        ----------
        flag : Flag
            Flag to set on the shell

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the shell. The shell will be sketched until you either call
        Shell.Unsketch(),
        Shell.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the shell is sketched.
            If omitted redraw is true. If you want to sketch several shells and only
            redraw after the last one then use false for redraw and call
            View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Sketch", redraw)

    def Skew(self):
        """
        Calculates the skew for the shell

        Returns
        -------
        float
            float
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Skew")

    def Taper(self):
        """
        Calculates the taper for the shell

        Returns
        -------
        float
            float
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Taper")

    def TiedNodeCheck(self, contact_label, flag, option1, option2):
        """
        Checks if nodes of shell are tied by contact or directly attached (non-zero option1)

        Parameters
        ----------
        contact_label : integer
            The label of the tied contact. If zero the tied contact is found for the shell by reverse lookup
        flag : Flag
            flag bit
        option1 : integer
            Directly tied node (logical OR) 0:NONE 1:NRB/C_EXNO 2:BEAM 4:SHELL 8:SOLID 16:TSHELL
        option2 : integer
            0:No action 1: report error if directly attached node (acc. option1) captured by contact

        Returns
        -------
        str
            string
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "TiedNodeCheck", contact_label, flag, option1, option2)

    def Timestep(self):
        """
        Calculates the timestep for the shell

        Returns
        -------
        float
            float
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Timestep")

    def Unblank(self):
        """
        Unblanks the shell

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank")

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the shell

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the shell is unsketched.
            If omitted redraw is true. If you want to unsketch several shells and only
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
        Shell
            Shell object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Warpage(self):
        """
        Calculates the warpage for the shell

        Returns
        -------
        float
            float
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Warpage")

    def WeightingFactors(self, s, t):
        """
        Calculates the weighting factors for a point on the shell from the isoparametric coords

        Parameters
        ----------
        s : float
            First isoparametric coordinate
        t : float
            Second isoparametric coordinate

        Returns
        -------
        int
            List of numbers containing weighting factors or None if not possible to calculate
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "WeightingFactors", s, t)

    def Xrefs(self):
        """
        Returns the cross references for this shell

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

