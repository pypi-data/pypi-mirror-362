import Oasys.gRPC


# Metaclass for static properties and constants
class SetSolidType(type):

    def __getattr__(cls, name):

        raise AttributeError("SetSolid class attribute '{}' does not exist".format(name))


class SetSolid(Oasys.gRPC.OasysItem, metaclass=SetSolidType):
    _rprops = {'include', 'index', 'label', 'model', 'title', 'total', 'type'}


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
        if name in SetSolid._rprops:
            return Oasys.D3PLOT._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("SetSolid instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the read only properties we define then error
        if name in SetSolid._rprops:
            raise AttributeError("Cannot set read-only SetSolid instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Static methods
    def First(model):
        """
        Returns the first solid set in the model (or None if there are no solid sets in the model)

        Parameters
        ----------
        model : Model
            Model to get first solid set in

        Returns
        -------
        SetSolid
            SetSolid object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "First", model)

    def FlagAll(model, flag):
        """
        Flags all of the solid sets in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all the solid sets will be flagged in
        flag : Flag
            Flag (see AllocateFlag) to set on the solid sets

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of SetSolid objects or properties for all of the solid sets in the model.
        If the optional property argument is not given then a list of SetSolid objects is returned.
        If the property argument is given, that property value for each solid set is returned in the list
        instead of a SetSolid object

        Parameters
        ----------
        model : Model
            Model that all the solid sets are in
        property : string
            Optional. Name for property to get for all solid sets in the model

        Returns
        -------
        list
            List of :py:class:`SetSolid <SetSolid>` objects or properties
        """
        return Oasys.D3PLOT._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Gets all of the solid sets in the model flagged with a defined flag.
        If the optional property argument is not given then a list of SetSolid objects is returned.
        If the property argument is given, that property value for each solid set is returned in the list
        instead of a SetSolid object

        Parameters
        ----------
        model : Model
            Model that the flagged solid sets are in
        flag : Flag
            Flag (see AllocateFlag) set on the solid sets to get
        property : string
            Optional. Name for property to get for all flagged solid sets in the model

        Returns
        -------
        list
            List of :py:class:`SetSolid <SetSolid>` objects or properties
        """
        return Oasys.D3PLOT._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, label):
        """
        Returns the SetSolid object for solid set in model with label (or None if it does not exist)

        Parameters
        ----------
        model : Model
            Model to get solid set in
        label : integer
            The Ansys LS-DYNA label for the solid set in the model

        Returns
        -------
        SetSolid
            SetSolid object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "GetFromID", model, label)

    def GetFromIndex(model, index):
        """
        Returns the SetSolid object for solid set in model with index (or None if it does not exist)

        Parameters
        ----------
        model : Model
            Model to get solid set in
        index : integer
            The D3PLOT internal index in the model for solid set, starting at 0

        Returns
        -------
        SetSolid
            SetSolid object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "GetFromIndex", model, index)

    def Last(model):
        """
        Returns the last solid set in the model (or None if there are no solid sets in the model)

        Parameters
        ----------
        model : Model
            Model to get last solid set in

        Returns
        -------
        SetSolid
            SetSolid object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Last", model)

    def Total(model):
        """
        Returns the total number of solid sets in the model

        Parameters
        ----------
        model : Model
            Model to get total in

        Returns
        -------
        integer
            The number of solid sets
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Total", model)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the solid sets in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all solid sets will be unset in
        flag : Flag
            Flag (see AllocateFlag) to unset on the solid sets

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)



# Instance methods
    def AllItems(self):
        """
        Returns all of the solid items for the solid set in the model

        Returns
        -------
        list
            list of Solid objects
        """
        return Oasys.D3PLOT._connection.instanceMethodStream(self.__class__.__name__, self._handle, "AllItems")

    def ClearFlag(self, flag):
        """
        Clears a flag on a solid set

        Parameters
        ----------
        flag : Flag
            Flag (see AllocateFlag) to clear on the solid set

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Flagged(self, flag):
        """
        Checks if the solid set is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag (see AllocateFlag) to test on the solid set

        Returns
        -------
        boolean
            True if flagged, False if not
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def Item(self, index):
        """
        Returns a solid item from the solid set in the model

        Parameters
        ----------
        index : integer
            The index in the solid set to get the solid from (0 <= index < total)

        Returns
        -------
        Solid
            Solid object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Item", index)

    def Next(self):
        """
        Returns the next solid set in the model (or None if there is not one)

        Returns
        -------
        SetSolid
            SetSolid object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous solid set in the model (or None if there is not one)

        Returns
        -------
        SetSolid
            SetSolid object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on a solid set

        Parameters
        ----------
        flag : Flag
            Flag (see AllocateFlag) to set on the solid set

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

