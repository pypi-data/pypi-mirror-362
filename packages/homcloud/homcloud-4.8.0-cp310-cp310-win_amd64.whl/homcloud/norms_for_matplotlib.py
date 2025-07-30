import math

import numpy as np
import matplotlib.colors as colors


class LogNorm(colors.LogNorm):
    def autoscale_None(self, A):
        super().autoscale_None(A)
        if self.vmax == self.vmin == 0.0:
            self._vmax = 1.1
            self._vmin = 0.9
            self._changed()
        elif self.vmin == 0.0:
            self.vmin = 1.0


class LogPlusOneNorm(colors.Normalize):
    """log(x+1) normalizer for matplotlib.colors."""

    def __init__(self, vmax, vmin=0, clip=False):
        colors.Normalize.__init__(self, vmax=vmax, vmin=vmin, clip=clip)

    def __call__(self, value, clip=None):
        if clip is None:
            clip = self.clip

        result, is_scalar = self.process_value(value)

        self.autoscale_None(result)
        vmax = float(self.vmax)
        if vmax <= 0.0:
            vmax = 1.0
        if clip:
            mask = np.ma.getmask(result)
            result = np.ma.array(np.clip(result.filled(vmax), 0.0, vmax), mask=mask)
        result = np.ma.array(np.log(result.data + 1.0) / math.log(vmax + 1.0), mask=result.mask, copy=False)
        if is_scalar:
            return result[0]
        else:
            return result

    def inverse(self, value):
        if not self.scaled():
            raise ValueError("Not invertible until scaled")

        vmax = float(self.vmax)
        if np.iterable(value):
            return np.ma.exp(value * math.log(vmax + 1)) - 1
        else:
            return math.exp(value * math.log(vmax + 1)) - 1


class LogLogNorm(colors.Normalize):
    """log(log(x+1)+1) normalizer for matplotlib.colors."""

    @staticmethod
    def loglog(x):
        return math.log(math.log(x + 1) + 1)

    def __call__(self, value, clip=None):
        if clip is None:
            clip = self.clip

        result, is_scalar = self.process_value(value)
        vmin, vmax = self.vmin, self.vmax

        if clip:
            result = np.ma.array(np.clip(result.filled(vmax), vmin, vmax), mask=np.ma.getmask(result))
        data = result.data
        data += 1.0
        np.log(data, data)
        data += 1.0
        np.log(data, data)
        data -= self.loglog(vmin)
        data /= self.loglog(vmax) - self.loglog(vmin)
        result = np.ma.array(data, mask=result.mask, copy=False)

        if is_scalar:
            return result[0]
        else:
            return result

    def inverse(self, value):
        if not self.scaled():
            raise ValueError("Not invertible until scaled")

        vmin = float(self.vmin)
        vmax = float(self.vmax)
        loglog_value = self.loglog(vmin) + value * (self.loglog(vmax) - self.loglog(vmin))
        if np.iterable(value):
            return np.ma.exp(np.ma.exp(loglog_value) - 1) - 1
        else:
            return math.exp(math.exp(loglog_value) - 1) - 1


class MidpointNormalize(colors.Normalize):
    """
    This class comes from http://matplotlib.org/users/colormapnorms.html
    """

    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))
