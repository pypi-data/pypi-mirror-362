from akida.core import (Layer, LayerParams, LayerType)


class ExtractToken(Layer):
    """A layer capable of extracting a range from input tensor.

    This is similar to numpy.take_along_axis, where the indices are in the
    range [begin:end]. Note that reduction axis will be the first axis that
    is not 1.

    Args:
        begin (int, optional): beginning of the range to take into account.
            Defaults to 0.
        end (int, optional): end of the range to take into account.
            Defaults to None.
        name (str, optional): name of the layer. Defaults to empty string.
    """

    def __init__(self,
                 begin=0,
                 end=None,
                 name=""):
        if end is None:
            end = begin + 1
        try:
            params = LayerParams(
                LayerType.ExtractToken, {
                    "begin": begin,
                    "end": end
                })
            # Call parent constructor to initialize C++ bindings
            # Note that we invoke directly __init__ instead of using super, as
            # specified in pybind documentation
            Layer.__init__(self, params, name)
        except BaseException:
            self = None
            raise
