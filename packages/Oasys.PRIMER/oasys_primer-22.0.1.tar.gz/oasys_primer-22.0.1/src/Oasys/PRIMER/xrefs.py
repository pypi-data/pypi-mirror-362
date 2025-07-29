import Oasys.gRPC


# Metaclass for static properties and constants
class XrefsType(type):

    def __getattr__(cls, name):

        raise AttributeError("Xrefs class attribute '{}' does not exist".format(name))


class Xrefs(Oasys.gRPC.OasysItem, metaclass=XrefsType):
    _rprops = {'numtypes', 'total'}


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

# If one of the read only properties we define then get it
        if name in Xrefs._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("Xrefs instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the read only properties we define then error
        if name in Xrefs._rprops:
            raise AttributeError("Cannot set read-only Xrefs instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Instance methods
    def GetItemID(self, type, pos):
        """
        Returns the ID of the item in the reference list

        Parameters
        ----------
        type : string
            The type of the item in the reference list (for a list of types see Appendix I of the
            PRIMER manual)
        pos : integer
            The position in the list for this item. Note that positions start at 0, not 1

        Returns
        -------
        int
            ID of item
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetItemID", type, pos)

    def GetItemType(self, type, pos):
        """
        Returns the type of the item in the reference list. This function is only required
        when trying to look at cross references to \*DEFINE_CURVE items. These items are used in a slightly
        different way in PRIMER (each time a curve is used a 'LOADCURVE REFERENCE' structure is created to
        store things like the units and descriptions of each axis for the curve). If you try to get the cross references
        for a curve all the references will be of type 'LOADCURVE REFERENCE' and numtypes will be 1.
        GetItemID() will correctly return the ID of the item
        from the 'LOADCURVE REFERENCE' structure but
        to get the type of the item this function is required

        Parameters
        ----------
        type : string
            The type of the item in the reference list (for a list of types see Appendix I of the
            PRIMER manual)
        pos : integer
            The position in the list for this item. Note that positions start at 0, not 1

        Returns
        -------
        str
            type of item (String). For every item apart from \*DEFINE_CURVE items this will be the same as the type argument
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetItemType", type, pos)

    def GetTotal(self, type):
        """
        Returns the total number of references of a type

        Parameters
        ----------
        type : string
            The type of the item in the reference list (for a list of types see Appendix I of the
            PRIMER manual)

        Returns
        -------
        int
            Number of refs (integer)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetTotal", type)

    def GetType(self, n):
        """
        Returns the type for an entry in the reference list.
        Note that for a curve all the references will be of type 'LOADCURVE REFERENCE' and
        numtypes will be 1. See
        GetItemType() for more details

        Parameters
        ----------
        n : integer
            The entry in the reference types that you want the type for.
            Note that entries start at 0, not 1

        Returns
        -------
        str
            The type of the item (string)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetType", n)

