import Oasys.gRPC


# Metaclass for static properties and constants
class SpcType(type):
    _consts = {'NODE', 'ROTATIONAL', 'SET', 'TRANSLATIONAL'}

    def __getattr__(cls, name):
        if name in SpcType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("Spc class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in SpcType._consts:
            raise AttributeError("Cannot set Spc class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class Spc(Oasys.gRPC.OasysItem, metaclass=SpcType):
    _props = {'bd_flag', 'birth', 'cid', 'death', 'dofrx', 'dofry', 'dofrz', 'dofx', 'dofy', 'dofz', 'heading', 'id', 'include', 'label', 'nid', 'type'}
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
        if name in Spc._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in Spc._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("Spc instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Spc._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in Spc._rprops:
            raise AttributeError("Cannot set read-only Spc instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, nid, cid, dofx, dofy, dofz, dofrx, dofry, dofrz, type, label=Oasys.gRPC.defaultArg, heading=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, nid, cid, dofx, dofy, dofz, dofrx, dofry, dofrz, type, label, heading)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new Spc object

        Parameters
        ----------
        model : Model
            Model that spc will be created in
        nid : integer
            Node ID or node set ID
        cid : integer
            Coordinate system ID
        dofx : integer
            Translational constraint in local x direction
        dofy : integer
            Translational constraint in local y direction
        dofz : integer
            Translational constraint in local z direction
        dofrx : integer
            Rotational constraint in local x direction
        dofry : integer
            Rotational constraint in local y direction
        dofrz : integer
            Rotational constraint in local z direction
        type : constant
            Specify the type of boundary spc (Can be
            Spc.NODE or
            Spc.SET)
        label : integer
            Optional. Spc number
        heading : string
            Optional. Title for the spc

        Returns
        -------
        Spc
            Spc object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def BlankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the boundary SPCs in the model

        Parameters
        ----------
        model : Model
            Model that all boundary SPCs will be blanked in
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
        Blanks all of the flagged boundary SPCs in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged boundary SPCs will be blanked in
        flag : Flag
            Flag set on the boundary SPCs that you want to blank
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
        Returns the first boundary SPC in the model

        Parameters
        ----------
        model : Model
            Model to get first boundary SPC in

        Returns
        -------
        Spc
            Spc object (or None if there are no boundary SPCs in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FirstFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the first free boundary SPC label in the model.
        Also see Spc.LastFreeLabel(),
        Spc.NextFreeLabel() and
        Model.FirstFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get first free boundary SPC label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            First free in layer in editing panels). If omitted the whole model will be used (Equivalent to
            First free in editing panels)

        Returns
        -------
        int
            Spc label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FirstFreeLabel", model, layer)

    def FlagAll(model, flag):
        """
        Flags all of the boundary SPCs in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all boundary SPCs will be flagged in
        flag : Flag
            Flag to set on the boundary SPCs

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Spc objects or properties for all of the boundary SPCs in a model in PRIMER.
        If the optional property argument is not given then a list of Spc objects is returned.
        If the property argument is given, that property value for each boundary SPC is returned in the list
        instead of a Spc object

        Parameters
        ----------
        model : Model
            Model to get boundary SPCs from
        property : string
            Optional. Name for property to get for all boundary SPCs in the model

        Returns
        -------
        list
            List of Spc objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Spc objects for all of the flagged boundary SPCs in a model in PRIMER
        If the optional property argument is not given then a list of Spc objects is returned.
        If the property argument is given, then that property value for each boundary SPC is returned in the list
        instead of a Spc object

        Parameters
        ----------
        model : Model
            Model to get boundary SPCs from
        flag : Flag
            Flag set on the boundary SPCs that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged boundary SPCs in the model

        Returns
        -------
        list
            List of Spc objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the Spc object for a boundary SPC ID

        Parameters
        ----------
        model : Model
            Model to find the boundary SPC in
        number : integer
            number of the boundary SPC you want the Spc object for

        Returns
        -------
        Spc
            Spc object (or None if boundary SPC does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last boundary SPC in the model

        Parameters
        ----------
        model : Model
            Model to get last boundary SPC in

        Returns
        -------
        Spc
            Spc object (or None if there are no boundary SPCs in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def LastFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the last free boundary SPC label in the model.
        Also see Spc.FirstFreeLabel(),
        Spc.NextFreeLabel() and
        see Model.LastFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get last free boundary SPC label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest free in layer in editing panels). If omitted the whole model will be used

        Returns
        -------
        int
            Spc label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "LastFreeLabel", model, layer)

    def NextFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the next free (highest+1) boundary SPC label in the model.
        Also see Spc.FirstFreeLabel(),
        Spc.LastFreeLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get next free boundary SPC label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest+1 in layer in editing panels). If omitted the whole model will be used (Equivalent to
            Highest+1 in editing panels)

        Returns
        -------
        int
            Spc label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NextFreeLabel", model, layer)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a boundary SPC

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only boundary SPCs from that model can be picked.
            If the argument is a Flag then only boundary SPCs that
            are flagged with limit can be selected.
            If omitted, or None, any boundary SPCs from any model can be selected.
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
        Spc
            Spc object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def RenumberAll(model, start):
        """
        Renumbers all of the boundary SPCs in the model

        Parameters
        ----------
        model : Model
            Model that all boundary SPCs will be renumbered in
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
        Renumbers all of the flagged boundary SPCs in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged boundary SPCs will be renumbered in
        flag : Flag
            Flag set on the boundary SPCs that you want to renumber
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
        Allows the user to select boundary SPCs using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting boundary SPCs
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only boundary SPCs from that model can be selected.
            If the argument is a Flag then only boundary SPCs that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any boundary SPCs can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of boundary SPCs selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(type, model, flag):
        """
        Sketches all the flagged boundary SPCs in the model and update the plot. 
        The SPCs will be sketched until you do a graphics update or delete the model

        Parameters
        ----------
        type : integer
            Type of constraints to be drawn. Can be Spc.TRANSLATIONAL or
            Spc.ROTATIONAL
        model : Model
            Model that all the flagged boundary SPCs will be sketched in
        flag : Flag
            Flag set on the boundary SPCs that you want to sketch

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "SketchFlagged", type, model, flag)

    def Total(model, exists=Oasys.gRPC.defaultArg):
        """
        Returns the total number of boundary SPCs in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing boundary SPCs should be counted. If false or omitted
            referenced but undefined boundary SPCs will also be included in the total

        Returns
        -------
        int
            number of boundary SPCs
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnblankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the boundary SPCs in the model

        Parameters
        ----------
        model : Model
            Model that all boundary SPCs will be unblanked in
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
        Unblanks all of the flagged boundary SPCs in the model

        Parameters
        ----------
        model : Model
            Model that the flagged boundary SPCs will be unblanked in
        flag : Flag
            Flag set on the boundary SPCs that you want to unblank
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
        Unsets a defined flag on all of the boundary SPCs in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all boundary SPCs will be unset in
        flag : Flag
            Flag to unset on the boundary SPCs

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model):
        """
        Unsketches all SPCs

        Parameters
        ----------
        model : Model
            Model that all SPCs will be unblanked in

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnsketchAll", model)

    def UnsketchFlagged(model, flag):
        """
        Unsketches all flagged SPCs

        Parameters
        ----------
        model : Model
            Model that all SPCs will be unsketched in
        flag : Flag
            Flag set on the SPCs that you want to unsketch

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnsketchFlagged", model, flag)



# Instance methods
    def AssociateComment(self, comment):
        """
        Associates a comment with a boundary SPC

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the boundary SPC

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def Blank(self):
        """
        Blanks the boundary SPC

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank")

    def Blanked(self):
        """
        Checks if the boundary SPC is blanked or not

        Returns
        -------
        bool
            True if blanked, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blanked")

    def ClearFlag(self, flag):
        """
        Clears a flag on the boundary SPC

        Parameters
        ----------
        flag : Flag
            Flag to clear on the boundary SPC

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the boundary SPC. The target include of the copied boundary SPC can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        Spc
            Spc object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a boundary SPC

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the boundary SPC

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "DetachComment", comment)

    def Flagged(self, flag):
        """
        Checks if the boundary SPC is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the boundary SPC

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a boundary SPC

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a Spc property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the Spc.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            boundary SPC property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this spc (\*BOUNDARY_SPC_xxxx).
        Note that a carriage return is not added.
        See also Spc.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the spc.
        Note that a carriage return is not added.
        See also Spc.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next boundary SPC in the model

        Returns
        -------
        Spc
            Spc object (or None if there are no more boundary SPCs in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous boundary SPC in the model

        Returns
        -------
        Spc
            Spc object (or None if there are no more boundary SPCs in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on the boundary SPC

        Parameters
        ----------
        flag : Flag
            Flag to set on the boundary SPC

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Sketch(self, type, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the Boundary SPC. The SPC will be sketched until you do a graphics update 
        or delete the model

        Parameters
        ----------
        type : constant
            Type of constraints to be drawn. Can be Spc.TRANSLATIONAL or
            Spc.ROTATIONAL
        redraw : boolean
            Optional. If set to true (or omitted) the plot will be redrawn each time.
            If sketching a large number of items, efficiency will be gained by setting the argument
            to false for all but the last item sketched. The final call will redraw

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Sketch", type, redraw)

    def Unblank(self):
        """
        Unblanks the boundary SPC

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank")

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the Spc

        Parameters
        ----------
        redraw : boolean
            Optional. If set to true (or omitted) the plot will be redrawn each time.
            If unsketching a large number of items, efficiency will be gained by setting the argument
            to false for all but the last item unsketched. The final call will redraw

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
        Spc
            Spc object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this boundary SPC

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

