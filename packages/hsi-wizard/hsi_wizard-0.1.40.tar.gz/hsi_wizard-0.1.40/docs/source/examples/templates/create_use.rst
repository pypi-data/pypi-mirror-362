.. _create:

Use and Create Template
=======================

This section demonstrates how to create and use templates in the `hsi-wizard` framework for processing a :class:`DataCube`. Templates help automate and reuse preprocessing workflows.

Create a Template
-----------------

The following example shows how to create a processing template. We generate synthetic image data, apply a sequence of transformations (like resizing and background removal), and save the recorded operations into a template file.

.. literalinclude:: ../../../../examples/03_templates/00_create_template.py
   :language: python
   :linenos:

The figure below shows the effect of preprocessing. The left image represents a slice of the data cube before processing, while the right image shows the same slice after applying the recorded operations.

.. figure:: ../../../../resources/imgs/create_template.png
   :align: center
   :alt: Creating a template from processed data
   :figclass: align-center
   :width: 80%

   Visualizing the preprocessing steps on synthetic data.

Use a Template
--------------

Once a template has been created, it can be applied to new data sets to ensure consistent preprocessing. The example below demonstrates how to load and apply a saved template to another :class:`DataCube`.

.. literalinclude:: ../../../../examples/03_templates/01_use_template.py
   :language: python
   :linenos:

The figure below shows the results of applying the template to a new data set.

.. figure:: ../../../../resources/imgs/use_template.png
   :align: center
   :alt: Applying a template to new data
   :figclass: align-center
   :width: 80%

   Applying a saved processing template for consistent analysis.

