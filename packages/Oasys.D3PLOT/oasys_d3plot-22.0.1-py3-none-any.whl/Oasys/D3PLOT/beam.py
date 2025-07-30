import Oasys.gRPC


# Metaclass for static properties and constants
class BeamType(type):

    def __getattr__(cls, name):

        raise AttributeError("Beam class attribute '{}' does not exist".format(name))


class Beam(Oasys.gRPC.OasysItem, metaclass=BeamType):
    _rprops = {'data', 'include', 'index', 'integrationPoints', 'label', 'material', 'model', 'part', 'type'}


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
        if name in Beam._rprops:
            return Oasys.D3PLOT._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("Beam instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the read only properties we define then error
        if name in Beam._rprops:
            raise AttributeError("Cannot set read-only Beam instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Static methods
    def BlankAll(window, model):
        """
        Blanks all of the beams in the model

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to blank the beams in
        model : Model
            Model that all the beams will be blanked in

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "BlankAll", window, model)

    def BlankFlagged(window, model, flag):
        """
        Blanks all of the beams in the model flagged with a defined flag

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to blank the beams in
        model : Model
            Model that the flagged beams will be blanked in
        flag : Flag
            Flag (see AllocateFlag) set on the beams to blank

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "BlankFlagged", window, model, flag)

    def First(model):
        """
        Returns the first beam in the model (or None if there are no beams in the model)

        Parameters
        ----------
        model : Model
            Model to get first beam in

        Returns
        -------
        Beam
            Beam object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "First", model)

    def FlagAll(model, flag):
        """
        Flags all of the beams in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all the beams will be flagged in
        flag : Flag
            Flag (see AllocateFlag) to set on the beams

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model, property=Oasys.gRPC.defaultArg):
        """
        Returns a list of Beam objects or properties for all of the beams in the model.
        If the optional property argument is not given then a list of Beam objects is returned.
        If the property argument is given, that property value for each beam is returned in the list
        instead of a Beam object

        Parameters
        ----------
        model : Model
            Model that all the beams are in
        property : string
            Optional. Name for property to get for all beams in the model

        Returns
        -------
        list
            List of :py:class:`Beam <Beam>` objects or properties
        """
        return Oasys.D3PLOT._connection.classMethodStream(__class__.__name__, "GetAll", model, property)

    def GetFlagged(model, flag, property=Oasys.gRPC.defaultArg):
        """
        Gets all of the beams in the model flagged with a defined flag.
        If the optional property argument is not given then a list of Beam objects is returned.
        If the property argument is given, that property value for each beam is returned in the list
        instead of a Beam object

        Parameters
        ----------
        model : Model
            Model that the flagged beams are in
        flag : Flag
            Flag (see AllocateFlag) set on the beams to get
        property : string
            Optional. Name for property to get for all flagged beams in the model

        Returns
        -------
        list
            List of :py:class:`Beam <Beam>` objects or properties
        """
        return Oasys.D3PLOT._connection.classMethodStream(__class__.__name__, "GetFlagged", model, flag, property)

    def GetFromID(model, label):
        """
        Returns the Beam object for beam in model with label (or None if it does not exist)

        Parameters
        ----------
        model : Model
            Model to get beam in
        label : integer
            The Ansys LS-DYNA label for the beam in the model

        Returns
        -------
        Beam
            Beam object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "GetFromID", model, label)

    def GetFromIndex(model, index):
        """
        Returns the Beam object for beam in model with index (or None if it does not exist)

        Parameters
        ----------
        model : Model
            Model to get beam in
        index : integer
            The D3PLOT internal index in the model for beam, starting at 0

        Returns
        -------
        Beam
            Beam object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "GetFromIndex", model, index)

    def GetMultipleData(component, items, options=Oasys.gRPC.defaultArg):
        """
        Returns the value for a data component for multiple beams. For each beam a local property called data will be created
        containing a number if a scalar component, or a list if a vector or tensor component (or None if the value cannot be calculated).
        The data is also returned as an object.
        Also see GetData

        Parameters
        ----------
        component : constant
            Component constant to get data for
        items : list
            List of Beam objects to get the data for.
            All of the beams must be in the same model
        options : dict
            Optional. Dictionary containing options for getting data. Can be any of:

        Returns
        -------
        dictionary
            Dictionary containing the data. A property is created in the dictionary for each beam with the label. The value of the property is a number if a scalar component or an array if a vector or tensor component (or None if the value cannot be calculated)
        """
        return Oasys.D3PLOT._connection.classMethodStream(__class__.__name__, "GetMultipleData", component, items, options)

    def Last(model):
        """
        Returns the last beam in the model (or None if there are no beams in the model)

        Parameters
        ----------
        model : Model
            Model to get last beam in

        Returns
        -------
        Beam
            Beam object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Last", model)

    def Pick():
        """
        Allows the user to pick a beam from the screen

        Returns
        -------
        Beam
            Beam object or None if cancelled
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Pick")

    def Select(flag):
        """
        Selects beams using an object menu

        Parameters
        ----------
        flag : Flag
            Flag (see AllocateFlag) to use when selecting beams

        Returns
        -------
        integer
            The number of beams selected or None if menu cancelled
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Select", flag)

    def Total(model):
        """
        Returns the total number of beams in the model

        Parameters
        ----------
        model : Model
            Model to get total in

        Returns
        -------
        integer
            The number of beams
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Total", model)

    def TotalDeleted(model):
        """
        Returns the total number of beams that have been deleted in
        a model in the state given by its
        state property

        Parameters
        ----------
        model : Model
            Model to get total in

        Returns
        -------
        integer
            The number of beams that have been deleted
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "TotalDeleted", model)

    def UnblankAll(window, model):
        """
        Unblanks all of the beams in the model

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to unblank the beams in
        model : Model
            Model that all the beams will be unblanked in

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "UnblankAll", window, model)

    def UnblankFlagged(window, model, flag):
        """
        Unblanks all of the beams in the model flagged with a defined flag

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to unblank the beams in
        model : Model
            Model that the flagged beams will be unblanked in
        flag : Flag
            Flag (see AllocateFlag) set on the beams to unblank

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "UnblankFlagged", window, model, flag)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the beams in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all beams will be unset in
        flag : Flag
            Flag (see AllocateFlag) to unset on the beams

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)



# Instance methods
    def Blank(self, window):
        """
        Blanks the beam in a graphics window

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to blank the beam in

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank", window)

    def Blanked(self, window):
        """
        Checks if the beam is blanked in a graphics window or not

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) in which to check if the beam is blanked

        Returns
        -------
        boolean
            True if blanked, False if not
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Blanked", window)

    def ClearFlag(self, flag):
        """
        Clears a flag on a beam

        Parameters
        ----------
        flag : Flag
            Flag (see AllocateFlag) to clear on the beam

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Deleted(self):
        """
        Checks if the beam has been deleted or not

        Returns
        -------
        boolean
            True if deleted, False if not
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Deleted")

    def Flagged(self, flag):
        """
        Checks if the beam is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag (see AllocateFlag) to test on the beam

        Returns
        -------
        boolean
            True if flagged, False if not
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def ForceMoment(self, options=Oasys.gRPC.defaultArg):
        """
        Returns the forces and moments for the beam

        Parameters
        ----------
        options : dict
            Optional. Dictionary containing options for getting data. Can be any of:

        Returns
        -------
        array
            Array containing the forces and moments [Fx, Fy, Fz, Mxx, Myy, Mzz] (or None if the value cannot be calculated)
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "ForceMoment", options)

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

    def LocalAxes(self):
        """
        Returns the local axes of the element in model space, expressed as direction cosines in a 2D list.
        Beam elements must have 3 nodes to be able to return local axes

        Returns
        -------
        list
            list of lists
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "LocalAxes")

    def Next(self):
        """
        Returns the next beam in the model (or None if there is not one)

        Returns
        -------
        Beam
            Beam object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous beam in the model (or None if there is not one)

        Returns
        -------
        Beam
            Beam object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on a beam

        Parameters
        ----------
        flag : Flag
            Flag (see AllocateFlag) to set on the beam

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Topology(self):
        """
        Returns the topology for the beam in the model

        Returns
        -------
        list
            list of Node objects
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Topology")

    def Unblank(self, window):
        """
        Unblanks the beam in a graphics window

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to unblank the beam in

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank", window)

