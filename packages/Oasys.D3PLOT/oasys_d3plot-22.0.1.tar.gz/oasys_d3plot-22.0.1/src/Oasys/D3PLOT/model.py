import Oasys.gRPC


# Metaclass for static properties and constants
class ModelType(type):

    def __getattr__(cls, name):

        raise AttributeError("Model class attribute '{}' does not exist".format(name))


class Model(Oasys.gRPC.OasysItem, metaclass=ModelType):
    _props = {'state', 'states', 'title'}
    _rprops = {'filename', 'number'}


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
        if name in Model._props:
            return Oasys.D3PLOT._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in Model._rprops:
            return Oasys.D3PLOT._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("Model instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Model._props:
            Oasys.D3PLOT._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in Model._rprops:
            raise AttributeError("Cannot set read-only Model instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, filename):
        handle = Oasys.D3PLOT._connection.constructor(self.__class__.__name__, filename)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Reads a file into the first free model in D3PLOT

        Parameters
        ----------
        filename : string
            Filename you want to read

        Returns
        -------
        Model
            Model object
        """


# Static methods
    def First():
        """
        Returns the Model object for the first model in D3PLOT
        (or None if there are no models)

        Returns
        -------
        Model
            Model object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "First")

    def GetFromID(model_number):
        """
        Returns the Model object for a model ID (or None if model does not exist)

        Parameters
        ----------
        model_number : integer
            number of the model you want the Model object for

        Returns
        -------
        Model
            Model object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "GetFromID", model_number)

    def Highest():
        """
        Returns the highest model number in D3PLOT (or 0 if no models). Also see Total()

        Returns
        -------
        integer
            Highest model number
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Highest")

    def Last():
        """
        Returns the Model object for the last model in D3PLOT
        (or None if there are no models)

        Returns
        -------
        Model
            Model object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Last")

    def Read(filename):
        """
        Reads a file into D3PLOT

        Parameters
        ----------
        filename : string
            Filename you want to read

        Returns
        -------
        Model
            Model object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Read", filename)

    def Total():
        """
        Returns the total number of models in use in D3PLOT. Also see Highest()

        Returns
        -------
        integer
            Total number of models in use
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Total")



# Instance methods
    def ClearFlag(self, flag):
        """
        Clears a flag on all of the items in the model

        Parameters
        ----------
        flag : Flag
            Flag (see AllocateFlag) to clear

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Delete(self):
        """
        Deletes a model in D3PLOT
        Do not use the Model object after calling this method

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Delete")

    def GraphicsWindows(self):
        """
        Returns the graphics window(s) that the model exists in

        Returns
        -------
        array
            Array of :py:class:`GraphicsWindow <GraphicsWindow>` objects
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "GraphicsWindows")

    def Next(self):
        """
        Returns the next model (or None if there is not one)

        Returns
        -------
        Model
            Model object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous model (or None if there is not one)

        Returns
        -------
        Model
            Model object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def ReadPropertiesFile(self, filename, info=Oasys.gRPC.defaultArg):
        """
        Reads a properties file for the model

        Parameters
        ----------
        filename : string
            Filename for the properties file you want to read
        info : dict
            Optional. Dictionary containing the information to set. Can be any of:

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "ReadPropertiesFile", filename, info)

    def Reread(self):
        """
        Rereads the model

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Reread")

    def Rescan(self):
        """
        Rescans the model

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Rescan")

    def Time(self, state):
        """
        Returns the analysis time for a particular state in the model

        Parameters
        ----------
        state : integer
            The state you want to get the time for (0 <= state <= states)

        Returns
        -------
        float
            Analysis time
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Time", state)

