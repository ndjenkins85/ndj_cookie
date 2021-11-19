Modeling
========

.. contents::
    :local:
    :backlinks: none

Modeling is largely static code and suitable for most use cases.

The primary way to use this code is through a YAML configuration file to run model experiments.

You can optionally create additional model types in `model.py`, provided they output a list of features for further reporting.

See the `model.run_model_training` for a list of steps undertaken in processing.

ndj_pipeline.model
------------------
.. automodule:: ndj_pipeline.model
   :members:

ndj_pipeline.prep
-----------------
.. automodule:: ndj_pipeline.prep
   :members:
