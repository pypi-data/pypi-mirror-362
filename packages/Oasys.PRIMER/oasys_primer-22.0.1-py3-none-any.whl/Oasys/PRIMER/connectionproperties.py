import Oasys.gRPC


# Metaclass for static properties and constants
class ConnectionPropertiesType(type):

    def __getattr__(cls, name):

        raise AttributeError("ConnectionProperties class attribute '{}' does not exist".format(name))


class ConnectionProperties(Oasys.gRPC.OasysItem, metaclass=ConnectionPropertiesType):
    _props = {'add', 'areaeq', 'con_id', 'd_dg_pr', 'd_dg_prf', 'd_etan', 'd_etanf', 'd_exsb', 'd_exsbf', 'd_exsn', 'd_exsnf', 'd_exss', 'd_exssf', 'd_gfad', 'd_gfadf', 'd_lcsb', 'd_lcsn', 'd_lcss', 'd_rank', 'd_sb', 'd_sbf', 'd_sclmrr', 'd_sigy', 'd_sigyf', 'd_sn', 'd_snf', 'd_ss', 'd_ssf', 'dg_typ', 'heading', 'include', 'moarfl', 'proprul'}
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
        if name in ConnectionProperties._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in ConnectionProperties._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("ConnectionProperties instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in ConnectionProperties._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in ConnectionProperties._rprops:
            raise AttributeError("Cannot set read-only ConnectionProperties instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, con_id, heading=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, con_id, heading)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new  \*DEFINE_CONNECTION_PROPERTIES object

        Parameters
        ----------
        model : Model
            Model that \*DEFINE_CONNECTION_PROPERTIES will be created in
        con_id : integer
            \*DEFINE_CONNECTION_PROPERTIES id
        heading : string
            Optional. Title for the \*DEFINE_CONNECTION_PROPERTIES

        Returns
        -------
        ConnectionProperties
            ConnectionProperties object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def Create(model, modal=Oasys.gRPC.defaultArg):
        """
        Starts an interactive editing panel to create a \*DEFINE_CONNECTION_PROPERTIES

        Parameters
        ----------
        model : Model
            Model that the \*DEFINE_CONNECTION_PROPERTIES will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        ConnectionProperties
            ConnectionProperties object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def First(model):
        """
        Returns the first \*DEFINE_CONNECTION_PROPERTIES in the model

        Parameters
        ----------
        model : Model
            Model to get first \*DEFINE_CONNECTION_PROPERTIES in

        Returns
        -------
        ConnectionProperties
            ConnectionProperties object (or None if there are no \*DEFINE_CONNECTION_PROPERTIESs in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FirstFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the first free \*DEFINE_CONNECTION_PROPERTIES label in the model.
        Also see ConnectionProperties.LastFreeLabel(),
        ConnectionProperties.NextFreeLabel() and
        Model.FirstFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get first free \*DEFINE_CONNECTION_PROPERTIES label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            First free in layer in editing panels). If omitted the whole model will be used (Equivalent to
            First free in editing panels)

        Returns
        -------
        int
            ConnectionProperties label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FirstFreeLabel", model, layer)

    def FlagAll(model, flag):
        """
        Flags all of the \*DEFINE_CONNECTION_PROPERTIESs in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all \*DEFINE_CONNECTION_PROPERTIESs will be flagged in
        flag : Flag
            Flag to set on the \*DEFINE_CONNECTION_PROPERTIESs

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of ConnectionProperties objects or properties for all of the \*DEFINE_CONNECTION_PROPERTIESs in a model in PRIMER.
        If the optional property argument is not given then a list of ConnectionProperties objects is returned.
        If the property argument is given, that property value for each \*DEFINE_CONNECTION_PROPERTIES is returned in the list
        instead of a ConnectionProperties object

        Parameters
        ----------
        model : Model
            Model to get \*DEFINE_CONNECTION_PROPERTIESs from
        property : string
            Optional. Name for property to get for all \*DEFINE_CONNECTION_PROPERTIESs in the model

        Returns
        -------
        list
            List of ConnectionProperties objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of ConnectionProperties objects for all of the flagged \*DEFINE_CONNECTION_PROPERTIESs in a model in PRIMER
        If the optional property argument is not given then a list of ConnectionProperties objects is returned.
        If the property argument is given, then that property value for each \*DEFINE_CONNECTION_PROPERTIES is returned in the list
        instead of a ConnectionProperties object

        Parameters
        ----------
        model : Model
            Model to get \*DEFINE_CONNECTION_PROPERTIESs from
        flag : Flag
            Flag set on the \*DEFINE_CONNECTION_PROPERTIESs that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged \*DEFINE_CONNECTION_PROPERTIESs in the model

        Returns
        -------
        list
            List of ConnectionProperties objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the ConnectionProperties object for a \*DEFINE_CONNECTION_PROPERTIES ID

        Parameters
        ----------
        model : Model
            Model to find the \*DEFINE_CONNECTION_PROPERTIES in
        number : integer
            number of the \*DEFINE_CONNECTION_PROPERTIES you want the ConnectionProperties object for

        Returns
        -------
        ConnectionProperties
            ConnectionProperties object (or None if \*DEFINE_CONNECTION_PROPERTIES does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last \*DEFINE_CONNECTION_PROPERTIES in the model

        Parameters
        ----------
        model : Model
            Model to get last \*DEFINE_CONNECTION_PROPERTIES in

        Returns
        -------
        ConnectionProperties
            ConnectionProperties object (or None if there are no \*DEFINE_CONNECTION_PROPERTIESs in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def LastFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the last free \*DEFINE_CONNECTION_PROPERTIES label in the model.
        Also see ConnectionProperties.FirstFreeLabel(),
        ConnectionProperties.NextFreeLabel() and
        see Model.LastFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get last free \*DEFINE_CONNECTION_PROPERTIES label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest free in layer in editing panels). If omitted the whole model will be used

        Returns
        -------
        int
            ConnectionProperties label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "LastFreeLabel", model, layer)

    def NextFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the next free (highest+1) \*DEFINE_CONNECTION_PROPERTIES label in the model.
        Also see ConnectionProperties.FirstFreeLabel(),
        ConnectionProperties.LastFreeLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get next free \*DEFINE_CONNECTION_PROPERTIES label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest+1 in layer in editing panels). If omitted the whole model will be used (Equivalent to
            Highest+1 in editing panels)

        Returns
        -------
        int
            ConnectionProperties label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NextFreeLabel", model, layer)

    def RenumberAll(model, start):
        """
        Renumbers all of the \*DEFINE_CONNECTION_PROPERTIESs in the model

        Parameters
        ----------
        model : Model
            Model that all \*DEFINE_CONNECTION_PROPERTIESs will be renumbered in
        start : integer
            Start point for renumbering

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "RenumberAll", model, start)

    def RenumberFlagged(model, flag, start):
        """
        Renumbers all of the flagged \*DEFINE_CONNECTION_PROPERTIESs in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged \*DEFINE_CONNECTION_PROPERTIESs will be renumbered in
        flag : Flag
            Flag set on the \*DEFINE_CONNECTION_PROPERTIESs that you want to renumber
        start : integer
            Start point for renumbering

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "RenumberFlagged", model, flag, start)

    def Select(flag, prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg):
        """
        Allows the user to select \*DEFINE_CONNECTION_PROPERTIESs using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting \*DEFINE_CONNECTION_PROPERTIESs
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only \*DEFINE_CONNECTION_PROPERTIESs from that model can be selected.
            If the argument is a Flag then only \*DEFINE_CONNECTION_PROPERTIESs that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any \*DEFINE_CONNECTION_PROPERTIESs can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of \*DEFINE_CONNECTION_PROPERTIESs selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def Total(model, exists=Oasys.gRPC.defaultArg):
        """
        Returns the total number of \*DEFINE_CONNECTION_PROPERTIESs in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing \*DEFINE_CONNECTION_PROPERTIESs should be counted. If false or omitted
            referenced but undefined \*DEFINE_CONNECTION_PROPERTIESs will also be included in the total

        Returns
        -------
        int
            number of \*DEFINE_CONNECTION_PROPERTIESs
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the \*DEFINE_CONNECTION_PROPERTIESs in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all \*DEFINE_CONNECTION_PROPERTIESs will be unset in
        flag : Flag
            Flag to unset on the \*DEFINE_CONNECTION_PROPERTIESs

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)



# Instance methods
    def AddMaterialDataLine(self):
        """
        Allows user to add material data line in \*DEFINE_CONNECTION_PROPERTIES

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AddMaterialDataLine")

    def AssociateComment(self, comment):
        """
        Associates a comment with a \*DEFINE_CONNECTION_PROPERTIES

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the \*DEFINE_CONNECTION_PROPERTIES

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
        Clears a flag on the \*DEFINE_CONNECTION_PROPERTIES

        Parameters
        ----------
        flag : Flag
            Flag to clear on the \*DEFINE_CONNECTION_PROPERTIES

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the \*DEFINE_CONNECTION_PROPERTIES. The target include of the copied \*DEFINE_CONNECTION_PROPERTIES can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        ConnectionProperties
            ConnectionProperties object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a \*DEFINE_CONNECTION_PROPERTIES

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the \*DEFINE_CONNECTION_PROPERTIES

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
        Checks if the \*DEFINE_CONNECTION_PROPERTIES is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the \*DEFINE_CONNECTION_PROPERTIES

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a \*DEFINE_CONNECTION_PROPERTIES

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetMaterialDataLine(self, row):
        """
        Returns the material data at given row in \*DEFINE_CONNECTION_PROPERTIES

        Parameters
        ----------
        row : integer
            Material data row number, eg. for first material data, row = 0

        Returns
        -------
        int
            List of numbers containing the material id, sigy, e_tan etc.
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetMaterialDataLine", row)

    def GetParameter(self, prop):
        """
        Checks if a ConnectionProperties property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the ConnectionProperties.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            \*DEFINE_CONNECTION_PROPERTIES property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this \*DEFINE_CONNECTION_PROPERTIES
        Note that a carriage return is not added.
        See also ConnectionProperties.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the \*DEFINE_CONNECTION_PROPERTIES.
        Note that a carriage return is not added.
        See also ConnectionProperties.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next \*DEFINE_CONNECTION_PROPERTIES in the model

        Returns
        -------
        ConnectionProperties
            ConnectionProperties object (or None if there are no more \*DEFINE_CONNECTION_PROPERTIESs in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous \*DEFINE_CONNECTION_PROPERTIES in the model

        Returns
        -------
        ConnectionProperties
            ConnectionProperties object (or None if there are no more \*DEFINE_CONNECTION_PROPERTIESs in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def RemoveMaterialDataLine(self, row):
        """
        Allows user to remove material data line in \*DEFINE_CONNECTION_PROPERTIES

        Parameters
        ----------
        row : integer
            Material data row number, eg. for first material data, row = 0

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "RemoveMaterialDataLine", row)

    def SetFlag(self, flag):
        """
        Sets a flag on the \*DEFINE_CONNECTION_PROPERTIES

        Parameters
        ----------
        flag : Flag
            Flag to set on the \*DEFINE_CONNECTION_PROPERTIES

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def SetMaterialDataLine(self, row, mid, sigy=Oasys.gRPC.defaultArg, etan=Oasys.gRPC.defaultArg, dg_pr=Oasys.gRPC.defaultArg, rank=Oasys.gRPC.defaultArg, sn=Oasys.gRPC.defaultArg, sb=Oasys.gRPC.defaultArg, ss=Oasys.gRPC.defaultArg, exsn=Oasys.gRPC.defaultArg, exsb=Oasys.gRPC.defaultArg, exss=Oasys.gRPC.defaultArg, lcsn=Oasys.gRPC.defaultArg, lcsb=Oasys.gRPC.defaultArg, lcss=Oasys.gRPC.defaultArg, gfad=Oasys.gRPC.defaultArg, sclmrr=Oasys.gRPC.defaultArg):
        """
        Allows user to set fields for material data line at given row in \*DEFINE_CONNECTION_PROPERTIES

        Parameters
        ----------
        row : integer
            Material data row number, eg. for first material data, row = 0
        mid : integer
            Material ID
        sigy : real
            Optional. Default yield stress
        etan : real
            Optional. Default tangent modulus
        dg_pr : real
            Optional. Default damage parameter
        rank : real
            Optional. Default rank value
        sn : real
            Optional. Default normal strength
        sb : real
            Optional. Default bending strength
        ss : real
            Optional. Default shear strength
        exsn : real
            Optional. Default normal stress exponent
        exsb : real
            Optional. Default bending stress exponent
        exss : real
            Optional. Default shear stress exponent
        lcsn : integer
            Optional. Default LC of normal stress scale factor wrt strain rate
        lcsb : integer
            Optional. Default LC of bending stress scale factor wrt strain rate
        lcss : integer
            Optional. Default LC of shear stress scale factor wrt strain rate
        gfad : real
            Optional. Default fading energy
        sclmrr : real
            Optional. Default scaling factor for torsional moment in failure function

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetMaterialDataLine", row, mid, sigy, etan, dg_pr, rank, sn, sb, ss, exsn, exsb, exss, lcsn, lcsb, lcss, gfad, sclmrr)

    def ViewParameters(self):
        """
        Object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. This function temporarily
        changes the behaviour so that if a property is a parameter the parameter name is returned instead.
        This can be used with 'method chaining' (see the example below) to make sure a property argument is correct

        Returns
        -------
        ConnectionProperties
            ConnectionProperties object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this \*DEFINE_CONNECTION_PROPERTIES

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

