DataQualityToolkit
==================
A Python toolkit for evaluating and visualizing the data quality of excel spreadsheets or other tabular data 

![Alt text](DQToolkit.png?raw=true "DQToolkit Visual")

Purpose of the project
======================

DataQualityToolkit is a Python powered library for the evaluation and visualization of the data 
quality of data provided in excel spreadsheets. 


General Info
=========================


Author: Open Risk, http://www.openriskmanagement.com

License: Apache 2.0

Documentation: Open Risk Manual, http://www.openriskmanual.org/wiki/Data_Quality

Training: Open Risk Academy, https://www.openriskacademy.com/login/index.php

Development website: https://github.com/open-risk/DataQualityToolkit

Production examples: https://www.opencpm.com


Functionality
=============

NB: The 0.2 release is (still) a heavily alpha version. 

You can use DataQualityToolkit to:
- Automatically produce validation reports and visualizations given an existing set validation rules
- Add to the validation rules
- There is an assumption that the spreadsheets are formatted in standard columnar format with all worksheet starting at the same header row
- There are many assumptions about the structure of wikitables (www source)

File structure
==============

* datasets/ Contains datasets useful for getting started with the DataQualityToolkit
* examples/ Contains examples
* DQToolkit.py Main objects

Usage
=====

Look at the examples directory on how to produce the visual include in this README file

Dependencies
============

-  DataQualityToolkit is written in Python and depends on numerical and data processing Python libraries (Numpy, Scipy, Pandas)
-  The Visualization API depends on Matplotlib
