import balder

from balderhub.unit.lib.setup_features import UnitFeature


class ScenarioUnit(balder.Scenario):
    """
    Scenario base class that can be used for test scenarios without any devices.

    .. note::
        Please do not forget to add the :class:`SetupUnit` to your environment. Tests will only be collected when this
        setup is active.
    """

    class _(balder.Device):
        __unit = UnitFeature()
