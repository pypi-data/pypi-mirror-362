import Oasys.gRPC


# Metaclass for static properties and constants
class GroupType(type):

    def __getattr__(cls, name):

        raise AttributeError("Group class attribute '{}' does not exist".format(name))


class Group(Oasys.gRPC.OasysItem, metaclass=GroupType):
    _props = {'title'}
    _rprops = {'label', 'model', 'type'}


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
        if name in Group._props:
            return Oasys.D3PLOT._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in Group._rprops:
            return Oasys.D3PLOT._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("Group instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Group._props:
            Oasys.D3PLOT._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in Group._rprops:
            raise AttributeError("Cannot set read-only Group instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, model):
        handle = Oasys.D3PLOT._connection.constructor(self.__class__.__name__, model)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Creates a new group in D3PLOT

        Parameters
        ----------
        model : Model object
            The model to create the group in

        Returns
        -------
        Group
            Group object
        """


# Static methods
    def First(model):
        """
        Returns the first group in the model (or None if there are no groups)

        Parameters
        ----------
        model : Model
            Model to get first group in

        Returns
        -------
        Group
            Group object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "First", model)

    def GetFromID(model, label):
        """
        Returns the Group object for group in model with label (or None if it does not exist)

        Parameters
        ----------
        model : Model
            Model to get group in
        label : integer
            The label for the group in the model

        Returns
        -------
        Group
            Group object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "GetFromID", model, label)

    def Last(model):
        """
        Returns the last group in the model (or None if there are no groups)

        Parameters
        ----------
        model : Model
            Model to get last group in

        Returns
        -------
        Group
            Group object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Last", model)

    def Total(model):
        """
        Returns the total number of groups in a model

        Parameters
        ----------
        model : Model
            Model to get group in

        Returns
        -------
        integer
            The number of groups
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Total", model)



# Instance methods
    def AddFlagged(self, flag):
        """
        Adds flagged items to the contents of the group

        Parameters
        ----------
        flag : Flag
            Flag (see AllocateFlag) set on items to add to the group

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "AddFlagged", flag)

    def Empty(self):
        """
        Empties the group (removes everything from the group)

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Empty")

    def FlagContents(self, flag):
        """
        Flags the contents of the group

        Parameters
        ----------
        flag : Flag
            Flag (see AllocateFlag) to set for the group contents

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "FlagContents", flag)

    def Next(self):
        """
        Returns the next group in the model (or None if there is not one)

        Returns
        -------
        Group
            Group object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous group in the model (or None if there is not one)

        Returns
        -------
        Group
            Group object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

