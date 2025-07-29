import Oasys.gRPC


# Metaclass for static properties and constants
class SetType(type):
    _consts = {'ADD', 'ALL_TYPES', 'BEAM', 'BOX', 'DISCRETE', 'GENERAL', 'GENERATE', 'IGA_EDGE', 'IGA_FACE', 'IGA_POINT_UVW', 'IGA_UVW', 'IGA_XYZ', 'INTERSECT', 'MM_GROUP', 'MODE', 'NODE', 'PART', 'PART_TREE', 'PERI_LAMINATE', 'SEGMENT', 'SEGMENT_2D', 'SHELL', 'SOLID', 'TSHELL'}

    def __getattr__(cls, name):
        if name in SetType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("Set class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in SetType._consts:
            raise AttributeError("Cannot set Set class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class Set(Oasys.gRPC.OasysItem, metaclass=SetType):
    _props = {'add', 'collect', 'colour', 'da1', 'da2', 'da3', 'da4', 'general', 'generate', 'include', 'intersect', 'its', 'label', 'model', 'sid', 'solver', 'title', 'transparency'}
    _rprops = {'advanced', 'collect_children', 'column', 'exists', 'general_lines', 'iga_opt', 'increment', 'smooth', 'total', 'type'}


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
        if name in Set._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in Set._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("Set instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Set._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in Set._rprops:
            raise AttributeError("Cannot set read-only Set instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self , model, *pargs, **kargs):
# Current constructor
        if len(pargs)==0 and len(kargs)==1:
            handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__ , model , kargs['details'])
        elif len(pargs)==1 and len(kargs)==0:
            handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__ , model , pargs[0])
# Must be deprecated constructor
        else:
            args = {
              'sid': Oasys.gRPC.missingArg,
              'type': Oasys.gRPC.missingArg,
              'title': Oasys.gRPC.defaultArg,
              'option': Oasys.gRPC.defaultArg
            }
            if len(pargs) >= 1:
                args['sid'] = pargs[0]
            if len(pargs) >= 2:
                args['type'] = pargs[1]
            if len(pargs) >= 3:
                args['title'] = pargs[2]
            if len(pargs) >= 4:
                args['option'] = pargs[3]
            for k in kargs:
                args[k] = kargs[k]
            for a in args:
                if args[a] == Oasys.gRPC.missingArg:
                    raise AttributeError("Argument {} missing in Set constructor".format(a))
            handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__ , model , args['sid'], args['type'], args['title'], args['option'])

        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)


# String representation
    def __repr__(self):
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "toString")


# Static methods
    def BlankAll(model, type=Oasys.gRPC.defaultArg, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the sets in the model

        Parameters
        ----------
        model : Model
            Model that all sets will be blanked in
        type : constant
            Optional. Type of sets to blank. Can be Set.BEAM,
            Set.BOX,
            Set.DISCRETE,
            Set.MM_GROUP,
            Set.NODE,
            Set.PART,
            Set.PART_TREE,
            Set.PERI_LAMINATE,
            Set.SEGMENT,
            Set.SEGMENT_2D,
            Set.SHELL,
            Set.SOLID or
            Set.TSHELL.
            Set.ALL_TYPES.
            If omitted sets of all types will be blanked
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
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "BlankAll", model, type, redraw)

    def BlankFlagged(model, flag, type=Oasys.gRPC.defaultArg, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the flagged sets in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged sets will be blanked in
        flag : Flag
            Flag set on the sets that you want to blank
        type : constant
            Optional. Type of sets to blank. Can be Set.BEAM,
            Set.BOX,
            Set.DISCRETE,
            Set.MM_GROUP,
            Set.NODE,
            Set.PART,
            Set.PART_TREE,
            Set.PERI_LAMINATE,
            Set.SEGMENT,
            Set.SEGMENT_2D,
            Set.SHELL,
            Set.SOLID or
            Set.TSHELL.
            Set.ALL_TYPES.
            If set, only flagged sets of this type will be blanked. If omitted flagged sets of all types will be blanked
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
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "BlankFlagged", model, flag, type, redraw)

    def Create(model, type, modal=Oasys.gRPC.defaultArg):
        """
        Starts an interactive editing panel to create a set

        Parameters
        ----------
        model : Model
            Model that the set will be created in
        type : constant
            Type of the set that you want to create. Can be Set.BEAM,
            Set.BOX,
            Set.DISCRETE,
            Set.IGA_EDGE,
            Set.IGA_FACE,
            Set.IGA_POINT_UVW,
            Set.MM_GROUP,
            Set.MODE,
            Set.NODE,
            Set.PART,
            Set.PART_TREE,
            Set.PERI_LAMINATE,
            Set.SEGMENT,
            Set.SEGMENT_2D,
            Set.SHELL,
            Set.SOLID or
            Set.TSHELL
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        Set
            Set object (or None if not made)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Create", model, type, modal)

    def First(model, type):
        """
        Returns the first set in the model

        Parameters
        ----------
        model : Model
            Model to get first set in
        type : constant
            Type of the set. Can be Set.BEAM,
            Set.BOX,
            Set.DISCRETE,
            Set.IGA_EDGE,
            Set.IGA_FACE,
            Set.IGA_POINT_UVW,
            Set.MM_GROUP,
            Set.MODE,
            Set.NODE,
            Set.PART,
            Set.PART_TREE,
            Set.PERI_LAMINATE,
            Set.SEGMENT,
            Set.SEGMENT_2D,
            Set.SHELL,
            Set.SOLID or
            Set.TSHELL

        Returns
        -------
        Set
            Set object (or None if there are no sets in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First", model, type)

    def FirstFreeLabel(model, type, layer=Oasys.gRPC.defaultArg):
        """
        Returns the first free set label in the model.
        Also see Set.LastFreeLabel(),
        Set.NextFreeLabel() and
        Model.FirstFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get first free Set label in
        type : constant
            Type of the set. Can be Set.BEAM,
            Set.BOX,
            Set.DISCRETE,
            Set.IGA_EDGE,
            Set.IGA_FACE,
            Set.IGA_POINT_UVW,
            Set.MM_GROUP,
            Set.MODE,
            Set.NODE,
            Set.PART,
            Set.PART_TREE,
            Set.PERI_LAMINATE,
            Set.SEGMENT,
            Set.SEGMENT_2D,
            Set.SHELL,
            Set.SOLID or
            Set.TSHELL
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            First free in layer in editing panels). If omitted the whole model will be used (Equivalent to
            First free in editing panels)

        Returns
        -------
        int
            Set label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FirstFreeLabel", model, type, layer)

    def FlagAll(model, flag, type=Oasys.gRPC.defaultArg):
        """
        Flags all of the sets in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all sets will be flagged in
        flag : Flag
            Flag to set on the sets
        type : constant
            Optional. Type of the set. Can be Set.BEAM,
            Set.BOX
            Set.DISCRETE,
            Set.IGA_EDGE,
            Set.IGA_FACE,
            Set.IGA_POINT_UVW,
            Set.MM_GROUP,
            Set.MODE,
            Set.NODE,
            Set.PART,
            Set.PART_TREE,
            Set.PERI_LAMINATE,
            Set.SEGMENT,
            Set.SEGMENT_2D,
            Set.SHELL,
            Set.SOLID or
            Set.TSHELL.
            If set, only sets of this type will be flagged. If omitted sets of all types will be flagged

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FlagAll", model, flag, type)

    def GetAll(model, type):
        """
        Returns a list of Set objects for all of the sets in a models in PRIMER

        Parameters
        ----------
        model : Model
            Model to get sets from
        type : constant
            Type of the set. Can be Set.BEAM,
            Set.BOX,
            Set.DISCRETE,
            Set.IGA_EDGE,
            Set.IGA_FACE,
            Set.IGA_POINT_UVW,
            Set.MM_GROUP,
            Set.MODE,
            Set.NODE,
            Set.PART,
            Set.PART_TREE,
            Set.PERI_LAMINATE,
            Set.SEGMENT,
            Set.SEGMENT_2D,
            Set.SHELL,
            Set.SOLID or
            Set.TSHELL

        Returns
        -------
        list
            List of Set objects
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetAll", model, type)

    def GetFlagged(model, flag, type):
        """
        Returns a list of Set objects for all of the flagged sets in a models in PRIMER

        Parameters
        ----------
        model : Model
            Model to get sets from
        flag : Flag
            Flag set on the set that you want to retrieve
        type : constant
            Type of the set. Can be Set.BEAM,
            Set.BOX,
            Set.DISCRETE,
            Set.IGA_EDGE,
            Set.IGA_FACE,
            Set.IGA_POINT_UVW,
            Set.MM_GROUP,
            Set.MODE,
            Set.NODE,
            Set.PART,
            Set.PART_TREE,
            Set.PERI_LAMINATE,
            Set.SEGMENT,
            Set.SEGMENT_2D,
            Set.SHELL,
            Set.SOLID or
            Set.TSHELL

        Returns
        -------
        list
            List of Set objects
        """
        return Oasys.PRIMER._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, type)

    def GetFromID(model, set_number, type):
        """
        Returns the Set object for a set ID

        Parameters
        ----------
        model : Model
            Model to find the set in
        set_number : integer
            number of the set you want the Set object for
        type : constant
            Type of the set. Can be Set.BEAM,
            Set.BOX,
            Set.DISCRETE,
            Set.IGA_EDGE,
            Set.IGA_FACE,
            Set.IGA_POINT_UVW,
            Set.MM_GROUP,
            Set.MODE,
            Set.NODE,
            Set.PART,
            Set.PART_TREE,
            Set.PERI_LAMINATE,
            Set.SEGMENT,
            Set.SEGMENT_2D,
            Set.SHELL,
            Set.SOLID or
            Set.TSHELL

        Returns
        -------
        Set
            Set object (or None if set does not exist)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model, set_number, type)

    def Last(model, type):
        """
        Returns the last set in the model

        Parameters
        ----------
        model : Model
            Model to get last set in
        type : constant
            Type of the set. Can be Set.BEAM,
            Set.BOX,
            Set.DISCRETE,
            Set.IGA_EDGE,
            Set.IGA_FACE,
            Set.IGA_POINT_UVW,
            Set.MM_GROUP,
            Set.MODE,
            Set.NODE,
            Set.PART,
            Set.PART_TREE,
            Set.PERI_LAMINATE,
            Set.SEGMENT,
            Set.SEGMENT_2D,
            Set.SHELL,
            Set.SOLID or
            Set.TSHELL

        Returns
        -------
        Set
            Set object (or None if there are no sets in the model)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last", model, type)

    def LastFreeLabel(model, type, layer=Oasys.gRPC.defaultArg):
        """
        Returns the last free set label in the model.
        Also see Set.FirstFreeLabel(),
        Set.NextFreeLabel() and
        Model.LastFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get last free Set label in
        type : constant
            Type of the set. Can be Set.BEAM,
            Set.BOX,
            Set.DISCRETE,
            Set.IGA_EDGE,
            Set.IGA_FACE,
            Set.IGA_POINT_UVW,
            Set.MM_GROUP,
            Set.MODE,
            Set.NODE,
            Set.PART,
            Set.PART_TREE,
            Set.PERI_LAMINATE,
            Set.SEGMENT,
            Set.SEGMENT_2D,
            Set.SHELL,
            Set.SOLID or
            Set.TSHELL
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest free in layer in editing panels). If omitted the whole model will be used

        Returns
        -------
        int
            Set label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "LastFreeLabel", model, type, layer)

    def NextFreeLabel(model, type, layer=Oasys.gRPC.defaultArg):
        """
        Returns the next free set label in the model.
        Also see Set.FirstFreeLabel(),
        Set.LastFreeLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        model : Model
            Model to get next free Set label in
        type : constant
            Type of the set. Can be Set.BEAM,
            Set.BOX,
            Set.DISCRETE,
            Set.IGA_EDGE,
            Set.IGA_FACE,
            Set.IGA_POINT_UVW,
            Set.MM_GROUP,
            Set.MODE,
            Set.NODE,
            Set.PART,
            Set.PART_TREE,
            Set.PERI_LAMINATE,
            Set.SEGMENT,
            Set.SEGMENT_2D,
            Set.SHELL,
            Set.SOLID or
            Set.TSHELL
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest+1 in layer in editing panels). If omitted the whole model will be used (Equivalent to
            Highest+1 in editing panels)

        Returns
        -------
        int
            Set label
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NextFreeLabel", model, type, layer)

    def Pick(type, prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg, button_text=Oasys.gRPC.defaultArg):
        """
        Allows the user to pick a set

        Parameters
        ----------
        type : constant
            Type of sets to pick. Can be Set.BEAM,
            Set.BOX, 
            Set.DISCRETE,
            Set.MM_GROUP,
            Set.NODE,
            Set.PART,
            Set.PART_TREE,
            Set.PERI_LAMINATE,
            Set.SEGMENT,
            Set.SEGMENT_2D,
            Set.SHELL,
            Set.SOLID or
            Set.TSHELL
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only sets from that model can be picked.
            If the argument is a Flag then only sets that
            are flagged with limit can be selected.
            If omitted, or None, any sets from any model can be selected.
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
        Set
            Set object (or None if not picked)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Pick", type, prompt, limit, modal, button_text)

    def RenumberAll(model, start, type=Oasys.gRPC.defaultArg):
        """
        Renumbers all of the sets in the model

        Parameters
        ----------
        model : Model
            Model that all sets will be renumbered in
        start : integer
            Start point for renumbering
        type : constant
            Optional. Type of sets to renumber. Can be Set.BEAM,
            Set.BOX
            Set.DISCRETE,
            Set.IGA_EDGE,
            Set.IGA_FACE,
            Set.IGA_POINT_UVW,
            Set.MM_GROUP,
            Set.MODE,
            Set.NODE,
            Set.PART,
            Set.PART_TREE,
            Set.PERI_LAMINATE,
            Set.SEGMENT,
            Set.SEGMENT_2D,
            Set.SHELL,
            Set.SOLID or
            Set.TSHELL.
            If omitted sets of all types will be blanked

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "RenumberAll", model, start, type)

    def RenumberFlagged(model, flag, start, type=Oasys.gRPC.defaultArg):
        """
        Renumbers all of the flagged sets in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged sets will be renumbered in
        flag : Flag
            Flag set on the sets that you want to renumber
        start : integer
            Start point for renumbering
        type : constant
            Optional. Type of sets to renumber. Can be Set.BEAM,
            Set.BOX
            Set.DISCRETE,
            Set.IGA_EDGE,
            Set.IGA_FACE,
            Set.IGA_POINT_UVW,
            Set.MM_GROUP,
            Set.MODE,
            Set.NODE,
            Set.PART,
            Set.PART_TREE,
            Set.PERI_LAMINATE,
            Set.SEGMENT,
            Set.SEGMENT_2D,
            Set.SHELL,
            Set.SOLID or
            Set.TSHELL.
            If omitted sets of all types will be blanked

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "RenumberFlagged", model, flag, start, type)

    def Select(type, flag, prompt, limit=Oasys.gRPC.defaultArg, modal=Oasys.gRPC.defaultArg):
        """
        Allows the user to select sets using standard PRIMER object menus

        Parameters
        ----------
        type : constant
            Type of sets to pick. Can be Set.BEAM,
            Set.BOX
            Set.DISCRETE,
            Set.IGA_EDGE,
            Set.IGA_FACE,
            Set.IGA_POINT_UVW,
            Set.MM_GROUP,
            Set.MODE,
            Set.NODE,
            Set.PART,
            Set.PART_TREE,
            Set.PERI_LAMINATE,
            Set.SEGMENT,
            Set.SEGMENT_2D,
            Set.SHELL,
            Set.SOLID or
            Set.TSHELL
        flag : Flag
            Flag to use when selecting sets
        prompt : string
            Text to display as a prompt to the user
        limit : Model or Flag
            Optional. If the argument is a Model then only sets from that model can be selected.
            If the argument is a Flag then only sets that
            are flagged with limit can be selected (limit should be different to flag).
            If omitted, or None, any sets from any model can be selected
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of items selected or None if menu cancelled
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", type, flag, prompt, limit, modal)

    def SketchFlagged(model, flag, type=Oasys.gRPC.defaultArg, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches all of the flagged sets in the model

        Parameters
        ----------
        model : Model
            Model that all the flagged sets will be sketched in
        flag : Flag
            Flag set on the sets that you want to sketch
        type : constant
            Optional. Type of sets to sketch. Can be Set.BEAM,
            Set.BOX
            Set.DISCRETE,
            Set.MM_GROUP,
            Set.NODE,
            Set.PART,
            Set.PART_TREE,
            Set.PERI_LAMINATE,
            Set.SEGMENT,
            Set.SEGMENT_2D,
            Set.SHELL,
            Set.SOLID or
            Set.TSHELL.
            Set.ALL_TYPES.
            If set, only flagged sets of this type will be sketched. If omitted flagged sets of all types will be sketched
        redraw : boolean
            Optional. If model should be redrawn or not.
            If omitted redraw is true. If you want to do several (un)sketches and only
            redraw after the last one then use false for all redraws apart from the last one.
            Alternatively you can redraw using View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "SketchFlagged", model, flag, type, redraw)

    def UnblankAll(model, type=Oasys.gRPC.defaultArg, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the sets in the model

        Parameters
        ----------
        model : Model
            Model that all sets will be unblanked in
        type : constant
            Optional. Type of sets to unblank. Can be Set.BEAM,
            Set.BOX
            Set.DISCRETE,
            Set.MM_GROUP,
            Set.NODE,
            Set.PART,
            Set.PART_TREE,
            Set.PERI_LAMINATE,
            Set.SEGMENT,
            Set.SEGMENT_2D,
            Set.SHELL,
            Set.SOLID or
            Set.TSHELL.
            Set.ALL_TYPES.
            If omitted sets of all types will be blanked
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
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnblankAll", model, type, redraw)

    def UnblankFlagged(model, flag, type=Oasys.gRPC.defaultArg, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the flagged sets in the model

        Parameters
        ----------
        model : Model
            Model that the flagged sets will be unblanked in
        flag : Flag
            Flag set on the sets that you want to unblank
        type : constant
            Optional. Type of sets to unblank. Can be Set.BEAM,
            Set.BOX
            Set.DISCRETE,
            Set.MM_GROUP,
            Set.NODE,
            Set.PART,
            Set.PART_TREE,
            Set.PERI_LAMINATE,
            Set.SEGMENT,
            Set.SEGMENT_2D,
            Set.SHELL,
            Set.SOLID or
            Set.TSHELL.
            Set.ALL_TYPES.
            If set, only flagged sets of this type will be unblanked. If omitted flagged sets of all types will be unblanked
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
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnblankFlagged", model, flag, type, redraw)

    def UnflagAll(model, flag, type=Oasys.gRPC.defaultArg):
        """
        Unsets a defined flag on all of the sets in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all sets will be unset in
        flag : Flag
            Flag to unset on the sets
        type : constant
            Optional. Type of the set. Can be Set.BEAM,
            Set.BOX
            Set.DISCRETE,
            Set.IGA_EDGE,
            Set.IGA_FACE,
            Set.IGA_POINT_UVW,
            Set.MM_GROUP,
            Set.MODE,
            Set.NODE,
            Set.PART,
            Set.PART_TREE,
            Set.PERI_LAMINATE,
            Set.SEGMENT,
            Set.SEGMENT_2D,
            Set.SHELL,
            Set.SOLID or
            Set.TSHELL

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnflagAll", model, flag, type)

    def UnsketchAll(model, type=Oasys.gRPC.defaultArg, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all sets

        Parameters
        ----------
        model : Model
            Model that all sets will be unsketched in
        type : constant
            Optional. Type of sets to unsketch. Can be Set.BEAM,
            Set.BOX
            Set.DISCRETE,
            Set.MM_GROUP,
            Set.NODE,
            Set.PART,
            Set.PART_TREE,
            Set.PERI_LAMINATE,
            Set.SEGMENT,
            Set.SEGMENT_2D,
            Set.SHELL,
            Set.SOLID or
            Set.TSHELL.
            If omitted sets of all types will be unsketched
        redraw : boolean
            Optional. If model should be redrawn or not after the sets are unsketched.
            If omitted redraw is true. If you want to unsketch several things and only
            redraw after the last one then use false for redraw and call
            View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnsketchAll", model, type, redraw)

    def UnsketchFlagged(model, flag, type=Oasys.gRPC.defaultArg, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all flagged sets

        Parameters
        ----------
        model : Model
            Model that all sets will be unsketched in
        flag : Flag
            Flag set on the sets that you want to unsketch
        type : constant
            Optional. Type of sets to unsketch. Can be Set.BEAM,
            Set.BOX
            Set.DISCRETE,
            Set.MM_GROUP,
            Set.NODE,
            Set.PART,
            Set.PART_TREE,
            Set.PERI_LAMINATE,
            Set.SEGMENT,
            Set.SEGMENT_2D,
            Set.SHELL,
            Set.SOLID or
            Set.TSHELL.
            If omitted sets of all types will be unsketched
        redraw : boolean
            Optional. If model should be redrawn or not after the sets are unsketched.
            If omitted redraw is true. If you want to unsketch several things and only
            redraw after the last one then use false for redraw and call
            View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnsketchFlagged", model, flag, type, redraw)



# Instance methods
    def Add(self, id1, id2=Oasys.gRPC.defaultArg, id3=Oasys.gRPC.defaultArg, id4=Oasys.gRPC.defaultArg):
        """
        Adds an item to the set. This cannot be used for _COLUMN and _GENERAL sets.
        For segment sets four nodes must be given to define a segment to add to the set

        Parameters
        ----------
        id1 : integer
            id of the item to add to the set (normal, _ADD or _ADD_ADVANCED sets) or Start ID (_GENERATE sets)
        id2 : integer
            Optional. type of the item to add to the set [1-7] (_ADD_ADVANCED sets) or End ID (_GENERATE sets)
            (only for SEGMENT, _GENERATE, _GENERATE_INCREMENT and _ADD_ADVANCED sets)
        id3 : integer
            Optional. Increment for _GENERATE_INCREMENT sets, otherwise id of the item to add to the set
            (only for SEGMENT and _GENERATE_INCREMENT sets)
        id4 : integer
            Optional. id of the item to add to the set
            (only for SEGMENT sets)

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Add", id1, id2, id3, id4)

    def AddCollectChild(self, set):
        """
        Adds a child collect set to the set. The child set label will be changed to be the same as the
        parent set and it will become a child. Also see Set.collect_children
        and Set.GetCollectChild

        Parameters
        ----------
        set : Set
            Set to be added as a child collect set

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AddCollectChild", set)

    def AddFlagged(self, flag):
        """
        Adds flagged items to the set. This cannot be used for _GENERAL or _GENERATE sets
        and cannot be used for segment sets

        Parameters
        ----------
        flag : Flag
            Flag for items to add to the set

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AddFlagged", flag)

    def AllItems(self):
        """
        Returns a list containing all of the items in the set, decomposing any complex set definitions as required to give those items.
        For Set.SEGMENT sets, each index in the list is a list containing the segment node IDs.
        For all other set types each index in the list is an item ID

        Returns
        -------
        list
            list
        """
        return Oasys.PRIMER._connection.instanceMethodStream(self.__class__.__name__, self._handle, "AllItems")

    def Blanked(self):
        """
        Checks if the set is blanked or not

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
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Browse", modal)

    def ClearFlag(self, flag):
        """
        Clears a flag on the set

        Parameters
        ----------
        flag : Flag
            Flag to clear on the set

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Contains(self, id):
        """
        Checks if an item is in the set.
        This cannot be used for ADD_ADVANCED, _GENERAL or _GENERATE sets
        and cannot be used for segment sets

        Parameters
        ----------
        id : integer
            id of the item to check

        Returns
        -------
        bool
            True if item is in set, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Contains", id)

    def Copy(self, range=Oasys.gRPC.defaultArg):
        """
        Copies the set

        Parameters
        ----------
        range : boolean
            Optional. If you want to keep the copied item in the range specified for the current include. 
            To set current include, use  Include.MakeCurrentLayer()

        Returns
        -------
        Set
            Set object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", range)

    def Edit(self, modal=Oasys.gRPC.defaultArg):
        """
        Starts an interactive editing panel to edit the set

        Parameters
        ----------
        modal : boolean
            Optional. If this window is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the window will be modal

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Edit", modal)

    def Empty(self):
        """
        Removes all items from the set. This cannot be used for _GENERATE sets
        and cannot be used for segment sets

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Empty")

    def Flagged(self, flag):
        """
        Checks if the set is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to clear on the set

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetCollectChild(self, number):
        """
        Returns a child collect set.
        Also see Set.collect_children
        and Set.AddCollectChild

        Parameters
        ----------
        number : Integer
            The index of the child collect set to return. Note that indices start at 0, not 1

        Returns
        -------
        Set
            Set object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetCollectChild", number)

    def GetGeneralData(self, index):
        """
        Returns a line of data for a GENERAL set

        Parameters
        ----------
        index : Integer
            The index of the GENERAL data to return. Note that indices start at 0, not 1.
            0 <= index < general_lines

        Returns
        -------
        list
            List containing data
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetGeneralData", index)

    def Keyword(self):
        """
        Returns the keyword for this set (\*SET_NODE etc).
        Note that a carriage return is not added.
        See also Set.KeywordCards()

        Returns
        -------
        str
            string containing the keyword
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Keyword")

    def KeywordCards(self):
        """
        Returns the keyword cards for the set.
        Note that a carriage return is not added.
        See also Set.Keyword()

        Returns
        -------
        str
            string containing the cards
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "KeywordCards")

    def Next(self):
        """
        Returns the next set in the model

        Returns
        -------
        Set
            Set object (or None if there are no more sets in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous set in the model

        Returns
        -------
        Set
            Set object (or None if there are no more sets in the model)
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def RebuildCache(self):
        """
        Rebuilds the cache for a set. As sets can be built using complex combinations
        of _GENERAL, _ADD, _INTERSECT options etc PRIMER creates a 'cache' for the set to
        speed up set drawing and usage. During normal interactive use this cache is rebuilt as necessary
        but in JavaScript it is possible for the cache to become out of date (e.g. you change a box
        position in JavaScript that is used by a \*SET_GENERAL). Calling this forces the cache to
        be rebuilt

        Returns
        -------
        None
            No return type
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "RebuildCache")

    def Remove(self, id):
        """
        Removes an item from the set. If the item is not in the set nothing is done.
        This cannot be used for ADD_ADVANCED, _COLUMN, _GENERAL or _GENERATE sets
        and cannot be used for segment sets

        Parameters
        ----------
        id : integer
            id of the item to remove from the set

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Remove", id)

    def RemoveFlagged(self, flag):
        """
        Removes flagged items from the set. This cannot be used for _GENERAL or _GENERATE sets
        and cannot be used for segment sets

        Parameters
        ----------
        flag : Flag
            Flag for items to remove from the set

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "RemoveFlagged", flag)

    def RemoveGeneralData(self, index):
        """
        Removes a line of data from a GENERAL set

        Parameters
        ----------
        index : Integer
            The index of the GENERAL data to remove. Note that indices start at 0, not 1.
            0 <= index < general_lines

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "RemoveGeneralData", index)

    def SetFlag(self, flag):
        """
        Sets a flag on the set

        Parameters
        ----------
        flag : Flag
            Flag to set on the set

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def SetGeneralData(self, index, data):
        """
        Sets a line of data for a GENERAL set

        Parameters
        ----------
        index : Integer
            The index of the GENERAL data to set. Note that indices start at 0, not 1.
            0 <= index <= general_lines
        data : List of data
            List containing GENERAL data to set

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetGeneralData", index, data)

    def Sketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Sketches the set. The set will be sketched until you either call
        Set.Unsketch(),
        Set.UnsketchAll(),
        Model.UnsketchAll(),
        or delete the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the set is sketched.
            If omitted redraw is true. If you want to sketch several sets and only
            redraw after the last one then use false for redraw and call
            View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Sketch", redraw)

    def Spool(self):
        """
        Spools a set, entry by entry. See also Set.StartSpool

        Returns
        -------
        list
            For Set.SEGMENT returns a list containing node IDs, for all other set types returns the ID of the item. Returns 0 if no more items
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Spool")

    def StartSpool(self, raw=Oasys.gRPC.defaultArg):
        """
        Starts a set spooling operation. See also Set.Spool

        Parameters
        ----------
        raw : boolean
            Optional. If true then the raw data from _GENERATE, _ADD and _INTERSECT sets will be returned instead of expanding the
            data ranges or child set contents. If omitted raw will be false

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "StartSpool", raw)

    def Unsketch(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches the set

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the set is unsketched.
            If omitted redraw is true. If you want to unsketch several sets and only
            redraw after the last one then use false for redraw and call
            View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unsketch", redraw)

    def Xrefs(self):
        """
        Returns the cross references for this set

        Returns
        -------
        Xrefs
            Xrefs object
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Xrefs")

