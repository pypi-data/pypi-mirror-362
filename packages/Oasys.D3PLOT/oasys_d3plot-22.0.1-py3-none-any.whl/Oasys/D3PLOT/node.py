import Oasys.gRPC


# Metaclass for static properties and constants
class NodeType(type):

    def __getattr__(cls, name):

        raise AttributeError("Node class attribute '{}' does not exist".format(name))


class Node(Oasys.gRPC.OasysItem, metaclass=NodeType):
    _rprops = {'data', 'include', 'index', 'label', 'model', 'type'}


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
        if name in Node._rprops:
            return Oasys.D3PLOT._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("Node instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the read only properties we define then error
        if name in Node._rprops:
            raise AttributeError("Cannot set read-only Node instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Static methods
    def BlankAll(window, model):
        """
        Blanks all of the nodes in the model

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to blank the nodes in
        model : Model
            Model that all the nodes will be blanked in

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "BlankAll", window, model)

    def BlankFlagged(window, model, flag):
        """
        Blanks all of the nodes in the model flagged with a defined flag

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to blank the nodes in
        model : Model
            Model that the flagged nodes will be blanked in
        flag : Flag
            Flag (see AllocateFlag) set on the nodes to blank

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "BlankFlagged", window, model, flag)

    def First(model):
        """
        Returns the first node in the model (or None if there are no nodes in the model)

        Parameters
        ----------
        model : Model
            Model to get first node in

        Returns
        -------
        Node
            Node object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "First", model)

    def FlagAll(model, flag):
        """
        Flags all of the nodes in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all the nodes will be flagged in
        flag : Flag
            Flag (see AllocateFlag) to set on the nodes

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Node objects or properties for all of the nodes in the model.
        If the optional property argument is not given then a list of Node objects is returned.
        If the property argument is given, that property value for each node is returned in the list
        instead of a Node object

        Parameters
        ----------
        model : Model
            Model that all the nodes are in
        property : string
            Optional. Name for property to get for all nodes in the model

        Returns
        -------
        list
            List of :py:class:`Node <Node>` objects or properties
        """
        return Oasys.D3PLOT._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Gets all of the nodes in the model flagged with a defined flag.
        If the optional property argument is not given then a list of Node objects is returned.
        If the property argument is given, that property value for each node is returned in the list
        instead of a Node object

        Parameters
        ----------
        model : Model
            Model that the flagged nodes are in
        flag : Flag
            Flag (see AllocateFlag) set on the nodes to get
        property : string
            Optional. Name for property to get for all flagged nodes in the model

        Returns
        -------
        list
            List of :py:class:`Node <Node>` objects or properties
        """
        return Oasys.D3PLOT._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, label):
        """
        Returns the Node object for node in model with label (or None if it does not exist)

        Parameters
        ----------
        model : Model
            Model to get node in
        label : integer
            The Ansys LS-DYNA label for the node in the model

        Returns
        -------
        Node
            Node object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "GetFromID", model, label)

    def GetFromIndex(model, index):
        """
        Returns the Node object for node in model with index (or None if it does not exist)

        Parameters
        ----------
        model : Model
            Model to get node in
        index : integer
            The D3PLOT internal index in the model for node, starting at 0

        Returns
        -------
        Node
            Node object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "GetFromIndex", model, index)

    def GetMultipleData(component, items, options=Oasys.gRPC.defaultArg):
        """
        Returns the value for a data component for multiple nodes. For each node a local property called data will be created
        containing a number if a scalar component, or a list if a vector or tensor component (or None if the value cannot be calculated).
        The data is also returned as an object.
        Also see GetData

        Parameters
        ----------
        component : constant
            Component constant to get data for
        items : list
            List of Node objects to get the data for.
            All of the nodes must be in the same model
        options : dict
            Optional. Dictionary containing options for getting data. Can be any of:

        Returns
        -------
        dictionary
            Dictionary containing the data. A property is created in the dictionary for each node with the label. The value of the property is a number if a scalar component or an array if a vector or tensor component (or None if the value cannot be calculated)
        """
        return Oasys.D3PLOT._connection.classMethodStream(__class__.__name__, "GetMultipleData", component, items, options)

    def Last(model):
        """
        Returns the last node in the model (or None if there are no nodes in the model)

        Parameters
        ----------
        model : Model
            Model to get last node in

        Returns
        -------
        Node
            Node object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Last", model)

    def Pick():
        """
        Allows the user to pick a node from the screen

        Returns
        -------
        Node
            Node object or None if cancelled
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Pick")

    def Select(flag):
        """
        Selects nodes using an object menu

        Parameters
        ----------
        flag : Flag
            Flag (see AllocateFlag) to use when selecting nodes

        Returns
        -------
        integer
            The number of nodes selected or None if menu cancelled
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Select", flag)

    def Total(model):
        """
        Returns the total number of nodes in the model

        Parameters
        ----------
        model : Model
            Model to get total in

        Returns
        -------
        integer
            The number of nodes
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Total", model)

    def UnblankAll(window, model):
        """
        Unblanks all of the nodes in the model

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to unblank the nodes in
        model : Model
            Model that all the nodes will be unblanked in

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "UnblankAll", window, model)

    def UnblankFlagged(window, model, flag):
        """
        Unblanks all of the nodes in the model flagged with a defined flag

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to unblank the nodes in
        model : Model
            Model that the flagged nodes will be unblanked in
        flag : Flag
            Flag (see AllocateFlag) set on the nodes to unblank

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "UnblankFlagged", window, model, flag)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the nodes in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all nodes will be unset in
        flag : Flag
            Flag (see AllocateFlag) to unset on the nodes

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)



# Instance methods
    def Acceleration(self):
        """
        Returns the acceleration for the node

        Returns
        -------
        array
            Array containing the nodal acceleration [Ax, Ay, Az] (or None if the value cannot be calculated)
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Acceleration")

    def Blank(self, window):
        """
        Blanks the node in a graphics window

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to blank the node in

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank", window)

    def Blanked(self, window):
        """
        Checks if the node is blanked in a graphics window or not

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) in which to check if the node is blanked

        Returns
        -------
        boolean
            True if blanked, False if not
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Blanked", window)

    def ClearFlag(self, flag):
        """
        Clears a flag on a node

        Parameters
        ----------
        flag : Flag
            Flag (see AllocateFlag) to clear on the node

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Coordinates(self):
        """
        Returns the coordinates for the node

        Returns
        -------
        array
            Array containing the nodal coordinates [Cx, Cy, Cz] (or None if the value cannot be calculated)
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Coordinates")

    def Displacement(self):
        """
        Returns the displacement for the node

        Returns
        -------
        array
            Array containing the nodal displacement [Dx, Dy, Dz] (or None if the value cannot be calculated)
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Displacement")

    def Elements(self, type):
        """
        Returns the elements using this node

        Parameters
        ----------
        type : constant
            The type of elements. Either Type.BEAM,
            Type.SHELL, Type.SOLID or
            Type.TSHELL

        Returns
        -------
        array
            Array containing the elements or None if there are no elements
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Elements", type)

    def Flagged(self, flag):
        """
        Checks if the node is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag (see AllocateFlag) to test on the node

        Returns
        -------
        boolean
            True if flagged, False if not
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

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
        Returns the next node in the model (or None if there is not one)

        Returns
        -------
        Node
            Node object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous node in the model (or None if there is not one)

        Returns
        -------
        Node
            Node object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on a node

        Parameters
        ----------
        flag : Flag
            Flag (see AllocateFlag) to set on the node

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Unblank(self, window):
        """
        Unblanks the node in a graphics window

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to unblank the node in

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank", window)

    def Velocity(self):
        """
        Returns the velocity for the node

        Returns
        -------
        array
            Array containing the nodal velocity [Vx, Vy, Vz] (or None if the value cannot be calculated)
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Velocity")

