import Oasys.gRPC


# Metaclass for static properties and constants
class RigidBodiesType(type):
    _consts = {'PART', 'SET'}

    def __getattr__(cls, name):
        if name in RigidBodiesType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("RigidBodies class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in RigidBodiesType._consts:
            raise AttributeError("Cannot set RigidBodies class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class RigidBodies(Oasys.gRPC.OasysItem, metaclass=RigidBodiesType):
    _props = {'colour', 'iflag', 'include', 'option', 'pidc', 'pidl'}
    _rprops = {'exists', 'label', 'model'}


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
        if name in RigidBodies._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in RigidBodies._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("RigidBodies instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in RigidBodies._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in RigidBodies._rprops:
            raise AttributeError("Cannot set read-only RigidBodies instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, options):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, options)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new RigidBodies object

        Parameters
        ----------
        model : Model
            Model that constrained rigid bodies will be created in
        options : dict
            Options specifying which properties would be used to create the keyword. If optional values are not used, then the default values below will be used

        Returns
        -------
        RigidBodies
            RigidBodies object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def BlankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the rigid body merges in the model

        Parameters
        ----------
        model : Model
            Model that all rigid body merges will be blanked in
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
        Blanks all of the flagged rigid body merges in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged rigid body merges will be blanked in
        flag : Flag
            Flag set on the rigid body merges that you want to blank
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
        Starts an interactive editing panel to create a rigid body merge

        Parameters
        ----------
        model : Model
            Model that the rigid body merge will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        RigidBodies
            RigidBodies object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def First(model):
        """
        Returns the first rigid body merge in the model

        Parameters
        ----------
        model : Model
            Model to get first rigid body merge in

        Returns
        -------
        RigidBodies
            RigidBodies object (or None if there are no rigid body merges in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FlagAll(model, flag):
        """
        Flags all of the rigid body merges in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all rigid body merges will be flagged in
        flag : Flag
            Flag to set on the rigid body merges

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of RigidBodies objects or properties for all of the rigid body merges in a model in PRIMER.
        If the optional property argument is not given then a list of RigidBodies objects is returned.
        If the property argument is given, that property value for each rigid body merge is returned in the list
        instead of a RigidBodies object

        Parameters
        ----------
        model : Model
            Model to get rigid body merges from
        property : string
            Optional. Name for property to get for all rigid body merges in the model

        Returns
        -------
        list
            List of RigidBodies objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of RigidBodies objects for all of the flagged rigid body merges in a model in PRIMER
        If the optional property argument is not given then a list of RigidBodies objects is returned.
        If the property argument is given, then that property value for each rigid body merge is returned in the list
        instead of a RigidBodies object

        Parameters
        ----------
        model : Model
            Model to get rigid body merges from
        flag : Flag
            Flag set on the rigid body merges that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged rigid body merges in the model

        Returns
        -------
        list
            List of RigidBodies objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the RigidBodies object for a rigid body merge ID

        Parameters
        ----------
        model : Model
            Model to find the rigid body merge in
        number : integer
            number of the rigid body merge you want the RigidBodies object for

        Returns
        -------
        RigidBodies
            RigidBodies object (or None if rigid body merge does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last rigid body merge in the model

        Parameters
        ----------
        model : Model
            Model to get last rigid body merge in

        Returns
        -------
        RigidBodies
            RigidBodies object (or None if there are no rigid body merges in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a rigid body merge

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only rigid body merges from that model can be picked.
            If the argument is a Flag then only rigid body merges that
            are flagged with limit can be selected.
            If omitted, or None, any rigid body merges from any model can be selected.
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
        RigidBodies
            RigidBodies object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def Select(flag, prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg):
        """
        Allows the user to select rigid body merges using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting rigid body merges
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only rigid body merges from that model can be selected.
            If the argument is a Flag then only rigid body merges that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any rigid body merges can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of rigid body merges selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged rigid body merges in the model. The rigid body merges will be sketched until you either call
        RigidBodies.Unsketch(),
        RigidBodies.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged rigid body merges will be sketched in
        flag : Flag
            Flag set on the rigid body merges that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the rigid body merges are sketched.
            If omitted redraw is true. If you want to sketch flagged rigid body merges several times and only
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
        Returns the total number of rigid body merges in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing rigid body merges should be counted. If false or omitted
            referenced but undefined rigid body merges will also be included in the total

        Returns
        -------
        int
            number of rigid body merges
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnblankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the rigid body merges in the model

        Parameters
        ----------
        model : Model
            Model that all rigid body merges will be unblanked in
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
        Unblanks all of the flagged rigid body merges in the model

        Parameters
        ----------
        model : Model
            Model that the flagged rigid body merges will be unblanked in
        flag : Flag
            Flag set on the rigid body merges that you want to unblank
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
        Unsets a defined flag on all of the rigid body merges in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all rigid body merges will be unset in
        flag : Flag
            Flag to unset on the rigid body merges

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all rigid body merges

        Parameters
        ----------
        model : Model
            Model that all rigid body merges will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the rigid body merges are unsketched.
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
        Unsketches all flagged rigid body merges in the model

        Parameters
        ----------
        model : Model
            Model that all rigid body merges will be unsketched in
        flag : Flag
            Flag set on the rigid body merges that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the rigid body merges are unsketched.
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
        Associates a comment with a rigid body merge

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the rigid body merge

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def Blank(self):
        """
        Blanks the rigid body merge

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank")

    def Blanked(self):
        """
        Checks if the rigid body merge is blanked or not

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
        Clears a flag on the rigid body merge

        Parameters
        ----------
        flag : Flag
            Flag to clear on the rigid body merge

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the rigid body merge. The target include of the copied rigid body merge can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        RigidBodies
            RigidBodies object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a rigid body merge

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the rigid body merge

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
        Extracts the actual colour used for rigid body merge.
        By default in PRIMER many entities such as elements get their colour automatically from the part that they are in.
        PRIMER cycles through 13 default colours based on the label of the entity. In this case the rigid body merge colour
        property will return the value Colour.PART instead of the actual colour.
        This method will return the actual colour which is used for drawing the rigid body merge

        Returns
        -------
        int
            colour value (integer)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ExtractColour")

    def Flagged(self, flag):
        """
        Checks if the rigid body merge is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the rigid body merge

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a rigid body merge

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a RigidBodies property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the RigidBodies.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            rigid body merge property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this constrained rigid bodies (\*CONSTRAINED_RIGID_BODIES).
        Note that a carriage return is not added.
        See also RigidBodies.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the constrained rigid bodies.
        Note that a carriage return is not added.
        See also RigidBodies.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next rigid body merge in the model

        Returns
        -------
        RigidBodies
            RigidBodies object (or None if there are no more rigid body merges in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous rigid body merge in the model

        Returns
        -------
        RigidBodies
            RigidBodies object (or None if there are no more rigid body merges in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on the rigid body merge

        Parameters
        ----------
        flag : Flag
            Flag to set on the rigid body merge

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the rigid body merge. The rigid body merge will be sketched until you either call
        RigidBodies.Unsketch(),
        RigidBodies.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the rigid body merge is sketched.
            If omitted redraw is true. If you want to sketch several rigid body merges and only
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
        Unblanks the rigid body merge

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank")

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the rigid body merge

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the rigid body merge is unsketched.
            If omitted redraw is true. If you want to unsketch several rigid body merges and only
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
        RigidBodies
            RigidBodies object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this rigid body merge

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

