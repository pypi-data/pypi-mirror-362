import Oasys.gRPC


# Metaclass for static properties and constants
class TransformationType(type):

    def __getattr__(cls, name):

        raise AttributeError("Transformation class attribute '{}' does not exist".format(name))


class Transformation(Oasys.gRPC.OasysItem, metaclass=TransformationType):
    _props = {'include', 'label', 'title', 'tranid'}
    _rprops = {'exists', 'model', 'nrow'}


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
        if name in Transformation._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in Transformation._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("Transformation instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Transformation._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in Transformation._rprops:
            raise AttributeError("Cannot set read-only Transformation instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, tranid, title=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, tranid, title)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new Transformation object

        Parameters
        ----------
        model : Model
            Model that transformation will be created in
        tranid : integer
            Transformation label
        title : string
            Optional. Transformation title

        Returns
        -------
        Transformation
            Transformation object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def Create(model, modal=Oasys.gRPC.defaultArg):
        """
        Starts an interactive editing panel to create a transformation

        Parameters
        ----------
        model : Model
            Model that the transformation will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        Transformation
            Transformation object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def First(model):
        """
        Returns the first transformation in the model

        Parameters
        ----------
        model : Model
            Model to get first transformation in

        Returns
        -------
        Transformation
            Transformation object (or None if there are no transformations in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FirstFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the first free transformation label in the model.
        Also see Transformation.LastFreeLabel(),
        Transformation.NextFreeLabel() and
        Model.FirstFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get first free transformation label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            First free in layer in editing panels). If omitted the whole model will be used (Equivalent to
            First free in editing panels)

        Returns
        -------
        int
            Transformation label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FirstFreeLabel", model, layer)

    def FlagAll(model, flag):
        """
        Flags all of the transformations in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all transformations will be flagged in
        flag : Flag
            Flag to set on the transformations

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Transformation objects or properties for all of the transformations in a model in PRIMER.
        If the optional property argument is not given then a list of Transformation objects is returned.
        If the property argument is given, that property value for each transformation is returned in the list
        instead of a Transformation object

        Parameters
        ----------
        model : Model
            Model to get transformations from
        property : string
            Optional. Name for property to get for all transformations in the model

        Returns
        -------
        list
            List of Transformation objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Transformation objects for all of the flagged transformations in a model in PRIMER
        If the optional property argument is not given then a list of Transformation objects is returned.
        If the property argument is given, then that property value for each transformation is returned in the list
        instead of a Transformation object

        Parameters
        ----------
        model : Model
            Model to get transformations from
        flag : Flag
            Flag set on the transformations that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged transformations in the model

        Returns
        -------
        list
            List of Transformation objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the Transformation object for a transformation ID

        Parameters
        ----------
        model : Model
            Model to find the transformation in
        number : integer
            number of the transformation you want the Transformation object for

        Returns
        -------
        Transformation
            Transformation object (or None if transformation does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last transformation in the model

        Parameters
        ----------
        model : Model
            Model to get last transformation in

        Returns
        -------
        Transformation
            Transformation object (or None if there are no transformations in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def LastFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the last free transformation label in the model.
        Also see Transformation.FirstFreeLabel(),
        Transformation.NextFreeLabel() and
        see Model.LastFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get last free transformation label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest free in layer in editing panels). If omitted the whole model will be used

        Returns
        -------
        int
            Transformation label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "LastFreeLabel", model, layer)

    def NextFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the next free (highest+1) transformation label in the model.
        Also see Transformation.FirstFreeLabel(),
        Transformation.LastFreeLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get next free transformation label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest+1 in layer in editing panels). If omitted the whole model will be used (Equivalent to
            Highest+1 in editing panels)

        Returns
        -------
        int
            Transformation label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NextFreeLabel", model, layer)

    def Select(flag, prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg):
        """
        Allows the user to select transformations using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting transformations
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only transformations from that model can be selected.
            If the argument is a Flag then only transformations that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any transformations can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of transformations selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def Total(model, exists=Oasys.gRPC.defaultArg):
        """
        Returns the total number of transformations in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing transformations should be counted. If false or omitted
            referenced but undefined transformations will also be included in the total

        Returns
        -------
        int
            number of transformations
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the transformations in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all transformations will be unset in
        flag : Flag
            Flag to unset on the transformations

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)



# Instance methods
    def AddRow(self, data, row=Oasys.gRPC.defaultArg):
        """
        Adds a row of data for a \*DEFINE_TRANSFORMATION

        Parameters
        ----------
        data : List of data
            The data you want to add
        row : integer
            Optional. The row you want to add the data at. Existing transforms will be shifted.
            If omitted the data will be added to the end of the existing transforms.
            Note that row indices start at 0

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AddRow", data, row)

    def AssociateComment(self, comment):
        """
        Associates a comment with a transformation

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the transformation

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
        Clears a flag on the transformation

        Parameters
        ----------
        flag : Flag
            Flag to clear on the transformation

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the transformation. The target include of the copied transformation can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        Transformation
            Transformation object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a transformation

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the transformation

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
        Checks if the transformation is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the transformation

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a transformation

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a Transformation property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the Transformation.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            transformation property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def GetRow(self, row):
        """
        Returns the data for a row in the transformation

        Parameters
        ----------
        row : integer
            The row you want the data for. Note row indices start at 0

        Returns
        -------
        list
            A list of numbers containing the row variables
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetRow", row)

    def Keyword(self):
        """
        Returns the keyword for this transformation.
        Note that a carriage return is not added.
        See also Transformation.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the transformation.
        Note that a carriage return is not added.
        See also Transformation.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next transformation in the model

        Returns
        -------
        Transformation
            Transformation object (or None if there are no more transformations in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous transformation in the model

        Returns
        -------
        Transformation
            Transformation object (or None if there are no more transformations in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def RemoveRow(self, row):
        """
        Removes the data for a row in \*DEFINE_TRANSFORMATION

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
        Sets a flag on the transformation

        Parameters
        ----------
        flag : Flag
            Flag to set on the transformation

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def SetRow(self, row, data):
        """
        Sets the data for a row in \*DEFINE_TRANSFORMATION

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

    def ViewParameters(self):
        """
        Object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. This function temporarily
        changes the behaviour so that if a property is a parameter the parameter name is returned instead.
        This can be used with 'method chaining' (see the example below) to make sure a property argument is correct

        Returns
        -------
        Transformation
            Transformation object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this transformation

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

