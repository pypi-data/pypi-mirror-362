import Oasys.gRPC


# Metaclass for static properties and constants
class UtilsType(type):

    def __getattr__(cls, name):

        raise AttributeError("Utils class attribute '{}' does not exist".format(name))


class Utils(Oasys.gRPC.OasysItem, metaclass=UtilsType):


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

        raise AttributeError("Utils instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# Set the property locally
        self.__dict__[name] = value


# Static methods
    def Ascii85Encode(data, length=Oasys.gRPC.defaultArg):
        """
        Encodes an ASCII85 encoded string. This enables binary data to be represented by ASCII characters using five ASCII characters
        to represent four bytes of binary data (making the encoded size 1/4 larger than the original). By doing this binary data can be stored in
        JavaScript strings. Note that the method used by D3PLOT to encode and decode strings differs from the standard ASCII85 encoding as that uses the
        ASCII characters ", ' and \ which cannot be used in JavaScript strings as they have special meanings. The method in D3PLOT uses
        0-84 are !-u (ASCII codes 33-117) (i.e. 33 is added to it) with the following exceptions
        v is used instead of " (ASCII code 118 instead of 34)
        w is used instead of ' (ASCII code 119 instead of 39)
        x is used instead of \ (ASCII code 120 instead of 92)
        If all five digits are 0 they are represented by a single character z instead of !!!!!

        Parameters
        ----------
        data : `ListBuffer `_
            `ListBuffer `_ containing the data
        length : integer
            Optional. Length of data in list buffer to encode. If omitted the whole list buffer will be encoded

        Returns
        -------
        str
            string
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Ascii85Encode", data, length)

    def Build():
        """
        Returns the build number

        Returns
        -------
        int
            integer
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Build")

    def CallPromiseHandlers():
        """
        Manually call any promise handlers/callbacks in the job queue

        Returns
        -------
        None
            no return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "CallPromiseHandlers")

    def CheckinLicense(feature):
        """
        Checks a license for a feature back in

        Parameters
        ----------
        feature : string
            feature to check license back in for

        Returns
        -------
        None
            no return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "CheckinLicense", feature)

    def CheckoutLicense(feature):
        """
        Checks out a license for a feature

        Parameters
        ----------
        feature : string
            feature to check license for

        Returns
        -------
        bool
            True if license available, False if not
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "CheckoutLicense", feature)

    def GarbageCollect():
        """
        Forces garbage collection to be done. This should not normally need to be called
        but in exceptional circumstances it can be called to ensure that garbage collection is done to
        return memory

        Returns
        -------
        None
            no return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "GarbageCollect")

    def HTMLBrowser():
        """
        Returns the path to the default HTML browser

        Returns
        -------
        str
            string of the path
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "HTMLBrowser")

    def HiResTimer():
        """
        A high resolution timer that can be used to time how long things take.
        The first time this is called the timer will start and return 0. Subsequent calls will return
        the time in nanoseconds since the first call. Note that the timer will almost certainly not have
        1 nanosecond precision but, depending on the platform, should should have a resolution of at least 1 microsecond.
        The resolution can be found by using Utils.TimerResolution()

        Returns
        -------
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "HiResTimer")

    def PdfReader():
        """
        Returns the path to the executable of the default pdf reader

        Returns
        -------
        str
            string of the path
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "PdfReader")

    def SHA256(filename):
        """
        Create a SHA-256 hash for a file

        Parameters
        ----------
        filename : string
            File to calculate the hash for

        Returns
        -------
        str
            string
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "SHA256", filename)

    def SHA512(filename):
        """
        Create a SHA-512 hash for a file

        Parameters
        ----------
        filename : string
            File to calculate the hash for

        Returns
        -------
        str
            string
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "SHA512", filename)

    def TimerResolution():
        """
        Returns the resolution (precision) of the Utils.HiResTimer() timer in nanoseconds

        Returns
        -------
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "TimerResolution")

    def UUID():
        """
        Create an UUID (Universally Unique Identifier)

        Returns
        -------
        str
            string
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "UUID")

    def Version():
        """
        Returns the version number

        Returns
        -------
        float
            real
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Version")

