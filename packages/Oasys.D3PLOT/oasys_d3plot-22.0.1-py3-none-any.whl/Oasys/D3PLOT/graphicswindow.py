import Oasys.gRPC


# Metaclass for static properties and constants
class GraphicsWindowType(type):
    _consts = {'NO_OFFSET', 'OFFSET_MODEL_SPACE', 'OFFSET_SCREEN_SPACE', 'UP_AUTOMATIC', 'UP_X', 'UP_Y', 'UP_Z'}

    def __getattr__(cls, name):
        if name in GraphicsWindowType._consts:
            return Oasys.D3PLOT._connection.classGetter(cls.__name__, name)

        raise AttributeError("GraphicsWindow class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in GraphicsWindowType._consts:
            raise AttributeError("Cannot set GraphicsWindow class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class GraphicsWindow(Oasys.gRPC.OasysItem, metaclass=GraphicsWindowType):
    _props = {'active', 'state'}
    _rprops = {'models', 'number', 'states'}


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

# If one of the properties we define then get it
        if name in GraphicsWindow._props:
            return Oasys.D3PLOT._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in GraphicsWindow._rprops:
            return Oasys.D3PLOT._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("GraphicsWindow instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in GraphicsWindow._props:
            Oasys.D3PLOT._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in GraphicsWindow._rprops:
            raise AttributeError("Cannot set read-only GraphicsWindow instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, *model):
        handle = Oasys.D3PLOT._connection.constructor(self.__class__.__name__, model)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Creates a new graphics window in D3PLOT

        Parameters
        ----------
        *model : Model object
            The model to open in this graphics window
            This argument can be repeated if required.
            Alternatively a single array argument containing the multiple values can be given

        Returns
        -------
        GraphicsWindow
            GraphicsWindow object
        """


# Static methods
    def First():
        """
        Returns the GraphicsWindow object for the first graphics window in D3PLOT
        (or None if there are no graphics windows)

        Returns
        -------
        GraphicsWindow
            GraphicsWindow object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "First")

    def GetFromID(graphics_window_number):
        """
        Returns the GraphicsWindow object for a graphics window ID (or None if graphics window does not exist)

        Parameters
        ----------
        graphics_window_number : integer
            number of the graphics window you want the GraphicsWindow object for

        Returns
        -------
        GraphicsWindow
            GraphicsWindow object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "GetFromID", graphics_window_number)

    def Last():
        """
        Returns the GraphicsWindow object for the last graphics window in D3PLOT
        (or None if there are no graphics windows)

        Returns
        -------
        GraphicsWindow
            GraphicsWindow object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Last")

    def Total():
        """
        Returns the total number of graphics windows in use in D3PLOT

        Returns
        -------
        integer
            Total number of graphics windows
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Total")



# Instance methods
    def AddModel(self, model):
        """
        Adds a model to a graphics window

        Parameters
        ----------
        model : Model object
            The model to add to the graphics window

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "AddModel", model)

    def Delete(self):
        """
        Deletes a graphics window in D3PLOT
        Do not use the GraphicsWindow object after calling this method

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Delete")

    def GetModelInfo(self, index):
        """
        Gets the information for a model in a graphics window

        Parameters
        ----------
        index : integer
            index of the model in the graphics window you want information for (0 <= index < models)

        Returns
        -------
        dict
            Dict with properties
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "GetModelInfo", index)

    def GetTargetEye(self):
        """
        Get the current target and eye settings

        Returns
        -------
        dict
            Dict with properties
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "GetTargetEye")

    def Next(self):
        """
        Returns the next graphics window (or None if there is not one)

        Returns
        -------
        GraphicsWindow
            GraphicsWindow object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous graphics window (or None if there is not one)

        Returns
        -------
        GraphicsWindow
            GraphicsWindow object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def Redraw(self):
        """
        Redraws the graphics window

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Redraw")

    def RemoveModel(self, model):
        """
        Removes a model from a graphics window

        Parameters
        ----------
        model : Model object
            The model to remove from the graphics window

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "RemoveModel", model)

    def SetModelInfo(self, index, info):
        """
        Sets the information for a model in a graphics window

        Parameters
        ----------
        index : integer
            index of the model in the graphics window you want to set information for (0 <= index < models)
        info : dict
            Dictionary containing the information to set. Can be any of:

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "SetModelInfo", index, info)

    def SetTargetEye(self, info):
        """
        Set the current target and eye settings

        Parameters
        ----------
        info : dict
            Dictionary containing the target and eye properties

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "SetTargetEye", info)

