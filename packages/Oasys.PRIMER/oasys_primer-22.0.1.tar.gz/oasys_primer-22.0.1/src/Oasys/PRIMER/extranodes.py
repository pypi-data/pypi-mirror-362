import Oasys.gRPC


# Metaclass for static properties and constants
class ExtraNodesType(type):
    _consts = {'NODE', 'SET'}

    def __getattr__(cls, name):
        if name in ExtraNodesType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("ExtraNodes class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in ExtraNodesType._consts:
            raise AttributeError("Cannot set ExtraNodes class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class ExtraNodes(Oasys.gRPC.OasysItem, metaclass=ExtraNodesType):
    _props = {'colour', 'id', 'iflag', 'include', 'option', 'pid'}
    _rprops = {'exists', 'label', 'model'}


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
        if name in ExtraNodes._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in ExtraNodes._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("ExtraNodes instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in ExtraNodes._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in ExtraNodes._rprops:
            raise AttributeError("Cannot set read-only ExtraNodes instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, option, pid, id, iflag):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, option, pid, id, iflag)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new ExtraNodes object

        Parameters
        ----------
        model : Model
            Model that constrained extra nodes will be created in
        option : constant
            Specify the type of constrained extra nodes. Can be
            ExtraNodes.NODE or
            ExtraNodes.SET)
        pid : integer
            Part ID of rigid body
        id : integer
            Node node ID or node set ID
        iflag : boolean
            Flag for adding node mass inertia to PART_INERTIA

        Returns
        -------
        ExtraNodes
            ExtraNodes object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def BlankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the constrained extra nodes in the model

        Parameters
        ----------
        model : Model
            Model that all constrained extra nodes will be blanked in
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
        Blanks all of the flagged constrained extra nodes in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged constrained extra nodes will be blanked in
        flag : Flag
            Flag set on the constrained extra nodes that you want to blank
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
        Starts an interactive editing panel to create a constrained extra node

        Parameters
        ----------
        model : Model
            Model that the constrained extra node will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        ExtraNodes
            ExtraNodes object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def First(model):
        """
        Returns the first constrained extra node in the model

        Parameters
        ----------
        model : Model
            Model to get first constrained extra node in

        Returns
        -------
        ExtraNodes
            ExtraNodes object (or None if there are no constrained extra nodes in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FlagAll(model, flag):
        """
        Flags all of the constrained extra nodes in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all constrained extra nodes will be flagged in
        flag : Flag
            Flag to set on the constrained extra nodes

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of ExtraNodes objects or properties for all of the constrained extra nodes in a model in PRIMER.
        If the optional property argument is not given then a list of ExtraNodes objects is returned.
        If the property argument is given, that property value for each constrained extra node is returned in the list
        instead of a ExtraNodes object

        Parameters
        ----------
        model : Model
            Model to get constrained extra nodes from
        property : string
            Optional. Name for property to get for all constrained extra nodes in the model

        Returns
        -------
        list
            List of ExtraNodes objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of ExtraNodes objects for all of the flagged constrained extra nodes in a model in PRIMER
        If the optional property argument is not given then a list of ExtraNodes objects is returned.
        If the property argument is given, then that property value for each constrained extra node is returned in the list
        instead of a ExtraNodes object

        Parameters
        ----------
        model : Model
            Model to get constrained extra nodes from
        flag : Flag
            Flag set on the constrained extra nodes that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged constrained extra nodes in the model

        Returns
        -------
        list
            List of ExtraNodes objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the ExtraNodes object for a constrained extra node ID

        Parameters
        ----------
        model : Model
            Model to find the constrained extra node in
        number : integer
            number of the constrained extra node you want the ExtraNodes object for

        Returns
        -------
        ExtraNodes
            ExtraNodes object (or None if constrained extra node does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last constrained extra node in the model

        Parameters
        ----------
        model : Model
            Model to get last constrained extra node in

        Returns
        -------
        ExtraNodes
            ExtraNodes object (or None if there are no constrained extra nodes in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a constrained extra node

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only constrained extra nodes from that model can be picked.
            If the argument is a Flag then only constrained extra nodes that
            are flagged with limit can be selected.
            If omitted, or None, any constrained extra nodes from any model can be selected.
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
        ExtraNodes
            ExtraNodes object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def Select(flag, prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg):
        """
        Allows the user to select constrained extra nodes using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting constrained extra nodes
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only constrained extra nodes from that model can be selected.
            If the argument is a Flag then only constrained extra nodes that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any constrained extra nodes can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of constrained extra nodes selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged constrained extra nodes in the model. The constrained extra nodes will be sketched until you either call
        ExtraNodes.Unsketch(),
        ExtraNodes.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged constrained extra nodes will be sketched in
        flag : Flag
            Flag set on the constrained extra nodes that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the constrained extra nodes are sketched.
            If omitted redraw is true. If you want to sketch flagged constrained extra nodes several times and only
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
        Returns the total number of constrained extra nodes in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing constrained extra nodes should be counted. If false or omitted
            referenced but undefined constrained extra nodes will also be included in the total

        Returns
        -------
        int
            number of constrained extra nodes
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnblankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the constrained extra nodes in the model

        Parameters
        ----------
        model : Model
            Model that all constrained extra nodes will be unblanked in
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
        Unblanks all of the flagged constrained extra nodes in the model

        Parameters
        ----------
        model : Model
            Model that the flagged constrained extra nodes will be unblanked in
        flag : Flag
            Flag set on the constrained extra nodes that you want to unblank
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
        Unsets a defined flag on all of the constrained extra nodes in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all constrained extra nodes will be unset in
        flag : Flag
            Flag to unset on the constrained extra nodes

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all constrained extra nodes

        Parameters
        ----------
        model : Model
            Model that all constrained extra nodes will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the constrained extra nodes are unsketched.
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
        Unsketches all flagged constrained extra nodes in the model

        Parameters
        ----------
        model : Model
            Model that all constrained extra nodes will be unsketched in
        flag : Flag
            Flag set on the constrained extra nodes that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the constrained extra nodes are unsketched.
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
        Associates a comment with a constrained extra node

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the constrained extra node

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def Blank(self):
        """
        Blanks the constrained extra node

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank")

    def Blanked(self):
        """
        Checks if the constrained extra node is blanked or not

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
        Clears a flag on the constrained extra node

        Parameters
        ----------
        flag : Flag
            Flag to clear on the constrained extra node

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the constrained extra node. The target include of the copied constrained extra node can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        ExtraNodes
            ExtraNodes object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a constrained extra node

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the constrained extra node

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
        Extracts the actual colour used for constrained extra node.
        By default in PRIMER many entities such as elements get their colour automatically from the part that they are in.
        PRIMER cycles through 13 default colours based on the label of the entity. In this case the constrained extra node colour
        property will return the value Colour.PART instead of the actual colour.
        This method will return the actual colour which is used for drawing the constrained extra node

        Returns
        -------
        int
            colour value (integer)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ExtractColour")

    def Flagged(self, flag):
        """
        Checks if the constrained extra node is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the constrained extra node

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a constrained extra node

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a ExtraNodes property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the ExtraNodes.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            constrained extra node property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this constrained extra nodes (\*CONSTRAINED_EXTRA_NODES).
        Note that a carriage return is not added.
        See also ExtraNodes.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the constrained extra nodes.
        Note that a carriage return is not added.
        See also ExtraNodes.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next constrained extra node in the model

        Returns
        -------
        ExtraNodes
            ExtraNodes object (or None if there are no more constrained extra nodes in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous constrained extra node in the model

        Returns
        -------
        ExtraNodes
            ExtraNodes object (or None if there are no more constrained extra nodes in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on the constrained extra node

        Parameters
        ----------
        flag : Flag
            Flag to set on the constrained extra node

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the constrained extra node. The constrained extra node will be sketched until you either call
        ExtraNodes.Unsketch(),
        ExtraNodes.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the constrained extra node is sketched.
            If omitted redraw is true. If you want to sketch several constrained extra nodes and only
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
        Unblanks the constrained extra node

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank")

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the constrained extra node

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the constrained extra node is unsketched.
            If omitted redraw is true. If you want to unsketch several constrained extra nodes and only
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
        ExtraNodes
            ExtraNodes object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this constrained extra node

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

