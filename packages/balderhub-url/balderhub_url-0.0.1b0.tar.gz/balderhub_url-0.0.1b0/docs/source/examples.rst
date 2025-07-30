Examples
********

This section shows different examples how you can use the :class:`Url` object.

.. note::
    This package does not provide any scenario or setup classes at the moment. It is primarily used for working with
    :class:`Url` objects by other BalderHub projects.

The ``Url`` object
==================

You can use the :class:`Url` object to interact with any kind of urls.

.. code-block:: python

    >>> url = Url('https://balder.dev')
    >>> url.is_schema()
    False
    >>> url.get_query_parameters()
    {}
    >>> url2 = Url('https://balder.dev/example?q1=abc&q2=2')
    >>> url2.get_query_parameters()
    {'q1': 'abc', 'q2': '2'}

    >>> url.compare(url2)
    False
    >>> url.compare('https://balder.dev')
    True

Use it as schema
----------------

You can even define a url schema and apply different non-schemas on it:


.. code-block::

    >>> schema = Url('https://hub.balder.dev/projects/<str:proj_name>')

    >>> balderhub_url = Url('https://hub.balder.dev/projects/url')

    >>> schema.is_schema()
    True

    >>> str(schema.fill_parameters(proj_name='url'))
    'https://hub.balder.dev/projects/url'

    >>> balderhub_url.extract_parameters(by_using_schema_url=schema)
    {'proj_name': 'url'}

    >>> balderhub_url.compare(schema)
    Traceback (most recent call last):
      File "/snap/pycharm-professional/506/plugins/python-ce/helpers/pydev/pydevconsole.py", line 364, in runcode
        coro = func()
      File "<input>", line 1, in <module>
      File "/home/max/Documents/Development/gitlab.stahl-schmidt.de/Balder/balderhub/balderhub-url/src/balderhub/url/lib/utils/url.py", line 187, in compare
        raise ValueError('cannot compare urls because schemas are not allowed and at least one url is a schema')
    ValueError: cannot compare urls because schemas are not allowed and at least one url is a schema

>>> balderhub_url.compare(schema, allow_schemas=True)
    True

    >>> Url('https://balder.dev').compare(schema, allow_schemas=True)
    False
