class HomCloudError(Exception):
    """
    Base exception class of all exceptions in homcloud.interface
    and homcloud.paraview_interface module.
    """

    def __init__(self, message, code):
        self.message = message
        self.code = code


class VolumeNotFound(HomCloudError):
    """
    Exception class for :meth:`Pair.optimal_volume` and
    :meth:`Pair.stable_volume`.
    """

    def __init__(self, message, code):
        super().__init__(message, code)
