import Oasys.gRPC


# Metaclass for static properties and constants
class TypeType(type):
    _consts = {'BEAM', 'BOLT', 'BWLD', 'CONTACT', 'CONX', 'CWLD', 'DES', 'ELEMENT', 'GROUP', 'GWLD', 'HSWA', 'HWLD', 'JOINT', 'MASS', 'MATERIAL', 'MIG', 'MODEL', 'NODE', 'NRB', 'PART', 'PRETENSIONER', 'RBOLT', 'RETRACTOR', 'RIGIDWALL', 'SBENT', 'SEATBELT', 'SECTION', 'SEGMENT', 'SET_BEAM', 'SET_DISCRETE', 'SET_NODE', 'SET_PART', 'SET_SHELL', 'SET_SOLID', 'SET_TSHELL', 'SHELL', 'SLIPRING', 'SOLID', 'SPC', 'SPH', 'SPRING', 'TSHELL', 'WINDOW', 'XSEC'}

    def __getattr__(cls, name):
        if name in TypeType._consts:
            return Oasys.D3PLOT._connection.classGetter(cls.__name__, name)

        raise AttributeError("Type class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in TypeType._consts:
            raise AttributeError("Cannot set Type class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class Type(Oasys.gRPC.OasysItem, metaclass=TypeType):


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

        raise AttributeError("Type instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# Set the property locally
        self.__dict__[name] = value
