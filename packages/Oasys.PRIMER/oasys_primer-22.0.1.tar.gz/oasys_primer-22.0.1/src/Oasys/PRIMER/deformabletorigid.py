import Oasys.gRPC


# Metaclass for static properties and constants
class DeformableToRigidType(type):
    _consts = {'AUTOMATIC', 'D2R', 'INERTIA', 'PART', 'PSET', 'R2D', 'SIMPLE'}

    def __getattr__(cls, name):
        if name in DeformableToRigidType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("DeformableToRigid class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in DeformableToRigidType._consts:
            raise AttributeError("Cannot set DeformableToRigid class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class DeformableToRigid(Oasys.gRPC.OasysItem, metaclass=DeformableToRigidType):
    _props = {'code', 'd2r', 'dtmax', 'entno', 'include', 'ixx', 'ixx_1', 'ixy', 'ixz', 'iyz', 'izz', 'lrb', 'ncsf', 'nrbf', 'offset', 'paired', 'pid', 'ptype', 'r2d', 'relsw', 'rwf', 'time1', 'time2', 'time3', 'tm', 'xc', 'yc', 'zc'}
    _rprops = {'exists', 'model', 'swset', 'type'}


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
        if name in DeformableToRigid._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in DeformableToRigid._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("DeformableToRigid instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in DeformableToRigid._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in DeformableToRigid._rprops:
            raise AttributeError("Cannot set read-only DeformableToRigid instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, type, pid=Oasys.gRPC.defaultArg, lrb=Oasys.gRPC.defaultArg, ptype=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, type, pid, lrb, ptype)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new DeformableToRigid object

        Parameters
        ----------
        model : Model
            Model that deformable to rigid will be created in
        type : constant
            Specify the type of DeformableToRigid (Can be
            DeformableToRigid.SIMPLE or
            DeformableToRigid.AUTOMATIC or
            DeformableToRigid.INERTIA )
        pid : integer
            Optional. Part or Part set ID which is switched to a rigid material. 
            Depends on value of ptype. 
            Used only for DeformableToRigid.SIMPLE or 
            DeformableToRigid.INERTIA
        lrb : integer
            Optional. Part ID of the lead rigid body to which the part is merged. 
            Used only for DeformableToRigid.SIMPLE
        ptype : integer
            Optional. Type of PID. Valid values are: 
            DeformableToRigid.PART or 
            DeformableToRigid.PSET. 
            Used only for DeformableToRigid.SIMPLE

        Returns
        -------
        DeformableToRigid
            DeformableToRigid object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def BlankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the deformable to rigids in the model

        Parameters
        ----------
        model : Model
            Model that all deformable to rigids will be blanked in
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
        Blanks all of the flagged deformable to rigids in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged deformable to rigids will be blanked in
        flag : Flag
            Flag set on the deformable to rigids that you want to blank
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
        Starts an interactive editing panel to create a deformable to rigid

        Parameters
        ----------
        model : Model
            Model that the deformable to rigid will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        DeformableToRigid
            DeformableToRigid object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def First(model):
        """
        Returns the first deformable to rigid in the model

        Parameters
        ----------
        model : Model
            Model to get first deformable to rigid in

        Returns
        -------
        DeformableToRigid
            DeformableToRigid object (or None if there are no deformable to rigids in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FirstFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the first free deformable to rigid label in the model.
        Also see DeformableToRigid.LastFreeLabel(),
        DeformableToRigid.NextFreeLabel() and
        Model.FirstFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get first free deformable to rigid label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            First free in layer in editing panels). If omitted the whole model will be used (Equivalent to
            First free in editing panels)

        Returns
        -------
        int
            DeformableToRigid label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FirstFreeLabel", model, layer)

    def FlagAll(model, flag):
        """
        Flags all of the deformable to rigids in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all deformable to rigids will be flagged in
        flag : Flag
            Flag to set on the deformable to rigids

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of DeformableToRigid objects or properties for all of the deformable to rigids in a model in PRIMER.
        If the optional property argument is not given then a list of DeformableToRigid objects is returned.
        If the property argument is given, that property value for each deformable to rigid is returned in the list
        instead of a DeformableToRigid object

        Parameters
        ----------
        model : Model
            Model to get deformable to rigids from
        property : string
            Optional. Name for property to get for all deformable to rigids in the model

        Returns
        -------
        list
            List of DeformableToRigid objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of DeformableToRigid objects for all of the flagged deformable to rigids in a model in PRIMER
        If the optional property argument is not given then a list of DeformableToRigid objects is returned.
        If the property argument is given, then that property value for each deformable to rigid is returned in the list
        instead of a DeformableToRigid object

        Parameters
        ----------
        model : Model
            Model to get deformable to rigids from
        flag : Flag
            Flag set on the deformable to rigids that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged deformable to rigids in the model

        Returns
        -------
        list
            List of DeformableToRigid objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the DeformableToRigid object for a deformable to rigid ID

        Parameters
        ----------
        model : Model
            Model to find the deformable to rigid in
        number : integer
            number of the deformable to rigid you want the DeformableToRigid object for

        Returns
        -------
        DeformableToRigid
            DeformableToRigid object (or None if deformable to rigid does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last deformable to rigid in the model

        Parameters
        ----------
        model : Model
            Model to get last deformable to rigid in

        Returns
        -------
        DeformableToRigid
            DeformableToRigid object (or None if there are no deformable to rigids in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def LastFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the last free deformable to rigid label in the model.
        Also see DeformableToRigid.FirstFreeLabel(),
        DeformableToRigid.NextFreeLabel() and
        see Model.LastFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get last free deformable to rigid label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest free in layer in editing panels). If omitted the whole model will be used

        Returns
        -------
        int
            DeformableToRigid label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "LastFreeLabel", model, layer)

    def NextFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the next free (highest+1) deformable to rigid label in the model.
        Also see DeformableToRigid.FirstFreeLabel(),
        DeformableToRigid.LastFreeLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get next free deformable to rigid label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest+1 in layer in editing panels). If omitted the whole model will be used (Equivalent to
            Highest+1 in editing panels)

        Returns
        -------
        int
            DeformableToRigid label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NextFreeLabel", model, layer)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a deformable to rigid

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only deformable to rigids from that model can be picked.
            If the argument is a Flag then only deformable to rigids that
            are flagged with limit can be selected.
            If omitted, or None, any deformable to rigids from any model can be selected.
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
        DeformableToRigid
            DeformableToRigid object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def RenumberAll(model, start):
        """
        Renumbers all of the deformable to rigids in the model

        Parameters
        ----------
        model : Model
            Model that all deformable to rigids will be renumbered in
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
        Renumbers all of the flagged deformable to rigids in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged deformable to rigids will be renumbered in
        flag : Flag
            Flag set on the deformable to rigids that you want to renumber
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
        Allows the user to select deformable to rigids using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting deformable to rigids
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only deformable to rigids from that model can be selected.
            If the argument is a Flag then only deformable to rigids that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any deformable to rigids can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of deformable to rigids selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged deformable to rigids in the model. The deformable to rigids will be sketched until you either call
        DeformableToRigid.Unsketch(),
        DeformableToRigid.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged deformable to rigids will be sketched in
        flag : Flag
            Flag set on the deformable to rigids that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the deformable to rigids are sketched.
            If omitted redraw is true. If you want to sketch flagged deformable to rigids several times and only
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
        Returns the total number of deformable to rigids in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing deformable to rigids should be counted. If false or omitted
            referenced but undefined deformable to rigids will also be included in the total

        Returns
        -------
        int
            number of deformable to rigids
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnblankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the deformable to rigids in the model

        Parameters
        ----------
        model : Model
            Model that all deformable to rigids will be unblanked in
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
        Unblanks all of the flagged deformable to rigids in the model

        Parameters
        ----------
        model : Model
            Model that the flagged deformable to rigids will be unblanked in
        flag : Flag
            Flag set on the deformable to rigids that you want to unblank
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
        Unsets a defined flag on all of the deformable to rigids in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all deformable to rigids will be unset in
        flag : Flag
            Flag to unset on the deformable to rigids

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all deformable to rigids

        Parameters
        ----------
        model : Model
            Model that all deformable to rigids will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the deformable to rigids are unsketched.
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
        Unsketches all flagged deformable to rigids in the model

        Parameters
        ----------
        model : Model
            Model that all deformable to rigids will be unsketched in
        flag : Flag
            Flag set on the deformable to rigids that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the deformable to rigids are unsketched.
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
        Associates a comment with a deformable to rigid

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the deformable to rigid

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def Blank(self):
        """
        Blanks the deformable to rigid

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank")

    def Blanked(self):
        """
        Checks if the deformable to rigid is blanked or not

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
        Clears a flag on the deformable to rigid

        Parameters
        ----------
        flag : Flag
            Flag to clear on the deformable to rigid

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the deformable to rigid. The target include of the copied deformable to rigid can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        DeformableToRigid
            DeformableToRigid object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a deformable to rigid

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the deformable to rigid

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

    def Flagged(self, flag):
        """
        Checks if the deformable to rigid is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the deformable to rigid

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a deformable to rigid

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetDefToRegAutoCard(self, ctype, index):
        """
        Returns the D2R or R2D cards for \*DEFORMABLE_TO_RIGID_AUTOMATC

        Parameters
        ----------
        ctype : integer
            The card type you want the data for. 
            Can be D2R or R2D
        index : integer
            The card index you want the data for. Note that card indices start at 0, not 1

        Returns
        -------
        list
            A list of numbers containing the 2 or 3 member (depending on Card type): Part or Part Set ID, LRB Part ID (only for card type D2R), and part type (PTYPE - Can be DeformableToRigid.PART or DeformableToRigid.PSET)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetDefToRegAutoCard", ctype, index)

    def GetParameter(self, prop):
        """
        Checks if a DeformableToRigid property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the DeformableToRigid.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            deformable to rigid property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this DeformableToRigid (\*DEFORMABLE_TO_RIGID_xxxx)
        Note that a carriage return is not added.
        See also DeformableToRigid.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the DeformableToRigid.
        Note that a carriage return is not added.
        See also DeformableToRigid.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next deformable to rigid in the model

        Returns
        -------
        DeformableToRigid
            DeformableToRigid object (or None if there are no more deformable to rigids in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous deformable to rigid in the model

        Returns
        -------
        DeformableToRigid
            DeformableToRigid object (or None if there are no more deformable to rigids in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def RemoveDefToRegAutoCard(self, ctype, index):
        """
        Removes the D2R or R2D cards for \*DEFORMABLE_TO_RIGID_AUTOMATC

        Parameters
        ----------
        ctype : integer
            The card type you want removed. 
            Can be D2R or R2D
        index : integer
            The card index you want removed. Note that card indices start at 0, not 1

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "RemoveDefToRegAutoCard", ctype, index)

    def SetDefToRegAutoCard(self, ctype, index, ptype, pid, lrb=Oasys.gRPC.defaultArg):
        """
        Sets the D2r or R2D card data f\*DEFORMABLE_TO_RIGID_AUTOMATIC

        Parameters
        ----------
        ctype : integer
            The card type you want to set. 
            Can be D2R or R2D
        index : integer
            The D2R or R2D card index you want to set.
            Note that cards start at 0, not 1
        ptype : integer
            Part type (PTYPE). Can be DeformableToRigid.PART or 
            DeformableToRigid.PSET
        pid : integer
            Part or Part Set ID
        lrb : integer
            Optional. LRB Part ID (only for card type D2R)

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetDefToRegAutoCard", ctype, index, ptype, pid, lrb)

    def SetFlag(self, flag):
        """
        Sets a flag on the deformable to rigid

        Parameters
        ----------
        flag : Flag
            Flag to set on the deformable to rigid

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the deformable to rigid. The deformable to rigid will be sketched until you either call
        DeformableToRigid.Unsketch(),
        DeformableToRigid.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the deformable to rigid is sketched.
            If omitted redraw is true. If you want to sketch several deformable to rigids and only
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
        Unblanks the deformable to rigid

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank")

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the deformable to rigid

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the deformable to rigid is unsketched.
            If omitted redraw is true. If you want to unsketch several deformable to rigids and only
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
        DeformableToRigid
            DeformableToRigid object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this deformable to rigid

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

