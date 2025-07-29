import Oasys.gRPC

class ItemObject(Oasys.gRPC.OasysItem):

    def __del__(self):
        if not Oasys.PRIMER._connection:
            return

        Oasys.PRIMER._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
        return Oasys.PRIMER._connection.instanceGetter(self.__class__.__name__, self._handle, name)


    def __setattr__(self, name, value):
        Oasys.PRIMER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
        return
