from balderhub.unit.scenarios import ScenarioUnit


class ScenarioSimpleUnitTestCase(ScenarioUnit):

    def test_simple(self):
        assert 1+2 == 3, 'basic math does not work anymore'
