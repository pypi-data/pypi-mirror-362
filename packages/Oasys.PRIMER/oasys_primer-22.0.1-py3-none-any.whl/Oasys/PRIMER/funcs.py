import Oasys.gRPC


def AllocateFlag():
    """
    Allocate a flag for use in the script. See also
    ReturnFlag() and
    Model.PropagateFlag().
    Once allocated the flag is automatically cleared for all the models currently in PRIMER

    Returns
    -------
    int
        Flag
    """
    return Oasys.PRIMER._connection.functionCall("AllocateFlag")


def BatchMode():
    """
    Check if PRIMER is running in "batch mode" (i.e. menus are not active).
    Menus will not be active if PRIMER is started with the -d=tty command line argument.
    Note that this is different to starting PRIMER with the -batch command line argument. When using -batch,
    the menu system is still running, but the main PRIMER window is not shown

    Returns
    -------
    bool
        True if in batch mode, False if not
    """
    return Oasys.PRIMER._connection.functionCall("BatchMode")


def DialogueFunction(name):
    """
    Set the function for dialogue callback. This function
    can be used to make PRIMER return any dialogue messages that are printed.
    This may be useful for you to know if a particular dialogue message has been printed or a particular event has taken place.
    The function will be called with 1 argument which is a string containing the dialogue message.
    To remove the dialogue function use DialogueFunction(None)

    Parameters
    ----------
    name : function
        The name of the function (or None to remove the function)

    Returns
    -------
    None
        No return value
    """
    return Oasys.PRIMER._connection.functionCall("DialogueFunction", name)


def DialogueInput(*command):
    """
    Execute one or more lines of command line dialogue input

    Parameters
    ----------
    *command : string
        Command to execute (as if it had been typed into the dialogue box)
        This argument can be repeated if required.
        Alternatively a single array argument containing the multiple values can be given

    Returns
    -------
    int
        0: No errors/warnings.
        > 0: This number of errors occurred.
        < 0: Absolute number is the number of warnings that occurred
    """
    return Oasys.PRIMER._connection.functionCall("DialogueInput", command)


def DialogueInputNoEcho(*command):
    """
    Execute one or more lines of command line dialogue input with no echo of commands to dialogue box

    Parameters
    ----------
    *command : string
        Command to execute (as if it had been typed into the dialogue box)
        This argument can be repeated if required.
        Alternatively a single array argument containing the multiple values can be given

    Returns
    -------
    int
        0: No errors/warnings.
        > 0: This number of errors occurred.
        < 0: Absolute number is the number of warnings that occurred
    """
    return Oasys.PRIMER._connection.functionCall("DialogueInputNoEcho", command)


def ErrorMessage(string):
    """
    Print an error message to the dialogue box adding a carriage return

    Parameters
    ----------
    string : Any valid javascript type
        The string/item that you want to print

    Returns
    -------
    None
        No return value
    """
    return Oasys.PRIMER._connection.functionCall("ErrorMessage", string)


def Execute(data):
    """
    Execute a program or script outside PRIMER and get the standard output and error streams

    Parameters
    ----------
    data : dict
        Execute data

    Returns
    -------
    dict
        Dict with properties
    """
    return Oasys.PRIMER._connection.functionCall("Execute", data)


def Exit(write_hook_interrupt=Oasys.gRPC.defaultArg):
    """
    Exit script

    Parameters
    ----------
    write_hook_interrupt : boolean
        Optional. If Exit() is called from a write_hook.js script, the first argument will be processed as in the following: 
        If the argument is provided and set to "true", it is used to interrupt the write out of the model, so that 
        the script exits without anything being written out. An argument value of "false" exits the script and allows 
        the model to be written out as normal. An example of this function's use in a Write Hook script can be found at 
        $OA_INSTALL/primer_library/scripts/hooks/example_write_hook.js

    Returns
    -------
    None
        No return value
    """
    return Oasys.PRIMER._connection.functionCall("Exit", write_hook_interrupt)


def FlagsAvailable():
    """
    Number of flags available to be used for AllocateFlag()

    Returns
    -------
    int
        Number of flags available
    """
    return Oasys.PRIMER._connection.functionCall("FlagsAvailable")


def GetCurrentDirectory():
    """
    Get the current working directory

    Returns
    -------
    str
        String containing current working directory
    """
    return Oasys.PRIMER._connection.functionCall("GetCurrentDirectory")


def GetInstallDirectory():
    """
    Get the directory in which executables are installed. This is the OA_INSTALL environment variable,
    or if that is not set the directory in which the current executable is installed. Returns None if not found

    Returns
    -------
    str
        string
    """
    return Oasys.PRIMER._connection.functionCall("GetInstallDirectory")


def GetPreferenceValue(program, name):
    """
    Get the Preference value with the given string in the any of 
    admin ("OA_ADMIN") or install ("OA_INSTALL") or home ("OA_HOME") directory oa_pref

    Parameters
    ----------
    program : string
        The program name string : Valid values are 'All', 'D3PLOT', 'PRIMER', 'REPORTER', 'SHELL',
        'T/HIS'
    name : string
        The preference name string

    Returns
    -------
    str
        : String containing preference value or None if preference string is not present in any oa_pref. Also if none of the above environment variables are not present, then API simply returns null. While returning preference value, locked preference value in admin and then install oa_pref takes precedence over home oa_pref. If preference is not locked in any of these oa_pref, preference in home directory oa_pref is returned
    """
    return Oasys.PRIMER._connection.functionCall("GetPreferenceValue", program, name)


def GetStartInDirectory():
    """
    Get the directory passed to PRIMER by the -start_in command line argument

    Returns
    -------
    str
        String containing start_in directory or None if not set
    """
    return Oasys.PRIMER._connection.functionCall("GetStartInDirectory")


def Getenv(name):
    """
    Get the value of an environment variable

    Parameters
    ----------
    name : string
        The environment variable name

    Returns
    -------
    str
        String containing variable value or None if variable does not exist
    """
    return Oasys.PRIMER._connection.functionCall("Getenv", name)


def Labels(type, state=Oasys.gRPC.defaultArg):
    """
    Set or get labelling of items in PRIMER

    Parameters
    ----------
    type : string
        The type of the item (for a list of types see Appendix I of the
        PRIMER manual). Additionally, to change the visibility of attached or unattached nodes
        you can use the types "ATTACHED_NODE" and "UNATTACHED_NODE"
    state : boolean
        Optional. If it is provided it is used to set the labelling status of entity. "true" to make items labelled and "false" to make them not labelled

    Returns
    -------
    bool
        Boolean
    """
    return Oasys.PRIMER._connection.functionCall("Labels", type, state)


def MacroFunction(name):
    """
    Set the function for macro callback. This function
    can be used to make PRIMER return the macro command that would be recorded
    if macro recording was active for every button press etc.
    This may be useful for you to know if a particular action has been done by the user.
    The function will be called with 1 argument which is a string containing the macro command.
    To remove the macro function use MacroFunction(None)

    Parameters
    ----------
    name : function
        The name of the function (or None to remove a function)

    Returns
    -------
    None
        No return value
    """
    return Oasys.PRIMER._connection.functionCall("MacroFunction", name)


def Message(string):
    """
    Print a message to the dialogue box adding a carriage return

    Parameters
    ----------
    string : Any valid javascript type
        The string/item that you want to print. If '\r' is added to the end of the string then
        instead of automatically adding a carriage return in the dialogue box, the next message will overwrite 
        the current one. This may be useful for giving feedback to the dialogue box when doing an operation

    Returns
    -------
    None
        No return value
    """
    return Oasys.PRIMER._connection.functionCall("Message", string)


def MilliSleep(time):
    """
    Pause execution of the script for time milliseconds. See also
    Sleep()

    Parameters
    ----------
    time : integer
        Number of milliseconds to pause for

    Returns
    -------
    None
        No return value
    """
    return Oasys.PRIMER._connection.functionCall("MilliSleep", time)


def NumberToString(number, width, pref_int=Oasys.gRPC.defaultArg):
    """
    Formats a number to a string with the specified width

    Parameters
    ----------
    number : integer/float
        The number you want to format
    width : integer
        The width of the string you want to format it to (must be less than 80)
    pref_int : boolean
        Optional. By default only integer values inside the single precision 32 bit signed integer limit of approximately
        +/-2e9 are formatted as integers, all other numeric values are formatted as floats. With this argument set to TRUE then
        integer values up to the mantissa precision of a 64 bit float, approximately +/-9e15, will also be formatted as integers

    Returns
    -------
    str
        String containing the number
    """
    return Oasys.PRIMER._connection.functionCall("NumberToString", number, width, pref_int)


def OpenManual(program, page):
    """
    Open the Oasys manuals at a requested page

    Parameters
    ----------
    program : string
        The program manual to open. Can be "primer", "d3plot" or "this"
    page : string
        The page to open in the manual, e.g. "running-this.html"

    Returns
    -------
    bool
        True if successful, False if not
    """
    return Oasys.PRIMER._connection.functionCall("OpenManual", program, page)


def PlayMacro(filename, options=Oasys.gRPC.defaultArg):
    """
    Play a macro in PRIMER

    Parameters
    ----------
    filename : string
        The name of the macro file to play
    options : dict
        Optional. Options specifying how the macro file should be replayed. If omitted the default values below will be used

    Returns
    -------
    bool
        True if an error occured during playback, False otherwise
    """
    return Oasys.PRIMER._connection.functionCall("PlayMacro", filename, options)


def Print(string):
    """
    Print a string to stdout. Note that a carriage return is not added

    Parameters
    ----------
    string : Any valid javascript type
        The string/item that you want to print

    Returns
    -------
    None
        No return value
    """
    return Oasys.PRIMER._connection.functionCall("Print", string)


def Println(string):
    """
    Print a string to stdout adding a carriage return

    Parameters
    ----------
    string : Any valid javascript type
        The string/item that you want to print

    Returns
    -------
    None
        No return value
    """
    return Oasys.PRIMER._connection.functionCall("Println", string)


def Requires(build):
    """
    Checks to see if the build number of PRIMER is high enough to run
    this script. If your script requires features that are only present in builds of
    PRIMER greater than a certain value Require can test this and only run the
    script if the build is high enough

    Parameters
    ----------
    build : integer
        The minimum build number that is required

    Returns
    -------
    None
        No return value (if the build is not high enough the script will terminate)
    """
    return Oasys.PRIMER._connection.functionCall("Requires", build)


def ReturnFlag(flag):
    """
    Return a flag used in the script. See also
    AllocateFlag() and
    Model.PropagateFlag()

    Parameters
    ----------
    flag : Flag
        The flag to return

    Returns
    -------
    None
        No return value
    """
    return Oasys.PRIMER._connection.functionCall("ReturnFlag", flag)


def RunScript(filename, separate=Oasys.gRPC.defaultArg):
    """
    Run a script.
    Note: RunScript is intended to run a 'child' script that will finish before the calling script finishes. Terminating the 
    calling script while child scripts are still running may give undefined behaviour

    Parameters
    ----------
    filename : string
        The name of the script file to run. If the filename is relative then the file
        will be searched for relative to this script. If not found then the script_directory preference
        will be used
    separate : boolean
        Optional. If the script will use separate memory from the current script. If it uses separate
        memory (true) then the 'child' script is completely separated from this script and knows nothing about variables in
        this script. If it does not use separate memory (false) then the 'child' script will have access to all of the
        variables in the current script and hence variables must not clash. It is strongly recommended that you use
        namespaces to stop variable names from clashing.
        If omitted the script will use separate memory

    Returns
    -------
    None
        No return value
    """
    return Oasys.PRIMER._connection.functionCall("RunScript", filename, separate)


def SetCurrentDirectory(directory_path):
    """
    Sets the current working directory

    Parameters
    ----------
    directory_path : string
        Path to the directory you would like to change into

    Returns
    -------
    bool
        True if successful, False if not
    """
    return Oasys.PRIMER._connection.functionCall("SetCurrentDirectory", directory_path)


def SetPreferenceValue(program, name, value, refresh=Oasys.gRPC.defaultArg):
    """
    Save the preference string and its value into oa_pref of home directory.
    If the preference is locked in admin ("OA_ADMIN") or install ("OA_INSTALL") oa_pref, then API is unsuccessful.
    Home directory is defined by environment variable OA_HOME. If OA_HOME is not defined then API is unsuccessful

    Parameters
    ----------
    program : string
        The program name string : Valid values are 'All', 'D3PLOT', 'PRIMER', 'REPORTER', 'SHELL',
        'T/HIS'
    name : string
        The preference name string
    value : string
        The preference value string. If "value" is of zero length, then the option is
        simply removed from the file if present, and no new entry is made.This argument cannot be None
    refresh : boolean
        Optional. If the saved preference should be refreshed. If omitted, the preference will NOT be refreshed.
        This argument is currently only available in PRIMER JS API and ignored in D3PLOT and T/HIS

    Returns
    -------
    int
        An integer. Returns 0 if the preference is saved succesfully or 1 if unsuccessful
    """
    return Oasys.PRIMER._connection.functionCall("SetPreferenceValue", program, name, value, refresh)


def Sleep(time):
    """
    Pause execution of the script for time seconds. See also
    MilliSleep()

    Parameters
    ----------
    time : integer
        Number of seconds to pause for

    Returns
    -------
    None
        No return value
    """
    return Oasys.PRIMER._connection.functionCall("Sleep", time)


def System(string):
    """
    Do a system command outside PRIMER. To run an external command and get the output then please use
    Execute() instead

    Parameters
    ----------
    string : Any valid javascript type
        The system command that you want to do

    Returns
    -------
    int
        integer (probably zero if command successful but is implementation-dependant)
    """
    return Oasys.PRIMER._connection.functionCall("System", string)


def Unix():
    """
    Test whether script is running on a Unix/Linux operating system. See also
    Windows()

    Returns
    -------
    bool
        True if Unix/Linux, False if not
    """
    return Oasys.PRIMER._connection.functionCall("Unix")


def Use(filename):
    """
    Use script from a separate file

    Parameters
    ----------
    filename : string
        Use allows you to include a script from a separate file. This may be useful if
        your script is very large and you want to split it up to help with maintenance. Alternatively
        you may have a 'library' of common functions which you always want to include in your scripts.
        Including the 'library' with Use means that any changes only have to be done in one place.
        PRIMER will look for the file in the same directory as the main script. If that fails then
        it will look in $OA_INSTALL/primer_library/scripts directory and the script directory specified by
        the primer\*script_directory preference.
        Note that the file is included when the script is compiled, NOT at runtime

    Returns
    -------
    None
        No return value
    """
    return Oasys.PRIMER._connection.functionCall("Use", filename)


def UuidCreate():
    """
    Create a UUID (Universally unique ID)

    Returns
    -------
    str
        string
    """
    return Oasys.PRIMER._connection.functionCall("UuidCreate")


def Visibility(type, state=Oasys.gRPC.defaultArg):
    """
    Set or get visibility of items in PRIMER

    Parameters
    ----------
    type : string
        The type of the item (for a list of types see Appendix I of the
        PRIMER manual). Additionally, to change the visibility of attached or unattached nodes
        you can use the types "ATTACHED_NODE" and "UNATTACHED_NODE"
    state : boolean
        Optional. If it is provided it is used to set the visibility. "true" to make items visible and "false" to make them not visible

    Returns
    -------
    bool
        Boolean
    """
    return Oasys.PRIMER._connection.functionCall("Visibility", type, state)


def WarningMessage(string):
    """
    Print a warning message to the dialogue box adding a carriage return

    Parameters
    ----------
    string : Any valid javascript type
        The string/item that you want to print

    Returns
    -------
    None
        No return value
    """
    return Oasys.PRIMER._connection.functionCall("WarningMessage", string)


def Windows():
    """
    Test whether script is running on a Windows operating system. See also
    Unix()

    Returns
    -------
    bool
        True if Windows, False if not
    """
    return Oasys.PRIMER._connection.functionCall("Windows")
