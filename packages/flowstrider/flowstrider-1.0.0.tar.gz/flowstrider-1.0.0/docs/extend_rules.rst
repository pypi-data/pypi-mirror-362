Threat Catalogs
==============

Threat catalogs are collections of threats that can be checked against a data flow graph.
FlowStrider comes with two built-in threat catalogs: STRIDE and BSI.
Each threat catalog includes a set of threats along with descriptions, possible mitigations, and the conditions under which each threat applies.


STRIDE Catalog
--------------
The STRIDE threat catalog is a generic collection of threats that covers the areas of spoofing, tampering, repudiation, information disclosure, denial of service, and elevation of privileges.
For more information about STRIDE, refer to the book "Threat Modeling: Designing for Security" by Adam Shostack.

BSI Catalog
--------------------
The BSI catalog is based on standards issued by the German Federal Office for Information Security (BSI).
It contains a set of 13 representative threats.
Compared to the STRIDE catalog, this catalog is more specific and leverages security-relevant contextual information from the elements of the data flow graph.

How to Create Your Own Threat Catalog
-------------------------------------

This section explains how to add your own threat catalog to FlowStrider.
It contains information regarding the general architecture, where to place your files and how to register your threats so they can be used.
Each threat includes rules that define the conditions under which it applies.
Therefore, threat catalogs are also referred to as rule collections or rulesets in the following documentation.

General Architecture
~~~~~~~~~~~~~~~~~~~~

FlowStrider uses a modular rule system. Each ruleset (e.g., BSI, STRIDE) is implemented as a Python module containing:

 - Node rules
 - Edge rules
 - A rule collection class that groups these rules

All available rule collections are registered in `collections.py`, so FlowStrider knows which rulesets to use.

Adding Your Own Rules
~~~~~~~~~~~~~~~~~~~~~

1. **Create a New Rule Collection**

 Place your new ruleset in a new or existing folder under `flowstrider/rules/builtin/`

 Example: `flowstrider/rules/builtin/my_rules/my_rule_collection.py`

2. **Define Your Rules**

 To define your own rules, follow the established structure used in existing rulesets such as `bsi_rule_collection.py` or `kubernetes_rule_collection_test.py`. Each rule should be implemented as a class derived from either `NodeRule` or `EdgeRule`. The core logic of your rule belongs in a `_test` classmethod, while all human-readable texts and descriptions are set in a separate `init_texts` classmethod, which contains the following:

  - `display_name`: The name of the rule
  - `short_description`: A brief summary of the rule, describing the bad outcome
  - `long_description`: A detailed explanation of the rule
  - `mitigation_options`: A list of suggested mitigations
  - `requirement`: A string describing the requirement being checked
  - `attribute_names`: A list of strings with the attributes that are going to be needed to determine if there is a threat or not

 **General Structure of a Rule Class**

 The following example illustrates the typical structure of a rule class. Here the logic is encapsulated in the `_test` classmethod, which should return `True` if the rule is violated (i.e. if a finding should be reported). The syntax prefix `cls.` is used, to access class-level variables, which are set in `init_texts`:

   .. code-block:: python

      class MyExampleNodeRule(NodeRule):
          @classmethod
          def init_texts(cls):
              cls.display_name = "Example Rule"
              cls.short_description = "Node is not a STRIDE process." # Describes the unfavorable outcome
              cls.long_description = (
                  "This rule checks if a node carries the 'STRIDE:Process' tag. "
                  "Nodes representing processes should always be tagged accordingly to ensure correct threat modeling."
              )
              cls.mitigation_options = ["Add the 'STRIDE:Process' tag to the node."]
              cls.requirement = "'STRIDE:Process' tag must be set."
              cls.attribute_names = []

          @classmethod
          def _test(cls, node, dfd):
              is_stride_process = "STRIDE:Process" in node.tags
              return not is_stride_process  # Return True if the rule is violated

 The ``_test`` method receives the relevant object (node or edge) and the dataflow diagram. It is best practice to return a boolean expression that directly reflects the rule's intent, as shown above.

 Once the rules are defined, group them in a collection class derived from `DataflowDiagramRuleCollection`:

   .. code-block:: python

      class MyRuleCollection(DataflowDiagramRuleCollection):
          tags = {"my_rules"}

          @classmethod
          def init_texts(cls):
              _ = settings.lang_out.gettext
              cls.name = _("My rule collection")

          node_rules = [MyExampleNodeRule]
          edge_rules = []

      __all__ = ["MyRuleCollection"]

3. **Add an `__init__.py`**

 In your ruleset folder (e.g., `my_rules/...`) add an `__init__.py` file that imports your collection:

     .. code-block:: python

        from .my_rule_collection import MyRuleCollection
        __all__ = ["MyRuleCollection"]

4. **Register Your Rule Collection**

 Edit `flowstrider/rules/collections.py` and import your collection at the top:

     .. code-block:: python

        from .builtin.my_rules import MyRuleCollection

 Add your collection to the `all_collections` list:

     .. code-block:: python

        all_collections = [
            BSIRuleCollection,
            GenericSTRIDERuleCollection,
            MyRuleCollection,  # <-- New rule goes here
        ]

5. **Tag Your JSON Models**

 In your DFD JSON files, add the tag for your ruleset (e.g., `"my_rules"`) to the
 `"tags"` list at the bottom, this tells FlowStrider to apply your ruleset to this data
 flow diagram in the ``elicit`` calls.

     .. code-block:: json

        {
          "dfd": {
            "id": "Example",
            "_comment": "*rest of the JSON content*"
            "tags": [
              "stride",
              "my_rules"
            ],
            "attributes": {}
          }
        }

6. **Add Attributes (Optional)**

 All available attributes are centrally defined in `flowstrider/rules/attributes_dict.py` in the `attributes` dictionary and each entry specifies:

  - A short display name
  - A description
  - The entity types the attribute applies to (e.g., `"Node: DataStore"`, `"Edge: Dataflow"`)
  - The list of accepted values (if applicable)

 For example:

  .. code-block:: python

   attributes = {
       "handles_confidential_data": [
           _("Handles confidential data"),
           _("Whether the entity handles confidential data."),
           ["Node: DataStore", "Node: Process", "Edge: Dataflow"],
           [True, False],
       ],
       "encryption_method": [
           _("Encryption method"),
           _("Which method of encryption will be used to encrypt the data."),
           ["Node: DataStore"],
           ["AES_128", "AES_192", "AES_256"],
       ],
       # More attributes ...
   }

 To add a new attribute, add a new entry to the dictionary while following the same structure, but reuse existing attributes where possible. If your attribute is only relevant for a specific ruleset, you may also organize it in a separate file (e.g., `my_attributes.py`)

7. **Using Attributes in JSON Models**

 Attributes are set in the DFD JSON files under the `attributes` key for each node or edge. For example:

  .. code-block:: json

   "Node1": {
     "id": "Node1",
     "name": "Database",
     "tags": ["STRIDE:DataStore"],
     "attributes": {
       "handles_confidential_data": true,
       "encryption_method": "AES-256"
     }
   }

 (While this step can be done manually, in practice it's easier handled by using the tool functions ``metadata`` and ``update`` as seen in :ref:`readme-usage`)

8. **Accessing Attributes in Rules**

 Within the rule classes, attributes of elements can be accessed through the `attributes` dictionary of the node or edge. For example:

  .. code-block:: python

   class MyEncryptionRule(NodeRule):
       @classmethod
       def init_texts(cls):
           cls.display_name = "Example Rule"
           cls.short_description = "..."
           cls.long_description = "..."
           cls.mitigation_options = ["..."]
           cls.attribute_names = ["handles_confidential_data", "encryption_method"]
           cls.allowed_encryption = attributes_dict.attributes[cls.attribute_names[1]][3]
           cls.requirement = attributes_dict.attributes[cls.attribute_names[1]][0]
                                                        + _(": one of {")
                                                        + ", ".join(cls.allowed_encryption)
                                                        + "}"

       @classmethod
       def _test(cls, node, dfd):
           handles_confidential = node.attributes.get(cls.attribute_names[0], False) # With default = False
           encryption = node.attributes.get(cls.attribute_names[1], "") # With default = empty string
           uses_allowed_encryption = meet_any_requirement(encryption, cls.allowed_encryption)
           return handles_confidential and not uses_allowed_encryption
