import Oasys.gRPC


# Metaclass for static properties and constants
class PartType(type):

    def __getattr__(cls, name):

        raise AttributeError("Part class attribute '{}' does not exist".format(name))


class Part(Oasys.gRPC.OasysItem, metaclass=PartType):
    _rprops = {'composite', 'data', 'elementType', 'include', 'index', 'label', 'material', 'model', 'nip', 'title', 'type'}


    def __del__(self):
        if not Oasys.D3PLOT._connection:
            return

        if self._handle is None:
            return

        Oasys.D3PLOT._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
# If constructor for an item fails in program, then _handle will not be set and when
# __del__ is called to return the object we will call this to get the (undefined) value
        if name == "_handle":
            return None

# If one of the read only properties we define then get it
        if name in Part._rprops:
            return Oasys.D3PLOT._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("Part instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the read only properties we define then error
        if name in Part._rprops:
            raise AttributeError("Cannot set read-only Part instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Static methods
    def BlankAll(window, model):
        """
        Blanks all of the parts in the model

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to blank the parts in
        model : Model
            Model that all the parts will be blanked in

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "BlankAll", window, model)

    def BlankFlagged(window, model, flag):
        """
        Blanks all of the parts in the model flagged with a defined flag

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to blank the parts in
        model : Model
            Model that the flagged parts will be blanked in
        flag : Flag
            Flag (see AllocateFlag) set on the parts to blank

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "BlankFlagged", window, model, flag)

    def First(model):
        """
        Returns the first part in the model (or None if there are no parts in the model)

        Parameters
        ----------
        model : Model
            Model to get first part in

        Returns
        -------
        Part
            Part object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "First", model)

    def FlagAll(model, flag):
        """
        Flags all of the parts in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all the parts will be flagged in
        flag : Flag
            Flag (see AllocateFlag) to set on the parts

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Part objects or properties for all of the parts in the model.
        If the optional property argument is not given then a list of Part objects is returned.
        If the property argument is given, that property value for each part is returned in the list
        instead of a Part object

        Parameters
        ----------
        model : Model
            Model that all the parts are in
        property : string
            Optional. Name for property to get for all parts in the model

        Returns
        -------
        list
            List of :py:class:`Part <Part>` objects or properties
        """
        return Oasys.D3PLOT._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Gets all of the parts in the model flagged with a defined flag.
        If the optional property argument is not given then a list of Part objects is returned.
        If the property argument is given, that property value for each part is returned in the list
        instead of a Part object

        Parameters
        ----------
        model : Model
            Model that the flagged parts are in
        flag : Flag
            Flag (see AllocateFlag) set on the parts to get
        property : string
            Optional. Name for property to get for all flagged parts in the model

        Returns
        -------
        list
            List of :py:class:`Part <Part>` objects or properties
        """
        return Oasys.D3PLOT._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, label):
        """
        Returns the Part object for part in model with label (or None if it does not exist)

        Parameters
        ----------
        model : Model
            Model to get part in
        label : integer
            The Ansys LS-DYNA label for the part in the model

        Returns
        -------
        Part
            Part object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "GetFromID", model, label)

    def GetFromIndex(model, index):
        """
        Returns the Part object for part in model with index (or None if it does not exist)

        Parameters
        ----------
        model : Model
            Model to get part in
        index : integer
            The D3PLOT internal index in the model for part, starting at 0

        Returns
        -------
        Part
            Part object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "GetFromIndex", model, index)

    def GetMultipleData(component, items, options=Oasys.gRPC.defaultArg):
        """
        Returns the value for a data component for multiple parts. For each part a local property called data will be created
        containing a number if a scalar component, or a list if a vector or tensor component (or None if the value cannot be calculated).
        The data is also returned as an object.
        Also see GetData

        Parameters
        ----------
        component : constant
            Component constant to get data for
        items : list
            List of Part objects to get the data for.
            All of the parts must be in the same model
        options : dict
            Optional. Dictionary containing options for getting data. Can be any of:

        Returns
        -------
        dictionary
            Dictionary containing the data. A property is created in the dictionary for each part with the label. The value of the property is a number if a scalar component or an array if a vector or tensor component (or None if the value cannot be calculated)
        """
        return Oasys.D3PLOT._connection.classMethodStream(__class__.__name__, "GetMultipleData", component, items, options)

    def Last(model):
        """
        Returns the last part in the model (or None if there are no parts in the model)

        Parameters
        ----------
        model : Model
            Model to get last part in

        Returns
        -------
        Part
            Part object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Last", model)

    def Pick():
        """
        Allows the user to pick a part from the screen

        Returns
        -------
        Part
            Part object or None if cancelled
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Pick")

    def Select(flag):
        """
        Selects parts using an object menu

        Parameters
        ----------
        flag : Flag
            Flag (see AllocateFlag) to use when selecting parts

        Returns
        -------
        integer
            The number of parts selected or None if menu cancelled
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Select", flag)

    def Total(model):
        """
        Returns the total number of parts in the model

        Parameters
        ----------
        model : Model
            Model to get total in

        Returns
        -------
        integer
            The number of parts
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Total", model)

    def UnblankAll(window, model):
        """
        Unblanks all of the parts in the model

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to unblank the parts in
        model : Model
            Model that all the parts will be unblanked in

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "UnblankAll", window, model)

    def UnblankFlagged(window, model, flag):
        """
        Unblanks all of the parts in the model flagged with a defined flag

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to unblank the parts in
        model : Model
            Model that the flagged parts will be unblanked in
        flag : Flag
            Flag (see AllocateFlag) set on the parts to unblank

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "UnblankFlagged", window, model, flag)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the parts in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all parts will be unset in
        flag : Flag
            Flag (see AllocateFlag) to unset on the parts

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)



# Instance methods
    def Blank(self, window):
        """
        Blanks the part in a graphics window

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to blank the part in

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank", window)

    def Blanked(self, window):
        """
        Checks if the part is blanked in a graphics window or not

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) in which to check if the part is blanked

        Returns
        -------
        boolean
            True if blanked, False if not
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Blanked", window)

    def ClearFlag(self, flag):
        """
        Clears a flag on a part

        Parameters
        ----------
        flag : Flag
            Flag (see AllocateFlag) to clear on the part

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Elements(self):
        """
        Returns a list containing the elements in the part

        Returns
        -------
        array
            Array of element objects
        """
        return Oasys.D3PLOT._connection.instanceMethodStream(self.__class__.__name__, self._handle, "Elements")

    def Flagged(self, flag):
        """
        Checks if the part is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag (see AllocateFlag) to test on the part

        Returns
        -------
        boolean
            True if flagged, False if not
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetCompositeData(self, ipt):
        """
        Returns the composite data for an integration point in \*PART_COMPOSITE

        Parameters
        ----------
        ipt : integer
            The integration point you want the data for. Note that integration points start at 0, not 1

        Returns
        -------
        list
            A list containing the material id and thickness values
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "GetCompositeData", ipt)

    def GetData(self, component, options=Oasys.gRPC.defaultArg):
        """
        Returns the value for a data component.
        Also see GetMultipleData

        Parameters
        ----------
        component : constant
            Component constant to get data for
        options : dict
            Optional. Dictionary containing options for getting data. Can be any of:

        Returns
        -------
        float|array
            Number if a scalar component, array if a vector or tensor component (or None if the value cannot be calculated because it's not available in the model).<br> If requesting an invalid component it will throw an error (e.g. Component.AREA of a node).
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "GetData", component, options)

    def Next(self):
        """
        Returns the next part in the model (or None if there is not one)

        Returns
        -------
        Part
            Part object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous part in the model (or None if there is not one)

        Returns
        -------
        Part
            Part object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on a part

        Parameters
        ----------
        flag : Flag
            Flag (see AllocateFlag) to set on the part

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Unblank(self, window):
        """
        Unblanks the part in a graphics window

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to unblank the part in

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank", window)

