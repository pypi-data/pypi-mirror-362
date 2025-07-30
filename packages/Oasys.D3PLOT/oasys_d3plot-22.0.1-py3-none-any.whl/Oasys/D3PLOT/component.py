import Oasys.gRPC


# Metaclass for static properties and constants
class ComponentType(type):
    _consts = {'ADENS', 'ADOMF', 'AM', 'AMMG', 'AMMS', 'AREA', 'AV', 'AX', 'AY', 'AZ', 'BAED', 'BAEN', 'BBED', 'BEAM', 'BEAX', 'BENL', 'BENLD', 'BENLP', 'BEP', 'BFMV', 'BFR', 'BFX', 'BFY', 'BFZ', 'BIE', 'BIED', 'BKEN', 'BKEND', 'BKENP', 'BMX', 'BMXX', 'BMY1', 'BMY2', 'BMYY', 'BMZ1', 'BMZ2', 'BMZZ', 'BPE1', 'BPE2', 'BRM', 'BRXX', 'BRY1', 'BRY2', 'BRZ1', 'BRZ2', 'BSAX', 'BSEN', 'BSEND', 'BSENP', 'BSXX', 'BSXY', 'BSZX', 'BV', 'BX', 'BY', 'BZ', 'CAREA', 'CFGX', 'CFGY', 'CFGZ', 'CFLX', 'CFLY', 'CFLZ', 'CFM', 'CSN', 'CST', 'CSX', 'CSY', 'CV', 'CX', 'CY', 'CZ', 'DENS', 'DM', 'DTDT', 'DV', 'DX', 'DY', 'DZ', 'E2MAX', 'E2MIN', 'E2SHEAR', 'EAV', 'EDEN', 'EMASS', 'EMAX', 'EMID', 'EMIN', 'EMS', 'ENGMAJ', 'ENGMIN', 'ENGTHK', 'ENL', 'ENLD', 'ENLP', 'EPL', 'ERATE', 'ERATIO', 'ETEN', 'EVON', 'EXX', 'EXY', 'EYY', 'EYZ', 'EZX', 'EZZ', 'FSTRN', 'GIE', 'GKE', 'GMASS', 'GMM', 'GMX', 'GMY', 'GMZ', 'GTE', 'GVM', 'GVX', 'GVY', 'GVZ', 'HGEN', 'IN_CORE', 'KEN', 'KEND', 'KENP', 'LODE_A', 'LODE_P', 'LODE_PA', 'MADD', 'NODE', 'OTHER', 'PEAV', 'PEMAG', 'PEMAX', 'PEMID', 'PEMIN', 'PEMS', 'PETEN', 'PEXX', 'PEXY', 'PEYY', 'PEYZ', 'PEZX', 'PEZZ', 'PRAT', 'RAM', 'RAV', 'RAX', 'RAY', 'RAZ', 'RDM', 'RDV', 'RDX', 'RDY', 'RDZ', 'RENAME', 'REPLACE', 'RFX', 'RFXY', 'RFY', 'RMX', 'RMXY', 'RMY', 'RQX', 'RQY', 'RT_F', 'RT_P', 'RVM', 'RVOL', 'RVV', 'RVX', 'RVY', 'RVZ', 'S2MAX', 'S2MIN', 'S2SHEAR', 'SAV', 'SB_F', 'SB_L', 'SCALAR', 'SED', 'SEN', 'SEND', 'SENP', 'SHX', 'SMAX', 'SMID', 'SMIN', 'SMS', 'SOLID_SHELL_TSHELL', 'SOX', 'SPC_F', 'SPC_M', 'SP_E', 'SP_F', 'SP_M', 'SP_R', 'SR_P', 'STEN', 'SVON', 'SW_F', 'SW_FAIL', 'SW_S', 'SW_TIME', 'SW_TRSN', 'SXX', 'SXY', 'SYY', 'SYZ', 'SZX', 'SZZ', 'TBOT', 'TEAV', 'TEMAX', 'TEMID', 'TEMIN', 'TEMP', 'TEMS', 'TENSOR', 'TETEN', 'TEXX', 'TEXY', 'TEYY', 'TEYZ', 'TEZX', 'TEZZ', 'TFM', 'TFV', 'TFX', 'TFY', 'TFZ', 'THK', 'TMID', 'TRI', 'TSTP', 'TTOP', 'UBMS', 'UBMV', 'UNOS', 'UNOV', 'USSS', 'USST', 'VECTOR', 'VM', 'VOL', 'VV', 'VX', 'VY', 'VZ', 'XSEC_A', 'XSEC_F', 'XSEC_M', 'YMOD', 'YSTRS', 'YUTF', 'YUTP'}

    def __getattr__(cls, name):
        if name in ComponentType._consts:
            return Oasys.D3PLOT._connection.classGetter(cls.__name__, name)

        raise AttributeError("Component class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in ComponentType._consts:
            raise AttributeError("Cannot set Component class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class Component(Oasys.gRPC.OasysItem, metaclass=ComponentType):
    _rprops = {'componentType', 'dataType', 'dispose', 'location', 'name'}


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
        if name in Component._rprops:
            return Oasys.D3PLOT._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("Component instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the read only properties we define then error
        if name in Component._rprops:
            raise AttributeError("Cannot set read-only Component instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, name, component, data, options=Oasys.gRPC.defaultArg):
        handle = Oasys.D3PLOT._connection.constructor(self.__class__.__name__, name, component, data, options)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Creates a new user defined binary data component in D3PLOT

        Parameters
        ----------
        name : string
            Name for the component
        component : constant
            The type of component stored in the user defined binary component. Either Component.NODE,
            Component.BEAM, Component.SOLID_SHELL_TSHELL or
            Component.OTHER
        data : constant
            The type of data stored in the user defined binary component. Either Component.SCALAR,
            Component.TENSOR or Component.VECTOR
        options : dict
            Optional. Dictionary containing extra information. Can contain any of:

        Returns
        -------
        Model
            Model object
        """


# Static methods
    def First():
        """
        Returns the first user defined binary component in D3PLOT (or None if there are no components)

        Returns
        -------
        Component
            Component object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "First")

    def GetFromID(number):
        """
        Returns the user defined binary component in D3PLOT by ID (or None if the component does not exist)

        Parameters
        ----------
        number : integer
            number of the component you want the Component object for

        Returns
        -------
        Component
            Component object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "GetFromID", number)

    def GetFromName(name):
        """
        Returns the user defined binary component in D3PLOT by name (or None if the component does not exist)

        Parameters
        ----------
        name : string
            name of the component you want the Component object for

        Returns
        -------
        Component
            Component object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "GetFromName", name)

    def Last():
        """
        Returns the last user defined binary component in D3PLOT (or None if there are no components)

        Returns
        -------
        Component
            Component object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Last")

    def Total():
        """
        Returns the total number of user defined binary components in D3PLOT

        Returns
        -------
        integer
            Total number of user binary components
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Total")



# Instance methods
    def Delete(self):
        """
        Deletes the next user defined binary data component.
        Do not use the component object after calling this method

        Returns
        -------
        Component
            Component object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Delete")

    def GetData(self, item, options=Oasys.gRPC.defaultArg):
        """
        Returns the user defined binary data component for an item

        Parameters
        ----------
        item : Node|Beam|Shell|Solid|Tshell
            The Node, Beam, Shell, Solid or
            Tshell the data should be retrieved for
        options : dict
            Optional. Dictionary containing extra information. Can contain any of:

        Returns
        -------
        float|array
            The component data
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "GetData", item, options)

    def Next(self):
        """
        Returns the next user defined binary data component (or None if there is not one)

        Returns
        -------
        Component
            Component object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous user defined binary data component (or None if there is not one)

        Returns
        -------
        Component
            Component object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def PutData(self, item, data, options=Oasys.gRPC.defaultArg):
        """
        Sets the user defined binary data component for an item

        Parameters
        ----------
        item : Node|Beam|Shell|Solid|Tshell
            The Node, Beam, Shell, Solid or
            Tshell the data should be set for
        data : float|list
            The data to set. If the component data property is Component.SCALAR
            this will be a single value. If the component data property is Component.VECTOR
            this is a list with length 3. If the component data property is Component.TESNOR
            this is a list with length 6
        options : dict
            Optional. Dictionary containing extra information. Can contain any of:

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "PutData", item, data, options)

