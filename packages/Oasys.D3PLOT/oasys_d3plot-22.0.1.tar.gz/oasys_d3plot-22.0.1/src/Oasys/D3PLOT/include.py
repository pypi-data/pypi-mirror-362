import Oasys.gRPC


# Metaclass for static properties and constants
class IncludeType(type):
    _consts = {'NATIVE', 'UNIX', 'WINDOWS'}

    def __getattr__(cls, name):
        if name in IncludeType._consts:
            return Oasys.D3PLOT._connection.classGetter(cls.__name__, name)

        raise AttributeError("Include class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in IncludeType._consts:
            raise AttributeError("Cannot set Include class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class Include(Oasys.gRPC.OasysItem, metaclass=IncludeType):
    _rprops = {'label', 'name', 'parent'}


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
        if name in Include._rprops:
            return Oasys.D3PLOT._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("Include instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the read only properties we define then error
        if name in Include._rprops:
            raise AttributeError("Cannot set read-only Include instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Static methods
    def First(model):
        """
        Returns the first include file in the model (or None if there are no include files in the model)

        Parameters
        ----------
        model : Model
            Model to get first include file in

        Returns
        -------
        Include
            Include object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "First", model)

    def GetFromID(model, number):
        """
        Returns the include file in the model with number (or None if it does not exist)

        Parameters
        ----------
        model : Model
            Model to get include file in
        number : integer
            The number for the include file in the model. Note that include file numbers start at 1. 0 is the main file

        Returns
        -------
        Include
            Include object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "GetFromID", model, number)

    def Last(model):
        """
        Returns the last include file in the model (or None if there are no include files in the model)

        Parameters
        ----------
        model : Model
            Model to get last include file in

        Returns
        -------
        Include
            Include object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Last", model)

    def Total(model):
        """
        Returns the total number of include files in the model

        Parameters
        ----------
        model : Model
            Model to get total in

        Returns
        -------
        int
            Number of includes
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Total", model)



# Instance methods
    def Next(self):
        """
        Returns the next include file in the model (or None if there is not one)

        Returns
        -------
        Include
            Include object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous include file in the model (or None if there is not one)

        Returns
        -------
        Include
            Include object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

