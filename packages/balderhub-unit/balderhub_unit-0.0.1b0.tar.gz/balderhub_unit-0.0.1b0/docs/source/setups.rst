Setups
******

Setup describe **what you have**.

This BalderHub package only provides one single setup class:

.. autoclass:: balderhub.unit.setups.SetupUnit
    :members:
    :private-members:

.. note::
    You must ensure that this class is collected by Balder, otherwise tests with scenarios from this package will not
    be called. The easiest way to do this is to create a file with `setup_balderhub.py` (or any other file starting
    with `setup_*`) and import the setup into it:

    .. code-block:: python

        # file `setup_balderhub.py`
        from balderhub.unit.setups import SetupUnit
