import Oasys.gRPC


# Metaclass for static properties and constants
class PrescribedAccelerometerRigidType(type):

    def __getattr__(cls, name):

        raise AttributeError("PrescribedAccelerometerRigid class attribute '{}' does not exist".format(name))


class PrescribedAccelerometerRigid(Oasys.gRPC.OasysItem, metaclass=PrescribedAccelerometerRigidType):
    _props = {'include', 'pid', 'solv'}
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
        if name in PrescribedAccelerometerRigid._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in PrescribedAccelerometerRigid._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("PrescribedAccelerometerRigid instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in PrescribedAccelerometerRigid._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in PrescribedAccelerometerRigid._rprops:
            raise AttributeError("Cannot set read-only PrescribedAccelerometerRigid instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, pid, solv=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, pid, solv)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new PrescribedAccelerometerRigid object

        Parameters
        ----------
        model : Model
            Model that prescribed accelerometer rigid will be created in
        pid : integer
            Part ID for rigid body whose motion is prescribed
        solv : integer
            Optional. Solver type

        Returns
        -------
        PrescribedAccelerometerRigid
            PrescribedAccelerometerRigid object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def Create(model, modal=Oasys.gRPC.defaultArg):
        """
        Starts an interactive editing panel to create a prescribed accelerometer rigid

        Parameters
        ----------
        model : Model
            Model that the prescribed accelerometer rigid will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        PrescribedAccelerometerRigid
            PrescribedAccelerometerRigid object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def First(model):
        """
        Returns the first prescribed accelerometer rigid in the model

        Parameters
        ----------
        model : Model
            Model to get first prescribed accelerometer rigid in

        Returns
        -------
        PrescribedAccelerometerRigid
            PrescribedAccelerometerRigid object (or None if there are no prescribed accelerometer rigids in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FlagAll(model, flag):
        """
        Flags all of the prescribed accelerometer rigids in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all prescribed accelerometer rigids will be flagged in
        flag : Flag
            Flag to set on the prescribed accelerometer rigids

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of PrescribedAccelerometerRigid objects or properties for all of the prescribed accelerometer rigids in a model in PRIMER.
        If the optional property argument is not given then a list of PrescribedAccelerometerRigid objects is returned.
        If the property argument is given, that property value for each prescribed accelerometer rigid is returned in the list
        instead of a PrescribedAccelerometerRigid object

        Parameters
        ----------
        model : Model
            Model to get prescribed accelerometer rigids from
        property : string
            Optional. Name for property to get for all prescribed accelerometer rigids in the model

        Returns
        -------
        list
            List of PrescribedAccelerometerRigid objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of PrescribedAccelerometerRigid objects for all of the flagged prescribed accelerometer rigids in a model in PRIMER
        If the optional property argument is not given then a list of PrescribedAccelerometerRigid objects is returned.
        If the property argument is given, then that property value for each prescribed accelerometer rigid is returned in the list
        instead of a PrescribedAccelerometerRigid object

        Parameters
        ----------
        model : Model
            Model to get prescribed accelerometer rigids from
        flag : Flag
            Flag set on the prescribed accelerometer rigids that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged prescribed accelerometer rigids in the model

        Returns
        -------
        list
            List of PrescribedAccelerometerRigid objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the PrescribedAccelerometerRigid object for a prescribed accelerometer rigid ID

        Parameters
        ----------
        model : Model
            Model to find the prescribed accelerometer rigid in
        number : integer
            number of the prescribed accelerometer rigid you want the PrescribedAccelerometerRigid object for

        Returns
        -------
        PrescribedAccelerometerRigid
            PrescribedAccelerometerRigid object (or None if prescribed accelerometer rigid does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last prescribed accelerometer rigid in the model

        Parameters
        ----------
        model : Model
            Model to get last prescribed accelerometer rigid in

        Returns
        -------
        PrescribedAccelerometerRigid
            PrescribedAccelerometerRigid object (or None if there are no prescribed accelerometer rigids in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def Select(flag, prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg):
        """
        Allows the user to select prescribed accelerometer rigids using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting prescribed accelerometer rigids
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only prescribed accelerometer rigids from that model can be selected.
            If the argument is a Flag then only prescribed accelerometer rigids that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any prescribed accelerometer rigids can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of prescribed accelerometer rigids selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def Total(model, exists=Oasys.gRPC.defaultArg):
        """
        Returns the total number of prescribed accelerometer rigids in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing prescribed accelerometer rigids should be counted. If false or omitted
            referenced but undefined prescribed accelerometer rigids will also be included in the total

        Returns
        -------
        int
            number of prescribed accelerometer rigids
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the prescribed accelerometer rigids in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all prescribed accelerometer rigids will be unset in
        flag : Flag
            Flag to unset on the prescribed accelerometer rigids

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)



# Instance methods
    def AssociateComment(self, comment):
        """
        Associates a comment with a prescribed accelerometer rigid

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the prescribed accelerometer rigid

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
        Clears a flag on the prescribed accelerometer rigid

        Parameters
        ----------
        flag : Flag
            Flag to clear on the prescribed accelerometer rigid

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the prescribed accelerometer rigid. The target include of the copied prescribed accelerometer rigid can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        PrescribedAccelerometerRigid
            PrescribedAccelerometerRigid object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a prescribed accelerometer rigid

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the prescribed accelerometer rigid

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
        Checks if the prescribed accelerometer rigid is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the prescribed accelerometer rigid

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a prescribed accelerometer rigid

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a PrescribedAccelerometerRigid property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the PrescribedAccelerometerRigid.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            prescribed accelerometer rigid property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def GetRow(self, row):
        """
        Returns the data for a row in the prescribed accelerometer rigid

        Parameters
        ----------
        row : integer
            The row you want the data for. Note row indices start at 0

        Returns
        -------
        list
            A list of numbers containing the row variables NID, CID, LCIDX, LCIDY and LCIDZ
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetRow", row)

    def Keyword(self):
        """
        Returns the keyword for this prescribed accelerometer rigid.
        Note that a carriage return is not added.
        See also PrescribedAccelerometerRigid.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the prescribed accelerometer rigid.
        Note that a carriage return is not added.
        See also PrescribedAccelerometerRigid.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next prescribed accelerometer rigid in the model

        Returns
        -------
        PrescribedAccelerometerRigid
            PrescribedAccelerometerRigid object (or None if there are no more prescribed accelerometer rigids in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous prescribed accelerometer rigid in the model

        Returns
        -------
        PrescribedAccelerometerRigid
            PrescribedAccelerometerRigid object (or None if there are no more prescribed accelerometer rigids in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def RemoveRow(self, row):
        """
        Removes the data for a row in \*BOUNDARY_PRESCRIBED_ACCELEROMETER_RIGID

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
        Sets a flag on the prescribed accelerometer rigid

        Parameters
        ----------
        flag : Flag
            Flag to set on the prescribed accelerometer rigid

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def SetRow(self, row, data):
        """
        Sets the data for a row in \*BOUNDARY_PRESCRIBED_ACCELEROMETER_RIGID

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
        PrescribedAccelerometerRigid
            PrescribedAccelerometerRigid object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this prescribed accelerometer rigid

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

