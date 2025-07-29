import Oasys.gRPC


# Metaclass for static properties and constants
class VelocityGenerationType(type):
    _consts = {'NODE_SET', 'PART', 'PART_SET'}

    def __getattr__(cls, name):
        if name in VelocityGenerationType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("VelocityGeneration class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in VelocityGenerationType._consts:
            raise AttributeError("Cannot set VelocityGeneration class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class VelocityGeneration(Oasys.gRPC.OasysItem, metaclass=VelocityGenerationType):
    _props = {'icid', 'id', 'include', 'irigid', 'ivatn', 'nx', 'ny', 'nz', 'omega', 'phase', 'type', 'vx', 'vy', 'vz', 'xc', 'yc', 'zc'}
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
        if name in VelocityGeneration._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in VelocityGeneration._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("VelocityGeneration instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in VelocityGeneration._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in VelocityGeneration._rprops:
            raise AttributeError("Cannot set read-only VelocityGeneration instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, type, id, omega, vx, vy, vz, ivatn, xc, yc, zc, nx, ny, nz, phase, irigid, icid):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, type, id, omega, vx, vy, vz, ivatn, xc, yc, zc, nx, ny, nz, phase, irigid, icid)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new VelocityGeneration object

        Parameters
        ----------
        model : Model
            Model that velocity will be created in
        type : constant
            Specify the type of Velocity generation (Can be
            VelocityGeneration.PART_SET or
            VelocityGeneration.PART or
            VelocityGeneration.NODE_SET)
        id : integer
            Set Part ID, Part set ID or Node set ID
        omega : float
            Angular velocity about the rotational axis
        vx : float
            Initial translational velocity in X direction
        vy : float
            Initial translational velocity in Y direction
        vz : float
            Initial translational velocity in Z direction
        ivatn : integer
            Tracked parts flag
        xc : float
            x-coordinate on rotational axis
        yc : float
            y-coordinate on rotational axis
        zc : float
            z-coordinate on rotational axis
        nx : float
            x-direction cosine
        ny : float
            y-direction cosine
        nz : float
            z-direction cosine
        phase : integer
            Dynamic relaxation flag
        irigid : integer
            Overide part inertia flag
        icid : integer
            Local coordinate system

        Returns
        -------
        VelocityGeneration
            VelocityGeneration object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def BlankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the initial velocity generations in the model

        Parameters
        ----------
        model : Model
            Model that all initial velocity generations will be blanked in
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
        Blanks all of the flagged initial velocity generations in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged initial velocity generations will be blanked in
        flag : Flag
            Flag set on the initial velocity generations that you want to blank
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
        Starts an interactive editing panel to create a initial velocity generation

        Parameters
        ----------
        model : Model
            Model that the initial velocity generation will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        VelocityGeneration
            VelocityGeneration object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def First(model):
        """
        Returns the first initial velocity generation in the model

        Parameters
        ----------
        model : Model
            Model to get first initial velocity generation in

        Returns
        -------
        VelocityGeneration
            VelocityGeneration object (or None if there are no initial velocity generations in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FlagAll(model, flag):
        """
        Flags all of the initial velocity generations in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all initial velocity generations will be flagged in
        flag : Flag
            Flag to set on the initial velocity generations

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of VelocityGeneration objects or properties for all of the initial velocity generations in a model in PRIMER.
        If the optional property argument is not given then a list of VelocityGeneration objects is returned.
        If the property argument is given, that property value for each initial velocity generation is returned in the list
        instead of a VelocityGeneration object

        Parameters
        ----------
        model : Model
            Model to get initial velocity generations from
        property : string
            Optional. Name for property to get for all initial velocity generations in the model

        Returns
        -------
        list
            List of VelocityGeneration objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of VelocityGeneration objects for all of the flagged initial velocity generations in a model in PRIMER
        If the optional property argument is not given then a list of VelocityGeneration objects is returned.
        If the property argument is given, then that property value for each initial velocity generation is returned in the list
        instead of a VelocityGeneration object

        Parameters
        ----------
        model : Model
            Model to get initial velocity generations from
        flag : Flag
            Flag set on the initial velocity generations that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged initial velocity generations in the model

        Returns
        -------
        list
            List of VelocityGeneration objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the VelocityGeneration object for a initial velocity generation ID

        Parameters
        ----------
        model : Model
            Model to find the initial velocity generation in
        number : integer
            number of the initial velocity generation you want the VelocityGeneration object for

        Returns
        -------
        VelocityGeneration
            VelocityGeneration object (or None if initial velocity generation does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last initial velocity generation in the model

        Parameters
        ----------
        model : Model
            Model to get last initial velocity generation in

        Returns
        -------
        VelocityGeneration
            VelocityGeneration object (or None if there are no initial velocity generations in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a initial velocity generation

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only initial velocity generations from that model can be picked.
            If the argument is a Flag then only initial velocity generations that
            are flagged with limit can be selected.
            If omitted, or None, any initial velocity generations from any model can be selected.
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
        VelocityGeneration
            VelocityGeneration object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def Select(flag, prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg):
        """
        Allows the user to select initial velocity generations using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting initial velocity generations
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only initial velocity generations from that model can be selected.
            If the argument is a Flag then only initial velocity generations that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any initial velocity generations can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of initial velocity generations selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged initial velocity generations in the model. The initial velocity generations will be sketched until you either call
        VelocityGeneration.Unsketch(),
        VelocityGeneration.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged initial velocity generations will be sketched in
        flag : Flag
            Flag set on the initial velocity generations that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the initial velocity generations are sketched.
            If omitted redraw is true. If you want to sketch flagged initial velocity generations several times and only
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
        Returns the total number of initial velocity generations in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing initial velocity generations should be counted. If false or omitted
            referenced but undefined initial velocity generations will also be included in the total

        Returns
        -------
        int
            number of initial velocity generations
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnblankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the initial velocity generations in the model

        Parameters
        ----------
        model : Model
            Model that all initial velocity generations will be unblanked in
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
        Unblanks all of the flagged initial velocity generations in the model

        Parameters
        ----------
        model : Model
            Model that the flagged initial velocity generations will be unblanked in
        flag : Flag
            Flag set on the initial velocity generations that you want to unblank
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
        Unsets a defined flag on all of the initial velocity generations in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all initial velocity generations will be unset in
        flag : Flag
            Flag to unset on the initial velocity generations

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all initial velocity generations

        Parameters
        ----------
        model : Model
            Model that all initial velocity generations will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the initial velocity generations are unsketched.
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
        Unsketches all flagged initial velocity generations in the model

        Parameters
        ----------
        model : Model
            Model that all initial velocity generations will be unsketched in
        flag : Flag
            Flag set on the initial velocity generations that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the initial velocity generations are unsketched.
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
        Associates a comment with a initial velocity generation

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the initial velocity generation

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def Blank(self):
        """
        Blanks the initial velocity generation

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank")

    def Blanked(self):
        """
        Checks if the initial velocity generation is blanked or not

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
        Clears a flag on the initial velocity generation

        Parameters
        ----------
        flag : Flag
            Flag to clear on the initial velocity generation

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the initial velocity generation. The target include of the copied initial velocity generation can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        VelocityGeneration
            VelocityGeneration object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a initial velocity generation

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the initial velocity generation

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
        Checks if the initial velocity generation is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the initial velocity generation

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a initial velocity generation

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a VelocityGeneration property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the VelocityGeneration.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            initial velocity generation property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this initial velocity (\*INITIAL_VELOCITY_GENERATION).
        Note that a carriage return is not added.
        See also VelocityGeneration.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the initial velocity_generation.
        Note that a carriage return is not added.
        See also VelocityGeneration.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next initial velocity generation in the model

        Returns
        -------
        VelocityGeneration
            VelocityGeneration object (or None if there are no more initial velocity generations in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous initial velocity generation in the model

        Returns
        -------
        VelocityGeneration
            VelocityGeneration object (or None if there are no more initial velocity generations in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on the initial velocity generation

        Parameters
        ----------
        flag : Flag
            Flag to set on the initial velocity generation

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the initial velocity generation. The initial velocity generation will be sketched until you either call
        VelocityGeneration.Unsketch(),
        VelocityGeneration.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the initial velocity generation is sketched.
            If omitted redraw is true. If you want to sketch several initial velocity generations and only
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
        Unblanks the initial velocity generation

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank")

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the initial velocity generation

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the initial velocity generation is unsketched.
            If omitted redraw is true. If you want to unsketch several initial velocity generations and only
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
        VelocityGeneration
            VelocityGeneration object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this initial velocity generation

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

