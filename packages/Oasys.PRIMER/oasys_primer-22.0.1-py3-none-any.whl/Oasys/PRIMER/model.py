import Oasys.gRPC


# Metaclass for static properties and constants
class ModelType(type):
    _consts = {'ABAQUS', 'CENTRE_AT_COFG', 'COMPRESS_KEEP', 'COMPRESS_OFF', 'COMPRESS_ON', 'DISCARD_PRIMARY_CLASH', 'DISCARD_SECONDARY_CLASH', 'GLOBAL_AXES', 'IGES', 'IGNORE_CLASH', 'INCREASE_PRIMARY_ALWAYS', 'INCREASE_PRIMARY_CLASH', 'INCREASE_SECONDARY_ALWAYS', 'INCREASE_SECONDARY_CLASH', 'INDIVIDUAL_GZIP', 'INDIVIDUAL_ZIP', 'KEEP_ORIGINAL', 'LOCAL_AXES', 'LSDYNA', 'MOVE_CLASH_UP', 'NASTRAN', 'PACKAGED_ZIP', 'PRINCIPAL_AXES', 'RADIOSS', 'REMOVE_FROM_SETS', 'REMOVE_INCLUDE_ONLY', 'REMOVE_JUNIOR', 'RENUMBER_TO_FREE', 'SHIFT_ALL_UP', 'USER_DEFINED_CENTRE', 'WRITE_DIALOGUE', 'WRITE_INCLUDE_TREE', 'WRITE_MODEL', 'WRITE_SELECT_INCLUDES'}
    _rprops = {'highest'}

    def __getattr__(cls, name):
        if name in ModelType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)
        if name in ModelType._rprops:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("Model class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the read only properties we define then error
        if name in ModelType._rprops:
            raise AttributeError("Cannot set read-only Model class attribute '{}'".format(name))

# If one of the constants we define then error
        if name in ModelType._consts:
            raise AttributeError("Cannot set Model class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class Model(Oasys.gRPC.OasysItem, metaclass=ModelType):
    _props = {'comments', 'id', 'layer', 'num', 'number', 'project', 'readlog', 'stage', 'title', 'visible'}
    _rprops = {'binary', 'compress', 'compressMode', 'control', 'damping', 'database', 'fileStartAscii', 'filename', 'loadBody', 'masterAscii', 'path'}


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
        if name in Model._props:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in Model._rprops:
            return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("Model instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Model._props:
            Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in Model._rprops:
            raise AttributeError("Cannot set read-only Model instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, number=Oasys.gRPC.defaultArg):
        handle = Oasys.PRIMER._connection.constructor(self.__class__.__name__, number)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new model in PRIMER

        Parameters
        ----------
        number : integer
            Optional. Model number to create. If omitted the next free model number will be used

        Returns
        -------
        Model
            Model object
        """


# Static methods
    def BlankAll():
        """
        Blanks all models

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "BlankAll")

    def DeleteAll():
        """
        Deletes all existing models from PRIMER

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "DeleteAll")

    def First():
        """
        Returns the Model object for the first model in PRIMER
        (or None if there are no models)

        Returns
        -------
        Model
            Model object
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "First")

    def FirstFreeItemLabel(type, layer=Oasys.gRPC.defaultArg):
        """
        Returns the first free label for an item type in the model.
        Also see Model.LastFreeItemLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        type : string
            The type of the item (for a list of types see Appendix I of the
            PRIMER manual)
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            First free in layer in editing panels). If omitted the whole model will be used (Equivalent to
            First free in editing panels)

        Returns
        -------
        int
            integer
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "FirstFreeItemLabel", type, layer)

    def GetAll():
        """
        Returns a list of Model objects for all the models in PRIMER

        Returns
        -------
        list
            List of Model objects
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetAll")

    def GetFromID(model_number):
        """
        Returns the Model object for a model ID or None if model does not exist

        Parameters
        ----------
        model_number : integer
            number of the model you want the Model object for

        Returns
        -------
        Model
            Model object
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "GetFromID", model_number)

    def Last():
        """
        Returns the Model object for the last model in PRIMER
        (or None if there are no models)

        Returns
        -------
        Model
            Model object
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Last")

    def LastFreeItemLabel(type, layer=Oasys.gRPC.defaultArg):
        """
        Returns the last free label for an item type in the model.
        Also see Model.FirstFreeItemLabel() and
        Model.NextFreeItemLabel()

        Parameters
        ----------
        type : string
            The type of the item (for a list of types see Appendix I of the
            PRIMER manual)
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest free in layer in editing panels). If omitted the whole model will be used

        Returns
        -------
        int
            integer
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "LastFreeItemLabel", type, layer)

    def Merge(primary_model, secondary_model, option_to_fix_clashes=Oasys.gRPC.defaultArg, merge_nodes_flag=Oasys.gRPC.defaultArg, dist=Oasys.gRPC.defaultArg, label=Oasys.gRPC.defaultArg, position=Oasys.gRPC.defaultArg):
        """
        Merge 2 models together to make a new model

        Parameters
        ----------
        primary_model : Model
            Primary Model for merge
        secondary_model : Model
            Secondary Model for merge
        option_to_fix_clashes : constant
            Optional. Type of fix. Can be Model.INCREASE_SECONDARY_ALWAYS,
            Model.INCREASE_SECONDARY_CLASH,
            Model.DISCARD_SECONDARY_CLASH,
            Model.INCREASE_PRIMARY_ALWAYS,
            Model.INCREASE_PRIMARY_CLASH or
            Model.DISCARD_PRIMARY_CLASH
        merge_nodes_flag : boolean
            Optional. If this flag is set to true, PRIMER will merge nodes after the model merge
        dist : float
            Optional. Nodes closer than dist will be potentially merged
        label : integer
            Optional. Label to keep after merge. If > 0 then highest label kept.
            If <= 0 then lowest kept.
            If omitted the lowest label will be kept
        position : integer
            Optional. Position to merge at. If > 0 then merged at highest label position.
            If < 0 then merged at lowest label position.
            If 0 then merged at midpoint.
            If omitted the merge will be done at the lowest label

        Returns
        -------
        Model
            Model object (or None if the merge is unsuccessful)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Merge", primary_model, secondary_model, option_to_fix_clashes, merge_nodes_flag, dist, label, position)

    def NextFreeItemLabel(type, layer=Oasys.gRPC.defaultArg):
        """
        Returns the next free label for an item type in the model.
        Also see Model.FirstFreeItemLabel() and
        Model.LastFreeItemLabel()

        Parameters
        ----------
        type : string
            The type of the item (for a list of types see Appendix I of the
            PRIMER manual)
        layer : Include number
            Optional. Include file (0 for the main file) to search for labels in (Equivalent to
            Highest+1 in layer in editing panels). If omitted the whole model will be used (Equivalent to
            Highest+1 in editing panels)

        Returns
        -------
        int
            integer
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "NextFreeItemLabel", type, layer)

    def Read(filename, filetype=Oasys.gRPC.defaultArg, number=Oasys.gRPC.defaultArg):
        """
        Reads a file into the first free model in PRIMER

        Parameters
        ----------
        filename : string
            Filename you want to read
        filetype : constant
            Optional. Filetype you want to read. Can be Model.LSDYNA,
            Model.ABAQUS,
            Model.NASTRAN,
            Model.RADIOSS or
            Model.IGES.
            If omitted the file is assumed to be a DYNA3D file.
            For Model.NASTRAN there are options that change how the model is read.
            See Options for details
        number : integer
            Optional. Model number to read file into. If omitted the next free model number will be used

        Returns
        -------
        Model
            Model object (or None if error)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Read", filename, filetype, number)

    def Select(prompt, modal=Oasys.gRPC.defaultArg):
        """
        Allows the user to select a model using standard PRIMER object menus.
        If there are no models in memory then Select returns None. If only one model is present
        then the model object is returned. If there is more than one model in memory then an
        object menu is mapped allowing the user to choose a model

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in PRIMER
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        Model
            Model object (or None if no models present)
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Select", prompt, modal)

    def Total():
        """
        Returns the total number of models

        Returns
        -------
        int
            integer
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "Total")

    def UnblankAll():
        """
        Unblanks all models

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "UnblankAll")



# Instance methods
    def AreaVolumeFlagged(self, flag):
        """
        Calculates the Area/Volume of the selected items.
        Note: The area calculation is based only on shell elements, and the volume calculation is based only on solid elements

        Parameters
        ----------
        flag : Flag
            Flag set on entities you wish to calculate area/volume for

        Returns
        -------
        dict
            Dict with properties
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "AreaVolumeFlagged", flag)

    def Attached(self, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Finds attached items to flagged items. The attached items are flagged with the same flag

        Parameters
        ----------
        flag : Flag
            Flag set on items that you want to find attached to
        redraw : boolean
            Optional. If true, the display will be updated to display only the original flagged items and the attached items

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Attached", flag, redraw)

    def Autofix(self):
        """
        Autofix option does a model check and autofixes all the fixable errors in the model

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Autofix")

    def Blank(self):
        """
        Blanks a model in PRIMER

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank")

    def BlankFlagged(self, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Blanks all of the flagged items in the model

        Parameters
        ----------
        flag : Flag
            Flag set on items that you want to blank
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
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "BlankFlagged", flag, redraw)

    def CentreOfGravity(self):
        """
        Returns the centre of gravity for a model

        Returns
        -------
        list
            A list containing the x, y and z coordinates for the CofG
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "CentreOfGravity")

    def Check(self, filename, detailed=Oasys.gRPC.defaultArg, json=Oasys.gRPC.defaultArg, include=Oasys.gRPC.defaultArg):
        """
        Checks a model, writing any errors to file

        Parameters
        ----------
        filename : string
            Name of file to write errors to
        detailed : boolean
            Optional. If set to "true", detailed error messages are given
        json : boolean
            Optional. If set, output in filename will be written in JSON format. If omitted json will be set to false.
            If JSON format is written then detailed will automatically be set.
            Note that when writing JSON format the labels produced can be strings instead of integers in some rare cases.
            If you are writing a script to read a JSON file, it must be able to cope with this.
            Specifically if the item is a character label the label will be a string. For child collect sets the label
            will be a string of the format 'X_Y' where X is the parent set label and Y will be the child set number (1, 2, 3 ...).
            In this case use Set.GetCollectChild() to get the object
        include : boolean
            Optional. If set, error messages will be written in include by include layout. 
            This option is not applicable if JSON is set

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Check", filename, detailed, json, include)

    def ClearFlag(self, flag):
        """
        Clears the flagging for a model in PRIMER. See also
        Model.PropagateFlag(),
        Model.SetFlag(),
        global.AllocateFlag() and
        global.ReturnFlag()

        Parameters
        ----------
        flag : Flag
            Flag to clear

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Copy(self, update=Oasys.gRPC.defaultArg):
        """
        Copy model to the next free model in PRIMER

        Parameters
        ----------
        update : boolean
            Optional. If the graphics should be updated after the model is copied.
            If omitted update will be set to false

        Returns
        -------
        Model
            Model object for new model
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Copy", update)

    def CopyFlagged(self, flag, update=Oasys.gRPC.defaultArg):
        """
        Copy flagged items in a model to the next free model in PRIMER

        Parameters
        ----------
        flag : Flag
            Flag set on items that you want to copy
        update : boolean
            Optional. If the graphics should be updated after the model is copied.
            If omitted update will be set to false

        Returns
        -------
        Model
            Model object for new model
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "CopyFlagged", flag, update)

    def Delete(self):
        """
        Deletes a model in PRIMER
        Do not use the Model object after calling this method

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Delete")

    def DeleteFlagged(self, flag, recursive=Oasys.gRPC.defaultArg):
        """
        Deletes all of the flagged items in the model. Note that this may not actually
        delete all of the items. For example if a node is flagged but the node is used in a shell
        which is not flagged then the node will not be deleted

        Parameters
        ----------
        flag : Flag
            Flag set on items that you want to delete
        recursive : boolean
            Optional. If deletion is recursive (for example, if a shell is deleted with recursion on the shell nodes will be deleted if possible).
            If omitted recursive will be set to true

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "DeleteFlagged", flag, recursive)

    def DeleteInclude(self, _py_class_include___label, method=Oasys.gRPC.defaultArg, force=Oasys.gRPC.defaultArg):
        """
        Tries to delete an include file from the model. Note that this may not actually
        delete the include file. For example if some of the items in the include file are required
        by other things in different includes then the include file will not be deleted

        Parameters
        ----------
        _py_class_include___label : integer
            label of include file that you want to delete
        method : constant
            Optional. Method for deleting items. Must be Model.REMOVE_FROM_SETS (default),
            Model.REMOVE_JUNIOR or
            Model.REMOVE_INCLUDE_ONLY.
            Model.REMOVE_FROM_SETS will only delete items within
            the include selected but may remove items from sets in other includes.
            Model.REMOVE_JUNIOR may delete items in other includes
            - this will happen if they 'belong' to items in this include and are considered 'junior'
            Model.REMOVE_INCLUDE_ONLY does the same as
            Model.REMOVE_FROM_SETS but will not remove
            items from sets in other includes
        force : boolean
            Optional. Forcible deletion option (for example, a node is deleted even when it is referenced by a shell
            which is not deleted). This will remove the include file (not just the contents)
            from the model. If this argument is omitted, force will be set to false

        Returns
        -------
        bool
            True if include successfully deleted, False otherwise
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "DeleteInclude", _py_class_include___label, method, force)

    def FlagDuplicate(self, flag):
        """
        Flag all nodes referenced in two different includes

        Parameters
        ----------
        flag : Flag
            Flag which will be used to flag the "duplicate" nodes

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "FlagDuplicate", flag)

    def Flagged(self, flag):
        """
        Checks if the model is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag to test on the model

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetIncludeTransformOffsets(self):
        """
        Looks at all of the items in the model and determines values
        for IDNOFF, IDEOFF, IDPOFF etc that could be used with
        Model.ImportIncludeTransform
        to guarantee that there would not be any clashes with existing items in the model

        Returns
        -------
        dict
            Dict with properties
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetIncludeTransformOffsets")

    def Hide(self):
        """
        Hides a model in PRIMER

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Hide")

    def Import(self, filename):
        """
        Imports a file into model m. The model can already contain items. However, note that
        if the file cannot be imported because of a label clash or other problem PRIMER may delete the model
        and the script will terminate. Note prior to v17 of PRIMER imported data would always be imported
        to the master model, irrespective of the current layer. From v17 onwards this has been corrected and
        the current layer is used to determine the destination of imported data

        Parameters
        ----------
        filename : string
            Filename of the Ansys LS-DYNA keyword file you want to import

        Returns
        -------
        int
            0: No errors/warnings.
            > 0: This number of errors occurred.
            < 0: Absolute number is the number of warnings that occurred
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Import", filename)

    def ImportInclude(self, source, target=Oasys.gRPC.defaultArg):
        """
        Imports a keyword file or an Include object from different model as a new include or into an existing include file for model m. The labels of any items
        in the imported include contents that clash with existing labels will automatically be renumbered with one exception. The behaviour for \*SET_COLLECT
        cards can be controlled with Options.merge_set_collect

        Parameters
        ----------
        source : String OR Include Object
            Can either be a Filename of the Ansys LS-DYNA include file you want to import, OR Include object of another model you want to import
        target : Include Object
            Optional. Include file object of current model if the Import has to be done in an existing include.
            If not using this argument the contents of the source will be imported as a new include.
            If using this argument the contents of the source will NOT be imported as a new include, they will be merged with the target include.
            Note: Target cannot be include number 0 (it must be an include file, not the master file)

        Returns
        -------
        Include
            Include object for include file
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ImportInclude", source, target)

    def ImportIncludeTransform(self, filename, idnoff, ideoff, idpoff, idmoff, idsoff, idfoff, iddoff, idroff):
        """
        Imports a file as an include transform file for model m. The labels of any items
        in the include file will be renumbered by idnoff, ideoff etc

        Parameters
        ----------
        filename : string
            Filename of the Ansys LS-DYNA include file you want to import
        idnoff : integer
            Offset for nodes in the file
        ideoff : integer
            Offset for elements in the file
        idpoff : integer
            Offset for parts in the file
        idmoff : integer
            Offset for materials in the file
        idsoff : integer
            Offset for sets in the file
        idfoff : integer
            Offset for functions and tables in the file
        iddoff : integer
            Offset for defines in the file
        idroff : integer
            Offset for other labels in the file

        Returns
        -------
        Include
            Include object if successful, None if not
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "ImportIncludeTransform", filename, idnoff, ideoff, idpoff, idmoff, idsoff, idfoff, iddoff, idroff)

    def Mass(self):
        """
        Returns the mass for a model

        Returns
        -------
        float
            float
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Mass")

    def MassPropCalc(self, flag):
        """
        Calculates the Mass, CoG, and Intertia Tensor of the flagged items
        and returns an object with the above properties. See Properties for
        mass properties calculation under options class to configure inclusion
        of lumped mass, etc

        Parameters
        ----------
        flag : Flag
            Calculate mass propetries of flagged items

        Returns
        -------
        dict
            Dict with properties
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "MassPropCalc", flag)

    def MergeNodes(self, flag, dist, label=Oasys.gRPC.defaultArg, position=Oasys.gRPC.defaultArg):
        """
        Attempts to merge nodes on items flagged with flag for this model in PRIMER.
        Merging nodes on \*AIRBAG_SHELL_REFERENCE_GEOMETRY can be controlled by using
        Options.node_replace_asrg.
        Also see Node.Merge()

        Parameters
        ----------
        flag : Flag
            Flag set on items to merge nodes
        dist : float
            Nodes closer than dist will be potentially merged
        label : integer
            Optional. Label to keep after merge. If > 0 then highest label kept.
            If <= 0 then lowest kept.
            If omitted the lowest label will be kept
        position : integer
            Optional. Position to merge at. If > 0 then merged at highest label position.
            If < 0 then merged at lowest label position.
            If 0 then merged at midpoint.
            If omitted the merge will be done at the lowest label

        Returns
        -------
        int
            The number of nodes merged
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "MergeNodes", flag, dist, label, position)

    def PopulateInitialVelocities(self):
        """
        Populate the initial velocity field (nvels) for all nodes of the model

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "PopulateInitialVelocities")

    def PropagateFlag(self, flag):
        """
        Propagates the flagging for a model in PRIMER. For example if a part in the model is
        flagged, this will flag the elements in the part, the nodes on those elements... See also
        Model.ClearFlag(),
        Model.SetFlag(),
        global.AllocateFlag() and
        global.ReturnFlag()

        Parameters
        ----------
        flag : Flag
            Flag to propagate

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "PropagateFlag", flag)

    def RenumberAll(self, start):
        """
        Renumbers all of the items in the model

        Parameters
        ----------
        start : integer
            Start point for renumbering

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "RenumberAll", start)

    def RenumberFlagged(self, flag, start, mode=Oasys.gRPC.defaultArg):
        """
        Renumbers all of the flagged items in the model

        Parameters
        ----------
        flag : Flag
            Flag set on items that you want to renumber
        start : integer
            Start point for renumbering
        mode : constant
            Optional. Renumber mode. Can be Model.IGNORE_CLASH,
            Model.MOVE_CLASH_UP,
            Model.SHIFT_ALL_UP, or
            Model.RENUMBER_TO_FREE (default),

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "RenumberFlagged", flag, start, mode)

    def SetColour(self, colour):
        """
        Sets the colour of the model

        Parameters
        ----------
        colour : colour from Colour class
            The colour you want to set the model to

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetColour", colour)

    def SetFlag(self, flag):
        """
        Sets the flagging for a model in PRIMER. See also
        Model.PropagateFlag(),
        Model.ClearFlag(),
        global.AllocateFlag() and
        global.ReturnFlag()

        Parameters
        ----------
        flag : Flag
            Flag to set

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Show(self):
        """
        Shows a model in PRIMER

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Show")

    def Unblank(self):
        """
        Unblanks a model in PRIMER

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank")

    def UnblankFlagged(self, flag, redraw=Oasys.gRPC.defaultArg):
        """
        Unblanks all of the flagged items in the model

        Parameters
        ----------
        flag : Flag
            Flag set on items that you want to unblank
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
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "UnblankFlagged", flag, redraw)

    def UnsketchAll(self, redraw=Oasys.gRPC.defaultArg):
        """
        Unsketches all of the sketched items in the model

        Parameters
        ----------
        redraw : boolean
            Optional. If model should be redrawn or not after the items are unsketched.
            If omitted redraw is true. If you want to unsketch several things and only
            redraw after the last one then use false for redraw and call
            View.Redraw()

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "UnsketchAll", redraw)

    def UpdateGraphics(self):
        """
        Updates the graphics for a model in PRIMER

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "UpdateGraphics")

    def UsesLargeLabels(self):
        """
        Checks to see if a model uses large labels

        Returns
        -------
        bool
            logical, True if model uses large labels, False otherwise
        """
        return Oasys.PRIMER._connection.instanceMethod(self.__class__.__name__, self._handle, "UsesLargeLabels")

    def Write(self, filename, options=Oasys.gRPC.defaultArg):
        """
        Writes a model in PRIMER to file

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

