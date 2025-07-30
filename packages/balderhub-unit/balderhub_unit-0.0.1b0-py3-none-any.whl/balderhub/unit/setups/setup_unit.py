import balder

from balderhub.unit.lib.setup_features import UnitFeature


class SetupUnit(balder.Setup):
    """
    The universal setup class for all unit tests without devices.
    """
    class _(balder.Device):
        __unit = UnitFeature()
