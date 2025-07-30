import balder


class UnitFeature(balder.Feature):
    """
    This internal used feature is defined in any scenario of this package. By using the scenario :class:`ScenarioUnit`
    as a base class, it will automatically be assigned to the internal device `ScenarioUnit._`
    The setup :class:`SetupUnit` is using the same. This will let to a fix variation between these items.
    No other scenario/setup mapping will match.
    """
    pass
