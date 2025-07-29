Execute a CWL Workflow as DIRAC job
===================================

WMS allows to execute CWL (`Common Workflow Language`_) ``CommandLineTool`` and ``Workflow`` as DIRAC jobs.
Note that this feature is currently limited to DIRAC jobs only.

.. _Common Workflow Language: https://www.commonwl.org/user_guide/index.html

How to run a CWL Workflow
-------------------------

Write your CWL Workflow
^^^^^^^^^^^^^^^^^^^^^^^

1. Provide the CWL ``Workflow`` or ``CommandlineTool`` description as well as the steps definition and the CWL inputs as a YAML file.
2. Local files needed by the Workflow (input files and steps definitions) must be present and accessible locally when executing the Workflow with ``cwltool`` and also when creating the DIRAC Job (see below).
3. Validate the CWL using: ``cwltool --validate workflow.cwl inputs.yaml``.
4. Once the Workflow is **validated** and **tested** you can submit it through the CTADIRAC API.

Create the DIRAC jobs using the CTADIRAC API
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Import the CWLJob class from CTADIRAC.
2. Load your local CWL and input files using ``Path`` using relative paths.
3. Create the ``job`` object by initializing ``CWLJob`` with the CWL Workflow, the CWL input.
4. Set the base CVMFS path which will be used for Docker images.
5. Run ``job.submit()`` to run the DIRAC job.

.. code-block::

    from pathlib import Path
    from CTADIRAC.Interfaces.API.CWLJob import CWLJob

    cwl_workflow = Path("src/wms/tests/cwl/hello_world/container_example.cwl")
    cwl_inputs = Path("src/wms/tests/cwl/hello_world/container_example_inputs.yaml")
    cvmfs_path = Path("/cvmfs/ctao.dpps.test/")
    job = CWLJob(
        cwl_workflow=cwl_workflow, cwl_inputs=cwl_inputs, cvmfs_base_path=cvmfs_path
    )
    job.setName("test_hello")
    res = job.submit()
    job_id = res["Value"]


Note that you must first initiate a DIRAC proxy before being able to submit a job.

Input and output data
^^^^^^^^^^^^^^^^^^^^^

The CWL parser will automatically interpret local input files as DIRAC Input Sandbox and Workflow outputs as Output Sandbox.
By default the CWL Workflow description and the input YAML file are passed as Input Sandbox to DIRAC.
If the path is prepend by ``LFN://`` then the file is interpreted as a DIRAC Input or Output Data, meaning handle by the file catalog.

Note that only CWL inputs and outputs ``File`` type will be interpret as files.

Specify Docker hints
^^^^^^^^^^^^^^^^^^^^

To execute the Workflow with specific Apptainer/Docker images, one must use the CWL ``hints`` in the ``CommandLineTool`` description:

.. code-block::

    hints:
        DockerRequirement:
            dockerPull: harbor.cta-observatory.org/proxy_cache/library/python:3.12-slim

The ``dockerPull`` path will be appended to the CVMFS base path at CWLJob initialization.
The ``hints`` section will then disappear from the CWL given to DIRAC and will be replace by a proper ``baseCommand``.
The image must be present on CVMFS before hand and one can add a list of apptainer options using ``apptainer_options`` in CWL_job.

Note that the container will be executed using the ``apptainer`` binary.

Supported CWL Requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^

Currently you can use ``StepInputExpressionRequirement`` and ``InlineJavascriptRequirement``.
The use of ``ExpressionTool`` step and ``ScatterFeatureRequirement`` are not currently handled (coming soon).
