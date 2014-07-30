eximhandler
===========

A simple logging handler class which sends an email using exim

It can be installed directly off github:

.. code-block:: console

    $ pip install git+git://github.com/danmichaelo/eximhandler.git

Usage
-------

.. code-block:: python

    import logging
    from eximhandler import EximHandler

    exim_handler = EximHandler('me@mydomain.com', 'Hello world')
    exim_handler.setLevel(logging.ERROR)

    logger = logging.getLogger()
    logger.addHandler(exim_handler)

