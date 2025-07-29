import Oasys.gRPC


# Metaclass for static properties and constants
class ElementDeathType(type):
    _consts = {'BEAM', 'BEAM_SET', 'SHELL', 'SHELL_SET', 'SOLID', 'SOLID_SET', 'THICK_SHELL', 'THICK_SHELL_SET'}

    def __getattr__(cls, name):
        if name in ElementDeathType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("ElementDeath class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in ElementDeathType._consts:
            raise AttributeError("Cannot set ElementDeath class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class ElementDeath(Oasys.gRPC.OasysItem, metaclass=ElementDeathType):
    _props = {'boxid', 'cid', 'eid', 'idgrp', 'include', 'inout', 'option', 'percent', 'sid', 'time', 'title', 'type'}
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
        if name in ElementDeath._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in ElementDeath._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("ElementDeath instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in ElementDeath._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in ElementDeath._rprops:
            raise AttributeError("Cannot set read-only ElementDeath instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, type, eid_sid):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, type, eid_sid)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new ElementDeath object

        Parameters
        ----------
        model : Model
            Model that element death will be created in
        type : string
            ElementDeath type. Can be
            ElementDeath.SOLID,
            ElementDeath.SOLID_SET,
            ElementDeath.BEAM,
            ElementDeath.BEAM_SET,
            ElementDeath.SHELL,
            ElementDeath.SHELL_SET,
            ElementDeath.THICK_SHELL or
            ElementDeath.THICK_SHELL_SET
        eid_sid : integer
            Element or element set ID

        Returns
        -------
        ElementDeath
            ElementDeath object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def Create(model, modal=Oasys.gRPC.defaultArg):
        """
        Starts an interactive editing panel to create a element death

        Parameters
        ----------
        model : Model
            Model that the element death will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        ElementDeath
            ElementDeath object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def First(model):
        """
        Returns the first element death in the model

        Parameters
        ----------
        model : Model
            Model to get first element death in

        Returns
        -------
        ElementDeath
            ElementDeath object (or None if there are no element deaths in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FlagAll(model, flag):
        """
        Flags all of the element deaths in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all element deaths will be flagged in
        flag : Flag
            Flag to set on the element deaths

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of ElementDeath objects or properties for all of the element deaths in a model in PRIMER.
        If the optional property argument is not given then a list of ElementDeath objects is returned.
        If the property argument is given, that property value for each element death is returned in the list
        instead of a ElementDeath object

        Parameters
        ----------
        model : Model
            Model to get element deaths from
        property : string
            Optional. Name for property to get for all element deaths in the model

        Returns
        -------
        list
            List of ElementDeath objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of ElementDeath objects for all of the flagged element deaths in a model in PRIMER
        If the optional property argument is not given then a list of ElementDeath objects is returned.
        If the property argument is given, then that property value for each element death is returned in the list
        instead of a ElementDeath object

        Parameters
        ----------
        model : Model
            Model to get element deaths from
        flag : Flag
            Flag set on the element deaths that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged element deaths in the model

        Returns
        -------
        list
            List of ElementDeath objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the ElementDeath object for a element death ID

        Parameters
        ----------
        model : Model
            Model to find the element death in
        number : integer
            number of the element death you want the ElementDeath object for

        Returns
        -------
        ElementDeath
            ElementDeath object (or None if element death does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last element death in the model

        Parameters
        ----------
        model : Model
            Model to get last element death in

        Returns
        -------
        ElementDeath
            ElementDeath object (or None if there are no element deaths in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def Select(flag, prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg):
        """
        Allows the user to select element deaths using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting element deaths
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only element deaths from that model can be selected.
            If the argument is a Flag then only element deaths that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any element deaths can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of element deaths selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def Total(model, exists=Oasys.gRPC.defaultArg):
        """
        Returns the total number of element deaths in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing element deaths should be counted. If false or omitted
            referenced but undefined element deaths will also be included in the total

        Returns
        -------
        int
            number of element deaths
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the element deaths in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all element deaths will be unset in
        flag : Flag
            Flag to unset on the element deaths

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)



# Instance methods
    def AssociateComment(self, comment):
        """
        Associates a comment with a element death

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the element death

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
        Clears a flag on the element death

        Parameters
        ----------
        flag : Flag
            Flag to clear on the element death

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the element death. The target include of the copied element death can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        ElementDeath
            ElementDeath object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a element death

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the element death

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
        Checks if the element death is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the element death

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a element death

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a ElementDeath property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the ElementDeath.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            element death property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this element death (\*DEFINE_ELEMENT_DEATH).
        Note that a carriage return is not added.
        See also ElementDeath.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the element death.
        Note that a carriage return is not added.
        See also ElementDeath.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next element death in the model

        Returns
        -------
        ElementDeath
            ElementDeath object (or None if there are no more element deaths in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous element death in the model

        Returns
        -------
        ElementDeath
            ElementDeath object (or None if there are no more element deaths in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on the element death

        Parameters
        ----------
        flag : Flag
            Flag to set on the element death

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
        ElementDeath
            ElementDeath object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this element death

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

