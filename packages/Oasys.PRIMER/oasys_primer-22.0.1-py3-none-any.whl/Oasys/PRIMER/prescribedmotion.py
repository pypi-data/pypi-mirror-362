import Oasys.gRPC


# Metaclass for static properties and constants
class PrescribedMotionType(type):
    _consts = {'EDGE_UVW', 'FACE_XYZ', 'NODE', 'NRBC', 'NRBC_LOCAL', 'POINT_UVW', 'RIGID', 'RIGID_LOCAL', 'SET', 'SET_BOX', 'SET_EDGE_UVW', 'SET_FACE_XYZ', 'SET_LINE', 'SET_POINT_UVW', 'SET_SEGMENT'}

    def __getattr__(cls, name):
        if name in PrescribedMotionType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("PrescribedMotion class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in PrescribedMotionType._consts:
            raise AttributeError("Cannot set PrescribedMotion class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class PrescribedMotion(Oasys.gRPC.OasysItem, metaclass=PrescribedMotionType):
    _props = {'birth', 'bndout2dynain', 'death', 'dof', 'form', 'heading', 'id', 'include', 'label', 'lcid', 'lrb', 'nbeg', 'nend', 'node1', 'node2', 'offset1', 'offset2', 'prmr', 'sf', 'sfd', 'type', 'typeid', 'vad', 'vid'}
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
        if name in PrescribedMotion._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in PrescribedMotion._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("PrescribedMotion instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in PrescribedMotion._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in PrescribedMotion._rprops:
            raise AttributeError("Cannot set read-only PrescribedMotion instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model, typeid, dof, vad, lcid, type, label=Oasys.gRPC.defaultArg, heading=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, model, typeid, dof, vad, lcid, type, label, heading)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new PrescribedMotion object

        Parameters
        ----------
        model : Model
            Model that PrescribedMotion will be created in
        typeid : integer
            Node ID, node set ID or part ID
        dof : integer
            Degree of freedom
        vad : integer
            Velocity/acceleration/displacement flag
        lcid : integer
            Load curve for motion
        type : constant
            Specify the type of prescribed motion (Can be
            PrescribedMotion.NODE,
            PrescribedMotion.SET,
            PrescribedMotion.RIGID,
            PrescribedMotion.RIGID_LOCAL,
            PrescribedMotion.NRBC,
            PrescribedMotion.NRBC_LOCAL,
            PrescribedMotion.SET_BOX,
            PrescribedMotion.SET_SEGMENT, 
            PrescribedMotion.SET_LINE,
            PrescribedMotion.POINT_UVW,
            PrescribedMotion.EDGE_UVW,
            PrescribedMotion.FACE_XYZ,
            PrescribedMotion.SET_POINT_UVW,
            PrescribedMotion.SET_EDGE_UVW or
            PrescribedMotion.SET_FACE_XYZ)
        label : integer
            Optional. PrescribedMotion number
        heading : string
            Optional. Title for the PrescribedMotion

        Returns
        -------
        PrescribedMotion
            PrescribedMotion object
        """


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def AnimationBackward():
        """
        Moves backward one frame of a PrescribedMotion animation (pausing animation first if required).
        Also see the PrescribedMotion.AnimationBegin() method
        which MUST be called before you start animating and the 
        PrescribedMotion.AnimationFinish() method
        which MUST be called after you have finished animating

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "AnimationBackward")

    def AnimationBegin(model, flag):
        """
        Begins a PrescribedMotion animation. This MUST be called before any of the other Animation methods.
        Also see the PrescribedMotion.AnimationFinish() method
        which MUST be called after you have finished animating

        Parameters
        ----------
        model : Model
            Model that PrescribedMotions are in
        flag : Flag
            Flag set on the PrescribedMotions that you want to animate

        Returns
        -------
        dict
            Dict with properties
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "AnimationBegin", model, flag)

    def AnimationFinish():
        """
        Finishes a PrescribedMotion animation. This MUST be called to finish animating. This will
        restore nodal coordinates but will not perform a graphics update.
        Also see the PrescribedMotion.AnimationBegin() method
        which MUST be called before you start animating

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "AnimationFinish")

    def AnimationForward():
        """
        Moves forward one frame of a PrescribedMotion animation (pausing animation first if required).
        Also see the PrescribedMotion.AnimationBegin() method
        which MUST be called before you start animating and the 
        PrescribedMotion.AnimationFinish() method
        which MUST be called after you have finished animating

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "AnimationForward")

    def AnimationGetData():
        """
        Returns the animation data (pausing animation first if required).
        Also see the PrescribedMotion.AnimationBegin() method
        which MUST be called before you start animating and the 
        PrescribedMotion.AnimationFinish() method
        which MUST be called after you have finished animating

        Returns
        -------
        dict
            Dict with properties
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "AnimationGetData")

    def AnimationPause():
        """
        Pauses playback of a PrescribedMotion animation.
        Also see the PrescribedMotion.AnimationBegin() method
        which MUST be called before you start animating and the 
        PrescribedMotion.AnimationFinish() method
        which MUST be called after you have finished animating

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "AnimationPause")

    def AnimationPlay():
        """
        Starts playback of a PrescribedMotion animation.
        Also see the PrescribedMotion.AnimationBegin() method
        which MUST be called before you start animating and the 
        PrescribedMotion.AnimationFinish() method
        which MUST be called after you have finished animating.
        This method should only be used
        from a script which implements a user interface so you can actually stop the animation!
        Don't forget to add a pause/stop button that calls 
        PrescribedMotion.AnimationPause()!

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "AnimationPlay")

    def AnimationSetData(data):
        """
        Sets the current animation data (pausing animation first if required).
        Also see the PrescribedMotion.AnimationBegin() method
        which MUST be called before you start animating and the 
        PrescribedMotion.AnimationFinish() method
        which MUST be called after you have finished animating

        Parameters
        ----------
        data : dict
            data returned from PrescribedMotion.AnimationBegin()
            or PrescribedMotion.AnimationGetData()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "AnimationSetData", data)

    def AnimationToEnd():
        """
        Moves to the end of a PrescribedMotion animation (pausing animation first if required).
        Also see the PrescribedMotion.AnimationBegin() method
        which MUST be called before you start animating and the 
        PrescribedMotion.AnimationFinish() method
        which MUST be called after you have finished animating

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "AnimationToEnd")

    def AnimationToStart():
        """
        Moves to the start of a PrescribedMotion animation (pausing animation first if required).
        Also see the PrescribedMotion.AnimationBegin() method
        which MUST be called before you start animating and the 
        PrescribedMotion.AnimationFinish() method
        which MUST be called after you have finished animating

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "AnimationToStart")

    def AnimationToTime():
        """
        Moves to a specific time in a PrescribedMotion animation (pausing animation first if required).
        Also see the PrescribedMotion.AnimationBegin() method
        which MUST be called before you start animating and the 
        PrescribedMotion.AnimationFinish() method
        which MUST be called after you have finished animating

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "AnimationToTime")

    def BlankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the boundary prescribed motions in the model

        Parameters
        ----------
        model : Model
            Model that all boundary prescribed motions will be blanked in
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
        Blanks all of the flagged boundary prescribed motions in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged boundary prescribed motions will be blanked in
        flag : Flag
            Flag set on the boundary prescribed motions that you want to blank
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
        Returns the first boundary prescribed motion in the model

        Parameters
        ----------
        model : Model
            Model to get first boundary prescribed motion in

        Returns
        -------
        PrescribedMotion
            PrescribedMotion object (or None if there are no boundary prescribed motions in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model)

    def FirstFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the first free boundary prescribed motion label in the model.
        Also see PrescribedMotion.LastFreeLabel(),
        PrescribedMotion.NextFreeLabel() and
        Model.FirstFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get first free boundary prescribed motion label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            First free in layer in editing panels). If omitted the whole model will be used (Equivalent to
            First free in editing panels)

        Returns
        -------
        int
            PrescribedMotion label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FirstFreeLabel", model, layer)

    def FlagAll(model, flag):
        """
        Flags all of the boundary prescribed motions in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all boundary prescribed motions will be flagged in
        flag : Flag
            Flag to set on the boundary prescribed motions

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of PrescribedMotion objects or properties for all of the boundary prescribed motions in a model in PRIMER.
        If the optional property argument is not given then a list of PrescribedMotion objects is returned.
        If the property argument is given, that property value for each boundary prescribed motion is returned in the list
        instead of a PrescribedMotion object

        Parameters
        ----------
        model : Model
            Model to get boundary prescribed motions from
        property : string
            Optional. Name for property to get for all boundary prescribed motions in the model

        Returns
        -------
        list
            List of PrescribedMotion objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of PrescribedMotion objects for all of the flagged boundary prescribed motions in a model in PRIMER
        If the optional property argument is not given then a list of PrescribedMotion objects is returned.
        If the property argument is given, then that property value for each boundary prescribed motion is returned in the list
        instead of a PrescribedMotion object

        Parameters
        ----------
        model : Model
            Model to get boundary prescribed motions from
        flag : Flag
            Flag set on the boundary prescribed motions that you want to retrieve
        property : string
            Optional. Name for property to get for all flagged boundary prescribed motions in the model

        Returns
        -------
        list
            List of PrescribedMotion objects or properties
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, number):
        """
        Returns the PrescribedMotion object for a boundary prescribed motion ID

        Parameters
        ----------
        model : Model
            Model to find the boundary prescribed motion in
        number : integer
            number of the boundary prescribed motion you want the PrescribedMotion object for

        Returns
        -------
        PrescribedMotion
            PrescribedMotion object (or None if boundary prescribed motion does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last boundary prescribed motion in the model

        Parameters
        ----------
        model : Model
            Model to get last boundary prescribed motion in

        Returns
        -------
        PrescribedMotion
            PrescribedMotion object (or None if there are no boundary prescribed motions in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model)

    def LastFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the last free boundary prescribed motion label in the model.
        Also see PrescribedMotion.FirstFreeLabel(),
        PrescribedMotion.NextFreeLabel() and
        see Model.LastFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get last free boundary prescribed motion label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest free in layer in editing panels). If omitted the whole model will be used

        Returns
        -------
        int
            PrescribedMotion label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "LastFreeLabel", model, layer)

    def NextFreeLabel(model, layer=Oasys.gRPC.defaultArg):
        """
        Returns the next free (highest+1) boundary prescribed motion label in the model.
        Also see PrescribedMotion.FirstFreeLabel(),
        PrescribedMotion.LastFreeLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get next free boundary prescribed motion label in
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest+1 in layer in editing panels). If omitted the whole model will be used (Equivalent to
            Highest+1 in editing panels)

        Returns
        -------
        int
            PrescribedMotion label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NextFreeLabel", model, layer)

    def Pick(prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a boundary prescribed motion

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only boundary prescribed motions from that model can be picked.
            If the argument is a Flag then only boundary prescribed motions that
            are flagged with limit can be selected.
            If omitted, or None, any boundary prescribed motions from any model can be selected.
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
        PrescribedMotion
            PrescribedMotion object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", prompt, limit, modal, button_text)

    def RenumberAll(model, start):
        """
        Renumbers all of the boundary prescribed motions in the model

        Parameters
        ----------
        model : Model
            Model that all boundary prescribed motions will be renumbered in
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
        Renumbers all of the flagged boundary prescribed motions in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged boundary prescribed motions will be renumbered in
        flag : Flag
            Flag set on the boundary prescribed motions that you want to renumber
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
        Allows the user to select boundary prescribed motions using standard PRIMER object menus

        Parameters
        ----------
        flag : Flag
            Flag to use when selecting boundary prescribed motions
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only boundary prescribed motions from that model can be selected.
            If the argument is a Flag then only boundary prescribed motions that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any boundary prescribed motions can be selected.
            from any model
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of boundary prescribed motions selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", flag, prompt, limit, modal)

    def SketchFlagged(model, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged boundary prescribed motions in the model. The boundary prescribed motions will be sketched until you either call
        PrescribedMotion.Unsketch(),
        PrescribedMotion.UnsketchFlagged(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        model : Model
            Model that all the flagged boundary prescribed motions will be sketched in
        flag : Flag
            Flag set on the boundary prescribed motions that you want to sketch
        redraw : boolean
            Optional. If model should be redrawn or not after the boundary prescribed motions are sketched.
            If omitted redraw is true. If you want to sketch flagged boundary prescribed motions several times and only
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
        Returns the total number of boundary prescribed motions in the model

        Parameters
        ----------
        model : Model
            Model to get total for
        exists : boolean
            Optional. true if only existing boundary prescribed motions should be counted. If false or omitted
            referenced but undefined boundary prescribed motions will also be included in the total

        Returns
        -------
        int
            number of boundary prescribed motions
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total", model, exists)

    def UnblankAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the boundary prescribed motions in the model

        Parameters
        ----------
        model : Model
            Model that all boundary prescribed motions will be unblanked in
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
        Unblanks all of the flagged boundary prescribed motions in the model

        Parameters
        ----------
        model : Model
            Model that the flagged boundary prescribed motions will be unblanked in
        flag : Flag
            Flag set on the boundary prescribed motions that you want to unblank
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
        Unsets a defined flag on all of the boundary prescribed motions in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all boundary prescribed motions will be unset in
        flag : Flag
            Flag to unset on the boundary prescribed motions

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)

    def UnsketchAll(model, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all boundary prescribed motions

        Parameters
        ----------
        model : Model
            Model that all boundary prescribed motions will be unblanked in
        redraw : boolean
            Optional. If model should be redrawn or not after the boundary prescribed motions are unsketched.
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
        Unsketches all flagged boundary prescribed motions in the model

        Parameters
        ----------
        model : Model
            Model that all boundary prescribed motions will be unsketched in
        flag : Flag
            Flag set on the boundary prescribed motions that you want to unsketch
        redraw : boolean
            Optional. If model should be redrawn or not after the boundary prescribed motions are unsketched.
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
        Associates a comment with a boundary prescribed motion

        Parameters
        ----------
        comment : Comment
            Comment that will be attached to the boundary prescribed motion

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AssociateComment", comment)

    def Blank(self):
        """
        Blanks the boundary prescribed motion

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank")

    def Blanked(self):
        """
        Checks if the boundary prescribed motion is blanked or not

        Returns
        -------
        bool
            True if blanked, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blanked")

    def ClearFlag(self, flag):
        """
        Clears a flag on the boundary prescribed motion

        Parameters
        ----------
        flag : Flag
            Flag to clear on the boundary prescribed motion

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the boundary prescribed motion. The target include of the copied boundary prescribed motion can be set using Options.copy_target_include

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. Default value is false.
            To set current include, use Include.MakeCurrentLayer()

        Returns
        -------
        PrescribedMotion
            PrescribedMotion object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def DetachComment(self, comment):
        """
        Detaches a comment from a boundary prescribed motion

        Parameters
        ----------
        comment : Comment
            Comment that will be detached from the boundary prescribed motion

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "DetachComment", comment)

    def Flagged(self, flag):
        """
        Checks if the boundary prescribed motion is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the boundary prescribed motion

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetComments(self):
        """
        Extracts the comments associated to a boundary prescribed motion

        Returns
        -------
        list
            List of Comment objects (or None if there are no comments associated to the node)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetComments")

    def GetParameter(self, prop):
        """
        Checks if a PrescribedMotion property is a parameter or not.
        Note that object properties that are parameters are normally returned as the integer or
        float parameter values as that is virtually always what the user would want. For this function to
        work the JavaScript interpreter must use the parameter name instead of the value. This can be done by setting
        the Options.property_parameter_names option to true
        before calling the function and then resetting it to false afterwards..
        This behaviour can also temporarily be switched by using the PrescribedMotion.ViewParameters()
        method and 'method chaining' (see the examples below)

        Parameters
        ----------
        prop : string
            boundary prescribed motion property to get parameter for

        Returns
        -------
        Parameter
            Parameter object if property is a parameter, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetParameter", prop)

    def Keyword(self):
        """
        Returns the keyword for this PrescribedMotion (\*BOUNDARY_PRESCRIBED_MOTION_xxxx).
        Note that a carriage return is not added.
        See also PrescribedMotion.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the PrescribedMotion.
        Note that a carriage return is not added.
        See also PrescribedMotion.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next boundary prescribed motion in the model

        Returns
        -------
        PrescribedMotion
            PrescribedMotion object (or None if there are no more boundary prescribed motions in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous boundary prescribed motion in the model

        Returns
        -------
        PrescribedMotion
            PrescribedMotion object (or None if there are no more boundary prescribed motions in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on the boundary prescribed motion

        Parameters
        ----------
        flag : Flag
            Flag to set on the boundary prescribed motion

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the boundary prescribed motion. The boundary prescribed motion will be sketched until you either call
        PrescribedMotion.Unsketch(),
        PrescribedMotion.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the boundary prescribed motion is sketched.
            If omitted redraw is true. If you want to sketch several boundary prescribed motions and only
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
        Unblanks the boundary prescribed motion

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank")

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the boundary prescribed motion

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the boundary prescribed motion is unsketched.
            If omitted redraw is true. If you want to unsketch several boundary prescribed motions and only
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
        PrescribedMotion
            PrescribedMotion object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ViewParameters")

    def Xrefs(self):
        """
        Returns the cross references for this boundary prescribed motion

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

