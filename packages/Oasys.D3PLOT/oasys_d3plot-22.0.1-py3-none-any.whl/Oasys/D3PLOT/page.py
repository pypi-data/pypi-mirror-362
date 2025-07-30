import Oasys.gRPC


# Metaclass for static properties and constants
class PageType(type):
    _consts = {'LAYOUT_1_1', 'LAYOUT_2_2', 'LAYOUT_3_3', 'LAYOUT_CUSTOM', 'LAYOUT_TILE_TALL', 'LAYOUT_TILE_WIDE'}

    def __getattr__(cls, name):
        if name in PageType._consts:
            return Oasys.D3PLOT._connection.classGetter(cls.__name__, name)

        raise AttributeError("Page class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in PageType._consts:
            raise AttributeError("Cannot set Page class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class Page(Oasys.gRPC.OasysItem, metaclass=PageType):
    _props = {'layout', 'x', 'y'}
    _rprops = {'number'}


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
        if name in Page._props:
            return Oasys.D3PLOT._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in Page._rprops:
            return Oasys.D3PLOT._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("Page instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Page._props:
            Oasys.D3PLOT._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in Page._rprops:
            raise AttributeError("Cannot set read-only Page instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Static methods
    def First():
        """
        Returns the Page object for the first page in D3PLOT

        Returns
        -------
        Page
            Page object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "First")

    def GetFromID(page_number):
        """
        Returns the Page object for a page ID

        Parameters
        ----------
        page_number : integer
            number of the page you want the Page object for

        Returns
        -------
        Page
            Page object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "GetFromID", page_number)

    def Last():
        """
        Returns the Page object for the last page in D3PLOT

        Returns
        -------
        Page
            Page object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Last")

    def Total():
        """
        Returns the total number of pages in D3PLOT

        Returns
        -------
        integer
            Total number of pages
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Total")



# Instance methods
    def Next(self):
        """
        Returns the next page (or None if there is not one)

        Returns
        -------
        Page
            Page object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous page (or None if there is not one)

        Returns
        -------
        Page
            Page object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def Show(self):
        """
        Shows this page in D3PLOT

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Show")

