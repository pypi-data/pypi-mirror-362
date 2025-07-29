import Oasys.gRPC


# Metaclass for static properties and constants
class ConstructionStagesType(type):

    def __getattr__(cls, name):

        raise AttributeError("ConstructionStages class attribute '{}' does not exist".format(name))


class ConstructionStages(Oasys.gRPC.OasysItem, metaclass=ConstructionStagesType):
    _props = {'ate', 'atr', 'ats', 'heading', 'include', 'istage', 'ivel0', 'label', 'rte', 'rts'}
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
        if name in ConstructionStages._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in ConstructionStages._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("ConstructionStages instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in ConstructionStages._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in ConstructionStages._rprops:
            raise AttributeError("Cannot set read-only ConstructionStages instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, stage_id, heading=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, stage_id, heading)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new ConstructionStages object

        Parameters
        ----------
        model : Model
            Model that \*DEFINE_CONSTRUCTION_STAGES will be created in
        stage_id : integer
            ConstructionStages id
        heading : string
            Optional. Title for the \*DEFINE_CONSTRUCTION_STAGES

        Returns
        -------
        ConstructionStages
            ConstructionStages object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def Create(model, modal=Oasys.gRPC.defaultArg):
        """
        Starts an interactive editing panel to create a \*DEFINE_CONSTRUCTION_STAGES

        Parameters
        ----------
        model : Model
            Model that the \*DEFINE_CONSTRUCTION_STAGES will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        ConstructionStages
            ConstructionStages object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def First(model):
        """
        Returns the first \*DEFINE_CONSTRUCTION_STAGES in the model

        Parameters
        ----------
        model : Model
            Model to get first \*DEFINE_CONSTRUCTION_STAGES in

        Returns
        -------
        ConstructionStages
            ConstructionStages object (or None if there are no \*DEFINE_CONSTRUCTION_STAGESs in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FirstFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the first free \*DEFINE_CONSTRUCTION_STAGES label in the model.
        Also see ConstructionStages.LastFreeLabel(),
        ConstructionStages.NextFreeLabel() and
        Model.FirstFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get first free \*DEFINE_CONSTRUCTION_STAGES label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            First free in layer in editing panels). If omitted the whole model will be used (Equivalent to
            First free in editing panels)

        Returns
        -------
        int
            ConstructionStages label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FirstFreeLabel", model, layer)

    def FlagAll(model, flag):
        """
        Flags all of the \*DEFINE_CONSTRUCTION_STAGESs in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all \*DEFINE_CONSTRUCTION_STAGESs will be flagged in
        flag : Flag
            Flag to set on the \*DEFINE_CONSTRUCTION_STAGESs

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of ConstructionStages objects or properties for all of the \*DEFINE_CONSTRUCTION_STAGESs in a model in PRIMER.
        If the optional property argument is not given then a list of ConstructionStages objects is returned.
        If the property argument is given, that property value for each \*DEFINE_CONSTRUCTION_STAGES is returned in the list
        instead of a ConstructionStages object

        Parameters
        ----------
        model : Model
            Model to get \*DEFINE_CONSTRUCTION_STAGESs from
        property : string
            Optional. Name for property to get for all \*DEFINE_CONSTRUCTION_STAGESs in the model

        Returns
        -------
        list
            List of ConstructionStages objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of ConstructionStages objects for all of the flagged \*DEFINE_CONSTRUCTION_STAGESs in a model in PRIMER
        If the optional property argument is not given then a list of ConstructionStages objects is returned.
        If the property argument is given, then that property value for each \*DEFINE_CONSTRUCTION_STAGES is returned in the list
        instead of a ConstructionStages object

        Parameters
        ----------
        model : Model
            Model to get \*DEFINE_CONSTRUCTION_STAGESs from
        flag : Flag
            Flag set on the \*DEFINE_CONSTRUCTION_STAGESs that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged \*DEFINE_CONSTRUCTION_STAGESs in the model

        Returns
        -------
        list
            List of ConstructionStages objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the ConstructionStages object for a \*DEFINE_CONSTRUCTION_STAGES ID

        Parameters
        ----------
        model : Model
            Model to find the \*DEFINE_CONSTRUCTION_STAGES in
        number : integer
            number of the \*DEFINE_CONSTRUCTION_STAGES you want the ConstructionStages object for

        Returns
        -------
        ConstructionStages
            ConstructionStages object (or None if \*DEFINE_CONSTRUCTION_STAGES does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last \*DEFINE_CONSTRUCTION_STAGES in the model

        Parameters
        ----------
        model : Model
            Model to get last \*DEFINE_CONSTRUCTION_STAGES in

        Returns
        -------
        ConstructionStages
            ConstructionStages object (or None if there are no \*DEFINE_CONSTRUCTION_STAGESs in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def LastFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the last free \*DEFINE_CONSTRUCTION_STAGES label in the model.
        Also see ConstructionStages.FirstFreeLabel(),
        ConstructionStages.NextFreeLabel() and
        see Model.LastFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get last free \*DEFINE_CONSTRUCTION_STAGES label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest free in layer in editing panels). If omitted the whole model will be used

        Returns
        -------
        int
            ConstructionStages label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "LastFreeLabel", model, layer)

    def NextFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the next free (highest+1) \*DEFINE_CONSTRUCTION_STAGES label in the model.
        Also see ConstructionStages.FirstFreeLabel(),
        ConstructionStages.LastFreeLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get next free \*DEFINE_CONSTRUCTION_STAGES label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest+1 in layer in editing panels). If omitted the whole model will be used (Equivalent to
            Highest+1 in editing panels)

        Returns
        -------
        int
            ConstructionStages label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NextFreeLabel", model, layer)

    def RenumberAll(model, start):
        """
        Renumbers all of the \*DEFINE_CONSTRUCTION_STAGESs in the model

        Parameters
        ----------
        model : Model
            Model that all \*DEFINE_CONSTRUCTION_STAGESs will be renumbered in
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
        Renumbers all of the flagged \*DEFINE_CONSTRUCTION_STAGESs in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged \*DEFINE_CONSTRUCTION_STAGESs will be renumbered in
        flag : Flag
            Flag set on the \*DEFINE_CONSTRUCTION_STAGESs that you want to renumber
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
        Allows the user to select \*DEFINE_CONSTRUCTION_STAGESs using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting \*DEFINE_CONSTRUCTION_STAGESs
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only \*DEFINE_CONSTRUCTION_STAGESs from that model can be selected.
            If the argument is a Flag then only \*DEFINE_CONSTRUCTION_STAGESs that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any \*DEFINE_CONSTRUCTION_STAGESs can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of \*DEFINE_CONSTRUCTION_STAGESs selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def Total(model, exists=Oasys.gRPC.defaultArg):
        """
        Returns the total number of \*DEFINE_CONSTRUCTION_STAGESs in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing \*DEFINE_CONSTRUCTION_STAGESs should be counted. If false or omitted
            referenced but undefined \*DEFINE_CONSTRUCTION_STAGESs will also be included in the total

        Returns
        -------
        int
            number of \*DEFINE_CONSTRUCTION_STAGESs
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the \*DEFINE_CONSTRUCTION_STAGESs in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all \*DEFINE_CONSTRUCTION_STAGESs will be unset in
        flag : Flag
            Flag to unset on the \*DEFINE_CONSTRUCTION_STAGESs

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)



# Instance methods
    def AssociateComment(self, comment):
        """
        Associates a comment with a \*DEFINE_CONSTRUCTION_STAGES

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the \*DEFINE_CONSTRUCTION_STAGES

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

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
        Clears a flag on the \*DEFINE_CONSTRUCTION_STAGES

        Parameters
        ----------
        flag : Flag
            Flag to clear on the \*DEFINE_CONSTRUCTION_STAGES

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the \*DEFINE_CONSTRUCTION_STAGES. The target include of the copied \*DEFINE_CONSTRUCTION_STAGES can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        ConstructionStages
            ConstructionStages object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a \*DEFINE_CONSTRUCTION_STAGES

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the \*DEFINE_CONSTRUCTION_STAGES

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
        Checks if the \*DEFINE_CONSTRUCTION_STAGES is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the \*DEFINE_CONSTRUCTION_STAGES

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a \*DEFINE_CONSTRUCTION_STAGES

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a ConstructionStages property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the ConstructionStages.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            \*DEFINE_CONSTRUCTION_STAGES property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this \*DEFINE_CONSTRUCTION_STAGES.
        Note that a carriage return is not added.
        See also ConstructionStages.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the \*DEFINE_CONSTRUCTION_STAGES.
        Note that a carriage return is not added.
        See also ConstructionStages.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next \*DEFINE_CONSTRUCTION_STAGES in the model

        Returns
        -------
        ConstructionStages
            ConstructionStages object (or None if there are no more \*DEFINE_CONSTRUCTION_STAGESs in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous \*DEFINE_CONSTRUCTION_STAGES in the model

        Returns
        -------
        ConstructionStages
            ConstructionStages object (or None if there are no more \*DEFINE_CONSTRUCTION_STAGESs in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on the \*DEFINE_CONSTRUCTION_STAGES

        Parameters
        ----------
        flag : Flag
            Flag to set on the \*DEFINE_CONSTRUCTION_STAGES

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def ViewParameters(self):
        """
        Object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. This function temporarily
        changes the behaviour so that if a property is a parameter the parameter name is returned instead.
        This can be used with 'method chaining' (see the example below) to make sure a property argument is correct

        Returns
        -------
        ConstructionStages
            ConstructionStages object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this \*DEFINE_CONSTRUCTION_STAGES

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

