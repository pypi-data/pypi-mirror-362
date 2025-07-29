import Oasys.gRPC


# Metaclass for static properties and constants
class StagedConstructionPartType(type):
    _consts = {'PART', 'SET'}

    def __getattr__(cls, name):
        if name in StagedConstructionPartType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("StagedConstructionPart class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in StagedConstructionPartType._consts:
            raise AttributeError("Cannot set StagedConstructionPart class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class StagedConstructionPart(Oasys.gRPC.OasysItem, metaclass=StagedConstructionPartType):
    _props = {'id', 'include', 'option', 'stga', 'stgr'}
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
        if name in StagedConstructionPart._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in StagedConstructionPart._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("StagedConstructionPart instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in StagedConstructionPart._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in StagedConstructionPart._rprops:
            raise AttributeError("Cannot set read-only StagedConstructionPart instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, option, id, stga, stgr):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, option, id, stga, stgr)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new StagedConstructionPart object

        Parameters
        ----------
        model : Model
            Model that Define staged construction parts will be created in
        option : constant
            Specify the type of Define staged construction parts. Can be
            StagedConstructionPart.PART or
            StagedConstructionPart.SET)
        id : integer
            Part ID or part set ID
        stga : integer
            Construction stage at which part is added
        stgr : integer
            Construction stage at which part is removed

        Returns
        -------
        StagedConstructionPart
            StagedConstructionPart object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def BlankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the Define staged construction parts in the model

        Parameters
        ----------
        model : Model
            Model that all Define staged construction parts will be blanked in
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
        Blanks all of the flagged Define staged construction parts in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged Define staged construction parts will be blanked in
        flag : Flag
            Flag set on the Define staged construction parts that you want to blank
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
        Starts an interactive editing panel to create a Define staged construction part

        Parameters
        ----------
        model : Model
            Model that the Define staged construction part will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        StagedConstructionPart
            StagedConstructionPart object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def First(model):
        """
        Returns the first Define staged construction part in the model

        Parameters
        ----------
        model : Model
            Model to get first Define staged construction part in

        Returns
        -------
        StagedConstructionPart
            StagedConstructionPart object (or None if there are no Define staged construction parts in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FlagAll(model, flag):
        """
        Flags all of the Define staged construction parts in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all Define staged construction parts will be flagged in
        flag : Flag
            Flag to set on the Define staged construction parts

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of StagedConstructionPart objects or properties for all of the Define staged construction parts in a model in PRIMER.
        If the optional property argument is not given then a list of StagedConstructionPart objects is returned.
        If the property argument is given, that property value for each Define staged construction part is returned in the list
        instead of a StagedConstructionPart object

        Parameters
        ----------
        model : Model
            Model to get Define staged construction parts from
        property : string
            Optional. Name for property to get for all Define staged construction parts in the model

        Returns
        -------
        list
            List of StagedConstructionPart objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of StagedConstructionPart objects for all of the flagged Define staged construction parts in a model in PRIMER
        If the optional property argument is not given then a list of StagedConstructionPart objects is returned.
        If the property argument is given, then that property value for each Define staged construction part is returned in the list
        instead of a StagedConstructionPart object

        Parameters
        ----------
        model : Model
            Model to get Define staged construction parts from
        flag : Flag
            Flag set on the Define staged construction parts that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged Define staged construction parts in the model

        Returns
        -------
        list
            List of StagedConstructionPart objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the StagedConstructionPart object for a Define staged construction part ID

        Parameters
        ----------
        model : Model
            Model to find the Define staged construction part in
        number : integer
            number of the Define staged construction part you want the StagedConstructionPart object for

        Returns
        -------
        StagedConstructionPart
            StagedConstructionPart object (or None if Define staged construction part does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last Define staged construction part in the model

        Parameters
        ----------
        model : Model
            Model to get last Define staged construction part in

        Returns
        -------
        StagedConstructionPart
            StagedConstructionPart object (or None if there are no Define staged construction parts in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a Define staged construction part

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only Define staged construction parts from that model can be picked.
            If the argument is a Flag then only Define staged construction parts that
            are flagged with limit can be selected.
            If omitted, or None, any Define staged construction parts from any model can be selected.
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
        StagedConstructionPart
            StagedConstructionPart object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def Select(flag, prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg):
        """
        Allows the user to select Define staged construction parts using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting Define staged construction parts
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only Define staged construction parts from that model can be selected.
            If the argument is a Flag then only Define staged construction parts that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any Define staged construction parts can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of Define staged construction parts selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged Define staged construction parts in the model. The Define staged construction parts will be sketched until you either call
        StagedConstructionPart.Unsketch(),
        StagedConstructionPart.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged Define staged construction parts will be sketched in
        flag : Flag
            Flag set on the Define staged construction parts that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the Define staged construction parts are sketched.
            If omitted redraw is true. If you want to sketch flagged Define staged construction parts several times and only
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
        Returns the total number of Define staged construction parts in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing Define staged construction parts should be counted. If false or omitted
            referenced but undefined Define staged construction parts will also be included in the total

        Returns
        -------
        int
            number of Define staged construction parts
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnblankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the Define staged construction parts in the model

        Parameters
        ----------
        model : Model
            Model that all Define staged construction parts will be unblanked in
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
        Unblanks all of the flagged Define staged construction parts in the model

        Parameters
        ----------
        model : Model
            Model that the flagged Define staged construction parts will be unblanked in
        flag : Flag
            Flag set on the Define staged construction parts that you want to unblank
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
        Unsets a defined flag on all of the Define staged construction parts in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all Define staged construction parts will be unset in
        flag : Flag
            Flag to unset on the Define staged construction parts

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all Define staged construction parts

        Parameters
        ----------
        model : Model
            Model that all Define staged construction parts will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the Define staged construction parts are unsketched.
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
        Unsketches all flagged Define staged construction parts in the model

        Parameters
        ----------
        model : Model
            Model that all Define staged construction parts will be unsketched in
        flag : Flag
            Flag set on the Define staged construction parts that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the Define staged construction parts are unsketched.
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
        Associates a comment with a Define staged construction part

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the Define staged construction part

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def Blank(self):
        """
        Blanks the Define staged construction part

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank")

    def Blanked(self):
        """
        Checks if the Define staged construction part is blanked or not

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
        Clears a flag on the Define staged construction part

        Parameters
        ----------
        flag : Flag
            Flag to clear on the Define staged construction part

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the Define staged construction part. The target include of the copied Define staged construction part can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        StagedConstructionPart
            StagedConstructionPart object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a Define staged construction part

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the Define staged construction part

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
        Checks if the Define staged construction part is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the Define staged construction part

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a Define staged construction part

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a StagedConstructionPart property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the StagedConstructionPart.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            Define staged construction part property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this Define staged construction parts (\*Define_staged_construction_part).
        Note that a carriage return is not added.
        See also StagedConstructionPart.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the Define staged construction parts.
        Note that a carriage return is not added.
        See also StagedConstructionPart.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next Define staged construction part in the model

        Returns
        -------
        StagedConstructionPart
            StagedConstructionPart object (or None if there are no more Define staged construction parts in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous Define staged construction part in the model

        Returns
        -------
        StagedConstructionPart
            StagedConstructionPart object (or None if there are no more Define staged construction parts in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on the Define staged construction part

        Parameters
        ----------
        flag : Flag
            Flag to set on the Define staged construction part

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the Define staged construction part. The Define staged construction part will be sketched until you either call
        StagedConstructionPart.Unsketch(),
        StagedConstructionPart.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the Define staged construction part is sketched.
            If omitted redraw is true. If you want to sketch several Define staged construction parts and only
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
        Unblanks the Define staged construction part

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank")

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the Define staged construction part

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the Define staged construction part is unsketched.
            If omitted redraw is true. If you want to unsketch several Define staged construction parts and only
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
        StagedConstructionPart
            StagedConstructionPart object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this Define staged construction part

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

