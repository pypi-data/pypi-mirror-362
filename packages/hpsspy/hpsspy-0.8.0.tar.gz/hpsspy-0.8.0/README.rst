======
HPSSPy
======

|License| |PyPI| |Downloads| |Actions Status| |Coveralls Status| |Documentation Status|

.. |License| image:: https://img.shields.io/pypi/l/hpsspy.svg
    :target: https://pypi.python.org/pypi/hpsspy
    :alt: License

.. |PyPI| image:: https://img.shields.io/pypi/v/hpsspy.svg
    :target: https://pypi.python.org/pypi/hpsspy
    :alt: PyPI Badge

.. |Downloads| image:: https://img.shields.io/pypi/dm/hpsspy.svg
    :target: https://pypi.python.org/pypi/hpsspy
    :alt: PyPI Downloads

.. |Actions Status| image:: https://github.com/weaverba137/hpsspy/workflows/CI/badge.svg
    :target: https://github.com/weaverba137/hpsspy/actions
    :alt: GitHub Actions CI Status

.. |Coveralls Status| image:: https://coveralls.io/repos/github/weaverba137/hpsspy/badge.svg
    :target: https://coveralls.io/github/weaverba137/hpsspy
    :alt: Test Coverage Status

.. |Documentation Status| image:: https://readthedocs.org/projects/hpsspy/badge/
    :target: https://hpsspy.readthedocs.io/en/latest/
    :alt: Documentation Status

Overview
--------

HPSSPy is a Python_ package for interacting with the HPSS_ tape storage
system at NERSC_.  It is currently being developed on GitHub_.

.. _Python: https://www.python.org
.. _HPSS: https://www.nersc.gov/what-we-do/computing-for-science/data-resources/storage
.. _NERSC: https://www.nersc.gov
.. _GitHub: https://github.com/weaverba137/hpsspy

Requirements
------------

HPSSPy assumes that the HPSS utilities `hsi and htar`_ are installed.  As of
2023, these utilities are only available within the NERSC_ environment.

.. _`hsi and htar`: https://docs.nersc.gov/filesystems/archive/#common-commands

License
-------

HPSSPy is free software licensed under a 3-clause BSD-style license. For details see
the ``LICENSE.rst`` file.
