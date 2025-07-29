import Oasys.gRPC


# Metaclass for static properties and constants
class PrescribedOrientationRigidType(type):
    _consts = {'ANGLES', 'DIRCOS', 'EULERP', 'VECTOR'}

    def __getattr__(cls, name):
        if name in PrescribedOrientationRigidType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("PrescribedOrientationRigid class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in PrescribedOrientationRigidType._consts:
            raise AttributeError("Cannot set PrescribedOrientationRigid class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class PrescribedOrientationRigid(Oasys.gRPC.OasysItem, metaclass=PrescribedOrientationRigidType):
    _props = {'birth', 'body', 'death', 'heading', 'id', 'include', 'intrp', 'intrp_1', 'iseq', 'ishft', 'lcidc11', 'lcidc12', 'lcidc13', 'lcidc21', 'lcidc22', 'lcidc23', 'lcidc31', 'lcidc32', 'lcidc33', 'lcide1', 'lcide2', 'lcide3', 'lcide4', 'lcidq1', 'lcidq2', 'lcidq3', 'lcids', 'lcidv1', 'lcidv2', 'lcidv3', 'option', 'pida', 'pidb', 'toffset', 'valspin'}
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
        if name in PrescribedOrientationRigid._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in PrescribedOrientationRigid._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("PrescribedOrientationRigid instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in PrescribedOrientationRigid._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in PrescribedOrientationRigid._rprops:
            raise AttributeError("Cannot set read-only PrescribedOrientationRigid instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, option, pidb, label=Oasys.gRPC.defaultArg, heading=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, option, pidb, label, heading)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new PrescribedOrientationRigid object

        Parameters
        ----------
        model : Model
            Model that prescribed orientation rigid will be created in
        option : constant
            Suffix for boundary prescribed orientation rigid. Can be
            PrescribedOrientationRigid.DIRCOS
            PrescribedOrientationRigid.ANGLES
            PrescribedOrientationRigid.EULERP
            PrescribedOrientationRigid.VECTOR
        pidb : integer
            Part ID for rigid body B whose orientation is prescribed
        label : integer
            Optional. PrescribedOrientationRigid number
        heading : string
            Optional. Title for the PrescribedOrientationRigid

        Returns
        -------
        PrescribedOrientationRigid
            PrescribedOrientationRigid object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def Create(model, modal=Oasys.gRPC.defaultArg):
        """
        Starts an interactive editing panel to create a prescribed orientation rigid

        Parameters
        ----------
        model : Model
            Model that the prescribed orientation rigid will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        PrescribedOrientationRigid
            PrescribedOrientationRigid object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def First(model):
        """
        Returns the first prescribed orientation rigid in the model

        Parameters
        ----------
        model : Model
            Model to get first prescribed orientation rigid in

        Returns
        -------
        PrescribedOrientationRigid
            PrescribedOrientationRigid object (or None if there are no prescribed orientation rigids in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FlagAll(model, flag):
        """
        Flags all of the prescribed orientation rigids in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all prescribed orientation rigids will be flagged in
        flag : Flag
            Flag to set on the prescribed orientation rigids

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of PrescribedOrientationRigid objects or properties for all of the prescribed orientation rigids in a model in PRIMER.
        If the optional property argument is not given then a list of PrescribedOrientationRigid objects is returned.
        If the property argument is given, that property value for each prescribed orientation rigid is returned in the list
        instead of a PrescribedOrientationRigid object

        Parameters
        ----------
        model : Model
            Model to get prescribed orientation rigids from
        property : string
            Optional. Name for property to get for all prescribed orientation rigids in the model

        Returns
        -------
        list
            List of PrescribedOrientationRigid objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of PrescribedOrientationRigid objects for all of the flagged prescribed orientation rigids in a model in PRIMER
        If the optional property argument is not given then a list of PrescribedOrientationRigid objects is returned.
        If the property argument is given, then that property value for each prescribed orientation rigid is returned in the list
        instead of a PrescribedOrientationRigid object

        Parameters
        ----------
        model : Model
            Model to get prescribed orientation rigids from
        flag : Flag
            Flag set on the prescribed orientation rigids that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged prescribed orientation rigids in the model

        Returns
        -------
        list
            List of PrescribedOrientationRigid objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the PrescribedOrientationRigid object for a prescribed orientation rigid ID

        Parameters
        ----------
        model : Model
            Model to find the prescribed orientation rigid in
        number : integer
            number of the prescribed orientation rigid you want the PrescribedOrientationRigid object for

        Returns
        -------
        PrescribedOrientationRigid
            PrescribedOrientationRigid object (or None if prescribed orientation rigid does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last prescribed orientation rigid in the model

        Parameters
        ----------
        model : Model
            Model to get last prescribed orientation rigid in

        Returns
        -------
        PrescribedOrientationRigid
            PrescribedOrientationRigid object (or None if there are no prescribed orientation rigids in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def Select(flag, prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg):
        """
        Allows the user to select prescribed orientation rigids using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting prescribed orientation rigids
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only prescribed orientation rigids from that model can be selected.
            If the argument is a Flag then only prescribed orientation rigids that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any prescribed orientation rigids can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of prescribed orientation rigids selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged prescribed orientation rigids in the model. The prescribed orientation rigids will be sketched until you either call
        PrescribedOrientationRigid.Unsketch(),
        PrescribedOrientationRigid.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged prescribed orientation rigids will be sketched in
        flag : Flag
            Flag set on the prescribed orientation rigids that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the prescribed orientation rigids are sketched.
            If omitted redraw is true. If you want to sketch flagged prescribed orientation rigids several times and only
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
        Returns the total number of prescribed orientation rigids in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing prescribed orientation rigids should be counted. If false or omitted
            referenced but undefined prescribed orientation rigids will also be included in the total

        Returns
        -------
        int
            number of prescribed orientation rigids
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the prescribed orientation rigids in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all prescribed orientation rigids will be unset in
        flag : Flag
            Flag to unset on the prescribed orientation rigids

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all prescribed orientation rigids

        Parameters
        ----------
        model : Model
            Model that all prescribed orientation rigids will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the prescribed orientation rigids are unsketched.
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
        Unsketches all flagged prescribed orientation rigids in the model

        Parameters
        ----------
        model : Model
            Model that all prescribed orientation rigids will be unsketched in
        flag : Flag
            Flag set on the prescribed orientation rigids that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the prescribed orientation rigids are unsketched.
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
        Associates a comment with a prescribed orientation rigid

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the prescribed orientation rigid

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
        Clears a flag on the prescribed orientation rigid

        Parameters
        ----------
        flag : Flag
            Flag to clear on the prescribed orientation rigid

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the prescribed orientation rigid. The target include of the copied prescribed orientation rigid can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        PrescribedOrientationRigid
            PrescribedOrientationRigid object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a prescribed orientation rigid

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the prescribed orientation rigid

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
        Checks if the prescribed orientation rigid is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the prescribed orientation rigid

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a prescribed orientation rigid

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a PrescribedOrientationRigid property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the PrescribedOrientationRigid.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            prescribed orientation rigid property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this prescribed orientation rigid.
        Note that a carriage return is not added.
        See also PrescribedOrientationRigid.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the prescribed orientation rigid.
        Note that a carriage return is not added.
        See also PrescribedOrientationRigid.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next prescribed orientation rigid in the model

        Returns
        -------
        PrescribedOrientationRigid
            PrescribedOrientationRigid object (or None if there are no more prescribed orientation rigids in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous prescribed orientation rigid in the model

        Returns
        -------
        PrescribedOrientationRigid
            PrescribedOrientationRigid object (or None if there are no more prescribed orientation rigids in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on the prescribed orientation rigid

        Parameters
        ----------
        flag : Flag
            Flag to set on the prescribed orientation rigid

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the prescribed orientation rigid. The prescribed orientation rigid will be sketched until you either call
        PrescribedOrientationRigid.Unsketch(),
        PrescribedOrientationRigid.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the prescribed orientation rigid is sketched.
            If omitted redraw is true. If you want to sketch several prescribed orientation rigids and only
            redraw after the last one then use false for redraw and call
            View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Sketch", redraw)

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the prescribed orientation rigid

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the prescribed orientation rigid is unsketched.
            If omitted redraw is true. If you want to unsketch several prescribed orientation rigids and only
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
        PrescribedOrientationRigid
            PrescribedOrientationRigid object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this prescribed orientation rigid

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

