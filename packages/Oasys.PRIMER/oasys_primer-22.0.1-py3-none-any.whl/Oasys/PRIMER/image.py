import Oasys.gRPC


# Metaclass for static properties and constants
class ImageType(type):
    _consts = {'COMPRESS', 'DITHER', 'OPTIMISE', 'SCREEN', 'X2', 'X4'}

    def __getattr__(cls, name):
        if name in ImageType._consts:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("Image class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in ImageType._consts:
            raise AttributeError("Cannot set Image class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class Image(Oasys.gRPC.OasysItem, metaclass=ImageType):


    def __del__(self):
        if not Oasys.PRIMER._connection:
            return

        if self._handle is None:
            return

        Oasys.PRIMER._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
# If constructor for an item fails in program, then _handle will not be set and when
# __del__ is called to return the object we will call this to get the (undefined) value
        if name == "_handle":
            return None

        raise AttributeError("Image instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# Set the property locally
        self.__dict__[name] = value


# Static methods
    def WriteBMP(filename, resolution=Oasys.gRPC.defaultArg, _8bit=Oasys.gRPC.defaultArg, options=Oasys.gRPC.defaultArg):
        """
        Create a bmp image of the current screen image

        Parameters
        ----------
        filename : string
            Filename you want to write.
            The file will be overwritten if it already exists
        resolution : constant
            Optional. The resolution to write the image at. Can be Image.SCREEN,
            Image.X2 or
            Image.X4. If omitted screen resolution will be used
        _8bit : boolean
            Optional. BMP images can be written using either 8 bit (256 colours) or 24 bit (16 million colours).
            If this is true then an 8 bit image will be written. If false (or omitted) a 24 bit image will be written
        options : constant
            Optional. For 8 bit images (see '8bit' argument) the palette can be optimised
            (Image.OPTIMISE) and/or dithered
            (Image.DITHER) and/or compressed
            (Image.COMPRESS)
            If 0 (or omitted) no palette optimising, dithering or compression will be done

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "WriteBMP", filename, resolution, _8bit, options)

    def WriteGIF(filename, resolution=Oasys.gRPC.defaultArg, palette=Oasys.gRPC.defaultArg):
        """
        Create a gif image of the current screen image

        Parameters
        ----------
        filename : string
            Filename you want to write.
            The file will be overwritten if it already exists
        resolution : constant
            Optional. The resolution to write the image at. Can be Image.SCREEN,
            Image.X2 or
            Image.X4. If omitted screen resolution will be used
        palette : constant
            Optional. The palette can be optimised
            (Image.OPTIMISE) and/or dithered
            (Image.DITHER). If 0 (or omitted) no
            palette optimising or dithering will be done

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "WriteGIF", filename, resolution, palette)

    def WriteJPEG(filename, resolution=Oasys.gRPC.defaultArg, quality=Oasys.gRPC.defaultArg):
        """
        Create a jpeg image of the current screen image

        Parameters
        ----------
        filename : string
            Filename you want to write.
            The file will be overwritten if it already exists
        resolution : constant
            Optional. The resolution to write the image at. Can be Image.SCREEN,
            Image.X2 or
            Image.X4. If omitted screen resolution will be used
        quality : integer
            Optional. Quality of the image in percent. Can be in the range [10,100]. If omitted, the quality is 90

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "WriteJPEG", filename, resolution, quality)

    def WritePNG(filename, resolution=Oasys.gRPC.defaultArg, _8bit=Oasys.gRPC.defaultArg, palette=Oasys.gRPC.defaultArg):
        """
        Create a png image of the current screen image

        Parameters
        ----------
        filename : string
            Filename you want to write.
            The file will be overwritten if it already exists
        resolution : constant
            Optional. The resolution to write the image at. Can be Image.SCREEN,
            Image.X2 or
            Image.X4. If omitted screen resolution will be used
        _8bit : boolean
            Optional. PNG images can be written using either 8 bit (256 colours) or 24 bit (16 million colours).
            If this is true then an 8 bit image will be written. If false (or omitted) a 24 bit image will be written
        palette : constant
            Optional. For 8 bit images (see '8bit' argument) the palette can be optimised
            (Image.OPTIMISE) and/or dithered
            (Image.DITHER). If 0 (or omitted) no
            palette optimising or dithering will be done

        Returns
        -------
        None
            No return value
        """
        return Oasys.PRIMER._connection.classMethod(__class__.__name__, "WritePNG", filename, resolution, _8bit, palette)

