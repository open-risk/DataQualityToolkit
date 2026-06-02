DataQualityToolkit
==================

DataQualityToolkit is a Python powered library for data quality analysis.

* Author: `Open Risk <http://www.openriskmanagement.com>`_
* License: Apache 2.0
* Mathematical Documentation: `Open Risk Manual <https://www.openriskmanual.org/wiki/Data_Quality>`_
* Development Website: `Github <https://github.com/open-risk/DataQualityToolkit>`_


Functionality
-------------

You can use DataQualityToolkit to

- Process Excel sheets, Wikitables and other tabular data
- Visualize DQ issues
- Characterise DQ issues

**NB: DataQualityToolkit is still in active development. If you encounter issues please raise them in our
GitHub repository**

Architecture
------------

TODO


Installation
=======================

You can install and use the DataQualityToolkit package in any system that supports the `Scipy ecosystem of tools <https://scipy.org/install.html>`_

Dependencies
-----------------

- numpy etc.

From PyPi
-------------

TODO

.. code:: bash

    pip3 install DQT

From sources
-------------

Download the sources to your preferred directory:

.. code:: bash

    git clone https://github.com/open-risk/DataQualityToolkit


Using virtualenv
----------------

It is advisable to install the package in a virtualenv so as not to interfere with your system's Python distribution

.. code:: bash

    virtualenv -p python3 tm_test
    source tm_test/bin/activate

If you do not have pandas already installed make sure you install it first (will also install numpy)

.. code:: bash

    pip3 install pandas
    pip3 install matplotlib
    pip3 install -r requirements.txt

Finally issue the install command and you are ready to go!

.. code:: bash

    python3 setup.py install

File structure
-----------------

The distribution has the following structure:

| DataQualityToolkit       The library source code
|    DQToolkit.py          Main data structures
| examples                 Usage examples
| docs                     Documentation
| datasets                 Contains a variety of datasets useful for getting started with DataQualityToolkit
| tests                    Testing suite (TODO)

Testing
----------------------

It is a good idea to run the test-suite. Before you get started:

- Adjust the source directory path in DataQualityToolkit/__init__ and then issue the following in at the root of the distribution
- Unzip the data files in the datasets directory

.. code:: bash

    python3 test.py

Getting Started
=======================

Check the Usage pages in this documentation

Look at the examples directory for a variety of typical workflows.


