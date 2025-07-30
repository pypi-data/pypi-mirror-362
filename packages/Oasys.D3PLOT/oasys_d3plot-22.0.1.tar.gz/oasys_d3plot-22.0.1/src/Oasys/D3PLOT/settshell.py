import Oasys.gRPC


# Metaclass for static properties and constants
class SetTshellType(type):

    def __getattr__(cls, name):

        raise AttributeError("SetTshell class attribute '{}' does not exist".format(name))


class SetTshell(Oasys.gRPC.OasysItem, metaclass=SetTshellType):
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
        if name in SetTshell._rprops:
            return Oasys.D3PLOT._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("SetTshell instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the read only properties we define then error
        if name in SetTshell._rprops:
            raise AttributeError("Cannot set read-only SetTshell instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Static methods
    def First(model):
        """
        Returns the first thick shell set in the model (or None if there are no thick shell sets in the model)

        Parameters
        ----------
        model : Model
            Model to get first thick shell set in

        Returns
        -------
        SetTshell
            SetTshell object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "First", model)

    def FlagAll(model, flag):
        """
        Flags all of the thick shell sets in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all the thick shell sets will be flagged in
        flag : Flag
            Flag (see AllocateFlag) to set on the thick shell sets

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of SetTshell objects or properties for all of the thick shell sets in the model.
        If the optional property argument is not given then a list of SetTshell objects is returned.
        If the property argument is given, that property value for each thick shell set is returned in the list
        instead of a SetTshell object

        Parameters
        ----------
        model : Model
            Model that all the thick shell sets are in
        property : string
            Optional. Name for property to get for all thick shell sets in the model

        Returns
        -------
        list
            List of :py:class:`SetTshell <SetTshell>` objects or properties
        """
        return Oasys.D3PLOT._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Gets all of the thick shell sets in the model flagged with a defined flag.
        If the optional property argument is not given then a list of SetTshell objects is returned.
        If the property argument is given, that property value for each thick shell set is returned in the list
        instead of a SetTshell object

        Parameters
        ----------
        model : Model
            Model that the flagged thick shell sets are in
        flag : Flag
            Flag (see AllocateFlag) set on the thick shell sets to get
        property : string
            Optional. Name for property to get for all flagged thick shell sets in the model

        Returns
        -------
        list
            List of :py:class:`SetTshell <SetTshell>` objects or properties
        """
        return Oasys.D3PLOT._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, label):
        """
        Returns the SetTshell object for thick shell set in model with label (or None if it does not exist)

        Parameters
        ----------
        model : Model
            Model to get thick shell set in
        label : integer
            The Ansys LS-DYNA label for the thick shell set in the model

        Returns
        -------
        SetTshell
            SetTshell object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "GetFromID", model, label)

    def GetFromIndex(model, index):
        """
        Returns the SetTshell object for thick shell set in model with index (or None if it does not exist)

        Parameters
        ----------
        model : Model
            Model to get thick shell set in
        index : integer
            The D3PLOT internal index in the model for thick shell set, starting at 0

        Returns
        -------
        SetTshell
            SetTshell object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "GetFromIndex", model, index)

    def Last(model):
        """
        Returns the last thick shell set in the model (or None if there are no thick shell sets in the model)

        Parameters
        ----------
        model : Model
            Model to get last thick shell set in

        Returns
        -------
        SetTshell
            SetTshell object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Last", model)

    def Total(model):
        """
        Returns the total number of thick shell sets in the model

        Parameters
        ----------
        model : Model
            Model to get total in

        Returns
        -------
        integer
            The number of thick shell sets
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Total", model)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the thick shell sets in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all thick shell sets will be unset in
        flag : Flag
            Flag (see AllocateFlag) to unset on the thick shell sets

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)



# Instance methods
    def AllItems(self):
        """
        Returns all of the thick shell items for the thick shell set in the model

        Returns
        -------
        list
            list of Tshell objects
        """
        return Oasys.D3PLOT._connection.instanceMethodStream(self.__class__.__name__, self._handle, "AllItems")

    def ClearFlag(self, flag):
        """
        Clears a flag on a thick shell set

        Parameters
        ----------
        flag : Flag
            Flag (see AllocateFlag) to clear on the thick shell set

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Flagged(self, flag):
        """
        Checks if the thick shell set is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag (see AllocateFlag) to test on the thick shell set

        Returns
        -------
        boolean
            True if flagged, False if not
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def Item(self, index):
        """
        Returns a thick shell item from the thick shell set in the model

        Parameters
        ----------
        index : integer
            The index in the thick shell set to get the thick shell from (0 <= index < total)

        Returns
        -------
        Tshell
            Tshell object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Item", index)

    def Next(self):
        """
        Returns the next thick shell set in the model (or None if there is not one)

        Returns
        -------
        SetTshell
            SetTshell object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous thick shell set in the model (or None if there is not one)

        Returns
        -------
        SetTshell
            SetTshell object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on a thick shell set

        Parameters
        ----------
        flag : Flag
            Flag (see AllocateFlag) to set on the thick shell set

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

