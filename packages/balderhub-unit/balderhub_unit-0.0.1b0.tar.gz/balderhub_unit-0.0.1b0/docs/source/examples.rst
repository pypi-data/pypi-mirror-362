Examples
********

This ``balderhub-unit`` package provides a simple interface for writing tests without any devices.

It provides a simple scenario class :class:`ScenarioUnit`, that helps to do that:

.. code-block:: python

    # file `scenario_calc_add.py`
    import balderhub.unit.scenarios

    from myapp.functions import calc_add

    class ScenarioCalcAdd(balderhub.unit.scenarios.ScenarioUnit):

        def test_add_two_numbers(self):

            assert calc_add(1, 2) == 3

To be able to run this test, you just need to add the predefined setup class :class:`SetupUnit` to the collection by
importing it, f.e.

.. code-block:: python

    # file setup_balderhub.py
    from balderhub.unit.setups import SetupUnit

Balder will automatically collect and execute the test with the predefined setup class :class`SetupUnit`.
