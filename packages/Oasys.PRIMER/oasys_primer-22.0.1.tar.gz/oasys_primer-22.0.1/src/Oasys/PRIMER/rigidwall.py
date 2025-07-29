import Oasys.gRPC


# Metaclass for static properties and constants
class RigidwallType(type):
    _consts = {'CYLINDER', 'FLAT', 'PLANAR', 'PRISM', 'SPHERE'}

    def __getattr__(cls, name):
        if name in RigidwallType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("Rigidwall class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in RigidwallType._consts:
            raise AttributeError("Cannot set Rigidwall class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class Rigidwall(Oasys.gRPC.OasysItem, metaclass=RigidwallType):
    _props = {'birth', 'boxid', 'd1', 'd2', 'd3', 'death', 'decaya', 'decayb', 'dfrica', 'dfricb', 'display', 'e', 'finite', 'forces', 'fric', 'heading', 'id', 'include', 'label', 'lcid', 'lencyl', 'lenl', 'lenm', 'lenp', 'mass', 'motion', 'moving', 'n1', 'n2', 'n3', 'n4', 'node1', 'node2', 'nsegs', 'nsid', 'nsidex', 'offset', 'opt', 'ortho', 'pid', 'pr', 'radcyl', 'radsph', 'ro', 'rwid', 'rwksf', 'sfrica', 'sfricb', 'soft', 'ssid', 'type', 'v0', 'vx', 'vy', 'vz', 'wvel', 'xh', 'xhev', 'xt', 'yh', 'yhev', 'yt', 'zh', 'zhev', 'zt'}
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
        if name in Rigidwall._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in Rigidwall._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("Rigidwall instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Rigidwall._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in Rigidwall._rprops:
            raise AttributeError("Cannot set read-only Rigidwall instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, type, nsid=Oasys.gRPC.defaultArg, rwid=Oasys.gRPC.defaultArg, heading=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, type, nsid, rwid, heading)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new Rigidwall object

        Parameters
        ----------
        model : Model
            Model that Rigidwall will be created in
        type : constant
            Specify the type of rigidwall (Can be
            Rigidwall.FLAT,
            Rigidwall.PRISM,
            Rigidwall.CYLINDER,
            Rigidwall.SPHERE,
            Rigidwall.PLANAR)
        nsid : integer
            Optional. Node set number
        rwid : integer
            Optional. Rigidwall number
        heading : string
            Optional. Title for the Rigidwall

        Returns
        -------
        Rigidwall
            Rigidwall object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def BlankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the rigidwalls in the model

        Parameters
        ----------
        model : Model
            Model that all rigidwalls will be blanked in
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
        Blanks all of the flagged rigidwalls in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged rigidwalls will be blanked in
        flag : Flag
            Flag set on the rigidwalls that you want to blank
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
        Starts an interactive editing panel to create a rigidwall

        Parameters
        ----------
        model : Model
            Model that the rigidwall will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        Rigidwall
            Rigidwall object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def First(model):
        """
        Returns the first rigidwall in the model

        Parameters
        ----------
        model : Model
            Model to get first rigidwall in

        Returns
        -------
        Rigidwall
            Rigidwall object (or None if there are no rigidwalls in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FirstFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the first free rigidwall label in the model.
        Also see Rigidwall.LastFreeLabel(),
        Rigidwall.NextFreeLabel() and
        Model.FirstFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get first free rigidwall label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            First free in layer in editing panels). If omitted the whole model will be used (Equivalent to
            First free in editing panels)

        Returns
        -------
        int
            Rigidwall label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FirstFreeLabel", model, layer)

    def FlagAll(model, flag):
        """
        Flags all of the rigidwalls in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all rigidwalls will be flagged in
        flag : Flag
            Flag to set on the rigidwalls

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Rigidwall objects or properties for all of the rigidwalls in a model in PRIMER.
        If the optional property argument is not given then a list of Rigidwall objects is returned.
        If the property argument is given, that property value for each rigidwall is returned in the list
        instead of a Rigidwall object

        Parameters
        ----------
        model : Model
            Model to get rigidwalls from
        property : string
            Optional. Name for property to get for all rigidwalls in the model

        Returns
        -------
        list
            List of Rigidwall objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Rigidwall objects for all of the flagged rigidwalls in a model in PRIMER
        If the optional property argument is not given then a list of Rigidwall objects is returned.
        If the property argument is given, then that property value for each rigidwall is returned in the list
        instead of a Rigidwall object

        Parameters
        ----------
        model : Model
            Model to get rigidwalls from
        flag : Flag
            Flag set on the rigidwalls that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged rigidwalls in the model

        Returns
        -------
        list
            List of Rigidwall objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the Rigidwall object for a rigidwall ID

        Parameters
        ----------
        model : Model
            Model to find the rigidwall in
        number : integer
            number of the rigidwall you want the Rigidwall object for

        Returns
        -------
        Rigidwall
            Rigidwall object (or None if rigidwall does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last rigidwall in the model

        Parameters
        ----------
        model : Model
            Model to get last rigidwall in

        Returns
        -------
        Rigidwall
            Rigidwall object (or None if there are no rigidwalls in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def LastFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the last free rigidwall label in the model.
        Also see Rigidwall.FirstFreeLabel(),
        Rigidwall.NextFreeLabel() and
        see Model.LastFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get last free rigidwall label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest free in layer in editing panels). If omitted the whole model will be used

        Returns
        -------
        int
            Rigidwall label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "LastFreeLabel", model, layer)

    def NextFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the next free (highest+1) rigidwall label in the model.
        Also see Rigidwall.FirstFreeLabel(),
        Rigidwall.LastFreeLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get next free rigidwall label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest+1 in layer in editing panels). If omitted the whole model will be used (Equivalent to
            Highest+1 in editing panels)

        Returns
        -------
        int
            Rigidwall label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NextFreeLabel", model, layer)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a rigidwall

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only rigidwalls from that model can be picked.
            If the argument is a Flag then only rigidwalls that
            are flagged with limit can be selected.
            If omitted, or None, any rigidwalls from any model can be selected.
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
        Rigidwall
            Rigidwall object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def RenumberAll(model, start):
        """
        Renumbers all of the rigidwalls in the model

        Parameters
        ----------
        model : Model
            Model that all rigidwalls will be renumbered in
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
        Renumbers all of the flagged rigidwalls in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged rigidwalls will be renumbered in
        flag : Flag
            Flag set on the rigidwalls that you want to renumber
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
        Allows the user to select rigidwalls using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting rigidwalls
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only rigidwalls from that model can be selected.
            If the argument is a Flag then only rigidwalls that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any rigidwalls can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of rigidwalls selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged rigidwalls in the model. The rigidwalls will be sketched until you either call
        Rigidwall.Unsketch(),
        Rigidwall.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged rigidwalls will be sketched in
        flag : Flag
            Flag set on the rigidwalls that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the rigidwalls are sketched.
            If omitted redraw is true. If you want to sketch flagged rigidwalls several times and only
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
        Returns the total number of rigidwalls in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing rigidwalls should be counted. If false or omitted
            referenced but undefined rigidwalls will also be included in the total

        Returns
        -------
        int
            number of rigidwalls
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnblankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the rigidwalls in the model

        Parameters
        ----------
        model : Model
            Model that all rigidwalls will be unblanked in
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
        Unblanks all of the flagged rigidwalls in the model

        Parameters
        ----------
        model : Model
            Model that the flagged rigidwalls will be unblanked in
        flag : Flag
            Flag set on the rigidwalls that you want to unblank
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
        Unsets a defined flag on all of the rigidwalls in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all rigidwalls will be unset in
        flag : Flag
            Flag to unset on the rigidwalls

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all rigidwalls

        Parameters
        ----------
        model : Model
            Model that all rigidwalls will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the rigidwalls are unsketched.
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
        Unsketches all flagged rigidwalls in the model

        Parameters
        ----------
        model : Model
            Model that all rigidwalls will be unsketched in
        flag : Flag
            Flag set on the rigidwalls that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the rigidwalls are unsketched.
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
        Associates a comment with a rigidwall

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the rigidwall

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def Blank(self):
        """
        Blanks the rigidwall

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank")

    def Blanked(self):
        """
        Checks if the rigidwall is blanked or not

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
        Clears a flag on the rigidwall

        Parameters
        ----------
        flag : Flag
            Flag to clear on the rigidwall

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the rigidwall. The target include of the copied rigidwall can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        Rigidwall
            Rigidwall object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a rigidwall

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the rigidwall

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

    def FindNodesBehind(self, flag):
        """
        Flags nodes that are behind a rigidwall

        Parameters
        ----------
        flag : Flag
            Flag to be set on nodes behind rigidwall

        Returns
        -------
        int
            Number of nodes found
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "FindNodesBehind", flag)

    def Flagged(self, flag):
        """
        Checks if the rigidwall is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the rigidwall

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a rigidwall

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a Rigidwall property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the Rigidwall.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            rigidwall property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def GetRow(self, row):
        """
        Returns the data for an NSEGS card row in the rigidwall

        Parameters
        ----------
        row : integer
            The row you want the data for. Note row indices start at 0

        Returns
        -------
        list
            A list of numbers containing the row variables VL and HEIGHT
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetRow", row)

    def Keyword(self):
        """
        Returns the keyword for this Rigidwall (\*RIGIDWALL).
        Note that a carriage return is not added.
        See also Rigidwall.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the Rigidwall.
        Note that a carriage return is not added.
        See also Rigidwall.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next rigidwall in the model

        Returns
        -------
        Rigidwall
            Rigidwall object (or None if there are no more rigidwalls in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous rigidwall in the model

        Returns
        -------
        Rigidwall
            Rigidwall object (or None if there are no more rigidwalls in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def RemoveRow(self, row):
        """
        Removes an NSEGS card row in the \*RIGIDWALL

        Parameters
        ----------
        row : integer
            The row you want to remove the data for.
            Note that row indices start at 0

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "RemoveRow", row)

    def SetFlag(self, flag):
        """
        Sets a flag on the rigidwall

        Parameters
        ----------
        flag : Flag
            Flag to set on the rigidwall

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def SetRow(self, row, data):
        """
        Sets the data for an NSEGS card row in the \*RIGIDWALL

        Parameters
        ----------
        row : integer
            The row you want to set the data for.
            Note that row indices start at 0
        data : List of data
            The data you want to set the row to

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetRow", row, data)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the rigidwall. The rigidwall will be sketched until you either call
        Rigidwall.Unsketch(),
        Rigidwall.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the rigidwall is sketched.
            If omitted redraw is true. If you want to sketch several rigidwalls and only
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
        Unblanks the rigidwall

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank")

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the rigidwall

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the rigidwall is unsketched.
            If omitted redraw is true. If you want to unsketch several rigidwalls and only
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
        Rigidwall
            Rigidwall object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this rigidwall

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

