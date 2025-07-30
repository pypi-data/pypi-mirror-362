import Oasys.gRPC


# Metaclass for static properties and constants
class SetNodeType(type):

    def __getattr__(cls, name):

        raise AttributeError("SetNode class attribute '{}' does not exist".format(name))


class SetNode(Oasys.gRPC.OasysItem, metaclass=SetNodeType):
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
        if name in SetNode._rprops:
            return Oasys.D3PLOT._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("SetNode instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the read only properties we define then error
        if name in SetNode._rprops:
            raise AttributeError("Cannot set read-only SetNode instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Static methods
    def First(model):
        """
        Returns the first node set in the model (or None if there are no node sets in the model)

        Parameters
        ----------
        model : Model
            Model to get first node set in

        Returns
        -------
        SetNode
            SetNode object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "First", model)

    def FlagAll(model, flag):
        """
        Flags all of the node sets in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all the node sets will be flagged in
        flag : Flag
            Flag (see AllocateFlag) to set on the node sets

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of SetNode objects or properties for all of the node sets in the model.
        If the optional property argument is not given then a list of SetNode objects is returned.
        If the property argument is given, that property value for each node set is returned in the list
        instead of a SetNode object

        Parameters
        ----------
        model : Model
            Model that all the node sets are in
        property : string
            Optional. Name for property to get for all node sets in the model

        Returns
        -------
        list
            List of :py:class:`SetNode <SetNode>` objects or properties
        """
        return Oasys.D3PLOT._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Gets all of the node sets in the model flagged with a defined flag.
        If the optional property argument is not given then a list of SetNode objects is returned.
        If the property argument is given, that property value for each node set is returned in the list
        instead of a SetNode object

        Parameters
        ----------
        model : Model
            Model that the flagged node sets are in
        flag : Flag
            Flag (see AllocateFlag) set on the node sets to get
        property : string
            Optional. Name for property to get for all flagged node sets in the model

        Returns
        -------
        list
            List of :py:class:`SetNode <SetNode>` objects or properties
        """
        return Oasys.D3PLOT._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, label):
        """
        Returns the SetNode object for node set in model with label (or None if it does not exist)

        Parameters
        ----------
        model : Model
            Model to get node set in
        label : integer
            The Ansys LS-DYNA label for the node set in the model

        Returns
        -------
        SetNode
            SetNode object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "GetFromID", model, label)

    def GetFromIndex(model, index):
        """
        Returns the SetNode object for node set in model with index (or None if it does not exist)

        Parameters
        ----------
        model : Model
            Model to get node set in
        index : integer
            The D3PLOT internal index in the model for node set, starting at 0

        Returns
        -------
        SetNode
            SetNode object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "GetFromIndex", model, index)

    def Last(model):
        """
        Returns the last node set in the model (or None if there are no node sets in the model)

        Parameters
        ----------
        model : Model
            Model to get last node set in

        Returns
        -------
        SetNode
            SetNode object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Last", model)

    def Total(model):
        """
        Returns the total number of node sets in the model

        Parameters
        ----------
        model : Model
            Model to get total in

        Returns
        -------
        integer
            The number of node sets
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Total", model)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the node sets in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all node sets will be unset in
        flag : Flag
            Flag (see AllocateFlag) to unset on the node sets

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)



# Instance methods
    def AllItems(self):
        """
        Returns all of the node items for the node set in the model

        Returns
        -------
        list
            list of Node objects
        """
        return Oasys.D3PLOT._connection.instanceMethodStream(self.__class__.__name__, self._handle, "AllItems")

    def ClearFlag(self, flag):
        """
        Clears a flag on a node set

        Parameters
        ----------
        flag : Flag
            Flag (see AllocateFlag) to clear on the node set

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Flagged(self, flag):
        """
        Checks if the node set is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag (see AllocateFlag) to test on the node set

        Returns
        -------
        boolean
            True if flagged, False if not
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def Item(self, index):
        """
        Returns a node item from the node set in the model

        Parameters
        ----------
        index : integer
            The index in the node set to get the node from (0 <= index < total)

        Returns
        -------
        Node
            Node object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Item", index)

    def Next(self):
        """
        Returns the next node set in the model (or None if there is not one)

        Returns
        -------
        SetNode
            SetNode object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous node set in the model (or None if there is not one)

        Returns
        -------
        SetNode
            SetNode object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on a node set

        Parameters
        ----------
        flag : Flag
            Flag (see AllocateFlag) to set on the node set

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

