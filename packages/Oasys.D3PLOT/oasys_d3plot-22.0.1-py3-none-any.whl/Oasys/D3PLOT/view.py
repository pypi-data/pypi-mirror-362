import Oasys.gRPC


# Metaclass for static properties and constants
class ViewType(type):
    _consts = {'CURRENT', 'HIDDEN', 'ISO', 'SHADED', 'WIRE', 'XY', 'XZ', 'YZ'}

    def __getattr__(cls, name):
        if name in ViewType._consts:
            return Oasys.D3PLOT._connection.classGetter(cls.__name__, name)

        raise AttributeError("View class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in ViewType._consts:
            raise AttributeError("Cannot set View class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class View(Oasys.gRPC.OasysItem, metaclass=ViewType):


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

        raise AttributeError("View instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# Set the property locally
        self.__dict__[name] = value


# Static methods
    def Ac():
        """
        Autoscales the view

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Ac")

    def Ct():
        """
        Does a contour plot

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Ct")

    def Hi():
        """
        Does a Hidden line plot

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Hi")

    def Li():
        """
        Does a line (wireframe) plot

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Li")

    def Redraw():
        """
        Redraws the plot using the current plot mode

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Redraw")

    def Sh():
        """
        Does a shaded plot

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Sh")

    def Show(view_type):
        """
        Redraws using one of the standard views

        Parameters
        ----------
        view_type : constant
            The view to show. Can be +/-View.XY,
            +/-View.YZ,
            +/-View.XZ or
            +/-View.ISO

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Show", view_type)

    def Si():
        """
        Does a shaded image contour plot

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Si")

    def Vec():
        """
        Does a vector plot

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Vec")

