import Oasys.gRPC


# Metaclass for static properties and constants
class BeltType(type):
    _consts = {'B_POST_SLIPRING', 'FIXED', 'FREE_SLIPRING', 'INSERT_AFTER', 'INSERT_BEFORE', 'KNOWN', 'MESH_2D_SLIPRING_SET_NODE', 'MESH_ALL', 'MESH_NODE', 'MESH_NRBC', 'MESH_RETRACTOR', 'MESH_SEATBELT', 'MESH_SET_NODE', 'MESH_SET_PART', 'MESH_SET_SHELL', 'MESH_SHELL', 'MESH_SLIPRING', 'MESH_XSEC', 'MSEG_B1_ONLY', 'MSEG_B2_ONLY', 'MSEG_BD_NEW', 'MSEG_CE_1D', 'MSEG_CE_2D', 'MSEG_CE_SH', 'MSEG_E1_1D', 'MSEG_E1_2D', 'MSEG_E1_SH', 'MSEG_E2_1D', 'MSEG_E2_2D', 'MSEG_E2_SH', 'MSEG_MIX_SB1', 'MSEG_MIX_SB2', 'MSEG_SH_ONLY', 'RETRACTOR', 'SLIPRING', 'TWIST', 'XSEC'}

    def __getattr__(cls, name):
        if name in BeltType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("Belt class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in BeltType._consts:
            raise AttributeError("Cannot set Belt class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class Belt(Oasys.gRPC.OasysItem, metaclass=BeltType):
    _props = {'acuteAngle', 'curvature', 'friction', 'id', 'include', 'iterations', 'label', 'length', 'overlap', 'parts', 'penetration', 'pidShell', 'pid_1d', 'pid_2d', 'projection', 'psiShell', 'psi_2d', 'rows', 'shells', 'slen_1d', 'solids', 't1Shell', 't1_2d', 't2Shell', 't2_2d', 't3Shell', 't3_2d', 't4Shell', 't4_2d', 'thickFactor', 'thickFlag', 'thickness', 'title', 'tolerance', 'tshells', 'width', 'xsect_pretext', 'xsect_pretext_option'}
    _rprops = {'elemSet', 'exists', 'meshSegs', 'model', 'n2sContact', 'nodeSet', 'nrbFirst', 'nrbLast', 'nsboSet', 'points', 'retractorFirst', 'retractorLast', 's2sContact', 'seatbeltFirst', 'seatbeltLast', 'segments', 'slipringFirst', 'slipringLast', 'xsectionFirst', 'xsectionLast'}


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
        if name in Belt._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in Belt._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("Belt instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Belt._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in Belt._rprops:
            raise AttributeError("Cannot set read-only Belt instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, id, title=Oasys.gRPC.defaultArg, structural_type=Oasys.gRPC.defaultArg, flag=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, id, title, structural_type, flag)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new Belt object

        Parameters
        ----------
        model : Model
            Model that the belt definition will be created in
        id : integer
            Belt number
        title : string
            Optional. Title for the belt
        structural_type : string
            Optional. Seatbelt will be fitted around this entity type. This will trigger creation of sets as required. Type can be one of MODEL, DUMMY, PART, any ELEMENT subtype such as SHELL, or any SET subtype such as SET_PART. See Appendix I of the PRIMER manual for more information on PRIMER types
        flag : integer
            Optional. Flag used to identify entities that the belt should fit around. This argument is ignored if structural_type is MODEL. Instead, the current model is used

        Returns
        -------
        Belt
            Belt object
        """


# Static methods
    def BlankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the belts in the model

        Parameters
        ----------
        model : Model
            Model that all belts will be blanked in
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
        Blanks all of the flagged belts in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged belts will be blanked in
        flag : Flag
            Flag set on the belts that you want to blank
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
        Returns the first belt in the model

        Parameters
        ----------
        model : Model
            Model to get first belt in

        Returns
        -------
        Belt
            Belt object (or None if there are no belts in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FirstFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the first free belt label in the model.
        Also see Belt.LastFreeLabel(),
        Belt.NextFreeLabel() and
        Model.FirstFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get first free belt label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            First free in layer in editing panels). If omitted the whole model will be used (Equivalent to
            First free in editing panels)

        Returns
        -------
        int
            Belt label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FirstFreeLabel", model, layer)

    def FlagAll(model, flag):
        """
        Flags all of the belts in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all belts will be flagged in
        flag : Flag
            Flag to set on the belts

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Belt objects or properties for all of the belts in a model in PRIMER.
        If the optional property argument is not given then a list of Belt objects is returned.
        If the property argument is given, that property value for each belt is returned in the list
        instead of a Belt object

        Parameters
        ----------
        model : Model
            Model to get belts from
        property : string
            Optional. Name for property to get for all belts in the model

        Returns
        -------
        list
            List of Belt objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Belt objects for all of the flagged belts in a model in PRIMER
        If the optional property argument is not given then a list of Belt objects is returned.
        If the property argument is given, then that property value for each belt is returned in the list
        instead of a Belt object

        Parameters
        ----------
        model : Model
            Model to get belts from
        flag : Flag
            Flag set on the belts that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged belts in the model

        Returns
        -------
        list
            List of Belt objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the Belt object for a belt ID

        Parameters
        ----------
        model : Model
            Model to find the belt in
        number : integer
            number of the belt you want the Belt object for

        Returns
        -------
        Belt
            Belt object (or None if belt does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last belt in the model

        Parameters
        ----------
        model : Model
            Model to get last belt in

        Returns
        -------
        Belt
            Belt object (or None if there are no belts in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def LastFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the last free belt label in the model.
        Also see Belt.FirstFreeLabel(),
        Belt.NextFreeLabel() and
        see Model.LastFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get last free belt label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest free in layer in editing panels). If omitted the whole model will be used

        Returns
        -------
        int
            Belt label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "LastFreeLabel", model, layer)

    def NextFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the next free (highest+1) belt label in the model.
        Also see Belt.FirstFreeLabel(),
        Belt.LastFreeLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get next free belt label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest+1 in layer in editing panels). If omitted the whole model will be used (Equivalent to
            Highest+1 in editing panels)

        Returns
        -------
        int
            Belt label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NextFreeLabel", model, layer)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a belt

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only belts from that model can be picked.
            If the argument is a Flag then only belts that
            are flagged with limit can be selected.
            If omitted, or None, any belts from any model can be selected.
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
        Belt
            Belt object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def RenumberAll(model, start):
        """
        Renumbers all of the belts in the model

        Parameters
        ----------
        model : Model
            Model that all belts will be renumbered in
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
        Renumbers all of the flagged belts in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged belts will be renumbered in
        flag : Flag
            Flag set on the belts that you want to renumber
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
        Allows the user to select belts using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting belts
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only belts from that model can be selected.
            If the argument is a Flag then only belts that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any belts can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of belts selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SetMeshingLabels(entity_type, label_value):
        """
        Set the start labels for the entities created for a Seat Belt

        Parameters
        ----------
        entity_type : constant
            The Meshing label can be
            Belt.MESH_NODE,
             Belt.MESH_SHELL,
            Belt.MESH_SET_NODE,
            Belt.MESH_SET_SHELL,
            Belt.MESH_SEATBELT,
            Belt.MESH_NRBC,
            BELT.MESH_RETRACTOR,
            Belt.MESH_XSEC,
            Belt.MESH_SLIPRING,
            Belt.MESH_SET_PART,
            Belt.MESH_2D_SLIPRING_SET_NODE,
            Belt.MESH_ALL
        label_value : integer
            The initial label value to be assigned for the entity type

        Returns
        -------
        None
            no return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "SetMeshingLabels", entity_type, label_value)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged belts in the model. The belts will be sketched until you either call
        Belt.Unsketch(),
        Belt.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged belts will be sketched in
        flag : Flag
            Flag set on the belts that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the belts are sketched.
            If omitted redraw is true. If you want to sketch flagged belts several times and only
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
        Returns the total number of belts in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing belts should be counted. If false or omitted
            referenced but undefined belts will also be included in the total

        Returns
        -------
        int
            number of belts
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnblankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the belts in the model

        Parameters
        ----------
        model : Model
            Model that all belts will be unblanked in
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
        Unblanks all of the flagged belts in the model

        Parameters
        ----------
        model : Model
            Model that the flagged belts will be unblanked in
        flag : Flag
            Flag set on the belts that you want to unblank
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
        Unsets a defined flag on all of the belts in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all belts will be unset in
        flag : Flag
            Flag to unset on the belts

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all belts

        Parameters
        ----------
        model : Model
            Model that all belts will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the belts are unsketched.
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
        Unsketches all flagged belts in the model

        Parameters
        ----------
        model : Model
            Model that all belts will be unsketched in
        flag : Flag
            Flag set on the belts that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the belts are unsketched.
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
        Associates a comment with a belt

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the belt

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def Blank(self):
        """
        Blanks the belt

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank")

    def Blanked(self):
        """
        Checks if the belt is blanked or not

        Returns
        -------
        bool
            True if blanked, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blanked")

    def ClearFlag(self, flag):
        """
        Clears a flag on the belt

        Parameters
        ----------
        flag : Flag
            Flag to clear on the belt

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the belt. The target include of the copied belt can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        Belt
            Belt object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a belt

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the belt

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "DetachComment", comment)

    def Fit(self):
        """
        (Re)fits belt

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Fit")

    def Flagged(self, flag):
        """
        Checks if the belt is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the belt

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def Generate(self):
        """
        Generates belt mesh. Extracts and uses existing mesh properties when a mesh is present; inserts a default mesh otherwise

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Generate")

    def GetComments(self):
        """
        Extracts the comments associated to a belt

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetMesh(self, index):
        """
        Returns the information for a belt mesh section (properties base_pt1, base_pt2, path_pt1, path_pt2, mode, lb1, lb2). See Belt.SetMesh() for more information on supported properties. Must be preceded by a call to Belt.Generate()

        Parameters
        ----------
        index : integer
            The index of the mesh section you want the information for. Note that mesh segments start at 0, not 1. 0 <= index < meshSegs

        Returns
        -------
        dict
            Dict containing the mesh section information
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetMesh", index)

    def GetParameter(self, prop):
        """
        Checks if a Belt property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the Belt.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            belt property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def GetPoint(self, index):
        """
        Returns the information for a path point (properties fixity, x, y, z, node, trx1, try1, trz1, tnx1, tny1, tnz1, tnode1, trx2, try2, trz2, tnx2, tny2, tnz2, tnode2).
        Properties fixity, x, y, z and node will always be returned. Twist properties trx1, try1, trz1, tnx1, tny1, tnz1, tnode1, trx2, try2, trz2, tnx2, tny2, tnz2 and tnode2 will only be
        returned if defined for the point

        Parameters
        ----------
        index : integer
            The index of the path point you want the information for. Note that path points start at 0, not 1. 0 <= index < points

        Returns
        -------
        dict
            Dict containing the path point information
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetPoint", index)

    def InsertPoint(self, index, position, data):
        """
        Inserts a path point before/after an existing one. Subsequent path points will be moved 'up' as required

        Parameters
        ----------
        index : integer
            The index of an existing path point. Note that path points start at 0, not 1. 0 <= index < points
        position : integer
            Do we want to insert before or after the path point denoted by index? The position can be
            Belt.INSERT_AFTER or
            Belt.INSERT_BEFORE
        data : dict
            Object containing the path point data

        Returns
        -------
        None
            no return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "InsertPoint", index, position, data)

    def Next(self):
        """
        Returns the next belt in the model

        Returns
        -------
        Belt
            Belt object (or None if there are no more belts in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous belt in the model

        Returns
        -------
        Belt
            Belt object (or None if there are no more belts in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def RemovePoint(self, index):
        """
        Removes a path point from a belt

        Parameters
        ----------
        index : integer
            The index of the path point you want to remove. Note that path points start at 0, not 1. 0 <= index < points

        Returns
        -------
        None
            no return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "RemovePoint", index)

    def SetFlag(self, flag):
        """
        Sets a flag on the belt

        Parameters
        ----------
        flag : Flag
            Flag to set on the belt

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def SetMesh(self, index, data):
        """
        Sets the data for various properties for a mesh section in a belt. Values for properties not invoked will be retained as is. Must be preceded by a call to Belt.Generate()

        Parameters
        ----------
        index : integer
            The index of the mesh section you want to set. Note that mesh segments start at 0, not 1
        data : dict
            Object containing the mesh section data

        Returns
        -------
        None
            no return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetMesh", index, data)

    def SetPoint(self, index, data):
        """
        Sets the data for a path point in a belt

        Parameters
        ----------
        index : integer
            The index of the path point you want to set. Note that path points start at 0, not 1.
            To add a new point use index points
        data : dict
            Object containing the path point data

        Returns
        -------
        None
            no return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetPoint", index, data)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the belt. The belt will be sketched until you either call
        Belt.Unsketch(),
        Belt.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the belt is sketched.
            If omitted redraw is true. If you want to sketch several belts and only
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
        Unblanks the belt

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank")

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the belt

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the belt is unsketched.
            If omitted redraw is true. If you want to unsketch several belts and only
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
        Belt
            Belt object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this belt

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

