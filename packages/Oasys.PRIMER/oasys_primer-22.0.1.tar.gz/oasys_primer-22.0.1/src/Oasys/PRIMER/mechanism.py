import Oasys.gRPC


# Metaclass for static properties and constants
class MechanismType(type):
    _consts = {'COUPLER', 'HINGE', 'LINE', 'PIN', 'ROTATION', 'TRANSLATION'}

    def __getattr__(cls, name):
        if name in MechanismType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("Mechanism class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in MechanismType._consts:
            raise AttributeError("Cannot set Mechanism class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class Mechanism(Oasys.gRPC.OasysItem, metaclass=MechanismType):
    _props = {'include', 'title'}
    _rprops = {'assemblies', 'connections', 'exists', 'id', 'label', 'model', 'points'}


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
        if name in Mechanism._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in Mechanism._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("Mechanism instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Mechanism._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in Mechanism._rprops:
            raise AttributeError("Cannot set read-only Mechanism instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Static methods
    def BlankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the mechanisms in the model

        Parameters
        ----------
        model : Model
            Model that all mechanisms will be blanked in
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
        Blanks all of the flagged mechanisms in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged mechanisms will be blanked in
        flag : Flag
            Flag set on the mechanisms that you want to blank
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
        Returns the first mechanism in the model

        Parameters
        ----------
        model : Model
            Model to get first mechanism in

        Returns
        -------
        Mechanism
            Mechanism object (or None if there are no mechanisms in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FirstFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the first free mechanism label in the model.
        Also see Mechanism.LastFreeLabel(),
        Mechanism.NextFreeLabel() and
        Model.FirstFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get first free mechanism label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            First free in layer in editing panels). If omitted the whole model will be used (Equivalent to
            First free in editing panels)

        Returns
        -------
        int
            Mechanism label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FirstFreeLabel", model, layer)

    def FlagAll(model, flag):
        """
        Flags all of the mechanisms in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all mechanisms will be flagged in
        flag : Flag
            Flag to set on the mechanisms

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Mechanism objects or properties for all of the mechanisms in a model in PRIMER.
        If the optional property argument is not given then a list of Mechanism objects is returned.
        If the property argument is given, that property value for each mechanism is returned in the list
        instead of a Mechanism object

        Parameters
        ----------
        model : Model
            Model to get mechanisms from
        property : string
            Optional. Name for property to get for all mechanisms in the model

        Returns
        -------
        list
            List of Mechanism objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Mechanism objects for all of the flagged mechanisms in a model in PRIMER
        If the optional property argument is not given then a list of Mechanism objects is returned.
        If the property argument is given, then that property value for each mechanism is returned in the list
        instead of a Mechanism object

        Parameters
        ----------
        model : Model
            Model to get mechanisms from
        flag : Flag
            Flag set on the mechanisms that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged mechanisms in the model

        Returns
        -------
        list
            List of Mechanism objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the Mechanism object for a mechanism ID

        Parameters
        ----------
        model : Model
            Model to find the mechanism in
        number : integer
            number of the mechanism you want the Mechanism object for

        Returns
        -------
        Mechanism
            Mechanism object (or None if mechanism does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last mechanism in the model

        Parameters
        ----------
        model : Model
            Model to get last mechanism in

        Returns
        -------
        Mechanism
            Mechanism object (or None if there are no mechanisms in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def LastFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the last free mechanism label in the model.
        Also see Mechanism.FirstFreeLabel(),
        Mechanism.NextFreeLabel() and
        see Model.LastFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get last free mechanism label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest free in layer in editing panels). If omitted the whole model will be used

        Returns
        -------
        int
            Mechanism label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "LastFreeLabel", model, layer)

    def NextFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the next free (highest+1) mechanism label in the model.
        Also see Mechanism.FirstFreeLabel(),
        Mechanism.LastFreeLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get next free mechanism label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest+1 in layer in editing panels). If omitted the whole model will be used (Equivalent to
            Highest+1 in editing panels)

        Returns
        -------
        int
            Mechanism label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NextFreeLabel", model, layer)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a mechanism

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only mechanisms from that model can be picked.
            If the argument is a Flag then only mechanisms that
            are flagged with limit can be selected.
            If omitted, or None, any mechanisms from any model can be selected.
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
        Mechanism
            Mechanism object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def RenumberAll(model, start):
        """
        Renumbers all of the mechanisms in the model

        Parameters
        ----------
        model : Model
            Model that all mechanisms will be renumbered in
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
        Renumbers all of the flagged mechanisms in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged mechanisms will be renumbered in
        flag : Flag
            Flag set on the mechanisms that you want to renumber
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
        Allows the user to select mechanisms using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting mechanisms
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only mechanisms from that model can be selected.
            If the argument is a Flag then only mechanisms that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any mechanisms can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of mechanisms selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged mechanisms in the model. The mechanisms will be sketched until you either call
        Mechanism.Unsketch(),
        Mechanism.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged mechanisms will be sketched in
        flag : Flag
            Flag set on the mechanisms that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the mechanisms are sketched.
            If omitted redraw is true. If you want to sketch flagged mechanisms several times and only
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
        Returns the total number of mechanisms in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing mechanisms should be counted. If false or omitted
            referenced but undefined mechanisms will also be included in the total

        Returns
        -------
        int
            number of mechanisms
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnblankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the mechanisms in the model

        Parameters
        ----------
        model : Model
            Model that all mechanisms will be unblanked in
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
        Unblanks all of the flagged mechanisms in the model

        Parameters
        ----------
        model : Model
            Model that the flagged mechanisms will be unblanked in
        flag : Flag
            Flag set on the mechanisms that you want to unblank
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
        Unsets a defined flag on all of the mechanisms in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all mechanisms will be unset in
        flag : Flag
            Flag to unset on the mechanisms

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all mechanisms

        Parameters
        ----------
        model : Model
            Model that all mechanisms will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the mechanisms are unsketched.
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
        Unsketches all flagged mechanisms in the model

        Parameters
        ----------
        model : Model
            Model that all mechanisms will be unsketched in
        flag : Flag
            Flag set on the mechanisms that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the mechanisms are unsketched.
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
    def AddNodeSetToAssembly(self, index, nsid):
        """
        Add node set to assembly

        Parameters
        ----------
        index : integer
            The index of the assembly in which you want to add node set. Note that reference points start at 0, not 1. 0 <= index < assemblies
        nsid : integer
            The node set ID that you want to add

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AddNodeSetToAssembly", index, nsid)

    def AddPartSetToAssembly(self, index, psid):
        """
        Add part set to assembly

        Parameters
        ----------
        index : integer
            The index of the assembly in which you want to add part set. Note that reference points start at 0, not 1. 0 <= index < assemblies
        psid : integer
            The part set ID that you want to add

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AddPartSetToAssembly", index, psid)

    def AddPartToAssembly(self, index, pid):
        """
        Add part to assembly

        Parameters
        ----------
        index : integer
            The index of the assembly in which you want to add part. Note that reference points start at 0, not 1. 0 <= index < assemblies
        pid : integer
            The part ID that you want to add

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AddPartToAssembly", index, pid)

    def AssociateComment(self, comment):
        """
        Associates a comment with a mechanism

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the mechanism

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def Blank(self):
        """
        Blanks the mechanism

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank")

    def Blanked(self):
        """
        Checks if the mechanism is blanked or not

        Returns
        -------
        bool
            True if blanked, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blanked")

    def ClearFlag(self, flag):
        """
        Clears a flag on the mechanism

        Parameters
        ----------
        flag : Flag
            Flag to clear on the mechanism

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the mechanism. The target include of the copied mechanism can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        Mechanism
            Mechanism object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a mechanism

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the mechanism

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "DetachComment", comment)

    def Flagged(self, flag):
        """
        Checks if the mechanism is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the mechanism

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

    def GetComments(self):
        """
        Extracts the comments associated to a mechanism

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetConnection(self, index):
        """
        Returns the information for a connection

        Parameters
        ----------
        index : integer
            The index of the connection you want the information for. Note that connections start at 0, not 1. 0 <= index < connections

        Returns
        -------
        dict
            Dict with properties
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetConnection", index)

    def GetParameter(self, prop):
        """
        Checks if a Mechanism property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the Mechanism.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            mechanism property to get parameter for

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
            The index of the reference point you want the information for. Note that reference points start at 0, not 1. 0 <= index < points

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
        Returns the next mechanism in the model

        Returns
        -------
        Mechanism
            Mechanism object (or None if there are no more mechanisms in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous mechanism in the model

        Returns
        -------
        Mechanism
            Mechanism object (or None if there are no more mechanisms in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def RemoveConnection(self, index):
        """
        Removes a connection from a mechanism

        Parameters
        ----------
        index : integer
            The index of the connection you want to remove. Note that connections start at 0, not 1.
            0 <= index < connections

        Returns
        -------
        None
            no return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "RemoveConnection", index)

    def RemoveNodeSetFromAssembly(self, index, nsid):
        """
        Remove node set from assembly

        Parameters
        ----------
        index : integer
            The index of the assembly from which you want to remove the node set. Note that reference points start at 0, not 1. 0 <= index < assemblies
        nsid : integer
            The node set ID that you want to remove

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "RemoveNodeSetFromAssembly", index, nsid)

    def RemovePartFromAssembly(self, index, pid):
        """
        Remove part from assembly

        Parameters
        ----------
        index : integer
            The index of the assembly from which you want to remove the part. Note that reference points start at 0, not 1. 0 <= index < assemblies
        pid : integer
            The part ID that you want to remove

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "RemovePartFromAssembly", index, pid)

    def RemovePartSetFromAssembly(self, index, psid):
        """
        Remove part set from assembly

        Parameters
        ----------
        index : integer
            The index of the assembly from which you want to remove the part set. Note that reference points start at 0, not 1. 0 <= index < assemblies
        psid : integer
            The part set ID that you want to remove

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "RemovePartSetFromAssembly", index, psid)

    def RemovePoint(self, index):
        """
        Removes a reference point from a mechanism

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

    def SetConnection(self, index, data):
        """
        Sets the data for a connection in a mechanism

        Parameters
        ----------
        index : integer
            The index of the connection you want to set. Note that connections start at 0, not 1.
            To add a new connection use index connections
        data : dict
            Object containing the connection data. The properties can be:

        Returns
        -------
        None
            no return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetConnection", index, data)

    def SetFlag(self, flag):
        """
        Sets a flag on the mechanism

        Parameters
        ----------
        flag : Flag
            Flag to set on the mechanism

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def SetPoint(self, index, data):
        """
        Sets the data for a reference point in a mechanism

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
        Sketches the mechanism. The mechanism will be sketched until you either call
        Mechanism.Unsketch(),
        Mechanism.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the mechanism is sketched.
            If omitted redraw is true. If you want to sketch several mechanisms and only
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
        Unblanks the mechanism

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank")

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the mechanism

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the mechanism is unsketched.
            If omitted redraw is true. If you want to unsketch several mechanisms and only
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
        Mechanism
            Mechanism object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this mechanism

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

