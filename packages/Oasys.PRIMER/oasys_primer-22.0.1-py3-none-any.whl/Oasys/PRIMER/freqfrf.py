import Oasys.gRPC


# Metaclass for static properties and constants
class FreqFRFType(type):
    _consts = {'BLANK', 'IGA_EDGE_UVW', 'IGA_EDGE_UVW_SET', 'IGA_FACE_XYZ', 'IGA_FACE_XYZ_SET', 'IGA_POINT_UVW', 'IGA_POINT_UVW_SET', 'NODE', 'NODE_SET', 'SEGMENT_SET', 'SUBCASE'}

    def __getattr__(cls, name):
        if name in FreqFRFType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("FreqFRF class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in FreqFRFType._consts:
            raise AttributeError("Cannot set FreqFRF class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class FreqFRF(Oasys.gRPC.OasysItem, metaclass=FreqFRFType):
    _props = {'dampf', 'dmpmas', 'dmpstf', 'dof1', 'dof2', 'fmax', 'fmin', 'fnmax', 'fspace', 'include', 'lcdam', 'lcfreq', 'lctyp', 'mdmax', 'mdmin', 'n1', 'n11', 'n11typ', 'n1typ', 'n2', 'n2typ', 'ncases', 'nfreq', 'option', 'output', 'relatv', 'restrt', 'vad1', 'vad2', 'vid1', 'vid2'}
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
        if name in FreqFRF._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in FreqFRF._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("FreqFRF instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in FreqFRF._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in FreqFRF._rprops:
            raise AttributeError("Cannot set read-only FreqFRF instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self , model, *pargs, **kargs):
# Current constructor
        if len(pargs)==0 and len(kargs)==1:
            handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__ , model , kargs['option'])
        elif len(pargs)==1 and len(kargs)==0:
            handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__ , model , pargs[0])
# Must be deprecated constructor
        else:
            args = {
              'n1': Oasys.gRPC.missingArg,
              'n1typ': Oasys.gRPC.missingArg,
              'n2': Oasys.gRPC.missingArg,
              'n2typ': Oasys.gRPC.missingArg
            }
            if len(pargs) >= 1:
                args['n1'] = pargs[0]
            if len(pargs) >= 2:
                args['n1typ'] = pargs[1]
            if len(pargs) >= 3:
                args['n2'] = pargs[2]
            if len(pargs) >= 4:
                args['n2typ'] = pargs[3]
            for k in kargs:
                args[k] = kargs[k]
            for a in args:
                if args[a] == Oasys.gRPC.missingArg:
                    raise AttributeError("Argument {} missing in FreqFRF constructor".format(a))
            handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__ , model , args['n1'], args['n1typ'], args['n2'], args['n2typ'])

        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def First(model):
        """
        Returns the first \*FREQUENCY_DOMAIN_FRF in the model

        Parameters
        ----------
        model : Model
            Model to get first \*FREQUENCY_DOMAIN_FRF in

        Returns
        -------
        FreqFRF
            FreqFRF object (or None if there are no \*FREQUENCY_DOMAIN_FRFs in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FlagAll(model, flag):
        """
        Flags all of the \*FREQUENCY_DOMAIN_FRFs in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all \*FREQUENCY_DOMAIN_FRFs will be flagged in
        flag : Flag
            Flag to set on the \*FREQUENCY_DOMAIN_FRFs

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of FreqFRF objects or properties for all of the \*FREQUENCY_DOMAIN_FRFs in a model in PRIMER.
        If the optional property argument is not given then a list of FreqFRF objects is returned.
        If the property argument is given, that property value for each \*FREQUENCY_DOMAIN_FRF is returned in the list
        instead of a FreqFRF object

        Parameters
        ----------
        model : Model
            Model to get \*FREQUENCY_DOMAIN_FRFs from
        property : string
            Optional. Name for property to get for all \*FREQUENCY_DOMAIN_FRFs in the model

        Returns
        -------
        list
            List of FreqFRF objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of FreqFRF objects for all of the flagged \*FREQUENCY_DOMAIN_FRFs in a model in PRIMER
        If the optional property argument is not given then a list of FreqFRF objects is returned.
        If the property argument is given, then that property value for each \*FREQUENCY_DOMAIN_FRF is returned in the list
        instead of a FreqFRF object

        Parameters
        ----------
        model : Model
            Model to get \*FREQUENCY_DOMAIN_FRFs from
        flag : Flag
            Flag set on the \*FREQUENCY_DOMAIN_FRFs that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged \*FREQUENCY_DOMAIN_FRFs in the model

        Returns
        -------
        list
            List of FreqFRF objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the FreqFRF object for a \*FREQUENCY_DOMAIN_FRF ID

        Parameters
        ----------
        model : Model
            Model to find the \*FREQUENCY_DOMAIN_FRF in
        number : integer
            number of the \*FREQUENCY_DOMAIN_FRF you want the FreqFRF object for

        Returns
        -------
        FreqFRF
            FreqFRF object (or None if \*FREQUENCY_DOMAIN_FRF does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last \*FREQUENCY_DOMAIN_FRF in the model

        Parameters
        ----------
        model : Model
            Model to get last \*FREQUENCY_DOMAIN_FRF in

        Returns
        -------
        FreqFRF
            FreqFRF object (or None if there are no \*FREQUENCY_DOMAIN_FRFs in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def Select(flag, prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg):
        """
        Allows the user to select \*FREQUENCY_DOMAIN_FRFs using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting \*FREQUENCY_DOMAIN_FRFs
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only \*FREQUENCY_DOMAIN_FRFs from that model can be selected.
            If the argument is a Flag then only \*FREQUENCY_DOMAIN_FRFs that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any \*FREQUENCY_DOMAIN_FRFs can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of \*FREQUENCY_DOMAIN_FRFs selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def Total(model, exists=Oasys.gRPC.defaultArg):
        """
        Returns the total number of \*FREQUENCY_DOMAIN_FRFs in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing \*FREQUENCY_DOMAIN_FRFs should be counted. If false or omitted
            referenced but undefined \*FREQUENCY_DOMAIN_FRFs will also be included in the total

        Returns
        -------
        int
            number of \*FREQUENCY_DOMAIN_FRFs
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the \*FREQUENCY_DOMAIN_FRFs in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all \*FREQUENCY_DOMAIN_FRFs will be unset in
        flag : Flag
            Flag to unset on the \*FREQUENCY_DOMAIN_FRFs

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)



# Instance methods
    def AddSubcaseData(self):
        """
        Allows user to add new subcase cards in \*FREQUENCY_DOMAIN_SSFRF. This method is only applicable when option is
        FreqFRF.SUBCASE.
        The new cards have uninitialised fields and should be updated by
        FreqFRF.SetSubcaseData().

        Returns
        -------
        integer
            Index of the new subcase
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AddSubcaseData")

    def AssociateComment(self, comment):
        """
        Associates a comment with a \*FREQUENCY_DOMAIN_FRF

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the \*FREQUENCY_DOMAIN_FRF

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
        Clears a flag on the \*FREQUENCY_DOMAIN_FRF

        Parameters
        ----------
        flag : Flag
            Flag to clear on the \*FREQUENCY_DOMAIN_FRF

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the \*FREQUENCY_DOMAIN_FRF. The target include of the copied \*FREQUENCY_DOMAIN_FRF can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        FreqFRF
            FreqFRF object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a \*FREQUENCY_DOMAIN_FRF

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the \*FREQUENCY_DOMAIN_FRF

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
        Checks if the \*FREQUENCY_DOMAIN_FRF is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the \*FREQUENCY_DOMAIN_FRF

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a \*FREQUENCY_DOMAIN_FRF

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a FreqFRF property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the FreqFRF.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            \*FREQUENCY_DOMAIN_FRF property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def GetSubcaseData(self, index):
        """
        Returns the data for a specific subcase as a list. For each subcase there will be 13
        values when vad1=12 else 11 values . There can be as many subcases as needed. 
        This method is only applicable when option is
        FreqFRF.SUBCASE.

        Parameters
        ----------
        index : integer
            Index you want the subcase data for. Note that indices start at 0

        Returns
        -------
        int
            An list containing the subcase data (values: title[string], n1[integer], n1typ[integer], n1typ[integer], dof1[integer], vad1[integer], vid1[integer], n2[integer], n2typ[integer],dof2[integer], vad2[integer], vid2[integer], n11[integer], n11typ[integer])  n11 and n11typ are present only when vad1 =12
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetSubcaseData", index)

    def Keyword(self):
        """
        Returns the keyword for this \*FREQUENCY_DOMAIN_FRF
        Note that a carriage return is not added.
        See also FreqFRF.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the \*FREQUENCY_DOMAIN_FRF.
        Note that a carriage return is not added.
        See also FreqFRF.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next \*FREQUENCY_DOMAIN_FRF in the model

        Returns
        -------
        FreqFRF
            FreqFRF object (or None if there are no more \*FREQUENCY_DOMAIN_FRFs in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous \*FREQUENCY_DOMAIN_FRF in the model

        Returns
        -------
        FreqFRF
            FreqFRF object (or None if there are no more \*FREQUENCY_DOMAIN_FRFs in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on the \*FREQUENCY_DOMAIN_FRF

        Parameters
        ----------
        flag : Flag
            Flag to set on the \*FREQUENCY_DOMAIN_FRF

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def SetSubcaseData(self, index, title, vad1, data):
        """
        Set the data for a specific subcase.
        There can be as many subcases as needed. This method is only applicable when option is
        FreqFRF.SUBCASE.

        Parameters
        ----------
        index : integer
            Index you want to set subcase data for. Note that indices start at 0
        title : string
            A description of the current subcase (can be blank)
        vad1 : integer
            Value of vad1
        data : List of data
            An list containing the subcase data (values: n1[integer],
            n1typ[integer], dof1[integer], vad1[integer], vid1[integer], n2[integer], n2typ[integer], dof2[integer], 
            vad2[integer], vid2[integer]) 
            For vad1=12 Extra 2 arguments to be given n1[integer], n11typ[integer]

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetSubcaseData", index, title, vad1, data)

    def ViewParameters(self):
        """
        Object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. This function temporarily
        changes the behaviour so that if a property is a parameter the parameter name is returned instead.
        This can be used with 'method chaining' (see the example below) to make sure a property argument is correct

        Returns
        -------
        FreqFRF
            FreqFRF object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this \*FREQUENCY_DOMAIN_FRF

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

