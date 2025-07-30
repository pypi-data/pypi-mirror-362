==================
Project Management
==================

Problem definition
------------------
The objectives of the tool lie on modeling possible threats of a given system in the
context of storing, sending or managing data. It focuses on automated threat
elicitation and integratability in the CI/CD pipeline of a software engineering process.
For achieving this, the tool is firstly supposed to read given systems as data flow
diagrams (dfd). Next, it should allow easy access and modification of metadata of the
dfd in relation to security properties. Primarily, it should then elicit possible
threats based on the information given. Integrated in the CI/CD pipeline, security
concerns should be expressed to inform about possible security gaps. Furthermore, the
tool is supposed to offer mitigation options that can be taken to improve security.

Essential requirements of the software are:

- reading data flow diagrams
- eliciting basic threats in the dfd and displaying them in a clear fashion
- incorporation of a basic ruleset (BSI) that can be used for elicitation
- modification of the metadata
- offering mitigation options based on the threats found
- integration in CI/CD pipeline

This software is being developed in application class 1

Constraints
-----------
- the tool is to be completed by 2025-07-23
- the essential requirements have to be met by 2025-05-13 for the conference paper
- certain key differences in comparison to existing similar tools must be established
  to reason for the necessity of the tool
- compatibility with CI/CD pipelines is necessary

Architectural concepts
----------------------
.. code-block:: python

               ruleset
                  |
                  v
               +------+
   dfd/     -> | Tool | -> threat elicitation
   metadata    +------+

The tool is supposed to take on the description of a system as a data flow diagram (dfd)
together with metadata relevant for the threat elicitation. Furthermore, the tool should
take a ruleset on which the dfd is to be analyzed. As output, the tool should give
a status code for found threats, together with a description of them and options to
mitigate them.
