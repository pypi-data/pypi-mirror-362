import Oasys.gRPC


# Metaclass for static properties and constants
class IncludeType(type):
    _consts = {'ABSOLUTE', 'COPY_INTO_CURRENT', 'COPY_INTO_SOURCE', 'ENDOFF', 'IDDOFF', 'IDEOFF', 'IDFOFF', 'IDMOFF', 'IDNOFF', 'IDPOFF', 'IDROFF', 'IDSOFF', 'INDIVIDUAL_GZIP', 'INDIVIDUAL_ZIP', 'KEEP_ORIGINAL', 'MASTER_ONLY', 'MERGE', 'NATIVE', 'NOT_WRITTEN', 'RELATIVE', 'SAME_DIR', 'SELECT', 'SUBDIR', 'UNIX', 'WINDOWS'}

    def __getattr__(cls, name):
        if name in IncludeType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("Include class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in IncludeType._consts:
            raise AttributeError("Cannot set Include class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class Include(Oasys.gRPC.OasysItem, metaclass=IncludeType):
    _props = {'comments', 'fctchg', 'fctlen', 'fctmas', 'fcttem', 'fcttim', 'file', 'genmax', 'genmin', 'incout', 'model', 'n_locked_range', 'name', 'nelmax', 'nelmin', 'parent', 'path', 'suppressed', 'tranid', 'transform'}
    _rprops = {'iddoff', 'ideoff', 'idfoff', 'idmoff', 'idnoff', 'idpoff', 'idroff', 'idsoff', 'label'}


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
        if name in Include._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in Include._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("Include instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Include._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in Include._rprops:
            raise AttributeError("Cannot set read-only Include instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, name, parent=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, name, parent)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new Include object

        Parameters
        ----------
        model : Model
            Model that include will be created in
        name : string
            Include filename
        parent : integer
            Optional. Parent include file number. If omitted parent will be 0 (main file)

        Returns
        -------
        Include
            Include object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def BlankAll(model, redraw=Oasys.gRPC.defaultArg, masterinclude=Oasys.gRPC.defaultArg):
        """
        Blanks all of the includes in the model

        Parameters
        ----------
        model : Model
            Model that all includes will be blanked in
        redraw : boolean
            Optional. If model should be redrawn or not.
            If omitted redraw is false. If you want to do several (un)blanks and only
            redraw after the last one then use false for all redraws apart from the last one.
            Alternatively you can redraw using View.Redraw()
        masterinclude : boolean
            Optional. If masterInclude file should be blanked or not.
            If omitted masterInclude is false. The master file is include file number 0

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "BlankAll", model, redraw, masterinclude)

    def BlankFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the flagged include files in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged includes will be blanked in
        flag : Flag
            Flag set on the includes that you want to blank
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
        Returns the first include file in the model

        Parameters
        ----------
        model : Model
            Model to get first include in

        Returns
        -------
        Include
            Include object (or None if there are no includes in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FlagAll(model, flag, masterinclude=Oasys.gRPC.defaultArg):
        """
        Flags all of the includes in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all includes will be flagged in
        flag : Flag
            Flag to set on the includes
        masterinclude : boolean
            Optional. If masterInclude file should be flagged or not.
            If omitted masterInclude is false. The master file is include file number 0

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag, masterinclude)

    def GetAll(model, masterinclude=Oasys.gRPC.defaultArg):
        """
        Returns a list of Include objects for all of the includes in a model in PRIMER

        Parameters
        ----------
        model : Model
            Model to get includes from
        masterinclude : boolean
            Optional. If masterInclude file should be included or not.
            If omitted masterInclude is false. The master file is include file number 0

        Returns
        -------
        list
            List of Include objects
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, masterinclude)

    def GetFromID(model, include_number):
        """
        Returns the Include object for an include label.
        Note that items that are in the
        main keyword file will have a layer value of 0 which can be used as the
        include number argument to this function to return master include file

        Parameters
        ----------
        model : Model
            Model to find the include in
        include_number : integer
            number of the include you want the Include object for

        Returns
        -------
        Include
            Include object (or None if include does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, include_number)

    def Last(model):
        """
        Returns the last include file in the model

        Parameters
        ----------
        model : Model
            Model to get last include in

        Returns
        -------
        Include
            Include object (or None if there are no includes in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick an include

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only includes from that model can be picked.
            If the argument is a Flag then only includes that
            are flagged with limit can be selected.
            If omitted, or None, any includes from any model can be selected.
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
        Include
            Include object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def Select(flag, prompt, model=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg):
        """
        Allows the user to select includes using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting includes
        prompt : string
            Text to display as a prompt to the user
        model : Model
            Optional. Model to select from
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of items selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, model, modal)

    def Total(model):
        """
        Returns the total number of include files in the model

        Parameters
        ----------
        model : Model
            Model to get include total from

        Returns
        -------
        int
            integer
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model)

    def UnblankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the includes in the model

        Parameters
        ----------
        model : Model
            Model that all includes will be unblanked in
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
        Unblanks all of the flagged include files in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged includes will be unblanked in
        flag : Flag
            Flag set on the includes that you want to unblank
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
        Unsets a defined flag on all of the includes in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all includes will be unset in
        flag : Flag
            Flag to unset on the includes

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)



# Instance methods
    def ClearFlag(self, flag, clear_contents=Oasys.gRPC.defaultArg):
        """
        Clears a flag on the include

        Parameters
        ----------
        flag : Flag
            Flag to clear on the include
        clear_contents : boolean
            Optional. If true then the items in the include file will also have flag cleared. If false (default)
            then the include file contents are not cleared

        Returns
        -------
        int
            Number of item flags cleared
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag, clear_contents)

    def Flagged(self, flag):
        """
        Checks if the include is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the include

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetDetailedRange(self, type_argument):
        """
        Gets detailed min and max label ranges for specified type from the include

        Parameters
        ----------
        type_argument : string
            Entity type for which ranges are returned

        Returns
        -------
        list
            A list containing the min and max label ranges for the specified type or None if no range defined for this type
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetDetailedRange", type_argument)

    def GetLockedLabelData(self, rangenum):
        """
        Returns the locked label data for include files. Also see the n_locked_range property

        Parameters
        ----------
        rangenum : integer
            The range number you want the data for; includes can have multiple ranges. 
            Note that range numbers start at 0, not 1

        Returns
        -------
        list
            A list containing the include name (string can also be "ALL" if range is applicable model-wide), start (min) label (integer), end (max) label (integer), safe range (0 or 1 for False or True), and entity type (string)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetLockedLabelData", rangenum)

    def IsEmpty(self):
        """
        Returns true if include is Empty (contains no INSTALLED static/sort/kid/include items)

        Returns
        -------
        bool
            logical
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "IsEmpty")

    def Keyword(self):
        """
        Returns the keyword for this include (\*INCLUDE, \*INCLUDE_TRANSFORM).
        Note that a carriage return is not added.
        See also Include.KeywordCards().
        This function is not supported for the master include file

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the include.
        Note that a carriage return is not added.
        See also Include.Keyword().
        Also note that this function is not supported for the master include file

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def MakeCurrentLayer(self):
        """
        Sets this include file to be the current layer so that any newly created items
        are put in this include file. Also see the Model.layer property

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "MakeCurrentLayer")

    def Modified(self, listing):
        """
        Returns true if include has been modified

        Parameters
        ----------
        listing : boolean
            false for no listing output, true for listing output

        Returns
        -------
        bool
            logical
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Modified", listing)

    def Next(self):
        """
        Returns the next include in the model.
        Note that this function is not supported for the master include file

        Returns
        -------
        Include
            Include object (or None if there are no more includes in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous include in the model.
        Note that this function is not supported for the master include file

        Returns
        -------
        Include
            Include object (or None if there are no more includes in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def RemoveLockedLabelData(self, rangenum):
        """
        Removes the locked label data for a range in include files. Also see the n_locked_range property

        Parameters
        ----------
        rangenum : integer
            The locked label range you want to remove.
            Note that range numbers start at 0, not 1

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "RemoveLockedLabelData", rangenum)

    def SetDetailedRange(self, type_argument, min_label, max_label):
        """
        Sets detailed min and max label ranges for specified type on the include

        Parameters
        ----------
        type_argument : string
            Entity type for which ranges are to be defined
        min_label : integer
            Defines the smallest label for entities of this type
        max_label : integer
            Defines the largest label for entities of this type

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetDetailedRange", type_argument, min_label, max_label)

    def SetFlag(self, flag, flag_contents=Oasys.gRPC.defaultArg):
        """
        Sets a flag on the include

        Parameters
        ----------
        flag : Flag
            Flag to set on the include
        flag_contents : boolean
            Optional. If true then the items in the include file will also be flagged. If false (default)
            then the include file contents are not flagged

        Returns
        -------
        int
            Number of items flagged
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag, flag_contents)

    def SetLockedLabelData(self, rangenum, min, max, type, safe=Oasys.gRPC.defaultArg, all_includes=Oasys.gRPC.defaultArg):
        """
        Sets the locked label data for a particular range for an include file. Also see the n_locked_range property

        Parameters
        ----------
        rangenum : integer
            The range you want to set the data for.
            Note that range numbers start at 0, not 1
        min : integer
            Start (min) label for a locked range
        max : integer
            End (max) label for a locked range
        type : string
            Entity type code - "NODE", "SHELL" etc. Can also be "ALL" 
            (for a list of types see Appendix I of the PRIMER manual)
        safe : boolean
            Optional. Determines whether a locked range is safe (protected)
        all_includes : boolean
            Optional. Specified range will be set model-wide (all includes). 
            Only useful when working with the 'master' include

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetLockedLabelData", rangenum, min, max, type, safe, all_includes)

    def SetTransformOffset(self, offset, value, check_only=Oasys.gRPC.defaultArg):
        """
        Sets offset values for include transform. This function is required to change the offset values
        rather than changing the properties directly so that the include can be checked to ensure
        that the new value does not cause any label clashes with existing items or any negative labels
        when the transform is unapplied when writing the include. Note that this function is not supported for the master include file

        Parameters
        ----------
        offset : constant
            The include transform offset type to change. Can be
            Include.IDNOFF,
            Include.IDEOFF,
            Include.IDPOFF,
            Include.IDMOFF,
            Include.IDSOFF,
            Include.IDFOFF,
            Include.IDDOFF or
            Include.IDROFF
        value : integer
            The value to change the offset to
        check_only : boolean
            Optional. Sometimes it may be necessary to check if changing an offset for an include will cause
            an error or label clash rather than actually changing it. If check only is true then
            PRIMER will just check to see if the new value for the offset will cause any label clashes
            or negative labels and not change the offset value or any item labels. If false or omitted
            then the offset and labels will be updated if there are no errors

        Returns
        -------
        bool
            logical, True if change successful. False if the change would cause a clash of labels or negative labels, in which case the value is not changed
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetTransformOffset", offset, value, check_only)

    def Write(self, filename, options=Oasys.gRPC.defaultArg):
        """
        Writes an include file. Note that this function is not supported for the master include file

        Parameters
        ----------
        filename : string
            Filename of the Ansys LS-DYNA keyword file you want to write
        options : dict
            Optional. Options specifying how the file should be written out. If omitted the default values below will be used.
            The properties available are:

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Write", filename, options)

