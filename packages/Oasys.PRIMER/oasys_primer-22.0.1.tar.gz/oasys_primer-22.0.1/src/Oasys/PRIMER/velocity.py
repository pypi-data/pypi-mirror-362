import Oasys.gRPC


# Metaclass for static properties and constants
class VelocityType(type):

    def __getattr__(cls, name):

        raise AttributeError("Velocity class attribute '{}' does not exist".format(name))


class Velocity(Oasys.gRPC.OasysItem, metaclass=VelocityType):
    _props = {'boxid', 'icid', 'include', 'irigid', 'nsid', 'nsidex', 'vx', 'vxe', 'vxr', 'vxre', 'vy', 'vye', 'vyr', 'vyre', 'vz', 'vze', 'vzr', 'vzre'}
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
        if name in Velocity._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in Velocity._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("Velocity instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Velocity._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in Velocity._rprops:
            raise AttributeError("Cannot set read-only Velocity instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, nsid, vx, vy, vz, vxr, vyr, vzr, boxid=Oasys.gRPC.defaultArg, irigid=Oasys.gRPC.defaultArg, nsidex=Oasys.gRPC.defaultArg, vxe=Oasys.gRPC.defaultArg, vye=Oasys.gRPC.defaultArg, vze=Oasys.gRPC.defaultArg, vxre=Oasys.gRPC.defaultArg, vyre=Oasys.gRPC.defaultArg, vzre=Oasys.gRPC.defaultArg, icid=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, nsid, vx, vy, vz, vxr, vyr, vzr, boxid, irigid, nsidex, vxe, vye, vze, vxre, vyre, vzre, icid)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new Velocity object

        Parameters
        ----------
        model : Model
            Model that velocity will be created in
        nsid : integer
            Set Node set ID
        vx : float
            Initial velocity in X direction
        vy : float
            Initial velocity in Y direction
        vz : float
            Initial velocity in Z direction
        vxr : float
            Initial rotational velocity about X axis
        vyr : float
            Initial rotational velocity about Y axis
        vzr : float
            Initial rotational velocity about Z axis
        boxid : integer
            Optional. Define box containing nodes
        irigid : integer
            Optional. IRIGID flag
        nsidex : integer
            Optional. Set Exempted Node set ID
        vxe : float
            Optional. Initial velocity in X direction of exempted nodes
        vye : float
            Optional. Initial velocity in Y direction of exempted nodes
        vze : float
            Optional. Initial velocity in Z direction of exempted nodes
        vxre : float
            Optional. Initial rotational velocity about X axis of exempted nodes
        vyre : float
            Optional. Initial rotational velocity about Y axis of exempted nodes
        vzre : float
            Optional. Initial rotational velocity about Z axis of exempted nodes
        icid : float
            Optional. Local coordinate system nodes

        Returns
        -------
        Velocity
            Velocity object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def BlankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the initial velocitys in the model

        Parameters
        ----------
        model : Model
            Model that all initial velocitys will be blanked in
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
        Blanks all of the flagged initial velocitys in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged initial velocitys will be blanked in
        flag : Flag
            Flag set on the initial velocitys that you want to blank
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

    def First(model):
        """
        Returns the first initial velocity in the model

        Parameters
        ----------
        model : Model
            Model to get first initial velocity in

        Returns
        -------
        Velocity
            Velocity object (or None if there are no initial velocitys in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FlagAll(model, flag):
        """
        Flags all of the initial velocitys in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all initial velocitys will be flagged in
        flag : Flag
            Flag to set on the initial velocitys

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Velocity objects or properties for all of the initial velocitys in a model in PRIMER.
        If the optional property argument is not given then a list of Velocity objects is returned.
        If the property argument is given, that property value for each initial velocity is returned in the list
        instead of a Velocity object

        Parameters
        ----------
        model : Model
            Model to get initial velocitys from
        property : string
            Optional. Name for property to get for all initial velocitys in the model

        Returns
        -------
        list
            List of Velocity objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Velocity objects for all of the flagged initial velocitys in a model in PRIMER
        If the optional property argument is not given then a list of Velocity objects is returned.
        If the property argument is given, then that property value for each initial velocity is returned in the list
        instead of a Velocity object

        Parameters
        ----------
        model : Model
            Model to get initial velocitys from
        flag : Flag
            Flag set on the initial velocitys that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged initial velocitys in the model

        Returns
        -------
        list
            List of Velocity objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the Velocity object for a initial velocity ID

        Parameters
        ----------
        model : Model
            Model to find the initial velocity in
        number : integer
            number of the initial velocity you want the Velocity object for

        Returns
        -------
        Velocity
            Velocity object (or None if initial velocity does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last initial velocity in the model

        Parameters
        ----------
        model : Model
            Model to get last initial velocity in

        Returns
        -------
        Velocity
            Velocity object (or None if there are no initial velocitys in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a initial velocity

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only initial velocitys from that model can be picked.
            If the argument is a Flag then only initial velocitys that
            are flagged with limit can be selected.
            If omitted, or None, any initial velocitys from any model can be selected.
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
        Velocity
            Velocity object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def Select(flag, prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg):
        """
        Allows the user to select initial velocitys using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting initial velocitys
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only initial velocitys from that model can be selected.
            If the argument is a Flag then only initial velocitys that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any initial velocitys can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of initial velocitys selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged initial velocitys in the model. The initial velocitys will be sketched until you either call
        Velocity.Unsketch(),
        Velocity.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged initial velocitys will be sketched in
        flag : Flag
            Flag set on the initial velocitys that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the initial velocitys are sketched.
            If omitted redraw is true. If you want to sketch flagged initial velocitys several times and only
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
        Returns the total number of initial velocitys in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing initial velocitys should be counted. If false or omitted
            referenced but undefined initial velocitys will also be included in the total

        Returns
        -------
        int
            number of initial velocitys
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnblankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the initial velocitys in the model

        Parameters
        ----------
        model : Model
            Model that all initial velocitys will be unblanked in
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
        Unblanks all of the flagged initial velocitys in the model

        Parameters
        ----------
        model : Model
            Model that the flagged initial velocitys will be unblanked in
        flag : Flag
            Flag set on the initial velocitys that you want to unblank
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
        Unsets a defined flag on all of the initial velocitys in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all initial velocitys will be unset in
        flag : Flag
            Flag to unset on the initial velocitys

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all initial velocitys

        Parameters
        ----------
        model : Model
            Model that all initial velocitys will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the initial velocitys are unsketched.
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
        Unsketches all flagged initial velocitys in the model

        Parameters
        ----------
        model : Model
            Model that all initial velocitys will be unsketched in
        flag : Flag
            Flag set on the initial velocitys that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the initial velocitys are unsketched.
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
        Associates a comment with a initial velocity

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the initial velocity

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def Blank(self):
        """
        Blanks the initial velocity

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank")

    def Blanked(self):
        """
        Checks if the initial velocity is blanked or not

        Returns
        -------
        bool
            True if blanked, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blanked")

    def ClearFlag(self, flag):
        """
        Clears a flag on the initial velocity

        Parameters
        ----------
        flag : Flag
            Flag to clear on the initial velocity

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the initial velocity. The target include of the copied initial velocity can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        Velocity
            Velocity object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a initial velocity

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the initial velocity

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "DetachComment", comment)

    def Flagged(self, flag):
        """
        Checks if the initial velocity is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the initial velocity

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a initial velocity

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a Velocity property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the Velocity.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            initial velocity property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this initial velocity (\*INITIAL_VELOCITY).
        Note that a carriage return is not added.
        See also Velocity.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the initial velocity.
        Note that a carriage return is not added.
        See also Velocity.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next initial velocity in the model

        Returns
        -------
        Velocity
            Velocity object (or None if there are no more initial velocitys in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous initial velocity in the model

        Returns
        -------
        Velocity
            Velocity object (or None if there are no more initial velocitys in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on the initial velocity

        Parameters
        ----------
        flag : Flag
            Flag to set on the initial velocity

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the initial velocity. The initial velocity will be sketched until you either call
        Velocity.Unsketch(),
        Velocity.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the initial velocity is sketched.
            If omitted redraw is true. If you want to sketch several initial velocitys and only
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
        Unblanks the initial velocity

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank")

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the initial velocity

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the initial velocity is unsketched.
            If omitted redraw is true. If you want to unsketch several initial velocitys and only
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
        Velocity
            Velocity object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this initial velocity

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

