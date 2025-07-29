import Oasys.gRPC


# Metaclass for static properties and constants
class ViewType(type):
    _consts = {'ABSOLUTE', 'ADDEDMASS', 'ADDEDMASSPART', 'AREA', 'ASPECTRATIO', 'CONTOUR', 'DENSITY', 'ELEMPROPS', 'ELEMQUAL', 'EMPFINALMASS', 'EMPNSMASS', 'EMPSTRUCTMASS', 'FAILEDCRITERIA', 'FINALMASS', 'FORM', 'FORMULATION', 'INITVELRES', 'INITVELS', 'INITVELX', 'INITVELY', 'INITVELZ', 'INTPOINT', 'INTPOINTS', 'ISO', 'JACOBIAN', 'LOADSHELLDIRECTION', 'MASSSCALE', 'MATERIALNUMBER', 'MATLPROPS', 'MAXINTANGLE', 'MAXSTRAIN', 'MININTANGLE', 'MINLENGTH', 'MINSTRAIN', 'PARAMETRICCOORD', 'PARTMASS', 'PERCENTADDEDMASS', 'PERCENTADDEDMASSPART', 'PLASTICSTRAIN', 'POISSONRATIO', 'QUALIMPERF', 'REMAINING', 'SHELLNORMALS', 'SHELLTHICKNESS', 'SKEW', 'STRUCTMASS', 'TAPER', 'TETCOLLAPSE', 'THINNING', 'TIMESTEP', 'UP_AUTOMATIC', 'UP_X', 'UP_Y', 'UP_Z', 'VECTOR', 'VOLUME', 'WARPAGE', 'XY', 'XZ', 'YIELDSTRESS', 'YOUNGMODULUS', 'YZ'}

    def __getattr__(cls, name):
        if name in ViewType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("View class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in ViewType._consts:
            raise AttributeError("Cannot set View class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class View(Oasys.gRPC.OasysItem, metaclass=ViewType):


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

        raise AttributeError("View instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# Set the property locally
        self.__dict__[name] = value


# Static methods
    def Ac():
        """
        Autoscales the view

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Ac")

    def Ct():
        """
        Does a contour plot

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Ct")

    def GetTargetEye():
        """
        Get the current target and eye settings

        Returns
        -------
        dict
            Dict with properties
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetTargetEye")

    def Hi():
        """
        Does a Hidden line plot

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Hi")

    def Li():
        """
        Does a line (wireframe) plot

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Li")

    def Redraw():
        """
        Redraws the plot using the current plot mode

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Redraw")

    def SetContourType(view_type, view_subtype, view_subtype2):
        """
        Sets a contour type (and subtype)

        Parameters
        ----------
        view_type : constant
            The type of contour to plot. Can be: 
            View.ELEMPROPS, 
            View.ELEMQUAL, 
            View.INITVELS, 
            View.LOADSHELLDIRECTION, 
            View.MASSSCALE, 
            View.MATLPROPS, 
            View.PARTMASS, 
            View.SHELLNORMALS, 
            View.SHELLTHICKNESS, 
            View.TIMESTEP
        view_subtype : constant
            The subtype of contour to plot.
            Note: This second argument is NOT required for types TIMESTEP and LOADSHELLDIRECTION. 
            Subtypes for Type TIMESTEP: 
            No subtypes 
            Subtypes for Type SHELLTHICKNESS: 
            View.ABSOLUTE, 
            View.REMAINING, 
            View.THINNING 
            Subtypes for SHELLNORMALS: 
            View.CONTOUR, 
            View.VECTOR 
            Subtypes for Type LOADSHELLDIRECTION: 
            No subtypes 
            Subtypes for Type ELEMPROPS: 
            View.AREA, 
            View.FORM, 
            View.FORMULATION, 
            View.INTPOINTS, 
            View.PLASTICSTRAIN, 
            View.VOLUME 
            Subtypes for Type ELEMQUAL: 
            View.ASPECTRATIO, 
            View.FAILEDCRITERIA, 
            View.JACOBIAN, 
            View.MAXINTANGLE, 
            View.MININTANGLE, 
            View.MINLENGTH, 
            View.QUALIMPERF, 
            View.SKEW, 
            View.TAPER, 
            View.TETCOLLAPSE, 
            View.WARPAGE 
            Subtypes for Type MASSSCALE: 
            View.ADDEDMASS, 
            View.ADDEDMASSPART, 
            View.PERCENTADDEDMASS, 
            View.PERCENTADDEDMASSPART 
            Subtypes for Type MATLPROPS: 
            View.DENSITY, 
            View.MATERIALNUMBER, 
            View.POISSONRATIO, 
            View.YIELDSTRESS, 
            View.YOUNGMODULUS 
            Subtypes for Type INITVELS: 
            View.INITVELX, 
            View.INITVELY, 
            View.INITVELZ, 
            View.INITVELRES 
            Subtypes for Type PARTMASS: 
            View.EMPFINALMASS, 
            View.EMPNSMASS, 
            View.EMPSTRUCTMASS, 
            View.FINALMASS, 
            View.STRUCTMASS
        view_subtype2 : constant
            The subtype of contour to plot.
            Note: This third argument is required only for ELEMENTPROP ->PLASTICSTRAIN/FORM/AREA/VOLUME. 
            The default is PARAMETRIC COORDINATE. 
            Subtypes for Type ELEMENTPROP -> PLASTICSTRAIN/FORM/AREA/VOLUME: 
            View.INTEGRATIONPOINT, 
            View.MAXSTRAIN, 
            View.MINSTRAIN, 
            View.PARAMETRICCOORD

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "SetContourType", view_type, view_subtype, view_subtype2)

    def SetTargetEye(info):
        """
        Set the current target and eye settings

        Parameters
        ----------
        info : dict
            Dictionary containing the target and eye properties

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "SetTargetEye", info)

    def Sh():
        """
        Does a shaded plot

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Sh")

    def Show(view_type):
        """
        Redraws using one of the standard views

        Parameters
        ----------
        view_type : constant
            The view to show. Can be +/-View.XY,
            +/-View.YZ,
            +/-View.XZ or
            +/-View.ISO

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Show", view_type)

    def Si():
        """
        Does a shaded image contour plot

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Si")

    def Vec():
        """
        Does a vector plot

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Vec")

