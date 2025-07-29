import Oasys.gRPC


# Metaclass for static properties and constants
class ParameterType(type):
    _consts = {'CHARACTER', 'INTEGER', 'LOCAL', 'MUTABLE', 'NOECHO', 'REAL'}

    def __getattr__(cls, name):
        if name in ParameterType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("Parameter class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in ParameterType._consts:
            raise AttributeError("Cannot set Parameter class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class Parameter(Oasys.gRPC.OasysItem, metaclass=ParameterType):
    _props = {'include', 'local', 'model', 'mutable', 'noecho', 'value'}
    _rprops = {'expression', 'name', 'type'}


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
        if name in Parameter._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in Parameter._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("Parameter instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Parameter._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in Parameter._rprops:
            raise AttributeError("Cannot set read-only Parameter instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, name, type, expression, value, suffix=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, name, type, expression, value, suffix)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new Parameter object

        Parameters
        ----------
        model : Model
            Model that parameter will be created in
        name : string
            Parameter name
        type : constant
            Can be Parameter.INTEGER, 
            Parameter.REAL or
            Parameter.CHARACTER
        expression : boolean
            true if \*PARAMETER_EXPRESSION, false otherwise
        value : integer/float/string
            Parameter value. The value will be a string for character parameters or parameter expressions,
            or a number for integer or real parameters
        suffix : constant
            Optional. Keyword suffix
            Can be Parameter.LOCAL for \*PARAMETER_..._LOCAL, 
            Parameter.MUTABLE for \*PARAMETER_..._MUTABLE, or
            Parameter.NOECHO for \*PARAMETER_..._NOECHO.
            These may be bitwise ORed together, ie Parameter.LOCAL | Parameter.MUTABLE | Parameter.NOECHO.
            If omitted the parameter will not be local or mutable

        Returns
        -------
        Parameter
            Parameter object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def AutoReorder(model):
        """
        Auto Reorders all the parameters in the model

        Parameters
        ----------
        model : Model
            Model that contains all parameters that will be re-ordered

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "AutoReorder", model)

    def FlagAll(model, flag):
        """
        Flags all of the parameters in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all parameters will be flagged in
        flag : Flag
            Flag to set on the parameters

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model):
        """
        Returns a list of Parameter objects for all of the parameters in a model in Primer

        Parameters
        ----------
        model : Model
            Model to get parameters from

        Returns
        -------
        list
            List of Parameter objects
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model)

    def GetAllOfName(model):
        """
        Returns a list of Parameter objects for all parameters in a model matching Name. If none are found
        that match it will return None. (Multiple parameters of the same name may exist if they use the _LOCAL or _MUTABLE suffices.
        PRIMER will also store multiple illegal instances of parameter name, using the instance as determined by the
        PARAMETER_DUPLICATION card.)

        Parameters
        ----------
        model : Model
            Model to get parameters from

        Returns
        -------
        list
            List of Parameter objects
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAllOfName", model)

    def GetFromName(model, parameter_name):
        """
        Returns the stored Parameter object for a parameter name.
        WARNING: if more than one parameter Name exists (eg _LOCAL, _MUTABLE) then only the first occurrence is returned.
        To return all parameters matching Name use GetAllOfName() instead

        Parameters
        ----------
        model : Model
            Model to find the parameter in
        parameter_name : string
            name of the parameter you want the Parameter object for

        Returns
        -------
        Parameter
            Parameter object (or None if parameter does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromName", model, parameter_name)

    def SaveAll(model):
        """
        Saves the current status and values of all of the parameters in the model.
        Calling this will also have the effect of turning off re-evaluating and updating of all parameters in the model
        when a parameter value is changed.
        To update several parameters in a model without re-evaluating all the parameters after each one is changed first
        call this, then update all of the parameter values, and then call
        Parameter.UpdateAll to apply the update.
        Parameter.SaveAll must be called before using
        Parameter.UpdateAll

        Parameters
        ----------
        model : Model
            Model that the parameters will be saved in

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "SaveAll", model)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the parameters in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all parameters will be unset in
        flag : Flag
            Flag to unset on the parameters

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UpdateAll(model):
        """
        Updates all of the parameters in the model after saving the state of all parameters using 
        Parameter.SaveAll and modifying the parameter 
        values. As parameter re-evaluation has been suppressed by
        Parameter.SaveAll you should ensure that all parameters
        in the model can be evaluated correctly before calling this to ensure that there are no errors. 
        If any of the parameters cannot be evaluated then the values saved in Parameter.SaveAll
        will be restored, the update will be aborted and an exception thrown.
        Calling this will also have the effect of turning back on re-evaluating and updating of all parameters in the model
        when a parameter value is changed.
        Parameter.SaveAll must be called before this method
        can be used

        Parameters
        ----------
        model : Model
            Model that the parameters will be updated in

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UpdateAll", model)



# Instance methods
    def ClearFlag(self, flag):
        """
        Clears a flag on the parameter

        Parameters
        ----------
        flag : Flag
            Flag to clear on the parameter

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Evaluate(self):
        """
        Evaluates a parameter expression, updating the evaluated value stored in PRIMER and returns the value.
        If the parameter is not an expression then the parameter value will just be returned.
        If evaluating the expression cannot be done because of an error (e.g. dividing by zero) an exception will be thrown

        Returns
        -------
        int
            number (real and integer parameters) or string (character parameters)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Evaluate")

    def Flagged(self, flag):
        """
        Checks if the parameter is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the parameter

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def Keyword(self):
        """
        Returns the keyword for this parameter (\*PARAMETER, \*PARAMETER_EXPRESSION).
        Note that a carriage return is not added.
        See also Parameter.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the parameter.
        Note that a carriage return is not added.
        See also Parameter.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def SetFlag(self, flag):
        """
        Sets a flag on the parameter

        Parameters
        ----------
        flag : Flag
            Flag to set on the parameter

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Xrefs(self):
        """
        Returns the cross references for this parameter

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

