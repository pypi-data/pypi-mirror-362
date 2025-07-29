import Oasys.gRPC


# Metaclass for static properties and constants
class BeamType(type):

    def __getattr__(cls, name):

        raise AttributeError("Beam class attribute '{}' does not exist".format(name))


class Beam(Oasys.gRPC.OasysItem, metaclass=BeamType):
    _props = {'cid', 'cid_1', 'colour', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'dofn1', 'dofn2', 'dofns', 'eid', 'elbow', 'include', 'iner', 'label', 'local', 'mn', 'n1', 'n2', 'n3', 'offset', 'orientation', 'parm1', 'parm2', 'parm3', 'parm4', 'parm5', 'pid', 'pid1', 'pid2', 'pid_opt', 'rr1', 'rr2', 'rt1', 'rt2', 'scalar', 'scalr', 'section', 'sn1', 'sn2', 'stype', 'thickness', 'transparency', 'vol', 'vx', 'vy', 'vz', 'warpage', 'wx1', 'wx2', 'wy1', 'wy2', 'wz1', 'wz2'}
    _rprops = {'exists', 'model', 'nodes'}


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
        if name in Beam._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in Beam._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("Beam instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Beam._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in Beam._rprops:
            raise AttributeError("Cannot set read-only Beam instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, eid, pid, n1, n2=Oasys.gRPC.defaultArg, n3=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, eid, pid, n1, n2, n3)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new Beam object. Use either 1, 2 or 3 nodes when
        creating a new beam

        Parameters
        ----------
        model : Model
            Model that beam will be created in
        eid : integer
            Beam number
        pid : integer
            Part number
        n1 : integer
            Node number 1
        n2 : integer
            Optional. Node number 2
        n3 : integer
            Optional. Node number 3

        Returns
        -------
        Beam
            Beam object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def BlankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the beams in the model

        Parameters
        ----------
        model : Model
            Model that all beams will be blanked in
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
        Blanks all of the flagged beams in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged beams will be blanked in
        flag : Flag
            Flag set on the beams that you want to blank
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
        Starts an interactive editing panel to create a beam

        Parameters
        ----------
        model : Model
            Model that the beam will be created in
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        Beam
            Beam object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, modal)

    def FindBeamInBox(model, xmin, xmax, ymin, ymax, zmin, zmax, flag=Oasys.gRPC.defaultArg, excl=Oasys.gRPC.defaultArg, vis_only=Oasys.gRPC.defaultArg):
        """
        Returns a list of Beam objects for the beams within a box.
        Please note this function provides a list of all beams that could potentially
        be in the box (using computationally cheap bounding box comparison) it is not
        a rigorous test of whether the beam is actually in the box.
        Note an extension of "spot_thickness" is applied to each beam.
        This may include beams that are ostensibly outside box. The user should apply their own test.
        (this function is intended to provide an upper bound of elems to test)
        Setting the "excl" flag will require that the beam is fully contained,
        but this may not capture all the beams you want to process

        Parameters
        ----------
        model : Model
            Model designated model
        xmin : real
            Minimum bound in global x
        xmax : real
            Maximum bound in global x
        ymin : real
            Minimum bound in global y
        ymax : real
            Maximum bound in global y
        zmin : real
            Minimum bound in global z
        zmax : real
            Maximum bound in global z
        flag : integer
            Optional. Optional flag to restrict beams considered, if 0 all beams considered
        excl : integer
            Optional. Optional flag ( 0) Apply inclusive selection
            ( 1) Apply exclusive selection
            inclusive selection means elements intersect box
            exclusive selection means elements contained in box
        vis_only : integer
            Optional. Optional flag to consider visible elements only (1), if (0) all elements considered

        Returns
        -------
        list
            List of Beam objects
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FindBeamInBox", model, xmin, xmax, ymin, ymax, zmin, zmax, flag, excl, vis_only)

    def First(model):
        """
        Returns the first beam in the model

        Parameters
        ----------
        model : Model
            Model to get first beam in

        Returns
        -------
        Beam
            Beam object (or None if there are no beams in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FirstFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the first free beam label in the model.
        Also see Beam.LastFreeLabel(),
        Beam.NextFreeLabel() and
        Model.FirstFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get first free beam label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            First free in layer in editing panels). If omitted the whole model will be used (Equivalent to
            First free in editing panels)

        Returns
        -------
        int
            Beam label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FirstFreeLabel", model, layer)

    def FlagAll(model, flag):
        """
        Flags all of the beams in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all beams will be flagged in
        flag : Flag
            Flag to set on the beams

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Beam objects or properties for all of the beams in a model in PRIMER.
        If the optional property argument is not given then a list of Beam objects is returned.
        If the property argument is given, that property value for each beam is returned in the list
        instead of a Beam object

        Parameters
        ----------
        model : Model
            Model to get beams from
        property : string
            Optional. Name for property to get for all beams in the model

        Returns
        -------
        list
            List of Beam objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Beam objects for all of the flagged beams in a model in PRIMER
        If the optional property argument is not given then a list of Beam objects is returned.
        If the property argument is given, then that property value for each beam is returned in the list
        instead of a Beam object

        Parameters
        ----------
        model : Model
            Model to get beams from
        flag : Flag
            Flag set on the beams that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged beams in the model

        Returns
        -------
        list
            List of Beam objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the Beam object for a beam ID

        Parameters
        ----------
        model : Model
            Model to find the beam in
        number : integer
            number of the beam you want the Beam object for

        Returns
        -------
        Beam
            Beam object (or None if beam does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last beam in the model

        Parameters
        ----------
        model : Model
            Model to get last beam in

        Returns
        -------
        Beam
            Beam object (or None if there are no beams in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def LastFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the last free beam label in the model.
        Also see Beam.FirstFreeLabel(),
        Beam.NextFreeLabel() and
        see Model.LastFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get last free beam label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest free in layer in editing panels). If omitted the whole model will be used

        Returns
        -------
        int
            Beam label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "LastFreeLabel", model, layer)

    def NextFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the next free (highest+1) beam label in the model.
        Also see Beam.FirstFreeLabel(),
        Beam.LastFreeLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get next free beam label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest+1 in layer in editing panels). If omitted the whole model will be used (Equivalent to
            Highest+1 in editing panels)

        Returns
        -------
        int
            Beam label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NextFreeLabel", model, layer)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a beam

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only beams from that model can be picked.
            If the argument is a Flag then only beams that
            are flagged with limit can be selected.
            If omitted, or None, any beams from any model can be selected.
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
        Beam
            Beam object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def RenumberAll(model, start):
        """
        Renumbers all of the beams in the model

        Parameters
        ----------
        model : Model
            Model that all beams will be renumbered in
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
        Renumbers all of the flagged beams in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged beams will be renumbered in
        flag : Flag
            Flag set on the beams that you want to renumber
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
        Allows the user to select beams using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting beams
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only beams from that model can be selected.
            If the argument is a Flag then only beams that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any beams can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of beams selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged beams in the model. The beams will be sketched until you either call
        Beam.Unsketch(),
        Beam.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged beams will be sketched in
        flag : Flag
            Flag set on the beams that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the beams are sketched.
            If omitted redraw is true. If you want to sketch flagged beams several times and only
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
        Returns the total number of beams in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing beams should be counted. If false or omitted
            referenced but undefined beams will also be included in the total

        Returns
        -------
        int
            number of beams
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnblankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the beams in the model

        Parameters
        ----------
        model : Model
            Model that all beams will be unblanked in
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
        Unblanks all of the flagged beams in the model

        Parameters
        ----------
        model : Model
            Model that the flagged beams will be unblanked in
        flag : Flag
            Flag set on the beams that you want to unblank
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
        Unsets a defined flag on all of the beams in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all beams will be unset in
        flag : Flag
            Flag to unset on the beams

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all beams

        Parameters
        ----------
        model : Model
            Model that all beams will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the beams are unsketched.
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
        Unsketches all flagged beams in the model

        Parameters
        ----------
        model : Model
            Model that all beams will be unsketched in
        flag : Flag
            Flag set on the beams that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the beams are unsketched.
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
        Associates a comment with a beam

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the beam

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def Blank(self):
        """
        Blanks the beam

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank")

    def Blanked(self):
        """
        Checks if the beam is blanked or not

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
        Clears a flag on the beam

        Parameters
        ----------
        flag : Flag
            Flag to clear on the beam

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the beam. The target include of the copied beam can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        Beam
            Beam object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a beam

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the beam

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

    def ElemCut(self, database_cross_section_label):
        """
        Returns coordinates of the intersections between a beam and a database cross section.
        Note this function does not check that the beam is in the cross section definition (part set)

        Parameters
        ----------
        database_cross_section_label : integer
            The label of the database cross section

        Returns
        -------
        list
            A list containing the x,y,z coordinates of the cut point, or None if it does not cut
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ElemCut", database_cross_section_label)

    def ExtractColour(self):
        """
        Extracts the actual colour used for beam.
        By default in PRIMER many entities such as elements get their colour automatically from the part that they are in.
        PRIMER cycles through 13 default colours based on the label of the entity. In this case the beam colour
        property will return the value Colour.PART instead of the actual colour.
        This method will return the actual colour which is used for drawing the beam

        Returns
        -------
        int
            colour value (integer)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ExtractColour")

    def Flagged(self, flag):
        """
        Checks if the beam is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the beam

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a beam

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a Beam property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the Beam.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            beam property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this beam (\*BEAM, \*BEAM_SCALAR or \*BEAM_SCALAR_VALUE).
        Note that a carriage return is not added.
        See also Beam.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the beam.
        Note that a carriage return is not added.
        See also Beam.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next beam in the model

        Returns
        -------
        Beam
            Beam object (or None if there are no more beams in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous beam in the model

        Returns
        -------
        Beam
            Beam object (or None if there are no more beams in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SectionFacePoints(self, face):
        """
        Returns the indices of the points for a faces to plot the true section of the beam.
        Note face numbers start at 0.
        Beam.SectionPoints must be called before this method

        Parameters
        ----------
        face : integer
            Face to get indices for

        Returns
        -------
        int
            List of integers
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SectionFacePoints", face)

    def SectionFaces(self):
        """
        Returns the number of faces to plot the true section of the beam.
        Beam.SectionPoints must be called before this method

        Returns
        -------
        int
            integer
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SectionFaces")

    def SectionPoints(self):
        """
        Returns the point coordinates to plot the true section of the beam.
        They are returned in a single list of numbers

        Returns
        -------
        float
            List of floats
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SectionPoints")

    def SetFlag(self, flag):
        """
        Sets a flag on the beam

        Parameters
        ----------
        flag : Flag
            Flag to set on the beam

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the beam. The beam will be sketched until you either call
        Beam.Unsketch(),
        Beam.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the beam is sketched.
            If omitted redraw is true. If you want to sketch several beams and only
            redraw after the last one then use false for redraw and call
            View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Sketch", redraw)

    def TiedNodeCheck(self, contact_label, flag, option1, option2):
        """
        Checks if nodes of beam are tied by contact or directly attached (non-zero option1)

        Parameters
        ----------
        contact_label : integer
            The label of the tied contact. If zero the tied contact is found for the beam by reverse lookup
        flag : Flag
            flag bit
        option1 : integer
            Directly tied node (logical OR) 0:NONE 1:NRB/C_EXNO 2:BEAM 4:SHELL 8:SOLID 16:TSHELL
        option2 : integer
            0:No action 1:report error if directly attached node (acc. option1) also captured by contact

        Returns
        -------
        str
            string
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "TiedNodeCheck", contact_label, flag, option1, option2)

    def Timestep(self):
        """
        Calculates the timestep for the beam

        Returns
        -------
        float
            float
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Timestep")

    def Unblank(self):
        """
        Unblanks the beam

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank")

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the beam

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the beam is unsketched.
            If omitted redraw is true. If you want to unsketch several beams and only
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
        Beam
            Beam object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this beam

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

