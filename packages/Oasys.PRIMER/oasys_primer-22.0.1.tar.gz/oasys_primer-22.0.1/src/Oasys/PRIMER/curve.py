import Oasys.gRPC


# Metaclass for static properties and constants
class CurveType(type):
    _consts = {'AFTER', 'BEFORE', 'CURVE', 'CURVE_FUNCTION', 'CURVE_SMOOTH', 'FUNCTION', 'TABLE'}

    def __getattr__(cls, name):
        if name in CurveType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("Curve class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in CurveType._consts:
            raise AttributeError("Cannot set Curve class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class Curve(Oasys.gRPC.OasysItem, metaclass=CurveType):
    _props = {'dattyp', 'dist', 'function', 'heading', 'include', 'label', 'lcid', 'lcint', 'ncurves', 'npoints', 'offa', 'offo', 'sfa', 'sfo', 'sidr', 'tend', 'trise', 'tstart', 'type', 'version', 'vmax'}
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
        if name in Curve._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in Curve._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("Curve instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Curve._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in Curve._rprops:
            raise AttributeError("Cannot set read-only Curve instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, options):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, options)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new Curve object

        Parameters
        ----------
        model : Model
            Model that curve will be created in
        options : dict
            Options for creating the curve

        Returns
        -------
        Curve
            Curve object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def Create(model, modal=Oasys.gRPC.defaultArg):
        """
        Starts an interactive editing panel to create a curve

        Parameters
        ----------
        model : Model
            Model that the curve will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        Curve
            Curve object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def CreateTable(model, modal=Oasys.gRPC.defaultArg):
        """
        Starts an interactive editing panel to create a table

        Parameters
        ----------
        model : Model
            Model that the curve will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        Curve
            Curve object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "CreateTable", model, modal)

    def First(model):
        """
        Returns the first curve in the model

        Parameters
        ----------
        model : Model
            Model to get first curve in

        Returns
        -------
        Curve
            Curve object (or None if there are no curves in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FirstFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the first free curve label in the model.
        Also see Curve.LastFreeLabel(),
        Curve.NextFreeLabel() and
        Model.FirstFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get first free curve label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            First free in layer in editing panels). If omitted the whole model will be used (Equivalent to
            First free in editing panels)

        Returns
        -------
        int
            Curve label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FirstFreeLabel", model, layer)

    def FlagAll(model, flag):
        """
        Flags all of the curves in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all curves will be flagged in
        flag : Flag
            Flag to set on the curves

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Curve objects or properties for all of the curves in a model in PRIMER.
        If the optional property argument is not given then a list of Curve objects is returned.
        If the property argument is given, that property value for each curve is returned in the list
        instead of a Curve object

        Parameters
        ----------
        model : Model
            Model to get curves from
        property : string
            Optional. Name for property to get for all curves in the model

        Returns
        -------
        list
            List of Curve objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Curve objects for all of the flagged curves in a model in PRIMER
        If the optional property argument is not given then a list of Curve objects is returned.
        If the property argument is given, then that property value for each curve is returned in the list
        instead of a Curve object

        Parameters
        ----------
        model : Model
            Model to get curves from
        flag : Flag
            Flag set on the curves that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged curves in the model

        Returns
        -------
        list
            List of Curve objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the Curve object for a curve ID

        Parameters
        ----------
        model : Model
            Model to find the curve in
        number : integer
            number of the curve you want the Curve object for

        Returns
        -------
        Curve
            Curve object (or None if curve does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last curve in the model

        Parameters
        ----------
        model : Model
            Model to get last curve in

        Returns
        -------
        Curve
            Curve object (or None if there are no curves in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def LastFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the last free curve label in the model.
        Also see Curve.FirstFreeLabel(),
        Curve.NextFreeLabel() and
        see Model.LastFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get last free curve label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest free in layer in editing panels). If omitted the whole model will be used

        Returns
        -------
        int
            Curve label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "LastFreeLabel", model, layer)

    def NextFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the next free (highest+1) curve label in the model.
        Also see Curve.FirstFreeLabel(),
        Curve.LastFreeLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get next free curve label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest+1 in layer in editing panels). If omitted the whole model will be used (Equivalent to
            Highest+1 in editing panels)

        Returns
        -------
        int
            Curve label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NextFreeLabel", model, layer)

    def RenumberAll(model, start):
        """
        Renumbers all of the curves in the model

        Parameters
        ----------
        model : Model
            Model that all curves will be renumbered in
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
        Renumbers all of the flagged curves in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged curves will be renumbered in
        flag : Flag
            Flag set on the curves that you want to renumber
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
        Allows the user to select curves using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting curves
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only curves from that model can be selected.
            If the argument is a Flag then only curves that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any curves can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of curves selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def Total(model, exists=Oasys.gRPC.defaultArg):
        """
        Returns the total number of curves in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing curves should be counted. If false or omitted
            referenced but undefined curves will also be included in the total

        Returns
        -------
        int
            number of curves
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the curves in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all curves will be unset in
        flag : Flag
            Flag to unset on the curves

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)



# Instance methods
    def AddPoint(self, xvalue, yvalue):
        """
        Adds a point to a load curve

        Parameters
        ----------
        xvalue : real
            The x value of the point
        yvalue : real
            The y value of the point

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AddPoint", xvalue, yvalue)

    def AddTableEntry(self, value, load_curve):
        """
        Adds an entry line to a table

        Parameters
        ----------
        value : real
            The value for for this entry in the table
        load_curve : integer
            The load curve corresponding to the defined value

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AddTableEntry", value, load_curve)

    def AssociateComment(self, comment):
        """
        Associates a comment with a curve

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the curve

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
        Clears a flag on the curve

        Parameters
        ----------
        flag : Flag
            Flag to clear on the curve

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the curve. The target include of the copied curve can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        Curve
            Curve object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a curve

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the curve

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
        Checks if the curve is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the curve

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a curve

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a Curve property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the Curve.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            curve property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def GetPoint(self, row):
        """
        Returns x and y data for a point in a curve

        Parameters
        ----------
        row : integer
            The row point you want the data for. Note that curve points start at 0, not 1

        Returns
        -------
        list
            A list containing the x coordinate and the y coordinate
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetPoint", row)

    def GetTableEntry(self, row):
        """
        Returns the value and curve label for a row in a table

        Parameters
        ----------
        row : integer
            The row point you want the data for. Note that curve points start at 0, not 1

        Returns
        -------
        list
            A list containing the value and the load curve label
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetTableEntry", row)

    def InsertPoint(self, ipt, xvalue, yvalue, position):
        """
        Inserts point values before or after a specified row of data on a load curve

        Parameters
        ----------
        ipt : integer
            The row you want to insert the data before or after.
            Note that the row data starts at 0, not 1
        xvalue : real
            The x value of the point
        yvalue : real
            The y value of the point
        position : integer
            Specify either before or after the selected row. Use 'Curve.BEFORE' for before, and 'Curve.AFTER' for after

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "InsertPoint", ipt, xvalue, yvalue, position)

    def InsertTableEntry(self, ipt, value, lcid, position):
        """
        Inserts a table row before or after a specified row of data on a table

        Parameters
        ----------
        ipt : integer
            The row you want to insert the data before or after.
            Note that the row data starts at 0, not 1
        value : real
            The value of the row
        lcid : integer
            The load curve corresponding to the defined value
        position : integer
            Specify either before or after the selected row. Use 'Curve.BEFORE' for before, and 'Curve.AFTER' for after

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "InsertTableEntry", ipt, value, lcid, position)

    def Keyword(self):
        """
        Returns the keyword for this curve (\*DEFINE_CURVE_xxxx).
        Note that a carriage return is not added.
        See also Curve.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the curve.
        Note that a carriage return is not added.
        See also Curve.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next curve in the model

        Returns
        -------
        Curve
            Curve object (or None if there are no more curves in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous curve in the model

        Returns
        -------
        Curve
            Curve object (or None if there are no more curves in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def RemovePoint(self, row):
        """
        Removes a row of data from a curve

        Parameters
        ----------
        row : integer
            The row point you want to remove. Note that curve points start at 0, not 1

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "RemovePoint", row)

    def RemoveTableEntry(self, ipt):
        """
        Removes the value and loadcurve values for a specified row of data on a load curve

        Parameters
        ----------
        ipt : integer
            The row you want to remove the data for.
            Note that the row data starts at 0, not 1

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "RemoveTableEntry", ipt)

    def SetFlag(self, flag):
        """
        Sets a flag on the curve

        Parameters
        ----------
        flag : Flag
            Flag to set on the curve

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def SetPoint(self, ipt, xvalue, yvalue):
        """
        Sets the x and y values for a specified row of data on a load curve

        Parameters
        ----------
        ipt : integer
            The row you want to set the data for.
            Note that the row data starts at 0, not 1
        xvalue : real
            The x value of the point
        yvalue : real
            The y value of the point

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetPoint", ipt, xvalue, yvalue)

    def SetTableEntry(self, ipt, value, load_curve):
        """
        Sets the value and loadcurve values for a specified row of data on a load curve

        Parameters
        ----------
        ipt : integer
            The row you want to set the data for.
            Note that the row data starts at 0, not 1
        value : real
            The value for for this entry in the table
        load_curve : integer
            The load curve corresponding to the defined value

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetTableEntry", ipt, value, load_curve)

    def ViewParameters(self):
        """
        Object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. This function temporarily
        changes the behaviour so that if a property is a parameter the parameter name is returned instead.
        This can be used with 'method chaining' (see the example below) to make sure a property argument is correct

        Returns
        -------
        Curve
            Curve object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this curve

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

