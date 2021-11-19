Data preparation
================

.. contents::
    :local:
    :backlinks: none

The following provides a reference guide to the data preparation steps.

It includes two python modules; data checks and transformations.

It is useful to separate these concerns, as once you have confidence in the schema, data typing, and consistency of data, you can confidently prepare feature engineering.

In addition, having feature engineering separate from the modeling step enhances the ability to create config generated model experimentation.

While there is some boilerplate code to help with logging and command line interface, functions created here are usually completely bespoke to the needs of the data analysis. The examples show the types of information to check, and required columns for config.

ndj_pipeline.data_checks
------------------------
.. automodule:: ndj_pipeline.data_checks
   :members:

ndj_pipeline.transform
----------------------
.. automodule:: ndj_pipeline.transform
   :members:
