import Oasys.gRPC


# Metaclass for static properties and constants
class TerminationType(type):
    _consts = {'BODY', 'CONTACT', 'CURVE', 'DELETED_SHELLS', 'DELETED_SHELLS_SET', 'DELETED_SOLIDS', 'DELETED_SOLIDS_SET', 'DOF_X', 'DOF_Y', 'DOF_Z', 'NODE', 'SENSOR', 'STOP_MAG', 'STOP_X', 'STOP_Y', 'STOP_Z'}

    def __getattr__(cls, name):
        if name in TerminationType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("Termination class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in TerminationType._consts:
            raise AttributeError("Cannot set Termination class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class Termination(Oasys.gRPC.OasysItem, metaclass=TerminationType):
    _props = {'actTime', 'dof', 'duration', 'id', 'include', 'maxc', 'minc', 'numDeletedElems', 'stop', 'threshold'}
    _rprops = {'exists', 'model', 'ptype', 'type'}


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
        if name in Termination._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in Termination._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("Termination instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Termination._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in Termination._rprops:
            raise AttributeError("Cannot set read-only Termination instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, type, id):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, type, id)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new Termination object

        Parameters
        ----------
        model : Model
            Model that termination will be created in
        type : constant
            Specify the type of Termination (Can be
            Termination.BODY or 
            Termination.CONTACT or 
            Termination.CURVE or 
            Termination.DELETED_SHELLS or 
            Termination.DELETED_SOLIDS or 
            Termination.NODE or 
            Termination.SENSOR)
        id : integer
            Can be Part ID for Termination.BODY or
            Termination.DELETED_SHELLS or 
            Termination.DELETED_SOLIDS, OR
            Contact ID for Termination.CONTACT, OR
            Node ID for Termination.NODE, OR
            Curve ID for Termination.CURVE, OR
            Part Set ID for Termination.DELETED_SHELLS_SET or 
            Termination.DELETED_SOLIDS_SET, OR
            Sensor Switch ID for Termination.SENSOR

        Returns
        -------
        Termination
            Termination object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def Create(model, modal=Oasys.gRPC.defaultArg):
        """
        Starts an interactive editing panel to create a termination

        Parameters
        ----------
        model : Model
            Model that the termination will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        Termination
            Termination object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def First(model):
        """
        Returns the first termination in the model

        Parameters
        ----------
        model : Model
            Model to get first termination in

        Returns
        -------
        Termination
            Termination object (or None if there are no terminations in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FlagAll(model, flag):
        """
        Flags all of the terminations in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all terminations will be flagged in
        flag : Flag
            Flag to set on the terminations

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Termination objects or properties for all of the terminations in a model in PRIMER.
        If the optional property argument is not given then a list of Termination objects is returned.
        If the property argument is given, that property value for each termination is returned in the list
        instead of a Termination object

        Parameters
        ----------
        model : Model
            Model to get terminations from
        property : string
            Optional. Name for property to get for all terminations in the model

        Returns
        -------
        list
            List of Termination objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Termination objects for all of the flagged terminations in a model in PRIMER
        If the optional property argument is not given then a list of Termination objects is returned.
        If the property argument is given, then that property value for each termination is returned in the list
        instead of a Termination object

        Parameters
        ----------
        model : Model
            Model to get terminations from
        flag : Flag
            Flag set on the terminations that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged terminations in the model

        Returns
        -------
        list
            List of Termination objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the Termination object for a termination ID

        Parameters
        ----------
        model : Model
            Model to find the termination in
        number : integer
            number of the termination you want the Termination object for

        Returns
        -------
        Termination
            Termination object (or None if termination does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last termination in the model

        Parameters
        ----------
        model : Model
            Model to get last termination in

        Returns
        -------
        Termination
            Termination object (or None if there are no terminations in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def Select(flag, prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg):
        """
        Allows the user to select terminations using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting terminations
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only terminations from that model can be selected.
            If the argument is a Flag then only terminations that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any terminations can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of terminations selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def Total(model, exists=Oasys.gRPC.defaultArg):
        """
        Returns the total number of terminations in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing terminations should be counted. If false or omitted
            referenced but undefined terminations will also be included in the total

        Returns
        -------
        int
            number of terminations
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the terminations in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all terminations will be unset in
        flag : Flag
            Flag to unset on the terminations

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)



# Instance methods
    def AssociateComment(self, comment):
        """
        Associates a comment with a termination

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the termination

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
        Clears a flag on the termination

        Parameters
        ----------
        flag : Flag
            Flag to clear on the termination

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the termination. The target include of the copied termination can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        Termination
            Termination object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a termination

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the termination

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
        Checks if the termination is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the termination

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a termination

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a Termination property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the Termination.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            termination property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this Termination (\*TERMINATION_xxxx)
        Note that a carriage return is not added.
        See also Termination.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the Termination.
        Note that a carriage return is not added.
        See also Termination.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next termination in the model

        Returns
        -------
        Termination
            Termination object (or None if there are no more terminations in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous termination in the model

        Returns
        -------
        Termination
            Termination object (or None if there are no more terminations in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on the termination

        Parameters
        ----------
        flag : Flag
            Flag to set on the termination

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
        Termination
            Termination object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this termination

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

