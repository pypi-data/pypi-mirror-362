Data Model
==========

As input for the **FlowStrider** tool, a data flow diagram of the software system under analysis is required. This diagram is described in a JSON file.
An example of how this file can be structured is provided in `test/resources`.

The core element is a data class called `DataflowDiagram`, which contains:

- **Nodes** represent processes, data stores, and external entities within the system
- **Edges** represent the data flows between these nodes
- **Clusters** define trust boundaries and group nodes accordingly

It is important to assign the correct type as a **tag** when creating nodes, edges, and clusters.
In addition, all three types (nodes, edges, and clusters) support a generic **attributes** dictionary that holds contextual information for each element.
The supported values for this contextual information are described in more detail further below under **Supported Context Attributes**.

The following section lists and explains the fields of these classes.


Dataflowdiagram
--------------------------------------

.. include:: _generated/dfd_class_table.rst

Node
--------------------------------------

.. include:: _generated/node_class_table.rst

Edge
--------------------------------------

.. include:: _generated/edge_class_table.rst

Cluster
--------------------------------------

.. include:: _generated/cluster_class_table.rst

Supported Context Information
--------------------------------------

.. include:: _generated/attributes_dict_table.rst
