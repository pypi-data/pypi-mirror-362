import Oasys.gRPC


# Metaclass for static properties and constants
class DummyType(type):

    def __getattr__(cls, name):

        raise AttributeError("Dummy class attribute '{}' does not exist".format(name))


class Dummy(Oasys.gRPC.OasysItem, metaclass=DummyType):
    _props = {'include', 'title'}
    _rprops = {'assemblies', 'exists', 'id', 'label', 'model', 'points', 'xhpoint', 'yhpoint', 'zhpoint'}


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
        if name in Dummy._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in Dummy._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("Dummy instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Dummy._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in Dummy._rprops:
            raise AttributeError("Cannot set read-only Dummy instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Static methods
    def BlankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the dummys in the model

        Parameters
        ----------
        model : Model
            Model that all dummys will be blanked in
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
        Blanks all of the flagged dummys in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged dummys will be blanked in
        flag : Flag
            Flag set on the dummys that you want to blank
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
        Returns the first dummy in the model

        Parameters
        ----------
        model : Model
            Model to get first dummy in

        Returns
        -------
        Dummy
            Dummy object (or None if there are no dummys in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FirstFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the first free dummy label in the model.
        Also see Dummy.LastFreeLabel(),
        Dummy.NextFreeLabel() and
        Model.FirstFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get first free dummy label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            First free in layer in editing panels). If omitted the whole model will be used (Equivalent to
            First free in editing panels)

        Returns
        -------
        int
            Dummy label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FirstFreeLabel", model, layer)

    def FlagAll(model, flag):
        """
        Flags all of the dummys in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all dummys will be flagged in
        flag : Flag
            Flag to set on the dummys

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Dummy objects or properties for all of the dummys in a model in PRIMER.
        If the optional property argument is not given then a list of Dummy objects is returned.
        If the property argument is given, that property value for each dummy is returned in the list
        instead of a Dummy object

        Parameters
        ----------
        model : Model
            Model to get dummys from
        property : string
            Optional. Name for property to get for all dummys in the model

        Returns
        -------
        list
            List of Dummy objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Dummy objects for all of the flagged dummys in a model in PRIMER
        If the optional property argument is not given then a list of Dummy objects is returned.
        If the property argument is given, then that property value for each dummy is returned in the list
        instead of a Dummy object

        Parameters
        ----------
        model : Model
            Model to get dummys from
        flag : Flag
            Flag set on the dummys that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged dummys in the model

        Returns
        -------
        list
            List of Dummy objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the Dummy object for a dummy ID

        Parameters
        ----------
        model : Model
            Model to find the dummy in
        number : integer
            number of the dummy you want the Dummy object for

        Returns
        -------
        Dummy
            Dummy object (or None if dummy does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last dummy in the model

        Parameters
        ----------
        model : Model
            Model to get last dummy in

        Returns
        -------
        Dummy
            Dummy object (or None if there are no dummys in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def LastFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the last free dummy label in the model.
        Also see Dummy.FirstFreeLabel(),
        Dummy.NextFreeLabel() and
        see Model.LastFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get last free dummy label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest free in layer in editing panels). If omitted the whole model will be used

        Returns
        -------
        int
            Dummy label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "LastFreeLabel", model, layer)

    def NextFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the next free (highest+1) dummy label in the model.
        Also see Dummy.FirstFreeLabel(),
        Dummy.LastFreeLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get next free dummy label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest+1 in layer in editing panels). If omitted the whole model will be used (Equivalent to
            Highest+1 in editing panels)

        Returns
        -------
        int
            Dummy label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NextFreeLabel", model, layer)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a dummy

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only dummys from that model can be picked.
            If the argument is a Flag then only dummys that
            are flagged with limit can be selected.
            If omitted, or None, any dummys from any model can be selected.
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
        Dummy
            Dummy object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def RenumberAll(model, start):
        """
        Renumbers all of the dummys in the model

        Parameters
        ----------
        model : Model
            Model that all dummys will be renumbered in
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
        Renumbers all of the flagged dummys in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged dummys will be renumbered in
        flag : Flag
            Flag set on the dummys that you want to renumber
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
        Allows the user to select dummys using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting dummys
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only dummys from that model can be selected.
            If the argument is a Flag then only dummys that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any dummys can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of dummys selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged dummys in the model. The dummys will be sketched until you either call
        Dummy.Unsketch(),
        Dummy.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged dummys will be sketched in
        flag : Flag
            Flag set on the dummys that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the dummys are sketched.
            If omitted redraw is true. If you want to sketch flagged dummys several times and only
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
        Returns the total number of dummys in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing dummys should be counted. If false or omitted
            referenced but undefined dummys will also be included in the total

        Returns
        -------
        int
            number of dummys
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnblankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the dummys in the model

        Parameters
        ----------
        model : Model
            Model that all dummys will be unblanked in
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
        Unblanks all of the flagged dummys in the model

        Parameters
        ----------
        model : Model
            Model that the flagged dummys will be unblanked in
        flag : Flag
            Flag set on the dummys that you want to unblank
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
        Unsets a defined flag on all of the dummys in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all dummys will be unset in
        flag : Flag
            Flag to unset on the dummys

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all dummys

        Parameters
        ----------
        model : Model
            Model that all dummys will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the dummys are unsketched.
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
        Unsketches all flagged dummys in the model

        Parameters
        ----------
        model : Model
            Model that all dummys will be unsketched in
        flag : Flag
            Flag set on the dummys that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the dummys are unsketched.
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
        Associates a comment with a dummy

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the dummy

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def Blank(self):
        """
        Blanks the dummy

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank")

    def Blanked(self):
        """
        Checks if the dummy is blanked or not

        Returns
        -------
        bool
            True if blanked, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blanked")

    def ClearFlag(self, flag):
        """
        Clears a flag on the dummy

        Parameters
        ----------
        flag : Flag
            Flag to clear on the dummy

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the dummy. The target include of the copied dummy can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        Dummy
            Dummy object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a dummy

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the dummy

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "DetachComment", comment)

    def Flagged(self, flag):
        """
        Checks if the dummy is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the dummy

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetAssembly(self, index):
        """
        Returns the information for an assembly

        Parameters
        ----------
        index : integer
            The index of the assembly you want the coordinates for. Note that reference points start at 0, not 1. 0 <= index < assemblies

        Returns
        -------
        dict
            Dict with properties
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetAssembly", index)

    def GetAssemblyChildInfo(self, label, index):
        """
        Get information about a child assembly from its parent assembly

        Parameters
        ----------
        label : integer
            The label of the parent assembly
        index : integer
            index of the child (start with 0 till n-1, where n is total number of child)

        Returns
        -------
        dict
            Dict with properties
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetAssemblyChildInfo", label, index)

    def GetAssemblyFromID(self, label):
        """
        Get assembly information for a given assembly ID and returns an object containing the details

        Parameters
        ----------
        label : integer
            The label of the assembly you want the Assembly object for

        Returns
        -------
        dict
            Dict with properties
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetAssemblyFromID", label)

    def GetAssemblyPart(self, label):
        """
        Returns a list of Part objects representing all the parts within the assembly

        Parameters
        ----------
        label : integer
            The label of the assembly

        Returns
        -------
        list
            List of Part objects
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetAssemblyPart", label)

    def GetComments(self):
        """
        Extracts the comments associated to a dummy

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a Dummy property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the Dummy.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            dummy property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def GetPoint(self, index):
        """
        Returns the information for a reference point

        Parameters
        ----------
        index : integer
            The index of the reference point you want the information for. Note that reference points start at 0, not 1.
            0 <= index < points

        Returns
        -------
        dict
            Dict with properties
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetPoint", index)

    def GetPointData(self, rpt):
        """
        Returns the coordinates of a reference point

        Parameters
        ----------
        rpt : integer
            The reference point you want the coordinates for. Note that reference points start at 0, not 1

        Returns
        -------
        list
            List containing the reference point coordinates
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetPointData", rpt)

    def GetPointTitle(self, rpt):
        """
        Returns the title of a reference point

        Parameters
        ----------
        rpt : integer
            The reference point you want the title for. Note that reference points start at 0, not 1

        Returns
        -------
        str
            The reference point title
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetPointTitle", rpt)

    def Next(self):
        """
        Returns the next dummy in the model

        Returns
        -------
        Dummy
            Dummy object (or None if there are no more dummys in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous dummy in the model

        Returns
        -------
        Dummy
            Dummy object (or None if there are no more dummys in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def RemovePoint(self, index):
        """
        Removes a reference point from a dummy

        Parameters
        ----------
        index : integer
            The index of the reference point you want to remove. Note that reference points start at 0, not 1. 0 <= index < points

        Returns
        -------
        None
            no return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "RemovePoint", index)

    def SelectAssembly(self):
        """
        Returns a list of objects containing the assembly informaitons or None if menu cancelled

        Returns
        -------
        list
            List of dicts with properties
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SelectAssembly")

    def SetAssemblyNodeSet(self, label, nsid):
        """
        Sets a set node for a Dummy/HBM assembly

        Parameters
        ----------
        label : integer
            The label of the assembly
        nsid : integer
            The label of the set node to be added into the assembly

        Returns
        -------
        None
            no return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetAssemblyNodeSet", label, nsid)

    def SetAssemblyPart(self, label, pid):
        """
        Sets a part for a Dummy assembly

        Parameters
        ----------
        label : integer
            The label of the assembly
        pid : integer
            The label of the set part to be added into the assembly

        Returns
        -------
        None
            no return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetAssemblyPart", label, pid)

    def SetAssemblyPartSet(self, label, psid):
        """
        Sets a set part for a Dummy/HBM assembly

        Parameters
        ----------
        label : integer
            The label of the assembly
        psid : integer
            The label of the set part to be added into the assembly

        Returns
        -------
        None
            no return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetAssemblyPartSet", label, psid)

    def SetAssemblyStopAngle(self, label, axis, stop_neg, stop_pos):
        """
        Sets -ve and +ve stop angles in the assembly

        Parameters
        ----------
        label : integer
            The label of the assembly
        axis : integer
            Axis (0 = X, 1 = Y, or 2 = Z) on which to define stop angles
        stop_neg : real
            -ve stop angle
        stop_pos : real
            +ve stop angle

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetAssemblyStopAngle", label, axis, stop_neg, stop_pos)

    def SetFlag(self, flag):
        """
        Sets a flag on the dummy

        Parameters
        ----------
        flag : Flag
            Flag to set on the dummy

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def SetPoint(self, index, data):
        """
        Sets the data for a reference point in a dummy

        Parameters
        ----------
        index : integer
            The index of the reference point you want to set. Note that reference points start at 0, not 1.
            To add a new point use index points
        data : dict
            Object containing the reference point data. The properties can be:

        Returns
        -------
        None
            no return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetPoint", index, data)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the dummy. The dummy will be sketched until you either call
        Dummy.Unsketch(),
        Dummy.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the dummy is sketched.
            If omitted redraw is true. If you want to sketch several dummys and only
            redraw after the last one then use false for redraw and call
            View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Sketch", redraw)

    def SketchAssembly(self, label, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the assembly

        Parameters
        ----------
        label : integer
            The label of the assembly you want to sketch
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
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SketchAssembly", label, redraw)

    def Unblank(self):
        """
        Unblanks the dummy

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank")

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the dummy

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the dummy is unsketched.
            If omitted redraw is true. If you want to unsketch several dummys and only
            redraw after the last one then use false for redraw and call
            View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unsketch", redraw)

    def UnsketchAssembly(self, label, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the assembly

        Parameters
        ----------
        label : integer
            The label of the assembly you want to unsketch
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
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "UnsketchAssembly", label, redraw)

    def ViewParameters(self):
        """
        Object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. This function temporarily
        changes the behaviour so that if a property is a parameter the parameter name is returned instead.
        This can be used with 'method chaining' (see the example below) to make sure a property argument is correct

        Returns
        -------
        Dummy
            Dummy object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this dummy

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

