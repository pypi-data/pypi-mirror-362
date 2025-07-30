import Oasys.gRPC


# Metaclass for static properties and constants
class OptionsType(type):
    _props = {'auto_confirm', 'exception_messages', 'max_widgets', 'max_window_lines', 'ssh_buffer_size'}

    def __getattr__(cls, name):
        if name in OptionsType._props:
            return Oasys.D3PLOT._connection.classGetter(cls.__name__, name)

        raise AttributeError("Options class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the properties we define then set it
        if name in OptionsType._props:
            Oasys.D3PLOT._connection.classSetter(cls.__name__, name, value)
            return

# Set the property locally
        cls.__dict__[name] = value


class Options(Oasys.gRPC.OasysItem, metaclass=OptionsType):


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

        raise AttributeError("Options instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# Set the property locally
        self.__dict__[name] = value
