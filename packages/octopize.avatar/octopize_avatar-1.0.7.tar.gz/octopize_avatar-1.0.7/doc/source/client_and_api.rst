Client
======

The `ApiClient` object
----------------------

The Python client acts as an interface that communicates with the avatarization engine.
For more information about the concepts and avatarization, checkout our main `docs <https://docs.octopize.io/docs/overview/>`_.

The :class:`Manager <avatars.manager.Manager>` is the main interfaces that you should use.
You'll instantiate it, and authenticate using the credentials to the engine.

The :class:`Runner <avatars.runner.Runner>` contains the main functionality for your anonymization. Use :meth:`avatars.manager.Manager.create_runner` to create a runner.


Methods
-------

Here below are the methods provided that communicate with the engine.
The API they expose uses `pydantic <https://pydantic-docs.helpmanual.io/>`_
objects to help you pass in the correct arguments to the methods.


.. automodule:: avatars.runner
   :members:
   :undoc-members:
