import Oasys.gRPC


# Metaclass for static properties and constants
class ConstantType(type):
    _consts = {'ALL', 'BASIC', 'BOTTOM', 'CONST_X', 'CONST_Y', 'CONST_Z', 'CURRENT_VAL', 'CUT_SECTION', 'CYLINDRICAL', 'DEFORMED', 'DELETE', 'FAMILY', 'GLOBAL', 'GT', 'GTEQ', 'INCLUDE', 'INTERSECTION', 'LEAVE', 'LOCAL', 'LS_DYNA', 'LT', 'LTEQ', 'MAGNITUDE', 'MATERIAL', 'MAX', 'MIDDLE', 'MIN', 'MODEL', 'N3', 'NEIPH', 'NEIPS', 'NEIPT', 'NIP_B', 'NIP_H', 'NIP_S', 'NIP_T', 'NORMAL', 'N_ON_PLAN', 'N_UBMS', 'N_UBMV', 'N_UNOS', 'N_UNOV', 'N_USSS', 'N_USST', 'OFF', 'OMIT', 'ON', 'OR_AND_V', 'OUTLINE', 'STATE', 'TOP', 'TRANSPARENT', 'UNION', 'USER', 'USER_DEFINED', 'X', 'XX', 'XY', 'Y', 'YY', 'YZ', 'Z', 'ZX', 'ZZ'}

    def __getattr__(cls, name):
        if name in ConstantType._consts:
            return Oasys.D3PLOT._connection.classGetter(cls.__name__, name)

        raise AttributeError("Constant class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in ConstantType._consts:
            raise AttributeError("Cannot set Constant class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class Constant(Oasys.gRPC.OasysItem, metaclass=ConstantType):


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

        raise AttributeError("Constant instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# Set the property locally
        self.__dict__[name] = value
