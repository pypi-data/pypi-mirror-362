import Oasys.gRPC

# ItemObject not (yet) used in D3PLOT but defined here for consistency with PRIMER

class ItemObject(Oasys.gRPC.OasysItem):

    def __del__(self):
        if not Oasys.D3PLOT._connection:
            return

        Oasys.D3PLOT._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
        return Oasys.D3PLOT._connection.instanceGetter(self.__class__.__name__, self._handle, name)


    def __setattr__(self, name, value):
        Oasys.D3PLOT._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
        return
