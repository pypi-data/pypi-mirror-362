import Oasys.gRPC


# Metaclass for static properties and constants
class NodeType(type):
    _consts = {'SCALAR', 'SCALAR_VALUE'}

    def __getattr__(cls, name):
        if name in NodeType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("Node class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in NodeType._consts:
            raise AttributeError("Cannot set Node class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class Node(Oasys.gRPC.OasysItem, metaclass=NodeType):
    _props = {'colour', 'include', 'label', 'ndof', 'nid', 'rc', 'scalar', 'tc', 'x', 'x1', 'x2', 'x3', 'y', 'z'}
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
        if name in Node._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in Node._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("Node instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Node._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in Node._rprops:
            raise AttributeError("Cannot set read-only Node instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, nid, x, y, z, tc=Oasys.gRPC.defaultArg, rc=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, nid, x, y, z, tc, rc)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new Node object

        Parameters
        ----------
        model : Model
            Model that node will be created in
        nid : integer
            Node number
        x : float
            X coordinate
        y : float
            Y coordinate
        z : float
            Z coordinate
        tc : integer
            Optional. Translational constraint (0-7). If omitted tc will be set to 0
        rc : integer
            Optional. Rotational constraint (0-7). If omitted rc will be set to 0

        Returns
        -------
        Node
            Node object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def BlankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the nodes in the model

        Parameters
        ----------
        model : Model
            Model that all nodes will be blanked in
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
        Blanks all of the flagged nodes in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged nodes will be blanked in
        flag : Flag
            Flag set on the nodes that you want to blank
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
        Starts an interactive editing panel to create a node

        Parameters
        ----------
        model : Model
            Model that the node will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        Node
            Node object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def First(model):
        """
        Returns the first node in the model

        Parameters
        ----------
        model : Model
            Model to get first node in

        Returns
        -------
        Node
            Node object (or None if there are no nodes in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FirstFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the first free node label in the model.
        Also see Node.LastFreeLabel(),
        Node.NextFreeLabel() and
        Model.FirstFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get first free node label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            First free in layer in editing panels). If omitted the whole model will be used (Equivalent to
            First free in editing panels)

        Returns
        -------
        int
            Node label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FirstFreeLabel", model, layer)

    def FlagAll(model, flag):
        """
        Flags all of the nodes in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all nodes will be flagged in
        flag : Flag
            Flag to set on the nodes

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Node objects or properties for all of the nodes in a model in PRIMER.
        If the optional property argument is not given then a list of Node objects is returned.
        If the property argument is given, that property value for each node is returned in the list
        instead of a Node object

        Parameters
        ----------
        model : Model
            Model to get nodes from
        property : string
            Optional. Name for property to get for all nodes in the model

        Returns
        -------
        list
            List of Node objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Node objects for all of the flagged nodes in a model in PRIMER
        If the optional property argument is not given then a list of Node objects is returned.
        If the property argument is given, then that property value for each node is returned in the list
        instead of a Node object

        Parameters
        ----------
        model : Model
            Model to get nodes from
        flag : Flag
            Flag set on the nodes that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged nodes in the model

        Returns
        -------
        list
            List of Node objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the Node object for a node ID

        Parameters
        ----------
        model : Model
            Model to find the node in
        number : integer
            number of the node you want the Node object for

        Returns
        -------
        Node
            Node object (or None if node does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last node in the model

        Parameters
        ----------
        model : Model
            Model to get last node in

        Returns
        -------
        Node
            Node object (or None if there are no nodes in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def LastFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the last free node label in the model.
        Also see Node.FirstFreeLabel(),
        Node.NextFreeLabel() and
        see Model.LastFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get last free node label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest free in layer in editing panels). If omitted the whole model will be used

        Returns
        -------
        int
            Node label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "LastFreeLabel", model, layer)

    def Merge(model, flag, dist, label=Oasys.gRPC.defaultArg, position=Oasys.gRPC.defaultArg):
        """
        Attempts to merge nodes flagged with flag for a model in PRIMER.
        Merging nodes on \*AIRBAG_SHELL_REFERENCE_GEOMETRY can be controlled by using
        Options.node_replace_asrg.
        Also see Model.MergeNodes()

        Parameters
        ----------
        model : Model
            Model that the nodes will be merged in
        flag : Flag
            Flag set on nodes to nodes
        dist : float
            Nodes closer than dist will be potentially merged
        label : integer
            Optional. Label to keep after merge. If > 0 then highest label kept.
            If <= 0 then lowest kept.
            If omitted the lowest label will be kept
        position : integer
            Optional. Position to merge at. If > 0 then merged at highest label position.
            If < 0 then merged at lowest label position.
            If 0 then merged at midpoint.
            If omitted the merge will be done at the lowest label

        Returns
        -------
        int
            The number of nodes merged
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Merge", model, flag, dist, label, position)

    def NextFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the next free (highest+1) node label in the model.
        Also see Node.FirstFreeLabel(),
        Node.LastFreeLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get next free node label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest+1 in layer in editing panels). If omitted the whole model will be used (Equivalent to
            Highest+1 in editing panels)

        Returns
        -------
        int
            Node label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NextFreeLabel", model, layer)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a node

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only nodes from that model can be picked.
            If the argument is a Flag then only nodes that
            are flagged with limit can be selected.
            If omitted, or None, any nodes from any model can be selected.
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
        Node
            Node object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def RenumberAll(model, start):
        """
        Renumbers all of the nodes in the model

        Parameters
        ----------
        model : Model
            Model that all nodes will be renumbered in
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
        Renumbers all of the flagged nodes in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged nodes will be renumbered in
        flag : Flag
            Flag set on the nodes that you want to renumber
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
        Allows the user to select nodes using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting nodes
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only nodes from that model can be selected.
            If the argument is a Flag then only nodes that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any nodes can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of nodes selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged nodes in the model. The nodes will be sketched until you either call
        Node.Unsketch(),
        Node.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged nodes will be sketched in
        flag : Flag
            Flag set on the nodes that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the nodes are sketched.
            If omitted redraw is true. If you want to sketch flagged nodes several times and only
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
        Returns the total number of nodes in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing nodes should be counted. If false or omitted
            referenced but undefined nodes will also be included in the total

        Returns
        -------
        int
            number of nodes
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnblankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the nodes in the model

        Parameters
        ----------
        model : Model
            Model that all nodes will be unblanked in
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
        Unblanks all of the flagged nodes in the model

        Parameters
        ----------
        model : Model
            Model that the flagged nodes will be unblanked in
        flag : Flag
            Flag set on the nodes that you want to unblank
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
        Unsets a defined flag on all of the nodes in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all nodes will be unset in
        flag : Flag
            Flag to unset on the nodes

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all nodes

        Parameters
        ----------
        model : Model
            Model that all nodes will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the nodes are unsketched.
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
        Unsketches all flagged nodes in the model

        Parameters
        ----------
        model : Model
            Model that all nodes will be unsketched in
        flag : Flag
            Flag set on the nodes that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the nodes are unsketched.
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
        Associates a comment with a node

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the node

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def Blank(self):
        """
        Blanks the node

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank")

    def Blanked(self):
        """
        Checks if the node is blanked or not

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
        Clears a flag on the node

        Parameters
        ----------
        flag : Flag
            Flag to clear on the node

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the node. The target include of the copied node can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        Node
            Node object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a node

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the node

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
        Extracts the actual colour used for node.
        By default in PRIMER many entities such as elements get their colour automatically from the part that they are in.
        PRIMER cycles through 13 default colours based on the label of the entity. In this case the node colour
        property will return the value Colour.PART instead of the actual colour.
        This method will return the actual colour which is used for drawing the node

        Returns
        -------
        int
            colour value (integer)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ExtractColour")

    def Flagged(self, flag):
        """
        Checks if the node is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the node

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetAttachedShells(self, recursive=Oasys.gRPC.defaultArg):
        """
        Returns the shells that are attached to the node

        Parameters
        ----------
        recursive : boolean
            Optional. If recursive is false then only the shells actually attached to the node will be
            returned (this could also be done by using the Xrefs class but this method
            is provided for convenience.
            If recursive is true then PRIMER will keep finding attached shells until no more can be found.
            If omitted recursive will be false

        Returns
        -------
        list
            List of Shell objects (or None if there are no attached shells)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetAttachedShells", recursive)

    def GetComments(self):
        """
        Extracts the comments associated to a node

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetFreeEdgeNodes(self):
        """
        If the node is on a shell free edge and that edge forms a loop like the boundary of a hole,
        then GetFreeEdgeNodes returns all of the nodes on the hole/boundary in order.
        Note that a free edge is a shell edge which is only used by one shell, whereas edges in the middle of
        a shell part will have got more than one adjacent shell and are therefore not free edges. If every
        node on a boundary belongs to exactly two free edges, then this function returns the list as described.
        In more involved combinatorics of shells, for example multiple parts sharing nodes along their
        boundaries, there can be one, three or more free edges at a node, and this function should not
        be used.
        If you only need to know whether or not a node is on a free edge, you should find the shells attached
        to it by cross references with Xrefs.GetItemID and see
        whether these shells have got other nodes in common as well. If nodes along an edge of a shell only
        appear in that one shell, this is a free edge.

        Returns
        -------
        list
            List of Node objects (or None if not on a shell free edge)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetFreeEdgeNodes")

    def GetInitialVelocities(self):
        """
        Returns the initial velocity of the node. 
        You need to be sure the field nvels of the node is populate before to use GetInitialVelocities. 
        To do so you can use  Model.PopNodeVels

        Returns
        -------
        list
            List containing the 3 translational and 3 rotational velocity values
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetInitialVelocities")

    def GetParameter(self, prop):
        """
        Checks if a Node property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the Node.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            node property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def GetReferenceGeometry(self):
        """
        Returns the airbag reference geometry of the node

        Returns
        -------
        int
            The reference geometry ID of the node (or 0 if it hasn't got any)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetReferenceGeometry")

    def Keyword(self):
        """
        Returns the keyword for this node (\*NODE, \*NODE_SCALAR or \*NODE_SCALAR_VALUE).
        Note that a carriage return is not added.
        See also Node.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the node.
        Note that a carriage return is not added.
        See also Node.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next node in the model

        Returns
        -------
        Node
            Node object (or None if there are no more nodes in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def NodalMass(self):
        """
        Get the mass of a node. This will be the sum of the 
        structural element mass attached to the node plus any lumped mass. 
        If called on the node of a PART_INERTIA or NRBC_INERTIA, this function will return 
        the mass of the part/nrbc, as 'nodal mass' has no meaning in this context

        Returns
        -------
        float
            float
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "NodalMass")

    def Previous(self):
        """
        Returns the previous node in the model

        Returns
        -------
        Node
            Node object (or None if there are no more nodes in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on the node

        Parameters
        ----------
        flag : Flag
            Flag to set on the node

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the node. The node will be sketched until you either call
        Node.Unsketch(),
        Node.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the node is sketched.
            If omitted redraw is true. If you want to sketch several nodes and only
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
        Unblanks the node

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank")

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the node

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the node is unsketched.
            If omitted redraw is true. If you want to unsketch several nodes and only
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
        Node
            Node object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this node

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

