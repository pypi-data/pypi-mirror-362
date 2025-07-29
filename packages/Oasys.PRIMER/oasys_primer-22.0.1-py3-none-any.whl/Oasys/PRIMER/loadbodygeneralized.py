import Oasys.gRPC


# Metaclass for static properties and constants
class LoadBodyGeneralizedType(type):
    _consts = {'NODE', 'SET_NODE', 'SET_PART'}

    def __getattr__(cls, name):
        if name in LoadBodyGeneralizedType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("LoadBodyGeneralized class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in LoadBodyGeneralizedType._consts:
            raise AttributeError("Cannot set LoadBodyGeneralized class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class LoadBodyGeneralized(Oasys.gRPC.OasysItem, metaclass=LoadBodyGeneralizedType):
    _props = {'angtyp', 'ax', 'ay', 'az', 'cid', 'drlcid', 'include', 'lcid', 'n1', 'n2', 'omx', 'omy', 'omz', 'type', 'xc', 'yc', 'zc'}
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
        if name in LoadBodyGeneralized._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in LoadBodyGeneralized._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("LoadBodyGeneralized instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in LoadBodyGeneralized._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in LoadBodyGeneralized._rprops:
            raise AttributeError("Cannot set read-only LoadBodyGeneralized instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, type, n1, n2, lcid, drlcid=Oasys.gRPC.defaultArg, xc=Oasys.gRPC.defaultArg, yc=Oasys.gRPC.defaultArg, zc=Oasys.gRPC.defaultArg, ax=Oasys.gRPC.defaultArg, ay=Oasys.gRPC.defaultArg, az=Oasys.gRPC.defaultArg, omx=Oasys.gRPC.defaultArg, omy=Oasys.gRPC.defaultArg, omz=Oasys.gRPC.defaultArg, cid=Oasys.gRPC.defaultArg, angtyp=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, type, n1, n2, lcid, drlcid, xc, yc, zc, ax, ay, az, omx, omy, omz, cid, angtyp)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new LoadBodyGeneralized object

        Parameters
        ----------
        model : Model
            Model that load body generalized will be created in
        type : constant
            Specify the type of load body generalized (Can be
            LoadBodyGeneralized.NODE or
            LoadBodyGeneralized.SET_NODE or
            LoadBodyGeneralized.SET_PART)
        n1 : integer
            Beginning Node ID for body force load or the node or Part set ID
        n2 : integer
            Ending Node ID for body force load. Set to zero if a set ID is defined
        lcid : integer
            Curve ID
        drlcid : integer
            Optional. Curve ID for dynamic relaxation phase
        xc : float
            Optional. X-center of rotation
        yc : float
            Optional. Y-center of rotation
        zc : float
            Optional. Z-center of rotation
        ax : float
            Optional. Scale factor for acceleration in x-direction
        ay : float
            Optional. Scale factor for acceleration in y-direction
        az : float
            Optional. Scale factor for acceleration in z-direction
        omx : float
            Optional. Scale factor for x-angular velocity or acceleration
        omy : float
            Optional. Scale factor for y-angular velocity or acceleration
        omz : float
            Optional. Scale factor for z-angular velocity or acceleration
        cid : integer
            Optional. Coordinate system ID to define acceleration
        angtyp : string
            Optional. Type of body loads

        Returns
        -------
        LoadBodyGeneralized
            LoadBodyGeneralized object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def BlankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the load body generalizeds in the model

        Parameters
        ----------
        model : Model
            Model that all load body generalizeds will be blanked in
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
        Blanks all of the flagged load body generalizeds in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged load body generalizeds will be blanked in
        flag : Flag
            Flag set on the load body generalizeds that you want to blank
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
        Returns the first load body generalized in the model

        Parameters
        ----------
        model : Model
            Model to get first load body generalized in

        Returns
        -------
        LoadBodyGeneralized
            LoadBodyGeneralized object (or None if there are no load body generalizeds in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FlagAll(model, flag):
        """
        Flags all of the load body generalizeds in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all load body generalizeds will be flagged in
        flag : Flag
            Flag to set on the load body generalizeds

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of LoadBodyGeneralized objects or properties for all of the load body generalizeds in a model in PRIMER.
        If the optional property argument is not given then a list of LoadBodyGeneralized objects is returned.
        If the property argument is given, that property value for each load body generalized is returned in the list
        instead of a LoadBodyGeneralized object

        Parameters
        ----------
        model : Model
            Model to get load body generalizeds from
        property : string
            Optional. Name for property to get for all load body generalizeds in the model

        Returns
        -------
        list
            List of LoadBodyGeneralized objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of LoadBodyGeneralized objects for all of the flagged load body generalizeds in a model in PRIMER
        If the optional property argument is not given then a list of LoadBodyGeneralized objects is returned.
        If the property argument is given, then that property value for each load body generalized is returned in the list
        instead of a LoadBodyGeneralized object

        Parameters
        ----------
        model : Model
            Model to get load body generalizeds from
        flag : Flag
            Flag set on the load body generalizeds that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged load body generalizeds in the model

        Returns
        -------
        list
            List of LoadBodyGeneralized objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the LoadBodyGeneralized object for a load body generalized ID

        Parameters
        ----------
        model : Model
            Model to find the load body generalized in
        number : integer
            number of the load body generalized you want the LoadBodyGeneralized object for

        Returns
        -------
        LoadBodyGeneralized
            LoadBodyGeneralized object (or None if load body generalized does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last load body generalized in the model

        Parameters
        ----------
        model : Model
            Model to get last load body generalized in

        Returns
        -------
        LoadBodyGeneralized
            LoadBodyGeneralized object (or None if there are no load body generalizeds in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a load body generalized

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only load body generalizeds from that model can be picked.
            If the argument is a Flag then only load body generalizeds that
            are flagged with limit can be selected.
            If omitted, or None, any load body generalizeds from any model can be selected.
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
        LoadBodyGeneralized
            LoadBodyGeneralized object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def Select(flag, prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg):
        """
        Allows the user to select load body generalizeds using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting load body generalizeds
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only load body generalizeds from that model can be selected.
            If the argument is a Flag then only load body generalizeds that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any load body generalizeds can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of load body generalizeds selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged load body generalizeds in the model. The load body generalizeds will be sketched until you either call
        LoadBodyGeneralized.Unsketch(),
        LoadBodyGeneralized.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged load body generalizeds will be sketched in
        flag : Flag
            Flag set on the load body generalizeds that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the load body generalizeds are sketched.
            If omitted redraw is true. If you want to sketch flagged load body generalizeds several times and only
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
        Returns the total number of load body generalizeds in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing load body generalizeds should be counted. If false or omitted
            referenced but undefined load body generalizeds will also be included in the total

        Returns
        -------
        int
            number of load body generalizeds
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnblankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the load body generalizeds in the model

        Parameters
        ----------
        model : Model
            Model that all load body generalizeds will be unblanked in
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
        Unblanks all of the flagged load body generalizeds in the model

        Parameters
        ----------
        model : Model
            Model that the flagged load body generalizeds will be unblanked in
        flag : Flag
            Flag set on the load body generalizeds that you want to unblank
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
        Unsets a defined flag on all of the load body generalizeds in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all load body generalizeds will be unset in
        flag : Flag
            Flag to unset on the load body generalizeds

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all load body generalizeds

        Parameters
        ----------
        model : Model
            Model that all load body generalizeds will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the load body generalizeds are unsketched.
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
        Unsketches all flagged load body generalizeds in the model

        Parameters
        ----------
        model : Model
            Model that all load body generalizeds will be unsketched in
        flag : Flag
            Flag set on the load body generalizeds that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the load body generalizeds are unsketched.
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
        Associates a comment with a load body generalized

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the load body generalized

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def Blank(self):
        """
        Blanks the load body generalized

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank")

    def Blanked(self):
        """
        Checks if the load body generalized is blanked or not

        Returns
        -------
        bool
            True if blanked, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blanked")

    def ClearFlag(self, flag):
        """
        Clears a flag on the load body generalized

        Parameters
        ----------
        flag : Flag
            Flag to clear on the load body generalized

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the load body generalized. The target include of the copied load body generalized can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        LoadBodyGeneralized
            LoadBodyGeneralized object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a load body generalized

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the load body generalized

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "DetachComment", comment)

    def Flagged(self, flag):
        """
        Checks if the load body generalized is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the load body generalized

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a load body generalized

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a LoadBodyGeneralized property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the LoadBodyGeneralized.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            load body generalized property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this load body generalized (\*LOAD_NODE_xxxx).
        Note that a carriage return is not added.
        See also LoadBodyGeneralized.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the load body generalized.
        Note that a carriage return is not added.
        See also LoadBodyGeneralized.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next load body generalized in the model

        Returns
        -------
        LoadBodyGeneralized
            LoadBodyGeneralized object (or None if there are no more load body generalizeds in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous load body generalized in the model

        Returns
        -------
        LoadBodyGeneralized
            LoadBodyGeneralized object (or None if there are no more load body generalizeds in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on the load body generalized

        Parameters
        ----------
        flag : Flag
            Flag to set on the load body generalized

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the load body generalized. The load body generalized will be sketched until you either call
        LoadBodyGeneralized.Unsketch(),
        LoadBodyGeneralized.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the load body generalized is sketched.
            If omitted redraw is true. If you want to sketch several load body generalizeds and only
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
        Unblanks the load body generalized

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank")

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the load body generalized

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the load body generalized is unsketched.
            If omitted redraw is true. If you want to unsketch several load body generalizeds and only
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
        LoadBodyGeneralized
            LoadBodyGeneralized object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this load body generalized

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

