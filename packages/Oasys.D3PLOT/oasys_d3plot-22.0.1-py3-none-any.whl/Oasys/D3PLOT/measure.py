import Oasys.gRPC


# Metaclass for static properties and constants
class MeasureType(type):
    _consts = {'AUTOMATIC', 'DEFORM', 'GENERAL', 'HIDDEN', 'LABEL', 'MAGNITUDE', 'MODEL_SPACE', 'NODE_ANGLE', 'NODE_ORIGIN', 'NODE_TO_NODE', 'NODE_TO_PART', 'PART_TO_PART', 'SCIENTIFIC', 'SHOW_ALL', 'SHOW_CURRENT', 'SHOW_NONE', 'TRANSPARENT', 'VECTOR', 'WIREFRAME'}
    _props = {'consider_blanking', 'current', 'display', 'format', 'line', 'offsets', 'precision', 'show'}
    _rprops = {'total'}

    def __getattr__(cls, name):
        if name in MeasureType._consts:
            return Oasys.D3PLOT._connection.classGetter(cls.__name__, name)
        if name in MeasureType._props:
            return Oasys.D3PLOT._connection.classGetter(cls.__name__, name)
        if name in MeasureType._rprops:
            return Oasys.D3PLOT._connection.classGetter(cls.__name__, name)

        raise AttributeError("Measure class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the properties we define then set it
        if name in MeasureType._props:
            Oasys.D3PLOT._connection.classSetter(cls.__name__, name, value)
            return

# If one of the read only properties we define then error
        if name in MeasureType._rprops:
            raise AttributeError("Cannot set read-only Measure class attribute '{}'".format(name))

# If one of the constants we define then error
        if name in MeasureType._consts:
            raise AttributeError("Cannot set Measure class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class Measure(Oasys.gRPC.OasysItem, metaclass=MeasureType):
    _props = {'name'}
    _rprops = {'index', 'type'}


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
        if name in Measure._props:
            return Oasys.D3PLOT._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in Measure._rprops:
            return Oasys.D3PLOT._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("Measure instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Measure._props:
            Oasys.D3PLOT._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in Measure._rprops:
            raise AttributeError("Cannot set read-only Measure instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, type, options):
        handle = Oasys.D3PLOT._connection.constructor(self.__class__.__name__, type, options)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new Measure object

        Parameters
        ----------
        type : constant
            Measure type. Can be
            Measure.NODE_TO_NODE,
            Measure.NODE_ANGLE,
            Measure.NODE_ORIGIN,
            Measure.NODE_TO_PART or
            Measure.PART_TO_PART
        options : dict
            Measure options

        Returns
        -------
        Measure
            Measure object
        """


# Static methods
    def Delete(type):
        """
        Deletes the measure with the given index

        Parameters
        ----------
        type : integer
            Index of the measure to be deleted, starting at 1

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Delete", type)

    def DeleteAll():
        """
        Deletes all measures

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "DeleteAll")

    def GetFromIndex(type):
        """
        Gets the measure object for a given index

        Parameters
        ----------
        type : integer
            Index of the measure, starting at 1

        Returns
        -------
        Measure
            Measure object for that index
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "GetFromIndex", type)



# Instance methods
    def Data(self):
        """
        Returns an object with data for this measure

        Returns
        -------
        dict
            Dict with properties
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Data")

