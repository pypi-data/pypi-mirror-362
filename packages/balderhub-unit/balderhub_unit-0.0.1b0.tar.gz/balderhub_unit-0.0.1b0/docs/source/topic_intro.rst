Introduction into using Unit Objects
************************************

This package is a simple BalderHub package that can be used as a kickstart tool, to just write down a test or even as
base class for a big unittest environment. In this section you find some short examples how you can use it.

Using it as a Kickstart-Environment
===================================

Balder provides a framework for working with many different devices within one single test automation framework. It
allows to reuse tests even for complete different devices.

However, sometimes you want to start without thinking about the device structure and feature definition. Here it can
help to simply write down a test. This package provides a simple scenario class to do that:

.. code-block:: python

    # file `scenario_coffee_machine.py`
    import balderhub.unit.scenarios

    from myapp.coffee_machine import CoffeeMachine
    from testutilities import TieredDeveloper

    class ScenarioCoffee(balderhub.unit.scenarios.ScenarioUnit):

        def test_execute_coffee_process():
            tiered_developer = TieredDeveloper()
            coffee_machine = CoffeeMachine()
            tiered_developer.start_coffee_machine(coffee_machine)
            tiered_developer.wait_until_machine_is_ready(coffee_machine)

            tiered_developer.place_cup()
            tiered_developer.press_coffee_button(coffee_machine)
            tiered_developer.wait_for_coffee_machine(coffee_machine)

            assert not tiered_developer.cup_is_empty()
            assert tiered_developer.coffee_tastes_good()


Of course, you can define your own devices and features at any time afterwards. To do this, simply replace the parent
class with the universal Scenario class or with another more-specific Scenario class.

.. code-block:: python

    # file `scenario_coffee_machine.py`
    class ScenarioCoffeeMachine(balder.Scenario):

        class Developer(balder.Device):
            cm_manager = ManageACoffeeMachineFeature()
            cup_manager = ManageACupFeature()
            drink = TasteAndDrinkCoffeesFeature()

        class CoffeeMachine(balder.Device):
            creation = CreateCoffeeFeature()

        @balder.fixture('setup')
        def start_coffee_machine(self):
            self.Developer.cm_manager.start_coffee_machine()
            self.Developer.cm_manager.wait_until_machine_is_ready()
            yield
            self.Developer.cm_manager.switch_coffee_machine_off()

        def test_create_coffee(self):
            self.Developer.cup_manager.place_cup()
            self.Developer.cup_manager.press_coffee_button()

            assert self.CoffeeMachine.creation.is_in_creation_process()

            self.Developer.cup_manager.wait_till_cup_is_full()

            assert self.Developer.drink.coffee_tastes_good()


Using it for unit tests
=======================

Of course you can also use this package for defining simple unit tests of classes or functions. Feel free to create your
own structure.
