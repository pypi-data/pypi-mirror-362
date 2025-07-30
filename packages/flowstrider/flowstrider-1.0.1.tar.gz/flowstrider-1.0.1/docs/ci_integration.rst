CI/CD Integration
=================

Our tool **FlowStrider** can be easily integrated into a CI/CD pipeline.

You need to specify the location of your DFD (Data Flow Diagram) file.
In our case, we use a folder named `threat_models`, which contains both the DFD and the corresponding management file.
Additionally, we use the ``--fail-on-threat undecided`` option to ensure that the pipeline fails if any undecided threats are detected.

Below is a simple `.gitlab-ci.yml` configuration:

.. code-block:: yaml

    stages:
    - security

    default:
    before_script:
        - git config --global user.email "you@example.com"
        - git config --global user.name "Your Name"
        - pip install -U pip
        - apt-get update && apt-get install -y graphviz

    threat_modeling:
    stage: security
    image: python:3.10
    script:
        - pip install flowstrider
        - echo "Running threat modeling..."
        - flowstrider elicit --output off --management-path $CI_PROJECT_DIR/threat_models/threat_management.json --fail-on-threat undecided $CI_PROJECT_DIR/threat_models/example_tool_paper.json
    only:
        - main
        - merge_requests
    allow_failure: False
